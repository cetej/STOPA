#!/usr/bin/env python3
"""Managed Agents Service for STOPA.

Flask service on :9100 that manages Anthropic cloud agents.
Handles agent lifecycle, memory bridging, cost tracking, and scheduling.

Usage:
    python scripts/managed_agents.py

Config (env vars):
    ANTHROPIC_API_KEY   — Anthropic API key (required)
    TELEGRAM_BOT_TOKEN  — Telegram bot token (optional, for notifications)
    AGENTS_PORT         — Port to listen on (default: 9100)
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from flask import Flask, Response, jsonify, request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("managed-agents")

# ─── Paths ────────────────────────────────────────────────────────────────

STOPA_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = STOPA_ROOT / "scripts"
MEMORY_DIR = STOPA_ROOT / ".claude" / "memory"
CONFIG_PATH = SCRIPTS_DIR / "agents.json"
COSTS_PATH = SCRIPTS_DIR / "cloud-costs.json"
PORT = int(os.environ.get("AGENTS_PORT", "9100"))

BETA_HEADER = "managed-agents-2026-04-01"
API_BASE = "https://api.anthropic.com/v1"
API_VERSION = "2023-06-01"
STOPA_RESULT_PATTERN = re.compile(
    r"<!--\s*STOPA_RESULT\s*\n(.*?)\nSTOPA_RESULT\s*-->",
    re.DOTALL,
)


# ─── Config ───────────────────────────────────────────────────────────────


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ─── Agent Registry ──────────────────────────────────────────────────────


class APIClient:
    """Raw HTTP client for Anthropic Managed Agents API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
            "anthropic-beta": BETA_HEADER,
            "content-type": "application/json",
        })

    def post(self, path: str, data: dict) -> dict:
        resp = self.session.post(f"{API_BASE}{path}", json=data, timeout=30)
        if not resp.ok:
            log.error("API %s %s → %d: %s", "POST", path, resp.status_code, resp.text[:500])
        resp.raise_for_status()
        return resp.json()

    def get(self, path: str) -> dict:
        resp = self.session.get(f"{API_BASE}{path}", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def stream_sse(self, path: str):
        """Yield SSE events from a streaming endpoint."""
        resp = self.session.get(
            f"{API_BASE}{path}",
            stream=True,
            timeout=300,
            headers={**self.session.headers, "accept": "text/event-stream"},
        )
        resp.raise_for_status()
        event_type = None
        data_lines: list[str] = []

        for line in resp.iter_lines(decode_unicode=True):
            if line is None:
                continue
            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data_lines.append(line[5:].strip())
            elif line == "":
                if event_type and data_lines:
                    raw = "\n".join(data_lines)
                    try:
                        parsed = json.loads(raw)
                    except json.JSONDecodeError:
                        parsed = {"raw": raw}
                    yield {"event": event_type, "data": parsed}
                event_type = None
                data_lines = []


class AgentRegistry:
    """Manages Anthropic Managed Agents via raw HTTP API."""

    def __init__(self, client: APIClient):
        self.client = client

    def ensure_environment(self, cfg: dict) -> str:
        """Create cloud environment if not yet provisioned."""
        if cfg.get("environment_id"):
            return cfg["environment_id"]

        log.info("Creating cloud environment...")
        resp = self.client.post("/environments", {
            "name": "stopa-env",
        })
        env_id = resp["id"]
        cfg["environment_id"] = env_id
        save_config(cfg)
        log.info("Environment created: %s", env_id)
        return env_id

    def ensure_agent(self, cfg: dict, agent_def: dict) -> str:
        """Create or reuse an agent."""
        if agent_def.get("agent_id"):
            return agent_def["agent_id"]

        prompt_path = SCRIPTS_DIR / agent_def["prompt_file"]
        system_prompt = prompt_path.read_text(encoding="utf-8")

        log.info("Creating agent: %s", agent_def["name"])
        resp = self.client.post("/agents", {
            "name": agent_def["name"],
            "model": agent_def["model"],
            "system": system_prompt,
            "tools": [{"type": "agent_toolset_20260401"}],
            "description": agent_def.get("description", ""),
        })
        agent_def["agent_id"] = resp["id"]
        save_config(cfg)
        log.info("Agent created: %s → %s", agent_def["name"], resp["id"])
        return resp["id"]


# ─── Session Manager ─────────────────────────────────────────────────────


class SessionManager:
    """Creates sessions, sends messages, collects results via raw HTTP."""

    def __init__(self, client: APIClient):
        self.client = client

    def run_agent(
        self,
        agent_id: str,
        environment_id: str,
        user_message: str,
        agent_name: str,
    ) -> dict:
        """Run an agent session end-to-end. Returns parsed result."""
        log.info("Starting session for %s", agent_name)

        # Create session
        resp = self.client.post("/sessions", {
            "agent": agent_id,
            "environment_id": environment_id,
        })
        session_id = resp["id"]
        log.info("Session %s created for %s", session_id, agent_name)

        # Send user message
        self.client.post(f"/sessions/{session_id}/events", {
            "events": [{
                "type": "user.message",
                "content": [{"type": "text", "text": user_message}],
            }],
        })

        # Poll events until session goes idle
        full_output = self._poll_until_done(session_id)

        # Parse STOPA_RESULT
        result = self._parse_result(full_output)
        result["session_id"] = session_id
        result["agent_name"] = agent_name
        result["raw_output"] = full_output
        result["timestamp"] = datetime.now(timezone.utc).isoformat()

        return result

    def _poll_until_done(self, session_id: str) -> str:
        """Poll session status + events until idle. Returns full text output."""
        max_wait = 300  # 5 minutes
        poll_interval = 5  # seconds between polls
        start = time.time()

        # Wait for session to start running first
        saw_running = False
        while time.time() - start < max_wait:
            try:
                status_resp = self.client.get(f"/sessions/{session_id}")
                status = status_resp.get("status", "unknown")
            except Exception as e:
                log.warning("Status check failed: %s", e)
                time.sleep(poll_interval)
                continue

            if status == "running":
                saw_running = True
            elif status == "idle" and saw_running:
                log.info("Session %s idle after running — collecting output", session_id)
                break
            elif status == "idle" and not saw_running:
                # Session hasn't started yet, keep waiting
                pass
            elif status == "terminated":
                log.error("Session %s terminated", session_id)
                break

            log.info("Session %s status: %s (%.0fs elapsed)", session_id, status, time.time() - start)
            time.sleep(poll_interval)

        # Collect all agent message events
        output_parts: list[str] = []
        try:
            events_resp = self.client.get(f"/sessions/{session_id}/events")
            for event in events_resp.get("data", []):
                if event.get("type") == "agent.message":
                    for block in event.get("content", []):
                        if block.get("type") == "text":
                            output_parts.append(block["text"])
                elif event.get("type") == "agent.tool_use":
                    log.info("  tool: %s", event.get("name", "?"))
        except Exception as e:
            log.error("Events fetch failed: %s", e)

        return "".join(output_parts)

    def _parse_result(self, output: str) -> dict:
        """Extract STOPA_RESULT JSON from agent output."""
        match = STOPA_RESULT_PATTERN.search(output)
        if not match:
            log.warning("No STOPA_RESULT block found in output")
            return {"parsed": False, "error": "No STOPA_RESULT block"}

        try:
            data = json.loads(match.group(1))
            data["parsed"] = True
            return data
        except json.JSONDecodeError as e:
            log.error("Failed to parse STOPA_RESULT: %s", e)
            return {"parsed": False, "error": str(e)}


# ─── Memory Bridge ────────────────────────────────────────────────────────


class MemoryBridge:
    """Bidirectional sync between cloud agents and local STOPA memory."""

    ALLOWED_ACTIONS = {"append", "create", "upsert"}

    def prepare_context(self, agent_name: str) -> str:
        """Read local memory files and build context string for the agent."""
        context_parts: list[str] = []

        # Always include news.md tail for dedup
        news_path = MEMORY_DIR / "news.md"
        if news_path.exists():
            lines = news_path.read_text(encoding="utf-8").splitlines()
            tail = "\n".join(lines[-50:])
            context_parts.append(f"## Previous news.md (last 50 lines)\n\n{tail}")

        # Include critical patterns
        cp_path = MEMORY_DIR / "critical-patterns.md"
        if cp_path.exists():
            context_parts.append(
                f"## Critical Patterns\n\n{cp_path.read_text(encoding='utf-8')}"
            )

        return "\n\n---\n\n".join(context_parts)

    def apply_results(self, result: dict) -> list[str]:
        """Apply file operations from STOPA_RESULT to local memory."""
        if not result.get("parsed"):
            # Save raw output for manual review
            self._save_raw(result)
            return ["Saved raw output (no STOPA_RESULT)"]

        applied: list[str] = []
        for file_op in result.get("files", []):
            path = file_op.get("path", "")
            action = file_op.get("action", "")
            content = file_op.get("content", "")

            if not self._validate_path(path):
                log.warning("Rejected invalid path: %s", path)
                applied.append(f"REJECTED: {path} (invalid path)")
                continue

            if action not in self.ALLOWED_ACTIONS:
                log.warning("Rejected invalid action: %s", action)
                applied.append(f"REJECTED: {action} (invalid action)")
                continue

            target = STOPA_ROOT / ".claude" / path
            target.parent.mkdir(parents=True, exist_ok=True)

            if action == "append":
                with open(target, "a", encoding="utf-8") as f:
                    f.write("\n" + content)
                applied.append(f"APPEND: {path}")

            elif action == "create":
                if target.exists():
                    applied.append(f"SKIPPED: {path} (already exists)")
                else:
                    target.write_text(content, encoding="utf-8")
                    applied.append(f"CREATE: {path}")

            elif action == "upsert":
                target.write_text(content, encoding="utf-8")
                applied.append(f"UPSERT: {path}")

        return applied

    def _validate_path(self, path: str) -> bool:
        """Validate path is within memory directory, no traversal."""
        if not path:
            return False
        # Must start with memory/
        if not path.startswith("memory/"):
            return False
        # No parent directory traversal
        if ".." in path:
            return False
        # No absolute paths
        if path.startswith("/") or ":" in path:
            return False
        return True

    def _save_raw(self, result: dict) -> None:
        """Save raw output when STOPA_RESULT parsing fails."""
        raw_dir = MEMORY_DIR / "raw"
        raw_dir.mkdir(exist_ok=True)
        date = datetime.now().strftime("%Y-%m-%d")
        name = result.get("agent_name", "unknown")
        filename = f"{date}-cloud-{name}.md"
        (raw_dir / filename).write_text(
            result.get("raw_output", "No output"),
            encoding="utf-8",
        )


# ─── Cost Tracker ─────────────────────────────────────────────────────────


class CostTracker:
    """Track cloud agent costs."""

    # Sonnet 4.5 pricing (per 1M tokens)
    PRICING = {
        "claude-sonnet-4-5-20250514": {"input": 3.0, "output": 15.0},
        "claude-sonnet-4-6-20260401": {"input": 3.0, "output": 15.0},
    }
    DEFAULT_PRICING = {"input": 3.0, "output": 15.0}

    def __init__(self):
        self.costs = self._load()

    def _load(self) -> dict:
        if COSTS_PATH.exists():
            with open(COSTS_PATH, encoding="utf-8") as f:
                return json.load(f)
        return {"daily": {}, "monthly": {}, "all_time": {"total": 0.0}}

    def _save(self) -> None:
        with open(COSTS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.costs, f, indent=2)

    def record(self, agent_name: str, model: str, usage: dict) -> float:
        """Record usage and return cost in USD."""
        pricing = self.PRICING.get(model, self.DEFAULT_PRICING)
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        cost = (input_tokens / 1_000_000) * pricing["input"] + (
            output_tokens / 1_000_000
        ) * pricing["output"]

        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")

        # Daily
        if today not in self.costs["daily"]:
            self.costs["daily"][today] = {}
        self.costs["daily"][today][agent_name] = (
            self.costs["daily"][today].get(agent_name, 0) + cost
        )

        # Monthly
        if month not in self.costs["monthly"]:
            self.costs["monthly"][month] = {"total": 0.0, "by_agent": {}}
        self.costs["monthly"][month]["total"] += cost
        self.costs["monthly"][month]["by_agent"][agent_name] = (
            self.costs["monthly"][month]["by_agent"].get(agent_name, 0) + cost
        )

        # All time
        self.costs["all_time"]["total"] += cost

        self._save()

        # Append to budget.md
        self._append_budget(agent_name, cost, month)

        return cost

    def _append_budget(self, agent_name: str, cost: float, month: str) -> None:
        budget_path = MEMORY_DIR / "budget.md"
        if budget_path.exists():
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            mtd = self.costs["monthly"].get(month, {}).get("total", 0)
            entry = f"| {now} | cloud:{agent_name} | ${cost:.3f} | ${mtd:.2f} (cloud MTD) |\n"
            with open(budget_path, "a", encoding="utf-8") as f:
                f.write(entry)

    def check_limits(self, cfg: dict) -> dict[str, bool]:
        """Check if any cost limits are exceeded."""
        limits = cfg.get("cost_limits", {})
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")

        daily_total = sum(self.costs.get("daily", {}).get(today, {}).values())
        monthly_total = (
            self.costs.get("monthly", {}).get(month, {}).get("total", 0)
        )

        return {
            "daily_exceeded": daily_total >= limits.get("daily_usd", 999),
            "monthly_exceeded": monthly_total >= limits.get("monthly_usd", 999),
            "daily_total": daily_total,
            "monthly_total": monthly_total,
        }

    def get_summary(self) -> dict:
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        return {
            "today": self.costs.get("daily", {}).get(today, {}),
            "today_total": sum(
                self.costs.get("daily", {}).get(today, {}).values()
            ),
            "month": self.costs.get("monthly", {}).get(month, {}),
            "all_time": self.costs.get("all_time", {}),
        }


# ─── Telegram Notifier ────────────────────────────────────────────────────


class TelegramNotifier:
    """Send notifications via Telegram Bot API."""

    def __init__(self, token: str | None, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send(self, message: str) -> bool:
        if not self.token:
            log.info("Telegram disabled (no token), message: %s", message[:100])
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            resp = requests.post(
                url,
                json={"chat_id": self.chat_id, "text": message},
                timeout=10,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            log.error("Telegram send failed: %s", e)
            return False

    def send_notifications(self, result: dict) -> None:
        for notif in result.get("notifications", []):
            if notif.get("channel") == "telegram":
                self.send(notif["message"])


# ─── Run History ──────────────────────────────────────────────────────────


class RunHistory:
    """Track agent run history in agents.json."""

    MAX_RUNS = 100

    @staticmethod
    def record(cfg: dict, run_data: dict) -> None:
        runs = cfg.get("runs", [])
        runs.append(
            {
                "id": str(uuid.uuid4())[:8],
                "agent": run_data.get("agent_name", "unknown"),
                "timestamp": run_data.get("timestamp", ""),
                "session_id": run_data.get("session_id", ""),
                "parsed": run_data.get("parsed", False),
                "cost": run_data.get("cost", 0),
                "stats": run_data.get("stats", {}),
                "applied": run_data.get("applied", []),
            }
        )
        # Keep last N runs
        cfg["runs"] = runs[-RunHistory.MAX_RUNS :]
        save_config(cfg)


# ─── Orchestrator ─────────────────────────────────────────────────────────


class AgentOrchestrator:
    """Main orchestration logic — ties everything together."""

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            log.error("ANTHROPIC_API_KEY not set")
            sys.exit(1)

        self.client = APIClient(api_key)
        self.registry = AgentRegistry(self.client)
        self.sessions = SessionManager(self.client)
        self.memory = MemoryBridge()
        self.costs = CostTracker()

        cfg = load_config()
        tg_token = os.environ.get(cfg.get("telegram_bot_token_env", ""), "")
        tg_chat = cfg.get("telegram_chat_id", "")
        self.telegram = TelegramNotifier(tg_token or None, tg_chat)

        self.consecutive_failures: dict[str, int] = {}

    def run_agent(self, agent_name: str, user_input: str | None = None) -> dict:
        """Execute a single agent run."""
        cfg = load_config()

        # Find agent definition
        agent_def = None
        for a in cfg["agents"]:
            if a["name"] == agent_name:
                agent_def = a
                break

        if not agent_def:
            return {"error": f"Agent '{agent_name}' not found"}

        if not agent_def.get("enabled", False):
            return {"error": f"Agent '{agent_name}' is disabled"}

        # Check cost limits
        limits = self.costs.check_limits(cfg)
        if limits["daily_exceeded"]:
            msg = f"Daily cost limit exceeded (${limits['daily_total']:.2f})"
            self.telegram.send(f"BUDGET ALERT: {msg}")
            return {"error": msg}
        if limits["monthly_exceeded"]:
            msg = f"Monthly cost limit exceeded (${limits['monthly_total']:.2f})"
            self.telegram.send(f"BUDGET ALERT: {msg}")
            return {"error": msg}

        # Ensure infrastructure
        env_id = self.registry.ensure_environment(cfg)
        agent_id = self.registry.ensure_agent(cfg, agent_def)

        # Prepare context
        context = self.memory.prepare_context(agent_name)
        message = context
        if user_input:
            message = f"{context}\n\n---\n\n## User Request\n\n{user_input}"

        # Run
        try:
            result = self.sessions.run_agent(
                agent_id=agent_id,
                environment_id=env_id,
                user_message=message,
                agent_name=agent_name,
            )
        except Exception as e:
            log.error("Agent run failed: %s", e)
            self.consecutive_failures[agent_name] = (
                self.consecutive_failures.get(agent_name, 0) + 1
            )
            if self.consecutive_failures.get(agent_name, 0) >= 3:
                agent_def["enabled"] = False
                save_config(cfg)
                self.telegram.send(
                    f"AGENT DISABLED: {agent_name} — 3 consecutive failures"
                )
            return {"error": str(e)}

        # Reset failure counter on success
        self.consecutive_failures[agent_name] = 0

        # Apply memory updates
        applied = self.memory.apply_results(result)
        result["applied"] = applied

        # Track cost
        usage = result.get("usage", {})
        cost = self.costs.record(agent_name, agent_def["model"], usage)
        result["cost"] = cost

        # Send notifications
        self.telegram.send_notifications(result)

        # Record run
        RunHistory.record(cfg, result)

        log.info(
            "Agent %s completed: parsed=%s, cost=$%.4f, files=%s",
            agent_name,
            result.get("parsed"),
            cost,
            applied,
        )

        return {
            "success": True,
            "agent": agent_name,
            "parsed": result.get("parsed", False),
            "cost": cost,
            "stats": result.get("stats", {}),
            "applied": applied,
            "session_id": result.get("session_id"),
        }


# ─── Flask App ────────────────────────────────────────────────────────────

app = Flask(__name__)
orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    global orchestrator
    if orchestrator is None:
        orchestrator = AgentOrchestrator()
    return orchestrator


@app.route("/health")
def health():
    return jsonify({"status": "ok", "port": PORT, "stopa_root": str(STOPA_ROOT)})


@app.route("/api/agents")
def list_agents():
    cfg = load_config()
    agents = []
    for a in cfg["agents"]:
        # Find last run
        last_run = None
        for r in reversed(cfg.get("runs", [])):
            if r["agent"] == a["name"]:
                last_run = r
                break

        agents.append(
            {
                "name": a["name"],
                "model": a["model"],
                "schedule": a.get("schedule"),
                "enabled": a.get("enabled", False),
                "description": a.get("description", ""),
                "agent_id": a.get("agent_id"),
                "last_run": last_run,
            }
        )
    return jsonify(agents)


@app.route("/api/agents/<name>")
def get_agent(name: str):
    cfg = load_config()
    agent_def = None
    for a in cfg["agents"]:
        if a["name"] == name:
            agent_def = a
            break

    if not agent_def:
        return jsonify({"error": "Not found"}), 404

    runs = [r for r in cfg.get("runs", []) if r["agent"] == name][-10:]
    return jsonify({"agent": agent_def, "runs": runs})


@app.route("/api/agents/<name>/run", methods=["POST"])
def run_agent(name: str):
    data = request.get_json(silent=True) or {}
    user_input = data.get("input")

    try:
        orch = get_orchestrator()
        result = orch.run_agent(name, user_input)
        return jsonify(result)
    except Exception as e:
        log.error("Run agent error: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/agents/<name>/runs")
def list_runs(name: str):
    cfg = load_config()
    runs = [r for r in cfg.get("runs", []) if r["agent"] == name]
    return jsonify(runs[-20:])


@app.route("/api/agents/<name>/toggle", methods=["POST"])
def toggle_agent(name: str):
    cfg = load_config()
    for a in cfg["agents"]:
        if a["name"] == name:
            a["enabled"] = not a.get("enabled", False)
            save_config(cfg)
            return jsonify({"name": name, "enabled": a["enabled"]})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/costs")
def get_costs():
    tracker = CostTracker()
    return jsonify(tracker.get_summary())


# ─── Simple Cron Scheduler (no external deps) ────────────────────────────


class SimpleCronScheduler:
    """Lightweight cron scheduler using threading. Checks every 60s."""

    def __init__(self):
        self._running = False
        self._thread: threading.Thread | None = None
        self._last_fired: dict[str, str] = {}  # agent_name → "YYYY-MM-DD HH:MM"

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        log.info("Cron scheduler started")

    def stop(self) -> None:
        self._running = False

    def _loop(self) -> None:
        while self._running:
            try:
                self._tick()
            except Exception as e:
                log.error("Scheduler tick error: %s", e)
            time.sleep(60)

    def _tick(self) -> None:
        now = datetime.now()
        now_key = now.strftime("%Y-%m-%d %H:%M")
        cfg = load_config()

        for agent_def in cfg["agents"]:
            cron_expr = agent_def.get("schedule")
            if not cron_expr or not agent_def.get("enabled", False):
                continue

            name = agent_def["name"]
            if self._last_fired.get(name) == now_key:
                continue

            if self._cron_matches(cron_expr, now):
                self._last_fired[name] = now_key
                log.info("Cron triggered: %s", name)
                threading.Thread(
                    target=self._run_agent, args=(name,), daemon=True
                ).start()

    @staticmethod
    def _cron_matches(expr: str, dt: datetime) -> bool:
        """Check if a 5-field cron expression matches the given datetime."""
        parts = expr.split()
        if len(parts) != 5:
            return False

        minute, hour, dom, month, dow = parts

        def matches_field(field: str, value: int, max_val: int) -> bool:
            if field == "*":
                return True
            for part in field.split(","):
                if "/" in part:
                    base, step = part.split("/")
                    start = 0 if base == "*" else int(base)
                    if (value - start) % int(step) == 0 and value >= start:
                        return True
                elif "-" in part:
                    lo, hi = part.split("-")
                    if int(lo) <= value <= int(hi):
                        return True
                elif int(part) == value:
                    return True
            return False

        return (
            matches_field(minute, dt.minute, 59)
            and matches_field(hour, dt.hour, 23)
            and matches_field(dom, dt.day, 31)
            and matches_field(month, dt.month, 12)
            and matches_field(dow, dt.weekday(), 6)  # 0=Mon
        )

    @staticmethod
    def _run_agent(agent_name: str) -> None:
        try:
            orch = get_orchestrator()
            result = orch.run_agent(agent_name)
            log.info("Scheduled run result for %s: %s", agent_name, result)
        except Exception as e:
            log.error("Scheduled run failed for %s: %s", agent_name, e)


# ─── Main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Managed Agents Service on :%d", PORT)
    log.info("STOPA root: %s", STOPA_ROOT)
    log.info("Config: %s", CONFIG_PATH)

    # Verify API key exists
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set — exiting")
        sys.exit(1)

    # Start scheduler
    scheduler = SimpleCronScheduler()
    scheduler.start()

    cfg = load_config()
    for a in cfg["agents"]:
        if a.get("schedule") and a.get("enabled"):
            log.info("Scheduled %s: %s", a["name"], a["schedule"])

    # Start Flask
    try:
        app.run(host="127.0.0.1", port=PORT, debug=False, threaded=True)
    finally:
        scheduler.stop()

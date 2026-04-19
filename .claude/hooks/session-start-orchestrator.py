#!/usr/bin/env python3
"""SessionStart orchestrator — runs 14 sub-hooks in parallel instead of sequentially.

Reduces startup latency from ~20s sequential to ~5s (bottleneck = slowest hook).
Each sub-hook gets the same stdin, timeouts are respected individually, failures are logged.
"""
from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HOOKS_DIR = Path(__file__).resolve().parent
LOG_PATH = HOOKS_DIR.parent / "memory" / "session-start-perf.jsonl"

# Declarative sub-hook registry. Each entry runs in parallel (IO-bound).
# Timeouts are generous because Windows subprocess spawn + antivirus can cost 500ms-1s each.
# Wall time is bounded by the slowest hook, not the sum — so large individual budgets are cheap.
SUB_HOOKS: list[dict] = [
    {"name": "ensure-shared-dir",       "cmd": ["bash", str(HOOKS_DIR / "ensure-shared-dir.sh")],       "timeout": 10},
    {"name": "checkpoint-check",        "cmd": ["bash", str(HOOKS_DIR / "checkpoint-check.sh")],        "timeout": 12},
    {"name": "pending-reminders",       "cmd": ["bash", str(HOOKS_DIR / "pending-reminders.sh")],       "timeout": 10},
    {"name": "memory-maintenance",      "cmd": ["bash", str(HOOKS_DIR / "memory-maintenance.sh")],      "timeout": 12},
    {"name": "auto-scribe",             "cmd": ["python", str(HOOKS_DIR / "auto-scribe.py")],           "timeout": 20},
    {"name": "memory-brief",            "cmd": ["bash", str(HOOKS_DIR / "memory-brief.sh")],            "timeout": 12},
    {"name": "context-inject",          "cmd": ["python", str(HOOKS_DIR / "context-inject.py")],        "timeout": 15},
    {"name": "verify-sweep",            "cmd": ["python", str(HOOKS_DIR / "verify-sweep.py")],          "timeout": 15},
    {"name": "improvement-funnel",      "cmd": ["bash", str(HOOKS_DIR / "improvement-funnel.sh")],      "timeout": 15},
    {"name": "evolve-trigger",          "cmd": ["bash", str(HOOKS_DIR / "evolve-trigger.sh")],          "timeout": 12},
    {"name": "learning-lifecycle",      "cmd": ["python", str(HOOKS_DIR / "learning-lifecycle.py")],    "timeout": 10},
    {"name": "pulse-generator",         "cmd": ["python", str(HOOKS_DIR / "pulse-generator.py")],       "timeout": 12},
    {"name": "build-permission-registry","cmd": ["python", str(HOOKS_DIR / "build-permission-registry.py")], "timeout": 12},
    {"name": "improvement-notify",      "cmd": ["bash", str(HOOKS_DIR / "improvement-notify.sh")],      "timeout": 12},
    {"name": "autonomy-digest",         "cmd": ["python", str(HOOKS_DIR / "autonomy-digest.py")],      "timeout": 8},
]


def run_hook(hook: dict, stdin_data: str) -> dict:
    """Run one sub-hook with its own timeout; return result dict (never raises)."""
    name = hook["name"]
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            hook["cmd"],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=hook["timeout"],
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.perf_counter() - start
        return {
            "name": name,
            "rc": proc.returncode,
            "elapsed_s": round(elapsed, 3),
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "status": "ok" if proc.returncode == 0 else "nonzero",
        }
    except subprocess.TimeoutExpired:
        return {
            "name": name,
            "rc": -1,
            "elapsed_s": hook["timeout"],
            "stdout": "",
            "stderr": f"timeout after {hook['timeout']}s",
            "status": "timeout",
        }
    except Exception as exc:
        return {
            "name": name,
            "rc": -2,
            "elapsed_s": round(time.perf_counter() - start, 3),
            "stdout": "",
            "stderr": f"exception: {exc!r}",
            "status": "error",
        }


def main() -> int:
    # Buffer stdin once — CC sends session_id/hook_event_name JSON here.
    try:
        stdin_data = sys.stdin.read() or "{}"
    except Exception:
        stdin_data = "{}"

    wall_start = time.perf_counter()

    # Fan out. max_workers = len(hooks) because they're IO-bound (mostly subprocess + file IO).
    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SUB_HOOKS)) as pool:
        futures = {pool.submit(run_hook, h, stdin_data): h["name"] for h in SUB_HOOKS}
        for fut in concurrent.futures.as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as exc:
                results.append({"name": futures[fut], "status": "pool-error", "stderr": repr(exc)})

    total_wall = round(time.perf_counter() - wall_start, 3)

    # Aggregate stdout — preserve order by declared list (not completion order) for stable output.
    order = {h["name"]: i for i, h in enumerate(SUB_HOOKS)}
    results.sort(key=lambda r: order.get(r["name"], 999))

    parts: list[str] = []
    for r in results:
        out = (r.get("stdout") or "").rstrip()
        if out:
            parts.append(out)
        # Surface only real failures (timeouts, exceptions). Nonzero exit without stderr
        # is a common "nothing to do" signal from bash hooks — don't clutter the banner.
        if r.get("status") in ("timeout", "error", "pool-error"):
            err = (r.get("stderr") or "").strip()[:200]
            parts.append(f"[hook:{r['name']}:{r['status']}] {err}" if err else f"[hook:{r['name']}:{r['status']}]")

    if parts:
        print("\n".join(parts))

    # Perf log (JSONL, one line per session-start run) — for tracking real latency over time.
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        perf = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_wall_s": total_wall,
            "hooks": [
                {"name": r["name"], "elapsed_s": r.get("elapsed_s"), "status": r.get("status")}
                for r in results
            ],
        }
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(perf, ensure_ascii=False) + "\n")
    except Exception:
        pass  # never block session start on logging failure

    return 0


if __name__ == "__main__":
    sys.exit(main())

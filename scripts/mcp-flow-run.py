#!/usr/bin/env python3
"""mcp-flow-run — execute declarative MCP cross-tool flows.

Loads a YAML flow definition, validates inputs, then iterates steps invoking
the declared MCP tools (option b: native stdio MCP via `mcp` SDK). Mirrors the
runtime semantics described in `.claude/skills/mcp-flow/SKILL.md`.

Usage:
    python scripts/mcp-flow-run.py <flow-name> [key=value ...]
    python scripts/mcp-flow-run.py pr-merged repo=cetej/STOPA pr=42
    python scripts/mcp-flow-run.py pr-merged repo=cetej/STOPA pr=42 --dry-run
    python scripts/mcp-flow-run.py pr-merged ... --start-at notify
    python scripts/mcp-flow-run.py pr-merged ... --verbose

Search order for flow files:
    1. .claude/skills/mcp-flow/flows/<name>.yaml         (shipped)
    2. .claude/memory/intermediate/mcp-flows/<name>.yaml (local, gitignored)

Server resolution order (first match wins):
    1. ~/.claude.json                projects[<repo>].mcpServers
    2. ~/.claude.json                mcpServers (user-global)
    3. claude_desktop_config.json    mcpServers

Tools whose server cannot be resolved (CC plugins, cowork integrations) cause
the step to fail with a clear error; flow continues per the step's on_error
policy. Use --dry-run to validate the YAML and unresolved-server set without
executing anything.

Exit codes:
    0  flow completed (status=completed or partial-but-tolerated)
    1  flow aborted (required input missing, abort step failed, etc.)
    2  configuration error (flow not found, YAML invalid)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_FLOWS_DIR = REPO_ROOT / ".claude" / "skills" / "mcp-flow" / "flows"
LOCAL_FLOWS_DIR = REPO_ROOT / ".claude" / "memory" / "intermediate" / "mcp-flows"
AUDIT_LOG_DIR = REPO_ROOT / ".claude" / "memory" / "intermediate" / "mcp-flow-runs"

CLAUDE_JSON = Path.home() / ".claude.json"
CLAUDE_DESKTOP_CONFIG = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"

TEMPLATE_RE = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")


# --------------------------------------------------------------------------- #
# Flow loading + validation                                                   #
# --------------------------------------------------------------------------- #

@dataclass
class Flow:
    name: str
    path: Path
    raw: dict[str, Any]
    inputs_schema: dict[str, dict[str, Any]] = field(default_factory=dict)
    steps: list[dict[str, Any]] = field(default_factory=list)
    dual_write: bool = False
    budget_cap: float | None = None


def find_flow(name: str) -> Path | None:
    for base in (SHIPPED_FLOWS_DIR, LOCAL_FLOWS_DIR):
        candidate = base / f"{name}.yaml"
        if candidate.exists():
            return candidate
    return None


def list_flows() -> list[str]:
    out: list[str] = []
    for base in (SHIPPED_FLOWS_DIR, LOCAL_FLOWS_DIR):
        if base.exists():
            out.extend(sorted(p.stem for p in base.glob("*.yaml")))
    return sorted(set(out))


def load_flow(name: str) -> Flow:
    path = find_flow(name)
    if path is None:
        available = list_flows()
        raise SystemExit(
            f"ERROR: Flow '{name}' not found.\n"
            f"Available: {', '.join(available) if available else '(none)'}\n"
            f"Create new flow at:\n"
            f"  shipped: {SHIPPED_FLOWS_DIR / f'{name}.yaml'}\n"
            f"  local:   {LOCAL_FLOWS_DIR / f'{name}.yaml'}"
        )
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SystemExit(f"ERROR: Failed to parse {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise SystemExit(f"ERROR: Flow {path} must be a YAML mapping at top level.")

    steps = raw.get("steps") or []
    if not isinstance(steps, list) or not steps:
        raise SystemExit(f"ERROR: Flow {path} has no steps.")

    seen_ids: set[str] = set()
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            raise SystemExit(f"ERROR: step #{i} in {path} is not a mapping.")
        sid = step.get("id")
        tool = step.get("tool")
        if not sid or not tool:
            raise SystemExit(f"ERROR: step #{i} in {path} missing 'id' or 'tool'.")
        if sid in seen_ids:
            raise SystemExit(f"ERROR: duplicate step id '{sid}' in {path}.")
        seen_ids.add(sid)
        on_error = step.get("on_error", "abort")
        if on_error not in {"abort", "continue", "retry"}:
            raise SystemExit(
                f"ERROR: step '{sid}' on_error='{on_error}' invalid "
                f"(must be abort|continue|retry)."
            )

    return Flow(
        name=raw.get("name", name),
        path=path,
        raw=raw,
        inputs_schema=raw.get("inputs") or {},
        steps=steps,
        dual_write=bool(raw.get("dual_write", False)),
        budget_cap=raw.get("budget_cap"),
    )


def parse_cli_inputs(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in pairs:
        if "=" not in raw:
            raise SystemExit(f"ERROR: input '{raw}' is not key=value.")
        k, v = raw.split("=", 1)
        out[k.strip()] = v
    return out


def resolve_inputs(
    schema: dict[str, dict[str, Any]],
    cli_inputs: dict[str, str],
) -> dict[str, str]:
    """Validate required + apply defaults. Defaults pre-render env vars."""
    resolved: dict[str, str] = {}
    for key, spec in schema.items():
        spec = spec or {}
        required = bool(spec.get("required", False))
        default = spec.get("default")
        if key in cli_inputs:
            resolved[key] = cli_inputs[key]
            continue
        if default is not None:
            # Pre-render env vars at input level; step-time render covers
            # nested {{inputs.X}} references that may chain into defaults.
            resolved[key] = render_template(str(default), {"inputs": {}, "env": dict(os.environ)})
            continue
        if required:
            raise SystemExit(
                f"ERROR: Flow requires input '{key}'. Provide via `{key}=value`."
            )
        resolved[key] = ""

    # Allow extra CLI inputs (forward-compat) but warn.
    for k, v in cli_inputs.items():
        if k not in resolved:
            resolved[k] = v
    return resolved


# --------------------------------------------------------------------------- #
# Template engine: {{inputs.X}}, {{step_<id>.output.Y}}, {{env.VAR}}, filters #
# --------------------------------------------------------------------------- #

def _filter_split(value: Any, arg: str | None) -> list[str]:
    sep = arg if arg else ","
    return str(value).split(sep)


def _filter_first(value: Any, _arg: str | None) -> Any:
    if isinstance(value, (list, tuple, str)) and len(value) > 0:
        return value[0]
    return ""


def _filter_last(value: Any, _arg: str | None) -> Any:
    if isinstance(value, (list, tuple, str)) and len(value) > 0:
        return value[-1]
    return ""


def _filter_lower(value: Any, _arg: str | None) -> str:
    return str(value).lower()


def _filter_upper(value: Any, _arg: str | None) -> str:
    return str(value).upper()


def _filter_default(value: Any, arg: str | None) -> Any:
    if value is None or value == "":
        return arg if arg is not None else ""
    return value


def _filter_truncate(value: Any, arg: str | None) -> str:
    n = int(arg) if arg else 80
    s = str(value)
    return s if len(s) <= n else s[:n] + "..."


def _filter_json(value: Any, _arg: str | None) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return str(value)


FILTERS = {
    "split": _filter_split,
    "first": _filter_first,
    "last": _filter_last,
    "lower": _filter_lower,
    "upper": _filter_upper,
    "default": _filter_default,
    "truncate": _filter_truncate,
    "json": _filter_json,
}


def _resolve_path(expr: str, ctx: dict[str, Any]) -> Any:
    """Walk dotted path in ctx. Returns '' on any miss (safe substitution)."""
    parts = expr.split(".")
    cur: Any = ctx
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list):
            try:
                cur = cur[int(p)]
            except (ValueError, IndexError):
                return ""
        else:
            return ""
    return cur


def _apply_filter_chain(value: Any, chain: list[str]) -> Any:
    cur = value
    for token in chain:
        token = token.strip()
        if not token:
            continue
        if ":" in token:
            name, arg = token.split(":", 1)
            name, arg = name.strip(), arg.strip()
        else:
            name, arg = token, None
        fn = FILTERS.get(name)
        if fn is None:
            raise ValueError(f"unknown filter: {name}")
        cur = fn(cur, arg)
    return cur


def _render_one(expr: str, ctx: dict[str, Any]) -> Any:
    parts = [p.strip() for p in expr.split("|")]
    head, filters = parts[0], parts[1:]
    value = _resolve_path(head, ctx)
    return _apply_filter_chain(value, filters) if filters else value


def render_template(text: str, ctx: dict[str, Any]) -> str:
    def sub(m: re.Match[str]) -> str:
        try:
            value = _render_one(m.group(1), ctx)
        except ValueError as exc:
            raise SystemExit(f"ERROR: template '{m.group(0)}' failed: {exc}") from exc
        if value is None:
            return ""
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, default=str)
        return str(value)

    return TEMPLATE_RE.sub(sub, text)


def render_args(value: Any, ctx: dict[str, Any]) -> Any:
    """Recursively render strings inside dict/list/str args."""
    if isinstance(value, str):
        return render_template(value, ctx)
    if isinstance(value, dict):
        return {k: render_args(v, ctx) for k, v in value.items()}
    if isinstance(value, list):
        return [render_args(v, ctx) for v in value]
    return value


def evaluate_skip_if(expr: str, ctx: dict[str, Any]) -> bool:
    """Tiny expression engine: '<rendered> == <rendered>' or '<r> != <r>'.

    Anything unparseable is treated as False (don't skip) — fail-open.
    """
    rendered = render_template(expr, ctx).strip()
    for op in ("==", "!="):
        if op in rendered:
            left, right = (s.strip().strip("'\"") for s in rendered.split(op, 1))
            return (left == right) if op == "==" else (left != right)
    return bool(rendered) and rendered.lower() not in {"false", "0", ""}


# --------------------------------------------------------------------------- #
# MCP server registry + invocation                                            #
# --------------------------------------------------------------------------- #

def parse_tool_name(tool: str) -> tuple[str, str]:
    if not tool.startswith("mcp__"):
        raise ValueError(f"tool '{tool}' must start with 'mcp__'")
    rest = tool[len("mcp__"):]
    if "__" not in rest:
        raise ValueError(f"tool '{tool}' missing __<tool> suffix")
    server, tool_name = rest.split("__", 1)
    return server, tool_name


def load_server_registry(cwd: Path) -> dict[str, dict[str, Any]]:
    """Aggregate server defs from project-level + user-level + claude desktop."""
    registry: dict[str, dict[str, Any]] = {}

    def absorb(servers: dict[str, Any] | None) -> None:
        if not servers:
            return
        for name, cfg in servers.items():
            if name not in registry and isinstance(cfg, dict):
                registry[name] = cfg

    def _norm(p: str) -> str:
        # `.claude.json` keys use forward slashes regardless of OS;
        # pathlib on Windows yields backslashes. Normalize both sides.
        return p.replace("\\", "/").rstrip("/").lower()

    # Project-level (highest priority)
    if CLAUDE_JSON.exists():
        try:
            data = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        projs = data.get("projects") or {}
        # Multiple keys can normalize to the same path (e.g. forward + back
        # slash duplicates), and only some carry mcpServers. Accumulate all
        # matches on the first parent that has any non-empty registry.
        candidates = [cwd, *cwd.parents]
        for cand in candidates:
            target = _norm(str(cand))
            matches = [projs[k] for k in projs if _norm(k) == target]
            absorbed_any = False
            for m in matches:
                ms = m.get("mcpServers") or {}
                if ms:
                    absorb(ms)
                    absorbed_any = True
            if absorbed_any:
                break
        absorb(data.get("mcpServers"))

    # Claude Desktop config (lowest priority — covers github, brave-search, etc.)
    if CLAUDE_DESKTOP_CONFIG.exists():
        try:
            data = json.loads(CLAUDE_DESKTOP_CONFIG.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        absorb(data.get("mcpServers"))

    return registry


async def call_mcp_tool(
    server_cfg: dict[str, Any],
    tool_name: str,
    arguments: dict[str, Any],
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Spawn stdio MCP server, call tool, return structured result."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    # Inherit ambient env (PATH, system vars), overlay server-specific env.
    env = dict(os.environ)
    env.update(server_cfg.get("env") or {})

    params = StdioServerParameters(
        command=server_cfg["command"],
        args=list(server_cfg.get("args") or []),
        env=env,
        cwd=server_cfg.get("cwd"),
    )

    async with AsyncExitStack() as stack:
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await asyncio.wait_for(session.initialize(), timeout=timeout)
        result = await asyncio.wait_for(
            session.call_tool(tool_name, arguments), timeout=timeout
        )

    # CallToolResult: .content (list of TextContent/ImageContent), .isError
    text_chunks: list[str] = []
    structured: Any = None
    for item in result.content or []:
        if hasattr(item, "text") and item.text:
            text_chunks.append(item.text)
    text_blob = "\n".join(text_chunks).strip()

    # Try parsing as JSON for downstream `{{step.output.X}}` access.
    if text_blob:
        try:
            structured = json.loads(text_blob)
        except json.JSONDecodeError:
            structured = text_blob

    return {
        "is_error": bool(getattr(result, "isError", False)),
        "output": structured if structured is not None else text_blob,
        "raw_text": text_blob,
    }


# --------------------------------------------------------------------------- #
# Step executor                                                               #
# --------------------------------------------------------------------------- #

@dataclass
class StepResult:
    step_id: str
    tool: str
    status: str  # ok | failed | skipped | dry-run
    output: Any = None
    error: str | None = None
    duration_ms: int = 0
    args_rendered: dict[str, Any] = field(default_factory=dict)
    redacted: bool = False


def _redact_args(args: dict[str, Any]) -> dict[str, Any]:
    """Shallow redaction: replace string values with placeholder."""
    return {k: ("<redacted>" if isinstance(v, str) else v) for k, v in args.items()}


async def run_step(
    step: dict[str, Any],
    ctx: dict[str, Any],
    registry: dict[str, dict[str, Any]],
    *,
    dry_run: bool,
    verbose: bool,
) -> StepResult:
    sid = step["id"]
    tool = step["tool"]
    args = step.get("args") or {}
    on_error = step.get("on_error", "abort")
    redact = bool(step.get("redact", False))

    # skip_if evaluation BEFORE rendering args (skip should not require valid args).
    skip_expr = step.get("skip_if")
    if skip_expr and evaluate_skip_if(str(skip_expr), ctx):
        if verbose:
            print(f"  [skip] {sid}: skip_if matched ({skip_expr})", file=sys.stderr)
        return StepResult(step_id=sid, tool=tool, status="skipped", output=None)

    rendered_args = render_args(args, ctx)
    log_args = _redact_args(rendered_args) if redact else rendered_args

    if verbose:
        print(f"  [step] {sid} → {tool}", file=sys.stderr)
        print(f"         args: {json.dumps(log_args, ensure_ascii=False, default=str)[:300]}",
              file=sys.stderr)

    if dry_run:
        return StepResult(
            step_id=sid, tool=tool, status="dry-run",
            output=None, args_rendered=log_args, redacted=redact,
        )

    try:
        server_name, tool_short = parse_tool_name(tool)
    except ValueError as exc:
        return StepResult(
            step_id=sid, tool=tool, status="failed",
            error=str(exc), args_rendered=log_args, redacted=redact,
        )

    server_cfg = registry.get(server_name)
    if server_cfg is None:
        return StepResult(
            step_id=sid, tool=tool, status="failed",
            error=(
                f"server '{server_name}' not found in registry. "
                f"Plugin/cowork servers are not auto-discoverable; configure under "
                f"~/.claude.json projects[{REPO_ROOT}].mcpServers or "
                f"claude_desktop_config.json mcpServers."
            ),
            args_rendered=log_args, redacted=redact,
        )

    attempts = 2 if on_error == "retry" else 1
    last_error: str | None = None
    start = time.monotonic()
    for attempt in range(1, attempts + 1):
        try:
            result = await call_mcp_tool(server_cfg, tool_short, rendered_args)
            duration_ms = int((time.monotonic() - start) * 1000)
            if result["is_error"]:
                last_error = f"tool returned isError=true: {result['raw_text'][:200]}"
                if attempt < attempts:
                    await asyncio.sleep(5)
                    continue
                return StepResult(
                    step_id=sid, tool=tool, status="failed",
                    error=last_error, output=result["output"],
                    duration_ms=duration_ms, args_rendered=log_args, redacted=redact,
                )
            return StepResult(
                step_id=sid, tool=tool, status="ok",
                output=result["output"], duration_ms=duration_ms,
                args_rendered=log_args, redacted=redact,
            )
        except Exception as exc:  # noqa: BLE001 — surface any MCP/transport error
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < attempts:
                if verbose:
                    print(f"         retry after error: {last_error}", file=sys.stderr)
                await asyncio.sleep(5)
                continue

    duration_ms = int((time.monotonic() - start) * 1000)
    return StepResult(
        step_id=sid, tool=tool, status="failed",
        error=last_error, duration_ms=duration_ms,
        args_rendered=log_args, redacted=redact,
    )


# --------------------------------------------------------------------------- #
# Reporting + audit log                                                       #
# --------------------------------------------------------------------------- #

def _truncate(value: Any, n: int = 80) -> str:
    s = json.dumps(value, ensure_ascii=False, default=str) if not isinstance(value, str) else value
    s = s.replace("\n", " ").replace("|", r"\|")
    return s if len(s) <= n else s[:n] + "..."


def render_report(
    flow: Flow,
    inputs: dict[str, str],
    results: list[StepResult],
    overall_status: str,
    total_ms: int,
) -> str:
    lines: list[str] = []
    lines.append(f"## MCP Flow: {flow.name}")
    lines.append("")
    lines.append(f"**Status**: {overall_status}")
    lines.append(f"**Inputs**: `{json.dumps(inputs, ensure_ascii=False)}`")
    lines.append(f"**Duration**: {total_ms} ms")
    lines.append(f"**Source**: `{flow.path.relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("### Step Log")
    lines.append("")
    lines.append("| # | Step | Tool | Status | Duration | Output (truncated) |")
    lines.append("|---|------|------|--------|----------|--------------------|")
    for i, r in enumerate(results, 1):
        out_cell = _truncate(r.error if r.status == "failed" and r.error else r.output, 60)
        lines.append(
            f"| {i} | {r.step_id} | `{r.tool}` | {r.status} | "
            f"{r.duration_ms} ms | {out_cell} |"
        )
    lines.append("")

    exposed = [
        s for s in flow.steps
        if s.get("expose")
    ]
    if exposed:
        lines.append("### Final Outputs")
        lines.append("")
        for s in exposed:
            sid = s["id"]
            r = next((r for r in results if r.step_id == sid), None)
            if r is None or r.status not in {"ok", "dry-run"}:
                continue
            lines.append(f"#### `{sid}`")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(r.output, ensure_ascii=False, indent=2, default=str)[:2000])
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


def write_audit_log(report: str, flow_name: str, dry_run: bool) -> Path:
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    suffix = "-dryrun" if dry_run else ""
    out = AUDIT_LOG_DIR / f"{flow_name}-{ts}{suffix}.md"
    out.write_text(report, encoding="utf-8")
    return out


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #

async def execute_flow(
    flow: Flow,
    inputs: dict[str, str],
    *,
    dry_run: bool,
    start_at: str | None,
    verbose: bool,
) -> tuple[str, list[StepResult], int]:
    registry = load_server_registry(REPO_ROOT)
    if verbose:
        print(f"[registry] {len(registry)} server(s): {sorted(registry)}", file=sys.stderr)

    ctx: dict[str, Any] = {
        "inputs": inputs,
        "env": dict(os.environ),
    }

    results: list[StepResult] = []
    overall = "completed"
    started = False
    flow_start = time.monotonic()

    for step in flow.steps:
        sid = step["id"]
        if start_at and not started:
            if sid != start_at:
                results.append(StepResult(
                    step_id=sid, tool=step["tool"], status="skipped",
                    error=f"skipped due to --start-at {start_at}",
                ))
                continue
            started = True

        result = await run_step(
            step, ctx, registry,
            dry_run=dry_run, verbose=verbose,
        )
        results.append(result)
        # Always expose under step_<id>.output even on failure (downstream may
        # tolerate empty output via filters).
        ctx[f"step_{sid}"] = {"output": result.output if result.status == "ok" else ""}

        if result.status == "failed":
            on_error = step.get("on_error", "abort")
            if on_error == "abort":
                overall = "failed"
                break
            overall = "partial"

    total_ms = int((time.monotonic() - flow_start) * 1000)
    return overall, results, total_ms


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute a declarative MCP cross-tool flow.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See .claude/skills/mcp-flow/SKILL.md for flow YAML schema.",
    )
    parser.add_argument("flow", nargs="?", help="Flow name (without .yaml)")
    parser.add_argument(
        "inputs", nargs="*",
        help="key=value pairs forwarded to flow inputs",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse + validate + render args, do not invoke MCP tools")
    parser.add_argument("--start-at", metavar="STEP_ID",
                        help="Skip steps until this id (resume after partial failure)")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--list", action="store_true",
                        help="List available flows and exit")
    args = parser.parse_args()

    if args.list:
        flows = list_flows()
        if not flows:
            print("(no flows found)")
            return 0
        print("Available flows:")
        for f in flows:
            print(f"  {f}")
        return 0

    if not args.flow:
        parser.print_usage(sys.stderr)
        print("ERROR: flow name is required (or use --list).", file=sys.stderr)
        return 2

    try:
        flow = load_flow(args.flow)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2

    cli_inputs = parse_cli_inputs(args.inputs)
    inputs = resolve_inputs(flow.inputs_schema, cli_inputs)

    if args.verbose:
        print(f"[flow] {flow.name} ({flow.path})", file=sys.stderr)
        print(f"[inputs] {json.dumps(inputs, ensure_ascii=False)}", file=sys.stderr)
        print(f"[mode] {'dry-run' if args.dry_run else 'live'}", file=sys.stderr)

    overall, results, total_ms = asyncio.run(execute_flow(
        flow, inputs,
        dry_run=args.dry_run,
        start_at=args.start_at,
        verbose=args.verbose,
    ))

    report = render_report(flow, inputs, results, overall, total_ms)
    print(report)

    if flow.dual_write or args.dry_run:
        # Always dual-write dry-runs (audit trail of validation), real runs
        # only if YAML opts in.
        out_path = write_audit_log(report, flow.name, args.dry_run)
        print(f"\n[audit] wrote {out_path.relative_to(REPO_ROOT)}", file=sys.stderr)

    if overall == "failed":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

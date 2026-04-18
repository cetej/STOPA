#!/usr/bin/env python3
"""Stop hook: bridge per-run optimization traces into session trace format.

Solves the trace format gap: /discover reads .traces/sessions/*.jsonl but
autoresearch/autoloop write to .traces/<run_id>/tools.jsonl. This bridge
copies relevant records from run traces into the session trace at session end.

Activation: only runs if a trace-active.json marker exists (optimization ran).
Writes: appends to the current session's .traces/sessions/ file.

Schema mapping:
  run trace → session trace
  {ts, seq, tool, exit, input_path, input_cmd} → {ts, tool, exit, path, cmd, source: "run:<run_id>"}
"""
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MARKER_PATH = PROJECT_ROOT / ".claude/memory/intermediate/trace-active.json"
SESSION_CACHE = PROJECT_ROOT / ".claude/memory/intermediate/session-trace-path"
SESSION_TRACES_DIR = PROJECT_ROOT / ".traces/sessions"


def get_session_trace_path() -> Path | None:
    """Find the current session's trace file."""
    if SESSION_CACHE.exists():
        try:
            cached = SESSION_CACHE.read_text(encoding="utf-8").strip()
            p = Path(cached)
            if p.exists():
                return p
        except OSError:
            pass
    # Fallback: most recent session trace
    if SESSION_TRACES_DIR.exists():
        traces = sorted(SESSION_TRACES_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        if traces:
            return traces[0]
    return None


def bridge_traces(run_dir: Path, session_path: Path, run_id: str):
    """Copy run trace records into session trace format."""
    tools_jsonl = run_dir / "tools.jsonl"
    if not tools_jsonl.exists():
        return 0

    bridged = 0
    with open(tools_jsonl, "r", encoding="utf-8", errors="replace") as f_in, \
         open(session_path, "a", encoding="utf-8") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Map to session trace format (compact)
            session_rec = {
                "ts": rec.get("ts", time.time()),
                "tool": rec.get("tool", "?"),
                "exit": rec.get("exit", 0),
                "source": f"run:{run_id}",
            }
            if rec.get("input_path"):
                session_rec["path"] = rec["input_path"]
            elif rec.get("input_cmd"):
                session_rec["cmd"] = rec["input_cmd"][:120]
            if rec.get("iteration") is not None:
                session_rec["iter"] = rec["iteration"]

            f_out.write(json.dumps(session_rec) + "\n")
            bridged += 1

    return bridged


def main():
    if not MARKER_PATH.exists():
        return

    try:
        marker = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    run_id = marker.get("run_id", "")
    trace_dir = marker.get("trace_dir", "")
    if not run_id or not trace_dir:
        return

    run_dir = Path(trace_dir)
    if not run_dir.exists():
        return

    session_path = get_session_trace_path()
    if session_path is None:
        # Create a new session trace file
        SESSION_TRACES_DIR.mkdir(parents=True, exist_ok=True)
        session_path = SESSION_TRACES_DIR / f"{time.strftime('%Y-%m-%d')}-bridge.jsonl"

    bridged = bridge_traces(run_dir, session_path, run_id)
    if bridged > 0:
        print(f"[trace-bridge] Bridged {bridged} records from {run_id} into session trace", file=sys.stderr)


if __name__ == "__main__":
    main()

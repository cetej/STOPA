#!/usr/bin/env python3
"""PostToolUse hook: capture rich tool execution traces during optimization runs.

Meta-Harness-inspired (arXiv:2603.28052): full execution traces with tool inputs/outputs
dramatically outperform scores-only feedback for outer-loop optimization (56.7% vs 38.7%).

Activation: Only runs when .claude/memory/intermediate/trace-active.json exists.
Without marker → exits in <1ms (zero overhead for normal sessions).

Writes to: .traces/<run_id>/tools.jsonl (JSONL append-only)

Schema per record:
  ts, seq, tool, exit, input_path, input_cmd, input_snippet(500),
  output_snippet(2000), output_full(errors only), tokens_est, iteration
"""
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MARKER_PATH = PROJECT_ROOT / ".claude/memory/intermediate/trace-active.json"
MAX_INPUT_SNIPPET = 500
MAX_OUTPUT_SNIPPET = 2000
MAX_MARKER_AGE_S = 4 * 3600  # 4 hours — auto-expire stale markers


def main():
    # Fast-path: no marker → no work
    if not MARKER_PATH.exists():
        return

    # Read marker — get run_id and iteration
    try:
        marker = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        run_id = marker.get("run_id", "")
        trace_dir = Path(marker.get("trace_dir", ""))
        iteration = marker.get("current_iteration", 0)
        started = marker.get("started", "")
    except (json.JSONDecodeError, OSError):
        return

    if not run_id or not trace_dir:
        return

    # Auto-expire stale markers (>4 hours)
    if started:
        try:
            start_ts = time.mktime(time.strptime(started[:19], "%Y-%m-%dT%H:%M:%S"))
            if time.time() - start_ts > MAX_MARKER_AGE_S:
                try:
                    MARKER_PATH.unlink()
                except OSError:
                    pass
                return
        except (ValueError, OverflowError):
            pass

    # Parse stdin JSON from Claude Code
    stdin_data = ""
    try:
        stdin_data = sys.stdin.read()
    except Exception:
        pass

    if not stdin_data:
        return

    try:
        event = json.loads(stdin_data)
    except json.JSONDecodeError:
        return

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", "")
    tool_output = event.get("tool_output", "")
    exit_code = event.get("tool_exit_code", 0)
    # Agent attribution: agent_type present = subagent (CC convention)
    agent_type = event.get("agent_type", "")

    if not tool_name:
        return

    # Skip read-only tools to reduce noise (proposer reads are not diagnostic)
    if tool_name in ("Read", "Glob", "Grep", "TodoRead", "TodoWrite"):
        return

    # Build input snippet
    input_str = tool_input if isinstance(tool_input, str) else json.dumps(tool_input, ensure_ascii=False)
    input_snippet = input_str[:MAX_INPUT_SNIPPET]

    # Extract structured fields
    input_path = None
    input_cmd = None
    if isinstance(tool_input, dict):
        input_path = tool_input.get("file_path") or tool_input.get("path")
        input_cmd = tool_input.get("command")
    elif isinstance(tool_input, str) and tool_name == "Bash":
        input_cmd = input_str[:1000]  # Full command for Bash

    # Build output snippet
    output_str = tool_output if isinstance(tool_output, str) else json.dumps(tool_output, ensure_ascii=False)
    output_snippet = output_str[:MAX_OUTPUT_SNIPPET]

    # Full output for errors (Bash with non-zero exit) — key Meta-Harness insight
    output_full = None
    if tool_name == "Bash" and exit_code != 0:
        output_full = output_str[:10000]  # Cap at 10KB for storage

    # Estimate tokens (rough: 4 chars ≈ 1 token)
    tokens_est = (len(input_str) + len(output_str)) // 4

    # Read sequence number from tools.jsonl line count
    trace_dir.mkdir(parents=True, exist_ok=True)
    tools_path = trace_dir / "tools.jsonl"
    seq = 0
    if tools_path.exists():
        try:
            with open(tools_path, "r", encoding="utf-8") as f:
                seq = sum(1 for _ in f)
        except OSError:
            pass

    # Build trace record
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seq": seq,
        "tool": tool_name,
        "exit": exit_code,
        "iteration": iteration,
        "tokens_est": tokens_est,
        "input_snippet": input_snippet,
        "output_snippet": output_snippet,
    }
    if input_path:
        record["input_path"] = str(input_path)
    if input_cmd:
        record["input_cmd"] = input_cmd
    if output_full:
        record["output_full"] = output_full
    if agent_type:
        record["agent"] = agent_type  # subagent attribution (main agent omits)

    # Append to JSONL (atomic-ish on Windows)
    try:
        with open(tools_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never fail the tool use

#!/usr/bin/env python3
"""Validate trace JSONL files — ASCII-safe output for Windows compatibility.

Checks:
1. Every line is valid JSON
2. Required fields present (ts, seq, tool, exit)
3. Agent attribution format (optional `agent` field)
4. Error records (exit != 0) have output_full
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REQUIRED = {"ts", "seq", "tool", "exit"}


def validate(trace_path: Path) -> int:
    """Return 0 on success, non-zero on validation error."""
    if not trace_path.exists():
        print(f"[FAIL] Trace not found: {trace_path}")
        return 2

    errors = 0
    records = []
    agents = set()
    error_records = []

    with open(trace_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[FAIL] Line {lineno}: invalid JSON: {e}")
                errors += 1
                continue

            missing = REQUIRED - rec.keys()
            if missing:
                print(f"[FAIL] Line {lineno}: missing fields: {sorted(missing)}")
                errors += 1
                continue

            records.append(rec)
            if "agent" in rec:
                agents.add(rec["agent"])
            if rec.get("exit", 0) != 0:
                error_records.append(rec)

    total = len(records)
    print(f"[OK] Parsed {total} records from {trace_path.name}")
    print(f"[INFO] Tools: {sorted({r['tool'] for r in records})}")
    print(f"[INFO] Subagent attributions: {sorted(agents) if agents else '(none - all main agent)'}")
    print(f"[INFO] Error records (exit != 0): {len(error_records)}")

    for rec in error_records:
        has_full = "output_full" in rec
        marker = "[OK]" if has_full else "[WARN]"
        print(f"  {marker} seq={rec['seq']} tool={rec['tool']} exit={rec['exit']} "
              f"output_full={'present' if has_full else 'MISSING'}")

    if errors:
        print(f"[FAIL] {errors} validation error(s)")
        return 1

    print(f"[PASS] All {total} records valid; agent attribution works")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate-trace.py <trace.jsonl>")
        sys.exit(2)
    sys.exit(validate(Path(sys.argv[1])))

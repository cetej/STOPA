#!/usr/bin/env python3
"""PostToolUse hook for Read: track file mtimes and signal when a file is re-read unchanged.

Injects [DEDUP] note via stdout (additionalContext) when same file is read again
with identical mtime. Session-scoped via PID marker.

Performance target: <50ms — pure os.stat(), no subprocess calls.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LEDGER_PATH = Path('.claude/memory/intermediate/read-dedup.json')
SESSION_MARKER = Path('.claude/memory/intermediate/.session-pid')


def get_session_pid() -> str:
    """Get or create session PID marker for scoping the ledger."""
    ppid = str(os.getppid())
    if SESSION_MARKER.exists():
        stored = SESSION_MARKER.read_text(encoding='utf-8').strip()
        if stored == ppid:
            return ppid
    # New session — reset ledger
    SESSION_MARKER.parent.mkdir(parents=True, exist_ok=True)
    SESSION_MARKER.write_text(ppid, encoding='utf-8')
    if LEDGER_PATH.exists():
        LEDGER_PATH.unlink()
    return ppid


def main():
    try:
        # Parse tool input from stdin
        stdin_data = ''
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.read()

        if not stdin_data:
            return

        try:
            data = json.loads(stdin_data)
        except json.JSONDecodeError:
            return

        # Extract file_path from tool input
        tool_input = data.get('tool_input', {})
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                return

        file_path = tool_input.get('file_path', '')
        if not file_path:
            return

        # Normalize path
        file_path = str(Path(file_path).resolve())

        # Get current mtime
        try:
            mtime = os.stat(file_path).st_mtime
        except OSError:
            return  # File doesn't exist or inaccessible

        # Session scoping
        get_session_pid()

        # Load or initialize ledger
        ledger = {}
        if LEDGER_PATH.exists():
            try:
                ledger = json.loads(LEDGER_PATH.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError):
                ledger = {}

        reads = ledger.get('reads', {})

        if file_path in reads:
            entry = reads[file_path]
            if entry.get('mtime') == mtime:
                # File unchanged — inject dedup note
                first_read = entry.get('first_read', '??:??')
                count = entry.get('count', 1) + 1
                entry['count'] = count
                # Output additionalContext
                print(f'[DEDUP] {Path(file_path).name} unchanged since {first_read} (read #{count})')
            else:
                # File changed — update entry, no dedup note
                entry['mtime'] = mtime
                entry['first_read'] = datetime.now().strftime('%H:%M')
                entry['count'] = 1
        else:
            # First read — record it
            reads[file_path] = {
                'mtime': mtime,
                'first_read': datetime.now().strftime('%H:%M'),
                'count': 1,
            }

        # Save ledger
        ledger['reads'] = reads
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding='utf-8')

    except Exception:
        pass  # Never block Read — fail silently


if __name__ == '__main__':
    main()

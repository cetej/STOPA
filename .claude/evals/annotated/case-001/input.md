---
source: annotation
trace: test-trace-2026-04-23.jsonl
trace_seq: 3
annotated_by: cetej
annotated_at: 2026-04-23T10:30:15
---

# Context

Record z trace:
- tool: Bash
- input: `python -m pytest tests/`
- exit: 1

Předchozí 3 tool calls (pro context):
- seq=0 Read: `file_path=/path/to/file`
- seq=1 Bash: `git status` → "On branch main"
- seq=2 Edit: `old_text: ..., new_text: ...` → "3 line(s) replaced"

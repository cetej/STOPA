#!/usr/bin/env bash
# SessionStart hook: surface pending reminders whose due_date has arrived.
# Reads .claude/memory/pending-reminders.md (NOT auto-regenerated — stable).
# Emits banner with title + action for each due item.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REMINDERS="$PROJECT_ROOT/memory/pending-reminders.md"

if [ ! -f "$REMINDERS" ]; then
  exit 0
fi

python3 - <<'PY' "$REMINDERS"
import sys, re
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

path = sys.argv[1]
try:
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
except Exception:
    sys.exit(0)

today = date.today().isoformat()
due = []

# Parse loose YAML: split on "- id:" boundaries
blocks = re.split(r'^- id:\s*', text, flags=re.MULTILINE)[1:]
for b in blocks:
    m_id = re.match(r'([^\s]+)', b)
    m_due = re.search(r'^\s*due_date:\s*([\d-]+)', b, re.MULTILINE)
    m_title = re.search(r'^\s*title:\s*"?([^"\n]+)"?', b, re.MULTILINE)
    m_prio = re.search(r'^\s*priority:\s*(\w+)', b, re.MULTILINE)
    m_action = re.search(r'^\s*action:\s*\|\s*\n((?:    .*\n)+)', b, re.MULTILINE)
    if not (m_id and m_due and m_title):
        continue
    if m_due.group(1) > today:
        continue
    action = ""
    if m_action:
        action = re.sub(r'^    ', '', m_action.group(1), flags=re.MULTILINE).strip()
    due.append({
        "id": m_id.group(1).strip(),
        "due": m_due.group(1),
        "title": m_title.group(1).strip(),
        "prio": (m_prio.group(1) if m_prio else "medium").strip(),
        "action": action,
    })

if not due:
    sys.exit(0)

print("=== Pending Reminders (" + str(len(due)) + " due) ===")
for item in due:
    age = (date.fromisoformat(today) - date.fromisoformat(item["due"])).days
    age_str = "today" if age == 0 else (f"{age}d overdue" if age > 0 else f"{-age}d early")
    print(f"  [{item['prio']}] {item['title']}")
    print(f"    due: {item['due']} ({age_str}) | id: {item['id']}")
    if item["action"]:
        first_line = item["action"].split("\n")[0]
        print(f"    -> {first_line}")
print("  (detail: .claude/memory/pending-reminders.md — archive completed items)")
PY

exit 0

#!/usr/bin/env bash
# PreToolUse:Bash — silent deny for catastrophic / irreversible commands.
# Runs alongside dippy and block-no-verify. Only blocks TOP-SEVERITY patterns
# to keep friction zero for normal work.
#
# Exit 2 = block with user-visible reason. Exit 0 = allow (pass to next hook).
#
# Scope: only patterns where a false positive cost (one manual override) is
# far lower than a false negative (data loss / breaking main).

INPUT=$(cat)

# Extract command — JSON "command" field or raw stdin as fallback.
CMD=$(echo "$INPUT" | python -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    ti = d.get('tool_input') or {}
    print(ti.get('command') or d.get('command') or '')
except Exception:
    print('')
" 2>/dev/null)

[ -z "$CMD" ] && exit 0

# Strip heredoc bodies before pattern matching — a commit message or doc
# string may legitimately contain strings like "dd of=/dev/sda" without
# actually invoking them. We only care about executed command syntax.
# Match any `<<'DELIM'` or `<<"DELIM"` or `<<DELIM` and drop everything
# until a line containing only DELIM.
CMD_FOR_MATCH=$(python -c "
import re, sys
s = sys.argv[1]
# Repeatedly strip heredocs
for _ in range(10):
    m = re.search(r'<<-?\s*[\"\\']?([A-Za-z_][A-Za-z0-9_]*)[\"\\']?', s)
    if not m:
        break
    delim = m.group(1)
    start = m.start()
    # find end delimiter on its own line
    end_re = re.compile(r'^\s*' + re.escape(delim) + r'\s*$', re.MULTILINE)
    em = end_re.search(s, m.end())
    if not em:
        # truncate to heredoc start if no closer
        s = s[:start]
        break
    s = s[:start] + s[em.end():]
print(s)
" "$CMD" 2>/dev/null || echo "$CMD")

block() {
  local reason="$1"
  echo "BLOCK: $reason" >&2
  echo "If you genuinely need this, run it manually outside Claude Code." >&2
  # Log for audit
  mkdir -p "$(dirname "$0")/../memory" 2>/dev/null
  echo "$(date +%Y-%m-%dT%H:%M:%S)|$reason|$CMD" >> "$(dirname "$0")/../memory/bash-safety-blocks.log" 2>/dev/null
  exit 2
}

# --- Catastrophic deletes ---
# rm -rf / or rm -rf /* or rm -rf ~  (with optional flags/spacing)
if echo "$CMD" | grep -qE '\brm[[:space:]]+(-[a-zA-Z]*r[a-zA-Z]*f|-rf|-fr)[[:space:]]+(/|~|/home|/root|/usr|/etc|/var|\$HOME|C:)([[:space:]]|$|/\*)'; then
  block "rm -rf on root-level path — would wipe system or home"
fi
# rm -rf * at start of command (current directory bomb)
if echo "$CMD" | grep -qE '^[[:space:]]*rm[[:space:]]+-rf?[[:space:]]+\*[[:space:]]*$'; then
  block "rm -rf * with no explicit target — ambiguous catastrophic delete"
fi

# --- Force-push to main/master on any remote ---
if echo "$CMD" | grep -qE '\bgit[[:space:]]+push[[:space:]]+.*(-f\b|--force(-with-lease)?\b).*[[:space:]](main|master)([[:space:]]|$|:)'; then
  block "git push --force to main/master — rewriting shared history"
fi

# --- Disk destroyers ---
if echo "$CMD" | grep -qE '\bdd[[:space:]]+.*\bof=/dev/(sd[a-z]|nvme|disk|hd)'; then
  block "dd writing to raw disk device — would erase drive"
fi
if echo "$CMD" | grep -qE '\bmkfs\.[a-z0-9]+[[:space:]]+/dev/'; then
  block "mkfs on disk device — would format drive"
fi

# --- System control ---
if echo "$CMD" | grep -qE '\b(shutdown|reboot|halt|poweroff)\b.*(-[hrfn]|now|\+[0-9])'; then
  block "shutdown/reboot command — would kill the machine mid-session"
fi

# --- Recursive chmod 777 on root-level paths ---
if echo "$CMD" | grep -qE '\bchmod[[:space:]]+-R[[:space:]]+(0?777)[[:space:]]+(/|~|\$HOME)'; then
  block "chmod -R 777 on root path — destroys permissions"
fi

# --- Git nuclear options ---
if echo "$CMD" | grep -qE '\bgit[[:space:]]+(clean[[:space:]]+-[xdf]*d[xdf]*f|reset[[:space:]]+--hard[[:space:]]+HEAD~[0-9]+)'; then
  # git clean -fdx without dry-run + git reset --hard HEAD~N (lose commits)
  # Allow if explicit --dry-run present
  if ! echo "$CMD" | grep -qE '(--dry-run|-n\b)'; then
    block "git clean -fdx / reset --hard HEAD~N without dry-run — irreversible"
  fi
fi

exit 0

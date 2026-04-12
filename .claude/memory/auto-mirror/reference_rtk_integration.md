---
name: RTK token optimizer integration
description: RTK (Rust Token Killer) installed as global PreToolUse hook — rewrites CLI commands for 60-90% token savings
type: reference
---

RTK v0.34.3 nainstalován jako globální Claude Code PreToolUse hook (2026-04-05).

**Binárky:**
- `C:\Users\stock\.local\bin\rtk.exe` — RTK binary
- `C:\Users\stock\.local\bin\jq.exe` — jq dependency

**Hook:** `~/.claude/hooks/rtk-rewrite.sh` — interceptuje Bash commands, deleguje na `rtk rewrite`

**Config:** `~/.claude/settings.json` — RTK hook je PRVNÍ v PreToolUse array (před dippy)

**Awareness:** `~/.claude/RTK.md` — referenced via `@RTK.md` v `~/.claude/CLAUDE.md`

**Meta příkazy:**
- `rtk gain` — token savings analytics
- `rtk gain --history` — command history with savings
- `rtk discover` — find missed optimization opportunities
- `rtk proxy <cmd>` — bypass filtering (debug)

**Upgrade:** `curl -sL https://github.com/rtk-ai/rtk/releases/latest/download/rtk-x86_64-pc-windows-msvc.zip -o /tmp/rtk.zip && python -c "import zipfile; zipfile.ZipFile('/tmp/rtk.zip').extractall('/tmp/rtk-up')" && cp /tmp/rtk-up/rtk.exe ~/.local/bin/`

**Repo:** https://github.com/rtk-ai/rtk

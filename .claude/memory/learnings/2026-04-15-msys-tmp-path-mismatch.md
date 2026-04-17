---
date: 2026-04-15
type: bug_fix
severity: medium
component: hook
tags: [windows, path, msys, git-bash, loop-state]
summary: "Git Bash/MSYS2 přeloží /tmp na C:\\Users\\<user>\\AppData\\Local\\Temp PŘED předáním argumentu Pythonu, ale Python Path('/tmp') resoluje na C:\\tmp. Každý skript přijímající cestu z bash musí mít _resolve_path() fallback. Opraveno v loop-state.py pro všechny subcommandy."
source: user_correction
uses: 5
successful_uses: 0
harmful_uses: 0
confidence: 1.00
failure_class: resource
verify_check: "Grep('_resolve_path', path='scripts/loop-state.py') → 1+ matches"
related: [2026-04-16-hook-cwd-anchor-pattern.md]
---

## Detail

**Root cause:** MSYS2 path translation (`/tmp` → `%LOCALAPPDATA%/Temp`) happens in the shell layer before Python process starts. Python's own `pathlib.Path('/tmp')` resolves to `C:\tmp` (native Windows). These are different directories.

**Symptom:** `python scripts/loop-state.py decay-predict /tmp/test.tsv` → "insufficient_data (have 0)" because file is at `C:\tmp\test.tsv` but script receives `C:\Users\stock\AppData\Local\Temp\test.tsv`.

**Fix:** `_resolve_path()` helper in `loop-state.py` — when MSYS-translated path doesn't exist, tries `C:\tmp\<basename>` as fallback. Applied to all subcommands via `read_tsv_tail()` and explicit calls at `Path(args.*)` sites.

**Broader lesson:** In STOPA, any Python script called from bash with file path arguments needs this guard. Relative paths (`.claude/memory/...`) are safe. Absolute Unix paths (`/tmp`, `/home`) are not.

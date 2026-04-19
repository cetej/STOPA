---
name: Verification discipline
description: Never claim done without proof — check output content not just exit code, grep after ruff autofix, verify before overwriting
type: feedback
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
User has been burned multiple times by false completion claims. Consolidated rules:

1. **Exit code is not enough** — always check output size and content after pipeline/build
2. **After ruff autofix**: grep EVERY removed symbol in entire file — F401 broke REQUESTS_AVAILABLE flag
3. **Before overwriting a file**: find ALL versions (projects, git history, archives), diff, take best as base
4. **Checkpoint mental test**: "Would a fresh session understand what to do AND what NOT to do?"
5. **Transparency**: say "Checkpoint says X, verifying" not "let me look at what needs doing"

**Why:** False completion = #1 cause of wasted follow-up sessions. Ruff autofix specifically deleted a flag variable used in try/except.

**How to apply:** Every "done" claim must have tool output evidence. Ruff fixes get extra grep pass. File overwrites get diff pass.

# Alerts — Actionable Issues

Rotating log of genuine problems that need user attention: failures, security findings, dependency vulnerabilities, quota warnings, API key health issues.

**Policy:** append-only, one entry per event. Entries older than 30 days migrate to `alerts-archive.md` during memory maintenance.

**Format:**
```
## YYYY-MM-DD HH:MM — [SOURCE] Short title
- **Severity:** critical | high | medium | low
- **Source:** task-name / hook-name / manual
- **Detail:** one paragraph describing the issue
- **Action suggested:** what user should do
- **Status:** open | acknowledged | resolved
```

**User reviews this file:** via `/status`, manually, or when a high-severity entry is added (shell-level notification can be added later without Telegram).

---

## Log

## 2026-04-21 14:27 — [keys-health] FAL_KEY — expired_or_invalid
- **Severity:** high
- **Source:** scripts/keys-health.py
- **Detail:** HTTP 401. Body: `{"detail": "No user found for Key ID and Secret"}`
- **Action suggested:** rotate FAL_KEY in ~/.claude/keys/secrets.env, run keys-sync.ps1
- **Status:** open

## 2026-04-21 15:23 — [keys-presence] Missing API keys: ANTHROPIC_API_KEY, GITHUB_TOKEN
- **Severity:** medium
- **Source:** SessionStart keys-presence-check.py
- **Detail:** The following required keys are not in environment:
  - `ANTHROPIC_API_KEY` — blocks L2 permission sentinel, sub-agents
  - `GITHUB_TOKEN` — blocks /fix-issue, /autofix, GitHub MCP
- **Action suggested:** fill values in `~/.claude/keys/secrets.env`, run `pwsh scripts/keys-sync.ps1`, restart CC.
- **Status:** open

## 2026-04-21 15:43 — [keys-health] FAL_KEY — expired_or_invalid
- **Severity:** high
- **Source:** scripts/keys-health.py
- **Detail:** HTTP 401. Body: `{"detail": "No user found for Key ID and Secret"}`
- **Action suggested:** rotate FAL_KEY in ~/.claude/keys/secrets.env, run keys-sync.ps1
- **Status:** open

## 2026-04-21 15:44 — [keys-health] FAL_KEY — http_405
- **Severity:** high
- **Source:** scripts/keys-health.py
- **Detail:** HTTP 405. Body: `{"detail":"Method Not Allowed"}`
- **Action suggested:** rotate FAL_KEY in ~/.claude/keys/secrets.env, run keys-sync.ps1
- **Status:** open

## 2026-04-21 15:50 — [keys-presence] Missing API keys: ANTHROPIC_API_KEY
- **Severity:** medium
- **Source:** SessionStart keys-presence-check.py
- **Detail:** The following required keys are not in environment:
  - `ANTHROPIC_API_KEY` — blocks L2 permission sentinel, sub-agents
- **Action suggested:** fill values in `~/.claude/keys/secrets.env`, run `pwsh scripts/keys-sync.ps1`, restart CC.
- **Status:** open

## 2026-04-23 04:08 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-23 04:11 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-23 20:22 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-23 20:24 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-23 20:27 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-23 20:56 — [hook] 🏁 Session dokončena 
- **Severity:** low
- **Source:** telegram-notify.sh (legacy caller)
- **Status:** open

## 2026-04-25 18:30 — [tool-radar-scan] New 🔴 tool: Hippo (kitfunso/hippo-memory) 8/10
- **Severity:** high
- **Source:** tool-radar-scan
- **Detail:** Biologically-inspired memory for AI agents (593★, MIT, TS+SQLite, v0.31.0 Apr 22 2026, npm i -g hippo-memory). Implements 7 mechanisms: 7-day half-life decay, retrieval strengthening (+2d per recall), error memories 2× persistence, consolidation cycles (`hippo sleep`), conflict detection, multi-tool portability (ChatGPT/Claude/Cursor → markdown), outcome feedback. Validates STOPA memory-files.md ACT-R note + introduces 2 NEW patterns absent from STOPA: (1) error memories 2× persistence (STOPA currently penalizes errors via harmful_uses, doesn't extend their half-life), (2) exponential decay with retrieval extension (STOPA uses linear 0.05 confidence boost).
- **Action suggested:** /improve STOPA — pilot exponential decay in evolve script + add "error 2× persistence" rule to memory-files.md. /improve 2BRAIN — multi-tool portability pattern (Claude/Cursor → markdown export). M effort.
- **Status:** open

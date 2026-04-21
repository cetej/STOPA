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

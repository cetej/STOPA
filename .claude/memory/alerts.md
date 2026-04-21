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

---
name: No secrets in config files
description: Never write API keys, tokens, or credentials directly into JSON config files — use env vars instead
type: feedback
---

NIKDY nezapisovat tokeny, API klíče ani credentials přímo do config souborů (claude_desktop_config.json, settings.json, apod.).

**Why:** Claude zapsal GitHub PAT a Brave API key přímo do claude_desktop_config.json. Tyto hodnoty se pak objevily v tool výstupech a zálohách — bezpečnostní incident.

**How to apply:** Při konfiguraci MCP serverů nebo jakýchkoli služeb vždy navrhnout uživateli nastavení přes systémové environment variables (Windows: setx). Pokud uživatel poskytne token, nikdy ho nekopírovat do souboru — místo toho mu říct jak si ho nastavit jako env var.

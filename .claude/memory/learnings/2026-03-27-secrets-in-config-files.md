---
date: 2026-03-27
type: anti_pattern
severity: critical
component: general
tags: [security, tokens, secrets, claude-desktop, env-vars]
summary: "NEVER write API keys/tokens into JSON config files. Use environment variables or .env files excluded from git."
source: auto_pattern
verify_check: "Grep('ANTHROPIC_API_KEY.*:.*sk-ant|ghp_[a-zA-Z0-9]{36,}', path='.claude/settings.json') → 0 matches"
confidence: 1.0
uses: 1
successful_uses: 0
harmful_uses: 0
---

# Tokeny a API klíče nesmí být přímo v config souborech

## Problém
Claude zapsal GitHub PAT a Brave API key přímo do `claude_desktop_config.json`
jako plaintext hodnoty v `env` bloku. Tyto soubory mohou být:
- zálohovány (backups/)
- zobrazeny v tool výstupech
- commitnuty omylem

## Anti-pattern
```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"  // NIKDY
}
```

## Správný přístup
- Tokeny ukládat do systémových env proměnných (Windows: setx / Environment Variables)
- Nebo do `.env` souboru, který je v `.gitignore`
- Config pak jen odkazuje: `"env": {}` (zdědí z prostředí)

## Pravidlo
Při konfiguraci MCP serverů nebo jakýchkoli JSON configů:
1. NIKDY nezapisovat tokeny/klíče přímo do souboru
2. Vždy navrhnout uživateli nastavení přes systémové env proměnné
3. Pokud uživatel trvá na přímém zápisu, explicitně upozornit na riziko

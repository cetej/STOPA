---
name: reference_anthropic_key
description: Anthropic API key — primary source is C:\Users\stock\.claude\keys\secrets.env (central store), never ask user
type: reference
originSessionId: cb748470-fec5-4188-b198-8e07e0688ce7
---
**Primary source:** `C:\Users\stock\.claude\keys\secrets.env` — centrální store pro všechny projekty. Obsahuje `ANTHROPIC_API_KEY=sk-ant-...` a další klíče (gitignored přes `.claude/keys/.gitignore`).

**Backup umístění (historická):**
- `C:\Users\stock\Documents\000_NGM\DANE\.env`
- NG-ROBOT projekt

**Použitý vzor pro nové projekty:**
1. `grep "^ANTHROPIC_API_KEY=" C:/Users/stock/.claude/keys/secrets.env | sed 's/^[^=]*=//' > <project>/secrets/api_key.txt`
2. Projekt si klíč načte přes vlastní helper (např. `load_api_key_from_file()` v KRIZOVKA/krizovka/clue_gen.py)
3. Adresář `secrets/` přidat do `.gitignore`

**Why:** Uživatel opakovaně upozorňoval, že klíč už existuje. Ptát se znovu = frustrace. Centrální `.claude/keys/secrets.env` je kanonický.

**How to apply:** Před jakýmkoli dotazem na klíč — **VŽDY** nejdřív `ls C:/Users/stock/.claude/keys/` a `grep ANTHROPIC secrets.env`. Nikdy nekopírovat klíč do chatu, jen extrahovat přes shell do cílového souboru.

**Windows subprocess gotcha (2026-04-25):** Bash tool a default PowerShell tool process scope NEVIDÍ User-scope env vars. `os.environ.get("ANTHROPIC_API_KEY")` v Pythonu spuštěném přes Bash() vrátí prázdné. **Tři způsoby jak to obejít:**
1. Source z `secrets.env`: `source <(grep ^ANTHROPIC_API_KEY= /c/Users/stock/.claude/keys/secrets.env)` před `python ...`
2. PowerShell explicitní načtení User scope: `$env:ANTHROPIC_API_KEY = [Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY","User")`
3. Python helper (preferred): `load_api_key_from_file()` čtoucí přímo `~/.claude/keys/secrets.env`

User opakovaně frustrován ("tohle už jsme řešili tolikrát"). Pravidlo: pokud Python script potřebuje API key, **nikdy** nespoléhat na os.environ — vždy explicitní fallback na secrets.env.

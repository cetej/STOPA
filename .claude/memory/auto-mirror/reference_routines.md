---
name: Anthropic Routines (Cloud Automations)
description: Claude Code Routines — cloud-hosted automations with schedule/webhook/API triggers, pricing, limits, migration plan
type: reference
originSessionId: fc93c392-b23d-40b3-889d-1f0bd89d9dbd
---
## Co jsou Routines

Cloud-hosted Claude Code sessions spouštěné automaticky. Laptop nemusí být zapnutý.
Trigger: cron schedule | webhook (GitHub) | API call.
URL: claude.ai/code/routines
Status: Research Preview (launched 2026-04-14)

## Pricing (Max plán = uživatel)

- **Max plán**: $100-200/měsíc, **15 runs/den**
- Pro: 5/den, Team/Enterprise: 25/den
- Tokenová cena = stejná jako běžná CC session
- Minimální cron interval: 1 hodina
- Managed Agents (pokročilejší): $0.08/session hour + tokeny

## Connectors

Gmail, Slack, Linear, Google Drive, Asana + všechny MCP servery

## API (RemoteTrigger tool)

- `list`, `get`, `create`, `update`, `run` — funguje z CLI
- Prompt se nepředává v trigger body — musí být v CCR environment (nebo UI)
- Neexistuje DELETE — jen `update {enabled: false}`
- `allowed_tools` je konfigurovatelné na úrovni triggeru

## Regionální omezení

- Cloud sessions mají regionální restrikce (ČR zatím nefunguje, stav 2026-04-15)
- Workaround: VPN na US pro setup, runs běží v cloudu nezávisle
- Docs: "Regional network restrictions: try a VPN or alternative network"

## Migrační plán (lokální tasks → routines)

**Vlna 1 (3-4 runs/den):** morning-watch, tool-radar-scan, weekly-digest
**Vlna 2 (1-2 runs/den):** cross-project-improve-sweep, dependency-audit, project-health, koder-queue
**Vlna 3 (2-3 runs/den):** brain-watch, brain-ingest, daily-rebalancer
**Zůstanou lokální:** autodream, dreams, auto-evolve-skills, weekly-compile, weekly-evolve, memory-maintenance, prompt-evolve, skill-evolution

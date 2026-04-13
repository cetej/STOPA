---
date: 2026-03-26
type: architecture
severity: high
component: orchestration
tags: [channels, telegram, 24x7, syncthing, launchagent, infrastructure, mac-mini]
summary: "Claude Channels has no message queue — messages lost if session not running. Use SyncThing for cross-device sync, LaunchAgent/systemd for persistence."
source: external_research
verify_check: "manual"
confidence: 1.0
uses: 1
successful_uses: 0
harmful_uses: 0
---

# Claude Channels 24/7 Architecture — klíčové vzory

## Zdroj

Virální Instagram reel + podrobný článek o nahrazení OpenClaw Claude Code Channels na Mac Mini.

## Critical: Channels nemá message queue

Pokud CC session neběží, Telegram/Discord zprávy se ZTRATÍ. Žádná fronta, žádný retry.
→ Session MUSÍ běžet 24/7. Každý výpadek = ztracené zprávy.

## SyncThing pro file sync ($0/měsíc)

P2P sync mezi dev laptop a serverem. Žádný cloud. Od 2013, ověřený.

### Co syncovat
- `~/.claude/skills/`
- `~/.claude/commands/`
- `settings.json`
- Knowledge base (Obsidian vault, reference docs)
- MCP tool configs

### Co NE-syncovat (.stignore)
- `settings.local.json` — machine-specific overrides
- `history.jsonl` — per-machine conversation logs
- `projects/` — Claude trackuje dle absolutní cesty (liší se mezi stroji)
- `node_modules`, `.git`, `.env` — bulky, machine-specific, credentials

### Path trick
Stejný username na obou strojích → shodné absolutní cesty → Claude neztrácí project mapping.

## LaunchAgent > cron (macOS)

Cron běží ve stripped-down env bez user session credentials → Claude Code auth selže.
LaunchAgent běží v user session → má přístup k auth.

### Ekvivalenty na jiných OS
- **Linux**: systemd user service (`systemctl --user`)
- **Windows**: Task Scheduler nebo NSSM (Non-Sucking Service Manager)

## Crash recovery pattern

1. LaunchAgent/systemd spouští restart script
2. Script: kill stará tmux session → sleep 2s → nová tmux session → spusť CC s --channels → sleep 20s → pošli "resume monitoring" prompt
3. Daily restart v 4:00 AM (prevence stale session)
4. RunAtLoad = auto-start po rebootu/power outage

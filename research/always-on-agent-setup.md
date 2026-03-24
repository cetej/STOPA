# Always-On Claude Agent — Setup Guide

Datum: 2026-03-24
Status: Research complete, ready to implement

## Přehled možností

| Řešení | Kde běží | Messaging | Persistence | Local files | Setup effort |
|--------|----------|-----------|-------------|-------------|-------------|
| **Claude Code Channels** | Tvůj PC (CLI) | Telegram, Discord | Session-scoped | Ano | Nízký |
| **Remote Control** | Tvůj PC (CLI) | claude.ai/code, mobilní app | Session-scoped | Ano | Minimální |
| **Scheduled Tasks** | Tvůj PC nebo cloud | N/A (cron) | Desktop/cloud: trvalé | Ano (local) | Nízký |
| **OpenClaw** | Tvůj PC (daemon) | 21+ platforem | Trvalé (daemon) | Ano | Střední |

### Doporučení pro tvůj setup

1. **Channels + Remote Control** (nativní, nejjednodušší) — okamžitě použitelné
2. **Scheduled Tasks** — pro automatizaci (daily scans, monitoring)
3. **OpenClaw** — pokud potřebuješ 24/7 daemon + WhatsApp/Signal

---

## 1. Claude Code Channels (Telegram/Discord)

### Requirements
- Claude Code v2.1.80+ (ty máš 2.1.80 ✓)
- claude.ai login (ne API key)
- [Bun](https://bun.sh) nainstalovaný
- Pro/Max subscription

### Setup — Telegram

```bash
# 1. Vytvoř Telegram bota
# Otevři @BotFather v Telegramu, pošli /newbot
# Zvol jméno a username (musí končit na "bot")
# Zkopíruj token

# 2. Nainstaluj plugin v Claude Code
/plugin install telegram@claude-plugins-official

# Pokud nenajde marketplace:
/plugin marketplace add anthropics/claude-plugins-official
/plugin marketplace update claude-plugins-official
# Pak znovu:
/plugin install telegram@claude-plugins-official

# 3. Reload plugins
/reload-plugins

# 4. Nastav token
/telegram:configure <BOT_TOKEN>
# Uloží se do ~/.claude/channels/telegram/.env

# 5. Restartuj s channels
claude --channels plugin:telegram@claude-plugins-official

# 6. Párování
# Pošli zprávu svému botovi v Telegramu
# Bot odpoví pairing kódem
# V Claude Code:
/telegram:access pair <CODE>
/telegram:access policy allowlist
```

### Setup — Discord

```bash
# 1. Vytvoř Discord bota
# https://discord.com/developers/applications → New Application
# Bot section → Reset Token → zkopíruj
# Privileged Gateway Intents → zapni Message Content Intent
# OAuth2 → URL Generator → scope: bot
# Permissions: View Channels, Send Messages, Send Messages in Threads,
#              Read Message History, Attach Files, Add Reactions
# Otevři vygenerovaný URL → přidej bota na server

# 2. Nainstaluj plugin
/plugin install discord@claude-plugins-official

# 3. Reload + konfigurace
/reload-plugins
/discord:configure <BOT_TOKEN>

# 4. Restartuj s channels
claude --channels plugin:discord@claude-plugins-official

# 5. Párování
# Pošli DM botovi na Discordu
/discord:access pair <CODE>
/discord:access policy allowlist
```

### Více channels najednou

```bash
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official
```

### Quickstart test (fakechat — localhost demo)

```bash
/plugin install fakechat@claude-plugins-official
# Restart:
claude --channels plugin:fakechat@claude-plugins-official
# Otevři http://localhost:8787 a pošli zprávu
```

### Důležité poznámky

- **Session-scoped**: channels fungují jen dokud běží Claude Code session
- **Permission prompts**: pokud Claude narazí na permission, session čeká (nebo channel může relay)
- Pro unattended: `--dangerously-skip-permissions` (jen v důvěryhodném prostředí!)
- **Allowlist**: jen spárované účty mohou posílat zprávy
- **Research preview**: zatím jen plugins z claude-plugins-official allowlistu
- Custom channels: `--dangerously-load-development-channels` pro vlastní

---

## 2. Remote Control (ovládání z mobilu/browseru)

### Requirements
- Claude Code v2.1.51+ ✓
- claude.ai login (ne API key)
- Pro/Max/Team/Enterprise subscription

### Setup

```bash
# Varianta A: Server mode (čeká na remote connections)
claude remote-control
claude remote-control --name "STOPA Dev"

# Varianta B: Interaktivní session s remote control
claude --remote-control
claude --remote-control "STOPA Dev"

# Varianta C: Z existující session
/remote-control
/remote-control STOPA Dev
```

### Připojení z jiného zařízení

1. **URL**: terminál zobrazí session URL → otevři v prohlížeči
2. **QR kód**: stiskni mezerník → naskenuj mobilem
3. **claude.ai/code**: najdi session v seznamu (zelená tečka = online)
4. **Claude app**: iOS/Android app → najdi session

### Zapnout pro všechny sessions

```
/config → Enable Remote Control for all sessions → true
```

### Multi-session server mode

```bash
claude remote-control --spawn worktree --capacity 8
# Každá session dostane vlastní git worktree
```

### Omezení
- Session končí když zavřeš terminál
- Timeout po ~10 min bez síťového spojení
- Vyžaduje claude.ai auth (ne API key, ne Bedrock/Vertex)

---

## 3. Scheduled Tasks (automatizace)

### 3 úrovně

| Typ | Persistence | Kde běží | Min. interval |
|-----|-------------|----------|---------------|
| `/loop` (session) | Ne — zmizí po zavření | CLI session | 1 min |
| Desktop tasks | Ano — přežijí restart | Tvůj PC (Desktop app) | 1 min |
| Cloud tasks | Ano — bez tvého PC | Anthropic cloud | 1 hodina |

### Session-scoped (/loop) — pro quick polling

```
# Každých 5 minut zkontroluj deploy
/loop 5m check if the deployment finished and tell me what happened

# Každých 20 minut review PR
/loop 20m /review-pr 1234

# Bez intervalu (default 10 min)
/loop check the build

# One-shot reminder
remind me at 3pm to push the release branch
in 45 minutes, check whether the integration tests passed
```

Správa:
```
what scheduled tasks do I have?
cancel the deploy check job
```

### Cron expressions (CronCreate tool)

| Výraz | Význam |
|-------|--------|
| `*/5 * * * *` | Každých 5 minut |
| `7 * * * *` | Každou hodinu v :07 |
| `0 9 * * 1-5` | Pracovní dny v 9:00 |

**Omezení session-scoped**:
- Funguje jen při běžící session
- 3-day auto-expiry pro recurring
- Max 50 tasků per session

### Cloud scheduled tasks (běží BEZ tvého PC)

Nejvyšší úroveň — běží na Anthropic infrastruktuře, nepotřebuješ zapnutý počítač.

```
# Z CLI:
/schedule                              # interaktivní vytvoření
/schedule daily PR review at 9am       # přímé vytvoření
/schedule list                         # seznam
/schedule run                          # manuální spuštění

# Nebo přes web UI:
# claude.ai/code/scheduled → New scheduled task
```

Setup:
1. Pojmenuj task + napiš self-contained prompt
2. Vyber GitHub repos (klonují se fresh každý run)
3. Zvol schedule: Hourly / Daily / Weekdays / Weekly
4. Připoj MCP connectors (Slack, Linear, Google Drive...)
5. Create

**Omezení**: min. interval 1 hodina, nemá přístup k lokálním souborům (vždy fresh clone).

Příklady promptů pro cloud tasks:
- "Review all open PRs with no activity in 48h, post summary comment"
- "Check CI failures from last night, create Slack summary"
- "Audit package.json for CVEs, open a GitHub issue"

### Desktop scheduled tasks (persistent, s lokálními soubory)

Konfiguruje se v Claude Desktop app → Schedule page. Min. interval 1 minuta, přístup k lokálním souborům. Běží dokud je Desktop app otevřená.

### GitHub Actions (CI/CD)

`schedule` trigger v GitHub Actions workflow — pro plně serverless automatizaci.

---

## 4. OpenClaw (24/7 daemon)

### Requirements
- Node.js 24 (doporučeno) nebo 22.16+
- Windows: WSL2 potřeba
- npm/pnpm/bun

### Instalace

```bash
# Produkční instalace
npm install -g openclaw@latest
openclaw onboard --install-daemon

# Nebo z source:
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
pnpm openclaw onboard --install-daemon
```

### Architektura

```
Messaging Platforms → Gateway (ws://127.0.0.1:18789)
                     ├─ Pi agent (RPC) → Claude API / OpenAI / DeepSeek
                     ├─ CLI interface
                     ├─ WebChat UI
                     ├─ macOS app
                     └─ iOS/Android nodes
```

Gateway běží jako daemon (launchd na macOS, systemd na Linux, WSL2 na Windows).

### Podporované platformy (21+)

WhatsApp (Baileys), Telegram (grammY), Slack (Bolt), Discord (discord.js),
Google Chat, Signal, BlueBubbles (iMessage), IRC, Microsoft Teams, Matrix,
Feishu, LINE, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon,
Twitch, Zalo, WebChat

### Příkazy

```bash
# Spuštění gateway
openclaw gateway --port 18789 --verbose

# Diagnostika
openclaw doctor

# Poslání zprávy
openclaw message send --to +1234567890 --message "Hello"

# Agent interakce
openclaw agent --message "Ship checklist" --thinking high

# Update
openclaw update --channel stable
```

### Chat příkazy (v messaging platformách)

- `/status` — stav session
- `/new` nebo `/reset` — reset session
- `/think <level>` — thinking mode
- `/verbose on|off` — verbose mode

### Bezpečnost

- DM pairing: neznámí uživatelé musí být schváleni pairing kódem
- Per-session elevated access
- Channel allowlisting
- `openclaw doctor` pro audit konfigurace

### Konfigurace s Claude (Anthropic API)

```bash
# Při onboarding wizard — vyber Anthropic, vlož API key z console.anthropic.com
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"

# Nebo environment variable:
export ANTHROPIC_API_KEY="sk-ant-..."
openclaw onboard
```

Config se uloží do `~/.openclaw/openclaw.json`. Doporučené modely:
- `claude-haiku-4-5` — rychlý, levný pro většinu tasků
- `claude-sonnet-4-5` — lepší reasoning pro komplexní úlohy

### Náklady

| Složka | Měsíčně |
|--------|---------|
| Infra (VPS/lokální) | $0-5 |
| API (light use) | $5-20 |
| API (heavy, 24/7) | $50-200+ |
| **Realistický rozsah** | **$6-50/měsíc** |

### Windows specifika

OpenClaw na Windows vyžaduje **WSL2** — nativní Windows daemon není podporován.
1. Nainstaluj WSL2 (`wsl --install`)
2. V WSL nainstaluj Node.js 24 (`nvm install 24`)
3. Spusť `openclaw onboard --install-daemon` v WSL
4. Gateway poběží jako systemd service v WSL

### Omezení
- Filesystem write/edit zamčený na workspace dir (`~/.openclaw/workspace/`)
- WhatsApp/Signal: neoficiální API bridge — riziko banu
- Údržba: ~4-8h initial setup, 2-4h/měsíc ongoing
- Anthropic OAuth zrušen (leden 2026) — jen API key

---

## 5. Kombinovaný setup pro STOPA

### Doporučená konfigurace

```
┌─────────────────────────────────────────────────┐
│ Tvůj PC (Windows 11)                            │
│                                                 │
│  Claude Code session                            │
│  ├─ --channels telegram                         │
│  ├─ --remote-control "STOPA"                    │
│  ├─ /loop 30m /watch quick                      │
│  ├─ STOPA hooks (Slack webhook notifications)   │
│  └─ MCP servers (Gmail, GCal, GitHub, ...)      │
│                                                 │
│  Přístup odkudkoli:                             │
│  ├─ Telegram bot → posílej úkoly z mobilu       │
│  ├─ claude.ai/code → ovládej z browseru         │
│  ├─ Claude app → ovládej z iOS/Android          │
│  └─ Slack → notifikace o session lifecycle      │
└─────────────────────────────────────────────────┘
```

### Spouštěcí skript

```bash
#!/bin/bash
# start-stopa-agent.sh
# Spustí Claude Code jako always-on agent v tmux (přežije odpojení terminálu)

cd /c/Users/stock/Documents/000_NGM/STOPA

# Varianta A: Přímé spuštění
claude \
  --channels plugin:telegram@claude-plugins-official \
  --remote-control "STOPA Agent" \
  --name "STOPA Always-On" \
  --permission-mode auto

# Varianta B: V tmux (doporučeno pro always-on)
# tmux new-session -d -s stopa-agent
# tmux send-keys -t stopa-agent "claude --channels plugin:telegram@claude-plugins-official --remote-control 'STOPA Agent' --permission-mode auto" Enter
# Připojit se: tmux attach -t stopa-agent
# Odpojit se (session běží dál): Ctrl+B, D
```

### Prerekvizity k nastavení

1. [ ] Nainstalovat Bun: `npm install -g bun` nebo https://bun.sh
2. [ ] Vytvořit Telegram bota přes @BotFather
3. [ ] Nainstalovat Telegram plugin: `/plugin install telegram@claude-plugins-official`
4. [ ] Nakonfigurovat token: `/telegram:configure <TOKEN>`
5. [ ] Spárovat účet
6. [ ] Otestovat: poslat zprávu z Telegramu

### Rozšíření (later)

- [ ] Discord channel (pro team notifications)
- [ ] Desktop scheduled tasks (pro daily /watch scans)
- [ ] OpenClaw (pokud potřebuješ WhatsApp/Signal bridge)
- [ ] Custom webhook channel (pro GitHub Actions → Claude)

---

## Reference

- [Channels docs](https://code.claude.com/docs/en/channels)
- [Channels reference (custom)](https://code.claude.com/docs/en/channels-reference)
- [Remote Control docs](https://code.claude.com/docs/en/remote-control)
- [Scheduled Tasks docs](https://code.claude.com/docs/en/scheduled-tasks)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Official channel plugins](https://github.com/anthropics/claude-plugins-official)

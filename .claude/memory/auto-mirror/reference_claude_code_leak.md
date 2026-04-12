---
name: reference_claude_code_leak
description: Claude Code source leak (2026-03-31) — upcoming features KAIROS, PROACTIVE, COORDINATOR_MODE, auto-permissions, new models
type: reference
---

Zdroj: npm @anthropic-ai/claude-code@2.1.88 source map leak (cli.js.map, 59.8 MB). Objevil @Fried_rice na X, 2026-03-31.

## Feature flagy s dopadem na STOPA

| Flag | Popis | Dopad na STOPA |
|------|-------|----------------|
| **KAIROS** (154×) | Autonomous daemon mode — background sessions, "dream" memory consolidation, GitHub webhooks, push notifications | Nahradí scheduled tasks / cron hacky |
| **PROACTIVE** (37×) | Autonomní práce mezi user messages, "tick" prompts, agent rozhoduje co dělat | Změní workflow `/watch`, monitoring |
| **COORDINATOR_MODE** (32×) | Nativní orchestrátor — spawn parallel workers, research/impl/verify delegace | Může nahradit nebo doplnit `/orchestrate` |
| **TRANSCRIPT_CLASSIFIER** (107×) | AI classifier auto-approve tool permissions ("Auto Mode") | Řeší approval fatigue (user feedback) |
| **FORK_SUBAGENT** | Fork sebe do parallel agents | Rychlejší než Agent tool |
| **VERIFICATION_AGENT** | Adversarial verification | Nativní `/critic` |
| **TOKEN_BUDGET** | Explicit budget commands (+500k, "spend 2M tokens") | Doplní `/budget` |
| **TEAMMEM** | Team memory sync across users | Sdílená memory pro týmy |
| **VOICE_MODE** (46×) | STT + TTS integrace | Hands-free coding |
| **ULTRAPLAN** | Advanced planning | Rozšíří plan mode |
| **WEB_BROWSER_TOOL** | Browser automation nativně | Nahradí MCP browse |

## Model codenames

- **Capybara** = Claude 4.6 variant (v8 aktuální, problémy: 29-30% false claims vs v4 16.7%, over-commenting)
- **Fennec** = migrováno na Opus 4.6
- **Numbat** = unreleased ("Remove this section when we launch numbat")
- **opus-4-7, sonnet-4-8** = existují interně (nesmí být v public commits)

## Ostatní

- **Undercover Mode** — Anthropic zaměstnanci v public repos, stripuje AI attribution, default ON
- **BUDDY system** — Tamagotchi pet (18 species, rarity tiers, stats: DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK)
- Bash command validation: 2,500+ řádků security kódu

## Actionable env vars a flagy (ověřeno 2026-04-01)

| Nastavení | Hodnota | Efekt | Status |
|-----------|---------|-------|--------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | `70` | Kompakce dřív → čistší kontext v dlouhých sessions | **Aktivní v settings.json** |
| `--bare` flag | CLI arg | Skip hooks/plugins/memory → ~10x rychlejší start pro one-off dotazy | Dostupné |
| `--dump-system-prompt` | CLI arg | Vypíše celý system prompt a skončí — debug/audit | Dostupné |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `0` | Vypne telemetrii | Dostupné |
| `CLAUDE_CODE_UNATTENDED_RETRY` | `1` | Auto-retry při rate limitu (429/529) | Dostupné |

## 4-tier compaction model

1. **Snip** — historická truncation, zachovává prompt cache
2. **Microcompaction** — time/size-based clearing tool results ("[content cleared]")
3. **Full compaction** — sumarizace konverzace, trigger přes AUTOCOMPACT_PCT nebo /compact
4. **Reactive collapse** — emergency na API 413, agresivní shrink

**Why:** Vysvětluje degradaci v dlouhých sessions. Nižší AUTOCOMPACT_PCT = častější ale menší kompakce = lepší kvalita.

**How to apply:** Sledovat GA release KAIROS a COORDINATOR_MODE — přepíše architekturu scheduled tasků a možná i custom orchestrace. Aktualizovat tier tabulku v CLAUDE.md při nových modelech. Proaktivně používat `/compact` na přirozených breakpointech. Pro quick one-off dotazy (regex, error lookup) použít `claude --bare`.

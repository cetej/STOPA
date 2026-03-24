# Jarvis Implementation Plan — STOPA Meta-Agent

**Datum**: 2026-03-24
**Prerekvizita**: `research/jarvis-gap-analysis-2026-03-24.md`
**Přístup**: Fix first, then enhance — 5 fází od hygieny po plnou autonomii

---

## Phase 1: Hygiena + Bug Fixes (1 session, ~30 min)

**Cíl**: Uvést systém do čistého stavu, opravit porušení pravidel.

| # | Úkol | Typ | Effort | Impact |
|---|------|-----|--------|--------|
| 1.1 | Archivovat permission-log.md (642→<300 řádků) | Bug fix | 5 min | Compliance |
| 1.2 | Maintenance news.md — archivovat staré záznamy | Bug fix | 5 min | Compliance |
| 1.3 | Vyčistit stale memory soubory (5 souborů) | Cleanup | 10 min | Čistota |
| 1.4 | Sync permission-auto-approve.sh do pluginu (v2→plugin) | Bug fix | 5 min | Konzistence |
| 1.5 | Opravit plugin.json (8→11 skills v popisu) | Bug fix | 2 min | Přesnost |
| 1.6 | Fix observe.sh duplikace (Pre+Post→jen Post) | Optimization | 3 min | Performance |
| 1.7 | Update budget.md (stale od 2026-03-20) | Bug fix | 2 min | Compliance |

### Detail 1.3 — Stale memory soubory

| Soubor | Řádky | Akce | Důvod |
|--------|-------|------|-------|
| czech_corrector_plan.md | 161 | Přesunout do research/ | Projekt-specifický, ne STOPA orchestrace |
| implementation-plan.md | 89 | Smazat nebo archivovat | Všechny items DONE |
| competitive-spec-kit.md | 98 | Přesunout do research/ | Jednorázový výstup /watch |
| project_zachvev.md | 16 | Přesunout do research/ | Patří do ZACHVEV projektu |
| feedback_checkpoints.md | 16 | Sloučit do learnings/ | Obsahuje 2 poučení o checkpointech |

### Detail 1.4 — permission-auto-approve sync

**Rozhodnutí k diskuzi**: Sync v2 (84 řádků) do pluginu, nebo ponechat záměrně konzervativnější v1?
- **Doporučení**: Sync v2 → plugin. Uživatel pluginu může overridnout přes hook profile.
- **Alternativa**: Vytvořit v1.5 — plugin verze s opt-in pro rozšířené auto-approve.

---

## Phase 2: Always-On Agent (1-2 sessions, ~2h)

**Cíl**: Dosáhnout dostupnosti odkudkoli — Telegram + Remote Control.
**Prerekvizita**: Research kompletní v `research/always-on-agent-setup.md`

| # | Úkol | Effort | Impact | Závislosti |
|---|------|--------|--------|------------|
| 2.1 | Nainstalovat Bun runtime | 5 min | Prereq | - |
| 2.2 | Vytvořit Telegram bota (@BotFather) | 10 min | Prereq | Manuální krok uživatele |
| 2.3 | Install + configure Telegram plugin | 15 min | HIGH | 2.1, 2.2 |
| 2.4 | Spárovat účet + otestovat | 10 min | HIGH | 2.3 |
| 2.5 | Zapnout Remote Control pro všechny sessions | 5 min | HIGH | - |
| 2.6 | Vytvořit spouštěcí skript (start-stopa-agent.sh) | 15 min | MEDIUM | 2.3, 2.5 |
| 2.7 | Scheduled task: daily /watch quick (9:00) | 15 min | MEDIUM | - |
| 2.8 | Push notifikace přes Telegram po dokončení tasku | 30 min | HIGH | 2.3 |
| 2.9 | Otestovat end-to-end: mobilní Telegram → úkol → notifikace | 15 min | Validace | 2.1-2.8 |

### Spouštěcí skript (draft)

```bash
#!/bin/bash
# start-stopa-agent.sh — Always-on STOPA agent
cd /c/Users/stock/Documents/000_NGM/STOPA
claude \
  --channels plugin:telegram@claude-plugins-official \
  --remote-control "STOPA Agent" \
  --name "STOPA Always-On"
```

### Doporučení

- **Telegram jako primární kanál** — nejrychlejší setup, mobilní notifikace zdarma
- **Remote Control jako doplněk** — pro složitější interakce z browseru
- **Discord zatím ne** — zbytečná duplikace, přidat později pro team scenáře
- **OpenClaw zatím ne** — overkill pro 1 uživatele, vyžaduje WSL2

### Jarvis milestone po Phase 2
> "Sir, I'm available on your phone. Send me tasks via Telegram, control me from your browser, and I'll brief you every morning."

---

## Phase 3: Cross-Project Intelligence (2-3 sessions, ~4h)

**Cíl**: Agent zná všechny tvoje projekty a přenáší znalosti mezi nimi.

| # | Úkol | Effort | Impact | Popis |
|---|------|--------|--------|-------|
| 3.1 | Globální memory v ~/.claude/memory/ | 1h | HIGH | Cross-project learnings, user preferences, project registry |
| 3.2 | Project registry (projects.json) | 30 min | HIGH | JSON se všemi projekty: cesta, repo URL, stav, poslední aktivita, tech stack |
| 3.3 | Cross-project search skill | 1h | HIGH | /xsearch — grep across registered projects |
| 3.4 | Vytvořit .claude/agents/ | 1h | MEDIUM | validator, architecture, code-learner (referencované v CLAUDE.md) |
| 3.5 | Globální learnings sync | 30 min | MEDIUM | Hook: po zápisu do lokálního learnings/ → kopie do ~/.claude/memory/learnings/ |

### Project Registry (draft)

```json
{
  "projects": [
    {
      "name": "STOPA",
      "path": "C:/Users/stock/Documents/000_NGM/STOPA",
      "repo": "cetej/STOPA",
      "type": "meta-orchestration",
      "stack": ["claude-code", "bash", "python"],
      "lastActivity": "2026-03-24",
      "status": "active"
    },
    {
      "name": "NG-ROBOT",
      "path": "C:/Users/stock/Documents/000_NGM/NG-ROBOT",
      "repo": "cetej/NG-ROBOT",
      "type": "content-pipeline",
      "stack": ["python", "openai", "wordpress"],
      "lastActivity": "2026-03-20",
      "status": "active"
    }
  ]
}
```

### Doporučení

- **Globální memory = game changer** — "V NG-ROBOT jsem narazil na stejný bug" → přenos řešení
- **Project registry** umožní scheduled tasks jako "projdi všechny projekty a zkontroluj stav"
- **Agents directory** odblokuje automatické spouštění validátorů (CLAUDE.md na to odkazuje)

### Jarvis milestone po Phase 3
> "I noticed the same pattern in NG-ROBOT that caused a bug in ADOBE-AUTOMAT last week. Shall I apply the fix?"

---

## Phase 4: Proaktivní Partner (3-4 sessions, ~8h)

**Cíl**: Agent přechází z reaktivního na proaktivní — navrhuje, analyzuje, upozorňuje.

| # | Úkol | Effort | Impact | Popis |
|---|------|--------|--------|-------|
| 4.1 | Post-commit analyzer hook | 2h | HIGH | Po git commit: "tohle může rozbít X" — backward compat, API changes |
| 4.2 | Priority rebalancer (scheduled task) | 2h | HIGH | Denní review: stav projektů, nesplněné úkoly, návrh co dělat dnes |
| 4.3 | Verbosity modes | 1h | MEDIUM | brief (Telegram: max 200 znaků), standard (CLI), detailed (planning) |
| 4.4 | Sémantické vyhledávání v learnings | 3h | MEDIUM | Embeddings-based retrieval místo grep (lepší recall) |
| 4.5 | Monitoring skill (/monitor) | 2h | MEDIUM | Health checks pro produkční projekty, alert routing |

### Post-commit analyzer (draft)

```bash
# Hook: PostToolUse (matcher: Bash, command contains "git commit")
# 1. Extrahuj diff posledního commitu
# 2. Analyzuj: breaking changes, security, API surface
# 3. Pokud risky → inject warning do kontextu
```

### Priority rebalancer (draft)

```
Scheduled task: daily 9:00
1. Přečti project registry
2. Pro každý aktivní projekt: git log --since=7d, open issues, stale branches
3. Sestav prioritizovaný seznam: "Dnes doporučuji: 1) PR review v NG-ROBOT, 2) Fix issue #12 v test1"
4. Pošli přes Telegram
```

### Doporučení

- **Post-commit analyzer je highest-impact** — prevence > oprava
- **Priority rebalancer** dělá z agenta strategického partnera, ne jen executora
- **Verbosity modes** zlepší Telegram UX dramaticky (teď by posílal walls of text)
- **Sémantické vyhledávání** je nice-to-have — grep funguje dobře pro structured YAML

### Jarvis milestone po Phase 4
> "Good morning. I analyzed your last commit — the API endpoint rename breaks 2 clients. Today I suggest: fix that first, then the NG-ROBOT content pipeline issue from yesterday."

---

## Phase 5: Plná Autonomie (vision, 5+ sessions)

**Cíl**: Agent běží 24/7, spravuje projekty proaktivně, učí se implicit preferences.

| # | Úkol | Effort | Impact | Popis | Status |
|---|------|--------|--------|-------|--------|
| 5.1 | 24/7 daemon (cloud scheduled tasks nebo OpenClaw) | 4-8h | VERY HIGH | Non-stop availability | BACKLOG |
| 5.2 | Multi-project orchestrace | Výzkum | HIGH | /project-sweep skill — health, deps, git cleanup | DONE |
| 5.3 | Implicit preference learning | Výzkum | MEDIUM | Bi-weekly preference-learner scheduled task | DONE |
| 5.4 | Weekly digest report | 2h | HIGH | weekly-digest scheduled task (Po 8:04) | DONE |
| 5.5 | Voice interface (Whisper + TTS) | Výzkum | LOW | Hands-free interakce | BACKLOG |
| 5.6 | Self-evolving skills | Výzkum | MEDIUM | skill-usage-tracker hook + skill-evolution monthly task | DONE |

### Implementováno (2026-03-24)

- **5.4 Weekly digest**: Scheduled task `weekly-digest` (Po 8:04) — project activity, news summary, learnings, memory health, priorities
- **5.2 Multi-project orchestrace**: `/project-sweep` skill — health checks, dependency audit, git cleanup, lint-config, custom commands across all registered projects
- **5.3 Preference learning**: Scheduled task `preference-learner` (1. a 15. v měsíci) — analyzuje git patterns, skill usage, decisions; navrhuje (neauto-zapisuje) nové preference
- **5.6 Self-evolving skills**: Hook `skill-usage-tracker.sh` loguje skill invocations do JSONL + scheduled task `skill-evolution` (1. v měsíci) analyzuje usage a navrhuje archivaci/optimalizaci

### Zbývá (backlog)

- **5.1 24/7 daemon** — vyžaduje cloud infra (Anthropic scheduled tasks, OpenClaw, nebo vlastní server)
- **5.5 Voice interface** — závisí na externím tooling (Whisper + TTS), nízká priorita

### Jarvis milestone po Phase 5
> "Good morning sir. While you slept, I resolved 3 dependabot PRs, NG-ROBOT build is green, and CascadeWatch found an interesting signal I'd like to discuss. Your schedule today has a 2-hour gap at 14:00 — shall I use it for the ADOBE-AUTOMAT refactor?"

---

## Prioritizace — Doporučené pořadí

```
Phase 1 (Hygiena)        ████████████ 30 min  — TEĎ (odblokuje vše ostatní)
Phase 2 (Always-On)      ████████████████ 2h  — PŘÍŠTÍ SESSION (biggest UX jump)
Phase 3 (Cross-Project)  ████████████████████ 4h  — po stabilizaci Phase 2
Phase 4 (Proaktivní)     ████████████████████████████ 8h  — iterativně
Phase 5 (Autonomie)      ████████████████████████████████████ 15h+  — long-term vision
```

### Rizika

| Riziko | Pravděpodobnost | Mitigace |
|--------|----------------|----------|
| Telegram plugin nestabilní (research preview) | Střední | Fallback na Remote Control |
| Token cost escalation s always-on | Vysoká | Budget tier + /budget skill monitoring |
| Cross-project memory příliš velká | Nízká | Stejná governance (500-line limit, archivace) |
| Over-engineering before validation | Střední | Implementovat po jedné fázi, validovat real-world |

### Metriky úspěchu

| Fáze | Metrika | Cíl |
|------|---------|-----|
| Phase 1 | Memory health score | A (95+/100) |
| Phase 2 | Úkol zadaný z mobilu → dokončený | <5 min response time |
| Phase 3 | Cross-project learning transfer | 1+ per týden |
| Phase 4 | Proaktivní upozornění | 3+ per týden |
| Phase 5 | Autonomní resolved issues | 5+ per týden |

---

## Quick Reference — Co dělat teď

```
1. /orchestrate Phase 1 (hygiena) — 30 min, 7 subtasků
2. Po dokončení: commit + push
3. Příští session: Phase 2 (Telegram setup — manuální kroky uživatele)
```

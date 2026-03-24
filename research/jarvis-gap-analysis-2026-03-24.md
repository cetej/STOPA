# STOPA Meta-Agent — Kompletní Audit + Jarvis Gap Analysis

**Datum**: 2026-03-24
**Stav**: Analýza kompletní, implementační plán připraven
**Metoda**: 3 paralelní audit agenti + manuální analýza

---

## 1. Aktuální stav systému

### Metriky

| Komponenta | Počet | Poznámka |
|------------|-------|----------|
| Skills (always-loaded) | 11 | Tier 1-3 |
| Commands (on-demand) | 17 | commands-over-skills split částečně implementován |
| Hook scripts | 15 | 9 event types |
| Memory files | 18 + 11 learnings | ~280K celkem |
| Rules | 4 | memory, python, skill-files, skill-tiers |
| Harnesses | 1 | skill-audit (score 3.9/5) |
| Plugin version | 2.1.0 | GitHub marketplace distribuce |
| Plugin skill sync | 100% | Všech 11 SKILL.md identických |
| Plugin hook sync | ~76% | 1 major drift (permission-auto-approve) |
| Memory health | B+ (87/100) | 1 file over limit, budget stale |

### Skills (11 source / 11 plugin)

| Skill | Tier | Řádky | Popis |
|-------|------|-------|-------|
| orchestrate | 1 | 686 | Multi-step decomposition, budget tiers, Agent Teams |
| scout | 1 | 154 | Codebase exploration |
| critic | 1 | 257 | Quality review |
| checkpoint | 1 | 186 | Session continuity |
| scribe | 1 | 138 | Decision/learning capture |
| verify | 2 | 127 | End-to-end proof |
| fix-issue | 2 | 126 | GitHub issue resolution |
| incident-runbook | 2 | 55 | Failure diagnosis |
| scenario | 2 | 201 | Edge case exploration |
| compact | 2 | 146 | Context compaction |
| seo-audit | 2 | 277 | Domain-specific |

### Hooks (17 skriptů, 9+ event types)

| Event | Hooks | Účel |
|-------|-------|------|
| SessionStart | checkpoint-check, memory-maintenance, memory-brief | Load stav, health check, brief |
| PreToolUse | dippy (Bash only), observe | Pre-flight checks |
| PostToolUse | activity-log, suggest-compact, observe, ruff-lint | Logging, kompakce, linting |
| PermissionRequest | permission-auto-approve | Auto-approve safe permissions |
| UserPromptSubmit | skill-suggest.py | Skill suggestions |
| Stop | scribe-reminder, cost-tracker | Learnings, cost |
| TaskCompleted | task-completed | Automation trigger |
| TeammateIdle | teammate-idle | Quality gate |
| StopFailure | stop-failure | Crash recovery |
| PostCompact | post-compact | Checkpoint reminder |

### Hook Profiles

| Profil | Level | Co běží |
|--------|-------|---------|
| minimal | 1 | checkpoint, memory-brief, activity-log |
| standard | 2 (default) | + cost-tracker, suggest-compact, scribe-reminder |
| strict | 3 | + observe, ruff-lint, all quality gates |

### Memory systém

| Soubor | Řádky | Stav |
|--------|-------|------|
| permission-log.md | 642 | OVER LIMIT (>500) |
| czech_corrector_plan.md | 161 | Stale, jednorázový plan |
| news.md | 142 | Needs maintenance |
| news-archive.md | 139 | OK |
| competitive-spec-kit.md | 98 | One-time artifact |
| implementation-plan.md | 89 | Stale (all items DONE) |
| checkpoint.md | 75 | Current |
| decisions.md | 48 | OK (7 active) |
| budget.md | 28 | Stale (od 2026-03-20) |
| learnings/ | 11 files | OK, YAML format, score B+ |

---

## 2. Nalezené problémy

### Kritické

1. **permission-log.md = 642 řádků** — porušuje 500-line limit, potřebuje archivaci
2. **news.md = 142 řádků** — hook hlásí potřebu maintenance
3. **Stale memory soubory**: czech_corrector_plan.md, implementation-plan.md, project_zachvev.md, competitive-spec-kit.md, feedback_checkpoints.md — jednorázové artefakty

### Střední

4. **observe.sh duplikace** — běží v PreToolUse I PostToolUse (dvojitý overhead)
5. **permission-auto-approve.sh major drift**: source v2.0 (84 řádků, 11 branches) vs plugin v1 (37 řádků, 4 branches)
6. **Plugin manifest mismatch**: plugin.json říká "8 skills" ale obsahuje 11
7. **4 hook path diffs** (source `.claude/hooks/` vs plugin `hooks/` — expected pro distribuce)
8. **Chybí .claude/agents/** — globální CLAUDE.md odkazuje na validator/architecture agenty

### Nízké

9. **activity-log.md = 7 řádků** — nepoužívá se aktivně
10. **budget.md stale** od 2026-03-20 (4 dny)
11. **budget-archive.md a decisions-archive.md** — prázdné (jen headers)

---

## 3. Jarvis Gap Analysis

### A) Proaktivita

| Jarvis schopnost | STOPA stav | Gap |
|------------------|-----------|-----|
| Sám upozorní na problémy | Částečně (hooks) | Chybí: monitoring externích zdrojů real-time |
| Navrhne řešení dřív než se zeptáš | Částečně (skill-suggest.py) | Chybí: post-commit analýza "co by mohlo rozbít" |
| Sleduje kontext průběžně | Ne (jen session start) | Chybí: continuous awareness (scheduled tasks) |
| Připomíná nesplněné úkoly | Částečně (checkpoint) | Chybí: deadline tracking, priority rebalancing |

### B) Paměť a Kontinuita

| Jarvis schopnost | STOPA stav | Gap |
|------------------|-----------|-----|
| Pamatuje si across sessions | Dobře (checkpoint + learnings) | Chybí: sémantické vyhledávání |
| Učí se z chyb | Dobře (COMPOUND loop) | Chybí: automatická deduplikace |
| Zná preference | Částečně (CLAUDE.md) | Chybí: implicit preference learning |
| Zná všechny projekty | Ne — izolované sessions | VELKÝ GAP: žádný cross-project context |

### C) Komunikace

| Jarvis schopnost | STOPA stav | Gap |
|------------------|-----------|-----|
| Dostupný odkudkoli | Připraveno (research) | Chybí: implementace Telegram/remote |
| Přirozený dialog | Omezený (CLI) | Chybí: voice, notifikace, mobilní UX |
| Různé verbosity | Ne | Chybí: brief/standard/detailed modes |
| Proaktivní status updates | Částečně (slack webhook) | Chybí: push notifikace na mobil |

### D) Multi-domain kompetence

| Jarvis schopnost | STOPA stav | Gap |
|------------------|-----------|-----|
| Kódování + review + deploy | Silné | OK |
| Monitoring produkce | Ne | GAP: no observability skill |
| Finanční přehled | Ne (jen agent budget) | Chybí: API billing alerts |
| Komunikace s týmem | Částečně (Agent Teams) | Chybí: Slack/email notifikace |
| Plánování a scheduling | Částečně (GCal MCP) | Chybí: time management skill |

### E) Autonomie

| Jarvis schopnost | STOPA stav | Gap |
|------------------|-----------|-----|
| Deleguje sub-úkoly | Silné (orchestrate + Teams) | OK |
| Běží bez dozoru | Ne — session-scoped | VELKÝ GAP: žádný always-on daemon |
| Self-healing | Částečně (stop-failure hook) | Chybí: auto-restart, retry |
| Scheduled úkoly | Ne (jen research) | GAP: neimplementovány |

---

## 4. Silné stránky

- Orchestrační loop (PLAN→WORK→ASSESS→COMPOUND) je propracovaný
- Hook systém pokrývá celý lifecycle (17 skriptů, 9+ events)
- Skills dobře strukturované s YAML frontmatter a tier systémem
- Memory má jasnou architekturu s governance rules
- Plugin distribuce funkční a v syncu (skills 100%)
- Research thorough (always-on setup, awesome-claude-code analysis)
- Hook profiles (minimal/standard/strict) pro flexibilitu
- Commands-over-skills split již částečně implementován

## 5. 3 Největší gapy k Jarvisovi

1. **Není always-on** — session-scoped, nedostupný z mobilu, žádné scheduled tasks
2. **Izolované projekty** — žádný cross-project context, žádný globální přehled
3. **Reaktivní, ne proaktivní** — čeká na příkazy, neskenuje, nenavrhuje

---

## 6. Implementační roadmapa

Viz `research/jarvis-implementation-plan.md`

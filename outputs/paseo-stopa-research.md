# Paseo → STOPA: Vzory pro vylepšení orchestrace — Research Brief

**Date:** 2026-04-14
**Question:** Jaké vzory z Paseo a širšího ekosystému mohou vylepšit STOPA orchestrační systém?
**Scale:** comparison
**Sources consulted:** 12 (4 primary reads, 8 discovery)

## Executive Summary

Paseo (getpaseo/paseo) je open-source multi-provider orchestrátor pro Claude Code, Codex a OpenCode s mobilním klientem. Analýza identifikuje **8 konkrétních vzorů** adoptovatelných do STOPA, z nichž 5 řeší skutečné gapy a 3 validují existující STOPA přístupy jako silnější alternativy. Nejdůležitější adopční kandidáti: **(1) heartbeat scheduler pro dlouhé orchestrace** [VERIFIED], **(2) plan-on-disk pro přežití compaction** [VERIFIED], **(3) post-PR CI monitoring loop** [VERIFIED]. STOPA je architektonicky silnější v memory systému, learnings retrieval a coordinator enforcement — Paseo řeší distribuci a multi-device přístup, ne znalostní management.

---

## Detailed Findings

### 1. Event-Driven vs Blokující Agent Model

**Paseo pattern:** `background: true` + `notifyOnFinish: true` na každém agentovi. Orchestrátor nečeká — dostane callback [VERIFIED][Paseo SKILL.md].

**MCP Tasks spec** definuje call-now/fetch-later model: MCP server vrátí `taskId` okamžitě, klient polluje nezávisle. State machine: `submitted → working → input_required → completed/failed` [VERIFIED][3].

**Temporal Signals** poskytují guaranteed delivery across process restarts — fire-and-forget feedback injection [VERIFIED][2].

**STOPA stav:** CC `Agent()` tool je inherentně blokující (vrátí result). `run_in_background: true` existuje, ale orchestrate skill ho nepoužívá systematicky.

**Doporučení:** STOPA už má `run_in_background: true` v Agent tool — problém není infrastruktura, ale skill design. Orchestrate skill by měl spouštět agenty s `run_in_background: true` a pokračovat dalšími nezávislými subtasky. Žádná nová infrastruktura potřeba.

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P1** | Nízký (skill edit) | Střední — paralelizace čekání |

---

### 2. Heartbeat Scheduler pro Dlouhé Orchestrace

**Paseo pattern:** `paseo create schedule name: "heartbeat-<slug>" every: "5m" expiresIn: "4h"`. Heartbeat re-reads plan z disku, listuje agenty, kontroluje status, course-correctuje [VERIFIED][Paseo SKILL.md].

**MindStudio:** 4-fázový cyklus Wake→Observe→Reason→Act kde LLM nahrazuje hardcoded rozhodovací logiku [VERIFIED][1]. Klíčové: interval musí respektovat API rate limits.

**CORAL (existující STOPA learning):** Heartbeat-triggered mid-run steering validován — odlišný od critica (critic hodnotí output, heartbeat mění direction) [VERIFIED][STOPA learning 2026-04-08].

**Mendonca pattern:** Hierarchický heartbeat přes rekurzivní self-delegation: diastole (fan out) → systole (aggregate up). Terminace role-driven, ne depth-driven [INFERRED][4].

**STOPA stav:** Žádný periodický self-check pro běžící orchestrace. `CronCreate` tool existuje, `/loop` skill existuje, ale orchestrate ho nepoužívá.

**Doporučení:** Přidat heartbeat do orchestrate Phase 6 (Setup). Implementace přes `CronCreate` nebo `ScheduleWakeup`:

```
Po spuštění implementačních agentů:
1. CronCreate("*/5 * * * *", "Heartbeat: přečti state.md, zkontroluj agenty, course-correct")
2. Po dokončení orchestrace: CronDelete
```

**Klíčové pravidlo z MCP spec [3]:** Push notifikace jsou speed hints, ne zdroj pravdy — vždy reconcilovat proti source of truth (state.md) [VERIFIED][3].

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P1** | Střední (skill edit + cron) | Vysoký — self-healing orchestrací |

---

### 3. Plan Persistence na Disk (Survives Compaction)

**Paseo pattern:** Plan persisted do `~/.paseo/plans/<task-slug>.md`. Explicitně: "The plan file on disk is the source of truth. Re-read before every verification and QA phase. It survives compaction." [VERIFIED][Paseo SKILL.md].

**STOPA stav:** `state.md` slouží jako shared state pro orchestraci, ale není explicitně navržen k přežití compaction. Plan je součástí konverzačního kontextu, ne souboru.

**Doporučení:** Při orchestrate Phase 4 (Plan): zapsat finální plán do `.claude/memory/intermediate/orchestrate-plan.md`. Každý agent re-reads plan z tohoto souboru. Při compaction: plan přežije na disku.

```
Phase 4: Write plan → .claude/memory/intermediate/orchestrate-plan.md
Phase 7+: Each agent reads plan from disk before starting work
Heartbeat: Re-reads plan as source of truth
```

Toto už STOPA částečně dělá (post-it pattern v memory-files.md), ale orchestrate ho explicitně nepoužívá.

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P1** | Nízký (skill edit) | Vysoký — reliability |

---

### 4. Post-PR CI Monitoring Loop

**Paseo pattern:** Po vytvoření PR heartbeat přechází do CI monitoring mode. `gh pr checks <pr-number>` → pokud fail: launch fix agent → push fix → CI re-run. Heartbeat se smaže až po ALL checks green [VERIFIED][Paseo SKILL.md].

**STOPA stav:** `/autofix` skill existuje pro fixování CI failures, ale není integrován do orchestrate flow. Orchestrate vytvoří PR a skončí.

**Doporučení:** Rozšířit orchestrate Phase 11 (Deliver): po PR creation spustit CI watch loop:

```
1. `gh pr create ...`
2. Loop: `gh pr checks <nr>` --watch
3. If fail: spawn fix agent, push fix, continue loop
4. If all green: report success
```

Alternativně: delegovat na `/autofix` s PR číslem.

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P2** | Střední (skill + integration) | Střední — eliminuje broken PRs |

---

### 5. Cross-Provider Worker/Verifier

**Paseo pattern:** `--provider codex/gpt-5.4` pro workera, `--verify-provider claude/opus` pro verifier. "Each catches the other's blind spots." [VERIFIED][Paseo SKILL.md].

**Empirická podpora:** Society of Thought (Kim et al., arXiv:2601.10825): heterogenita perspektiv → výkon. Critic s odlišným system promptem empiricky validován [INFERRED][STOPA learning 2026-03-30].

**STOPA stav:** Critic = stejný model jako worker. CC nemá nativní multi-provider support — Paseo to řeší přes vlastní daemon, STOPA by musela řešit jinak.

**Doporučení:** Pro STOPA je multi-provider orchestrace out of scope (STOPA běží uvnitř CC, ne nad ním). Ale heterogenní verification se dá přiblížit:

- **Critic s odlišným system promptem** (už v learnings jako validovaný vzor)
- **Model override v Agent():** `model: "haiku"` vs `model: "opus"` pro worker vs verifier
- **Advisor tool** (Anthropic): Opus jako advisor pro Sonnet executory

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P3** | Nízký (existing tools) | Střední — blind spot reduction |

---

### 6. Read-Only Coordinator Enforcement

**Paseo:** Behaviorální enforcement — skill says "you do NOT edit code" ale žádný tool deny-list [VERIFIED][Paseo SKILL.md, Reading-2].

**TAKT** (github.com/nrslib/takt, 947 stars): YAML workflow s `edit: false` per step — strukturálně vynuceno na CLI úrovni [VERIFIED][Reading-2].

**STOPA stav:** `permission-tier: coordinator` s `deny-tools: [Bash, Write, Edit]` — strukturálně silnější než Paseo, srovnatelné s TAKT [VERIFIED][STOPA skill-files.md].

**Závěr:** STOPA je v tomto bodě PŘED Paseo. Žádná akce potřeba — stávající mechanismus je dostatečný.

---

### 7. Grill Phase (Structured Interview Before Research)

**Paseo:** Grill = depth-first decision tree interview s uživatelem, provedený PŘED research fází. "Research the codebase first to avoid asking questions the code can answer." [VERIFIED][Paseo SKILL.md].

**STOPA stav:** Orchestrate nemá explicitní Grill fázi. Přechází od triage rovnou na scout/plan. Výsledek: občas scout hledá špatnou věc, protože uživatelské zadání je vágní.

**Doporučení:** Přidat lightweight Grill fázi do orchestrate — ale respektovat STOPA Behavioral Genome ("Neptej se krok po kroku"):

```
Phase 2.5 (Grill - only in default mode, not --auto):
1. Grep codebase for context (5 queries max)
2. Identifikuj 1-3 klíčové decision points
3. Polož JE JEDNOU jako batch (ne po jedné)
4. Pokud vše jasné z kódu → skip Grill entirely
```

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P2** | Nízký (skill edit) | Střední — eliminuje scope drift |

---

### 8. Preferences/Config Persistence

**Paseo:** `~/.paseo/orchestrate.json` — persisted user preferences pro modely, providers [VERIFIED][Paseo SKILL.md].

**STOPA stav:** Žádný dedicated preferences soubor pro orchestraci. Model selection je per-session (behavioral genome rules).

**Doporučení:** STOPA má auto-memory systém, key-facts.md a decisions.md — přidání dalšího config souboru je zbytečné. Orchestration preferences patří do `key-facts.md` nebo auto-memory feedback.

| Priorita | Effort | Impact |
|----------|--------|--------|
| **P4** | Skip | Nízký — existující systémy stačí |

---

## Adopční Plán

### Wave 1 — Quick Wins (P1, skill edits only)

| # | Akce | Soubor | Effort |
|---|------|--------|--------|
| 1 | Plan-on-disk: orchestrate zapisuje plan do `intermediate/orchestrate-plan.md` | orchestrate SKILL.md | 30 min |
| 2 | Background agents: orchestrate spouští agenty s `run_in_background: true` | orchestrate SKILL.md | 30 min |
| 3 | Heartbeat: orchestrate přidá CronCreate po spuštění implementačních agentů | orchestrate SKILL.md | 1h |

### Wave 2 — Integrations (P2)

| # | Akce | Soubor | Effort |
|---|------|--------|--------|
| 4 | Post-PR CI loop: orchestrate deliver fáze integruje `/autofix` | orchestrate SKILL.md | 2h |
| 5 | Lightweight Grill: batch questions fáze | orchestrate SKILL.md | 1h |

### Wave 3 — Optimization (P3)

| # | Akce | Soubor | Effort |
|---|------|--------|--------|
| 6 | Heterogenní verification: critic s model override (haiku worker, opus critic) | critic SKILL.md, orchestrate | 1h |

### Skip

- Multi-provider routing (Paseo-specific, out of scope pro CC-native STOPA)
- Config persistence file (existující systémy stačí)
- Dynamic provider registry (overkill)

---

## STOPA Výhody (co Paseo nemá)

1. **Learnings system** s confidence, maturity, decay, graduation — Paseo nemá žádný persistent knowledge systém
2. **Hybrid retrieval** (BM25 + grep + graph walk) — Paseo plans jsou jen flat markdown
3. **Behavioral Genome** — distilled identity přes kompresi; Paseo jen CLAUDE.md
4. **Core Invariants** — compression-proof rules; Paseo nemá ekvivalent
5. **Auto-evolve** — learnings → critical-patterns graduation pipeline
6. **Dreams consolidation** — cross-session memory linking
7. **CORAL shared state** pattern (z literatury, partially implemented)
8. **Skill lifecycle** (draft → validated → core maturity tiers)
9. **50+ skills** vs Paseo's 6 experimentálních
10. **Budget tracking** — Paseo nemá cost awareness

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | MindStudio Heartbeat | https://www.mindstudio.ai/blog/agentic-os-heartbeat-pattern-proactive-ai-agent | 4-phase heartbeat: Wake→Observe→Reason→Act; LLM v reason phase | primary | high |
| 2 | Temporal Ambient Agents | https://temporal.io/blog/orchestrating-ambient-agents-with-temporal | Signals = guaranteed async delivery across restarts | primary | high |
| 3 | WorkOS MCP Tasks | https://workos.com/blog/mcp-async-tasks-ai-agent-workflows | call-now/fetch-later; tasks/get = source of truth, notifications = hints | primary | high |
| 4 | Mendonca Heartbeat | https://medium.com/@marcilio.mendonca/the-agentic-heartbeat-pattern | Recursive self-delegation: diastole/systole phases | primary | medium |
| 5 | TAKT Framework | https://github.com/nrslib/takt | YAML workflow s `edit: false` per step — read-only coordinator structural enforcement | primary | high |
| 6 | Paseo orchestrate SKILL.md | https://github.com/getpaseo/paseo/blob/main/skills/paseo-orchestrate/SKILL.md | 11-phase flow, heartbeat, plan-on-disk, notifyOnFinish, hard rules | primary | high |
| 7 | Paseo loop SKILL.md | https://github.com/getpaseo/paseo/blob/main/skills/paseo-loop/SKILL.md | Cross-provider worker/verifier loop | primary | high |
| 8 | Paseo handoff SKILL.md | https://github.com/getpaseo/paseo/blob/main/skills/paseo-handoff/SKILL.md | Zero-context briefing template | primary | high |
| 9 | CORAL (arXiv:2604.01658) | STOPA learning | Heartbeat mid-run steering, shared public state | secondary | high |
| 10 | SAS vs MAS (arXiv:2604.02460) | STOPA learning | Single-agent ≥ MAS at equal compute | secondary | high |
| 11 | Self-org agents (arXiv:2603.28990) | STOPA learning | +8% self-org na explorativních tasks | secondary | high |
| 12 | Society of Thought (arXiv:2601.10825) | STOPA learning | Heterogenní perspektivy → výkon | secondary | high |

## Sources

1. MindStudio — Heartbeat Pattern — https://www.mindstudio.ai/blog/agentic-os-heartbeat-pattern-proactive-ai-agent
2. Temporal — Ambient Agents — https://temporal.io/blog/orchestrating-ambient-agents-with-temporal
3. WorkOS — MCP Async Tasks — https://workos.com/blog/mcp-async-tasks-ai-agent-workflows
4. Mendonca — Agentic Heartbeat — https://medium.com/@marcilio.mendonca/the-agentic-heartbeat-pattern
5. TAKT — https://github.com/nrslib/takt
6. Paseo — https://github.com/getpaseo/paseo
7. CORAL paper — arXiv:2604.01658
8. SAS vs MAS — arXiv:2604.02460
9. Self-org agents — arXiv:2603.28990
10. Society of Thought — arXiv:2601.10825

## Coverage Status

- **[VERIFIED]:** 10 claims (Paseo SKILL.md přečteny přímo, 4 web sources přes Jina)
- **[INFERRED]:** 2 claims (cross-source synthesis)
- **[SINGLE-SOURCE]:** 0
- **[UNVERIFIED]:** 0

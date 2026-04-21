---
date: 2026-04-22
type: architectural_evaluation
subject: Google ADK (adk-python) vs STOPA
verdict: adopt-patterns
source: WebFetch research (6 calls, github.com/google/adk-python + adk.dev)
---

# Google ADK — Architectural Evaluation vs STOPA

## Executive Summary

Google ADK (8200+ hvězd za 2 týdny, duben 2026) je **code-first Python framework pro production AI agenty** — primárně optimalizovaný pro Gemini/Vertex AI, ale model-agnostic přes LiteLLM (včetně Claude). Překryv se STOPA je **minimální na produktové úrovni**: ADK řeší "jak postavit a nasadit AI agent aplikaci na GCP," STOPA řeší "jak orchestrovat Claude Code jako development harness." **Nejsou konkurenti — jsou komplementy v jiných runtime vrstvách.** Doporučení: **adopt-patterns** (3 konkrétní vzory), monitor release cadence, žádná migrace.

## Comparative Table

| Dimenze | STOPA | Google ADK | Winner/Note |
|---------|-------|------------|-------------|
| Definice agenta | SKILL.md + YAML frontmatter (markdown-driven) | Python `Agent(...)` class + volitelný Agent Config YAML | STOPA čitelnější pro non-devs, ADK typovější |
| Agent typy | coordinator/worker skills, implicit | LlmAgent, SequentialAgent, ParallelAgent, LoopAgent, BaseAgent | **ADK** — Workflow agenti jako first-class primitivy |
| Memory model | state.md + learnings/ (YAML) + checkpoint.md + outcomes/ + failures/ | SessionService (konverzační) + MemoryService (long-term) | **STOPA** bohatší (confidence, maturity, impact, retrieval), **ADK** čistší separace session/memory |
| Orchestration | /orchestrate + Agent() sub-agents, budget tiers | hierarchical sub_agents, coordinator pattern | Podobné; STOPA má explicitní tiers, ADK má deterministické workflow typy |
| Budget / cost | budget.md + tiers (light/standard/deep/farm) | ❌ žádná nativní podpora | **STOPA** jednoznačně |
| Hooks / middleware | 70+ hooků přes 13 lifecycle eventů (SessionStart, PreToolUse...) | 6 callback eventů (before/after × Agent/Model/Tool) | **STOPA** podstatně bohatší, ADK má ekvivalent pro runtime guardrails |
| Self-improvement | /dreams, /evolve, /self-evolve, /autoloop (RCL, SEPL operators) | ❌ žádné meta-skills | **STOPA** jednoznačně |
| Model portability | Claude-native | Gemini-native + Claude/OpenAI/Ollama/vLLM přes LiteLLM | **ADK** výrazně lépe pro multi-provider |
| Testing / eval | /eval (trace grading), /verify (end-to-end) | `adk eval` — trajectory matching + response score + user simulation | **ADK** — formálnější trajectory-based eval, STOPA /eval je lightweight |
| Distribuce | Plugin marketplace přes GitHub | pip `google-adk` + Cloud Run / Vertex AI deploy | Různé audience: CC plugin vs production deploy |
| Remote agents | neřešeno | A2A protocol (agent-to-agent RPC) | **ADK** — pokud STOPA potřebuje multi-device, tohle je template |
| HITL | /orchestrate Phase 3 clarification | Tool Confirmation flow (nativní) | **ADK** — formálnější, STOPA ad-hoc |

## 3 Patterns Worth Adopting

### 1. Workflow Agents jako deterministické primitivy

**Zdroj v ADK:** `SequentialAgent`, `ParallelAgent`, `LoopAgent` (google.github.io/adk-docs → /agents). Workflow agent řídí flow **bez LLM reasoningu** — pouze orchestruje child agenty podle fixní struktury.

**Problém ve STOPA:** `/orchestrate` vždy volá LLM pro rozhodnutí, i když flow je deterministický (např. "scout → implement → critic → verify" je stejný vzor pro většinu multi-file úkolů). To jsou zbytečné LLM calls — kontext mutace, ale rozhodnutí je fixní.

**STOPA implementation sketch:**
- Přidat do `/orchestrate` frontmatter pole `workflow-type: sequential | parallel | loop | llm-decided` (default `llm-decided` = současné chování)
- Když tier=light a workflow-type=sequential: orchestrátor přeskočí LLM rozhodování v Phase 3 a vygeneruje fixní DAG
- Ekvivalent ADK `SequentialAgent`: `/orchestrate --workflow=sequential scout,implement,critic,verify` = žádné LLM volání pro flow logiku
- Úspora: ~1 LLM call v Phase 3 pro standardní tiery (odhad 5-8% token savings pro light/standard)
- Ref: SEPL operator σ (Select) může být u deterministických workflow no-op

### 2. Trajectory-based eval s user simulation

**Zdroj v ADK:** `adk eval` framework (adk.dev/evaluate). Eval set = JSON s `user_queries`, `expected_tool_trajectory`, `expected_intermediate_responses`, `reference_final_response`, `initial_session_state`. Kritéria: `tool_trajectory_avg_score` (exact match) + `response_match_score` (semantic) + `hallucinations_v1`/`safety_v1` s user simulation.

**Problém ve STOPA:** `/eval` dnes grade-uje JSONL trace heuristicky (critic LLM judge), ale nekontroluje **očekávanou trajektorii** (pořadí tool calls, sub-agent spawns). Regrese v agent routingu projdou, pokud finální výstup vypadá OK.

**STOPA implementation sketch:**
- Rozšířit `.claude/evals/<skill>/cases/*.yaml` o pole `expected_trajectory: [scout, critic, verify]` (ordered list skill/agent names)
- `/eval` porovná skutečnou sekvenci sub-agent spawnů vs expected → `trajectory_score ∈ [0,1]`
- Přidat user simulation mode pro `/orchestrate` a `/brainstorm`: eval set obsahuje multi-turn scénář, LLM judge simuluje uživatele
- Integrate do CI: GitHub Action `stopa-eval.yml` selže při `trajectory_score < 0.8` na canonical cases
- Ref: HERA failure trajectory records (již ve STOPA) + ADK trajectory scoring = silnější regresní detekce

### 3. Session Service / Memory Service formální split

**Zdroj v ADK:** `SessionService` (konverzační state, Events) vs `MemoryService` (long-term, cross-session, searchable archive). `InMemorySessionService` pro dev, `VertexAiSessionService` pro prod. MemoryService ingestuje completed sessions a poskytuje search API.

**Problém ve STOPA:** Rozdělení není explicitní. `state.md` mixuje session data + project facts, `checkpoint.md` je session-scoped ale čte se napříč sessions, `learnings/` je long-term ale per-session zápis. Skills nevědí kam psát — příklad: `/scribe` může legitimně zapsat do `state.md` NEBO `decisions.md` NEBO `learnings/`.

**STOPA implementation sketch:**
- Formálně pojmenovat: `.claude/memory/session/` (session-scoped, clear on `/checkpoint finalize`) vs `.claude/memory/longterm/` (cross-session, current `learnings/`, `decisions.md`, `key-facts.md`)
- Move: `state.md` → `session/current.md`, `checkpoint.md` zůstává ale označeno jako session bridge
- Skill frontmatter: `writes-to: session | longterm | both` — orchestrátor validuje
- MemoryService ekvivalent: existující `hybrid-retrieve.py` + `memory-search.py` + `concept-graph.json` **už jsou** jako MemoryService, jen nemají název. Pojmenovat sjednocuje.
- Ref: ADK A2A protokol pro remote agent-to-agent komunikaci je **nepotřebný** pro STOPA (single-device Claude Code), ignorovat

## Critical Questions — Answers

1. **Konkurent nebo komplement?** Komplement. ADK = production AI app framework (deploy na GCP), STOPA = Claude Code orchestration meta-projekt. Překryv < 20%.

2. **Top 3 adopce?** Workflow Agent primitivy, Trajectory eval, Session/Memory split (viz výše).

3. **Nahradí ADK KODER?** Ne. KODER je execution layer uvnitř Claude Code session (Task tool + sub-agents). ADK runtime žije v Python procesu — jiná vrstva. KODER a ADK mohou koexistovat bez konfliktu.

4. **Co STOPA dělá lépe a mělo by zůstat?** Budget tiers, rich learnings (confidence/maturity/impact/harmful_uses), 70+ hooks (vs ADK 6 callbacks), self-evolution skills, čeština/multi-lingual skill descriptions, markdown-driven skill definice (čitelné pro non-devs), RLM/SEPL operator formalizace.

5. **Konflikt "Claude Code skill ekosystém" vs "ADK multi-provider agents"?** Ne. Skill ekosystém = jak orchestrovat CC session; ADK = jak postavit deployable agent aplikaci. Pokud by STOPA někdy potřeboval production deployment (nabízet skills jako SaaS, multi-user), ADK by byl kandidát jako runtime — ne replacement.

## Final Verdict: `adopt-patterns`

Důvody:
- **Ignore** odmítnuto: 3 konkrétní vzory mají pozitivní ROI (trajectory eval zvlášť)
- **Monitor** je minimum, ale aktivní adopce je lepší — bi-weekly release cadence znamená rychlý vývoj
- **Migrate** odmítnuto: STOPA má 70+ hooks, self-evolution, budget tiers a skill ekosystém které ADK nemá; migrace by znamenala masivní regresi STOPA-specific features
- **Adopt-patterns** je rational: vzít 3 konkrétní vzory, implementovat inkrementálně, STOPA zůstává authoritative

## Action Items (priority MED, routed to news.md)

1. **Workflow Agent primitives** — přidat `workflow-type:` do `/orchestrate` (P1, 1-2 dny)
2. **Trajectory eval** — rozšířit `/eval` o `expected_trajectory` pole a `trajectory_score` (P2, 2-3 dny)
3. **Session/Memory split** — přejmenovat directories a přidat `writes-to:` validaci (P3, ~1 den + sync projekty)
4. **Monitor** — sledovat ADK releases každé 2 týdny, re-evaluate při 1.0 release

## Sources

- [google/adk-python GitHub](https://github.com/google/adk-python) — 8200+ stars, bi-weekly releases, latest 2026-04-17
- [ADK docs — agents](https://adk.dev/agents/) — agent types, workflow patterns
- [ADK docs — callbacks](https://adk.dev/callbacks/) — 6 events, registration pattern
- [ADK docs — sessions](https://adk.dev/sessions/) — SessionService vs MemoryService
- [ADK docs — evaluate](https://adk.dev/evaluate/) — trajectory matching, user simulation
- [ADK main](https://adk.dev/) — LiteLLM integration, A2A protocol, Claude support

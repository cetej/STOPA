# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-04-27 (morning-watch + arxiv-daily-digest) | Next: ~2026-05-04

**Scan log**: `2026-04-27` — morning-watch + arxiv | Items: CC v2.1.116 quality fixes, vim modes, hooks→MCP, ParaManager, Self-Optimizing MAS
**Scan log**: `2026-04-26` — arxiv-daily-digest | Items: 1 action, 2 watch — Self-Improving Error Diagnosis, MAS Orchestration survey
**Scan log**: `2026-04-25` — arxiv-daily-digest | Items: 2 action, 3 watch — SWE-Adept, Agentic Code Reasoning
**Scan log**: `2026-04-24` — morning-watch + arxiv | Items: Memory for Managed Agents beta, CC inline thinking
**Scan log**: `2026-04-21` — full scan | Items: 7 action, 5 watch, 4 info — CC hooks expansion, Google ADK, Agent resume breaking change, context engineering moat
**Scan log**: `2026-04-20` — arxiv-daily-digest | Items: 1 action, 4 watch — Context Awareness Gate (arXiv:2411.16133)
**Scan log**: `2026-04-19` — arxiv-daily-digest | Items: 1 action, 4 watch — RL for RAG (arXiv:2510.24652), TEA Protocol, Orchestral AI

(Older scan logs Apr 12-18 archived to news-archive.md on 2026-04-28)

## Actionable Rate

**Current: 14/27 = 51.9%** | Target: 50% REACHED | Baseline (2026-04-14): 5/27 = 18.5%
Formula: `python scripts/actionable-rate.py`

## Passes Rate (Harness Adoption)

**Current (2026-04-21):** 1/8 projects adopted | 11/15 features pass (73.3%)
**Baseline (2026-04-19):** 0/8 projects adopted | **Target:** >=2 projects + >=30% pass rate by 2026-05-17
Formula: `python scripts/passes-rate.py`

**Adopted:**
- NG-ROBOT (2026-04-21, commit 10a8d0e) — 15 features: 11 done / 3 in_progress (F012 Studio Video, F013 TTS unification, F014 INBOX audit) / 1 planned (F015 Phase 7b SEO)

**Next candidates:** ZACHVEV (active social analysis), POLYBOT (prediction markets), MONITOR (OSINT).

## Action Items (Open)

| # | Item | Urgency | Next Step |
|---|------|---------|-----------|
| 111 | **Harness adoption pilot** — NG-ROBOT adopted 2026-04-21 (commit 10a8d0e, 11/15=73.3%). 1/8 projects. | MED | Replicate on ZACHVEV or POLYBOT; reach target 2+ projects by 2026-05-17 |
| 109 | **CC Plugin monitors manifest key** — background monitoring v pluginech | HIGH | Evaluovat pro stopa-orchestration plugin |
| 110 | **Fine-grained tool streaming GA** — event-level streaming | MED | Vyuzit v Claude API integracich, NG-ROBOT |
| 105 | **CC Desktop redesign** — sidebar, terminal+editor, HTML/PDF preview, routines | HIGH | Otestovat novy workspace |
| 100 | **Meta Muse Spark** — Meta frontier model, Contemplating mode | MED | Pridat do /eval tier srovnani |
| 74 | **Claude Sonnet 5** — postupny rollout | MED | Prepnout model tiers az dostupny |
| 96 | **Prompt caching auto-placement** | MED | Zjednodusit NG-ROBOT caching |
| 97 | **Compaction API (beta)** | MED | Evaluovat pro /compact backend |
| 84 | **Claude Managed Agents (Public Beta)** | MED | Evaluovat jako alternativu |
| 86 | ant CLI | LOW | Sledovat az GA |
| 98 | **OpenClaw extra cost** | LOW | Sledovat pricing |
| 65 | CC forceRemoteSettingsRefresh | LOW | Sledovat pri distribuci |
| 42 | CC Voice Mode — Czech included | MED | Otestovat az dostupny |
| 44 | CC HTTP hooks | PARKED | Adopt pri remote agents |
| 113 | **CC /ultrareview** — cloud parallel multi-agent code review command | MED | Evaluovat jako heavy-tier backend pro /critic skill |
| 114 | **CC 7 novych hook events** — CwdChanged, FileChanged, TaskCreated, PostCompact, StopFailure, PermissionDenied, Elicitation | MED | Aktualizovat event list v behavioral-genome.md; StopFailure handler pro STOPA |
| 115 | **CC PowerShell Tool (Windows preview)** — CLAUDE_CODE_USE_POWERSHELL_TOOL opt-in | MED | Otestovat na Windows — potencialni nahrada Bash pro Windows-native ops |
| 116 | **Google ADK** (google/adk-python) — 8200+ stars, multi-agent Python framework | MED | Evaluovat vs STOPA architektura — overit jestli uz pokryto v ADR 0016 Phase B |
| 117 | **max_tokens 300k Batches API** — Opus 4.6 + Sonnet 4.6, beta header output-300k-2026-03-24 | DEFER | NG-ROBOT potvrzen jako pokracujici (ADR 0016 Phase D: 20% sunset H2 2027). Odlozit AZ po OCR migraci (GLM-OCR, immediate priority #1). |
| 118 | **Context Engineering as AI Moat** (Harrison Chase) — 5 patterns: trace observability, state mgmt, external memory, HITL, sleep-time compute | MED | Chase 5-pattern gap analysis vs STOPA — preverit prekryv s ADR 0016 MemoryBackend |

## Recent Findings (Apr 21)

| Date | Type | Item | Priority | Acted |
|------|------|------|----------|-------|
| 2026-04-21 | ACTION | CC /ultrareview — cloud multi-agent code review | med | No |
| 2026-04-21 | ACTION | CC 7 novych hooks: CwdChanged, FileChanged, TaskCreated, PostCompact, StopFailure, PermissionDenied, Elicitation | med | No |
| 2026-04-21 | ACTION | CC PowerShell Tool — Windows opt-in preview (CLAUDE_CODE_USE_POWERSHELL_TOOL) | med | No |
| 2026-04-21 | ACTION | Google ADK (google/adk-python) — 8200+ stars | med | No (check ADR 0016 Phase B) |
| 2026-04-21 | ACTION | Harrison Chase: Context Engineering as AI Moat — 5 patterns | med | No (check vs ADR 0016) |
| 2026-04-21 | ACTION | max_tokens 300k Batches API (Opus 4.6/Sonnet 4.6) | low | No (check NG-ROBOT obsolescence) |
| 2026-04-21 | WATCH | CC /ultraplan — cloud planning sessions | med | No |
| 2026-04-21 | WATCH | arXiv:2604.04990 Architecture Without Architects | med | No |
| 2026-04-21 | WATCH | arXiv:2604.12843 Growing Pains Benchmarking — 100 anchor questions | med | No |
| 2026-04-21 | WATCH | Simon Willison LLM library: server-side tool execution | med | No |
| 2026-04-21 | WATCH | transformers v5.5.0: TimesFM 2.5, VibeVoice ASR | med | No |
| 2026-04-21 | INFO | Claude Mythos Preview gated (Project Glasswing, invite-only) | low | No |
| 2026-04-21 | INFO | /less-permission-prompts oficialni CC command | low | No |
| 2026-04-21 | INFO | Qwen3.6-35B lepsi nez Opus 4.7 na vizualech | low | No |
| 2026-04-21 | INFO | SWE-Bench-Verified data leakage concern (arXiv:2512.10218) | low | No |

(Findings Apr 15-20 + scans Apr 21-23 archived to news-archive.md on 2026-04-28)

## Watch List (Ongoing)

### Models & Releases
| Item | Detail | Trigger |
|------|--------|---------|
| Mythos/Capybara | Training dokoncen, piloting (2026-04-03). Step change coding+reasoning. | GA datum — preplanovat STOPA model tiers |
| Claude Sonnet 5 #74 | Postupny rollout — ceka na account access | Prepnout tiers az dostupny |
| Gemini CLI #75 | Apache 2.0, ReAct loop, MCP support, 1M context. Direct competitor. | Sledovat adopci |
| Gemma 4 #61 | 4 modely (2B-31B), Apache 2.0, vision+reasoning | Open-weight alternativa |

### Agent/Tool Research (active)
| Item | Detail |
|------|--------|
| Meta-Harness #73 | MEDIAN traces: 50.0 vs scores-only: 34.6 (+15 pts). /eval musi reportovat median; /orchestrate pridat tool inventory P1 |
| agent-browser #70 | CLI pro agenty: snapshot-refs-act, Rust daemon, CDP. npm install -g agent-browser |
| Hermes Agent v0.8.0 #96 | 40K+ stars, persistent memory, auto-generated skills, cross-platform, MCP OAuth 2.1 |
| Memory Intelligence Agent arXiv:2604.04503 | Cache + memory layers blizke STOPA MemPalace |
| DACS #102 acted | Registry-Focus context switching, 3.53x efficiency — implementovat v orchestrate pro >3 agenty |
| TraceGuard #103 acted | 5D CoT monitoring — upgrade /critic na 5D |
| MCP Toolbox for DBs #71 | 30+ DB (PostgreSQL, MongoDB, Redis), NL2SQL. Trigger: POLYBOT/MONITOR DB layer |
| Colab MCP Server #76 | Google Colab runtime s GPU pro agenty. Kandidat: POLYBOT inference |

## 2026-04-24 Morning Watch

| # | Item | Summary | Action |
|---|------|---------|--------|
| #113 | Memory for Claude Managed Agents public beta | Memory API pro Managed Agents v public beta pod `managed-agents-2026-04-01` headerem — agenti si pamatují kontext přes sessions | Evaluovat pro STOPA cross-session agent state; update #84 |
| #114 | CC inline thinking progress | Thinking spinner nyní zobrazuje průběh inline ("still thinking", "thinking more", "almost done") místo separátního hint řádku — nový CC release | Minor UX, žádná akce |

## 2026-04-24 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-24 | [ACTION] | Self-Optimizing Multi-Agent Systems for Deep Research (arXiv:2604.02988) — self-play loop where agents explore prompt combinations autonomously | high | No | arxiv-daily-digest |
| 2026-04-24 | [WATCH] | Small Model as Master Orchestrator with Parallel Subtask Decomposition (arXiv:2604.17009) | medium | No | arxiv-daily-digest |
| 2026-04-24 | [WATCH] | Adaptive Orchestration: Scalable Self-Evolving MAS (arXiv:2601.09742) | medium | No | arxiv-daily-digest |
| 2026-04-24 | [WATCH] | RL for Self-Improving Agent with Skill Library — SAGE (arXiv:2512.17102) | medium | No | arxiv-daily-digest |
| 2026-04-24 | [WATCH] | CoCR-RAG: Concept-oriented Context Reconstruction (arXiv:2603.23989) | medium | No | arxiv-daily-digest |

## 2026-04-25 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-25 | [ACTION] | SWE-Adept: LLM Agentic Framework for Deep Codebase Analysis (arXiv:2603.01327) — two-agent split, +4.7% on SWE-Bench; applicable to /scout + /fix-issue | high | No | arxiv-daily-digest |
| 2026-04-25 | [ACTION] | Agentic Code Reasoning (arXiv:2603.01896) — semi-formal reasoning, 78%→88% on patch equivalence; implementable in /critic and /verify | high | No | arxiv-daily-digest |
| 2026-04-25 | [WATCH] | SWE-AGILE: Software Agent Framework (arXiv:2604.11716) | medium | No | arxiv-daily-digest |
| 2026-04-25 | [WATCH] | From Reasoning to Agentic: Credit Assignment in RL (arXiv:2604.09459) | medium | No | arxiv-daily-digest |
| 2026-04-25 | [WATCH] | Evaluating Multi-Hop Reasoning in RAG: CARE (arXiv:2604.18234, ECIR 2026) | medium | No | arxiv-daily-digest |

## 2026-04-26 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-26 | [ACTION] | Towards Self-Improving Error Diagnosis in Multi-Agent Systems (arXiv:2604.17658) — directly applicable to /critic and /learn-from-failure | high | No | arxiv-daily-digest |
| 2026-04-26 | [WATCH] | The Orchestration of Multi-Agent Systems (arXiv:2601.13671) — survey, reference taxonomy for /orchestrate | medium | No | arxiv-daily-digest |
| 2026-04-26 | [WATCH] | LLM-Based Agentic Systems for Software Engineering Survey (arXiv:2601.09822) | medium | No | arxiv-daily-digest |

## 2026-04-27 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-27 | [ACTION] | Small Model as Master Orchestrator: ParaManager (arXiv:2604.17009) — directly applicable to STOPA orchestrate dispatcher pattern (haiku-as-orchestrator + parallel decomposition) | high | No | arxiv-daily-digest |
| 2026-04-27 | [ACTION] | Self-Optimizing Multi-Agent Systems for Deep Research (arXiv:2604.02988) — applicable to /deepresearch and /self-evolve adversarial co-evolution loop | high | No | arxiv-daily-digest |
| 2026-04-27 | [WATCH] | CAMCO Safe and Policy-Compliant MAS Orchestration (arXiv:2604.17240) — relevant for /orchestrate budget tier guards and circuit breakers | medium | No | arxiv-daily-digest |
| 2026-04-27 | [WATCH] | Context Kubernetes (arXiv:2604.11623) — potential pattern for STOPA skills + memory + hooks lifecycle management | medium | No | arxiv-daily-digest |
| 2026-04-27 | [WATCH] | Principled Context Engineering for RAG via Conformal Prediction (arXiv:2511.17908) — relevant for hybrid-retrieve.py budget-aware shrinking with statistical guarantees | medium | No | arxiv-daily-digest |

## 2026-04-27 morning-watch

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-27 | [ACTION] | Claude Code v2.1.116 quality fixes — restored higher default reasoning effort, fixed caching bug; affects daily CC use, no STOPA action needed | high | No | morning-watch |
| 2026-04-27 | [ACTION] | CC adds vim visual modes + custom themes + direct MCP tool hooks — relevant for STOPA hook architecture (invariant-checker could call MCP tools directly) | medium | No | morning-watch |
| 2026-04-27 | [WATCH] | Rate Limits API + Haiku 3 retired — programmatic rate-limit query for orgs/workspaces (useful for STOPA budget guards); Haiku 3 EOL, STOPA already on 4.5 | medium | No | morning-watch |

## 2026-04-29 morning-watch

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-29 | [ACTION] | CC PostToolUse hooks now replace tool output via `hookSpecificOutput.updatedToolOutput` — applicable to STOPA verify-sweep / invariant-checker hooks (mutate tool output, not just block) | medium | No | morning-watch |
| 2026-04-29 | [INFO] | CC `/skills` adds type-to-filter search box — minor UX, no STOPA action | low | No | morning-watch |
| 2026-04-29 | [WATCH] | Sonnet 4.5/4 1M context beta retired 2026-04-30 (tomorrow) — STOPA already on Opus 4.7 1M (standard pricing), no action; flag if any skill pinned to Sonnet 4.5 with 1M flag | medium | No | morning-watch |

## Weekly Digest 2026-04-27

**Aktivita projektů (od 2026-04-20):**
- STOPA: 50 commits — Karpathy Rule 5 wired (orchestrate/fix-issue success criteria), orchestrate-light Haiku tier, hybrid-retrieve Context Awareness Gate + auto grep_only, brain-bridge → radar/news (issue #24 closed), Hippo+GenericAgent memory dynamics adoption, L2 sentinel fix
- NG-ROBOT: 155 commits — pipeline runs (CMS h1_title fix klíčový), většina hook-generated automatika
- ADOBE-AUTOMAT, ZACHVEV, POLYBOT, MONITOR, GRAFIK: 0 commitů (idle)

**Novinky:**
- 14 ACTION items open; top urgency: #109 CC Plugin manifest monitors, #105 CC Desktop redesign, #114 CC 7 nových hook events
- 5 WATCH items z Apr 21 scanu + 4 nové ACTION/WATCH 2026-04-27 (ParaManager arXiv:2604.17009, Self-Optimizing MAS arXiv:2604.02988, CAMCO, Context K8s)
- Trend: orchestrace + memory engineering dominují papers; Anthropic posouvá CC k hookům jako primární extension point

**Poučení týdne (12 nových learnings od 2026-04-20):**
- 2026-04-27: verify-cc-features-against-docs, l2-sentinel-double-eval
- 2026-04-26: autoreason-mid-tier-sweet-spot (graduation candidate)
- 2026-04-25: mcp-config-canonical-location
- 2026-04-24: scheduled-task-discipline
- 2026-04-23: llm-confirmation-bias, ucsd-devs-dont-vibe, deepmind-agent-attack-vectors
- 2026-04-21: vertical-scaling-phase-b-not-implemented, doom-loop-signal, ch-samostatne-pismeno

**Údržba:**
- decisions.md (34) ✓, budget.md (39) ✓, news.md trimmed 267→~155 (2026-04-28 archive)
- Actionable rate 51.9% (target 50% ✓ dosažen)
- Harness adoption: 1/8 projektů (NG-ROBOT) — pod target 2+ do 2026-05-17

**Doporučení na týden 2026-04-28 → 2026-05-04:**
1. **Harness pilot replikace** na ZACHVEV nebo POLYBOT — kritické pro target do 2026-05-17 (item #111)
2. **Evaluace CC novinek**: PowerShell Tool (#115), 7 hook events (#114) → behavioral-genome.md update; /ultrareview (#113) jako heavy-tier critic backend
3. **Implementace ACTION items** z 2026-04-27 digestu: ParaManager pattern v /orchestrate, Self-Optimizing MAS v /self-evolve

Older digests: see news-archive.md

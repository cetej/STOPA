# Meta-Agent Competitive Landscape — STOPA positioning (April 2026)

**Date:** 2026-04-21
**Question:** What meta-agent systems with persistent memory + multi-project orchestration exist as of April 2026, and where does STOPA stand?
**Scope:** survey (12+ candidates, 4 dimensions)
**Sources consulted:** 38 discovery URLs + 15 deeply read primary sources + 9 existing brain/wiki concepts
**Verification status:** 2-phase (discovery Haiku → reading Sonnet via Jina Reader → lead verification of critical numbers)

---

## Executive Summary

Terén meta-agentních systémů v dubnu 2026 se dělí na čtyři tábory:

1. **Memory-first frameworks** (Letta, mem0, Zep, LangMem) — silné v paměti, slabé v orchestraci a skillech. Cílí primárně na enterprise SaaS.
2. **Generalist orchestrators** (OpenHands 70K★, Goose 43K★, Suna) — dominují GitHub metrikami, silné v multi-agent dekompozici, ale memory je ad-hoc.
3. **Coding agents s persistencí** (Cursor Composer 2, Aider+LanceDB, Cline, Warp, Claude Code) — pragmatická paměť pro developery, ale single-project scope.
4. **Platform-level personal AI** (Microsoft Copilot Studio, Google Gemini Personal Intelligence, Claude Memory, Apple Intelligence) — obrovský rozpočet, ale ecosystem-locked.

**STOPA pozice**: nejedinečnější je **kombinace** (a) file-based persistent memory s YAML front-matter a grep-first retrieval, (b) cross-project routing přes GitHub issues, (c) vlastní self-evolve loop (autoloop, autoresearch, scribe), (d) 80+ skill systém s hooks. Individuální dimenze existují u konkurence; **jejich složení pro osobního-AI-uživatele nevidím jinde**.

**Největší obsolescence signál**: **Claude Managed Agents Memory tool** (Research Preview, `managed-agents-2026-04-01` beta header) [VERIFIED][7] — když vyjde GA, nahradí přímo jádro STOPA memory layer (6 tools: list/search/read/write/edit/delete, 100 KB/memory, max 8 stores/session, cross-session persistence, audit trail přes verzovanou ledger). Horizon: 6-12 měsíců.

**Druhý signál**: **Microsoft Copilot Studio autonomous agents** s nativním scheduled execution [VERIFIED][1] — pokud Microsoft vydá non-enterprise tier, STOPA scheduled-tasks vrstva ztrácí unikátnost.

---

## Comparison Matrix

| Projekt | Memory model | Multi-project | Self-improve | Skills abstrakce | Runtime | License | Maturita | OS integrace |
|---------|--------------|---------------|--------------|------------------|---------|---------|----------|--------------|
| **STOPA** | file+grep+YAML frontmatter + concept-graph | native (/improve, project profiles) | autoloop/scribe/evolve cycle | 80+ skills, user-invocable, hooks | local (CC) | private | produkce (interně) | terminal + hooks |
| **Letta** (ex-MemGPT) | 3-tier hierarchical, agent-controlled | manual | Skill Learning (Dec 2025), Context Constitution | Context Repositories s git verzováním | local + cloud | OSS (Apache) | produkce [VERIFIED][6] | chat / API |
| **mem0** | semantic + graph + KV, self-editing | manual | — | 21 framework integrations | local + cloud | OSS + SaaS | produkce, ~48K★ [VERIFIED][1,2] | chat / API |
| **Zep** | temporal knowledge graph (Graphiti) | manual | — | Graph RAG, MCP | cloud SaaS | OSS engine + komerční SaaS | produkce, $125/$375/mo [VERIFIED][5] | chat / API |
| **LangMem** | storage-agnostic, 3 typy (claimed) | LangGraph native | prompt auto-optimization | LangGraph tools | local (SDK) | OSS | alpha [PARTIAL][3] | chat / API |
| **OpenHands** | per-session, RAG file_search | ne (repo-scope) | — | agent SDK, MCP | local (Docker/K8s) | OSS (MIT) | produkce, 70K★, v1.6.0 [VERIFIED][5] | terminal + browser |
| **Goose** (Block) | per-session | ne | — | MCP-first, extensions, Recipes | desktop + CLI | OSS (Apache) | produkce, **42,895★** [VERIFIED][4] | desktop + terminal |
| **Suna** (Kortix) | shared FS + DB | ne | — | sub-agent delegation | cloud + self-host | OSS | beta | chat |
| **Sakana AI Scientist v2** | tree-search trajektorie | ne | evaluation loop | research-only skills | cloud | OSS | experimental, 42% failure rate | chat |
| **Cursor Composer 2** | semantic codebase index + RL long-horizon | ne | — | custom agents | cloud (app) | komerční | produkce, CursorBench 61.3 [VERIFIED][6] | desktop + terminal |
| **Aider** | LanceDB vector 384-dim | ne (project-scope) | — | ne | local | OSS (Apache) | produkce | terminal |
| **Cline** | explicit Memory Bank (user-controlled) | ne | — | MCP | VS Code extension | OSS | produkce | editor |
| **Warp Terminal AI** | block-based + AI Knowledge | ne | — | workflows | desktop | komerční | produkce | terminal (native) |
| **Claude Code** (Anthropic) | CLAUDE.md + auto memory MEMORY.md (v2.1.59+) | přes settings.json | — | skills/commands, hooks | local | komerční | produkce [VERIFIED][8] | terminal |
| **Claude Managed Agents Memory** | 6 memory tools, 100KB×8 stores, ledger | workspace-scope | cross-session persistence explicit | memory API | cloud (Anthropic) | komerční, Research Preview | **Research Preview** [VERIFIED][7] | API |
| **OpenAI Agents SDK** | file_search RAG ($2.50/1K q) | ne | — | Agent objects, handoffs | SDK + cloud | open SDK + komerční | produkce, mar 2025 [VERIFIED][4] | API |
| **Microsoft Copilot Studio** | enterprise data governance | M365 ecosystem | — | low-code connectors, 1000+ integrations | cloud (Azure) | komerční, enterprise | produkce (Wave 2) [VERIFIED][1] | M365 / Power Platform |
| **Google Gemini Personal Intelligence** | cross-Google-apps context | Google apps only | — | agentic browser, Gmail, Calendar | cloud | komerční (AI Pro/Ultra) | produkce, Jan 2026 [VERIFIED][2] | chat + Chrome + Android |
| **Apple Intelligence / Siri** | on-device + Private Cloud Compute | apps s App Intents | — | App Intents framework | device-locked | komerční | beta, iOS 27 roadmap | OS-level (iOS/macOS) |

---

## Detailed Findings

### Where STOPA leads

1. **Memory as a first-class architectural concern with explicit semantics** [INFERRED][STOPA internal + 7,8]
STOPA má rozlišené typy paměti: `learnings/` s YAML front-matter (type, severity, component, tags, uses, confidence, maturity), `failures/` jako HERA trajektorie, `decisions.md` s ADR indexem, `outcomes/` jako per-run RCL credit records, `critical-patterns.md` jako always-read top 10. Žádný konkurent v research-cutu tuto úroveň dekompozice nemá: Letta má 3-tier, mem0 má 3-tier+graph, ale bez lifecycle fields a graduation triggerů.

2. **Cross-project routing s profily** [INFERRED][STOPA internal]
`/improve` + `~/.claude/memory/projects/*.yaml` (priority thresholds, watch_topics) + automatická sweep přes scheduled task + GitHub issue creation. Ostatní projekty řeší cross-project až při deploymentu (enterprise orchestrators) nebo vůbec (všichni coding agents).

3. **Self-improvement loop (autoloop, autoresearch, scribe, evolve)** [INFERRED][STOPA internal + existing brain/wiki on ByteRover, Process-Reward Agents]
Explicitní SEPL operátory (ρ Reflect, σ Select, ι Improve, ε Evaluate, κ Commit) s commit-invariants a rollback protokolem. Letta má Context Constitution (principy) a Skill Learning, ale není to stejné jako měřitelný Karpathy-style loop. mem0 nemá.

4. **Harness engineering → file-based mutovatelný runtime** [INFERRED][STOPA + SemaClaw concept][9]
Hooks, scheduled tasks, `.claude/memory/` file system, instrumentation = SemaClaw-like harness (arXiv:2604.11548). Komerční produkty mají cloud-locked black-box verze; STOPA má tohle lokálně a viditelně.

### Where STOPA lags

1. **Vector/graph retrieval vs. jen grep** — cost estimate **medium**
mem0 (66.9% LOCOMO LLM-Judge, 1.44s p95, ~1,800 tokens/konverzace) [VERIFIED][2] a Zep (+15 bodů LongMemEval nad mem0 v marketingu, temporal fact invalidation) ukazují, že pokročilé retrieval je potřeba pro větší memory. STOPA má `hybrid-retrieve.py` (grep+BM25+graph walk RRF), ale chybí skutečný vector index. Pro malou memory OK, pro 10K+ learnings už ne.

2. **GA-quality memory API s persistent stores** — cost estimate **high (wait-and-adopt)**
Claude Managed Agents Memory (6 tools, 100KB×8 stores, workspace-scope, ledger, cross-session explicit) [VERIFIED][7] je dnes Research Preview, ale při GA bude přímou náhradou za DIY paměť v STOPA. Adopce = přepsat retrieval/write vrstvu na Claude API Memory tool, zachovat vlastní lifecycle sémantiku nad ní.

3. **No persistent graph retrieval engine** — cost estimate **medium**
Zep Graphiti (temporal knowledge graph, fact validity windows) je production-grade implementací toho, co STOPA přibližuje přes `concept-graph.json` + `associative-recall.py`. STOPA graf se neautomatizuje do CI, chybí persistent storage engine a temporal reasoning.

4. **No formal benchmarking** — cost estimate **low-medium**
OpenHands (SWE-bench Verified 53%+), Cursor Composer 2 (CursorBench 61.3, Terminal-Bench 2.0 61.7, SWE-bench Multilingual 73.7) [VERIFIED][6], Letta Code (42.5% Terminal-Bench) [VERIFIED][6] — všichni publikují čísla. STOPA nemá referenční benchmark ("actionable_rate 51.9%" je interní proxy). Znamená to, že nevíme, jestli se zlepšujeme, nebo jen zvětšujeme.

5. **Single-user, single-machine** — cost estimate **low, strategické**
Žádný sync s jinou instancí, žádný multi-device (mobile/remote access mimo Telegram, který uživatel právě vypnul). Zep i mem0 mají SaaS tiery s HIPAA; STOPA neopustí Windows box.

### Where STOPA sits in mainstream (table stakes)

- **MCP integrace** — má každý: Goose, OpenHands, Cline, Claude Code, Cursor, Zep (Knowledge Graph MCP).
- **Scheduled tasks** — má Microsoft Copilot Studio, Google Gemini Personal Intelligence (Q1 2026), STOPA přes mcp-scheduled-tasks. Cursor/Aider/Cline nikoli.
- **Hooks / post-edit automation** — Claude Code má nativně (stejné jako STOPA využívá), Goose má Recipes, Cursor má agents. Ostatní ne.
- **File-based config (CLAUDE.md / .cursorrules / .cline-memory)** — všichni coding agents mají analog.

### Obsolescence signals — co nás může "sníst" za 6-12 měsíců

**Signál 1: Claude Managed Agents Memory GA** [VERIFIED][7]
- **Co:** 6 memory tools (list/search/read/write/edit/delete), 100KB × 8 stores × session, workspace-scoped, cross-session persistence explicitně deklarována, každá mutace → immutable verzovaný záznam (audit).
- **Gap proti STOPA:** STOPA má bohatší lifecycle (maturity, confidence, uses/harmful_uses/impact_score, supersedes, valid_until), Anthropic má **nativní API + ecosystem integraci**.
- **Timeline:** Research Preview teď (2026-04-01 beta header); GA pravděpodobně Q2-Q3 2026.
- **Dopad:** -50 % hodnoty vlastního retrieval/write layeru, pokud STOPA nezvládne migraci. Cross-project routing, skill systém, cscheduled tasks zůstávají STOPA unikátní.

**Signál 2: Microsoft Copilot Studio multi-agent + scheduling, + potenciální SMB tier** [VERIFIED][1]
- **Co:** Autonomous agents s trigger-based execution (hourly/daily/weekly/monthly), multi-agent orchestration (March 2026 update), enterprise connectors.
- **Gap:** Dnes enterprise-only (M365 / Power Platform licence). Pricing a SMB/individuální tier nepublikován.
- **Timeline:** Pokud vyjde personal tier v 2026 (pravděpodobnost ~40 %), STOPA ztratí "orchestrace + scheduled tasks" diferenciátor v očích ne-dev uživatelů.
- **Dopad:** Nezasahuje coding workflow, ale zasahuje universum "personal productivity + automation".

**Signál 3: Cursor Composer 2 long-horizon RL + jeho nástupci** [VERIFIED][6]
- **Co:** Frontier model trénovaný RL na long-horizon úkolech, "hundreds of actions" v jednom běhu, CursorBench 61.3 vs Composer 1 (38.0).
- **Gap proti STOPA:** Složité úkoly, kde STOPA dnes dělá orchestrate → multiple agents → synthesis, Composer 2 **single agent**. Pokud tahle třída modelů zjednoduší orchestraci, STOPA orchestration value klesá.
- **Timeline:** Už produkce. Claude Sonnet 4.7 + Opus 5 (pokud přijde Q2-Q3 2026) s podobným RL long-horizon tréninkem = podobný efekt.
- **Dopad:** Orchestrate skill přestává být must-have, stává se nice-to-have.

**Signál 4: Letta Context Constitution + Context Repositories s git verzováním** [VERIFIED][6]
- **Co:** Open-source Context Repositories (Feb 2026), Skill Learning (Dec 2025), Context-Bench + Recovery-Bench + Letta Evals open-source (April 2026).
- **Gap proti STOPA:** Letta má **veřejný benchmark stack** a **open-source eval infrastructure**. STOPA má vlastní harness uvnitř .claude/evals, ale není externě publikovatelné.
- **Timeline:** Už teď.
- **Dopad:** Community gravituje k Letta pro reference implementation. Když si někdo vytvoří "STOPA pro Lettu" s lepším kódem, komunita pójde tam.

---

## Strategická doporučení

1. **Přijmout Claude Managed Agents Memory jako backend, zachovat STOPA lifecycle sémantiku vrstvou nad.** Adopce lifecycle fields (maturity, confidence, supersedes, impact_score) jako JSON payload do memory_write contents. Migrace: 2-4 týdny, jak GA vyjde.

2. **Přidat vector/graph retrieval** (Qdrant local / sqlite-vss / LanceDB) vedle grep. mem0-style self-editing, Zep-style temporal invalidation. Cost: medium, velké učící ROI. Opraví dnešní grep-only bottleneck na velkých learnings/.

3. **Publikovat benchmark**. STOPA-Bench: orchestrate latency, actionable_rate, critic-pass rate, learning graduation throughput. Externalizovat via blog + GitHub. Staví credibility vs Letta/mem0/Zep.

4. **Sleduj Microsoft Copilot Studio pricing quarterly** (ne jen anounce). Když SMB tier vyjde, STOPA positioning pro non-dev use-case se mění. Reakce: zaměřit STOPA explicitně na dev + cross-project coding workflow.

5. **Neinvestovat do mobile/remote access nad Telegram** (user explicitně vypnul). Místo toho: `alerts.md` + scheduled email digest jako alternativní notification kanál, pokud user bude chtít.

---

## Evidence Table (merged from Reading 1 + 2 + lead verification)

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Mem0 arXiv paper | https://arxiv.org/abs/2504.19413 | 91% lower p95 latency, 90%+ token savings vs full-context on LOCOMO | primary | VERIFIED |
| 2 | Mem0 blog | https://mem0.ai/blog/state-of-ai-agent-memory-2026 | LOCOMO: Mem0=66.9%, Mem0g=68.4%, full-context=72.9%, OpenAI memory=52.9% | primary | VERIFIED |
| 3 | LangMem official docs | https://langchain-ai.github.io/langmem/ | Core API + background manager; no benchmark data on page | primary | VERIFIED (absence) |
| 4 | OpenAI Agents SDK | https://openai.com/index/new-tools-for-building-agents/ | Responses API + SDK, no native scheduling, file_search $2.50/1K q | primary | VERIFIED |
| 5 | Zep pricing | https://www.getzep.com/pricing/ | Flex $125/mo (50K credits), Flex Plus $375/mo (200K credits), 1 credit = 1 episode (≤350B) | primary | VERIFIED (lead re-check) |
| 6 | Letta blog | https://www.letta.com/blog/ | Letta Code launched Apr 6 2026, OSS; Terminal-Bench 42.5% (4th overall, Aug 2025) | primary | VERIFIED |
| 7 | Claude Managed Agents Memory docs | https://platform.claude.com/docs/en/managed-agents/memory | Research Preview; 6 tools; 100KB×8 stores; workspace-scoped; cross-session explicit; ledger | primary | VERIFIED |
| 8 | Claude Code memory | https://code.claude.com/docs/en/memory | CLAUDE.md + auto memory MEMORY.md v2.1.59+, loads first 200 lines at session start | primary | VERIFIED |
| 9 | Microsoft Copilot Studio blog | https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/unlocking-autonomous-agent-capabilities-with-microsoft-copilot-studio/ | Enterprise-oriented SaaS, scheduled + event triggers, no pricing on page | primary | VERIFIED |
| 10 | Gemini Drop Jan 2026 | https://blog.google/innovation-and-ai/products/gemini-app/gemini-drop-january-2026/ | Personal Intelligence + Chrome auto browse; "Scheduled Actions 10-limit" NOT in this source | primary | SINGLE-SOURCE (claim corrected) |
| 11 | Goose launch | https://block.xyz/inside/block-open-source-introduces-codename-goose | Launched Jan 28 2025, MCP-first, LLM-agnostic, Apache 2.0 | primary | VERIFIED |
| 12 | Goose GitHub | https://github.com/block/goose | 42,895 stars as of 2026-04-21 (NOT 29K) | primary | VERIFIED |
| 13 | OpenHands Index | https://openhands.dev/blog/openhands-index | Jan 29 2026; 5 categories; Claude 4.5 Opus = overall winner; exact SWE-bench % in chart image | primary | VERIFIED |
| 14 | Cursor Composer 2 | https://cursor.com/blog/composer-2 | Published March 19 2026; CursorBench 61.3, Terminal-Bench 2.0 61.7; hundreds of actions via RL long-horizon; $0.50/$2.50 per M tokens; NO persistent memory feature | primary | VERIFIED |
| 15 | STOPA brain/wiki concepts (9 sources) | `.claude/memory/brain/wiki/concepts/` | ByteRover, Corpus2Skill, SemaClaw, Persistent-Identity, Process-Reward, Externalization, Knowledge-Compounding, Missing-Knowledge-Layer, ADR Context Strategies — all sourced from arXiv in April 2026 | secondary (baseline) | VERIFIED (internal) |

---

## Disagreements & Open Questions

- **Gemini "Scheduled Actions 10-limit"** — claim from Discovery D nenalezen v primárním Jan 2026 Drop blogu. Pravděpodobně jiný zdroj (Google I/O 2025 nebo separátní feature drop). **Otevřená otázka.**
- **OpenHands SWE-bench Verified exact %** — Discovery B řekl 53%, Reading 2 řekl "chart image, nevyčtitelné textově". Oba zdroje souhlasí, že Claude 4.5 Opus je overall winner. Přesné číslo open.
- **Mem0 "91.6 / 93.4" — NEPOTVRZENO.** Discovery A uvedl jako accuracy scores, Reading 1 vyvrátil (91 % bylo latency reduction, 66.9 % je správná LOCOMO accuracy). Pokud se někde najde "91.6 / 93.4" jako benchmark, jsou to jiné datasety (LongMemEval), které jsme v tomto kole nezasáhli.
- **Microsoft Copilot Studio SMB/personal tier** — není v zdrojích ani potvrzeno, ani vyvráceno. Je to hlavní neznámá pro obsolescence timeline.

---

## Coverage Status

- **[VERIFIED]** (directly fetched + content confirmed): 14 source URLs via Jina Reader + 1 GitHub API + 1 manual curl check (Zep pricing). All 9 STOPA brain/wiki concepts internally verified.
- **[SINGLE-SOURCE]**: Gemini Drop (claim about "10-action limit" NOT in fetched source).
- **[INFERRED]**: STOPA competitive positioning claims (derived from 15+ primary sources combined with internal knowledge of STOPA architecture).
- **[UNVERIFIED]**: Mem0 "91.6/93.4" accuracy claim (rejected — actual scores are different). LangMem P95 latency 59.82s (not on official docs). "Claude Code v2.1.30+" (corrected to v2.1.59+).

---

## Sources

Verified primary sources (direct fetch):

1. Mem0 — Building Production-Ready AI Agents with Scalable Long-Term Memory — https://arxiv.org/abs/2504.19413
2. Mem0 — State of AI Agent Memory 2026 — https://mem0.ai/blog/state-of-ai-agent-memory-2026
3. LangMem — https://langchain-ai.github.io/langmem/
4. OpenAI — New Tools for Building Agents — https://openai.com/index/new-tools-for-building-agents/
5. Zep — Pricing — https://www.getzep.com/pricing/
6. Letta — Blog (Letta Code, Context Constitution, Context Repositories) — https://www.letta.com/blog/
7. Anthropic — Managed Agents Memory — https://platform.claude.com/docs/en/managed-agents/memory
8. Anthropic — Claude Code Memory — https://code.claude.com/docs/en/memory
9. Microsoft — Unlocking autonomous agent capabilities — https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/unlocking-autonomous-agent-capabilities-with-microsoft-copilot-studio/
10. Google — Gemini Drop January 2026 — https://blog.google/innovation-and-ai/products/gemini-app/gemini-drop-january-2026/
11. Block — Introducing codename Goose — https://block.xyz/inside/block-open-source-introduces-codename-goose
12. GitHub — block/goose — https://github.com/block/goose
13. OpenHands — Index benchmark — https://openhands.dev/blog/openhands-index
14. Cursor — Composer 2 — https://cursor.com/blog/composer-2

Additional discovery-level sources (not directly read, 30+ URLs): see `outputs/.research/meta-agent-competitive-discovery-{A,B,C,D}.md`.

STOPA brain/wiki baseline (verified internally):

- ByteRover — `.claude/memory/brain/wiki/concepts/byterover.md` (arXiv:2604.01599)
- Corpus2Skill — `corpus2skill.md` (arXiv:2604.14572)
- SemaClaw — `semaclaw-harness-engineering.md` (arXiv:2604.11548)
- Persistent-Identity — `persistent-identity-agents.md` (arXiv:2604.09588)
- Process-Reward Agents — `process-reward-agents.md` (arXiv:2604.09482)
- Externalization in LLM Agents — `externalization-llm-agents.md` (arXiv:2604.08224)
- Knowledge Compounding — `knowledge-compounding.md` (arXiv:2604.11243)
- Missing Knowledge Layer — `missing-knowledge-layer.md` (arXiv:2604.11364)
- ADR Context Strategies — `adr-context-strategies.md`

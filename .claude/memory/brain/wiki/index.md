# 2BRAIN Wiki — Master Index

Obsah kompilovaných wiki článků organizovaný podle typu entity.
LLM čte tento soubor PRVNÍ při odpovídání na dotazy.

**Last updated:** 2026-04-20
**Total articles:** 50

---

## Concepts (35)

| Article | Summary | Sources | Updated |
|---------|---------|---------|---------|
| [context-engineering](concepts/context-engineering.md) | Karpathyho princip: disciplinované plnění context window | Karpathy Gist, X post | 2026-04-13 |
| [second-brain](concepts/second-brain.md) | Architektonický vzor pro osobní knowledge management s LLM | Karpathy, BASB, Zettelkasten, akademické papery | 2026-04-13 |
| [ecphory-rag](concepts/ecphory-rag.md) | Entity-centric KG RAG inspirovaný neurovědou: 94% token reduction | arXiv:2510.08958 | 2026-04-13 |
| [active-metacognitive-curation](concepts/active-metacognitive-curation.md) | Aktivní memory management: systém rozhoduje co udržovat/promovat/zahazovat | arXiv:2508.13171 | 2026-04-13 |
| [zettelkasten](concepts/zettelkasten.md) | Atomicita + connectivity: PKM metoda pro long-term knowledge emergence | zettelkasten.de | 2026-04-13 |
| [basb-code](concepts/basb-code.md) | Capture→Organize→Distill→Express: workflow pro transformaci informací | Tiago Forte | 2026-04-13 |
| [llm-wiki](concepts/llm-wiki.md) | Karpathyho vzor: LLM buduje markdown wiki místo RAG; token shift k "operating knowledge" | Karpathy Gist, CoderSera, EvoAI, X | 2026-04-14 |
| [rlvr](concepts/rlvr.md) | 4. fáze tréninku LLM: RL na ověřitelných odměnách → spontánní reasoning emergence | Karpathy blog 2025 | 2026-04-13 |
| [vibe-coding](concepts/vibe-coding.md) | Programování v přirozeném jazyce: kód je zdarma, pomíjivý, tvárný | Karpathy blog 2025 | 2026-04-13 |
| [jagged-intelligence](concepts/jagged-intelligence.md) | LLMs jako "přivolaní duchové": geniální v math/code, zmatkaní u triviálního | Karpathy blog 2025 | 2026-04-13 |
| [verifiability-sw2](concepts/verifiability-sw2.md) | SW 2.0 klíčový prediktor: verifikovatelné úkoly → dramatický AI pokrok | Karpathy blog Nov 2025 | 2026-04-13 |
| [memfactory](concepts/memfactory.md) | RL-based unifikovaný framework pro agent memory (extraction/updating/retrieval + GRPO, +14.8%) | arXiv:2603.29493 | 2026-04-14 |
| [agent-memory-taxonomy](concepts/agent-memory-taxonomy.md) | Write-Manage-Read loop + 5 rodin memory mechanismů + 3D taxonomie (temporal/substrate/control) | arXiv:2603.07670 | 2026-04-14 |
| [nurture-first-development](concepts/nurture-first-development.md) | NFD paradigma: agent začíná minimálně, roste z dialogu s experty; Knowledge Crystallization Cycle | arXiv:2603.10808 | 2026-04-15 |
| [reinforced-reasoning](concepts/reinforced-reasoning.md) | 3 pilíře reasoning LLM: data construction, RL (PRM>ORM), test-time scaling; 5 metod + STOPA mapování | arXiv:2501.09686 | 2026-04-15 |
| [memory-caching-rnn](concepts/memory-caching-rnn.md) | RNN + cachované memory checkpointy = O(L) až O(L²) interpolace; GRM gating; hybrid modely = MC se segment=1 | arXiv:2602.24281 | 2026-04-15 |
| [ai-empathic-templates](concepts/ai-empathic-templates.md) | 83-90% LLM odpovědí = 1 regex šablona; 10 taktik; struktura > slovník pro AI detection | arXiv:2604.08479 | 2026-04-15 |
| [rational-rewards](concepts/rational-rewards.md) | PARROT: reasoning reward model s 4-dim kritikou; dual-space (RL + test-time prompt refinement); 8B = Gemini-2.5-Pro | arXiv:2604.11626 | 2026-04-15 |
| [artifacts-as-memory](concepts/artifacts-as-memory.md) | Formální důkaz: env artefakty = external memory, 4× redukce interní kapacity; "artifacts first, scale second" | arXiv:2604.08756 | 2026-04-15 |
| [cpmi-process-reward](concepts/cpmi-process-reward.md) | CPMI: contrastive PMI jako step-level reward label bez MC rolloutů; −84% čas, −98% tokeny, ACL 2026 | arXiv:2604.10660 | 2026-04-16 |
| [think-prm](concepts/think-prm.md) | ThinkPRM: generativní PRM s CoT verifikací; 1% labelů, +8% OOD, +7.2% vs LLM-as-a-Judge | arXiv:2504.16828 | 2026-04-17 |
| [context-kubernetes](concepts/context-kubernetes.md) | Deklarativní knowledge orchestrace pro agenty; YAML manifesty, 3-tier permissions, TLA+ ověřeno | arXiv:2604.11623 | 2026-04-17 |
| [multi-agent-hpc](concepts/multi-agent-hpc.md) | Planner-executor na exascale HPC; shared MCP server coordination; Aurora supercomputer | arXiv:2604.07681 | 2026-04-17 |
| [tool-use-evolution](concepts/tool-use-evolution.md) | Survey: single→multi-tool orchestration; 6 dimenzí (planning, training, safety, efficiency, completeness, eval) | arXiv:2603.22862 | 2026-04-17 |
| [gaama](concepts/gaama.md) | Graph Augmented Associative Memory; 4 node types, PPR retrieval, 78.9% LoCoMo-10 SOTA | arXiv:2603.27910 | 2026-04-17 |
| [a-mem](concepts/a-mem.md) | Zettelkasten agentic memory: interconnected notes, new memories trigger updates to existing entries (NeurIPS 2025) | arXiv:2502.12110 | 2026-04-18 |
| [agentic-memory-unified](concepts/agentic-memory-unified.md) | Unified RL framework: memory ops as tools (store/retrieve/update/summarize/discard), step-wise GRPO | arXiv:2601.01885 | 2026-04-18 |
| [memory-augmented-routing](concepts/memory-augmented-routing.md) | 47% queries semantically similar; 8B+memory = 69% of 235B at 4% cost; hybrid BM25+cosine +7.7 F1 | arXiv:2603.23013 | 2026-04-18 |
| [agentforge](concepts/agentforge.md) | Execution-grounded SWE: 5 agents, Docker sandbox, 40% SWE-BENCH Lite (+26-28pp) | arXiv:2604.13120 | 2026-04-18 |
| [prompt-injection-defense](concepts/prompt-injection-defense.md) | Privilege separation (323×) + JSON formatting (7×) = 0% ASR; Claude Opus 4.5 = 0.5% vs Gemini 8.5% | arXiv:2603.13424 + arXiv:2603.15714 | 2026-04-18 |
| [critical-step-optimization](concepts/critical-step-optimization.md) | CSO: train only on verified critical steps; 37% improvement on GAIA, 16% trajectory coverage needed | arXiv:2602.03412 | 2026-04-18 |
| [multi-agent-orchestration-protocols](concepts/multi-agent-orchestration-protocols.md) | MCP + Agent2Agent protocols; governance/observability/accountability for enterprise | arXiv:2601.13671 | 2026-04-18 |
| [automated-alignment-researchers](concepts/automated-alignment-researchers.md) | 9 parallel Claude Opus 4.6 agents close 97% performance gap vs humans 23% in 7 days | Anthropic tweet 2026-04-14 | 2026-04-18 |
| [agentic-engineering-patterns](concepts/agentic-engineering-patterns.md) | Agentic engineering ≠ vibe coding; code is cheap now; red/green TDD with agents | Willison simonwillison.net | 2026-04-18 |
| [claude-code-design-space](concepts/claude-code-design-space.md) | 1.6% decision logic / 98.4% operational infra; 5-layer compaction; 7 perm modes; 27 hook events; sidechain isolation | arXiv:2604.14228 Liu et al. | 2026-04-18 |
| [claude-opus-47](concepts/claude-opus-47.md) | Claude Opus 4.7: 3× SWE tasks, 98.5% visual acuity, xhigh effort tier, tokenizer change 1.0–1.35× | Anthropic 2026-04 | 2026-04-20 |
| [architecture-descriptors-ai-agents](concepts/architecture-descriptors-ai-agents.md) | Formal architecture descriptors: −33–44% agent nav steps, −52% behavioral variance; S-expr > YAML for errors | arXiv:2604.13108 | 2026-04-20 |
| [on-device-rag-unified](concepts/on-device-rag-unified.md) | Unified on-device RAG: 1/10 context parity with server RAG; shared retrieval + compression model; privacy-first | arXiv:2604.14403 | 2026-04-20 |
| [kill-chain-canary](concepts/kill-chain-canary.md) | Kill-chain injection tracking EXPOSED→PERSISTED→RELAYED→EXECUTED; Claude 0/164 ASR; write-node = key defense | arXiv:2603.28013 | 2026-04-20 |

## People (3)

| Article | Summary | Updated |
|---------|---------|---------|
| [karpathy](people/karpathy.md) | Andrej Karpathy — LLM Wiki, RLVR, Vibe Coding, Ghosts vs Animals, Verifiability, Farzapedia, AI Capability Gap | 2026-04-18 |
| [tiago-forte](people/tiago-forte.md) | Tiago Forte — BASB, PARA, Progressive Summarization | 2026-04-13 |
| simon-willison | Simon Willison — Agentic Engineering Patterns, simonwillison.net | 2026-04-18 |

## Reasoning Patterns (5)

| Article | Summary | Updated |
|---------|---------|---------|
| [compiler-analogy](reasoning/compiler-analogy.md) | Raw sources = source code, LLM = compiler, wiki = binary | 2026-04-13 |
| [para-method](reasoning/para-method.md) | Projects/Areas/Resources/Archive — organizace podle actionability | 2026-04-13 |
| [progressive-summarization](reasoning/progressive-summarization.md) | Vrstevnatá distilace: highlight → bold → executive summary | 2026-04-13 |
| [two-generators](reasoning/two-generators.md) | Jeden retrieval pipeline, dva konzumenti: člověk a LLM | 2026-04-13 |

## Projects

_(zatím prázdné — naplní se s prvními /capture záznamy)_

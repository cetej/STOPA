# 2BRAIN Wiki — Master Index

Obsah kompilovaných wiki článků organizovaný podle typu entity.
LLM čte tento soubor PRVNÍ při odpovídání na dotazy.

**Last updated:** 2026-04-24
**Total articles:** 87

---

## Concepts (58)

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
| [system-prompt-archaeology](concepts/system-prompt-archaeology.md) | Willison: Claude system prompts → git repo; git log/diff/blame for prompt evolution tracking across model versions | simonwillison.net | 2026-04-21 |
| [knowledge-drift-chronos](concepts/knowledge-drift-chronos.md) | Chronos: Event Evolution Graph for time-aware retrieval; vanilla RAG fails under continuous knowledge drift | arXiv:2604.05096 | 2026-04-21 |
| [context-awareness-gate](concepts/context-awareness-gate.md) | CAG: dynamic gate deciding per-query whether retrieval is needed; prevents context contamination in RAG | arXiv:2411.16133 | 2026-04-21 |
| [swe-agents-survey](concepts/swe-agents-survey.md) | Survey 150+ papers/50+ benchmarks; agent-based SWE = SOTA; self-evolving systems = research frontier | arXiv:2510.09721 | 2026-04-21 |
| [adr-context-strategies](concepts/adr-context-strategies.md) | ADR generation: 3-5 prior records = optimal context window; context engineering > model scale | arXiv:2604.03826 | 2026-04-21 |
| [externalization-llm-agents](concepts/externalization-llm-agents.md) | Agents advance by reorganizing runtime, not weights; 3 externalization pillars (memory/skills/protocols) + harness engineering | arXiv:2604.08224 | 2026-04-21 |
| [knowledge-compounding](concepts/knowledge-compounding.md) | Tokens as capital goods: persistent KB lowers cost over time; 84.6% savings (47K vs 305K tokens); H(t) coverage rate model | arXiv:2604.11243 | 2026-04-21 |
| [missing-knowledge-layer](concepts/missing-knowledge-layer.md) | CoALA/JEPA lack Knowledge layer; 4-layer decomposition: Knowledge (supersession) / Memory (decay) / Wisdom (evidence-gated) / Intelligence (ephemeral) | arXiv:2604.11364 | 2026-04-21 |
| [semaclaw-harness-engineering](concepts/semaclaw-harness-engineering.md) | SemaClaw: open-source personal AI agent framework; DAG orchestration + PermissionBridge + 3-tier context + Agentic wiki | arXiv:2604.11548 | 2026-04-21 |
| [byterover](concepts/byterover.md) | Agent-native hierarchical memory: same LLM reasons + curates; 5-tier progressive retrieval; maturity tiers (draft→validated→core); SOTA LoCoMo | arXiv:2604.01599 | 2026-04-21 |
| [persistent-identity-agents](concepts/persistent-identity-agents.md) | Multi-anchor identity: distributed resilience (identity files + memory logs + skill memory); soul.py; RAG+RLM routing | arXiv:2604.09588 | 2026-04-21 |
| [process-reward-agents](concepts/process-reward-agents.md) | PRA: frozen policy + domain reward module = online step-wise verification; 80.8% MedQA Qwen3-4B SOTA; +25.7% without retraining | arXiv:2604.09482 | 2026-04-21 |
| [corpus2skill](concepts/corpus2skill.md) | Navigate don't retrieve: offline corpus→skill tree; bird's-eye navigation + backtracking; beats dense RAG/RAPTOR on WixQA | arXiv:2604.14572 | 2026-04-21 |
| [headless-services-ai](concepts/headless-services-ai.md) | API/MCP-first services for AI agents; headless > GUI for agent access; Salesforce Headless 360; SaaS pricing disruption | Willison simonwillison.net | 2026-04-22 |
| [training-data-poisoning](concepts/training-data-poisoning.md) | Adversarial data labeling (pelicans_riding_bicycles) as resistance to AI crawling; integrity concerns for web-trained models | Willison simonwillison.net | 2026-04-22 |
| [paramanager-orchestrator](concepts/paramanager-orchestrator.md) | Small Model as Master Orchestrator; Agent-as-Tool paradigm; parallel subtask decomposition; decoupled planning/execution | arXiv:2604.17009 | 2026-04-22 |
| [self-optimizing-deep-research](concepts/self-optimizing-deep-research.md) | Self-play prompt optimization for Deep Research agents; rivals expert-engineered systems; removes prompt engineering bottleneck | arXiv:2604.02988 | 2026-04-22 |
| [cocr-rag](concepts/cocr-rag.md) | CoCR-RAG: AMR-based concept distillation + context reconstruction for multi-source RAG; PopQA/EntityQuestions SOTA | arXiv:2603.23989 | 2026-04-22 |
| [adaptive-orchestration-dmoe](concepts/adaptive-orchestration-dmoe.md) | Generalization-Specialization Dilemma; DMoE dynamic agent pool; Meta-Cognition Engine + LRU eviction; Self-Evolving Concierge | arXiv:2601.09742 | 2026-04-22 |
| [qwen3-27b-dense-coding](concepts/qwen3-27b-dense-coding.md) | Qwen3.6-27B: 27B dense model matches 397B MoE on coding; 16.8 GB quantized = local inference viable | simonwillison.net | 2026-04-23 |
| [claude-code-pricing-incident](concepts/claude-code-pricing-incident.md) | Anthropic's Max plan pricing test rollback; trust erosion from opaque pricing changes; STOPA budget impact | simonwillison.net | 2026-04-23 |
| [mnemonic-sovereignty](concepts/mnemonic-sovereignty.md) | Security of LTM in LLM agents: 6-phase lifecycle, 9 governance primitives, no architecture covers all; STOPA gaps identified | arXiv:2604.16548 | 2026-04-23 |
| [camco-policy-orchestration](concepts/camco-policy-orchestration.md) | CAMCO: constraint-explicit middleware for enterprise MAS; 0 policy violations, 92-97% utility retention, 2.4 iterations | arXiv:2604.17240 | 2026-04-23 |
| [rag-dive](concepts/rag-dive.md) | Dynamic multi-turn RAG evaluation via LLM-simulated users; detects performance changes static benchmarks miss | arXiv:2604.16310 | 2026-04-23 |
| [analysis-bench-agents](concepts/analysis-bench-agents.md) | AnalysisBench: agentic architecture > model choice; 94% vs 77%; LLM self-validation overstates success | arXiv:2604.11270 | 2026-04-23 |
| [conformal-rag-filtering](concepts/conformal-rag-filtering.md) | Conformal prediction for RAG context filtering; 2-3× reduction with statistical coverage guarantees | arXiv:2511.17908 | 2026-04-23 |
| [single-multi-evolution-loop](concepts/single-multi-evolution-loop.md) | Multi-model collaboration + distillation loop: +8% individual, +14.9% collaborative; single-model inference cost | arXiv:2602.05182 | 2026-04-23 |
| [cognitive-fabric-nodes](concepts/cognitive-fabric-nodes.md) | CFN active middleware: memory + topology + semantic grounding + security; >10% improvement on HotPotQA/MuSiQue | arXiv:2604.03430 | 2026-04-23 |
| [sage-skill-library](concepts/sage-skill-library.md) | SAGE: RL-based skill library self-improvement; +8.9% completion, −26% steps, −59% tokens via skill reuse; GRPO | arXiv:2512.17102 | 2026-04-24 |
| [resilient-write-mcp](concepts/resilient-write-mcp.md) | Six-layer durable write surface for LLM coding agents; 5× recovery speedup, 13× self-correction rate | arXiv:2604.10842 | 2026-04-24 |
| [coars-agentic-recommenders](concepts/coars-agentic-recommenders.md) | CoARS: co-evolving recommender+user agents via self-distilled RL; coupled supervision + token-level credit assignment | arXiv:2604.10029 | 2026-04-24 |
| [single-vs-multi-agent-tokens](concepts/single-vs-multi-agent-tokens.md) | Single-agent matches/exceeds MAS on multi-hop reasoning under equal token budgets; Data Processing Inequality | arXiv:2604.02460 | 2026-04-24 |
| [meta-harness-optimization](concepts/meta-harness-optimization.md) | Automated harness optimization via code search; +7.7 accuracy, −75% context tokens vs SOTA; TerminalBench-2 | arXiv:2603.28052 | 2026-04-24 |
| [ai-disempowerment-patterns](concepts/ai-disempowerment-patterns.md) | Anthropic: 1 in 50–70 conversations mildly disempowering; users seek disempowerment; 3 dimensions (reality/value/action) | Anthropic Research 2026 | 2026-04-24 |
| [ai-coding-skill-atrophy](concepts/ai-coding-skill-atrophy.md) | AI delegation → 17% lower comprehension; debugging gap largest; strategic use preserves mastery | Anthropic Research | 2026-04-24 |
| [ai-transforming-work-anthropic](concepts/ai-transforming-work-anthropic.md) | 28→59% daily work, 9.8→21.2 consecutive calls; delegation heuristics; 27% entirely new work created | Anthropic Research 2026 | 2026-04-24 |
| [anthropic-amazon-5gw-compute](concepts/anthropic-amazon-5gw-compute.md) | Anthropic-AWS: up to 5 GW secured for training + inference; 1 GW by Q4 2026 | @AnthropicAI tweet 2026-04-20 | 2026-04-24 |

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

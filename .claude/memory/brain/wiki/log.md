# 2BRAIN Log

Append-only chronologický záznam ingestů, dotazů a maintenance průchodů.

---

| Date | Event | Articles touched | Source |
|------|-------|-----------------|--------|
| 2026-04-13 | INIT: 2BRAIN založen na základě deepresearch | 5 seed articles | outputs/2brain-research.md |
| 2026-04-13 | SEED: context-engineering, second-brain, compiler-analogy, karpathy | index.md created | Karpathy Gist, BASB, Zettelkasten |
| 2026-04-13 | COMPILE: 8 new articles (ecphory-rag, active-metacognitive-curation, zettelkasten, basb-code, para-method, progressive-summarization, two-generators, tiago-forte) | 13 total articles | Research R1-R3 |
| 2026-04-13 | GRAPH: expanded to 19 nodes, 25 edges (added tiago-forte, cognitive-workspace, personal-ai, para-method, progressive-summarization, two-generators, active-metacognitive-curation) | knowledge-graph.json v1.1 | — |
| 2026-04-13 | RAW: archived 3 research outputs (karpathy, academic, pkm-tools) | raw/ 3 files | deepresearch pipeline |
| 2026-04-13 | INGEST: karpathy.bearblog.dev — 12 blog posts (2024-2025) | +4 new articles (rlvr, vibe-coding, jagged-intelligence, verifiability-sw2), updated karpathy.md | brain-ingest scheduled task |
| 2026-04-13 | GRAPH: expanded to 23 nodes, 35 edges (v1.2) — added rlvr, vibe-coding, jagged-intelligence, verifiability-sw2 | knowledge-graph.json v1.2 | — |
| 2026-04-14 | INGEST: 5 inbox items — MemFactory (arXiv:2603.29493), Agent Memory Survey (arXiv:2603.07670), 3× Karpathy LLM Wiki articles (CoderSera, EvoAI, X) | +2 new articles (memfactory, agent-memory-taxonomy), updated llm-wiki.md + karpathy.md | brain-ingest scheduled task |
| 2026-04-14 | GRAPH: expanded to 26 nodes, 46 edges (v1.3) — added memfactory, agent-memory-taxonomy, operating-knowledge + 11 new edges | knowledge-graph.json v1.3 | — |
| 2026-04-15 | INGEST: arXiv:2603.10808 — Nurture-First Development | +1 new article (nurture-first-development.md) | brain-ingest (manual run) |
| 2026-04-15 | GRAPH: expanded to 27 nodes, 54 edges (v1.4) — added nurture-first-development + 8 new edges | knowledge-graph.json v1.4 | — |
| 2026-04-15 | FIX: brain-ingest absolute path opravena, /capture hybrid routing implementována (URL→inbox, text→direct) | — | maintenance |
| 2026-04-15 | CAPTURE: RationalRewards (arXiv:2604.11626) — PARROT reasoning reward model, dual-space optimization | +1 new article (rational-rewards.md), graph +1 node +3 edges | /capture (text) |
| 2026-04-15 | CAPTURE: AI Empathic Templates (arXiv:2604.08479) — 10 taktik, regex šablona, struktura > slovník | +1 new article (ai-empathic-templates.md), graph +1 node +3 edges | /capture (text) |
| 2026-04-15 | CAPTURE: Memory Caching (arXiv:2602.24281) — RNN + checkpoint caching, O(L)↔O(L²) interpolace, 4 varianty | +1 new article (memory-caching-rnn.md), graph +1 node +4 edges | /capture (text) |
| 2026-04-15 | CAPTURE: Artifacts as Memory (arXiv:2604.08756) — formální důkaz external memory, 4× kapacitní redukce, emergentní traces | +1 new article (artifacts-as-memory.md), graph +1 node +6 edges | /capture (text) |
| 2026-04-16 | INGEST: arXiv:2604.10660 — CPMI (Contrastive Process Reward Modeling, ACL 2026); −84% dataset time, −98% token gen | +1 new article (cpmi-process-reward.md), graph +1 node +4 edges (v1.5) | brain-ingest scheduled task |
| 2026-04-17 | INGEST: 6 inbox items — ThinkPRM (2504.16828), Context Kubernetes (2604.11623), Multi-Agent HPC (2604.07681), Tool Use Evolution (2603.22862), GAAMA (2603.27910), Karpathy LLM KB tweet | +5 new articles, updated llm-wiki.md, graph +5 nodes +16 edges (v1.6) | brain-ingest scheduled task |
| 2026-04-18 | ADOPT: multica-ai/andrej-karpathy-skills (57k★ CLAUDE.md) — gap analysis against STOPA behavioral-genome; 2 rules adopted (match-existing-style, mention-dead-code) + ambiguity surfacing | updated karpathy.md + behavioral-genome.md (+Code Editing Discipline section) | manual review |
| 2026-04-18 | INGEST: arXiv:2604.14228 — Dive into Claude Code (Liu et al., VILA Lab/UCL); 1.6%/98.4% ratio, 5-layer compaction, 7 perm modes, 27 hook events, sidechain design, CC vs OpenClaw | +1 new article (claude-code-design-space.md), +2 STOPA learnings, graph +2 nodes +8 edges (v1.8) | /ingest (manual) |
| 2026-04-18 | INGEST: 12 inbox items — A-MEM (2502.12110), Agentic Memory RL (2601.01885), Memory-Augmented Routing (2603.23013), AgentForge (2604.13120), OpenClaw injection defense (2603.13424), Critical Step Optimization (2602.03412), Injection competition (2603.15714), MAS orchestration protocols (2601.13671), 4 social posts (Karpathy ×2, Anthropic AAR, Willison agentic-eng) | +10 new wiki articles, updated karpathy.md + llm-wiki.md, graph +13 nodes +38 edges (v1.7) | brain-ingest scheduled task |
| 2026-04-20 | INGEST: 6 inbox items — Claude Opus 4.7 (Anthropic), Architecture Descriptors (2604.13108), On-Device RAG (2604.14403), Kill-Chain Canary (2603.28013), transformer-circuits emotions (403 skip), deedydas Claude codenames tweet (speculative/skip) | +4 new wiki articles, graph +4 nodes +16 edges (v1.9) | brain-ingest scheduled task |
| 2026-04-20 | CONFIG: added Bash(python3 *), Bash(python3 -m *), Bash(powershell *) to settings.json permissions.allow — scheduled tasks bypass PermissionRequest hook, need explicit allowlist | — | less-permission-prompts scan |

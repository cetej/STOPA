# 2BRAIN Inbox

Sem přidej URL nebo text k zachycení. Scheduled task `brain-ingest` je zpracuje automaticky.

Format: jeden záznam per řádek. Prefix určuje typ:
- `URL: https://...` — fetch a kompiluj do wiki
- `IDEA: text...` — přímý capture myšlenky
- `WATCH: https://...` — přidej do watchlistu pro pravidelný monitoring

Zpracované záznamy se přesunou do `inbox-archive.md`.

---

## Queue

URL: https://simonwillison.net/2026/Apr/22/qwen36-27b/
URL: https://simonwillison.net/2026/apr/22/claude-code-confusion/
URL: https://arxiv.org/abs/2604.16548
URL: https://arxiv.org/abs/2604.17240
URL: https://arxiv.org/abs/2604.16310
URL: https://arxiv.org/abs/2604.11270
URL: https://arxiv.org/abs/2511.17908
URL: https://arxiv.org/abs/2602.05182
URL: https://arxiv.org/abs/2604.03430

## Processed

| Date | Item |
|------|------|
| 2026-04-13 | URL: https://karpathy.bearblog.dev/ — zpracováno, 4 nové wiki články |
| 2026-04-14 | URL: https://arxiv.org/abs/2603.29493 — MemFactory paper → new wiki article memfactory.md |
| 2026-04-14 | URL: https://arxiv.org/abs/2603.07670 — Agent Memory Survey → new wiki article agent-memory-taxonomy.md |
| 2026-04-14 | URL: https://ghost.codersera.com/blog/karpathy-llm-knowledge-base-second-brain/ — Karpathy LLM KB → updated llm-wiki.md (3-folder arch, limits) |
| 2026-04-14 | URL: https://evoailabs.medium.com/why-andrej-karpathys-llm-wiki-is-the-future-of-personal-knowledge-7ac398383772 — LLM Wiki EvoAI → updated llm-wiki.md (compounding, RAG critique) |
| 2026-04-14 | URL: https://x.com/ICPandaDAO/status/2040434533619892603 — Karpathy operating knowledge → updated llm-wiki.md + karpathy.md + new graph node |
| 2026-04-15 | URL: https://arxiv.org/abs/2603.10808 — Nurture-First Development → new wiki article nurture-first-development.md, 8 graph edges |
| 2026-04-16 | URL: https://arxiv.org/abs/2604.10660 — CPMI Process Reward Modeling (ACL 2026) → new wiki article cpmi-process-reward.md, 4 graph edges |
| 2026-04-17 | URL: https://arxiv.org/abs/2504.16828 — ThinkPRM → new wiki article think-prm.md, 4 graph edges |
| 2026-04-17 | URL: https://arxiv.org/abs/2604.11623 — Context Kubernetes → new wiki article context-kubernetes.md, 3 graph edges |
| 2026-04-17 | URL: https://arxiv.org/abs/2604.07681 — Multi-Agent HPC → new wiki article multi-agent-hpc.md, 2 graph edges |
| 2026-04-17 | URL: https://arxiv.org/abs/2603.22862 — Tool Use Evolution → new wiki article tool-use-evolution.md, 2 graph edges |
| 2026-04-17 | URL: https://arxiv.org/abs/2603.27910 — GAAMA → new wiki article gaama.md, 5 graph edges |
| 2026-04-17 | URL: https://x.com/karpathy/status/2039805659525644595 — Karpathy LLM KB tweet → updated llm-wiki.md (Operační workflow sekce) |
| 2026-04-18 | URL: https://arxiv.org/abs/2502.12110 — A-MEM (NeurIPS 2025) → new wiki article a-mem.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2601.01885 — Agentic Memory RL → new wiki article agentic-memory-unified.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2603.23013 — Memory-Augmented Routing → new wiki article memory-augmented-routing.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2604.13120 — AgentForge → new wiki article agentforge.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2603.13424 — OpenClaw prompt injection → merged into prompt-injection-defense.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2602.03412 — Critical Step Optimization → new wiki article critical-step-optimization.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2603.15714 — Injection competition → merged into prompt-injection-defense.md |
| 2026-04-18 | URL: https://arxiv.org/abs/2601.13671 — MAS orchestration protocols → new wiki article multi-agent-orchestration-protocols.md |
| 2026-04-18 | URL: https://x.com/karpathy/status/2042334451611693415 — Karpathy AI capability gap → updated karpathy.md, new graph node |
| 2026-04-18 | URL: https://x.com/karpathy/status/2040572272944324650 — Karpathy Farzapedia → updated karpathy.md + llm-wiki.md, new graph node |
| 2026-04-18 | URL: https://x.com/AnthropicAI/status/2044138483870998932 — Anthropic automated alignment researchers → new wiki article automated-alignment-researchers.md |
| 2026-04-18 | URL: https://x.com/simonw/status/2025990408514523517 — Willison agentic engineering → new wiki article agentic-engineering-patterns.md |
| 2026-04-20 | URL: https://www.anthropic.com/news/claude-opus-4-7 — Claude Opus 4.7 → new wiki article claude-opus-47.md, graph +1 node +3 edges |
| 2026-04-20 | URL: https://transformer-circuits.pub/2026/emotions/index.html — 403 Forbidden, skip |
| 2026-04-20 | URL: https://arxiv.org/abs/2604.13108 — Formal Architecture Descriptors → new wiki article architecture-descriptors-ai-agents.md, graph +1 node +4 edges |
| 2026-04-20 | URL: https://arxiv.org/abs/2604.14403 — On-Device RAG Unified Model → new wiki article on-device-rag-unified.md, graph +1 node +4 edges |
| 2026-04-20 | URL: https://arxiv.org/abs/2603.28013 — Kill-Chain Canaries → new wiki article kill-chain-canary.md, graph +1 node +4 edges |
| 2026-04-20 | URL: https://x.com/deedydas/status/2020350881464742330 — speculative Claude codenames (unofficial), skip |
| 2026-04-21 | URL: https://simonwillison.net/2026/Apr/18/extract-system-prompts/ — Willison system prompt archaeology → new wiki article system-prompt-archaeology.md, graph +1 node +5 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.05096 — Chronos: Knowledge Drift in LLMs → new wiki article knowledge-drift-chronos.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2411.16133 — Context Awareness Gate (CAG) for RAG → new wiki article context-awareness-gate.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2510.09721 — LLM-SWE Agents Survey (150+ papers, 50+ benchmarks) → new wiki article swe-agents-survey.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.03826 — ADR Context Strategies: 3-5 records optimal → new wiki article adr-context-strategies.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.08224 — Externalization in LLM Agents (memory/skills/protocols/harness) → new wiki article externalization-llm-agents.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.11243 — Knowledge Compounding (Agentic ROI, 84.6% token savings) → new wiki article knowledge-compounding.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.11364 — Missing Knowledge Layer in Cognitive Architectures → new wiki article missing-knowledge-layer.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.11548 — SemaClaw harness engineering (DAG orchestration, PermissionBridge) → new wiki article semaclaw-harness-engineering.md, graph +1 node +5 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.01599 — ByteRover agent-native hierarchical memory (5-tier retrieval, AKL) → new wiki article byterover.md, graph +1 node +5 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.09588 — Persistent Identity multi-anchor architecture (soul.py, RAG+RLM) → new wiki article persistent-identity-agents.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.09482 — Process Reward Agents (PRA, 80.8% MedQA, step-wise rewards) → new wiki article process-reward-agents.md, graph +1 node +4 edges |
| 2026-04-21 | URL: https://arxiv.org/abs/2604.14572 — Corpus2Skill navigable RAG (hierarchical skill dirs, beats RAPTOR) → new wiki article corpus2skill.md, graph +1 node +5 edges |
| 2026-04-22 | URL: https://simonwillison.net/2026/Apr/19/headless-everything/ — Headless Everything for Personal AI → new wiki article headless-services-ai.md, graph +1 node +3 edges |
| 2026-04-22 | URL: https://simonwillison.net/2026/Apr/21/scosman/ — Training data poisoning (pelicans_riding_bicycles) → new wiki article training-data-poisoning.md, graph +1 node +2 edges |
| 2026-04-22 | URL: https://arxiv.org/abs/2604.17009 — Small Model as Master Orchestrator (ParaManager) → new wiki article paramanager-orchestrator.md, graph +1 node +4 edges |
| 2026-04-22 | URL: https://arxiv.org/abs/2604.02988 — Self-Optimizing Multi-Agent Deep Research (ECIR 2026) → new wiki article self-optimizing-deep-research.md, graph +1 node +4 edges |
| 2026-04-22 | URL: https://arxiv.org/abs/2603.23989 — CoCR-RAG concept-oriented context reconstruction → new wiki article cocr-rag.md, graph +1 node +4 edges |
| 2026-04-22 | URL: https://arxiv.org/abs/2604.13120 — DUPLICATE SKIP (AgentForge already processed 2026-04-18) |
| 2026-04-22 | URL: https://arxiv.org/abs/2601.09742 — Adaptive Orchestration DMoE (Self-Evolving Concierge, Meta-Cognition Engine) → new wiki article adaptive-orchestration-dmoe.md, graph +1 node +5 edges |

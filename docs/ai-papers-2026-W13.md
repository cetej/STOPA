# Top AI Papers — Week 13, 2026 (March 23–29)

Source: https://twitter.com/... (repost, 29. 3. 2026)

---

## 1. Hyperagents — Self-referential self-improvement
https://arxiv.org/abs/2603.19461

Self-referential agents combining task agent + meta agent into a single editable program. Meta-level modification procedure is itself editable (metacognitive self-modification). DGM-Hyperagents eliminates assumption that task performance and self-modification skill must be aligned → domain-general self-improvement. Outperforms DGM and baselines.

**Relevance:** STOPA self-improvement loop, orchestrate skill meta-level.

---

## 2. Agentic AI and the Next Intelligence Explosion
https://arxiv.org/abs/2603.20639

Google researchers: AI "singularity" will be social, not individual. Frontier reasoning models simulate internal "societies of thought." Argues for institutional alignment (organizations/markets) over dyadic RLHF alignment. Human-AI centaurs as hybrid actors.

**Relevance:** Conceptual framing for multi-agent orchestration design.

---

## 3. ARC-AGI-3
https://arxiv.org/abs/2603.24621

Interactive benchmark for agentic intelligence via novel turn-based environments. Humans: 100%, frontier AI: <1%. Core Knowledge priors only (no language/external knowledge). Efficiency-based scoring: hard cutoff at 5× human action count.

**Relevance:** Benchmark to watch; illustrates gap between current AI and adaptive reasoning.

---

## 4. Claudini — Autonomous adversarial attack discovery via Claude Code
https://arxiv.org/abs/2603.24511

Autoresearch pipeline using Claude Code autonomously discovers novel adversarial LLM attack algorithms, outperforming all 30+ existing methods. Starting from GCG → iterates to 40% ASR on CBRN queries vs 10% for baselines. Attacks transfer to held-out models (100% ASR on Meta-SecAlign-70B vs 56% baseline). White-box red-teaming suits autoresearch due to dense quantitative feedback. Open-source.

**Relevance: HIGH** — Direct model for `/autoresearch` skill. Proves Claude Code agent loop can produce novel research autonomously.

---

## 5. Attention Residuals (AttnRes)
https://arxiv.org/abs/2603.15031

Kimi/Moonshot: replaces fixed unit-weight residual connections with softmax attention over preceding layer outputs. Content-dependent depth-wise selection. Block AttnRes for scalability. Mitigates PreNorm dilution. Tested on 48B/3B activated model, 1.4T tokens.

**Relevance:** Low — architecture research, not actionable for NGM stack.

---

## 6. MemCollab — Agent-agnostic collaborative memory
https://arxiv.org/abs/2603.23234

Collaborative memory framework: contrasts reasoning trajectories from different agents on same task → distills abstract reasoning constraints (agent-agnostic). Task-aware retrieval conditioned on task category. Improves accuracy + efficiency across diverse agents incl. cross-family settings.

**Relevance: MEDIUM** — Interesting pattern for STOPA memory architecture: shared memory across different Claude model tiers (Haiku/Sonnet/Opus agents).

---

## 7. Composer 2 — Cursor's agentic coding model
https://arxiv.org/abs/2603.24477

Two-phase training: continued pretraining + large-scale RL. Train-in-harness infrastructure matching deployment environment. CursorBench (real large codebase problems). Scores: 61.7 Terminal-Bench, 73.7 SWE-bench Multilingual. Domain-specialized RL competes with larger general models.

**Relevance:** Ecosystem context — competitor/reference for harness eval design.

---

## 8. PivotRL — Turn-level RL for long-horizon agents
https://arxiv.org/abs/2603.21383

NVIDIA: identifies "pivots" (high-variance intermediate turns) in SFT trajectories and focuses RL training signal there. +4.17% in-domain, +10.04% out-of-domain vs SFT. 4× fewer rollout turns vs end-to-end RL. Adopted by Nemotron-3-Super-120B.

**Relevance:** Low — training methodology, not inference-time actionable.

---

## 9. Workflow Optimization for LLM Agents (IBM Survey)
https://arxiv.org/abs/2603.22386

Maps methods for designing/optimizing LLM agent workflows as agentic computation graphs (ACGs). Three dimensions: when structure is determined, what is optimized, which evaluation signals guide optimization. Covers AFlow (MCTS over operator graphs), ADAS (code-space search via meta-agents), evolutionary multi-agent design.

**Relevance: HIGH** — Already captured in `reference_ibm_workflow_optimization.md`. Extend with ACG framing.

---

## 10. BIGMAS — Brain-inspired graph multi-agent systems
https://arxiv.org/abs/2603.15371

Organizes specialized LLM agents as nodes in dynamically constructed directed graph, coordinating via centralized shared workspace (global workspace theory). GraphDesigner agent produces task-specific agent graph + workspace contract. Graph complexity tracks task demands (3-node to 9-node cyclic). Outperforms multi-agent baselines on reasoning + planning.

**Relevance: MEDIUM** — Directed graph + shared workspace = interesting pattern for STOPA orchestrate. Centralized workspace maps to STOPA memory files.

---

## Summary — Actionable for NGM

| Paper | Action |
|-------|--------|
| Claudini | Study autoresearch loop design for `/autoresearch` improvement |
| Hyperagents | Consider editable meta-level for STOPA orchestrate self-improvement |
| MemCollab | Explore agent-agnostic memory patterns for cross-tier Claude sharing |
| BIGMAS | GraphDesigner pattern for dynamic orchestration graphs |
| IBM Survey | Update `reference_ibm_workflow_optimization.md` with ACG framing |

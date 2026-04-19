---
name: Optimization & RL Research Cluster
description: Papers on RL optimization, prompt evolution, learning primitives — informing STOPA iterative skills
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Cluster of RL/optimization papers informing STOPA iterative skill design.

| Paper | Key Finding | STOPA Impact |
|-------|------------|--------------|
| RCL (arXiv:2604.03189) | 7 optimization primitives for context-space learning | Dual-trace, optimizer state, failure replay |
| EGGROLL (Oxford/MILA) | Low-rank ES, GRPO scoring, adaptive sigma | Adopted into prompt-evolve, self-evolve, autoloop |
| GDPO (arXiv:2601.05242) | Multi-reward RL: decouple per-reward norm | Conditional gating for priority ordering |
| MCMC sampling (arXiv:2510.14901) | Sampling from p^α matches RL on reasoning | No training needed, base models underestimated |
| ASI-Evolve (arXiv:2603.29640) | Analyzer modul, UCB1/MAP-Elites, L_task difficulty | Autonomous research framework |
| Principia (arXiv:2603.18886) | On-policy judges >> prompted, MC shortcutting = rationalization | Rule-based verification brittle |
| Acemoglu (arXiv:2604.04906) | Global aggregator hurts ≥1 dim | skill_scope + circular detection + inverse freq |
| GEPA (arXiv:2604.02988) | Evolutionary prompt optimization | Basis for /prompt-evolve |
| HERA (Virginia Tech) | Failure-driven learning +38.69%, Experience Library + RoPE | Integration plan in HERA_INTEGRATION.md |
| Meta-Harness (arXiv:2603.28052) | Full traces >> summaries for optimization | Integrated into autoloop/autoresearch/self-evolve |
| SD-ZERO (arXiv:2604.12002) | Self-revision → dense token-level supervision from binary rewards, -50% length | Self-check before critic pattern, error localization, repair loop improvement |

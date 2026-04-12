---
name: reference_selfoptimizing_prompts
description: "arXiv:2604.02988 — GEPA evolutionary prompt optimization outperforms expert-crafted prompts; basis for /prompt-evolve skill and prompt-library.yaml"
type: reference
---

**Paper:** "Self-Optimizing Multi-Agent Systems for Deep Research" (Câmara, Slot, Zavrel, ECIR 2026 Workshop)
**arXiv:** 2604.02988

**Architecture:** 4-agent pipeline (Orchestrator → Reader → Aggregator → Writer) — validates STOPA /deepresearch decomposition.

**Key finding:** GEPA (Genetic-Pareto evolutionary algorithm) > TextGrad (greedy hill-climbing) > expert prompts > OpenAI optimizer.
- Weak prompt + GEPA: 0.513 → 0.705 (+37%)
- Expert prompt + GEPA: 0.667 → 0.701 (+5%)
- Generic optimizer (OpenAI): 0.583-0.667 (underperforms due to lack of task-specific feedback)

**STOPA integration:**
- `prompt-library.yaml` — centrální YAML s extrahovanými prompt templates (image styles, video negative prompts, suffixes, TTS voice settings)
- `/prompt-evolve` skill — GEPA-inspired evolutionary optimization: SEED → MUTATE (5 variants) → GENERATE → EVALUATE (vision rubric) → SELECT (Pareto) → PERSIST
- `/nano` a `/klip` skills modifikovány pro čtení z prompt-library
- Eval rubric: Composition (0.25) + Clarity (0.25) + Relevance (0.25) + Aesthetic (0.25)

**Practical implication:** Meta-prompt customization matters — generic optimization fails. Task-specific eval criteria are essential.

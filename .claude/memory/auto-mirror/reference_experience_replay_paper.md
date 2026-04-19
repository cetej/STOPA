---
name: Experience Replay pro LLM RL Training
description: Meta FAIR 2026: replay buffer šetří 40% compute v RL post-training; STOPA aplikace — outcomes reuse v Phase 0 iterativních skills
type: reference
---

arXiv:2604.08706 (Meta FAIR, 2026-04-13): "Efficient RL Training for LLMs with Experience Replay"
Autoři: Arnal, Cabannes, Cohen, Kempe, Munos

**Core finding:** Strict on-policy (generate-then-discard) je suboptimální pokud je inference drahá (μ=4-10×). Replay buffer šetří 40% compute při stejné nebo vyšší přesnosti.

**Key mechanism:** FIFO buffer N trajektorií, uniform sampling. Optimal design (Theorem 4.5): N/R = f(staleness variance σ², correlation ρ, cost ratio μ).

**STOPA implikace:**
1. outcomes/ = replay buffer — ale skills ho v Phase 0 nečtou (gap)
2. optstate/ = optimizer momentum — existuje, ale cold_start (total_runs=0 v autoloop)
3. replay-queue.md = HERA replay validace — existuje, ale prázdná
4. Positive-bias: číst "What Worked" z outcomes prioritně, "What Failed" jako anticuriculum
5. W/T ratio analogie: deep tier = vyšší critic:scout ratio (více iterací, méně generace)

**Learnings zapsány:** 2026-04-13-experience-replay-outcomes-reuse.md, 2026-04-13-generate-then-discard-suboptimal.md

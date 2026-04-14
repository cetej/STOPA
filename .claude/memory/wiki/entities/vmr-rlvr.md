---
name: VMR-RLVR
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [vmr-rlvr-open-ended-verifiable-rewards]
tags: [rl-training, policy-optimization, evaluation, open-ended-tasks, pairwise-comparison]
---

# VMR-RLVR

> Verifiable Multiple-Choice Reformulation for RLVR — rozšiřuje RLVR na open-ended úlohy tím, že přeformuluje generativní úlohy na binární výběr (which is better?), čímž zachovává verifiable reward signal.

## Key Facts

- Core mechanismus: pro každou open-ended úlohu vytvoří pár (chosen, rejected) odpovědí → model volí lepší → 1/0 feedback (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)
- Nevyžaduje reward model (na rozdíl od RLHF) — verifiable signal z pairwise choice bez auxiliary networks (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)
- Reasoning modely: +3.29 bodů průměrně, DeepSeek-R1-Distill-Qwen-14B překonal 32B model (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)
- Non-reasoning modely (Qwen2.5-14B-Instruct): minimální zlepšení → funguje jen u modelů s existující reasoning schopností (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)
- VMR-RLVR > DPO (Direct Preference Optimization) — naučí se hlubší porozumění kvalitě, ne jen napodobování dat (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)
- Kvalitativní zlepšení: méně repetice, hlubší analýza, lepší porozumění implicitním/metaforickým významům (ref: sources/vmr-rlvr-open-ended-verifiable-rewards.md)

## Relevance to STOPA

Pairwise comparison pattern je přesně to, co STOPA autoreason skill dělá (A vs B → výběr lepšího). VMR-RLVR ukazuje, že tato struktura je dostatečná pro stabilní učení — STOPA critic jako "verifier" v iterativní smyčce má akademické opodstatnění. Potvrzuje Tool-Genesis scale reversal: reasoning modely profitují víc z iterativního feedbacku než non-reasoning modely.

## Mentioned In

- [VMR-RLVR: Open-Ended Verifiable Rewards](../sources/vmr-rlvr-open-ended-verifiable-rewards.md)

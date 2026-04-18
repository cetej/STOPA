---
date: 2026-04-15
source_type: text
source_url: https://arxiv.org/abs/2604.11626
---

# RationalRewards (arXiv:2604.11626)

PARROT framework pro reasoning-based reward modely. Místo skalárního skóre produkuje strukturovanou kritiku ve 4 dimenzích (text faithfulness, image faithfulness, visual quality, text rendering).

PARROT = rationales jako latentní proměnné přes ELBO — teacher generuje zdůvodnění zakotvená v preference labels, consistency filtering ponechá jen prediktivní rationale, student distilace bez labelu. 10-20× méně dat než skalární baselines.

Dual-space optimization: parameter space (RL s multi-dim skóry) + prompt space (Generate→Critique→Refine loop za inference bez update vah). 8B model = Gemini-2.5-Pro na preference prediction. Test-time refinement matches/exceeds RL fine-tuning.

Klíčový insight: structured reasoning jako inductive bias brání reward hackingu a odemyká latentní capability generátorů, které suboptimální prompty nevyužijí.

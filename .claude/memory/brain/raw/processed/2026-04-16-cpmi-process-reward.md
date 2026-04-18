---
date: 2026-04-16
source_type: url
source_url: https://arxiv.org/abs/2604.10660
---

# Efficient Process Reward Modeling via Contrastive Mutual Information (arXiv:2604.10660)

ACL 2026. Autoři: Nakyung Lee, Sangwoo Hong, Jungwoo Lee.

Problem: Trénování Process Reward Models (PRM) vyžaduje buď drahé lidské anotace krok po kroku, nebo výpočetně náročné Monte Carlo estimace (MC rollouts z každého intermediate stavu).

Řešení: CPMI (Contrastive Pointwise Mutual Information) — automatická metoda pro labeling step-level odměn bez human annotation ani MC rollouts. Kvantifikuje, o kolik konkrétní reasoning krok zvyšuje mutual information mezi krokem a správnou odpovědí — relativně vůči "hard-negative" alternativám. Využívá interní pravděpodobnostní distribuce modelu.

Výsledky: 84% redukce času na dataset construction (vs Monte Carlo), 98% redukce požadavků na generování tokenů. Vyšší přesnost na process-level evaluacích a matematických reasoning benchmarcích.

Klíčový insight: PMI jako proxy pro "příspěvek kroku k řešení" je efektivnější signál než MC rollout estimates, protože kontrastuje se špatnými alternativami (hard negatives), nikoli jen s průměrným výstupem.

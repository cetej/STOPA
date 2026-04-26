---
title: Credit Assignment v Reinforcement Learningu pro velké jazykové modely
url: https://arxiv.org/abs/2604.09459
date: 2026-04-26
concepts: ["Credit Assignment Problem", "Reasoning RL vs Agentic RL", "Process Reward Models", "Multi-turn prostředí", "Temporal Difference Learning", "Hindsight Counterfactual Analysis", "Granularita přiřazování (token/segment/step/turn)", "Privilegované asymetrické kritiky"]
entities: ["Chenchen Zhang", "arXiv"]
source: brain-ingest-local
---

# Credit Assignment v Reinforcement Learningu pro velké jazykové modely

**URL**: https://arxiv.org/abs/2604.09459

## Key Idea

Systematický přehled 47 metod přiřazování kreditu (credit assignment) v reinforcement learningu pro LLM, rozlišující mezi reasoning RL (tokeny v chain-of-thought) a agentic RL (multi-turn interakce s prostředím).

## Claims

- Credit assignment v reasoning RL (500-30K+ tokenů) a agentic RL (100K-1M tokenů) představují odlišné výzvy – agentic RL zahrnuje stochastické přechody a částečnou pozorovatelnost
- Reasoning CA dozrává kolem process reward models a critic-free group comparison, zatímco agentic CA vyžaduje nové přístupy bez precedentu v reasoning RL
- Studie poskytuje trojici znovu použitelných zdrojů: strukturovaný inventář paper s taxonomií, reporting checklist a benchmark protokol s rozhodovacím stromem pro výběr metod
- Taxonomie organizuje metody podle granularity (token, segment, step, turn, multi-agent) a metodologie (Monte Carlo, temporal difference, model-based, game-theoretic, information-theoretic)

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení credit assignment v multi-turn agentic scénářích, kde je potřeba vyhodnocovat příspěvek jednotlivých akcí agentů v dlouhých trajektoriích s částečnou pozorovatelností – to je přímo aplikovatelné na koordinaci a učení v multi-agentních STOPA systémech.

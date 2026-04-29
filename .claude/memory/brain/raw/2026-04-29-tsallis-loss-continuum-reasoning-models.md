---
title: Tsallis loss: kontinuum mezi RL a SFT pro trénink reasoning modelů
url: http://arxiv.org/abs/2604.25907v1
date: 2026-04-29
concepts: ["Tsallis q-logarithm", "RLVR (reinforcement learning from verifiable rewards)", "cold-start problém", "gradient amplification", "GARL (Gradient-Amplified RL)", "PAFT (Posterior-Attenuated Fine-Tuning)", "reasoning models", "ztrátové funkce"]
entities: ["Chu-Cheng Lin", "Eugene Ie"]
source: brain-ingest-local
---

# Tsallis loss: kontinuum mezi RL a SFT pro trénink reasoning modelů

**URL**: http://arxiv.org/abs/2604.25907v1

## Key Idea

Článek zavádí rodinu ztrátových funkcí J_Q založenou na Tsallisově q-logaritmu, která interpoluje mezi reinforcement learningem (q=0) a supervised fine-tuningem (q=1), řeší problém cold-startu při malé počáteční úspěšnosti a nabízí dva estimátory: GARL a PAFT.

## Claims

- Exploitation pólu (q=0) vyžaduje Ω(1/p_0) času na únik z cold-startu, zatímco density-estimation pól (q=1) uniká v Θ(log(1/p_0))
- GARL při q=0.75 výrazně zmírňuje cold-start stalling a uniká tam, kde GRPO zcela selhává
- PAFT při q=0.75 poskytuje stabilní gradienty a dosahuje nejlepších výsledků na HotPotQA (47.9 maj@16, +14.4 oproti GRPO)

## Relevance for STOPA

Přístup k tréninku reasoning modelů s variabilním kompromisem mezi exploitací a explorací je relevantní pro orchestraci složitých reasoning úloh, kde je třeba balancovat mezi využitím existujících schopností a učením nových strategií.

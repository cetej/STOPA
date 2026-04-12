---
name: ASI-Evolve framework reference
description: ASI-Evolve (arXiv:2603.29640): autonomní AI výzkumný framework — learn→design→experiment→analyze smyčka s Cognition Base a Analyzer modulem
type: reference
---

# ASI-Evolve: AI Accelerates AI (arXiv:2603.29640)

Weixian Xu et al., 2026-03-31. Framework pro autonomní AI výzkum přes data, architektury, RL algoritmy.

## Klíčové komponenty

- **Researcher**: LLM generuje kandidáty (full-code nebo diff-based editing)
- **Engineer**: spouští experimenty, early rejection, timeouts
- **Analyzer**: transformuje logy/traces na kompaktní diagnostické reporty (NE skalární signál)
- **Cognition Base**: domain knowledge z literatury, semantic search retrieval, fast-start bez omezení explorace
- **Database**: persistence s UCB1/random/greedy/MAP-Elites sampling policies

## Výsledky

- 105 architektur překonalo DeltaNet; best +0.97 bodu (~3× lidský pokrok)
- Data curation: MMLU +18.64, CSQA +18.80 bodů
- RL: AMC32 +12.5, AIME24 +11.67 nad GRPO
- Drug-target: +6.94 AUROC cold-start generalization

## Task difficulty framework

L_task = ⟨C_exec, S_space, D_feedback⟩ — klasifikace obtížnosti výzkumných tasků:
- C_exec: výpočetní náklady a engineering komplexita per trial
- S_space: šíře prostoru hledání
- D_feedback: obtížnost extrakce insights z výsledků

## Ablace

- Bez Analyzeru: rychlý start (Cognition), pak plató — Analyzer kritický pro long-term evoluci
- Bez Cognition: pomalý cold-start, ale udržitelná evoluce přes self-guided trial-and-error

## Relevance pro STOPA

1. **Analyzer = upgrade pro failure pipeline**: structured diagnostics > skalární pass/fail; ovlivní failure-recorder.py
2. **UCB1 vs MAP-Elites**: sampling strategy pro optstate/ v autoloop/autoresearch
3. **L_task framework**: formalizace budget tierů (light/standard/deep/farm) přes C_exec × S_space × D_feedback

## Open source

https://github.com/open-lm-research/ASI-Evolve

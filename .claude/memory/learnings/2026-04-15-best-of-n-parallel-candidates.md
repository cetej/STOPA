---
date: 2026-04-15
type: architecture
severity: medium
component: orchestration
tags: [best-of-n, parallel-exploration, mcts, autoloop, autoresearch, test-time-scaling]
summary: "Best-of-N s PRM scoring: místo lineární iterace (zkus A, pokud fail zkus B) generuj 2-3 kandidáty paralelně, ohodnoť lightweight criticem, expand nejlepšího. Aplikovatelné na autoloop, autoresearch, deep-tier orchestrate."
source: external_research
uses: 4
successful_uses: 1
harmful_uses: 0
confidence: 1.0
maturity: draft
skill_scope: [autoloop, autoresearch, orchestrate]
related: [2026-04-15-parcae-exponential-decay-stopping.md, 2026-04-15-sd-zero-self-revision-supervision.md]
verify_check: "manual"
---

## Detail

arXiv:2501.09686 dokumentuje Best-of-N jako nejjednodušší test-time scaling metodu:

1. Generuj N nezávislých řešení/přístupů
2. Ohodnoť každé PRM/criticem (lightweight, ne full review)
3. Vyber nejlepší a expand/iteruj na něm

Výhody nad lineární iterací:
- **Explorační šíře** — pokrývá víc řešení v solution space
- **Paralelní** — N kandidátů běží současně (agent spawning)
- **Lepší starting point** — iteruješ na nejlepším kandidátu, ne na prvním

Survey ukazuje: Best-of-N + PRM scoring konzistentně překonává single-sample + iterativní opravy.

## Navrhovaná implementace

### Autoloop: Parallel candidates

Místo:
```
iter1: edit → score → edit → score → edit → score
```

Nově:
```
fork: [candidate_A, candidate_B, candidate_C] (parallel agents)
score: lightweight critic na každém
pick: nejlepší → iterate dál
```

### Autoresearch: Hypothesis branching

Místo lineárního testování hypotéz:
```
fork: [hypothesis_1, hypothesis_2] (parallel experiments)
eval: měřitelný výsledek každého
pick: nejlepší → deep-dive
```

### Orchestrate deep tier: Approach selection

Pro deep-tier úkoly kde existuje víc validních přístupů:
```
scout: identifikuj 2-3 přístupy
fork: [approach_A, approach_B] (parallel workers)
critic: lightweight eval na každém
merge: implementuj nejlepší, cituj proč
```

### Omezení

- Smysl dává jen pro N=2-3 (víc je příliš drahé pro Claude API)
- Vyžaduje task decomposability — musí jít rozdělit na nezávislé větve
- Light tier: nemá smysl (single-pass stačí)
- Overhead: N× agent cost za forking fázi

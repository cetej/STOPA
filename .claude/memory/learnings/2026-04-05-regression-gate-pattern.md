---
date: 2026-04-05
type: best_practice
severity: high
component: orchestration
tags: [eval, autoharness, self-evolve, regression, testing]
summary: "Regression gate pattern — fixed failures se stávají permanentními test cases, takže každé zlepšení je aditivní a bar jde jen nahoru. Bez gate optimalizuješ v kruhu."
source: external_research
confidence: 0.95
uses: 1
harmful_uses: 0
impact_score: 0.0
related: []
verify_check: "manual"
successful_uses: 0
---

# Regression Gate Pattern (NeoSigma auto-harness)

## Princip

Při iterativní optimalizaci agenta (autoloop, self-evolve, autoharness) nestačí měřit celkové skóre — potřebuješ **akkumulující regression suite**, kde každý vyřešený failure cluster přidá nový test case.

Bez regression gate: agent opraví A, ale rozbije B. Opraví B, rozbije A. Optimalizace v kruhu.
S regression gate: opravené A se stane permanentním testem. Příště musí projít A i B. Bar jde jen nahoru.

## Architektura

```
iteration N:
  1. Run benchmark → collect failures
  2. Cluster failures by root cause (ne symptom!)
  3. Propose fix for highest-impact cluster
  4. TWO-STEP GATE:
     a) regression suite (all previously fixed cases) must PASS
     b) overall val_score must not drop
  5. If both pass → accept fix, add cluster's test cases to regression suite
  6. If fail → reject, try different approach
```

## Jak adoptovat v STOPA

### /eval skill
- Aktuálně: replay traces, detekuj regresy, compare konfigurací
- Upgrade: zavést `workspace/suite.json` ekvivalent — akkumulující regression set
- Každý resolved failure cluster z /autoharness přidá eval case do suite

### /autoharness skill
- Aktuálně: generuje validátory z observed failure patterns (jednorázové)
- Upgrade: failure clustering by proposed fix (ne symptom), regression gate před acceptem

### /self-evolve skill
- Aktuálně: adversarial co-evolution loop
- Upgrade: regression suite roste s každou iterací, eval cases z minulých iterací se neodstraní

## Zdroj

NeoSigma auto-harness (https://github.com/neosigmaai/auto-harness)
- Tau3 benchmark: 0.56 → 0.78 (~40% jump)
- Klíčový insight: "Without the gate you're optimizing in a loop. With it, every improvement is additive."
- Další insight: clustering failures by proposed fix forces attack on underlying cause, prevents overfitting to individual cases

# Verifiability — Software 2.0 klíčový prediktor

**Type:** concept
**Tags:** ai, mental-model, software-development, automation
**Related:** [[rlvr]], [[jagged-intelligence]], [[karpathy]]
**Updated:** 2026-04-13

---

Karpathyho framework pro předpovídání co AI dokáže automatizovat: verifiability nahrazuje specifiability jako klíčový prediktor.

## Historická progrese

| Éra | Paradigma | Klíčový prediktor | Co to znamená |
|-----|-----------|-------------------|---------------|
| Software 1.0 | Explicitní kód | **Specifiability** | Lze-li přesně popsat pravidla → lze automatizovat |
| Software 2.0 | Neural networks | **Trainability** | Lze-li shromáždit labelled data → lze natrénovat |
| Software 3.0 (AI era) | LLMs + RLVR | **Verifiability** | Lze-li ověřit správnost → lze automatizovat (lépe) |

## Definice verifikovatelného úkolu

Úkol je verifikovatelný pokud splňuje 3 podmínky:
1. **Resettable**: lze vrátit do výchozího stavu pro opakované pokusy
2. **Efficient**: lze provést mnoho pokusů rychle
3. **Rewardable**: existuje automatizovatelná odměna (test pass/fail, math answer check)

## Příklady

**Verifikovatelné (rychlý pokrok, RLVR funguje):**
- Matematické důkazy
- Kód (unit testy, linting, kompilace)
- Puzzle-like úkoly (chess, go)
- Logické úsudky

**Neověřitelné (pomalejší pokrok):**
- Kreativní psaní (co je "dobré"?)
- Strategické rozhodování s dlouhým horizontem
- Common-sense uvažování
- Sociální interakce, empatie

## Proč to způsobuje Jagged Frontier

RLVR může trénovat pouze na verifikovatelných doménách.
→ Dramatický pokrok tam, kde existuje ověřitelná odměna
→ Stagnace (nebo pomalejší pokrok) jinde
→ Výsledek: LLM je geniální matematicky, ale může selhat na "strawberry"

## Praktická aplikace pro STOPA

Při návrhu agentic tasků: preferuj subtasky s jasnou verifikací (testy, grepping, syntaktická kontrola) před subtasky s fuzzy výstupem. Verifikovatelné subtasky → spolehlivější agent výkon.

Viz: `/verify`, `/harness`, `/tdd` skills — všechny pracují na principu verifikovatelnosti.

## Zdroj

Karpathy: "Verifiability" (Nov 2025) — https://karpathy.bearblog.dev/verifiability/

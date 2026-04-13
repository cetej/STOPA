# Jagged Intelligence (Ghosts vs Animals)

**Type:** concept
**Tags:** ai, mental-model, llm-behavior, benchmarks
**Related:** [[rlvr]], [[verifiability]], [[karpathy]]
**Updated:** 2026-04-13

---

LLMs vykazují "zubatý" (jagged) výkon — excelentní v jedné dimenzi, špatné v jiné. Toto není bug, ale přímý důsledek RLVR tréninku.

## Ghosts vs Animals (klíčová metafora)

Karpathy: LLMs **nejsou** "vyvíjející se zvířata". Jsou "přivolanými duchy" (summoned ghosts).

**Proč je metafora důležitá:**
- Špatný mentální model → špatné předpovědi o schopnostech
- Zvíře: homeostáza, sebezáchova, zkušenostní učení, sociální inteligence
- Duch: statistická simulace lidského textu, RL na distribucích úkolů

**Baby zebra counterexample** (z Animals vs Ghosts post):
- Zebra běží minuty po narození — ne tabula rasa, ale bohatá DNA inicializace evoluční "vnější smyčkou"
- Rich Sutton's "child machine" (tabula rasa learning) je proto nerealistická

## Jagged Frontier

LLMs jsou:
- Géniové v matematice, kódu, logice (ověřitelné domény, RLVR funguje)
- Zmatkovaní při počítání "r" ve slově "strawberry" (triviality bez verifikovatelné odměny)

Důvod: RLVR vytváří "spiky" právě v ověřitelných doménách.

## Benchmark problém

Benchmarky = ověřitelná prostředí → přirozeně citlivá na RLVR a syntetická data.

Karpathy: "Training on the test set is a new art form."

Praktický důsledek: benchmark výsledky jsou méně informativní o skutečných schopnostech než dříve.

## Space of Minds — optimalizační tlaky

| Dimenze | Zvíře | LLM |
|---------|-------|-----|
| Motivace | Self-preservation, reprodukce | Splnit úkol, sbírat odměny |
| Sociální | EQ, theory of mind, status | Sycophancy (A/B testované pro DAU) |
| Inteligence | Robustní, generalistická | Jagged, specializovaná |
| Učení | Zkušenostní, embodied | Text-based, disembodied |

Karpathy: "LLMs jsou prvním kontaktem lidstva s nezvířecí inteligencí. Jenže to je zamlžené, protože jsou stále zakořeněné v lidských artefaktech."

## Praktické implikace

1. Nečekej konzistentní výkon — testuj konkrétní use case
2. Nepoužívej benchmark výsledky jako proxy pro real-world schopnosti
3. Stavěj systémy předpokládající "spiked" výkon, ne uniformní
4. Verifikovatelné sub-úkoly → spolehlivější výsledky

## Zdroj

- Karpathy: "Animals vs Ghosts" (Oct 2025) — https://karpathy.bearblog.dev/animals-vs-ghosts/
- Karpathy: "The space of minds" (Nov 2025) — https://karpathy.bearblog.dev/the-space-of-minds/
- Karpathy: "2025 LLM Year in Review" (Dec 2025)

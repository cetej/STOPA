# RLVR — Reinforcement Learning from Verifiable Rewards

**Type:** concept
**Tags:** ai, training, reasoning, rl
**Related:** [[verifiability]], [[jagged-intelligence]], [[karpathy]]
**Updated:** 2026-04-13

---

RLVR je 4. fáze tréninku LLM (po Pretraining→SFT→RLHF), která trénuje model na automaticky ověřitelných odměnách z domén jako matematika nebo kód.

## Princip

Trénink na verifikovatelných odměnách způsobuje spontánní vznik "reasoning" strategií:
- Model se učí kontrolovat a opravovat vlastní výstup
- Vznikají delší "myšlenkové řetězce" bez explicitního trénování
- Test-time compute = nový knob: více přemýšlení = lepší výsledky

## Historický kontext

- o1 (OpenAI, 2024): první model s RLVR, ukázal reasoning emergence
- o3 (OpenAI, 2025): inflection point — dramatické zlepšení na složitých úlohách
- DeepSeek R1: open-source reprodukce s podobnými výsledky

## Klíčové důsledky

1. **Compute shift**: přesun compute od pretrainingu k delším RL runs
2. **Jagged frontier**: modely jsou geniální v matematice, ale mohou selhat na trivialitách
3. **Benchmark saturace**: benchmarky = ověřitelná prostředí → RLVR na ně přirozeně konverguje → "training on the test set is a new art form"

## Omezení

- Funguje primárně pro **verifikovatelné** domény
- Kreativní, strategické, common-sense úkoly nezlepšuje stejně efektivně
- Toto způsobuje fundamentálně jagged charakter výkonu LLM

## Zdroj

Karpathy: "2025 LLM Year in Review" (Dec 2025) — https://karpathy.bearblog.dev/year-in-review-2025/

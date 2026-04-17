# ThinkPRM — Process Reward Models That Think

**Source:** arXiv:2504.16828
**Added:** 2026-04-17

## Core Idea

Process Reward Models (PRM) hodnotí správnost jednotlivých reasoning kroků. Klasické discriminativní PRMs dělají binární klasifikaci bez reasoning — vyžadují velké množství procesních labelů (PRM800K).

ThinkPRM obrací přístup: místo klasifikace *generuje* chain-of-thought verifikaci při každém kroku. Long CoT model inherentně umí reasonovat — proč nevyužít tuto schopnost pro verifikaci?

## Metodologie

Generativní verifikátor: pro každý krok řešení model produkuje vlastní reasoning sekvenci hodnotící správnost kroku, teprve pak vydá verdikt.

- Potřebuje jen **1% procesních labelů** z PRM800K
- Neztrácí generalizaci na out-of-domain tasky
- Škáluje s délkou CoT (více reasoning = lepší verifikace)

## Výsledky

| Benchmark | ThinkPRM výhoda |
|-----------|----------------|
| ProcessBench, MATH-500, AIME '24 | Překonává discriminativní verifiery |
| GPQA-Diamond (OOD) | +8% |
| LiveCodeBench (OOD) | +4.5% |
| vs LLM-as-a-Judge | +7.2% při stejném token budgetu |

## Proč to funguje

Generativní verifikace aktivuje "slow thinking" — model se neptá "je tento krok správný?" ale "proč by tento krok mohl být špatný a jak to ověřím?". Tím se vyhne surface-level pattern matching a dosáhne hlubší verifikace.

## Significance pro STOPA

`/critic` v STOPA funguje jako LLM-as-a-Judge — ThinkPRM ukazuje, že přidání explicit CoT reasoning při hodnocení dává +7.2%. Implementovatelné jako "chain-of-thought critic" v `/critic` pro komplexní evaluace.

Obecnější princip: verifiery mají profitovat ze stejných CoT capabilities jako generators. **Generativní verifikace > discriminativní klasifikace** pro reasoning-intensive tasks.

## Connections

- Related: [[cpmi-process-reward]] — CPMI řeší labeling efektivitu PRMs, ThinkPRM řeší verifikaci quality; komplementární přístupy
- Related: [[rational-rewards]] — PARROT strukturovaná kritika ↔ ThinkPRM CoT verifikace: obojí přidává reasoning vrstvu nad skalární reward
- Enables: [[rlvr]] — lepší step-level verifikace = lepší reward signal pro RLVR trénování
- Applied-in: [[stopa]] — /critic = LLM-as-a-Judge, ThinkPRM ukazuje CoT verifikace dává +7.2%

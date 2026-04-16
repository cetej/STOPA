# CPMI — Contrastive Process Reward Modeling

**Source:** arXiv:2604.10660 (ACL 2026)
**Added:** 2026-04-16

## Core Idea

Process Reward Models (PRM) hodnotí správnost jednotlivých reasoning kroků v chain-of-thought — nikoli jen finální odpověď. Trénovat je bylo drahé: buď ruční anotace, nebo Monte Carlo rollouts z každého intermediate stavu (spustit model stokrát z každého kroku a odhadnout pravděpodobnost úspěchu).

CPMI (Contrastive Pointwise Mutual Information) tento bottleneck odstraňuje. Místo rolloutů používá model vlastní interní distribuce pravděpodobností a kvantifikuje: _"O kolik tento krok zvyšuje mutual information mezi sekvencí a správnou odpovědí — oproti hard-negative alternativám?"_

## Metodologie

Klasická PMI: `PMI(step; answer) = log P(step, answer) / (P(step) × P(answer))`

Kontrastní rozšíření: místo absolutní hodnoty se porovnává vůči nesprávným alternativám (hard negatives). Reward = relativní PMI signal, nikoli absolutní.

- Interní pravděpodobnostní distribuce modelu nahrazují MC rollouts
- Žádné lidské anotace
- Žádné doplňkové generování tokenů pro estimaci

## Výsledky

| Metrika | CPMI vs Monte Carlo |
|---------|---------------------|
| Čas na dataset construction | −84% |
| Počet generovaných tokenů | −98% |
| Přesnost (math reasoning benchmarks) | Vyšší nebo srovnatelná |

## Proč to funguje

Hard-negative kontrast je klíčový: PMI samo o sobě by mohlo ocenit i irelevantní kroky, pokud korelují s odpovědí. Kontrast vůči špatným alternativám vytváří signál blízký "kauzálnímu příspěvku kroku" — bez potřeby simulovat alternativní trajektorie.

## Significance pro STOPA

PRMs jsou základ pro step-level reward v `/autoreason`, `/critic`, a `/autoloop`. CPMI ukazuje, že reward labeling lze provést bez additional rollouts — jde o efektivnější verzi toho, co `/critic` dělá heuristicky: hodnotit kvalitu intermediate kroků.

## Connections

- Related: [[reinforced-reasoning]] — PRM step-level scoring je jedna z metod popsaných v arXiv:2501.09686; CPMI řeší jejich training bottleneck
- Related: [[rational-rewards]] — PARROT (structured critique) vs CPMI (contrastive PMI): obojí překonává skalární reward signály
- Related: [[memfactory]] — RL-based training framework, CPMI poskytuje efektivnější step-level labely pro RL
- Enables: efektivnější trénování critic modelů v STOPA (levnější PRM = dostupnější step-level feedback)

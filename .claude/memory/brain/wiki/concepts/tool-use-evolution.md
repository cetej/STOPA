# Tool Use Evolution — Od Single Tool k Multi-Tool Orchestration

**Source:** arXiv:2603.22862 (survey paper, 14 autorů)
**Added:** 2026-04-17

## Core Idea

Survey zachycuje fundamentální posun: výzkum se přesunul od "umí model správně vybrat a zavolat jeden nástroj" k "jak řídit komplexní multi-tool sekvence přes rozšířené trajektorie s průběžnou zpětnou vazbou a měnícími se podmínkami."

## 6 Dimenzí Multi-Tool Orchestration

| Dimenze | Co řeší |
|---------|---------|
| **Inference-time planning** | Jak agenti plánují sekvence toolů před exekucí |
| **Training approaches** | Jak trénovat agenty na multi-tool tasky |
| **Safety mechanisms** | Jak zajistit bezpečnost v dlouhých tool sekvencích |
| **Resource efficiency** | Jak minimalizovat zbytečná tool volání |
| **Capability completeness** | Co současné systémy umí vs čeho jim chybí |
| **Evaluation benchmarks** | Jak měřit výkon v multi-tool scénářích |

## Klíčové Trendy

**Long-horizon planning**: úkoly přes desítky tool volání, s intermediate feedback loops a dynamickými podmínkami.

**Integrated solutions required**: Reliability + scalability + verifiability musí být řešeny jako systém, ne izolovaně. Izolovaná tool invocation nestačí.

**Aplikační domény**: software engineering, enterprise workflows, graphical interfaces, mobile systems.

## Výzvy (z ablation studií v surveyi)

- Sekvence toolů jsou fragile: error early → cascade failures
- Tool selection accuracy klesá s délkou plánování
- Safety: dlouhé trajektorie = více surface pro injection/manipulation
- Evaluation: benchmarky pro single tool zastarávají

## Significance pro STOPA

Survey externally validuje STOPA architektonická rozhodnutí:

- **Circuit breakers** (3-fix escalation) → řeší cascade failures v long sequences
- **/verify + /harness** → verifiability v orchestraci
- **Budget tiers** → resource efficiency (kolik agentů, jak hluboké plánování)
- **Safety: constrained-tools** → explicit tool safety boundaries

Klíčový insight: přechod single→multi tool odpovídá přechodu light→deep tier v STOPA. Komplexita orchestrace není linear — je to phase transition.

## Connections

- Validates: [[stopa]] — circuit breakers, budget tiers, /verify, constrained-tools řeší přesně 6 dimenzí surveye
- Related-to: [[context-engineering]] — multi-tool trajectory management = context engineering challenge (tool results musí být v kontextu správně)
- Related-to: [[multi-agent-hpc]] — HPC paper implementuje multi-tool orchestration at physical computation scale

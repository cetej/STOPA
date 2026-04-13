# Active Metacognitive Curation

**Type:** concept
**Tags:** ai, memory, architecture, cognitive-science
**Related:** [[ecphory-rag]], [[second-brain]], [[cognitive-workspace]]
**Source:** arXiv:2508.13171 (Cognitive Workspace, 2025)

---

Paradigma aktivního memory managementu — systém sám rozhoduje co udržovat, promovat a zahazovat. Opak pasivního RAG (query → retrieve).

## Proč pasivní RAG nestačí

Pasivní RAG operuje: dotaz přijde → prohledej → vrať výsledky. Žádná metacognitivní vrstva nerozhoduje:
- Co by mělo zůstat v "hot" paměti?
- Co je zastaralé a mělo by se archivovat?
- Co si kontradikuje a vyžaduje rezoluci?
- Co je relevantní pro právě probíhající úkol (ne jen pro dotaz)?

## Kognitivní základ

Grounded v Baddeleyho 4-komponentním modelu pracovní paměti:
1. **Centrální exekutiva** — řídí pozornost a koordinaci (= orchestrator)
2. **Fonologická smyčka** — krátkodobá verbální paměť (= context window)
3. **Vizuálně-prostorový náčrtník** — prostorové zpracování (= diagram/graph views)
4. **Epizodický buffer** — integrace informací z různých zdrojů (= synthesis step)

+ Clarkova teze rozšířené mysli: externě uložená znalost JE součástí kognitivního systému.

## Metriky

- 58.6% memory reuse vs 0% pasivní RAG
- 17-18% net efficiency gain (p << 0.001, Cohen's d >> 23)
- Trade-off: 3.3× vyšší počet operací (acceptable v async systému)

## Implementace v 2BRAIN

STOPA hooks = metacognitivní vrstva:
- `learning-admission.py` — rozhoduje co přijmout (= gate)
- `verify-sweep.py` — audituje staré znalosti (= pruning)
- `outcome-credit.py` — trackuje impact (= evaluation)
- Chybí: brain-curation.py — automatická detekce kontradikcí a stale článků ve wiki/

## Konvergentní vzor

Společný nález všech 4 akademických paperů: entity-centric storage + cue-driven multi-hop retrieval + **active metacognitive curation** = SOTA. Žádná z komponent sama nestačí.

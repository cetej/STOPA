# Paměťové systémy pro AI agenty — Research Brief

**Datum:** 2026-04-11
**Otázka:** Co skutečně dělá AI agent memory systémy užitečnými vs. jen existujícími?
**Scale:** survey
**Zdrojů konzultováno:** 12 přečteno, 40+ discovery

## Executive Summary

Tři klíčové zjištění z výzkumu:

1. **Retrieval kvalita dominuje nad storage sofistikovaností.** MemMachine ablation studie ukazuje +9.4% z optimalizace retrieval vs +0.8% z lepšího ukládání [VERIFIED][4]. STOPA investuje hodně do struktury learnings YAML — ale víc by pomohlo zlepšit hybrid-retrieve.py.

2. **Offline konsolidace ("dreams") je empiricky validovaná.** Reflexion zvyšuje HumanEval z 80% na 91% [VERIFIED][1]. Generative Agents bez reflection degenerují za 48h [VERIFIED][1]. OpenClaw implementuje dream cyklus: collect → consolidate → evaluate, s Smart Skip optimalizací (90% token úspora při idle) [VERIFIED][3].

3. **Kvalita >> Kvantita — curated memory beats add-all.** Fine-tuned evaluátor na 300 příkladech dramaticky překonává vanilla LLM soudce pro memory admission [VERIFIED][5]. History-based deletion (nízký průměrný utility) funguje lépe než periodická údržba [VERIFIED][5].

## Detailed Findings

### A. Proč keyword/grep retrieval selhává

ACT-R kognitivní architektura definuje retrieval jako activation competition, ne lookup. Aktivace kombinuje 3 nezávislé signály [INFERRED][5,6]:

| Signál | ACT-R termín | STOPA ekvivalent | Status |
|--------|-------------|-----------------|--------|
| Recence/frekvence | Base-level learning | time-weighted relevance, `uses:` | Implementováno |
| Sémantická relevance | Spreading activation | concept-graph 1-hop, hybrid-retrieve | Částečně |
| Důležitost/salientnost | Partial matching + utility | `impact_score`, `harmful_uses` | Implementováno |

Keyword search zachycuje NULA z těchto signálů. Embedding search zachycuje jeden (sémantiku). Teprve tří-signálová fúze funguje spolehlivě [INFERRED][5,6].

ByteRover ukazuje alternativu: hierarchický Context Tree (Domain > Topic > Subtopic > Entry) řeší většinu dotazů pod 100ms BEZ embedding calls — strukturální pre-filtering před sémantickým matchingem [VERIFIED][5].

### B. Konsolidace a dreams

**Dual-buffer pattern** (validováno napříč systémy): nové paměti vstupují do probačního bufferu, promovány do long-term až po re-verifikaci, deduplikaci a importance scoringu [VERIFIED][1].

**OpenClaw dream cycle** [VERIFIED][3]:
1. **Collect**: scan 7d logů, detekce priority markerů
2. **Consolidate**: routing do memory vrstev, deduplikace, linkování
3. **Evaluate**: scoring, forgetting curves, health metriky
4. Smart Skip: pokud žádné nové nekonsolidované logy → exit (~2K tokenů místo ~150K)

**Triggery konsolidace:**
- Pre-compaction flush (před summarizací kontextu)
- Scheduled offline (cron "dreams", default 4 AM)
- Event-driven (po dokončení tasku)

**Hoarding vs amnesia** [VERIFIED][1]: safety-critical instrukce mohou zmizet po 3 summarizačních cyklech. Řešení: dual-buffer s explicit protection pro safety rules.

### C. Architektury s měřitelnými výsledky

| Systém | Mechanismus | LoCoMo výsledek | Token efektivita | Klíčový insight |
|--------|------------|----------------|-----------------|-----------------|
| MemoryOS | 3-tier FIFO + segmented pages | +49% F1 | — | Tier konsolidace filtruje šum |
| A-MEM | Zettelkasten + backward-updating | "superior to SOTA" | 92% redukce | Staré paměti se aktualizují při nových |
| Mem0 | Graph-enhanced extraction | +26% Judge | 90% úspora | Extraction je bottleneck |
| MemMachine | Ground-truth preservation | 0.917 accuracy | 80% méně než Mem0 | Retrieval >> ingestion |

### D. Co STOPA už dělá dobře

- Graduation pattern (learnings → critical-patterns) = MemoryOS tier consolidation ✓
- Time-weighted relevance = ACT-R base-level learning ✓
- Admission control (learning-admission hook) = dual-buffer quality gate ✓
- Archive-not-delete = OpenClaw archival policy ✓
- Reflexion notes (core-invariant #7) ✓
- Hybrid retrieval s RRF (multi-signal fusion) ✓

### E. Gapy v STOPA — co chybí

1. **Offline dream konsolidace** — žádná proaktivní cross-session detekce vzorů
2. **Backward-updating** — nový learning neaktualizuje kontext starých related learnings
3. **Strukturální pre-filtering** — flat grep, ne hierarchický tree
4. **Utility-based archivace** — trackuje uses, ale nearchivuje systematicky low-utility
5. **Měření downstream dopadu** — MemoryArena ukazuje, že recall ≠ decision quality

## Doporučení pro implementaci

### Priorita 1: Dreams scheduled task
- Cron: 1x denně (nebo po N sessions)
- Collect: scan learnings/, outcomes/, checkpoint.md
- Consolidate: cross-link related learnings, backward-update contexts
- Evaluate: archive low-utility, promote high-impact
- Smart Skip: pokud žádné nové outcomes → exit early

### Priorita 2: Retrieval improvement
- Strukturální pre-filtering přes concept-graph.json PŘED grep
- Query routing: simple → grep, complex → hybrid, novel → LLM reasoning

### Priorita 3: Měření
- Track "memory helped" vs "memory irrelevant" na per-task basis
- MemoryArena-style: měř decision quality, ne recall accuracy

## Sources

1. Memory for Autonomous LLM Agents: survey — https://arxiv.org/html/2603.07670v1
2. MemoryOS (EMNLP 2025 Oral) — https://arxiv.org/abs/2506.06326
3. OpenClaw Memory docs + openclaw-auto-dream — https://docs.openclaw.ai/concepts/memory / https://github.com/LeoYeAI/openclaw-auto-dream
4. MemMachine — https://arxiv.org/abs/2604.04853
5. How Memory Management Impacts LLM Agents — https://arxiv.org/html/2505.16067v2
6. ACM: Memory Mechanism of LLM-based Agents — https://dl.acm.org/doi/10.1145/3748302
7. A-MEM (NeurIPS 2025) — https://arxiv.org/abs/2502.12110
8. Mem0 — https://arxiv.org/abs/2504.19413
9. From Human Memory to AI Memory: survey — https://arxiv.org/html/2504.15965v2
10. LangChain LangMem — https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
11. ByteRover — https://arxiv.org/abs/2604.01599
12. ACT-R cognitive architecture (Anderson et al.)

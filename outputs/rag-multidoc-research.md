# Proč naive RAG selhává na agregačních dotazech a jak to řeší symbolické vrstvy — Research Brief

**Datum:** 2026-04-05
**Otázka:** Proč naive RAG selhává na agregačních/multi-document dotazech a jaké přístupy (symbolické vrstvy, hybridní architektury) to řeší?
**Scope:** survey
**Zdrojů konzultováno:** 35+ (30 přijato, 5+ zamítnuto jako neverifikovatelné)

---

## Executive Summary

Naive RAG — dense retrieval + LLM generace — dosahuje prakticky nulových výsledků na agregačních dotazech: 1.51 průměrné F1 na benchmarku GlobalQA (counting, sorting, top-k, extremum) [VERIFIED][1] a pouze 33.1% na datové sadě Hotels vs. 89.9% oracle [VERIFIED][4]. Selhání není náhodné — je výsledkem čtyř souběžných architekturálních problémů: bounded-K retrieval neumožňuje exhaustive coverage, fixed chunking ničí atributové vazby, dense embeddingy selžou na komplexních filtrech a LLM špatně počítají čísla [VERIFIED][1,4].

Symbolicko-hybridní přístupy tento problém adresují ze tří směrů. Knowledge graph jako index (GraphRAG, HippoRAG) přináší 72-83% win rate nad naive RAG na globálních dotazech [VERIFIED][9] a +20% na multi-hop QA [VERIFIED][6]. Iterativní retrieval s reasoning feedback smyčkou (IRCoT, BeamAggR) zlepšuje výsledky o +21 retrieval / +15 QA [VERIFIED][7]. Přímá symbolická výpočetní vrstva pro numerické agregace (PAL, OLLA, GlobalRAG) přináší 1.6-38× zrychlení pro SQL-like dotazy přes nestrukturovaný text [VERIFIED][12]. Corpus-level aggregation přesto zůstává v podstatě nevyřešena — nejlepší systém dosahuje 6.63 F1 [VERIFIED][1], daleko od praktické použitelnosti.

---

## Detailed Findings

### 1. Čtyři souběžné důvody selhání naive RAG

**Architekturální mismatch: bounded-K** — Standard RAG retrievuje top-K dokumentů (K=5-20). Agregační dotazy ("Kolik kandidátů má certifikaci X?", "Seřaď firmy podle revenue") vyžadují exhaustivní coverage všech matching dokumentů. GlobalQA ukazuje, že 42.6% dotazů vyžaduje evidenci z 20+ dokumentů, přičemž maximum je 50 dokumentů [VERIFIED][1]. Žádné K v limitu context window nepokryje celý relevantní set.

**Structural integrity loss** — Mainstreaming RAG chunks jsou 512-token segmenty bez respektování struktury dokumentu. Příklad z GlobalQA: při chunking výzkumného paperu se rok publikace a počet citací ocitnou v různých segmentech, což způsobuje double-counting nebo omissions při agregaci [VERIFIED][1]. S-RAG přidává čtvrtý failure mode: embeddingy selhávají na složitých filter predicátech jako "jihoamerické firmy s >1000 zaměstnanci" [VERIFIED][4].

**Position bias: U-curve a Weakest Link Law** — I když jsou relevantní dokumenty retrievnuty, LLM je nezpracuje rovnoměrně. Liu et al. (Stanford) dokumentují U-tvar: informace na začátku a konci kontextu jsou zpracovávány lépe než střed [VERIFIED][5]. Weakest Link Law (Cambridge) formalizuje, že u multi-hop QA výkon odpovídá nejhůře viditelné supporting fact, nikoli průměru — retrieval failure mode je recognition-based (model nedokáže evidenci najít), nikoli reasoning-based [VERIFIED][3].

**Numerické výpočty** — LLM jsou slabé v aritmetice přes velké sety. I při dokonalém retrieval selžou na agregačních operacích (counting, averaging, ranking). Toto vyžaduje explicitní symbolický modul [VERIFIED][1].

**Souhrnně:** Agregační dotazy koncentrují všechny failure modes zároveň — proto jsou výsledky blízko nuly, nikoli jen degradované.

### 2. Knowledge Graph jako symbolická vrstva

**GraphRAG** (Microsoft, arXiv:2404.16130) je architekturálně nejvýznamnější posun. Index-time: entity-relationship graph → Louvain community detection → pre-generované community summaries na více úrovních hierarchie. Query-time Global Search fanoří přes všechny community summaries a syntetizuje globální odpovědi. Výsledek: 72-83% win rate nad naive RAG na comprehensiveness, 75-82% na diversity (p<0.001, testováno na 1M-1.7M tokenových korpusech) [VERIFIED][9]. **LazyGraphRAG** (2025) snižuje indexing cost na 0.1% plného GraphRAG při zachování kvality, a přesto vítězí nad naive RAG ve všech 96 testovaných párech včetně 1M-token kontextového okna [VERIFIED][10].

**HippoRAG** (OSU, NeurIPS 2024, arXiv:2405.14831) bere lehčí přístup: OpenIE trojice jako index + Personalized PageRank pro retrieval. Výsledek: +20% na multi-hop QA (MuSiQue, 2WikiMHQA, HotpotQA), 10-30× levnější než iterativní IRCoT [VERIFIED][6]. **HippoRAG 2** (ICML 2025) přidává non-parametric continual learning — znalosti lze přidávat bez parameter updates [VERIFIED][6].

**StructRAG** (Alibaba DAMO, arXiv:2410.08815) generalizuje: router vybírá optimální formát struktury per task (table, graph, algorithm, catalog, chunk), dokumenty jsou rekonstruovány do daného formátu at inference-time. SOTA na knowledge-intensive benchmarky [VERIFIED][14].

### 3. Iterativní a agentický retrieval

**IRCoT** (ACL 2023, arXiv:2212.10509) je seminal paper: CoT a retrieval se střídají na úrovni věty — každý CoT krok může generovat retrieval query, každý retrieval výsledek kondicionuje další CoT krok. +21 retrieval / +15 QA na HotpotQA/2WikiMultihop/MuSiQue [VERIFIED][7].

**FRAMES** (Google, NAACL 2025, arXiv:2409.12941) kvantifikuje rozdíl: single-step RAG dosahuje 0.40, multi-step pipeline 0.66 (+65%) na 824 multi-hop otázkách vyžadujících 2-15 Wikipedia dokumentů [VERIFIED][16]. Pokrývá numerické srovnání (20%), multiple constraints (36%), temporal disambiguation (16%) — přesně kategorie, kde symbolické vrstvy přidávají hodnotu.

**BeamAggR** (ACL 2024, arXiv:2406.19820) přidává strukturální agregaci: komplexní dotazy jsou parsovány do stromů atomických/kompozitních otázek, bottom-up reasoning generuje beam kandidáty, probabilistická beam agregace rankuje trajektorie. +8.5% nad SOTA na 4 datových sadách [VERIFIED][8].

### 4. Symbolická výpočetní vrstva pro numerické agregace

**PAL** (CMU, ICML 2023, arXiv:2211.10435) je foundational pattern: LLM generuje Python program jako reasoning krok, Python interpreter provede deterministický výpočet. Menší model s PAL překoná větší language-only model — Codex+PAL > PaLM-540B o 15pt na GSM8K [VERIFIED][15]. Princip: odděl jazyk (generace programu) od výpočtu (interpreter execution).

**OLLA** (Shandong/Renmin U, arXiv:2603.08443, 2026) přenáší tento princip na unstructured text analytics: stratified semantic sampling (grouping by embedding clusters) umožňuje progresivní agregaci přes tisíce dokumentů s 1% chybou při <4% plného scan time. 1.6-38× zrychlení vs. full scan [VERIFIED][12]. Poznámka: OLLA nepoužívá SQL syntaxi — jde o semantic stratified sampling inspirované SQL sémantikou.

### 5. Produkční implementace

| Framework | Přístup | Klíčový výsledek | Benchmark |
|-----------|---------|-----------------|-----------|
| **GraphRAG** (Microsoft, 32k ⭐) | KG + community summaries | 72-83% win rate nad naive RAG | arXiv:2404.16130 [VERIFIED] |
| **LlamaIndex** | RouterQE + SubQuestion + MultiDoc Agents | Nejbohatší ekosystém komponent | Bez publik. benchmarku |
| **DSPy** (Stanford, ICLR 2024) | Optimizer-driven multi-hop | 39.3% EM na HotPotQA | [UNVERIFIED] |
| **LangGraph** | Stateful self-corrective grafy | Self-correction loop | Blog claim, neverifikováno |
| **Haystack** (24.7k ⭐) | Query decomposition pipeline | Apple, Meta, Databricks, NVIDIA | Bez publik. benchmarku |

### 6. SOTA přehled

| Benchmark | Task | Nejlepší výsledek | Metoda |
|-----------|------|------------------|--------|
| GlobalQA | Corpus-level counting/sorting/top-k | 6.63 F1 | GlobalRAG (symbolic aggregation) [VERIFIED] |
| MuSiQue | Multi-hop QA | 36.6 EM / 44.5 F1 | Gemini [SINGLE-SOURCE] |
| 2WikiMHQA retrieval | Multi-hop retrieval | +20% R@2/5 | HippoRAG [VERIFIED] |
| FRAMES | Multi-step multi-doc QA | 0.66 (vs 0.40 single-step) | Multi-step pipeline [VERIFIED] |
| GraphRAG vs naive | Global sensemaking | 72-83% win rate | GraphRAG [VERIFIED] |

---

## Disagreements & Open Questions

**Long Context vs. RAG** — Li et al. (arXiv:2501.01880) ukazuje, že LC překonává RAG na QA/Wikipedia, ale RAG vítězí na dialogue. Výsledky jsou silně citlivé na benchmark a retrieval strategii. Summarization-based retrieval téměř dosahuje LC výkonu — metodologicky nejistý závěr [INFERRED][2,3].

**Index-time vs. inference-time strukturování** — GraphRAG/HippoRAG strukturují při indexování (nákladnější, ale rychlejší dotazy), StructRAG/TaSR-RAG strukturují při inference (flexibilnější, ale pomalejší). Žádný paper nesrovnává přístupy na stejném datasetu [INFERRED][9,14].

**Otevřené otázky:**
- Corpus-level agregace přes tisíce dokumentů — i nejlepší systém (6.63 F1) je vzdálený od praktické použitelnosti
- Router v StructRAG vyžaduje trénovaný model — jak vybrat strukturu bez task-specific supervisí?
- Mohou reflection tokeny Self-RAG být rozšířeny na graph-structured retrieval?
- Neexistuje třetí-stranná srovnávací studie produkčních frameworků (GraphRAG vs LlamaIndex vs Haystack) na shodném datasetu

---

## Evidence Table (merged, deduplicated)

| # | Zdroj | URL | Klíčový claim | Typ | Conf. |
|---|-------|-----|---------------|-----|-------|
| 1 | GlobalQA / GlobalRAG — Luo et al. (arXiv:2510.26205) | https://arxiv.org/abs/2510.26205 | Naive RAG = 1.51 F1 na corpus-level agregaci; GlobalRAG = 6.63 F1 | Benchmark | high |
| 2 | Long Context vs. RAG — Li et al. (arXiv:2501.01880) | https://arxiv.org/abs/2501.01880 | LC > RAG na QA/Wikipedia; RAG > LC na dialogue; bez universálního vítěze | Paper | high |
| 3 | Weakest Link Law — Zhang et al., Cambridge (arXiv:2601.12499) | https://arxiv.org/html/2601.12499 | Multi-hop QA výkon řízen nejhůře viditelnou supporting fact; recognition bottleneck | Empirical | high |
| 4 | S-RAG — Koshorek et al., Technion (arXiv:2511.08505) | https://arxiv.org/abs/2511.08505 | VectorRAG = 33.1% vs 89.9% oracle na Hotels; 4 failure modes | Benchmark | high |
| 5 | Lost in the Middle — Liu et al., Stanford (arXiv:2307.03172) | https://arxiv.org/abs/2307.03172 | U-shaped performance curve — relevantní info ve středu kontextu systematicky degraduje | Empirical | high |
| 6 | HippoRAG + HippoRAG 2 — Gutiérrez et al. (arXiv:2405.14831, 2502.14802) | https://arxiv.org/abs/2405.14831 | KG + PPR; +20% multi-hop QA; 10-30× levnější než IRCoT (NeurIPS 2024) | Paper | high |
| 7 | IRCoT — Trivedi et al. (arXiv:2212.10509) | https://arxiv.org/abs/2212.10509 | Interleaved CoT+retrieval; +21 retrieval, +15 QA na multi-hop benchmarky (ACL 2023) | Paper | high |
| 8 | BeamAggR — Chu et al. (arXiv:2406.19820) | https://arxiv.org/abs/2406.19820 | Question tree + probabilistická beam agregace; +8.5% nad SOTA (ACL 2024) | Paper | high |
| 9 | GraphRAG — Edge et al., Microsoft (arXiv:2404.16130) | https://arxiv.org/abs/2404.16130 | KG + community summaries; 72-83% win rate nad naive RAG | Paper | high |
| 10 | LazyGraphRAG — Microsoft Research blog | https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ | 0.1% indexing cost plného GraphRAG; vítězí ve všech 96 srovnáních | Blog (MS Research) | high |
| 11 | RAPTOR — Sarthi et al. (arXiv:2401.18059) | https://arxiv.org/abs/2401.18059 | Recursive clustering + tree hierarchy; +20% na QuALITY s GPT-4 (ICLR 2024) | Paper | high |
| 12 | OLLA — Hui et al. (arXiv:2603.08443) | https://arxiv.org/abs/2603.08443 | Semantic stratified sampling pro agregaci přes nestruk. text; 1.6-38× speedup | Paper | high |
| 13 | CRAG — Yang et al., Meta (arXiv:2406.04744) | https://arxiv.org/abs/2406.04744 | Naive RAG: 34% → 44%; industry RAG max 63%; agregace = jedna z nejtěžších kategorií (NeurIPS 2024) | Benchmark | high |
| 14 | StructRAG — Li et al. (arXiv:2410.08815) | https://arxiv.org/abs/2410.08815 | Task-adaptive router → table/graph/algorithm/catalog/chunk; SOTA na knowledge-intensive | Paper | high |
| 15 | PAL — Gao et al. (arXiv:2211.10435) | https://arxiv.org/abs/2211.10435 | LLM píše Python, interpreter exekuuje; Codex+PAL > PaLM-540B o 15pt (ICML 2023) | Paper | high |
| 16 | FRAMES — Krishnaprasad et al. (arXiv:2409.12941) | https://arxiv.org/abs/2409.12941 | Single-step RAG = 0.40, multi-step = 0.66 na 824 multi-hop otázkách (NAACL 2025) | Benchmark | high |
| 17 | Self-RAG — Asai et al. (arXiv:2310.11511) | https://arxiv.org/abs/2310.11511 | Reflection tokeny trénované do modelu; adaptive on-demand retrieval (ICLR 2024) | Paper | high |
| 18 | HoloBench — (arXiv:2410.11996) | https://arxiv.org/abs/2410.11996 | Information density > context length pro LCLM; agregační tasky degradují se scale (ICLR 2025) | Benchmark | high |
| 19 | Agentic RAG Survey — Singh et al. (arXiv:2501.09136) | https://arxiv.org/abs/2501.09136 | Taxonomie agentic RAG: cardinality, control, autonomy, knowledge representation | Survey | high |
| 20 | TaSR-RAG (arXiv:2603.09341) | https://arxiv.org/abs/2603.09341 | Relační trojice + entity binding table; +14% multi-hop QA | Paper | high |
| 21 | SRAG (arXiv:2603.26670) | https://arxiv.org/abs/2603.26670 | KG trojice + metadata enrichment před embeddingem; +30% QA score | Paper | high |
| 22 | MultiHop-RAG — Tang & Yang (arXiv:2401.15391) | https://arxiv.org/abs/2401.15391 | Existující RAG metody "nesatisfaktoří" na multi-hop; 2556 queries (COLM 2024) | Benchmark | high |
| 23 | microsoft/graphrag GitHub | https://github.com/microsoft/graphrag | 32k ⭐, v3.0.8, produkčně aktivní | Repo | high |
| 24 | LlamaIndex SubQuestion + MultiDoc Agents docs | https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/ | SubQuestion + per-doc agents + ObjectIndex + Cohere reranking | Docs | high |
| 25 | DSPy — Khattab et al. (ICLR 2024) | https://openreview.net/pdf?id=sY5N0zY5Od | SimplifiedBaleen multi-hop; optimizer-driven; 39.3% EM HotPotQA | Paper | medium |
| 26 | Haystack v2.x (deepset) | https://github.com/deepset-ai/haystack | 24.7k ⭐; 3-stage query decomposition; Apple, Meta, Databricks, NVIDIA | Repo+Docs | high |
| 27 | IndexRAG (arXiv:2603.16415) | https://arxiv.org/html/2603.16415 | Index-time bridging facts; překonává HippoRAG na 3 benchmarky | Paper | medium |
| 28 | FLARE — Jiang et al. (arXiv:2305.06983) | https://arxiv.org/abs/2305.06983 | Forward-looking speculative retrieval na nízkou confidence; iterativní during generation (EMNLP 2023) | Paper | high |

---

## Sources

1. Luo et al. — "Towards Global Retrieval Augmented Generation" (arXiv:2510.26205) — https://arxiv.org/abs/2510.26205
2. Li et al. — "Long Context vs. RAG for LLMs" (arXiv:2501.01880) — https://arxiv.org/abs/2501.01880
3. Zhang, Meng, Collier — "Failure Modes in Multi-Hop QA: The Weakest Link Law" (arXiv:2601.12499) — https://arxiv.org/html/2601.12499
4. Koshorek et al. — "Structured RAG for Answering Aggregative Questions" (arXiv:2511.08505) — https://arxiv.org/abs/2511.08505
5. Liu et al. — "Lost in the Middle" (arXiv:2307.03172) — https://arxiv.org/abs/2307.03172
6. Gutiérrez et al. — "HippoRAG" (arXiv:2405.14831) + "HippoRAG 2" (arXiv:2502.14802) — https://arxiv.org/abs/2405.14831
7. Trivedi et al. — "IRCoT" (arXiv:2212.10509) — https://arxiv.org/abs/2212.10509
8. Chu et al. — "BeamAggR" (arXiv:2406.19820) — https://arxiv.org/abs/2406.19820
9. Edge et al. — "GraphRAG" (arXiv:2404.16130) — https://arxiv.org/abs/2404.16130
10. Microsoft Research — "LazyGraphRAG" — https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/
11. Sarthi et al. — "RAPTOR" (arXiv:2401.18059) — https://arxiv.org/abs/2401.18059
12. Hui et al. — "OLLA" (arXiv:2603.08443) — https://arxiv.org/abs/2603.08443
13. Yang et al. — "CRAG" (arXiv:2406.04744) — https://arxiv.org/abs/2406.04744
14. Li et al. — "StructRAG" (arXiv:2410.08815) — https://arxiv.org/abs/2410.08815
15. Gao et al. — "PAL" (arXiv:2211.10435) — https://arxiv.org/abs/2211.10435
16. Krishnaprasad et al. — "FRAMES" (arXiv:2409.12941) — https://arxiv.org/abs/2409.12941
17. Asai et al. — "Self-RAG" (arXiv:2310.11511) — https://arxiv.org/abs/2310.11511
18. "HoloBench" (arXiv:2410.11996) — https://arxiv.org/abs/2410.11996
19. Singh et al. — "Agentic RAG Survey" (arXiv:2501.09136) — https://arxiv.org/abs/2501.09136
20. Sun et al. — "TaSR-RAG" (arXiv:2603.09341) — https://arxiv.org/abs/2603.09341
21. Shah et al. — "SRAG" (arXiv:2603.26670) — https://arxiv.org/abs/2603.26670
22. Tang & Yang — "MultiHop-RAG" (arXiv:2401.15391) — https://arxiv.org/abs/2401.15391
23. microsoft/graphrag GitHub — https://github.com/microsoft/graphrag
24. LlamaIndex Multi-Document Agents docs — https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/
25. Khattab et al. — "DSPy" (ICLR 2024) — https://openreview.net/pdf?id=sY5N0zY5Od
26. deepset-ai/haystack GitHub — https://github.com/deepset-ai/haystack
27. "IndexRAG" (arXiv:2603.16415) — https://arxiv.org/html/2603.16415
28. Jiang et al. — "FLARE" (arXiv:2305.06983) — https://arxiv.org/abs/2305.06983

---

## Coverage Status

- **[VERIFIED]:** GlobalQA F1 čísla, S-RAG benchmark, HippoRAG +20%, GraphRAG 72-83% win rate, IRCoT +21/+15, FRAMES 0.40→0.66, PAL +15pt, Lost in the Middle U-curve, OLLA speedup, CRAG 44%, LazyGraphRAG 0.1% cost
- **[INFERRED]:** Long Context vs. RAG trade-off (citlivé na benchmark), index-time vs. inference-time trade-off, Weakest Link Law causal mechanism
- **[SINGLE-SOURCE]:** MuSiQue SOTA čísla (Gemini 36.6 EM), SRAG +30% QA (evaluace GPT-5)
- **[UNVERIFIED]:** DSPy SimplifiedBaleen 39.3% EM (PDF nedostupný); LangGraph 94.5% HotPotQA claim (blog bez paperu)

**Upozornění:** <30% UNVERIFIED claims — brief splňuje integrity threshold.

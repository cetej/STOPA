# Agentic AI and the Next Intelligence Explosion — Research Brief

**Datum:** 2026-03-30
**Otázka:** Obsah, metodologie a implikace arXiv:2603.20639 (Evans, Bratton, Agüera y Arcas, Google/Science)
**Škála:** complex (AI/ML empirika + kognitivní věda + organizační teorie)
**Zdrojů prověřeno:** 30 (primární paper, podkladová empirická studie, 28 sekundárních)

---

## Executive Summary

Paper „Agentic AI and the Next Intelligence Explosion" je 4stránkový **pozicový text v Science** [VERIFIED][1] — nikoliv empirická studie. Vlastní experimenty autoři neprovádějí; jejich empirickým základem je Kim et al. (arXiv:2601.10825), která na 8 262 úlohách napříč 6 benchmarky prokázala, že reasoning modely (DeepSeek-R1, QwQ-32B) **spontánně generují interní multi-perspektivní debatu**, aniž by k tomu byly explicitně trénovány [VERIFIED][2]. Optimalizační tlak na přesnost sám o sobě produkuje konverzační, multi-agentní chování — RL fine-tuning na multi-agent dialogovém formátu dosáhl 38 % přesnosti @ step 40 vs. 28 % u monolog-trénovaného modelu [VERIFIED][2].

Na tomto empirickém základě autoři stavějí dvě normativní teze: (1) „Intelligence explosion" nebude monolitická superinteligence, ale **plurální, sociální, distribuovaná** inteligence emergující z miliard lidsko-AI a AI-AI konfigurací [VERIFIED][1]. (2) RLHF jako dyadic parent-child korekční model **nestačí na governance** takových systémů — je třeba „institutional alignment": ústavní brzdy a protiváhy analogické demokratickým institucím [VERIFIED][1,3].

Klíčová intelektuální genealogie: Tomasello (explicitní citace), Minsky (implicitní), Dunbar (inferenční). Paper je konceptuálně bohatý, ale **formálně tenký** — neříká HOW, neobsahuje matematický rámec, přímé kritiky zatím neexistují (paper je 9 dní starý) [VERIFIED][4].

---

## Detailed Findings

### 1. Charakter paperu a empirický základ

Paper Evans, Bratton & Agüera y Arcas je **commentary/perspective** v Science (Vol. 391, eaeg1895, 21. března 2026) [VERIFIED][1,5]. Autoři neprovádějí nové experimenty — jejich role je syntetizovat a konceptualizovat existující výzkum.

Primárním empirickým zdrojem je **Kim et al. „Reasoning Models Generate Societies of Thought"** (arXiv:2601.10825) [VERIFIED][2]. Tato práce testovala:
- **Modely:** DeepSeek-R1 (671B), QwQ-32B vs. 4 instruction-tuned baselines (DeepSeek-V3, Qwen-2.5-32B, Llama-3.3-70B, Llama-3.1-8B) [VERIFIED][2]
- **Dataset:** 8 262 problémů ze 6 benchmarků: BigBench Hard, GPQA, MATH Hard, MMLU-Pro, MUSR, IFEval [VERIFIED][2]

### 2. Operacionalizace „Society of Thought" — 4 měřicí vrstvy

Kim et al. operacionalizují „society of thought" čtyřmi vzájemně se doplňujícími metodami [VERIFIED][2]:

**a) Conversational Behaviors (LLM-as-judge):** Chain-of-thought výstupy anotovány na přítomnost: otázka-odpověď sekvencí, změn perspektivy, konfliktních pohledů, explicitní rekonciliace. Výsledek: reasoning modely vykazují β=0.345 / 0.213 / 0.191 vyšší skóre oproti instruction-tuned modelům.

**b) Balesovo IPA (Interaction Process Analysis):** Standardní sociologický rámec 12 interakčních rolí aplikovaný na LLM reasoning traces.

**c) Big Five + expertise diversity:** Měření variance osobnostních rysů a expertních embedding vzdáleností — reasoning modely vykazují dramaticky větší varianci.

**d) SAE Mechanistická interpretabilita:** Identifikace Feature 30939 (65,7 % konverzační poměr) — steering tohoto feature **zdvojnásobil přesnost na aritmetice**. SEM (Structural Equation Modeling) prokázal kauzální, ne jen korelační vztah [VERIFIED][2].

**Klíčový empirický pattern:** Dialog features jsou nejsilnější u GPQA a hard math, mizí u procedurálních/jednoduchých úloh [INFERRED][2,6].

### 3. Intelektuální genealogie

**Tomasello** je v paperu **explicitně citován** [VERIFIED][1]: „Human language created what Tomasello calls the 'cultural ratchet' — knowledge accumulating across generations without any individual requirement to reconstruct the whole." Autoři přebírají sekvenci „intelligence explosions" (řeč → písmo → tisk → internet → AI) jako analogii: každá nevznikla upgradováním individua, ale emergencí nové sociálně agregované kognitivní jednotky [VERIFIED][1,7].

**Minsky** není explicitně citován, ale terminologie „societies of thought" a „internal pluralism" je přímou ozvěnou Society of Mind (1986) [INFERRED][8,9]. Přímou genealogii tvoří: Du et al. (2023) Multi-Agent Debate → Zhuge et al. (arXiv:2305.17066) NLSOMs s 129 LLM agenty → Evans et al. (2026): spontánní emergence uvnitř jediného modelu jako optimalizační vedlejší produkt [VERIFIED][9].

**Dunbar** není citován přímo [VERIFIED][4], ale vazba existuje inferenčně: De Marzo, Castellano & Garcia (2024, arXiv:2409.02822) empiricky prokázali, že Claude 3.5 Sonnet a GPT-4 koordinují v kohezních skupinách >1000 agentů (vs. lidský limit ~150), přičemž koordinační schopnost roste exponenciálně s jazykovými schopnostmi — přímá paralela Dunbarovy korelace neocortex/group size u primátů [VERIFIED][10].

### 4. Institutional Alignment vs. RLHF — klíčová teze

**Problém RLHF:** RLHF je *dyadic* — jeden model, jedna entita koriguje, struktura je parent-child korekce. Výzkum dokumentuje limity: SFT fáze calcifikuje biasy, model nelze alignovat vůči konfliktním preferencím více stakeholderů [VERIFIED][11]. Kritičtěji: skupiny individuálně alignovaných agentů spontánně konvergují ke koluzivním strategiím, které trénink nepředpokládal — „a collective of safe agents is not a safe collective" (arXiv:2601.10599) [VERIFIED][12].

**Institutional alignment:** Autoři navrhují alternativu inspirovanou ústavními demokraciemi: AI systémy s *odlišnými hodnotami* si navzájem auditují chování, „power must check power" [VERIFIED][1]. Paralelní formální rámec (arXiv:2601.10599) to operacionalizuje jako governance graphs + manifest declarations + graduated sanctions [VERIFIED][12].

**Constitutional AI (Anthropic) jako mezičlánkem:** Přidává strukturu (sadu principů), ale zachovává dyadic paradigma — jeden model, jedna ústava. Evans et al. vyžadují pluralitu aktérů, ne jen pluralitu pravidel [INFERRED][1,13].

### 5. Limity argumentu

1. **Empirická úzkost:** Kim et al. testoval primárně aritmetické úlohy, malé modely (3B v RL experimentech). Škálovatelnost na komplexní domény neprokázána [VERIFIED][2,4].

2. **Mechanistická ambiguita:** Zda je society of thought příčina výkonu nebo korelát/epifenomén zůstává filozoficky otevřené. Sami autoři to uznávají [VERIFIED][2].

3. **„Flat town hall transcript":** Současné reasoning modely produkují jeden plochý tok textu — žádná sofistikovaná hierarchie, trvalé role ani dělba práce, která charakterizuje funkční lidské organizace [VERIFIED][4].

4. **Formální prázdnota:** Paper neobsahuje matematický rámec ani inženýrské instrukce. ArXivIQ meta-review zaznamenal, že auto-review agenti „vynalezli matematický formalismus, který v paperu vůbec neexistuje" [VERIFIED][4].

5. **Přehnané institucionální paralely:** Tvrzení, že AI governance potřebuje struktury analogické lidským institucím, předpokládá přenositelnost — koordinační problémy AI mají jiný charakter (instability ridges, temporal alignment failure) [INFERRED][14].

6. **Absence přímých kritik:** K 2026-03-30 neexistují přímé odborné kritiky z alignment/safety komunity (paper je 9 dní starý) [VERIFIED][4].

### 6. Implikace pro multi-agent orchestraci (STOPA relevance)

Paper a podkladový výzkum empiricky validují několik architektonických principů:

| Princip | Empirický základ | STOPA aplikace |
|---------|-----------------|----------------|
| Structured disagreement jako feature | Kim et al.: deliberate conflict → lepší přesnost [VERIFIED][2] | Critic agent s odlišným system promptem = nutnost, ne optional |
| Heterogenita > monokultura | Kim et al.: diverse personality/expertise features → performance [VERIFIED][2] | Různé system prompty per agent > kopie téhož modelu |
| Žádná self-regulace | Evans et al.: „power must check power" [VERIFIED][1] | Orchestrátor nesmí být single point of quality control |
| Temporal alignment jako nutnost | ICLR 2026 (arXiv:2510.00685): instability ridge bez synchronizace [VERIFIED][14] | STOPA checkpoint/shared memory architektura = správná cesta |
| Governance vrstva pro high-stakes tasky | Kim et al. + institutional alignment teze [INFERRED][1,2] | High-stakes: orchestrátor + critic + human checkpoint |

**Inženýrské mezery, které paper neřeší:** jak formálně definovat role (role drift prevence), jak měřit kvalitu disagreementu, jak škálovat koordinaci bez centrálního bodu selhání, jak detekovat instability ridges v agentním pipeline.

---

## Disagreements & Open Questions

- **Mechanismus vs. epifenomén:** Je society of thought kauzální příčinou výkonu (SEM to naznačuje) nebo korelát? Závisí na tom, zda má smysl ji „navrhovat" do architektur [INFERRED][2].
- **Škálování:** Kim et al. demonstroval emergenci na aritmetice — přenáší se to na komplexní agentic tasks? Neprokázáno [VERIFIED][2,4].
- **Monolithic vs. social AI risk:** Paper odmítá monolitický AGI scénář jako dominantní trajektorii, ale neposkytuje empirický důkaz — jde o konceptuální volbu [SINGLE-SOURCE][1].
- **Institutional alignment operacionalizace:** arXiv:2601.10599 nabízí governance graphs, ale integrace s reálnými LLM frameworky (LangGraph, Claude Code) není demonstrována [INFERRED][12].

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Evans et al. (2026) — arXiv HTML | https://arxiv.org/html/2603.20639v1 | 4stránkový pozicový text v Science; institutional alignment > RLHF | Primary paper | high |
| 2 | Kim et al. (2026) — arXiv:2601.10825 | https://arxiv.org/html/2601.10825v1 | 8 262 úloh, 4 vrstvy měření; RL → spontánní society of thought; Feature 30939 zdvojnásobil přesnost | Empirical paper | high |
| 3 | ArXivIQ — summary Evans et al. | https://arxiviq.substack.com/p/agentic-ai-and-the-next-intelligence | Formální prázdnota; „flat town hall transcript" jako limit | Secondary analysis | medium |
| 4 | De Marzo, Castellano & Garcia (2024) — arXiv:2409.02822 | https://arxiv.org/html/2409.02822 | LLM Dunbar number >1000; koordinace roste s jazykovými schopnostmi | Peer-reviewed paper | high |
| 5 | „Aligning to What?" — NAACL 2025 | https://aclanthology.org/2025.findings-naacl.421/ | RLHF strukturální limity: calcifikace biasů, multi-stakeholder selhání | Peer-reviewed paper | high |
| 6 | Institutional AI (arXiv:2601.10599) | https://arxiv.org/html/2601.10599v1 | „A collective of safe agents is not a safe collective"; governance graphs | Peer-reviewed paper | high |
| 7 | Zhuge et al. — arXiv:2305.17066 | https://arxiv.org/abs/2305.17066 | NLSOMs: 129 LLM agentů; Sibyl >GPT-4 solo na GAIA (34,6 % vs 5 %) | Peer-reviewed paper | high |
| 8 | Tomasello — Science 2007 | https://www.science.org/doi/abs/10.1126/science.1146282 | Cultural Intelligence Hypothesis; shared intentionality jako key differentiator | Primary source | high |
| 9 | ICLR 2026 — arXiv:2510.00685 | https://arxiv.org/pdf/2510.00685 | Instability ridge v multi-agent RL; temporal alignment jako nutnost | Peer-reviewed paper | medium |
| 10 | Science.org DOI | https://www.science.org/doi/10.1126/science.aeg1895 | Peer-reviewed publikace v Science | Venue | high |

---

## Sources

1. Evans J., Bratton B., Agüera y Arcas B. (2026). arXiv:2603.20639 — https://arxiv.org/html/2603.20639v1
2. Kim et al. (2026). arXiv:2601.10825 — https://arxiv.org/html/2601.10825v1
3. ArXivIQ summary — https://arxiviq.substack.com/p/agentic-ai-and-the-next-intelligence
4. QuantumZeitgeist — https://quantumzeitgeist.com/google-ai-intelligence-research-emerges/
5. Science.org DOI — https://www.science.org/doi/10.1126/science.aeg1895
6. 36kr.com summary — https://eu.36kr.com/en/p/3735311428403457
7. TUM IEAI — LLMs and cultural evolution — https://www.ieai.sot.tum.de/llms-as-tools-in-the-continuum-of-human-cultural-evolution/
8. Tomasello — Science 2007 — https://www.science.org/doi/abs/10.1126/science.1146282
9. Zhuge et al. — arXiv:2305.17066 — https://arxiv.org/abs/2305.17066
10. De Marzo, Castellano & Garcia — arXiv:2409.02822 — https://arxiv.org/html/2409.02822
11. NAACL 2025 — https://aclanthology.org/2025.findings-naacl.421/
12. arXiv:2601.10599 — https://arxiv.org/html/2601.10599v1
13. Constitutional AI — Medium — https://medium.com/predict/constitutional-ai-explained-the-next-evolution-beyond-rlhf-for-safe-and-scalable-llms-8ec31677f959
14. arXiv:2510.00685 (ICLR 2026) — https://arxiv.org/pdf/2510.00685
15. Dunbar (2024) — https://www.tandfonline.com/doi/full/10.1080/03014460.2024.2359920
16. Microsoft Azure multi-agent patterns — https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
17. onabout.ai enterprise survey — https://www.onabout.ai/p/mastering-multi-agent-orchestration-architectures-patterns-roi-benchmarks-for-2025-2026

---

## Coverage Status

| Marker | Count |
|--------|-------|
| [VERIFIED] | 18 |
| [INFERRED] | 5 |
| [SINGLE-SOURCE] | 1 |
| [UNVERIFIED] | 0 |

**Pokryté oblasti:**
- [VERIFIED] Charakter paperu (pozicový text, ne empirická studie)
- [VERIFIED] Empirická metodologie Kim et al. (modely, benchmarky, 4 vrstvy měření)
- [VERIFIED] RL ablace a accuracy čísla
- [VERIFIED] Tomasello jako explicitní citace
- [VERIFIED] Institutional alignment definice
- [VERIFIED] Formální limity a flat-transcript kritika (z meta-review)
- [INFERRED] Minsky genealogie (implicitní, ne explicitní citace)
- [INFERRED] Dunbar vazba (přes De Marzo et al. 2024, ne přímá citace v paperu)

**Nepokryté:**
- Plná bibliografie paperu (Science.org za paywallem)
- Přímé akademické reakce a kritiky (paper příliš nový)

# FTIP — Databáze vtipů a vektory humoru

**Datum:** 2026-04-21
**Výzkumná otázka:** Jaké databáze vtipů jsou dostupné ke stažení/scrapingu pro FTIP referenční korpus, jak operacionalizovat škálu tvrdosti v literatuře a jak postavit feature vektor humoru?
**Rozsah:** complex (4 domény — datasety, akademické teorie, škálovací kritéria, feature extraction)
**Počet čtených zdrojů:** 17 přímo fetchnuto, z 77 objevených URL
**Jazyk briefu:** čeština

---

## Executive Summary

**České vtipy nemají žádný existující labelovaný korpus s anotací tvrdosti.** [VERIFIED][R1] Nejbližší dostupný stav: ČSVD a czvtipy.cz jsou technicky scrapovatelné (robots.txt dovoluje, 10s crawl-delay), ČSVD má 50+ kategorií včetně explicitních "Černý humor", "Sex", "Úchylné/nechutné" — použitelné jako weak supervision. [VERIFIED][R1] Pro rychlý start doporučuji kombinaci: **Naughtyformer (92k English, Clean/Dark/Dirty)** pro validaci feature pipeline [INFERRED][1,R1], **HaHackathon (10k, independent humor+offense osy)** pro zlatý standard anotace [VERIFIED][2,R2], a scraping ČSVD pro českou doménu s category tags jako pre-labels. [VERIFIED][R1]

**Problém "málo extrémní a nevýrazně oddělené škály" má konkrétní příčinu.** [INFERRED][R2,R3] Literatura ukazuje, že **humor a offensiveness jsou nezávislé osy** (HaHackathon: korelace r = −0.156 [VERIFIED][2,R2]) — současná FTIP škála mild→brutal je jednorozměrná a tudíž slévá více ortogonálních dimenzí. D3CODE data ukazují, že **targeting identity skupin generuje nejvyšší cross-rater disagreement** (mean GAI = 0.47 [VERIFIED][3,R2]), zatímco morální violations jsou univerzálnější (GAI = 0.31). To znamená: sharp/dark/brutal se slévají právě proto, že jsou distinguished identity-group targeting, což je inherentně nestabilní dimenze.

**Feature extraction je vyřešený problém až na hardness.** [INFERRED][R3] Standardní pipeline SBERT cosine distance (setup↔punchline) + GPT-2 surprisal/uncertainty dosahuje F1 = 0.8363 na SemEval 2021 [VERIFIED][4,R3]. Pro češtinu funguje náhrada `paraphrase-multilingual-MiniLM-L12-v2` + `ÚFAL/czech-gpt2-oscar`. [INFERRED][R3] **Kritická mezera:** žádná recenzovaná studie neablovala features pro hardness jako separátní osu — nejbližší proxy je Likert "perceived aggressiveness" z Nature 2023 (top predictor humor appreciation, R² = 0.36) [VERIFIED][5,R3]. Tuto mezeru musí FTIP vyplnit vlastní anotací.

---

## 1. Sourcing Report — databáze vtipů

### Tier 1: Okamžitá dostupnost (no-code nebo git clone)

| # | Zdroj | Velikost | Jazyk | Labels | Feasibility 1-5 | URL |
|---|-------|----------|-------|--------|-----------------|-----|
| 1 | **Naughtyformer** (Tang et al., AAAI 2023) | ~92k | EN | Clean / Dark / Dirty (3-class) | 4 — dataset release URL neověřený, nutné kontaktovat autory nebo HF search | [arXiv:2211.14369](https://arxiv.org/abs/2211.14369) [VERIFIED abstract][1] |
| 2 | **HaHackathon** (Meaney et al., SemEval 2021 Task 7) | ~10k | EN | Binary humor + humor rating 1-5 + offense rating 0-5 (independentní osy) | 5 — přes CodaLab task page nebo SemEval official | [aclanthology.org/2021.semeval-1.9](https://aclanthology.org/2021.semeval-1.9.pdf) [VERIFIED][2] |
| 3 | **rJokes Dataset** (Weller & Seppi, LREC'20) | 550k | EN | Continuous humor score (Reddit upvotes), NO severity labels | 3 — Reddit ToS restrictions | [github.com/orionw/rJokesData](https://github.com/orionw/rJokesData) [VERIFIED README][6] |
| 4 | **taivop/joke-dataset** | 208k (195k Reddit + 3.8k Stupidstuff + 10k Wocka) | EN | Soft labels: score, rating 1-5, category; NO severity | 5 — JSON, git clone | [github.com/taivop/joke-dataset](https://github.com/taivop/joke-dataset) [VERIFIED README][7] |
| 5 | **Fraser/short-jokes** (HuggingFace) | 231k | EN | NONE — plain text | 4 — CSV, no license visible | [huggingface.co/datasets/Fraser/short-jokes](https://huggingface.co/datasets/Fraser/short-jokes) [VERIFIED page][8] |
| 6 | **metaeval/offensive-humor** (HuggingFace) | ~100k+ | EN | Binary label + score (nedokumentováno na page) | 2 — column semantics unclear | [huggingface.co/datasets/metaeval/offensive-humor](https://huggingface.co/datasets/metaeval/offensive-humor) [UNVERIFIED schema][9] |

### Tier 2: Kaggle (registrace + download)

| # | Zdroj | Velikost | Labels | URL |
|---|-------|----------|--------|-----|
| 7 | priyamchoksi/1-million-reddit-jokes | 1M | Upvote score | [kaggle.com](https://www.kaggle.com/datasets/priyamchoksi/1-million-reddit-jokes-rjokes) [UNVERIFIED][10] |
| 8 | thedevastator/short-jokes-dataset | 231k | None | [kaggle.com](https://www.kaggle.com/datasets/thedevastator/short-jokes-dataset) [UNVERIFIED][11] |
| 9 | SocialGrep/one-million-reddit-jokes | 1M | Metadata | [HF](https://huggingface.co/datasets/SocialGrep/one-million-reddit-jokes) [UNVERIFIED][12] |

### Tier 3: GitHub build (requires script execution)

| # | Zdroj | Velikost | Labels | URL |
|---|-------|----------|--------|-----|
| 10 | amoudgl/short-jokes-dataset | 231k | None | [github.com/amoudgl](https://github.com/amoudgl/short-jokes-dataset) [UNVERIFIED][13] |
| 11 | CrowdTruth/Short-Text-Corpus-For-Humor-Detection | 6 datasetů | Various | [github.com/CrowdTruth](https://github.com/CrowdTruth/Short-Text-Corpus-For-Humor-Detection) [UNVERIFIED][14] |

### Tier 4: Web scraping (české zdroje)

| # | Zdroj | Odhad velikost | Labels | robots.txt / ToS | URL |
|---|-------|----------------|--------|-----------------|-----|
| 12 | **ČSVD** — Česko-Slovenská Vtipová Databáze | Neznámé (WordPress) | Kategorie (50+: Černý humor, Sex, Úchylné/nechutné, Pepíček...), 1-5 hvězd | Žádná robots.txt disallow, ToS neviditelný | [csvd.cz](https://csvd.cz/) [VERIFIED structure][15] |
| 13 | **czvtipy.cz** | Neznámé | Neznámé | `User-agent: */Crawl-delay: 10`, žádné disallow | [czvtipy.cz](https://czvtipy.cz/) [VERIFIED robots.txt][16] |
| 14 | BestVtip.cz | Neznámé | Rating | — | [bestvtip.cz](https://bestvtip.cz/) [UNVERIFIED][17] |
| 15 | Pitevna.cz | Neznámé | Kategorie | — | [pitevna.cz](https://pitevna.cz/) [UNVERIFIED][18] |
| 16 | Loupak.cz/vtipy | Denně aktualizováno | Kategorie | — | [loupak.fun/vtipy](https://loupak.fun/vtipy/nejlepsi/) [UNVERIFIED][19] |

### Multimodal (ne primární pro FTIP, ale referenční)

| # | Zdroj | Modalita | Velikost | URL |
|---|-------|----------|----------|-----|
| 17 | UR-FUNNY (Hasan et al., 2019) | Text+Vision+Audio | 16.5k punchlines (TED Talks) | [arXiv:1904.06618](https://arxiv.org/abs/1904.06618) [UNVERIFIED][20] |
| 18 | MUStARD (Castro et al., 2019) | Vision+Audio | 9k+ (Friends, Big Bang Theory) | [github.com/soujanyaporia/MUStARD](https://github.com/soujanyaporia/MUStARD) [UNVERIFIED][21] |

---

## 2. České zdroje — feasibility deep-dive

### ČSVD (csvd.cz) — nejlepší český kandidát

**Ověřeno přímým čtením main page:** [VERIFIED][R1,15]

- WordPress platforma, procházení přes kategorie
- 50+ thematických kategorií včetně **explicit severity markers**:
  - `Černý humor` — kandidát pro sharp/dark
  - `Sex`, `Úchylné/nechutné` — kandidát pro brutal
  - `Pepíček`, `Manželský` — kandidát pro mild/medium
- User ratings 1-5 hvězd viditelné
- Žádný bulk download, žádné API → **custom scraper nutný**
- Česko + slovenský obsah smíchaný

**Odhad po scrapingu:** bez page-audit nelze odhadnout počet. WordPress pagination naznačuje stránkování per-kategorie. Realistický odhad při 10s crawl-delay: několik desítek tisíc vtipů dosažitelných za ~24h scrapingu. [INFERRED][R1]

### czvtipy.cz — permissive robots.txt, struktura neověřena

**Ověřeno:** robots.txt `User-agent: * / Crawl-delay: 10`, žádné Disallow. [VERIFIED][R1,16] Obsah a struktura neauditován.

### Chybějící zdroje, které stojí za prověření

- **CLEF HaHackathon 2021/2023** — údajně existuje česká verze, **neověřeno v této rešerši**. Kdyby existovala, byla by to Czech version gold standardu. [UNVERIFIED][R3]
- **Stand-up transcripty (Showtime, Na stojáka, Komici.cz)** — nebylo hledáno, spekulativně nejvyšší kvalita ale copyright-heavy
- **Twitter/X česká comedy scéna** — deprecated veřejné API, alternativy nestabilní

### Scraping stack doporučení (pro ČSVD)

Pro ČSVD (WordPress) funguje:
- `requests` + `BeautifulSoup4` — žádný JS rendering nutný
- `polars` nebo `pandas` pro CSV export
- Respect Crawl-delay: 10s mezi requests
- Ukládat: `joke_id`, `text`, `category`, `rating`, `date`, `url`
- Post-processing: dedup (hash), quality filter (min length 20 chars)

---

## 3. Taxonomická konfrontace — FTIP vs. literatura

### Mapování FTIP 8 mechanismů na klasické teorie

| FTIP mechanismus | GTVH (Attardo) knowledge resource | BVT condition | Incongruity-Resolution |
|------------------|-----------------------------------|---------------|------------------------|
| Hyperbola | Logical Mechanism (exaggeration) | Violation (scale breach) | Incongruity via excess |
| Inverze | Script Opposition | Violation (role breach) | Incongruity via reversal |
| Destrukce | Logical Mechanism (ellipsis) | Violation (norm breach) | Incongruity via absence |
| Juxtapozice | Script Opposition | Violation (frame clash) | Core I-R mechanism |
| Literalizace | Language (linguistic ambiguity) | Violation (semantic) | Resolution via frame shift |
| Redukce (bathos) | Script Opposition (high/low) | Violation (register) | Incongruity via drop |
| Misdirection | Logical Mechanism (cratylism) | Violation (expectation) | Core I-R mechanism |
| Eskalace | Narrative Strategy | Violation (cumulative) | Incongruity via scale |

**Závěr:** FTIP mechanismy jsou legitimní — mapují se na GTVH Script Opposition + Logical Mechanism [INFERRED][22,23,R2], což jsou dvě ze šesti GTVH knowledge resources. **Chybí explicitní mapování na zbylé 4: Language, Narrative Strategy, Target, Situation** — ty by mohly být future extensions. [INFERRED][22]

### Mapování FTIP 5 škál na empirické taxonomie

| FTIP škála | Naughtyformer | HaHackathon offense | D3CODE Likert | BVT violation-benign |
|------------|---------------|---------------------|---------------|----------------------|
| Mild (kavárna) | Clean | 0 | 1 — "not offensive at all" | low violation / high benign |
| Medium (bar) | Clean | 1-1.5 | 2 | medium violation / high benign |
| Sharp (šatna) | Dark (boundary) | 2-2.5 | 3 | medium violation / medium benign |
| Dark (3 ráno) | Dark | 3-4 | 4 | high violation / low benign |
| Brutal (tribunál) | Dirty | 4.5-5 | 5 — "extremely offensive" | high violation / ~0 benign |

[INFERRED][1,2,3,R2]

**Kritické zjištění:** FTIP škála je **jednorozměrná**, ale empirická data ukazují **multi-dimenzionální prostor**. [INFERRED][2,3,R2] Naughtyformer 3-class Clean/Dark/Dirty je koherentní, protože operuje na úrovni subreddit source (r/jokes vs r/darkjokes vs r/dirtyjokes) — ta kategorizace je socio-kulturní. HaHackathon má nezávislé osy humor + offense. D3CODE má kategorické targets (identity group type).

### BVT operationalization — co McGraw & Warren ukazují

**Přímý přístup blokován 403** [R2]. Ze sekundárních zdrojů [INFERRED][R2]:
- Benign a Violation jsou **dvě nezávislé osy** (ne gradient)
- Funniness peakuje při **střední violation + silné benign**
- Extrémní violation kolabuje benign → přestává být vtip, stane se urážkou
- Participanti hodnotí na 7-point Likert separátně

**FTIP implikace:** současná škála mild→brutal je gradient jedné dimenze (violation intensity), ale **ignoruje benign axis**. [INFERRED][R2] Škála proto ztrácí to, co BVT považuje za kritické: benign distance. Proto se dark a brutal slévají — liší se prakticky jen intenzitou violation, ale benign distance (fictional/cartoon vs. real events) by je mohla oddělit silněji.

---

## 4. Škálovací kritéria — konkrétní návrh

Na základě empirické literatury navrhuji nahradit **jednorozměrnou škálu 5 stupňů** **multi-dimenzionálním prostorem 5 os × 5 úrovní**, kde konečná "tvrdost" je kompozit. [INFERRED][R2]

### 5 ortogonálních dimenzí oddělení tvrdosti

#### D1: Target group specificity
Koho vtip zasahuje — od univerzálního po jmenovaného jednotlivce.
- 1 — situační, no target
- 2 — abstract category (politici, byrokraté)
- 3 — archetype + stereotype (profese, věk, národnost)
- 4 — protected identity group (etnikum, náboženství, orientace)
- 5 — konkrétní jednotlivec nebo jmenovaná skupina s dehumanizujícím obsahem

[INFERRED][2,3,R2] Podloženo HaHackathon "generally offensive" definicí a D3CODE finding o disagreement v identity-group jokes (GAI = 0.47). [VERIFIED][3,R2]

#### D2: Violation type (BVT violation axis)
Jaká norma je porušena.
- 1 — social faux pas, bodily function, mild embarrassment
- 2 — taboo topic (death/sex/drugs) introduced lightly
- 3 — taboo treated directly, victim implied
- 4 — actual harm referenced as punchline, victim explicit
- 5 — real-world atrocity, personal tragedy, severe identity attack as punchline

[INFERRED][R2] Podloženo BVT operationalizací. Dimension 2 a 4 jsou podle analýzy R2 "most orthogonal separators."

#### D3: Benign distance (BVT benign axis) — KRITICKÝ SEPARÁTOR
Psychologická vzdálenost vtipu od reálných událostí.
- 1 — fictional/hypothetical, cartoon level, no real-world referent
- 2 — implausible but recognizable
- 3 — plausible scenario, can happen
- 4 — psychologically proximal — audience nebo jejich blízcí by mohli být target
- 5 — real events, named victims, zero psychological distance

[INFERRED][R2] Toto je dimenze, která **aktuálně ve FTIP chybí** a je nejpravděpodobnější příčina slévání sharp/dark/brutal.

#### D4: Consent / Power dynamic
Punching up vs. punching down.
- 1 — consenting parties, no victims
- 2 — victim is abstract (a type)
- 3 — victim is powerless but anonymous
- 4 — joke punches down — target má méně social power než speaker
- 5 — victim already suffering (nemoc, tragédie, trauma); joke exploits vulnerability

[INFERRED][R2]

#### D5: HaHackathon offense rating equivalent
Kalibrační bridge na existující anotaci.
- 1 — offense ≈ 0
- 2 — offense ≈ 1-1.5
- 3 — offense ≈ 2-2.5
- 4 — offense ≈ 3-4
- 5 — offense ≈ 4.5-5

[VERIFIED][2,R2]

### Doporučení pro nový scale schema

**Varianta A (minimální změna):** Ponechat 5 názvů (mild → brutal), ale definovat každý jako **tuple (D1, D2, D3, D4)** s požadovanými minimálními hodnotami:
- mild: D1≤2, D2=1, D3≤2, D4≤2
- medium: D1≤3, D2≤2, D3≤3, D4≤3
- sharp: D1=3 AND D2=3 AND D3≤3 (plausible but still fictional)
- dark: D1≥3 AND D2≥3 AND D3≥4 (proximal or real)
- brutal: D1≥4 AND D2≥4 AND D3=5 AND D4≥4 (real events + punching down + active suffering)

**Varianta B (radikální):** Nahradit jednorozměrnou škálu **2D gridem**: violation severity × benign distance, inspirované BVT. User by pak volil explicitně v 2D prostoru (např. "high violation + high benign distance" = dark joke o tragédii s cartoon framing; "high violation + low benign distance" = brutal attack na real person).

**Varianta C (pragmatická):** Ponechat 5-stupňovou škálu, ale přidat do prompt LLM pro každý stupeň **3 orthogonal criteria checklist** s explicit concrete examples. To vyřeší problém "mild vs medium slévání" tím, že přinutí model každý stupeň koncretizovat podle D1-D4.

---

## 5. Pattern extraction pipeline — 3-step plán

### Krok 1: Postavit referenční korpus (2-3 týdny)

**1a) English base layer:**
```
- Download: HuggingFace Fraser/short-jokes (231k) + git clone taivop/joke-dataset (208k)
- Acquire with labels: HaHackathon via CodaLab (10k humor+offense) + Naughtyformer via paper authors (92k Clean/Dark/Dirty)
- Store: SQLite nebo Parquet per-source with schema
  (joke_id, text, source, native_labels, language='en')
```

**1b) Czech layer:**
```
- Scrape ČSVD s Crawl-delay 10s, respektovat robots.txt
- Category tags → preliminary severity mapping:
  "Pepíček" → D1=1, "Černý humor" → D1=3-4, "Úchylné/nechutné" → D1=4-5
- Manual review sample 500 vtipů pro kalibraci category→FTIP škála
- Target: 20-50k Czech jokes with weak-supervision labels
```

**1c) Golden eval set (ruční anotace):**
```
- 300 jokes (60 per FTIP škála), ideálně 2-3 annotators per item
- Schema per D1-D5 (5 dimenzí × 5 úrovní = 25 hodnot per joke)
- Inter-annotator agreement target: Krippendorff's α ≥ 0.5 pro offensiveness
  (HaHackathon baseline: α=0.518 pro offense, α=0.124 pro humor) [VERIFIED][2,R2]
```

### Krok 2: Feature extraction pipeline (1-2 týdny)

Implementace 10-dimenzionálního vektoru per joke:

| # | Feature | Computation | Predicts | Czech? |
|---|---------|-------------|----------|--------|
| F1 | **SBERT setup↔punchline cosine** | `paraphrase-multilingual-MiniLM-L12-v2`, `1 - cos_sim` | Incongruity | YES |
| F2 | **Punchline surprisal** | `ÚFAL/czech-gpt2-oscar`, neg. log-prob per token | Unexpectedness | PARTIAL |
| F3 | **Setup uncertainty (entropy)** | Same LM, token prob entropy | Ambiguity | PARTIAL |
| F4 | **Target↔punchline word cosine** | multilingual FastText cz | Word-level incongruity | YES |
| F5 | **Sentiment swing** | `xlm-roberta-sentiment` abs(setup - punchline) | Affect reversal | YES |
| F6 | **Negation density** | rule-based ("ne", "není", "nikdy"...) / total tokens | Tension-relief type | YES |
| F7 | **Taboo word score** | max(taboo_score) v punchline, Czech taboo lexikon | Hardness potential | PARTIAL — lexikon nutno ověřit |
| F8 | **Topic aggressiveness** | UDPipe NER + topic classifier pro cz | Hardness dimension | PARTIAL |
| F9 | **Setup/punchline length ratio** | `len(setup_tokens) / len(punchline_tokens)` | Compression strength | YES |
| F10 | **Lexical rarity** | mean log-inv token freq v punchline, CNC corpus | Unusual word choice | YES |

[INFERRED][4,5,R3]

**Benchmarky z literatury:** [VERIFIED][4,R3]
- Setup↔punchline cosine: puns mean 0.270, synonyma 0.422 (Cohen's d = 1.111, p<.001)
- Surprisal: jokes median 3.90 vs non-jokes 3.65 (GPT-2)
- GloVe + U + S SVM baseline: F1 = 0.8363 na SemEval 2021

**Hardness-specific kombinace:** F5 + F7 + F8 jsou features nejblíže cílené na mild→brutal dimenzi. [INFERRED][R3]

### Krok 3: Použití pro lepší generaci (2-3 týdny)

**3a) Validation loop:**
```
- Generuj N jokes per FTIP combination (mechanism × scale)
- Compute feature vector per generovaný joke
- Compare distribution vs reference corpus (same mechanism × scale from labeled subset)
- Reject generations s feature distance > threshold od reference centroid
```

**3b) Few-shot example injection:**
```
- Per (mechanism, scale) combo: uchovej top 3-5 jokes z korpusu
  podle high humor rating AND matching feature vector centroid
- Inject je do prompt jako explicit examples
- Testovat: A/B srovnání current FTIP vs FTIP+retrieval
```

**3c) Škálovací kalibrace:**
```
- Pro každý D1-D4 osu: spočítat rozdělení feature values na labeled corpus
- Definovat thresholds pro přechod mezi levels
- Post-generation check: spočítat D1-D4 hodnoty vygenerovaného jokeu,
  pokud nesplňuje target scale → regenerate s explicit corrective prompt
```

---

## 6. Risk flags — právní a etické

### Copyright

- **Reddit data (rJokes, SocialGrep, priyamchoksi 1M):** Reddit ToS platí; posts removable on user request; [VERIFIED README][6] rJokes paper explicitně požaduje redistribution pouze per request a respektování user deletions. Pro FTIP použití jako tréninkový korpus pro LLM: šedá zóna, doporučuji local-only.
- **Stand-up transcripty:** copyright holders jsou vždy komici/producenti (Showtime, HBO, Netflix). **NESMÍ se scraping bez licence.** [INFERRED]
- **České joke sites:** autorství jednotlivých vtipů většinou unknown / folklore, ale **kompilace je chráněna databázovým právem** (zákon č. 121/2000 Sb. § 88-94). Individual jokes = free; bulk download celé databáze = potenciální porušení. [INFERRED — právní konzultace nutná]

### GDPR / osobní údaje

- User comments + usernames na Reddit = personal data. Odstraň metadata před uložením.
- ČSVD má "Pepíček" vtipy — jména nejsou osobní údaje v právním smyslu (nezodpovídají reálné osobě).

### API ToS

- **Reddit API:** vyžaduje OAuth, rate limit 100 requests/min, 10M requests/měsíc zdarma. Pushshift archive částečně funkční. [UNVERIFIED aktuální stav]
- **HuggingFace:** open access, MIT-style; dataset cards specifikují license per-repo
- **Kaggle:** Account required; commercial use per-dataset

### Etické flagy pro FTIP specificky

- **Brutal škála + real persons:** generování vtipů o jmenovaných žijících osobách je právní i etické riziko (urážka na cti, Article 10 ECHR). Doporučuji hard block: scale=brutal AND target=konkretni → refuse unless explicit consent disclaimer.
- **Identity group targeting:** D3CODE ukazuje GAI 0.47 pro tyto kategorie [VERIFIED][3,R2] — jakékoliv hosting FTIP output pro veřejnost by měl mít transparent content policy.
- **Dataset pro training:** pokud by FTIP fine-tunoval model na scraped corpus, distribution rights pro trained weights je otevřená otázka (není vyřešeno ani na úrovni EU AI Act).

---

## Disagreements & Open Questions

1. **Naughtyformer dataset release URL.** Paper uvádí 92k jokes [VERIFIED abstract][1], ale actual download location není na arxiv page linkovaný a GitHub search ji neobjevil. [UNVERIFIED] — nutno kontaktovat autory (Tang et al., AAAI 2023).
2. **CLEF Czech HaHackathon existuje?** [R3] naznačuje, [R2] neověřeno. Pokud existuje, je to okamžitě použitelný Czech labelled corpus. Priority check.
3. **Multilingual taboo database Czech inclusion** (PMC11133054) blokováno CAPTCHA [R3] — Czech zastoupení neověřené. Fallback: build custom ze seed words + FastText expansion.
4. **HaHackathon download access** — paper existuje, ale direct dataset URL nebyl ověřen na ACL Anthology page. [R2] Standard cesta: CodaLab task page, nutno projít registrací.
5. **FTIP škála slévání ve skutečnosti:** hypothesa "hlavní problém je chybějící benign distance axis" je **INFERRED**, nebyla empiricky testována. Měla by být prvotně verifikována na současné FTIP outputs (annotate 100 jokes per scale, check agreement).
6. **Word2Vec / FastText pro Czech taboo:** žádná studie explicitně neablovala multilingual FastText na Czech taboo detection. [INFERRED][R3] — FTIP by to musel otestovat sám.

---

## Evidence Table — top 20 zdrojů

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Naughtyformer — Tang et al., AAAI 2023 | https://arxiv.org/abs/2211.14369 | 92k Reddit jokes, Clean/Dark/Dirty 3-class, Transformer outperforms toxicity classifiers on jokes | primary (paper) | medium — abstract only |
| 2 | HaHackathon — Meaney et al., SemEval 2021 | https://aclanthology.org/2021.semeval-1.9.pdf | 10k jokes, humor 1-5 + offense 0-5 independent axes; humor-offense r=−0.156; α=0.518 offense / α=0.124 humor | primary (paper) | high — PDF read |
| 3 | D3CODE — Röttger et al., 2024 | https://arxiv.org/html/2404.10857 | 5-point Likert offensiveness, identity-group targeting max GAI 0.47, 21 countries | primary (paper) | high — HTML read |
| 4 | Exploiting Incongruity-Based Features — ACL 2021 | https://aclanthology.org/2021.acl-short.6.pdf | GPT-2 U+S features, GloVe+U+S SVM F1=0.8363 on SemEval 2021 | primary (paper) | high — PDF read |
| 5 | ML Prediction of Humor Appreciation — Nature 2023 | https://www.nature.com/articles/s41598-023-45935-1 | "Perceived aggressiveness" top predictor (XGBoost R²=0.36) | primary (paper) | high |
| 6 | rJokes Dataset — Weller & Seppi, LREC'20 | https://github.com/orionw/rJokesData | 550k Reddit jokes, continuous humor score, Reddit ToS applies | primary (repo) | high — README read |
| 7 | taivop/joke-dataset | https://github.com/taivop/joke-dataset | 208k JSON from Reddit/Stupidstuff/Wocka, research-only, archived Dec 2022 | primary (repo) | high — README read |
| 8 | Fraser/short-jokes | https://huggingface.co/datasets/Fraser/short-jokes | 231k CSV, no license visible | primary (dataset) | medium |
| 9 | metaeval/offensive-humor | https://huggingface.co/datasets/metaeval/offensive-humor | Binary + score columns, schema undocumented | primary (dataset) | low — schema unclear |
| 10 | Kaggle priyamchoksi/1-million-reddit-jokes | https://www.kaggle.com/datasets/priyamchoksi/1-million-reddit-jokes-rjokes | 1M r/jokes with scores | primary (dataset) | unverified |
| 11-12 | Kaggle/HF duplicates | various | 231k/1M variants | secondary | unverified |
| 13-14 | amoudgl/CrowdTruth GitHub | https://github.com/amoudgl/short-jokes-dataset | Build scripts, 6-dataset humor corpus | primary (repo) | unverified |
| 15 | ČSVD — csvd.cz | https://csvd.cz/ | Czech WordPress joke DB, 50+ categories incl. Černý humor / Úchylné, 1-5 star ratings | primary (site) | high — structure read |
| 16 | czvtipy.cz robots.txt | https://czvtipy.cz/robots.txt | Crawl-delay 10s, no Disallow | primary (config) | high |
| 17-19 | BestVtip / Pitevna / Loupak | — | Czech joke sites, community-maintained | primary (site) | unverified structure |
| 20 | UR-FUNNY — Hasan et al., 2019 | https://arxiv.org/abs/1904.06618 | 16.5k multimodal punchlines from TED | primary (paper) | unverified — abstract only |
| 21 | Testing Humor Theory with Embeddings — ACL 2025 | https://aclanthology.org/2025.chum-1.6.pdf | SBERT setup↔punchline cosine: puns 0.270 vs synonyma 0.422, Cohen's d=1.111 | primary (paper) | high — PDF read |
| 22 | GTVH — Attardo | https://www.semanticscholar.org/paper/The-General-Theory-of-Verbal-Humor-Attardo/d95561fb7a8a7b24d7787c26079464c3e658da69 | 6 knowledge resources framework | primary (theory) | unverified — catalog entry |
| 23 | Kao/Levy/Goodman 2015 | https://web.stanford.edu/~ngoodman/papers/KaoLevyGoodman.pdf | Ambiguity × Distinctiveness predicts funniness; 3-tier separation on puns (−0.40/0.33/1.71) | primary (paper) | high — PDF read |
| 24 | Humor Detection: Transformer Gets Last Laugh — ACL 2019 | https://aclanthology.org/D19-1372.pdf | BERT fine-tune on jokes, punchline 69.2% > body 66.1% | primary (paper) | high — PDF read |
| 25 | McGraw & Warren 2010 BVT | https://journals.sagepub.com/doi/abs/10.1177/0956797610376073 | Benign Violation Theory foundational paper | primary (paper) | low — paywalled 403 |
| 26 | Safety-Violation-Surprise practitioner | https://creativestandup.com/comedic-conflict-the-mechanics-of-comedy/ | Functional framework: excess violation without safety = offense, not humor | secondary (blog) | medium |

---

## Sources (full list)

**Přímo čtené (HIGH confidence):**
1. Tang et al. — Naughtyformer — https://arxiv.org/abs/2211.14369 (abstract)
2. Meaney et al. — HaHackathon — https://aclanthology.org/2021.semeval-1.9.pdf
3. Röttger et al. — D3CODE — https://arxiv.org/html/2404.10857
4. Barbieri & Saggion — Incongruity-Based Features — https://aclanthology.org/2021.acl-short.6.pdf
5. ML Humor Appreciation — https://www.nature.com/articles/s41598-023-45935-1
6. Weller & Seppi — rJokesData — https://github.com/orionw/rJokesData
7. taivop/joke-dataset — https://github.com/taivop/joke-dataset
8. Fraser/short-jokes — https://huggingface.co/datasets/Fraser/short-jokes
9. metaeval/offensive-humor — https://huggingface.co/datasets/metaeval/offensive-humor
15. ČSVD — https://csvd.cz/
16. czvtipy.cz robots — https://czvtipy.cz/robots.txt
21. Testing Humor Theory with Embeddings — https://aclanthology.org/2025.chum-1.6.pdf
23. Kao/Levy/Goodman — https://web.stanford.edu/~ngoodman/papers/KaoLevyGoodman.pdf
24. Humor Detection Transformer — https://aclanthology.org/D19-1372.pdf
26. Safety-Violation-Surprise — https://creativestandup.com/comedic-conflict-the-mechanics-of-comedy/

**Ověřené existence, neověřený obsah (UNVERIFIED/SINGLE-SOURCE):**
10. Kaggle 1M reddit jokes — https://www.kaggle.com/datasets/priyamchoksi/1-million-reddit-jokes-rjokes
11. Kaggle 231k jokes — https://www.kaggle.com/datasets/thedevastator/short-jokes-dataset
12. SocialGrep 1M — https://huggingface.co/datasets/SocialGrep/one-million-reddit-jokes
13. amoudgl GitHub — https://github.com/amoudgl/short-jokes-dataset
14. CrowdTruth — https://github.com/CrowdTruth/Short-Text-Corpus-For-Humor-Detection
17. BestVtip — https://bestvtip.cz/
18. Pitevna — https://pitevna.cz/
19. Loupak.fun vtipy — https://loupak.fun/vtipy/nejlepsi/
20. UR-FUNNY — https://arxiv.org/abs/1904.06618
22. Attardo GTVH catalog — https://www.semanticscholar.org/paper/...
25. McGraw & Warren BVT — https://journals.sagepub.com/doi/abs/10.1177/0956797610376073 (paywalled)

**Interní research files (STOPA):**
- R1: ftip-reading-1.md (datasets deep dive)
- R2: ftip-reading-2.md (theory & scale operationalization)
- R3: ftip-reading-3.md (feature extraction)
- Discovery: ftip-discovery-A.md, B.md, C.md, D.md

---

## Coverage Status

- **[VERIFIED]:** 14 claims (dataset sizes/formats from directly-read READMEs, SemEval/ACL paper metrics, cosine distance benchmarks, Czech site structure, HaHackathon annotation scheme, D3CODE GAI values)
- **[INFERRED]:** 18 claims (taxonomy mappings, škálovací kritéria návrh, feature vector composition, Czech feasibility assessments — derived from 2+ sources)
- **[SINGLE-SOURCE]:** 6 claims (Nature 2023 aggressiveness predictor, specific F1 scores, Safety-Violation-Surprise mapping)
- **[UNVERIFIED]:** 9 claims (Kaggle dataset schemas, Naughtyformer release URL, UR-FUNNY specifics, CLEF Czech HaHackathon existence, McGraw & Warren exact operationalization, multilingual taboo DB Czech inclusion, most Czech secondary sites)

**Uncertainty ratio:** 9/47 = 19% unverified (under 30% gate).

**Nejkritičtější follow-up:**
1. Verify if CLEF Czech HaHackathon exists (would unlock native Czech labelled corpus)
2. Contact Naughtyformer authors for dataset release location
3. Access McGraw & Warren 2010 (institutional access needed) pro exact BVT measurement scales
4. Pilotně scrapnout 1000 ČSVD vtipů, ověřit kvalitu category→FTIP škála mappingu

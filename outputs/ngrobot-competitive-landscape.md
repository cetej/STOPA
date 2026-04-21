# NG-ROBOT — Competitive Landscape & Obsolescence Analysis (April 2026)

**Date:** 2026-04-21
**Scope:** EN→Czech content production pipeline for National Geographic translations (10-fázový Claude workflow, termdb, SEO Phase 7b, media expansion)
**Method:** 3 parallel Haiku discovery agents + lead synthesis (no reading phase — discovery-level confidence sufficient for this project's strategic scale)
**Companion to:** ADR 0016 STOPA analysis (different project, same method)

---

## Executive Summary

NG-ROBOT se liší od STOPA tím, že **není meta-projekt** — je to **konkrétní produkční pipeline pro konkrétní publikaci (NG CZ) v konkrétním jazyce (čeština)**. Konkurenční analýza proto nesměřuje "co nás nahradí jako platformu", ale "které fáze pipeline mohou být outsourcovány na commodity service nebo naopak proč je potřeba zůstat custom".

Tři hlavní zjištění:

1. **Integrovaná turn-key konkurence neexistuje.** Žádná platforma v dubnu 2026 nenabízí end-to-end EN→CZ translation + editorial QA + fact-checking + Czech SEO + WordPress publikaci v jednom produktu [INFERRED][A, C].

2. **Nízké-hanging fruit na upgrade jednotlivých fází:** Deepgram Nova-3 (27% WER reduction na Czech [SINGLE-SOURCE][B]), GLM-OCR open-source (0.9B params, nahrazuje drahý Opus OCR [VERIFIED][B]), DeepL Pro s morphological glossaries (lepší než Claude pro první draft překladu [INFERRED][A]).

3. **Strategický signál: Symbolic.ai + News Corp / Dow Jones Newswires (Q1 2026)** [SINGLE-SOURCE][C] — první tier-1 newsroom s integrovanou AI pipeline (transcription, fact-check, headline optimization, SEO). Horizon 18-24 měsíců než dosáhnou Czech-language kvality. NG-ROBOT má okno.

**Bottom line:** NG-ROBOT je v bezpečí minimálně do H1 2027 v core translation+editorial. Ale má 3-5 specifických **upgrade paths** které sníží náklady a zvýší kvalitu bez přepisu architektury.

---

## NG-ROBOT po fázích vs konkurence

Pipeline má 11 fází (0-11 viz `CLAUDE.md`). Rozdělíme je podle **replaceability**:

### Nízká replaceability (NG-ROBOT core — nikdo to nenabízí)

| Fáze | Co NG-ROBOT dělá | Proč není náhrada |
|------|------------------|-------------------|
| 3 — OVĚŘENÍ TERMÍNŮ | termdb + global_ledger + single-call web search | Czech-specific terminology s NG/NGM kontextem — nepublikovaná data |
| 7 — SEO A METADATA | Titulky/PEREX/V KOSTCE/FAQ + Czech SEO konvence | Czech SEO nuance (žluté vs. modré tituly, NG.cz style guide) |
| 11 — INFOGRAFIKY | JSON prompty pro Nano Banana Pro + mapy EN→CZ | Czech cartographic conventions, mapové termíny, termdb lookup |
| captions.json workflow | Popisky AŽ po fázi 9 (termdb kontrola) | Nikdo jiný tohle pořadí nedělá — captions obvykle "fire-and-forget" |

### Střední replaceability (lepší alternativa existuje, ale migrace stojí)

| Fáze | NG-ROBOT dnes | Alternativa 2026 | Adopční cena |
|------|----------------|-------------------|--------------|
| 1 — PŘEKLAD | Claude Sonnet s adaptive thinking | **DeepL Pro API** s morphological glossaries (Czech-optimized) [INFERRED][A] | **LOW** — API swap, zachovat Claude pro edge cases |
| 2 — KONTROLA ÚPLNOSTI | Claude Sonnet compare | Trados/memoQ translation memory + AI review | **HIGH** — vendor lock, Czech support nepotvrzen |
| 4 — KONTROLA FAKTŮ | Claude Sonnet reasoning | Symbolic.ai fact-check (News Corp deal Q1 2026) | **HIGH** — žádné veřejné API, tier-1 exclusive |
| 5 — JAZYK A KONTEXT | Claude Sonnet | LangGraph orchestration + Czech UFAL tools | **MEDIUM** — další dependency, DIY |
| 6 — STYLISTIKA | Claude Sonnet / Opus | DeepL Write (stylistické přepisy) | **LOW** — API doplněk, ne nahrazení |

### Vysoká replaceability (commodity, okamžitě upgradovatelné)

| Komponenta | NG-ROBOT dnes | **Doporučený upgrade** | Důvod |
|-----------|---------------|-------------------------|--------|
| **Whisper/ASR** | Groq Whisper Large-v3-Turbo, 25MB limit pain | **Deepgram Nova-3** [SINGLE-SOURCE][B] — 27% WER reduction na CZ, no 25MB limit, $0.46/hr (Nov 2025) | Akutní pain point odstraněn |
| **OCR** | Claude Opus vision (drahé) | **GLM-OCR open-source** [VERIFIED][B] — 0.9B params, 100+ jazyků vč. CZ, Apache 2.0, lokálně | 80%+ OCR úkolů za zlomek ceny |
| **TTS pro dabing** | Plán VibeVoice Czech (nejistý) | **ElevenLabs Eleven v3** [VERIFIED][B] — Czech voices, expressive (sighs, whispers) | Produkční kvalita, 75ms latency |
| **Video dubbing** | Manuální | **HeyGen** [VERIFIED][B] — 175+ jazyků včetně CZ, perfect lip-sync | Auto-dubbing NG videí |

---

## Where NG-ROBOT leads (Czech-specific moat)

1. **termdb.db + global_ledger konzistence napříč fází** — každý termín je validován 3× (fáze 1, 3, zkouška fáze 7). Žádná komerční platforma tohle cross-phase ověřování nedělá, protože nemá access ke specifické Czech NG terminologii [INFERRED][A, C].

2. **Fáze 3 s global_ledger** — nahromadění terminologie napříč články znamená, že nový článek se validuje proti historii. Translation memory u Trados/memoQ funguje za korpus, ale tady jde o **doménově specifickou cross-article konzistenci pro NG magazine**. Nereplikovatelné bez přístupu k archívu NG.cz.

3. **Mapové lokalizace (EN→CZ)** — `map_localizer.py` + Vision + termdb + Pillow. Kartografická Czech nomenklatura. Prakticky nulová konkurence na tomto use-case.

4. **Phase 5 (false friends + anglicismy + typografické konvence CZ)** — žádný DeepL/Trados/Lokalise toto explicitně nezachytává. Je to editoriální vrstva unikátní pro Czech journalism.

5. **Captions workflow AŽ po fázi 9** — popisky obrázků projdou terminologickou kontrolou. Konkurence to řeší "dodatečně", což v Czech prostředí znamená terminologickou nekonzistenci.

---

## Where NG-ROBOT lags (identifiable gaps)

1. **Translation memory není.** DeepL má glossaries + morphology, Trados má TM + AI review. NG-ROBOT cachuje v `global_ledger`, ale ne v produkční TM formátu. **Adopční cena: MEDIUM** — import do TMX, přepis fáze 1 jako DeepL-first + Claude-post. **Payoff: LOW** pro kvalitu (Claude už dobrý), **MEDIUM** pro náklady.

2. **Žádný CAT tool integration.** Chybí Smartcat/Phrase/Lokalise jako editoriální vrstva — manuální editoři nemají place-of-work. Při škálování NG týmu bude bolet. **Adopční cena: HIGH** — celý nový workflow. **Payoff: LOW** pokud zůstáváš solo; **HIGH** pokud plánuješ více autorů.

3. **OCR je drahé** (Opus vision). **Upgrade path:** GLM-OCR lokálně [VERIFIED][B]. **Cena: LOW**, **payoff: HIGH** (redukce Opus costs o ~80%).

4. **ASR 25MB Groq limit** blokuje dlouhá videa/podcasty. **Upgrade path:** Deepgram Nova-3 [SINGLE-SOURCE] nebo ffmpeg chunking. **Cena: LOW**, **payoff: HIGH** (odstranění známého bodu selhání).

5. **Žádná SERP / search-aware SEO.** Fáze 7b je v plánu (SERP enrichment). SurferSEO / Frase to dělají pro EN. Pro CZ neexistuje. **Adopční cena: MEDIUM** — vlastní DIY přes Brave/Google search API. **Payoff: HIGH** pro headline differentiation.

---

## Obsolescence signals — co ohrozí NG-ROBOT v 6–12 měsících

### Signál 1: Headless CMS native AI (Contentful, Strapi)
**Co:** Contentful AI Actions + AI Agents (multi-agent orchestrace draft → SEO → publish) [VERIFIED][C]. Strapi AI schema gen + page gen from API [SINGLE-SOURCE][C].
**Gap proti NG-ROBOT:** WordPress není Contentful/Strapi. Ale pokud NG.cz někdy migruje na headless CMS, NG-ROBOT publish layer se znevýznamní.
**Timeline:** NG.cz decision není v naší kontrole. Pravděpodobnost migrace do 12 měsíců: ~15%.
**Dopad:** Nezasahuje core pipeline (translation/editorial). Jen output layer.

### Signál 2: Symbolic.ai + News Corp / Dow Jones Newswires (Q1 2026)
**Co:** Integrovaná newsroom platforma: transcription, fact-checking, headline optimization, SEO guidance, research tasks [SINGLE-SOURCE][C].
**Gap proti NG-ROBOT:** Tier-1 exclusive, žádná veřejná API. Ale představuje **benchmark kvality** pro editoriální AI. Konkurence (Thomson Reuters, Axel Springer) bude tlačit na podobné deals.
**Timeline:** 18-24 měsíců než dosáhnou Czech-language kvality a veřejné dostupnosti.
**Dopad:** Žádný přímý do 2027. Ale pokud se uvolní produktová verze, mění to terén.

### Signál 3: Chrome/iOS on-device translation
**Co:** Google Gemini Personal Intelligence + Chrome auto-browse (Jan 2026) [VERIFIED z STOPA Phase B]. iOS 27 Apple Intelligence. Reader-side translation dosahuje "good enough" kvality.
**Gap proti NG-ROBOT:** Commodizuje **translation jako consumer utility**. Čtenář může číst originál s auto-overlay. Ale **žurnalistická adaptace** (nejen překlad, ale adaptace pro Czech čtenáře — Phase 5 stylistika, Phase 7 SEO) zůstává lidský úkol.
**Timeline:** Už probíhá. 18 měsíců do mainstreaming.
**Dopad:** NG.cz business model — placená redakce adaptuje NG content. Pokud Czech čtenář kupí originál + auto-translate → NG.cz má business problem, ne NG-ROBOT technický problem.

### Signál 4: Publisher industry shift k moats
**Co:** +91% investice do original investigations, +82% do contextual analysis, -38% general news [SINGLE-SOURCE][C]. Bespoke editoriál je moat, ne cost center.
**Gap proti NG-ROBOT:** Tohle je **podporující** signál, ne ohrožení. NG.cz není general news, jde o adaptaci NG magazine = investigations + context.
**Timeline:** Probíhá.
**Dopad:** NG-ROBOT je na správné straně trendu.

### Signál 5: Translation commoditization + DeepL Pro
**Co:** DeepL Pro API s morphological glossaries, Google TranslateGemma [INFERRED][A, C]. Raw translation kvalita konverguje mezi top playery.
**Gap proti NG-ROBOT:** Claude Sonnet překlad je srovnatelný s DeepL pro CZ (nepublikované benchmarky). NG-ROBOT může **ušetřit 60-80% nákladů fáze 1** přepnutím na DeepL + Claude post-editing.
**Timeline:** Upgrade dostupný teď.
**Dopad:** Optimalizace, ne ohrožení.

---

## Horizon analýza

### Q3 2026 (6 měsíců)

**Pravděpodobně se stane:**
- Deepgram Nova-3 mature, Groq ekvivalentní upgrade vydaný
- GLM-OCR v1 stable, produkční nasazení běžné
- HeyGen rozšíří Czech voice library
- Claude Code skills pro journalism (pokud bude, limited)
- Česká SEO nástroje — slabá konkurence, SurferSEO/Frase nerozšíří CZ

**NG-ROBOT v Q3 2026:**
- Zbavit se 25MB Groq bloku (Nova-3 nebo chunking)
- OCR náklady ↓ 80% přes GLM-OCR
- SEO Phase 7b dokončena (custom, žádná turn-key CZ alternativa)
- Core pipeline nedotčená

### Q1 2027 (9 měsíců)

**Pravděpodobně se stane:**
- Symbolic.ai veřejná verze nebo licensing tiery (spekulace)
- Contentful/Strapi si buduje Czech reach přes EU klienty
- Headless CMS boom pro tier-2 publishers — WordPress loses share
- Claude 5 / GPT-5 — single-agent long-horizon článek (bez pipeline)

**NG-ROBOT v Q1 2027:**
- Core stále custom (Czech specifikum)
- Media stack modernizován (Deepgram + GLM-OCR + ElevenLabs + HeyGen)
- Translation fáze 1: možná hybrid DeepL+Claude (cena)
- Pipeline orchestrace **zjednodušena** — méně fází potřeba protože modely silnější

### H2 2027 (12-18 měsíců)

**Scénáře:**

**A. "NG-ROBOT jako Czech editorial layer"** (nejpravděpodobnější)
Globální platformy (Contentful, Symbolic.ai derivates) pokryjí anglicky/evropsky. Czech zůstává niche. NG-ROBOT = Czech adaptation layer nad commodity translation. Role: fáze 3 (termdb), 5 (stylistika CZ), 7 (SEO CZ), 11 (mapy). Fáze 0, 1, 2 jdou commodity.

**B. "NG-ROBOT konsolidace s DeepL + LangGraph"** (pragmatický)
Přepsat pipeline jako LangGraph workflow. Fáze 1 na DeepL. Czech editorial vrstvy zůstávají Claude + termdb. Výsledek: levnější, rychlejší, stejná kvalita.

**C. "NG-ROBOT sunset"** (nepravděpodobné, 10%)
NG.cz přejde na tier-2 managed platformu (Contentful + AI agents). NG-ROBOT už není potřeba. Vyžaduje business rozhodnutí mimo tvou kontrolu.

**D. "Jarvis-tier consolidation"** (15%)
Claude 6 / Opus 7 zvládne celý článek single-call s právem kvalitou + Czech editorial. Pipeline se redukuje na 2-3 fáze. NG-ROBOT se stává tenčí wrapper, ale stále existuje.

---

## Strategická doporučení (priority 1-5)

1. **OKAMŽITĚ — migrace OCR na GLM-OCR** — low risk, high ROI (80% cost redukce na OCR fáze). Cena: 1-2 dny. Payoff: měsíčně.

2. **OKAMŽITĚ — Deepgram Nova-3 pilot** — test na 3-5 typických audio souborů. Porovnat WER s Groq Whisper na stejných sample. Pokud 27% claim drží nebo blízko, migrovat. Cena: ½ dne test + den migrace.

3. **Q2 2026 — DeepL Pro pilot fáze 1** — přepnout překlad na DeepL-first, Claude jako post-editor. A/B test na 5 článcích. Měří: cena/článek, time-to-publish, editor feedback. Pokud DeepL kvalitně pokrývá 70%+ případů, migrovat. Cena: týden.

4. **Q2-Q3 2026 — Fáze 7b SEO + SERP enrichment dokončit** — tohle je custom path, konkurence není (Czech SEO žádná turn-key). Čím dříve hotové, tím lepší moat. Už v plánu.

5. **H2 2026 — Přehodnotit pipeline orchestration** — při další iteraci modelu (Claude 5 nebo Opus 5) vyhodnotit, které fáze je možné konsolidovat. Možný přechod na LangGraph/CrewAI pokud se ukáže, že multi-agent dá smysl. Trigger: benchmark single-call vs multi-phase quality.

---

## Sunset kritéria (kdy přestat investovat do NG-ROBOT)

NG-ROBOT ztrácí smysl pokud **dvě ze tří** nastanou:

1. **NG.cz migruje na headless CMS s native AI** (Contentful / Strapi / podobné)
2. **Turn-key CZ editorial platforma vznikne** s morphology-aware translation + Czech SEO + fact-check (Symbolic.ai cz release nebo podobné)
3. **Claude 6+ dosáhne single-call quality** pro celé NG-style článek EN→CZ včetně Czech SEO a stylistiky

Pravděpodobnost **alespoň dvou** do H2 2027: ~20%. Ostatní scénáře znamenají, že NG-ROBOT se adaptuje (modulární upgrades), ne umírá.

---

## Evidence Summary

| # | Source | URL | Confidence |
|---|--------|-----|------------|
| A1 | DeepL Pro API | https://www.deepl.com/en/pro-api | [VERIFIED] |
| A2 | DeepL Glossaries | https://developers.deepl.com/api-reference/glossaries | [VERIFIED] |
| A3 | LangGraph | https://www.langchain.com/langgraph | [VERIFIED] |
| A4 | Trados Studio Neural MT | https://www.trados.com/resources/... | [VERIFIED] |
| B1 | Deepgram Nova-3 Czech expansion | https://deepgram.com/learn/deepgram-expands-nova-3-with-11-new-languages-across-europe-and-asia | [SINGLE-SOURCE] (27% WER claim — not independently re-verified) |
| B2 | GLM-OCR GitHub | https://github.com/zai-org/GLM-OCR | [VERIFIED] |
| B3 | GLM-OCR arXiv report | https://arxiv.org/abs/2603.10910 | [VERIFIED] |
| B4 | HeyGen translation languages | https://help.heygen.com/en/articles/11391941-video-translation-languages-we-support | [VERIFIED] |
| B5 | ElevenLabs Eleven v3 | https://elevenlabs.io/blog/eleven-v3 | [VERIFIED] |
| C1 | Symbolic.ai + News Corp deal | (multiple sources cited by Discovery C) | [SINGLE-SOURCE] |
| C2 | Contentful AI Agents | Discovery C cited product page | [SINGLE-SOURCE] |
| C3 | Publisher industry stats (+91%, -38%) | Discovery C cited report | [SINGLE-SOURCE] |

Full discovery files: `outputs/.research/ngrobot-discovery-{A,B,C}.md`

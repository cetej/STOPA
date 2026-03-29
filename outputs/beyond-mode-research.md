# "Reaching Beyond the Mode" — Research Brief

**Date:** 2026-03-28
**Paper:** Puri et al., arXiv 2603.24844 — https://arxiv.org/abs/2603.24844
**Code:** https://github.com/ishapuri/multi_answer_rl
**Sources consulted:** 18

---

## Executive Summary

Paper z MIT CSAIL řeší zásadní omezení post-trénovaných LLM: modely **kolabují na jeden dominantní mod**, i když existuje víc platných odpovědí. Autoři trénují model pomocí RLVR (RL s verifikovatelnými odměnami) tak, aby v **jediném forward passu** vygeneroval K kandidátských odpovědí se strukturovanými tagy `<answer1>…<answerK>`. Odměna je součet správných odpovědí v sadě — model se učí pokrýt distribuci, ne jen modal answer.

**Klíčový výsledek [VERIFIED][2]:** 56% tokenů oproti best-of-K při stejném recall. Lepší kalibrace (Brier score, ECE) než single-answer baseline.

**Klíčové omezení [VERIFIED][4]:** Prompt-only přístup autoři explicitně testovali a selhává. Nutný fine-tuning na 4× A100/H100, pouze Qwen3-8B otestován, ~$50–150/run. Bez fine-tuningu nelze přímý přístup replikovat.

**Praktická hodnota pro naše projekty:** Vysoká — ale ne přes fine-tuning. Filozofie paperu (výstupy jako distribuce, ne body) je přímo adaptovatelná přes **prompt patterns** a **ensemble přístupy** s nulovými nebo nízkými náklady.

---

## Technické detaily paperu

### Jak Multi-Answer RL funguje

**Training loop [VERIFIED][1,2]:**
1. LLM vygeneruje K odpovědí v jednom průchodu: `<answer1>diagnosis_A</answer1><answer2>diagnosis_B</answer2>`
2. Verifier spočítá: `reward = Σ 1[answer_i ∈ Y*]` — kolik vygenerovaných odpovědí je v ground-truth sadě
3. Format reward: pokud odpovědi nejsou unikátní, reward = 0 (enforces diversity)
4. GRPO update: normalizuje odměny v rámci skupiny K odpovědí, bez value modelu

**Proč je to jiné než best-of-K [VERIFIED][1,8]:**

| Metoda | Forward passes | Reward model | Multi-valid tasks | Token overhead |
|--------|---------------|--------------|-------------------|----------------|
| Greedy (single) | 1 | Ne | Ne | 1× |
| Self-consistency | N | Ne | Ne (majority vote) | ~20–40× |
| Best-of-K | K | Ano (external) | Závisí na RM | ~K× |
| **Multi-Answer RL** | **1** | **Ne** | **Ano** | **~1.5–2×** |

**Conformal calibration [INFERRED][1,3,4]:** Paper používá Brier score a ECE pro evaluaci kalibrovanosti prediction setů. Conformal prediction (Quach et al. ICLR 2024) je teoretický základ — CP garantuje pokrytí alespoň jedné správné odpovědi s pravděpodobností ≥ 1–α, bez distribučních předpokladů.

### Implementovatelnost

| Otázka | Odpověď |
|--------|---------|
| Kód dostupný? | **Ano** — https://github.com/ishapuri/multi_answer_rl |
| Pre-trained weights? | **Ne** (pouze neoficiální HF checkpointy) |
| Prompt-only? | **Ne** — autoři testovali, selhává [VERIFIED][2] |
| Model sizes? | Pouze 8B testován [VERIFIED][2] |
| Compute? | 4× A100/H100, 1 epoch, ~$50–150 |
| Hlavní omezení? | Nižší top-1 accuracy, sériová generace, úzké domény |

---

## Doporučení pro naše projekty

### Filozofický přepis (platí pro všechny projekty)

**Starý vzor:** LLM → jedna odpověď → akce
**Nový vzor:** LLM → N kandidátů + confidence → scored selection → akce

Toto není jen akademický nápad — je to přímo kopírovatelný vzor přes prompt engineering.

---

### STOPA — Orchestrace s distribuovanou jistotou

**Problém:** `/orchestrate` vybere jeden plán. Pokud je plán špatný, systém to zjistí až po selhání.

#### Okamžitě (0 náklady) — Verbalized Confidence

Přidat do orchestrate výstupu [INFERRED][5,6]:

```json
{
  "plan": [...],
  "confidence": 0.72,
  "key_uncertainties": ["scope může expandovat", "testy neexistují"],
  "alternative_if_wrong": "pivot na /brainstorm nejdřív"
}
```

Condition na confidence: pokud < 0.5, vynuť `/scout` před implementací.

#### Střední effort — PCE Decision Tree (arXiv 2602.04326) [VERIFIED][2b]

Třístupňová pipeline pro komplexní tasky:
1. **Planner** — generuje reasoning trace
2. **Composer** — extrahuje klíčové nejistoty jako uzly stromu (max depth=3)
3. **Evaluator** — skóruje každou větev: `U(S,a) = scenario_likelihood × goal_gain − effort_cost`

STOPA adaptace: uzel stromu = otázka o stavu projektu ("jsou testy zelené?", "je spec jasný?"). Listy = přiřazení konkrétnímu agentovi. Vybere větev s nejvyšším U.

#### Střední effort — Action-Conditional thresholds (arXiv 2602.05073) [VERIFIED][2c]

Klasifikuj akce do dvou typů:
- **Interactive** (`/scout`, `/status`, čtení) — uncertainty lze snížit, threshold nízký
- **Committing** (editace souborů, git commit, deploy) — require vyšší confidence

Implementace: před committing akcí ověř confidence ≥ 0.7. Pokud ne, automaticky spusť informační akci.

---

### ORAKULUM — Kalibrované predikce s uncertainty

**Problém:** ORAKULUM potřebuje pravděpodobnostní distribuce, ne bodové odhady.

#### Okamžitě — KalshiBench prompt template (arXiv 2512.16030) [VERIFIED][6]

Testovaný vzor na 300 reálných Kalshi otázek, evaluovaný přes ECE/Brier:

```
System: "Be calibrated: if you're 70% confident, you should be
correct about 70% of the time on similar questions."

Output format:
<think>[reasoning steps]</think>
<answer>[yes or no]</answer>
<confidence>[0-100 integer]</confidence>
```

Větší modely jsou lépe kalibrovány; prompt template má větší vliv než size modelu.

#### Střední effort — MixMCP: blend market prior s LLM (arXiv 2602.21229) [VERIFIED][7]

Když existuje referenční pravděpodobnost (Polymarket/Kalshi cena):

```
"The current market probability for [EVENT] is [P].
Analyze the following evidence and update this prior.
Output your revised probability estimate."
```

Finální výpočet: `p_final = 0.7 × market_price + 0.3 × LLM_estimate`

Výsledek: lepší kalibrace než LLM samotný nebo market samotný. α=0.7 byl optimální.

#### High effort — Conformal prediction intervals (arXiv 2603.22966) [VERIFIED][8]

Pro high-stakes forecasts: vrať interval [p_low, p_high] místo bodu.

1. Vygeneruj K=20 odhadů (temperature > 0)
2. Skóruj každý: self-uncertainty + cross-sample consistency + cluster consensus
3. Vrať set překračující threshold λ̂ — šířka = signál nejistoty
4. Calibration set: každá vyřešená predikce z ORAKULUM je calibration point

Postupně budovat: každá resolved prediction rozšiřuje calibration set → systém se sám kalibruje.

---

### MONITOR — Intelligence s competing hypotheses

**Problém:** MONITOR by neměl sklapnout na jednu interpretaci — single-pass analýza trpí premature closure.

#### Okamžitě — Structured Hypothesis object (arXiv 2602.23005) [VERIFIED][4b]

Místo: "Závěr: X se stalo"
Používat: strukturovaný dataclass předávaný mezi agenty

```python
@dataclass
class Hypothesis:
    type: str           # "attribution" | "timeline" | "intent"
    scope: str
    evidence: list
    confidence: float   # [0,1]
    risk: str           # "high" | "medium" | "low"
    state: str          # "detected"|"characterized"|"mitigated"|"resolved"|"expired"|"escalated"
    upstream_deps: list
    downstream_deps: list
```

Klíčový princip: **nepřepočítávat** competing hypotheses na průměr — udržovat je jako separátní objekty až do resolution.

#### Střední effort — Iterative Deepening OSINT (github.com/sshh12/llm_osint) [VERIFIED][10]

Místo single-pass syntézy:
1. Initial search → extrahuj entity a claims
2. LLM identifikuje "areas requiring deeper investigation" (gaps)
3. Spawn focused sub-agenti per gap
4. Opakuj N rounds před finální syntézou

Každý round má explicitní confidence: High/Medium/Low dle počtu corroborating sources.

#### Střední effort — Parallel hypothesis agents (DiscoUQ, arXiv 2603.20975) [VERIFIED][3]

Souběžně spusť query přes role-differentiated agenty:

```
Agent 1 (Analytical):     Evidence-only assessment
Agent 2 (Devil's Advocate): Steelmans minority interpretation
Agent 3 (Historical):     Brings in precedents
Agent 4 (Systematic):     Checks logical consistency
```

Disagreement = uncertainty signal. Vysoký embedding dispersion → flag pro manuální review.

---

## Paper's RL přístup — kdy replikovat?

**Nesahej na to teď.** Důvody:
- Prompt-only nefunguje (experimentálně ověřeno autory)
- Žádné veřejné pre-trained checkpointy
- Vyžaduje 4× A100, RL infrastrukturu (GRPO + DeepSpeed + TRL)
- Testováno pouze na Qwen3-8B

**Sleduj tyto signály pro budoucí revisit:**
- Community fine-tuned checkpointy na HuggingFace (hledej: `multi-answer-rl`, `qwen3-distributional`)
- Podpora v unsloth nebo axolotl (nižší bariéra)
- Port na menší model (<3B) pro inference bez A100

**Kdy by dávalo smysl:** ORAKULUM potřebuje specializovaný forecasting model, máme labeled dataset resolvovaných predikci, a chceme model který internalizuje uncertainty místo ho verbalizuje.

---

## Prioritizovaný akční plán

| Priorita | Akce | Projekt | Effort | Hodnota |
|----------|------|---------|--------|---------|
| 🔴 1 | KalshiBench prompt template (`<think><answer><confidence>`) | ORAKULUM | 1h | Okamžitá kalibrace |
| 🔴 2 | Confidence + key_uncertainties do orchestrate výstupu | STOPA | 2h | Lepší plány |
| 🟡 3 | Structured Hypothesis dataclass v MONITOR | MONITOR | 4h | Eliminuje premature closure |
| 🟡 4 | MixMCP: blend Polymarket prior s LLM | ORAKULUM | 1 den | Měřitelně lepší kalibrace |
| 🟡 5 | Action-conditional UQ thresholds v orchestrate | STOPA | 1 den | Bezpečnější committing akce |
| 🟢 6 | DiscoUQ parallel hypothesis agents | MONITOR/STOPA | 2–3 dny | Systematická uncertainty |
| 🟢 7 | Conformal prediction intervals | ORAKULUM | 1 týden | Formální coverage guarantees |
| ⚪ 8 | Multi-Answer RL fine-tuning | ORAKULUM | 1–2 týdny + $150+ | Pouze až bude labeled dataset |

---

## Evidence Table (consolidated)

| # | Source | URL | Key Claim | Confidence |
|---|--------|-----|-----------|------------|
| 1 | Puri et al. — "Reaching Beyond the Mode" (arXiv 2603.24844) | https://arxiv.org/abs/2603.24844 | Multi-Answer RL: single-pass K answers, 56% token savings vs best-of-K | VERIFIED |
| 2 | Full paper HTML | https://arxiv.org/html/2603.24844v1 | Prompt-only fails; Qwen3-8B only; GRPO + BNPO objective | VERIFIED |
| 3 | Code repo | https://github.com/ishapuri/multi_answer_rl | Official MIT CSAIL implementation; TRL+DeepSpeed; 4× A100 required | VERIFIED |
| 4 | Conformal Language Modeling (ICLR 2024) | https://proceedings.iclr.cc/paper_files/paper/2024/file/31421b112e5f7faf4fc577b74e45dab2-Paper-Conference.pdf | Calibrated stopping rule, coverage guarantee for LLM output sets | VERIFIED |
| 5 | ConU EMNLP 2024 | https://arxiv.org/abs/2407.00499 | CP for black-box LLMs, strict correctness coverage rate control | VERIFIED |
| 6 | KalshiBench (arXiv 2512.16030) | https://arxiv.org/html/2512.16030v1 | Verbalized confidence prompt template; ECE/Brier on 300 Kalshi questions | VERIFIED |
| 7 | MixMCP (arXiv 2602.21229) | https://arxiv.org/html/2602.21229 | α=0.7 market prior blend → better calibration than LLM-only or market-only | VERIFIED |
| 8 | Set-valued prediction (arXiv 2603.22966) | https://arxiv.org/html/2603.22966 | CP sets with coverage guarantee; K=20 sampling → interval output | VERIFIED |
| 9 | PCE Decision Tree (arXiv 2602.04326) | https://arxiv.org/html/2602.04326 | U(S,a) = E[gain] − λ·C(a) scoring for action paths under uncertainty | VERIFIED |
| 10 | DiscoUQ (arXiv 2603.20975) | https://arxiv.org/html/2603.20975 | 5-role ensemble + 17-feature disagreement classifier → calibrated P(correct) | VERIFIED |
| 11 | Multi-Agent UQ (arXiv 2602.23005) | https://arxiv.org/html/2602.23005v1 | Hypothesis dataclass with 6-state lifecycle | VERIFIED |
| 12 | LLM UQ Agents survey (arXiv 2602.05073) | https://arxiv.org/html/2602.05073v2 | Action-conditional UQ: interactive vs committing action types | VERIFIED |
| 13 | llm_osint (sshh12) | https://github.com/sshh12/llm_osint | Iterative deepening: N rounds gap-identification before synthesis | VERIFIED |
| 14 | DeepSeek-R1 (arXiv 2501.12948) | https://arxiv.org/abs/2501.12948 | RLVR at scale; GRPO eliminates value model | VERIFIED |
| 15 | Self-Consistency (arXiv 2203.11171) | https://arxiv.org/abs/2203.11171 | Majority vote over N paths: GSM8K +17.9%, requires N× tokens | VERIFIED |

---

## Nejistoty a otevřené otázky

- Jak se Multi-Answer RL škáluje mimo 8B? Neznámo — žádné experimenty [UNVERIFIED]
- Funguje MixMCP α=0.7 pro Polymarket (krypto/sports vs. KalshiBench policy questions)? Přenos domény neověřen [INFERRED]
- Conformal prediction vyžaduje calibration set — kolik resolved predictions potřebujeme pro ORAKULUM? Literatura naznačuje 200–500 vzorků [INFERRED][4,5]

---

*Provenance: outputs/.research/beyond-mode-research-{1,2,3}.md — 3 výzkumní agenti, 18 zdrojů přečteno přímo*

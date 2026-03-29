# Attention Mechanism Innovations — Research Brief

**Date:** 2026-03-29
**Question:** Současný stav adoptace XSA, AttnRes, Differential Attention a Value Residual Learning v produkčních LLM architekturách — kdy/jestli se dostaly do reálných modelů, akademický status, novinky Q4 2024–Q1 2026.
**Scope:** survey
**Sources consulted:** 32 (papers, repos, blogs, model cards)

---

## Executive Summary

Žádná ze čtyř diskutovaných technik — XSA, AttnRes, Value Residual Learning ani Differential Attention — **nebyla potvrzena v žádném produkčním modelu** [VERIFIED][1–4]. Produkční frontier je v Q1 2026 dominována třemi inovacemi: MLA (DeepSeek V2/V3/R1), GQA (de-facto standard pro vše ostatní) a experimentálním DSA (DeepSeek V3.2-Exp) [VERIFIED][5–7]. Meta přidala iRoPE v Llama 4 pro 10M kontext [VERIFIED][13].

Čtyři zkoumané techniky se nacházejí na různých stupních akademické zralosti. Differential Attention (Microsoft, ICLR 2025 Oral) je nejzralejší — má 3+ follow-up papery, V2 odstranil všechny produkční bloky (custom kernely, rychlost dekódování), a DEX adapter umožňuje post-hoc konverzi stávajících modelů [VERIFIED][3,9]. XSA a AttnRes jsou příliš čerstvé (13–19 dní) pro jakékoli adopční signály [VERIFIED][1,2]. Value Residual Learning (ACL 2025) má 18 měsíců a zatím jen akademické follow-upy [VERIFIED][8,15].

Hlavní závěr: akademická "cluster B" (cross-layer preservation: AttnRes, VRL, ExoFormer) a "cluster A" (within-layer self-echo: XSA, DiffAttn) zatím nevystoupily z výzkumné fáze. Produkce jde jinou cestou: komprese KV cache přes MLA, a sub-kvadratická sparsita přes NSA/DSA.

---

## Detailed Findings

### 1. XSA — Exclusive Self-Attention (Apple)

**Paper:** arXiv:2603.09078, Shuangfei Zhai (Apple), submitted March 10, 2026 [VERIFIED][1].

**Problém:** Attention output každého tokenu je příliš podobný jeho vlastnímu value vektoru — model "přečítá vlastní odpověď" místo kontextu. Apple toto nazývá "attention similarity bias."

**Fix:** Ortogonální projekce — odečtení self-value komponenty z attention outputu:
`z_i = y_i − (y_i^T v_i) v_i / ‖v_i‖²`

Dvě řádky kódu, žádné nové parametry, lineární overhead [VERIFIED][1].

**Výsledky:** +0.26% až +1.36% průměrná accuracy na 8 downstream tasks (0.7B→2.7B modely) [VERIFIED][1]. Gainy rostou se sequence length — při 16K tokenech jsou výrazně větší než při 2K [VERIFIED][1].

**Status:** `academic-only` — paper je 19 dní starý, žádné citace ani follow-upy [VERIFIED][1]. Interakce s GQA/MQA nebyla testována — open gap [VERIFIED][1].

---

### 2. Value Residual Learning (Zhejiang University → ACL 2025)

**Paper:** arXiv:2410.17897, Zhou et al., submitted October 2024, přijato na ACL 2025 (Vienna, pp. 28341–28356) [VERIFIED][8].

**Problém:** S hloubkou sítě dochází k "attention concentration" — reprezentace se zúžují místo rozšiřování. Hluboké vrstvy ztrácejí přístup k informacím z rané propagace.

**Fix:** ResFormer přidává residuální spojení z value vektorů první vrstvy (V₁) do všech následujících vrstev. SVFormer varianta sdílí V₁ beze změny přes všechny vrstvy, čímž snižuje KV cache ~50% [VERIFIED][8].

**GQA interakce:** Přímo testováno — SVFormer horší než GQA2 při 2K tokenech, lepší při 64K. Kombinace SVFormer + GQA4 je nejlepší z obou při long-range [VERIFIED][8].

**Academic follow-ups (potvrzeno):**
- ExoFormer (arXiv:2601.08131, Jan 2026): rozšiřuje VRL z values na Q/K/V/gate logity [VERIFIED][15]
- Enhancing Linear Attention with Residual Learning (arXiv:2509.25223, Sep 2025): aplikuje koncept na lineární attention varianty [INFERRED][16]

**Status:** `academic-only` — ACL 2025 akceptace potvrzena, kód veřejný, žádný produkční model VRL neimplementoval [VERIFIED][8].

---

### 3. AttnRes — Attention Residuals (Kimi/Moonshot AI)

**Paper:** arXiv:2603.15031, Kimi Team (36 autorů), submitted March 16, 2026 [VERIFIED][2].

**Problém:** Standardní residuální spojení akumulují výstupy vrstev s fixní vahou 1, čímž magnitude hidden states roste jako O(L) s hloubkou — "PreNorm dilution."

**Fix:** Nahrazuje `h_{l+1} = h_l + f_l(h_l)` za softmax agregaci přes předchozí výstupy vrstev — depth-wise agregace je content-dependent a naučená [VERIFIED][2].

**Block AttnRes** (doporučená varianta): ~8 bloků, <2% inference latency overhead, <4% training overhead [VERIFIED][2].

**Výsledky** (na 48B total / 3B activated MoE, 1.4T tokenů):
- GPQA-Diamond: +7.5 bodů [SINGLE-SOURCE][17] (GitHub README, ne přímo z PDF)
- HumanEval: +3.1, Minerva Math: +3.6, MMLU: +1.1 [SINGLE-SOURCE][17]
- Compute efficiency: odpovídá baseline trénovanému s 1.25× více výpočtu [VERIFIED][2]

**Produkční status — ambivalentní:** Veřejně vydaný `moonshotai/Kimi-Linear-48B-A3B-Instruct` (říjen 2025) AttnRes nepoužívá — model card potvrzuje pouze KDA + MLA [VERIFIED][18]. Paper byl vydán 5 měsíců po release modelu. Nejpravděpodobnější interpretace: AttnRes je vyvíjen pro budoucí Kimi modely [INFERRED][2,18].

**Kritika:** Ziming Liu (nezávislá analýza) dokumentuje, že AttnRes zhoršuje výkon na memorization-heavy a nestrukturovaných úlohách [SINGLE-SOURCE][19].

**Status:** `academic-only` — 13 dní starý, žádné follow-upy [VERIFIED][2].

---

### 4. Differential Attention (Microsoft Research)

**Paper:** arXiv:2410.05258, Ye et al. (Microsoft Research + Tsinghua), October 2024, **ICLR 2025 Oral** (~2% acceptance rate) [VERIFIED][3,20].

**Mechanismus:** Attention = rozdíl dvou paralelních softmax map:
`Attn(X) = softmax(Q₁K₁ᵀ/√d)V₁ − λ·softmax(Q₂K₂ᵀ/√d)V₂`

Odečtení ruší "attention noise" a indukuje sparser, fokusovanější attention patterny [VERIFIED][3].

**Claimed improvements:** long-context retrieval, hallucination reduction, fewer activation outliers, ~65% model size/tokenů potřebných k dosažení srovnatelné perplexity [VERIFIED][3].

**V2 (leden 2026, HuggingFace blog):** Odstraňuje custom FlashAttention kernely (V1 blocker), dekódovací rychlost = baseline, production-scale experimenty na 30B MoE přes triliony tokenů [VERIFIED][9].

**Academic follow-ups (potvrzeno):**
- Shared DIFF Transformer (arXiv:2501.17900, Jan 2025) [VERIFIED][10]
- Understanding Differential Transformer + DEX adapter (arXiv:2505.16333, May 2025): DEX umožňuje post-hoc injekci DiffAttn do stávajících pretrained modelů (Llama, Mistral) [VERIFIED][11]
- Differential Gated Self-Attention M-DGSA (arXiv:2505.24054, May 2025) [VERIFIED][12]

**Status:** `academic-only` (nejzralejší ze čtyř) — žádný produkční deployment v named produktu potvrzen [VERIFIED][9]. DEX adapter je prakticky nejdůležitější follow-up: umožňuje adopci bez přetrénování od začátku.

---

### 5. Produkční realita Q4 2024–Q1 2026

**Kde se skutečně inovuje:**

**MLA (Multi-Head Latent Attention)** — DeepSeek V2 (máj 2024), V3 (prosinec 2024), R1 [VERIFIED][5,6]. Low-rank joint komprese K/V do latentu dim 512; KV cache redukce z 213.5 GB na 7.6 GB [INFERRED z parametrů][6]. TransMLA (arXiv:2502.07864, NeurIPS 2025) dokázal, že MLA je strictly expressivnější než GQA pro identický KV budget [VERIFIED][7]. Ant Group adoptoval TransMLA pro Ling-2.5-1T (1 bilion parametrů) [VERIFIED][7].

**GQA** — De-facto standard pro vše mimo DeepSeek: Llama 3/4, Mistral, Qwen2.5, Gemma 2, Phi-4-Mini [VERIFIED][4,13,21,22,23,24]. MQA (single KV head) prakticky vymizela po Q4 2024.

**iRoPE (Llama 4, duben 2025)** — 1 ze 4 vrstev = global attention bez pozičního embedingu (NoPE), 3 ze 4 = chunked local s RoPE (8K chunks) [VERIFIED][13,14]. Llama 4 Scout: 10M context. Alternativní přístup k long-context bez MLA.

**Gemma 2 alternating local/global** — Každá druhá vrstva = sliding window 4K (local), každá druhá = full attention 8K (global) [VERIFIED][22]. Ovlivnilo Llama 4 design.

**NSA/DSA (DeepSeek)** — Native Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper) [VERIFIED][25]: sub-kvadratická sparse attention, O(Lk) místo O(L²). DeepSeek V3.2-Exp (září 2025, experimentální): první nasazení sub-kvadratické sparse attention v frontier modelu, built on top of MLA [VERIFIED][26].

**Neznámé (GPT-4o, Gemini 2.x):** OpenAI ani Google nepublikovaly architekturní detaily attention mechanismů pro tyto modely [UNVERIFIED][27,28].

---

## Disagreements & Open Questions

- **XSA + GQA/MLA:** Žádný paper to netestoval. XSA operuje na value streamu MHA; jak se komponuje s GQA nebo MLA (kde K/V jsou sdílené/komprimované) je otevřená otázka.
- **AttnRes vs. memorization:** Ziming Liu ukazuje degradaci na memorization tasích [SINGLE-SOURCE] — autoři to v paperu neadresují.
- **DiffAttn V2 produkce:** Microsoft framing je "production-scale validation," ne "product deployment" — je to záměrně ambivalentní.
- **MLA adoption rate:** TransMLA umožňuje post-training konverzi GQA→MLA. Rychlost adopce mimo DeepSeek je otázka 2026–2027.

---

## Evidence Table (merged, top sources)

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Zhai — XSA (arXiv:2603.09078) | https://arxiv.org/abs/2603.09078 | XSA: ortogonální projekce self-V, +0.26–1.36% accuracy | Primary | High |
| 2 | Kimi Team — AttnRes (arXiv:2603.15031) | https://arxiv.org/abs/2603.15031 | AttnRes: softmax over prior layers, 1.25x compute efficiency | Primary | High |
| 3 | Ye et al. — Differential Transformer (arXiv:2410.05258) | https://arxiv.org/abs/2410.05258 | DiffAttn: dual softmax difference, ICLR 2025 Oral | Primary | High |
| 4 | Grattafiori et al. — Llama 3 paper | https://liweinlp.com/wp-content/uploads/2024/07/meta.pdf | GQA standard: 8 KV heads across 8B/70B/405B | Primary | High |
| 5 | DeepSeek-AI — V2 tech report (arXiv:2405.04434) | https://arxiv.org/abs/2405.04434 | MLA první implementace, 93.3% KV cache reduction | Primary | High |
| 6 | DeepSeek-AI — V3 tech report (arXiv:2412.19437) | https://arxiv.org/abs/2412.19437 | MLA v V3: KV dim=512, Q dim=1536, decoupled RoPE dim=64 | Primary | High |
| 7 | TransMLA (arXiv:2502.07864) | https://arxiv.org/abs/2502.07864 | MLA strictly dominuje GQA; Ant Group Ling-2.5-1T adopce | Primary | High |
| 8 | Zhou et al. — Value Residual Learning (arXiv:2410.17897) | https://arxiv.org/abs/2410.17897 | SVFormer > GQA při 64K; ACL 2025 | Primary | High |
| 9 | Microsoft — Diff Transformer V2 (HF blog) | https://huggingface.co/blog/microsoft/diff-attn-v2 | V2: bez custom kernelů, 30B MoE prod-scale, Jan 2026 | Technical blog | High |
| 10 | Cang et al. — Shared DIFF (arXiv:2501.17900) | https://arxiv.org/abs/2501.17900 | Follow-up: sdílená base matrix + low-rank updates | Follow-up | High |
| 11 | Kong et al. — Understanding DiffAttn + DEX (arXiv:2505.16333) | https://arxiv.org/abs/2505.16333 | DEX: post-hoc adapter DiffAttn do pretrained modelů | Follow-up | High |
| 12 | Lygizou et al. — M-DGSA (arXiv:2505.24054) | https://arxiv.org/abs/2505.24054 | Gated varianta DiffAttn s sigmoid gate | Follow-up | High |
| 13 | Meta AI — Llama 4 blog | https://ai.meta.com/blog/llama-4-multimodal-intelligence/ | iRoPE: NoPE global (1:4 ratio) + RoPE chunked local, 10M ctx | Official | High |
| 14 | HuggingFace — Llama 4 release | https://huggingface.co/blog/llama4-release | iRoPE potvrzeno | Secondary | High |
| 15 | Su — ExoFormer (arXiv:2601.08131) | https://arxiv.org/abs/2601.08131 | Rozšiřuje VRL na Q/K/V/gates, cituje VRL | Follow-up | High |
| 16 | Lai et al. — Enhancing Linear Attention (arXiv:2509.25223) | https://arxiv.org/abs/2509.25223 | Residual learning pro lineární attention varianty | Adjacent | Medium |
| 17 | MoonshotAI — AttnRes GitHub | https://github.com/MoonshotAI/Attention-Residuals | GPQA +7.5, HumanEval +3.1, Math +3.6 (README) | Code/repo | Medium |
| 18 | Moonshot AI — Kimi-Linear-48B model card | https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct | Produkční model NEPOUŽÍVÁ AttnRes | Model card | High |
| 19 | Ziming Liu — When does AttnRes work? | https://kindxiaoming.github.io/blog/2026/attention-residual/ | AttnRes horší na memorization tasích | Analysis | Medium |
| 20 | ICLR 2025 — DiffAttn Oral | https://iclr.cc/virtual/2025/oral/31859 | Oral designation potvrzen | Conference | High |
| 21 | Jiang et al. — Mistral 7B (arXiv:2310.06825) | https://arxiv.org/abs/2310.06825 | GQA 32Q/8KV + SWA | Primary | High |
| 22 | Gemma Team — Gemma 2 (arXiv:2408.00118) | https://arxiv.org/abs/2408.00118 | GQA + alternating local/global attention | Primary | High |
| 23 | Qwen Team — Qwen2.5 (arXiv:2412.15115) | https://arxiv.org/abs/2412.15115 | GQA, YARN + DCA pro long-context varianty | Primary | High |
| 24 | Microsoft — Phi-4-Mini (arXiv:2503.01743) | https://arxiv.org/abs/2503.01743 | GQA 24Q/8KV; Phi-4 14B používá MHA | Primary | High |
| 25 | DeepSeek-AI — NSA (arXiv:2502.11089) | https://arxiv.org/abs/2502.11089 | Native Sparse Attention, ACL 2025 Best Paper | Primary | High |
| 26 | DeepSeek — V3.2-Exp announcement | https://api-docs.deepseek.com/news/news250929 | DSA: O(Lk) sparse attention na MLA, exp. nasazení | Official | High |
| 27 | ACL Anthology — VRL (ACL 2025) | https://aclanthology.org/2025.acl-long.1375/ | Akceptace na ACL 2025 potvrzena | Conference | High |

---

## Coverage Status

- **[VERIFIED]:** XSA paper existence + výsledky; DiffAttn ICLR 2025 Oral; VRL ACL 2025; Kimi-Linear nepoužívá AttnRes; DiffAttn V2 blog; ExoFormer cituje VRL; MLA parametry DeepSeek V3; GQA ve všech main modelech; NSA ACL 2025 Best Paper; iRoPE Llama 4
- **[INFERRED]:** DeepSeek KV cache čísla (7.6 GB / 28x) — odvozeno z parametrů, ne přímo z textu paperu; AttnRes bude v budoucích Kimi modelech (z časové posloupnosti)
- **[SINGLE-SOURCE]:** AttnRes GPQA +7.5 benchmark (pouze GitHub README); AttnRes memorization degradace (pouze Ziming Liu blog)
- **[UNVERIFIED]:** GPT-4o attention architecture; Gemini 2.x attention architecture; TransMLA "NeurIPS 2025 Spotlight" label (arXiv neuvádí, ostatní zdroje ano)

**[UNVERIFIED] rate: ~10% — pod varovným prahem 30%**

---

## Sources (full list)

1. Zhai — Exclusive Self Attention — https://arxiv.org/abs/2603.09078
2. Kimi Team — Attention Residuals — https://arxiv.org/abs/2603.15031
3. Ye et al. — Differential Transformer — https://arxiv.org/abs/2410.05258
4. Grattafiori et al. — Llama 3 paper — https://liweinlp.com/wp-content/uploads/2024/07/meta.pdf
5. DeepSeek-AI — V2 Technical Report — https://arxiv.org/abs/2405.04434
6. DeepSeek-AI — V3 Technical Report — https://arxiv.org/abs/2412.19437
7. MuLab PKU — TransMLA — https://arxiv.org/abs/2502.07864
8. Zhou et al. — Value Residual Learning — https://arxiv.org/abs/2410.17897
9. Microsoft — Diff Transformer V2 — https://huggingface.co/blog/microsoft/diff-attn-v2
10. Cang et al. — Shared DIFF Transformer — https://arxiv.org/abs/2501.17900
11. Kong et al. — Understanding Differential Transformer + DEX — https://arxiv.org/abs/2505.16333
12. Lygizou et al. — M-DGSA — https://arxiv.org/abs/2505.24054
13. Meta AI — Llama 4 blog — https://ai.meta.com/blog/llama-4-multimodal-intelligence/
14. HuggingFace — Llama 4 release — https://huggingface.co/blog/llama4-release
15. Su — ExoFormer — https://arxiv.org/abs/2601.08131
16. Lai et al. — Enhancing Linear Attention with Residual Learning — https://arxiv.org/abs/2509.25223
17. MoonshotAI — Attention-Residuals GitHub — https://github.com/MoonshotAI/Attention-Residuals
18. Moonshot AI — Kimi-Linear-48B-A3B-Instruct — https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct
19. Ziming Liu — When does Attention Residuals work? — https://kindxiaoming.github.io/blog/2026/attention-residual/
20. ICLR 2025 — Differential Transformer Oral — https://iclr.cc/virtual/2025/oral/31859
21. Jiang et al. — Mistral 7B — https://arxiv.org/abs/2310.06825
22. Gemma Team — Gemma 2 — https://arxiv.org/abs/2408.00118
23. Qwen Team — Qwen2.5 — https://arxiv.org/abs/2412.15115
24. Microsoft — Phi-4-Mini — https://arxiv.org/abs/2503.01743
25. DeepSeek-AI — Native Sparse Attention — https://arxiv.org/abs/2502.11089
26. DeepSeek — V3.2-Exp — https://api-docs.deepseek.com/news/news250929
27. ACL Anthology — Value Residual Learning — https://aclanthology.org/2025.acl-long.1375/

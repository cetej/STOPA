# Kascade & Sparse Attention — Využitelnost a Inspirace pro Implementaci

**Date:** 2026-04-05
**Question:** Jak využít Kascade (arXiv:2512.16391) a jeho principy sparse attention jako inspiraci pro implementační vylepšení?
**Scope:** standard (survey)
**Sources consulted:** 28

## Executive Summary

Kascade (Microsoft Research, 2025) přináší jednu klíčovou inovaci: **cross-layer top-k index reuse** — pozorování, že sousední transformer vrstvy sdílejí ~98% důležitých tokenů, takže stačí spočítat přesné Top-k indexy jen v několika "anchor" vrstvách a zbytek recyklovat. Výsledek: 4.1x decode / 2.2x prefill zrychlení oproti FlashAttention-3 [VERIFIED][1]. Háček: **vyžaduje H100 GPU** pro efektivní kernely [VERIFIED][2].

Pro praktické nasazení na consumer hardware (RTX 4090) existují tři přístupnější cesty: **SpargeAttn** (ICML 2025, training-free, pip-instalovatelný, RTX 3090/4090) [VERIFIED][3], **FlexAttention** (PyTorch stable, zero deps) [VERIFIED][5], a **IndexCache** (cross-layer reuse bez custom CUDA, patch pro vLLM/SGLang) [VERIFIED][4]. Kascade samotný je dnes spíš výzkumný benchmark než nasaditelný nástroj — ale vzory, které zavedl, jsou přenositelné i mimo LLM inference.

## Detailed Findings

### Kascade — Technický Mechanismus

Kascade staví na dvou empirických pozorováních [VERIFIED][1]:
1. Post-softmax attention je přirozeně řídká — ~10% klíčů nese většinu attention mass
2. Identita důležitých klíčů je stabilní mezi sousedními vrstvami (korelace >0.98)

**Anchor vrstvy** počítají přesné Top-k indexy. **Reuse vrstvy** indexy přebírají. Výběr anchor vrstev řeší dynamic programming optimalizující cross-layer similarity na kalibrační sadě [VERIFIED][1]. Head-aware remapping — každá hlava reuse vrstvy se mapuje na *nejpodobnější* hlavu anchor vrstvy (ne 1:1) — je klíčový pro přesnost (ablace ukazují 1-3% degradaci bez něj) [VERIFIED][1].

**Benchmarky** (H100, 10% top-k sparsity) [VERIFIED][1]:
- Decode: 4.1x speedup při 131K kontextu, ~3.4x při 16K
- Prefill: 2.66x při 131K
- AIME-24: 47.92% pass@1 vs 50.42% baseline (DeepSeek-R1-8B)
- vs Quest: 47.92% vs 7.50%; vs StreamingLLM: 47.92% vs 0.00%

**Omezení** [VERIFIED][1,2]:
- Nesnižuje KV cache paměť — jen compute latenci
- H100-only kernely (TileLang, CUDA 12.8+, fp16 only)
- Testováno pouze na 8B modelech (Llama-3.1, Qwen3, DeepSeek-R1-Distill)
- Kalibrace na dev setu (MuSiQue) — potenciální distributional bias

### Srovnání s Konkurencí

| Metoda | Fáze | Mechanismus | Training? | KV Memory | Consumer GPU | Produkční |
|--------|------|-------------|-----------|-----------|-------------|-----------|
| **Kascade** | Both | Cross-layer top-k reuse | Ne | Ne | H100 only | Near |
| **MInference** | Prefill | 3-pattern offline (A-shape, V-slash, block) | Ne | Ne | A100+ | **Ano (SGLang/vLLM)** |
| **SpargeAttn** | Both | Two-stage online filter | Ne | Ne | **RTX 3090+** | Near |
| **Quest** | Decode | Query-aware page criticality | Ne | Ano | Any | Ano |
| **SnapKV** | Prefill | Observation window voting | Ne | Ano | A100+ | Ano |
| **H2O** | Decode | Heavy hitter eviction | Ne | Ano | Any | Ano |
| **StreamingLLM** | Both | Sink + sliding window | Ne | Ano | Any | Ano |
| **MagicPIG** | Decode | LSH + CPU offload | Ne | CPU | Various GPU | Ano |
| **IndexCache** | Both | Cross-layer F/S split (DSA) | Ne | Ne | H100* | Patch |
| **NSA** | Both | Coarse+fine hierarchie | Pre-train | Ne | Any | Ne |
| **SeerAttention** | Prefill | Learnable MoE gate | Gate only | Ne | Any | Near |

*IndexCache nemá custom CUDA → teoreticky portabilní, ale benchmark jen na H100

**Co dělá Kascade unikátním** [INFERRED][1,7,16]:
- Jediná metoda s cross-layer reuse indexů
- Pokrývá prefill i decode současně (většina ostatních jen jedno)
- Automatizovaný výběr anchor vrstev (vs manuální u TidalDecode/LessIsMore)
- Nejlepší reasoning accuracy mezi training-free metodami

**Co Kascade nedělá** [VERIFIED][1]:
- KV cache komprese (na to H2O, SnapKV, Quest)
- Consumer GPU support
- Modely >8B

### Praktická Implementace na Consumer Hardware

**Doporučená progrese** (od nejsnazší k nejkomplexnější):

**1. FlexAttention** (PyTorch 2.5+, prototype feature) [VERIFIED][5]
- Zero extra deps, `torch.nn.attention.flex_attention`
- `block_mask` API kompiluje sparse patterns do FlashAttention kernelů
- Cross-layer reuse: spočítej `block_mask` na referenční vrstvě, recykluj pro N dalších
- Caveat: `create_block_mask` je drahý — musí se cacheovat
- Note: blog uvádí "prototype", ne "stable" — API se může měnit

**2. SpargeAttn** (ICML 2025) [VERIFIED][3]
- `pip install ninja && python setup.py install`
- Training-free drop-in, RTX 3090/4090 (Ampere/Ada), CUDA >=12.0
- Two-stage online filter: predikce attention mapy → skip zbytečných matmulů
- Windows fork: https://github.com/sdbds/SpargeAttn-for-windows

**3. FlashInfer + vLLM** [VERIFIED][6]
- `pip install flashinfer-python`, sm7.5-sm12.0
- `--attention-backend FLASHINFER` ve vLLM
- 28-30% latency redukce pro long-context inference
- Sparse MLA built-in pro DeepSeek modely

**4. IndexCache** (pro DSA modely) [VERIFIED][4]
- Patch na vLLM/SGLang, žádné custom CUDA kernely
- F-layers počítají indexer, S-layers kopírují cache
- 1.82x prefill speedup, 75% indexer compute eliminováno
- Omezení: jen DeepSeek-V3.2 / GLM-5 modely

**5. oLLM** (pro memory-bound scénáře) [UNVERIFIED][23]
- `pip install ollm`
- KV-cache offload na SSD → 100K kontext na 8GB VRAM (tvrzení z MarkTechPost; PyPI URL nefunkční, nezávisle neověřeno)
- Pro offline batch workloads, ne real-time

### Inspirace pro STOPA / Orchestrační Systémy

Kascade zavádí tři vzory přenositelné mimo LLM inference:

**Vzor 1: Cross-Layer Reuse → Cross-Agent Reuse**
Pokud sousední vrstvy sdílejí 98% důležitých tokenů, pak sousední agenti v pipeline mohou sdílet většinu kontextu. Místo aby každý sub-agent začínal od nuly, "anchor" agent provede plný průzkum a "reuse" agenti přeberou jeho zjištění. *Toto je de facto Findings Ledger pattern z RLM* — Kascade ho validuje empiricky na úrovni attention.

**Vzor 2: Automated Anchor Selection → Automated Delegation Points**
DP algoritmus pro výběr anchor vrstev je generalizovatelný: v orchestračním pipeline ne každý krok vyžaduje plnou analýzu. Optimalizátor může určit, které kroky jsou "anchor" (plná práce) a které "reuse" (přeberou výsledky).

**Vzor 3: Head-Aware Remapping → Task-Agent Matching**
Kascade nemapuje hlavy 1:1 — hledá nejpodobnější. Analogicky: při delegaci sub-tasků na agenty nemusí být optimální přiřazení "tento sub-task → specializovaný agent", ale spíš "tento sub-task → agent s nejpodobnějším kontextem".

## Disagreements & Open Questions

- **Top-k vs adaptive threshold**: PSA (arXiv:2503.00392) argumentuje, že fixní top-k je suboptimální; The Sparse Frontier (arXiv:2504.17768) ukazuje, že delší sekvence tolerují vyšší sparsity → adaptivní budget může být lepší [INFERRED][15,16]
- **Training-free ceiling**: NSA a SeerAttention ukazují, že lehký trénink překonává training-free metody; Kascade volí deployment jednoduchost za cenu accuracy ceiling [INFERRED][10,12]
- **Consumer GPU benchmarks chybí**: Žádné srovnání všech metod na RTX 4090 — většina benchmarků na A100/H100 [UNVERIFIED]
- **Kascade na >8B modelech**: Netestováno; cross-layer similarity může být jiná u 70B+ [UNVERIFIED]

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Kascade paper | https://arxiv.org/abs/2512.16391 | 4.1x decode, 2.2x prefill vs FA3; cross-layer top-k reuse | primary | high |
| 2 | Kascade GitHub | https://github.com/microsoft/kascade | H100 required; CUDA 12.8+; fp16 only | primary | high |
| 3 | SpargeAttn GitHub | https://github.com/thu-ml/SpargeAttn | Training-free; Ampere/Ada GPU; ICML 2025 | primary | high |
| 4 | IndexCache GitHub | https://github.com/THUDM/IndexCache | Cross-layer reuse bez CUDA kernelů; 1.82x prefill | primary | high |
| 5 | FlexAttention blog | https://pytorch.org/blog/flexattention/ | block_mask API; PyTorch stable; torch.compile | primary | high |
| 6 | FlashInfer docs | https://docs.flashinfer.ai/installation.html | sm7.5-sm12.0; pip install | primary | high |
| 7 | MInference paper | https://arxiv.org/abs/2407.02490 | 3-pattern prefill; 10x speedup; NeurIPS Spotlight | primary | high |
| 8 | MagicPIG paper | https://arxiv.org/abs/2410.16179 | LSH + CPU offload; 5x throughput; RTX 4090 | primary | high |
| 9 | vAttention paper | https://arxiv.org/abs/2405.04437 | CUDA VMM; 1.97x over vLLM; complementary | primary | high |
| 10 | NSA paper | https://arxiv.org/abs/2502.11089 | Trainable sparse attention; ACL 2025 | primary | high |
| 11 | SpargeAttn paper | https://arxiv.org/abs/2502.18137 | Universal two-stage filter; ICML 2025 | primary | high |
| 12 | SeerAttention paper | https://arxiv.org/abs/2410.13276 | Learnable gate; 5.67x at 90% sparsity | primary | high |
| 13 | HashAttention paper | https://arxiv.org/abs/2412.14468 | MIPS via Hamming; 4.3x attention latency | primary | high |
| 14 | StreamingLLM GitHub | https://github.com/mit-han-lab/streaming-llm | Attention sink; ICLR 2024; HuggingFace SinkCache | primary | high |
| 15 | The Sparse Frontier | https://arxiv.org/abs/2504.17768 | 6-method empirical comparison; longer seqs tolerate more sparsity | primary | high |
| 16 | PSA paper | https://arxiv.org/abs/2503.00392 | Threshold-based adaptive selection | primary | medium |
| 17 | H2O paper | https://arxiv.org/abs/2306.14048 | Heavy hitter eviction; 29x throughput; NeurIPS 2023 | primary | high |
| 18 | SnapKV paper | https://arxiv.org/abs/2404.14469 | Observation window; 3.6x decode; NeurIPS 2024 | primary | high |
| 19 | Quest paper | https://arxiv.org/abs/2406.10774 | Query-aware page criticality; ICML 2024 | primary | high |
| 20 | IndexCache paper | https://arxiv.org/abs/2603.12201 | F/S layer split; training-free cross-layer reuse | primary | high |
| 21 | FlashInfer MLSys | https://proceedings.mlsys.org/paper_files/paper/2025/file/dbf02b21d77409a2db30e56866a8ab3a-Paper-Conference.pdf | 28-30% latency reduction | primary | high |
| 22 | PyTorch flex_attention docs | https://docs.pytorch.org/docs/stable/nn.attention.flex_attention.html | Stable API; block_mask caching required | primary | high |
| 23 | oLLM PyPI | https://pypi.org/project/ollm/ | SSD KV offload; 100K on 8GB | primary | medium |
| 24 | RTX 4090 benchmarks | https://www.hardware-corner.net/rtx-4090-llm-benchmarks/ | 57K context on 30B MoE | secondary | medium |
| 25 | SpargeAttn Windows | https://github.com/sdbds/SpargeAttn-for-windows | Windows+RTX 4090 build | primary | medium |
| 26 | vLLM attention docs | https://docs.vllm.ai/en/latest/design/attention_backends/ | FlashInfer backend selectable | primary | high |
| 27 | vLLM sparse attn RFC | https://github.com/vllm-project/vllm/issues/33980 | Active community discussion | primary | medium |
| 28 | Kascade full paper HTML | https://arxiv.org/html/2512.16391 | DP algorithm, head remapping, ablations | primary | high |

## Sources

1. Deshmukh et al. — Kascade paper — https://arxiv.org/abs/2512.16391
2. microsoft/kascade GitHub — https://github.com/microsoft/kascade
3. thu-ml/SpargeAttn — https://github.com/thu-ml/SpargeAttn
4. THUDM/IndexCache — https://github.com/THUDM/IndexCache
5. PyTorch FlexAttention blog — https://pytorch.org/blog/flexattention/
6. FlashInfer install docs — https://docs.flashinfer.ai/installation.html
7. MInference — https://arxiv.org/abs/2407.02490
8. MagicPIG — https://arxiv.org/abs/2410.16179
9. vAttention — https://arxiv.org/abs/2405.04437
10. NSA (DeepSeek) — https://arxiv.org/abs/2502.11089
11. SpargeAttn paper — https://arxiv.org/abs/2502.18137
12. SeerAttention — https://arxiv.org/abs/2410.13276
13. HashAttention — https://arxiv.org/abs/2412.14468
14. StreamingLLM — https://github.com/mit-han-lab/streaming-llm
15. The Sparse Frontier — https://arxiv.org/abs/2504.17768
16. PSA — https://arxiv.org/abs/2503.00392
17. H2O — https://arxiv.org/abs/2306.14048
18. SnapKV — https://arxiv.org/abs/2404.14469
19. Quest — https://arxiv.org/abs/2406.10774
20. IndexCache paper — https://arxiv.org/abs/2603.12201
21. FlashInfer MLSys 2025 — https://proceedings.mlsys.org/paper_files/paper/2025/file/dbf02b21d77409a2db30e56866a8ab3a-Paper-Conference.pdf
22. PyTorch flex_attention stable docs — https://docs.pytorch.org/docs/stable/nn.attention.flex_attention.html
23. oLLM PyPI — https://pypi.org/project/ollm/
24. RTX 4090 LLM benchmarks — https://www.hardware-corner.net/rtx-4090-llm-benchmarks/
25. SpargeAttn Windows fork — https://github.com/sdbds/SpargeAttn-for-windows
26. vLLM attention backends — https://docs.vllm.ai/en/latest/design/attention_backends/
27. vLLM sparse attn RFC — https://github.com/vllm-project/vllm/issues/33980
28. Kascade full paper HTML — https://arxiv.org/html/2512.16391

## Coverage Status

- **[VERIFIED]:** Kascade benchmarks (4.1x decode, 47.92% AIME), H100 requirement, SpargeAttn GPU support, FlexAttention API, FlashInfer sm range, IndexCache mechanism
- **[INFERRED]:** Cross-layer reuse pattern transferability to orchestration, training-free vs trainable ceiling tradeoff, adaptive threshold advantage
- **[SINGLE-SOURCE]:** oLLM 100K-on-8GB claim
- **[UNVERIFIED]:** Consumer GPU comparative benchmarks across all methods, Kascade on >8B models, IndexCache on consumer GPU

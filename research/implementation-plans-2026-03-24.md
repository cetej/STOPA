# Implementation Plans — Research Evaluation 2026-03-24

Konkrétní task specs na základě hands-on research + code exploration.
Každý task spec je self-contained — Claude v cílovém projektu ho může vzít a jet.

---

## 1. STOPA — HTTP Hooks (Slack/Webhook Notifikace)

**Status**: IMPLEMENT NOW
**Effort**: ~2h
**Prereqs**: Slack incoming webhook URL, Python 3.x

### Task Spec (pro Claude v STOPA)

> **Úkol**: Implementuj HTTP webhook notifikace pro Claude Code hook eventy.
>
> **Kontext**: CC od v2.1.63 podporuje HTTP hooks — `"type": "http"` v settings.json.
> Kvůli TLS SNI bugu (#30613) HTTPS na externích doménách nefunguje.
> Workaround: localhost proxy server, který přeposílá do Slack webhook.
>
> **Co vytvořit**:
>
> 1. **`scripts/webhook-proxy.py`** — Python HTTP server (http.server/aiohttp):
>    - Poslouchá na `http://localhost:9090/webhook`
>    - Přijímá POST z CC hook (JSON body s `hook_event_name`, `tool_name`, `session_id`, `cwd`)
>    - Formátuje zprávu pro Slack (event name, timestamp, krátký popis)
>    - Přeposílá POST na Slack incoming webhook URL (z env var `SLACK_WEBHOOK_URL`)
>    - Graceful error handling — pokud Slack nereaguje, loguj ale nepadej
>    - Loguj příchozí requesty do stdout pro debugging
>
> 2. **`.claude/settings.local.json`** (template, NE commitovat — obsahuje URL):
>    ```json
>    {
>      "hooks": {
>        "TaskCompleted": [
>          {
>            "matcher": "",
>            "hooks": [
>              {
>                "type": "http",
>                "url": "http://localhost:9090/webhook",
>                "timeout": 10,
>                "statusMessage": "Notifying webhook..."
>              }
>            ]
>          }
>        ],
>        "StopFailure": [
>          {
>            "matcher": "",
>            "hooks": [
>              {
>                "type": "http",
>                "url": "http://localhost:9090/webhook",
>                "timeout": 10,
>                "statusMessage": "Reporting error..."
>              }
>            ]
>          }
>        ]
>      }
>    }
>    ```
>
> 3. **Merge instrukce**: `settings.local.json` se merguje s `settings.json`.
>    Existující command hooks v `settings.json` zůstanou. HTTP hooks v local přidávají
>    do STEJNÝCH event arrays — ověř že CC merguje hooks správně (append, ne replace).
>
> **Známé limitace**:
> - URL v hook configu nepodporuje env vars (#31653) — musí být hardcoded
> - Non-blocking: timeout/connection failure = tiché, CC pokračuje
> - Proxy musí běžet PŘED CC session (jinak se notifikace tiše zahodí)
>
> **Test**: Spusť proxy (`python scripts/webhook-proxy.py`), spusť CC session,
> dokonči libovolný task → ověř zprávu ve Slack kanálu.

---

## 2. test1 — Video Gen Strategy

**Status**: NO ACTION NOW
**Effort**: 0h teď

### Findings z code exploration

- **Pyramid Flow**: standalone `PyramidDiTForVideoGeneration`, model `rain1011/pyramid-flow-sd3`
- **Python 3.8.10**, **PyTorch 2.1.2** (pinned), **diffusers >=0.30.1** (jen utility)
- **Žádné Claude model IDs** — safe od Haiku 3 retirement
- **Žádná CLAUDE.md** — čistý implementation repo
- Entry point: `app.py` (Gradio), podporuje t2v + i2v, CPU offloading, multi-GPU

### Proč NEupgradovat diffusers

1. diffusers 0.32+ importuje TorchAO → crash s PyTorch 2.1.2
2. diffusers 0.37 dropnul Python 3.8
3. Pyramid Flow nepoužívá `DiffusionPipeline` — MagCache/TaylorSeer by nefungovaly
4. Modular Diffusers je experimentální API

### Budoucí task spec (až se rozhodne o novém video modelu)

> **Úkol**: Přidej druhý video generation pipeline vedle Pyramid Flow.
>
> **Kontext**: Pyramid Flow (Python 3.8, PyTorch 2.1.2) zůstává jako fallback.
> Nový pipeline bude v SEPARÁTNÍM virtualenvu s Python 3.11+, PyTorch 2.4+, diffusers 0.37+.
>
> **Model**: [LTX-2 / Kandinsky 5 Pro / Wan 2.2] — TBD na základě benchmarků.
>
> **Co vytvořit**:
> 1. `requirements-v2.txt` — Python 3.11+, PyTorch 2.4+, diffusers 0.37+
> 2. `pipeline_v2.py` — nový pipeline s `DiffusionPipeline` nebo `ModularPipeline`
> 3. Inference caching: `pipe.transformer.enable_cache(MagCacheConfig(...))`
>    - MagCache: kalibrace (1 run s `calibrate=True`) → `mag_ratios` JSON → inference
>    - TaylorSeer: `TaylorSeerCacheConfig(cache_interval=5, max_order=1)`
> 4. `app_v2.py` — Gradio UI pro nový model (nebo přidat tab do `app.py`)
> 5. A/B comparison: side-by-side output Pyramid Flow vs nový model
>
> **Nespouštěj tento task** dokud není rozhodnuto o konkrétním modelu.

---

## 3. NG-ROBOT — FlexAttention Prototyp

**Status**: PROTOTYPE NOW (Triton path), FULL MIGRATION after PyTorch 2.12
**Effort**: ~4h prototyp, ~2 dny plná migrace

### Findings z code exploration

**Soubor**: `pyramid_dit/modeling_mmdit_block.py`

4 attention třídy (řádky 85-486):

| Třída | Řádky | Mechanismus | Poznámka |
|-------|-------|-------------|----------|
| `VarlenFlashSelfAttentionWithT5Mask` | 85-166 | `flash_attn_varlen_func` | Primary, single GPU |
| `SequenceParallelVarlenFlashSelfAttentionWithT5Mask` | 169-259 | flash_attn + `all_to_all` | Multi-GPU |
| `VarlenSelfAttentionWithT5Mask` | 262-321 | `F.scaled_dot_product_attention` | Fallback |
| `SequenceParallelVarlenSelfAttentionWithT5Mask` | 324-393 | SDPA + `all_to_all` | Multi-GPU fallback |

**Klíčové parametry**:
- `is_causal=False` (řádek 309, 375)
- `dropout_p=0.0` (disabled)
- Head dim: 64, 24 hlav
- RoPE: `apply_rope()` na Q,K před attention (řádky 90-95)
- T5Mask: variable-length sekvence s padding/unpadding
- **Temporal causal attention nepodporován flash_attn** (assert řádek 150)

**Claude model IDs**: `config.py` řádky 76-100 — už na `claude-haiku-4-5-20251001` (safe)

### Task Spec — Fáze 1: Prototyp (pro Claude v NG-ROBOT)

> **Úkol**: Vytvoř FlexAttention prototyp pro jednu attention třídu v Pyramid DiT.
>
> **Kontext**: NG-ROBOT používá 4 attention třídy v `pyramid_dit/modeling_mmdit_block.py`.
> Dvě používají `flash_attn_varlen_func` (primary), dvě `F.scaled_dot_product_attention` (fallback).
> FlexAttention (PyTorch 2.5+) umožňuje definovat attention patterns jako Python funkce
> (`score_mod`, `mask_mod`), které se JIT-kompilují do fused kernelů.
>
> **Hlavní výhoda**: Flash attention aktuálně NEPODPORUJE temporal causal attention
> (viz assert na řádku 150: `"The flash attention does not support temporal causal"`).
> FlexAttention by to vyřešil přes custom `mask_mod`.
>
> **Co udělat**:
>
> 1. **Vytvoř `pyramid_dit/modeling_flex_attention.py`** — nová třída
>    `FlexSelfAttentionWithT5Mask` jako alternativa k `VarlenSelfAttentionWithT5Mask`
>    (řádky 262-321 v `modeling_mmdit_block.py`):
>
>    ```python
>    from torch.nn.attention.flex_attention import flex_attention, create_block_mask
>
>    class FlexSelfAttentionWithT5Mask(nn.Module):
>        def __init__(self, ...):
>            # Stejné parametry jako VarlenSelfAttentionWithT5Mask
>            # head_dim=64, num_heads=24
>            pass
>
>        def forward(self, query, key, value, attention_mask, ...):
>            # 1. apply_rope() na Q, K (stejně jako originál, řádky 271-276)
>            # 2. Konvertuj T5Mask attention_mask na mask_mod funkci:
>            #    def t5_mask_mod(b, h, q_idx, kv_idx):
>            #        return attention_mask[stage][b, q_idx, kv_idx]  # nebo obdobně
>            # 3. create_block_mask() — CACHE výsledek per (batch, seq_len) config
>            # 4. flex_attention(q, k, v, block_mask=block_mask)
>            pass
>    ```
>
> 2. **Přidej temporal causal mask** (to co flash_attn neumí):
>    ```python
>    def temporal_causal_mask(b, h, q_idx, kv_idx):
>        # Causal across frames, full attention within frame
>        q_frame = q_idx // tokens_per_frame
>        kv_frame = kv_idx // tokens_per_frame
>        return q_frame >= kv_frame
>    ```
>
> 3. **Benchmark skript** `scripts/bench_flex_attention.py`:
>    - Porovnej latency a memory: SDPA vs FlexAttention vs flash_attn
>    - Testuj s reálnými rozměry: batch=1, seq_len=768*768/(8*8)=9216 tokens (768p),
>      heads=24, head_dim=64
>    - Měř s i bez temporal causal mask
>
> 4. **NEMĚŇ existující kód** — prototyp je v novém souboru, originální třídy zůstanou
>
> **Požadavky**:
> - PyTorch ≥2.5 (FlexAttention dostupný, Triton backend)
> - `torch.compile` potřeba pro optimální výkon
> - `create_block_mask` je drahý — volat jednou, cachovat
> - FlexAttention nepodporuje dropout (NG-ROBOT ho nepoužívá — `dropout_p=0.0`)
>
> **Výstup**: Benchmark výsledky (latency ms, peak memory MB) pro 3 varianty.
> Pokud FlexAttention ≥1.3× rychlejší než SDPA → plánovat plnou migraci.

### Task Spec — Fáze 2: Plná migrace (BUDOUCÍ, po PyTorch 2.12)

> **Úkol**: Migruj všechny 4 attention třídy na FlexAttention s FA4 backendem.
>
> **Prereqs**: PyTorch 2.12+ (FA4 backend stable), Fáze 1 benchmark ≥1.3× speedup.
>
> **Co udělat**:
>
> 1. Upgrade PyTorch na 2.12+ v `requirements.txt`
> 2. V `modeling_mmdit_block.py` přidej `FlexSelfAttentionWithT5Mask` jako 5. třídu
>    (z Fáze 1 prototypu, ověřený benchmark)
> 3. V `JointAttention` (řádky 396-562) přidej `use_flex_attn` flag:
>    - Pokud `True` → použij FlexAttention (s FA4: `kernel_options={"BACKEND": "FLASH"}`)
>    - Pokud `False` → fallback na flash_attn nebo SDPA (stávající chování)
> 4. Block mask cache: slovník `{(batch, seq_len): BlockMask}`, invaliduj při změně
> 5. `torch.compile(dynamic=False)` wrapper pro flex_attention call
> 6. **Temporal causal attention**: nově dostupný díky FlexAttention (řádek 150 assert odstraněn)
> 7. End-to-end benchmark: generuj stejné video s SDPA a FlexAttention, porovnej:
>    - Latency (ms per frame)
>    - Peak GPU memory (MB)
>    - Output quality (PSNR/SSIM proti SDPA output)
>
> **Gotchas**:
> - FA4 backend = H100/B200 only (A100/RTX → Triton fallback, stále OK)
> - `dynamic=False` = separate compiled artifact per (batch, seq_len) shape
> - Head dim 64 < 192 → backward pass OK na všech GPU
> - Block size 64×64 — ověřit že T5Mask sparse regiony alignují na 64-token hranice
>
> **Nespouštěj tento task** dokud PyTorch 2.12 není released a Fáze 1 ukazuje speedup.

---

## 4. ADOBE-AUTOMAT — Minor Cleanup

**Status**: OPTIONAL, LOW PRIORITY
**Effort**: ~15 min

### Findings

- **Haiku 3**: SAFE — žádné reference k `claude-3-haiku-20240307`
- **Model IDs**: Už na Haiku 4.5 (`claude-haiku-4-5-20251001`)
- **Minor issue**: Dva různé Sonnet IDs — `claude-sonnet-4-6` (engine.py) vs `claude-sonnet-4-20250514` (translation_service.py, models.py)

### Task Spec (pro Claude v ADOBE-AUTOMAT)

> **Úkol**: Sjednoť Sonnet model ID na `claude-sonnet-4-6` v celém projektu.
>
> **Kontext**: `backend/core/engine.py` definuje konstantu `MODEL_SONNET = "claude-sonnet-4-6"`,
> ale dva soubory používají starší ID `claude-sonnet-4-20250514`:
> - `backend/services/translation_service.py` řádek 177: `model: str = "claude-sonnet-4-20250514"`
> - `backend/models.py` řádek 144: `model: str = "claude-sonnet-4-20250514"`
>
> **Co udělat**:
> 1. V `translation_service.py` řádek 177: změň default na `MODEL_SONNET` (importuj z engine.py)
> 2. V `models.py` řádek 144: změň default na `"claude-sonnet-4-6"` (Pydantic model nemůže importovat z engine)
> 3. Ověř že žádné další soubory nepoužívají starý ID: `grep -r "sonnet-4-20250514"`

---

## Souhrnný akční plán

| # | Projekt | Task | Kdy | Effort | Urgence |
|---|---------|------|-----|--------|---------|
| 1 | **STOPA** | HTTP hooks → webhook proxy + settings | Další session | ~2h | medium |
| 2 | **ADOBE-AUTOMAT** | Sjednotit Sonnet model ID | Při práci na AA | ~15 min | low |
| 3 | **NG-ROBOT** | FlexAttention prototyp (Triton path) | Při práci na NR | ~4h | medium |
| 4 | **NG-ROBOT** | FlexAttention plná migrace (FA4) | Po PyTorch 2.12 | ~2 dny | deferred |
| 5 | **test1** | Nový video pipeline (ne upgrade PF) | Při rozhodnutí o modelu | ~8-16h | deferred |

## Haiku 3 Retirement Check (Apr 19, 2026)

| Projekt | Status | Detail |
|---------|--------|--------|
| NG-ROBOT | SAFE | `claude-haiku-4-5-20251001` v `config.py:78` |
| ADOBE-AUTOMAT | SAFE | `claude-haiku-4-5-20251001` v `engine.py:34` |
| test1 | SAFE | Žádné Claude model IDs |
| STOPA | SAFE | Žádné hardcoded model IDs (skills používají `model:` frontmatter) |

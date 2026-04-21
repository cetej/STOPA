# NG-ROBOT — Migration plan: sync streaming → Message Batches API

**Date:** 2026-04-21
**Trigger:** Anthropic 300k max_tokens cap na Batches API (beta `output-300k-2026-03-24`, Opus 4.6 + Sonnet 4.6)
**Scenario:** B (projekt nepoužívá Batches)

## Current state

NG-ROBOT používá **sync streaming API** (`client.messages.stream()`) napříč celou pipeline.
Centrální processor: `claude_processor/core.py:415` → `stream_kwargs` pattern.

**Strop max_tokens** hardcoded na 128K v `core.py:523`:
```python
effective_max_tokens = min(estimated_output_tokens, 128000)
```

**Žádné volání `client.messages.batches.create()` nikde v codebase.**
(Výskyty slova "batch" jsou interní: `_audit_inbox_batch.py`, `auto_agent.py` bulk processing, RSS batch.)

## Benefit analysis

| Aspekt | Sync streaming (current) | Batches API |
|--------|--------------------------|-------------|
| Max output tokens | 128k (hard cap) | **300k** (beta) |
| Cena | Plná | **50%** |
| Delivery time | Okamžité (streaming) | ~1h typically, až 24h SLA |
| Use case | Interaktivní (Web UI, CLI ad-hoc) | Offline bulk |
| Progress feedback | Live stream | Polling `batches.retrieve()` |

## Fáze NG-ROBOT — kandidáti na migraci

| Fáze | Kandidát? | Odůvodnění |
|------|-----------|------------|
| 0 Analýza (Haiku, 2000 tok) | **NE** | Rychle, malý output, Haiku 4.5 stejně nemá 300k cap |
| 1 Překlad (Sonnet, high) | **MOŽNÁ** | Dlouhé články benefitují z 300k. Ale sekvenční: blokuje fázi 2+ |
| 2 Kontrola úplnosti | **NE** | Závisí na fázi 1, short output |
| 3 Ověření termínů | **NE** | Web search tool, interaktivní pattern |
| 4 Kontrola faktů | **NE** | Adaptive thinking reasoning, short output |
| 5 Jazyk a kontext | **NE** | Edit operace, short output |
| 6 Stylistika | **NE** | Edit operace |
| 7 SEO a metadata | **NE** | Structured output, short |
| 8 Související články | **NE** | Haiku, web search |
| 9 Finální článek | **POTENCIÁLNĚ** | Kompilace dlouhého výstupu — 300k cap by odemkl delší články |
| 11 Infografiky | **NE** | JSON prompty, short output |

**Verdikt: migrace Batches API NENÍ doporučena pro NG-ROBOT.**

Důvody:
1. **Sekvenční pipeline.** Fáze 1-9 jsou sekvenční — fáze N čeká na N-1. Batches (1h SLA) zrušit 8-10 hodin processing time per článek místo dnešních ~5-15 minut.
2. **Web UI je primární rozhraní.** `ngrobot_web.py` (Flask, port 5001) — uživatel chce live feedback. Streaming je core UX.
3. **Auto_agent.py (RSS bulk)** by teoreticky mohl batches použít, ale RSS → pub cycle je typicky same-day, ne overnight.
4. **128k hard cap je dostatečný pro 99% článků.** Current `estimated_output_tokens = input_chars / 3 * 1.3` dává rezervu. NG articles typicky 5-15k slov → 20-40k output tokens.
5. **CLAUDE.md learning proti MAX_TOKENS inflation:** "Globálně nezvyšovat — thinking tokeny vyplní budget, 3-8× pomalejší, 2-3× dražší."

## Pokud by se migrace někdy vyžadovala — hybrid pattern

```
[Fáze 0-8] → sync streaming (live UX)
     ↓
[Fáze 9 finální článek, když input > 50k znaků]
     ↓
Batches API s beta header `anthropic-beta: output-300k-2026-03-24`
     ↓
Polling + callback do pipeline
```

**Implementation sketch** (NEIMPLEMENTOVÁNO, jen pattern):

```python
# claude_processor/core.py — new method
def process_batch(self, content, system_prompt, max_tokens=200000):
    """Pro fáze které potřebují >128k output (dlouhé články)."""
    batch = self.client.messages.batches.create(
        requests=[{
            "custom_id": "phase-9-final",
            "params": {
                "model": self.model,
                "max_tokens": max_tokens,
                "system": [...],
                "messages": [...],
            }
        }],
        extra_headers={"anthropic-beta": "output-300k-2026-03-24"}
    )
    # Polling loop
    while True:
        status = self.client.messages.batches.retrieve(batch.id)
        if status.processing_status == "ended":
            break
        time.sleep(60)  # 1 min poll interval
    # Fetch results
    results = self.client.messages.batches.results(batch.id)
    return results[0]
```

**Cena vs. čas trade-off:** pro bulk RSS (20+ článků/den) by hybrid uspořil ~40% nákladů na fázi 9. ROI:
- Úspora: ~$0.30 per článek (předpoklad Sonnet 4.6 $3/$15 per MTok)
- 20 článků/den × 30 dní = 600 článků
- **~$180/měsíc úspora** při fázi 9 přes Batches
- Náklad: latency +1h na článek (z 15 min → 75 min celkově)

## Decision

**Current: NE migrovat.** Projekt je interaktivní, 128k cap dostatečný, live feedback je core UX.

**Re-visit trigger:**
- NG-ROBOT začne produkovat články > 40k tokens output (novinářské formáty, dlouhé features)
- Bulk RSS pipeline poroste na 50+ článků/den (cena začne převažovat)
- Anthropic odemkne 300k pro sync API (beta změna)

## Files reviewed (scout results)

- `claude_processor/core.py:415` — streaming entry point
- `claude_processor/core.py:523` — 128k hardcoded cap
- `map_localizer.py` — 8 volání, max_tokens 2000-16000
- `ngrobot_web.py:1994` — max_tokens 64000 (jediné high-tokens volání)
- `bundle_composer.py` — 2× 16000
- `fix_photo_captions.py` — 4000
- `blueprints/articles_bp.py` — 3× (2000-4000)
- `seo_verification.py` — 200-800
- `ng-video/studio/scenario_generator.py` — 3× (2048-4096)

**Žádný soubor neublíží z 300k cap unlock bez Batches migration.**

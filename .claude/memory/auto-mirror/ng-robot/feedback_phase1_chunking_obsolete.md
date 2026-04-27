---
name: Phase 1 chunking is obsolete with Sonnet 4.6
description: Chunking protokol pro dlouhé články byl navržen proti Claude 3 output cap (4K); Sonnet 4.6 má dynamický max_tokens až 128K a zvládne článek single-call. Chunking pro články <150K znaků je vypnutý.
type: feedback
originSessionId: 519d5931-43c8-472a-8dfa-cf85871167b7
---
**Pravidlo:** Phase 1 překlad zpracovává článek v jediném API callu pro všechny vstupy pod 150K znaků / 80 popisků / 60K est. tokenů. Chunking protokol (`_translate_with_chunking`) je zachován jen jako fallback pro extrémní délky.

**Why:** Audit 2026-04-24 (článek Grand Canyon, 57K znaků) ukázal, že chunking při aktivaci způsoboval: fabrikaci H2 sekcí (model si vymýšlel strukturu mezi chunky), vynechávání sekcí (Phase 2 je zpětně doplňovala), 2,3× duplikaci popisků v `9_final.md`, a falešně pozitivní validaci (`extract_captions()` regex hledal CZ formát na EN vstupu → 0 vs 0 projde). Sonnet 4.6 má MAX_TOKENS dynamicky škálovaný do 128K ([core.py:526-532](../../../claude_processor/core.py#L526)) — chunking z éry Claude 3 je dědictvím.

**How to apply:**
- Když něco navrhuje chunking/split/batching pro Phase 1, ověř, že current Sonnet 4.6 zvládne single-call (`estimated_output_tokens = input_chars / 3 * 1.3` pod 128K)
- Nesahat zpět na `THRESHOLDS` v `utilities.py:1566` bez revalidace Claude limitů
- Pokud chunking musí zůstat jako fallback, MUSÍ respektovat: canonical H2 outline z Phase 0 (future work), žádné generování sekce FOTOGRAFIE A MÉDIA v chuncích (Phase 9 to dělá z captions.json), explicitní "NEGENERUJ nové H2" instrukce pro chunky 2+
- Obecné pravidlo: Historické workaroundy proti API limitům re-validuj při každém model upgradu — limity se v roce 2025-2026 výrazně zvedly.

**Podrobnosti auditu:** `docs/LEARNINGS.md` entry 2026-04-24.

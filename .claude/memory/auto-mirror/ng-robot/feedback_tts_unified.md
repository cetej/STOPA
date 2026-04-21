---
name: TTS musí být jednotné napříč funkcemi
description: Uživatel chce jeden TTS výběr pro všechny features (debate, Studio Video, audio články), ne tři oddělené cesty
type: feedback
originSessionId: aa410bbe-2fcf-4314-96a7-03fba4aa2d1d
---
TTS provider a hlas se musí dát vybrat z UI **všude stejně** — jeden source of truth. Dnes je to rozsekané do tří nezávislých cest:

1. `tts_provider.py` (edge/google/gemini) — debate, audio články, Settings → TTS
2. `ng-video/studio/render.py` (edge/elevenlabs) — Studio Video, hardcoded
3. Žádná UI volba pro Studio Video ani video poutáky

**Why:** Uživatel nechce "bordel" kdy jedna funkce běží přes ElevenLabs, jiná přes Edge, a Settings stránka ovládá jen část. Taky: ElevenLabs s jedním defaultním hlasem nedává smysl — má cenu až když se nahraje **custom klonovaný hlas**.

**How to apply:**
- Nedělat ElevenLabs defaultním providerem nikde (default = edge_tts, zdarma)
- Před přidáním nové TTS feature: ověř že jde přes centrální `tts_provider.py` a respektuje Settings
- Až se bude řešit unifikace: integrovat ElevenLabs do `tts_provider.py` (nová třída), přidat `elevenlabs` do config.html dropdown, Studio Video musí číst provider ze Settings (ne hardcoded v scenario_generator)
- ElevenLabs skutečně aktivovat až s custom voice clone (default knihovna nemá smysl pro NG)

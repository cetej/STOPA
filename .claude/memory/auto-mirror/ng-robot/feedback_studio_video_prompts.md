---
name: Studio Video — prompt quality lessons
description: Lessons from chimps article iteration — what makes good/bad Seedance+NanoBanana prompts
type: feedback
---

## Nano Banana Pro (Gemini) — co nefunguje
- Slova "montage", "collage", "grid", "series of", "sequence of" → generuje doslova mřížku malých obrázků místo jedné scény
- "rapid" → interpretuje jako koláž

**Why:** Nano Banana bere prompt doslova. "Rapid montage of chimpanzees" = 4 malé obrázky v mřížce.
**How to apply:** QA sanitizace v `_sanitize_visual_prompts()` odchytává tato slova. Pokud přidáš nové — testuj na reálném článku.

## Seedance 2.0 — co nefunguje
- Close-up tváře vyplňující celý frame → statické, Seedance nemá co animovat (žádné depth layers pro parallax)
- Abstraktní narativ ("two groups approach river, one retreats") → Seedance nedává smysluplný pohyb

**Why:** Seedance animuje z jednoho obrázku. Potřebuje depth layers (foreground/subject/background) pro parallax a viditelný pohybový potenciál (vítr, voda, chůze).
**How to apply:** Kameraman prompt explicitně vyžaduje depth layers a mid-action subjekt.

## Seedance 2.0 — co UMÍ (ale nebylo využíváno)
- Seedance zvládá choreografii více postav — problém byl v formulaci promptu, ne v modelu
- Speed ramping, rack focus, tracking shots — rozumí filmové terminologii
- Komplexní scény s atmosférou (mlha, déšť, vítr) → animuje je přirozeně

**Why:** Původní Kameraman prompt psal statické fotografické scény. Seedance potřebuje popis ZÁBĚRU s pohybem.
**How to apply:** Kameraman (Sonnet, ne Haiku) píše pro VIDEO, ne pro fotografii. Každý prompt musí mít pohybový element.

## Voiceover — co nefunguje
- Haiku ignoruje char limit ("~75 znaků") → píše 2× delší texty
- Encyclopedický styl ("V ugandském pralese se odehrává...") → nudný

**Why:** LLM neumí přesně počítat znaky. Měkký hint nestačí.
**How to apply:** 3-vrstvá ochrana: (1) tvrdý MAXIMÁLNĚ limit v promptu, (2) pre-TTS trim v generate_scenario(), (3) post-TTS trim v task_generate_studio_video(). Styl: "piš jako TRAILER, ne jako encyklopedii".

## UI problém
- Scenario.json se uloží až PO celém pipeline (včetně renderu). Během generace UI ukazuje starý scénář.

**Why:** scenario.json se zapisuje 2× — jednou po scénáři (řádek 1993), ale s prázdnými image/clip paths. Finální zápis (řádek 2031) přepíše až po všech krocích.
**How to apply:** TODO — přidat průběžný zápis scenario.json po každém kroku (images, clips).

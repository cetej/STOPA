---
name: Studio Video — poučení z první implementace
description: Co nefungovalo při Studio Video vývoji — anti-patterns a pravidla
type: feedback
---

# Studio Video — poučení

## Nesahej na fungující pipeline jiného workflow
Video poutáky (social_video_generator.py) fungují. Studio Video je NOVÝ workflow — sdílet infrastrukturu (Remotion, TTS), ne měnit existující kód.
**Why:** Uživatel explicitně řekl "video poutáky neruš".
**How to apply:** Při přidávání nové funkcionality — nové soubory, ne editace existujících working features.

## Obrázky z článku NIKDY jako default
`images[0]` z článku může být infografika, portrait, editovaný diagram. Nesahej na ně slepě.
**Why:** Intro scéna dostala českou infografiku "Jak vzniká sluneční erupce" — portrait formát s textem. Seedance ji animoval a byl to hnus.
**How to apply:** Všechny scény generovat nové obrázky. Články mají volbu "Z článku" v editoru — to je ruční výběr, ne automatický default.

## Audio řídí délku videa, ne naopak
Nejdřív TTS → změřit délku → přepočítat scény. Ne: nastavit 30s → nagenerovat audio → ořezat.
**Why:** Edge TTS generoval 85s audio pro "30s" video — scény byly 21s každá.
**How to apply:** Pipeline pořadí: scénář → TTS → přepočet durations → obrázky → klipy → render.

## Nano Banana (Gemini) > FLUX Pro pro reálné téma
FLUX hallucintuje technologii (Atlantis místo Orion). Nano Banana zná skutečné objekty.
**Why:** Článek o Artemis II — FLUX vygeneroval raketoplán z 80. let.
**How to apply:** Default generátor = Nano Banana (`image_generator.py`). FLUX jen jako volba v editoru.

## Sonnet + Haiku > jen Haiku pro scénář
Haiku sám začne článek vedlejší historkou. Sonnet má editorial úsudek.
**Why:** Haiku začal scénou "V říjnu 1989..." místo hlavního sdělení "Artemis II je mimo ochranu".
**How to apply:** Call 1: Sonnet plánuje (hlavní sdělení, pořadí). Call 2: Haiku vyplní structured JSON.

## FAL_KEY: .env > shell env
Shell env může mít starou hodnotu. Vždy `load_dotenv(override=True)`.
**Why:** 401 Unauthorized — shell měl starý FAL_KEY, .env měl nový.
**How to apply:** `from dotenv import load_dotenv; load_dotenv(Path('.env'), override=True)` na začátku render.py.

## Smazaný soubor se nedá vrátit
Když najdeš soubor na špatném místě — přesuň, nesmaž.
**Why:** Smazal jsem vyrenderované 27MB video místo přesunutí na správné místo.
**How to apply:** `shutil.move()`, ne `rm -rf`.

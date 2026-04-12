---
name: IDML master page filtering
description: IDML extraction must skip master-page-only stories — they contain template placeholder text, not editorial content
type: feedback
---

IDML extrakce musí filtrovat stories patřící pouze master pages (MasterSpreads).

**Why:** Každý IDML z NGM obsahuje master page stories s InDesign placeholder textem (pseudo-latina "uis vend occab ipsam..."), template headlines ("Minihead", "Headline here"), layout anotace ("HI flap", "fold", "GUTTER SPACE") a šablonové patičky. Nic z toho se nepřekládá. Uživatel to vidí v editoru a je to matoucí.

**How to apply:** `list_stories(unpacked_dir, skip_master=True)` v `idml_processor.py` porovnává ParentStory reference z MasterSpreads/ vs Spreads/. Stories referencované POUZE z MasterSpreads se přeskočí. Pokud je patička overridnutá na konkrétní stránce, přesune se do Spreads reference a projde filtrem.

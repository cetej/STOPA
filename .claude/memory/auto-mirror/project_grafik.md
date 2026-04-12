---
name: project_grafik
description: GRAFIK — modular layered image editor using Qwen-Image-Layered via fal.ai, at 000_NGM/GRAFIK
type: project
---

GRAFIK je modulární grafický editor s vrstvami. Používá Qwen-Image-Layered přes fal.ai API pro dekompozici obrázků na RGBA vrstvy.

**Umístění**: `C:\Users\stock\Documents\000_NGM\GRAFIK\`
**Package**: `grafik` (pip install -e .)
**Porty**: API 8100, UI 8501

**Why:** Univerzální nástroj pro lokalizaci map (swap textových vrstev), editaci hero images a obecnou práci s vrstvami. Připojitelný do NG-ROBOT a dalších projektů jako knihovna.

**How to apply:** Při image-related úkolech v jiných projektech zvažuj použití `from grafik import ...` místo ad-hoc Pillow kódu. Fáze 2 (workflows, ops) ještě neimplementována.

---
name: project_dane
description: DANE — Czech personal income tax calculator at 000_NGM/DANE, official form filling, Excel formuláře TODO
type: project
---

DANE je daňový kalkulátor FO v ČR za zdaňovací období 2025 (podání 2026).

**Umístění:** `C:\Users\stock\Documents\000_NGM\DANE`

**Stack:** Python 3.10+, Pydantic v2, Streamlit, PyMuPDF, openpyxl, anthropic (OCR)

**Stav (2026-03-30):**
- Core engine kompletní (tax_calculator, social_insurance, health_insurance, relief_advisor)
- Oficiální PDF formuláře se vyplňují přes pymupdf overlay (form_filler.py)
- Excel generator má 3 listy (DP, ČSSZ, ZP) se vzorci — vizuální styl odpovídající PDF
- UI: Streamlit 4-step wizard (Podklady → Osobní údaje → Kontrola → Výsledek)
- Questionnaire engine (501 řádků) existuje ale NENÍ integrován do UI
- OCR extractor používá Claude Opus (drahé) — měl by Haiku/Sonnet

**TODO — plné Excel formuláře (ROZPRACOVÁNO):**
- Přístup: kopírovat `templates/PavelS_DANE_2018.xlsx` (12 listů, kompletní layout) a aktualizovat na 2025
- Detailní zadání: `docs/TASK_excel_forms.md` (změny řádků, vzorců, konstant 2018→2025)
- ADIS EPO scrape: `docs/adis_epo_structure.md` (přesné texty řádků 2025)
- PDF reference: `templates/mfin5405_page0-3.png`, `cssz_ref_p0-1.png`, `vzp_ref_p0.png`
- `dane/excel_forms.py` — NEDOKONČENO, rozpracovaný template-based přístup
- ČSSZ/ZP: nemají šablonu 2018 — buď uživatel dodá, nebo generovat od nuly
- UI (`ui/app.py`): PDF buttony odstraněny, jen Excel, ale import fallbacků nefunguje

**TODO — GLM-OCR evaluace:**
- Vyzkoušet GLM-OCR (0.9B, Apache 2.0) jako náhradu Claude Opus pro OCR extrakci podkladů
- `pip install glmocr`, běží lokálně (vLLM/SGLang/Ollama) — žádné API náklady
- #1 na OmniDocBench V1.5 (94.62), silný na tabulky a formuláře
- Repo: github.com/THUDM/GLM-OCR
- Porovnat kvalitu vs Claude na českých daňových dokladech (potvrzení zaměstnavatele, faktury)
- Pokud OK → nahradit `ocr_extractor.py` backend

**TODO — questionnaire integrace:**
- Napojit questionnaire.py do UI flow (mezi Podklady a Osobní údaje)
- OCR extrahovaná data řídí, co se questionnaire ptá dál

**Zdravotní pojišťovny:**
- Jednotný formulář (zp_jednotny_2025.pdf) funguje pro všechny ZP
- Kódy: 111=VZP, 201=VoZP, 205=ČPZP, 207=OZP, 209=ZPŠ, 211=ZP MV, 213=RBP

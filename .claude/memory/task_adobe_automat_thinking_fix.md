---
name: ADOBE-AUTOMAT — Sonnet 4.6 thinking/effort fix
description: Doporučení pro opravu text pipeline v ADOBE-AUTOMAT po breaking change Anthropic API (thinking/effort)
type: project
---

# ADOBE-AUTOMAT — Nutné opravy text pipeline

**Kontext:** Sonnet 4.6 změnil chování thinking/effort (viz learning `2026-04-01-sonnet46-thinking-effort-breaking-change.md`). NG-ROBOT měl identický problém a už je opravený. ADOBE-AUTOMAT používá stejný pattern a je ohrožený.

## Ohrožená místa

### 1. `backend/services/text_pipeline/processor.py:194-210`
Stejný pattern jako NG-ROBOT:
- `thinking: adaptive` + `effort: low/medium` → leaked artefakty do výstupu
- `thinking: disabled` → agresivní sumarizace u dlouhých textů

### 2. Fáze reprodukující celý text (KRITICKÉ)
| Fáze | Třída | Aktuální stav | Riziko |
|------|-------|---------------|--------|
| 2 CompletenessChecker | DISABLE_THINKING=True, effort=low | Model sumarizuje místo reprodukce celého článku |
| 5 LanguageContextOptimizer | DISABLE_THINKING=True, effort=medium | Stejné riziko sumarizace |
| 6 StylisticEditor | DISABLE_THINKING=True | Opus — méně náchylný, ale sledovat |

Všechny tři fáze instruují "NIKDY NEZKRACUJ TEXT" — ale model to s thinking:disabled ignoruje.

### 3. Fáze s thinking ON (leaked artefakty)
| Fáze | Místo | Riziko |
|------|-------|--------|
| 3 TermVerifier._research_terms | phases.py:401-413 | Chain-of-thought může leaknout do výstupu |
| 4 FactChecker._audit_facts | phases.py:583-594 | Stejné riziko |

## Doporučené opravy (podle NG-ROBOT vzoru)

### A. PATCH formát pro fáze 2, 5 (priorita 1)
Místo reprodukce celého článku → model vrací jen PATCH bloky s opravami. Programatická aplikace patchů na originál. Eliminuje závislost na reprodukci 20-30K textu.

### B. Strip thinking artefaktů v processor.py (priorita 1)
Přidat post-processing regex v `process()` po získání výstupu:
```python
import re
output = re.sub(r'<antml[^>]*>.*?</antml[^>]*>', '', output, flags=re.DOTALL)
output = re.sub(r'<thinking>.*?</thinking>', '', output, flags=re.DOTALL)
```

### C. DISABLE_THINKING = True pro text-reprodukční fáze (už je)
Aktuální nastavení je správné — nechat thinking OFF. Ale bez PATCH formátu hrozí sumarizace.

### D. Ověřit IDML integritu
ADOBE-AUTOMAT zapisuje zpět do IDML s `<!--[elem-...]-->` markery. Pokud model zkrátí text, ztratí se markery → IDML write-back selže. Testovat na reálném článku.

## Priorita
**VYSOKÁ** — při příštím spuštění pipeline na delším článku (>15K znaků) hrozí stejné selhání jako v NG-ROBOT (fragment 40% výstupu).

## Postup testování
1. Vzít existující zpracovaný článek a pustit znovu od fáze 2
2. Ověřit, že výstup není zkrácený (porovnat délku s originálem)
3. Zkontrolovat výstup na leaked `<antml*>` nebo `<thinking>` tagy
4. Ověřit IDML write-back s novým výstupem

# NG-ROBOT Memory

## Workflow v43.0 - Kritické změny (2026-02-05)

### Aktuální názvy souborů fází
| Fáze | Soubor |
|------|--------|
| 5 | `5_language.md` |
| 6 | `6_stylized.md` |
| 7 | `7_seo.md` |

### PHASES centralizace (aktualizováno 2026-03-23)
PHASES dict je centralizovaný v `config.py` — ngrobot.py, auto_agent.py, ngrobot_web.py ho importují.
Dříve byl duplikovaný ve 3 souborech — nyní stačí měnit na jednom místě.

## Automatické stahování videí

### Kde se stahují
- **Fáze 0.5** v `run_pipeline.py` (před fází 1)
- Po fázi 9 v `auto_agent.py`

### Požadavky
1. `url` musí být dostupné (z metadata.json nebo fallback z original.md)
2. Složka `videos/` nesmí existovat

### URL Fallback seznam (run_pipeline.py)
```python
[article_path / 'original.md',      # RSS články
 article_path / '1_translated.md',  # Přeložené články
 article_path / '0_original.txt']   # Starší formát
```

## České popisky médií

### Workflow
1. Fáze 1-7: České popisky se generují inline v textu
2. Fáze 9: FinalArticleProcessor kompiluje finální článek
3. Po fázi 9: `update_final_captions_from_json()` čte české popisky z `7_media.md`
4. Po fázi 9: `extract_metadata_from_final()` ukládá do `captions.json`

### Kritické: Regex pro FOTO bloky
Formát v43.0: `**FOTO 1:** filename.jpg\n- **Popisek:**...`
Regex musí zachytit filename na stejné řádce.

## Časté chyby

### `cannot access local variable 're'`
Příčina: `import re` uvnitř funkce stínuje globální import
Řešení: Odstranit redundantní import, použít globální

### Přeskakování článků s `--start-stage`
Příčina: Kontrola `9_final.md` ignorovala `start_stage`
Řešení: `if final_check.exists() and not start_stage:`

### Popisky anglicky místo česky
Příčina: `update_final_captions_from_json` hledá špatný soubor
Řešení: Používat `7_media.md` (ne `7_stylized.md`)

## CMS Aqua — DAM obrázky
- **NIKDY nevolat `set-in-review` s `inReview=True`** — zamyká obrázky v CMS editoru
- PUT `/Infobox/{id}` retouch vyžaduje `"id"` v payloadu
- Retouch PŘED `update_article()` — jinak embedded.infobox.image = null

## Otevřené úkoly
- [project_inbox_image_positions.md](project_inbox_image_positions.md) — inbox články nemají správné pozice obrázků/infoboxů v CMS exportu
- [project_visual_social_redesign.md](project_visual_social_redesign.md) — redesign vizuálního/social workflow (sloučení 3 tabů do 2)
- [project_web_refactoring_checkpoint.md](project_web_refactoring_checkpoint.md) — Web UI refactoring: hotové (#2,#6,#14), zbývá blueprinty+logging (#15/#17)
- **ngrobot_web.py helper extrakce** — 4899 řádků, 0 routes (v blueprintech), 43 helperů. Kandidáti: `web_helpers/markdown_converter.py` (472ř), `web_helpers/infobox_utils.py` (321ř), `web_helpers/article_parser.py` (451ř). Celkem ~1200ř = 25% redukce. Nízká priorita.

## Feedback
- [feedback_restart_servers.md](feedback_restart_servers.md) — Po editaci .py souborů VŽDY restartovat běžící servery (sys.modules cache)

## Reference
- [reference_mcp_servers.md](reference_mcp_servers.md) — přehled MCP serverů a status line konfigurace
- [feedback_skill_evals.md](feedback_skill_evals.md) — pravidla pro skills: Nano Banana 15K znaků, volné koncepty, flexibilní aspect ratio

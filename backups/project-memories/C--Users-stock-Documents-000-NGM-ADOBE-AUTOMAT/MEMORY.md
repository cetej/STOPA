# ADOBE-AUTOMAT Memory

## NGM Localizer — Web App

- **Backend**: FastAPI (`backend/main.py`), port 8100
- **Frontend**: Svelte 5 runes, Tailwind, build → `frontend/dist/`
- **Serving**: Backend mountuje dist/ jako StaticFiles (POSLEDNÍ mount)
- **Routing**: SPA hash router — dashboard, extractor, editor, outputs, writeback

### Stav (2026-03-07)
- Phase 1-7 DONE — vše včetně MAP writeback a routing fix
- **Routing**: writable store (router.js), NE .svelte.js modul (nefunguje v prod buildu)
- **KRITICKÉ**: Svelte 5 prod build — each_key_duplicate error tiše rollbackuje celý render
- **Deduplikace ID**: vrstvy se stejným jménem → el.id kolize → opraveno v text_extractor.py

### ExtendScript — důležité
- `layer.textFrames` je HLUBOKÁ kolekce → VŽDY filtrovat `isDirectChild(tf, layer)`
- extract_texts.jsx + write_texts.jsx — konzistentní indexování přímých potomků
- MAP writeback: adaptivní dávkování (`_make_batches()`) — max 50KB nebo 30 položek

### Architektura projektu
- Dashboard: drag-and-drop (.idml → auto projekt+extrakce+editor, .ai → MAP+extractor)
- Extractor: IDML flow (3 kroky: upload IDML, upload překlad DOCX, extrakce) + MAP flow (Illustrator)
- IDML překlad: upload DOCX → `docx_parser.py` → `docx_matcher.py` → spárování s elementy
- AI překlad: `translation_service.py` (Claude API, batch 25, TM cache)
- Export: CSV, XLSX flat, XLSX grouped, JSON
- Writeback: IDML (`idml_writeback.py`) + MAP (`map_writeback.py`)

### Spuštění
- Backend: `cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8100`
- Frontend rebuild: `cd frontend && npm run build`
- **POZOR**: Windows zombie python — vždy `taskkill //IM python.exe //F` před restartem

## Text Pipeline (2026-03-22) — post-translation processing

- **Modul**: `backend/services/text_pipeline/` — adaptace fází 2-6 z NG-ROBOT
- **API**: `POST /api/projects/{id}/process-text` (`routers/pipeline.py`)
- **Frontend**: pipeline panel v Editoru — checkboxy fází, tlačítko "Spustit pipeline"
- **Fáze**: 2=Úplnost, 3=Termíny (2-call: Research→Apply), 4=Fakta+jednotky, 5=Jazyk, 6=Stylistika
- **Element merger**: spojí elementy do textu se značkami `<!--[elem-ID]-->`, po pipeline rozřeže zpět
- **Findings ledger**: cross-phase context (3→5, 4→5, 5→6) v `data/projects/{id}/findings_ledger.json`
- **CzechCorrector** (4.5): běží deterministicky po všech LLM fázích
- **Prompty**: zkopírované z NG-ROBOT do `text_pipeline/prompts/` (5 adresářů + knowledge base)
- **Napojení**: SpeciesDB (218K), TermDB, NormalizedTermDB (244K), CorrectorRulesDB — vše dostupné

### Kontext rozhodnutí
- Zkopírováno (ne importováno) z NG-ROBOT — nezávislost, přizpůsobení IDML kontextu
- Elementy se značkují ID značkami → pipeline zpracuje jako celek → split back
- Prompty se mění zřídka — duplicitní údržba je přijatelné riziko
- ~15-20 dokumentů/měsíc, API náklady ~$15-30/měsíc za celý pipeline

## Feedback
- [IDML master page filtering](feedback_idml_master_pages.md) — extrakce přeskakuje master-page-only stories (template placeholder texty)

## Layout Generator (2026-03-23)
- **Stav**: Session 1-8 + 10-11 DONE — kompletní pipeline + multi-article + Illustrator integration
- Detailní plán: `docs/PLAN_LAYOUT_GENERATOR.md` (Session 9 Template Editor zbývá)
- **Moduly**: `backend/services/layout/` — template_analyzer, spread_patterns, style_profiles, idml_builder, layout_planner, image_analyzer, text_parser, pdf_preview, caption_matcher, map_detector, illustrator_exporter
- **Modely**: `backend/models_layout.py` — Pydantic modely (FrameSpec, SpreadAnalysis, TemplateAnalysis, SpreadPattern, LayoutPlan, MapInfo...)
- **Router**: `backend/routers/layout.py` — 43 endpointů (CRUD, upload, plan, generate, batch, PDF, captions, style transfer, patterns, multi-article, maps)
- **Storage**: `data/layout_projects/{id}/` — meta.json, images/, maps/, layout_plan.json, {id}.idml, preview.pdf, variants/
- **Dataset**: 15 IDML z květnového čísla v `input/samples/`, analýzy v `data/templates/`
- **Session 11 features**: Map Detector (heuristiky), Illustrator Exporter (AI šablona přes ExtendScript), Map Re-import, IDML builder maps integration
- **NG stránka**: 495×720pt, 12 sloupců, 24pt gutter, asymetrické marginy
- **Importy**: Layout moduly používají `from models_layout import ...` (bez `backend.` prefixu)
- **ExtendScript cesta**: `illustrator_exporter.py` → `parent.parent.parent / "extendscripts"` (3 úrovně nahoru)

## OpenJarvis Adopce (2026-03-23)
- [Analýza a plán](reference_openjarvis.md) — cherry-pick patterns z Stanford OpenJarvis
- [Fáze 3 zadání](project_openjarvis_phase3.md) — Model Routing, EventBus, Trace Dashboard
- **Nový modul**: `backend/core/` — Registry, Engine abstrakce, TraceCollector
- **Stav**: Fáze 1+2 DONE, Fáze 3 připravena (3 nezávislé bloky)
- **Cíl**: sjednotit 3× copy-paste `anthropic.Anthropic()` → jedna Engine abstrakce s model routing

## Detailní reference → docs/
- Poučení a konvence: `docs/LEARNINGS.md`
- Řešení problémů: `docs/TROUBLESHOOTING.md`
- ExtendScript vzory: `memory/illustrator_extendscript.md`

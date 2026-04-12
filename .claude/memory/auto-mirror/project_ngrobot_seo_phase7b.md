---
name: NG-ROBOT Phase 7b SEO Verification
description: Phase 7b (SEO verification) + SERP enrichment pre-Phase 7 implemented in NG-ROBOT — keyword density, Czech readability, SERP competitor differentiation
type: project
---

Implemented 2026-04-06. Three components:

**Phase 7b — SEO Verification** (`claude_processor/seo_verification.py`):
- Keyword Density: exact phrase + component matching, placement check (H1, first 100 words, H2)
- Czech Readability: Mistrik Index (Czech Flesch equivalent), sentence length, passive voice, polysyllabic ratio
- SERP Competitor Analysis: post-check comparing generated headlines with Google.cz results

**SERP Enrichment pre-Phase 7** (Varianta C):
- `fetch_serp_for_article()` runs BEFORE Phase 7
- Haiku extracts 2-3 Czech search queries from article
- `web_search_api.py` fetches Google.cz top 5 results per query
- Competitor titles injected into Phase 7 prompt: "tvoje titulky musí být ODLIŠNÉ a SILNĚJŠÍ"
- Phase 7 (Sonnet) generates headlines with awareness of what already ranks

**Why:** Original Phase 7 generated headlines in vacuum. SERP enrichment provides competitive context at generation time, not just as post-check.

**How to apply:** When touching Phase 7 or SEO pipeline — this architecture is: SERP fetch → Phase 7 (with serp_data param) → Phase 7b (verification report). Phase 7b is read-only, never modifies article.

**Files:** `claude_processor/seo_verification.py` (new), `claude_processor/phases.py` (+serp_data param), `document_processor.py` (+SERP pre-fetch + 7b call), `config.py` (+7b in PHASES dict)

---
name: Project direction
description: BIOLIB se transformuje z bio databaze na vicedomenovou terminologickou DB (geografie, medicina, fyzika, astronomie, idiomy)
type: project
---

Projekt se transformuje z biology-specific databaze na univerzalni terminologicku DB.

**Why:** Uzivatel potrebuje preklady odbornych terminu z vice oboru — prioritne geografie, medicina, idiomy, fyzika, astronomie.

**How to apply:** Vsechny nove features navrhovej domain-agnostic. Pri pridavani novych domen pouzij importer framework (importers/base.py). Hlavni DB je termdb.db, puvodni biolib_names.db a species_names.db jsou legacy.

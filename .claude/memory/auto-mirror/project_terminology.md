---
name: Terminology system
description: ngm-terminology plugin + termdb.db — species DB, term DB, lookup optimization TODO, Czech corrector plan
type: project
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
**ngm-terminology v1.1.0**: species DB (218K taxons), term DB (1950 terms), enricher, CLI, auto-discovery.

**Architecture:**
- termdb.db (246K) = single lookup source
- species_names.db = full taxonomy metadata (keep for now)

**TODO:**
- Remove global_ledger.json dual-write, deprecate species_names.db across connected projects
- termdb.db lookup optimization: 30s→<5s (in-memory cache, batch SQL, FTS5, DB shrink)

**Czech corrector plan:**
- Variant A: prompt quick wins
- Variant B: hybrid MorphoDiTa+Hunspell corrector in ngm-terminology

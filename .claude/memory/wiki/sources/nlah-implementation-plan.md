---
title: "NLAH Implementation Plan — 3 aplikovatelné poznatky pro STOPA"
slug: nlah-implementation-plan
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 5
---

# NLAH Implementation Plan — 3 aplikovatelné poznatky pro STOPA

> **TL;DR**: Implementační plán tří poznatků z arXiv:2603.25723 (Natural-Language Agent Harnesses). Klíčové: self-evolution jako acceptance-gated disciplína (+4.8% SWE-bench), path-addressable file-backed state (+5.5% OSWorld), a detekce verifier divergence (-0.8% SWE-bench jako varování). Celkový effort ~24h, P1 priority: strukturovaný state.md + checkpoint.md.

## Key Claims

1. NLAH self-evolution modul přidal +4.8% na SWE-bench Verified — nejsilnější jednotlivý modul v celém NLAH systému — `[verified]` (arXiv:2603.25723)
2. File-backed state přidal +5.5% na OSWorld (nejsilnější modul pro computer-use) a +1.6% na SWE-bench — klíčem jsou tři vlastnosti: externalized, path-addressable, compaction-stable — `[verified]` (arXiv:2603.25723)
3. Verifier modul způsobil -0.8% na SWE-bench — příčina: "verifier divergence" — optimalizace vlastních proxy metrik místo skutečné user satisfaction — `[verified]` (arXiv:2603.25723)
4. STOPA state.md a checkpoint.md jsou prózou — chybí path-addressable subtask IDs (`state.md#st-2`) — identifikovaná mezera C+ vs požadovaná úroveň A — `[argued]`
5. Critic Accuracy Ledger (`.claude/memory/critic-accuracy.jsonl`) s implicit user signal (commit po PASS = aligned, commit po FAIL = overridden) umožňuje detekci divergence bez approval fatigue — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| NLAH (Natural-Language Agent Harnesses) | paper | existing (ref in MEMORY.md) |
| Acceptance-Gated Self-Evolution | concept | new |
| Path-Addressable State | concept | new |
| Verifier Divergence | concept | new |
| Critic Accuracy Ledger | concept | new |

## Relations

- NLAH `validates` Acceptance-Gated Self-Evolution
- NLAH `validates` Path-Addressable State
- Verifier Divergence `degrades` NLAH verifier module
- Critic Accuracy Ledger `detects` Verifier Divergence
- Path-Addressable State `improves` STOPA checkpoint.md

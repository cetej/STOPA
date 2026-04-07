---
title: "Natural-Language Agent Harnesses (NLAH) — Research Brief"
slug: nlah-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 5
---

# Natural-Language Agent Harnesses (NLAH) — Research Brief

> **TL;DR**: Pan et al. (arXiv:2603.25723, Tsinghua + Harbin IT) formalizují design vzor kde je orchestrační logika vyjádřena jako přenositelný NL artefakt místo controller kódu. Klíčové výsledky: migrace kódu na text zvyšuje výkon 30.4% → 47.2% na OSWorld (topologický shift, ne lepší model). File-backed state module +5.5% na OSWorld. Self-evolution modul +4.8% na SWE-bench. STOPA SKILL.md soubory jsou v podstatě NLAHs — paper poskytuje akademické zdůvodnění empiricky vyvinutého přístupu.

## Key Claims

1. Migrace kódu na NLAH: 30.4% → 47.2% na OSWorld — přičina je topologický shift (file-backed state + artifact verifikace vs. screenshot-grounded repair) — `[verified]`
2. File-backed state module: +5.5% na OSWorld, +1.6% na SWE-bench — nejsilnější modul pro computer-use — `[verified]`
3. Self-evolution modul: +4.8% na SWE-bench Verified — nejsilnější jednotlivý modul na code tasks — `[verified]`
4. Verifier modul způsobil -0.8% na SWE-bench — extra struktura automaticky nezlepšuje výkon, může divergovat od acceptance criteria — `[verified]`
5. 90% prompt tokenů a tool calls se děje v delegovaných child agentech, ne v parent threadu — IHR je koordinátor, ne vykonavatel — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| NLAH (Natural-Language Agent Harness) | concept | new |
| IHR (Intelligent Harness Runtime) | concept | new |
| File-backed state module | concept | new |
| OS-Symphony | paper | new |
| Self-evolution module (NLAH) | concept | new |

## Relations

- `NLAH (Natural-Language Agent Harness)` `formalizes` `STOPA SKILL.md`
- `IHR (Intelligent Harness Runtime)` `interprets` `NLAH (Natural-Language Agent Harness)`
- `File-backed state module` `is part of` `NLAH (Natural-Language Agent Harness)`
- `OS-Symphony` `is migrated to` `NLAH (Natural-Language Agent Harness)`
- `Self-evolution module (NLAH)` `adds +4.8% to` `SWE-bench Verified baseline`

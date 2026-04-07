---
title: "Open-Source Resume Builders on GitHub (2024-2026) — Research Brief"
slug: magic-resume-research-2
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 4
---
# Open-Source Resume Builders on GitHub (2024-2026)

> **TL;DR**: Reactive-Resume (36.1k stars) dominuje jako de facto standard pro web-based self-hostable resume editing. Dominant stack 2024-2026: TypeScript + React/Next.js + Tailwind CSS + Zustand. Největší UX posun: nativní AI integrace přímo v editoru. RenderCV (16.2k) přešel na Typst typesetter jako pip-installable LaTeX náhradu s CJK podporou.

## Key Claims

1. Reactive-Resume migroval z Next.js na TanStack Start (React 19, Vite), používá ORPC type-safe RPC a Better Auth s passkeys — `[verified]`
2. RenderCV přešel z LaTeX na Typst v2.0: LaTeX nešel pip-install čistě a chyběla CJK jazyková podpora; Typst řeší obě — `[verified]`
3. react-beautiful-dnd (dominantní DnD knihovna) byl archivován Atlassianem 18. srpna 2025; maintained fork je hello-pangea/dnd — `[verified]`
4. Zustand nahrazuje Redux Toolkit jako emerging standard pro state management v nových projektech — `[inferred]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Reactive-Resume | tool | new |
| RenderCV | tool | new |
| Typst | tool | new |
| Resume-Matcher | tool | new |
| TanStack Start | tool | new |
| react-pdf | tool | new |
| hello-pangea/dnd | tool | new |
| Zustand | tool | new |

## Relations

- RenderCV `replaced` LaTeX `with` Typst `for PDF generation`
- Reactive-Resume `migrated-from` Next.js `to` TanStack Start
- hello-pangea/dnd `is-maintained-fork-of` react-beautiful-dnd
- Resume-Matcher `extends` resume builders `with AI job tailoring`
- Zustand `replacing` Redux Toolkit `in newer projects`

---
date: 2026-04-13
source_type: url
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# Karpathy's LLM Wiki Pattern (Gist) — Raw Capture

## Core Idea
The pattern replaces traditional RAG with a persistent, LLM-maintained wiki. Instead of re-discovering knowledge from scratch on every query, the LLM incrementally builds and updates structured markdown files that sit between raw sources and the user.

Key distinction: "the wiki is a persistent, compounding artifact" rather than ephemeral retrieval results.

## Three-Layer Architecture

**Raw Sources** — Immutable curated documents (articles, papers, images, data). The LLM reads but never modifies these.

**The Wiki** — Directory of LLM-generated markdown files covering summaries, entity pages, concept pages, comparisons, and synthesis. The LLM owns this layer entirely.

**The Schema** — Configuration document (e.g., CLAUDE.md) that specifies wiki structure, conventions, and workflows. Humans and LLM co-evolve this over time.

## Core Operations

**Ingest:** Drop new sources; LLM processes them by discussing takeaways, writing summaries, updating indexes, and revising relevant entity/concept pages. A single source might touch 10-15 wiki pages.

**Query:** Ask questions against the wiki. LLM searches relevant pages, synthesizes answers with citations, and can file valuable discoveries back as new pages.

**Lint:** Periodically health-check the wiki for contradictions, stale claims, orphan pages, missing cross-references, and data gaps.

## Key Files

**index.md** — Content-oriented catalog organized by category, with links and one-line summaries. Updated on every ingest.

**log.md** — Append-only chronological record of ingests, queries, lint passes.

## Fundamental Principle

"The human's job is to curate sources, direct analysis, ask good questions, and think about meaning. The LLM's job is everything else."

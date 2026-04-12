---
name: Diarization Intelligence
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [garry-tan-thin-harness-fat-skills]
tags: [skill-design, research, memory, knowledge-extraction]
---

# Diarization Intelligence

> The process of reading all documents about a subject and writing a structured profile — a single page of judgment distilled from dozens or hundreds of sources.

## Key Facts

- Model reads all documents, surfaces contradictions, notes temporal changes, synthesizes structured intelligence (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Not achievable by SQL queries, RAG pipelines, or retrieval alone — requires actual model judgment (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Example output: "SAYS: Datadog for AI agents / ACTUALLY BUILDING: 80% of commits are in billing module" — contradiction surfaced (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Enables downstream skills to consume structured intelligence rather than raw documents (ref: sources/garry-tan-thin-harness-fat-skills.md)
- Core of any real knowledge work pipeline — converts raw sources into compound knowledge (ref: sources/garry-tan-thin-harness-fat-skills.md)

## Relevance to STOPA

Directly describes what `/ingest` and `/compile` do. The entity extraction + claim synthesis pipeline in ingest IS diarization. Understanding this framing helps design better extraction skills.

## Mentioned In

- [Key Concepts for AI Agentic Skills Design — Thin Harness Fat Skills](../sources/garry-tan-thin-harness-fat-skills.md)

---
title: "PaperDesk: Local Document Workflow Automation"
slug: paperdesk-document-workflow
source_type: url
url: "https://github.com/Abdulmuiz44/PaperDesk"
date_ingested: 2026-04-18
date_published: "2026 (early development)"
authors: "Abdulmuiz44"
entities_extracted: 1
claims_extracted: 3
---

# PaperDesk: Local Document Workflow Automation

> **TL;DR**: Windows-only .NET 8/WPF desktop app for local document automation. Very early stage (13 commits, no releases). Safe-by-default philosophy — all actions need explicit approval. Conceptually similar to paperless-ngx but desktop-native and Windows-only.

## Key Claims

1. All operations require explicit user approval before execution ("safe-by-default") — `asserted`
2. Fully local, no cloud dependencies — privacy-first design — `asserted`
3. Early-stage: SQLite + DDD architecture in place, but features (OCR, search, dedup) not yet implemented — `asserted`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [PaperDesk](../entities/paperdesk.md) | tool | new |

## Relations

- PaperDesk `competes_with` paperless-ngx — both are local-first document management tools (different OS targets)

## Cross-References

- Related entity: [paperless-ngx](../entities/paperless-ngx.md) (web-based, Linux/Docker vs Windows desktop)
- Related learnings: none
- Contradictions: none

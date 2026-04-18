---
title: "paperless-ngx: Community Document Management System"
slug: paperless-ngx-document-management
source_type: url
url: "https://github.com/paperless-ngx/paperless-ngx"
date_ingested: 2026-04-18
date_published: "ongoing (GitHub repo)"
authors: "paperless-ngx community"
entities_extracted: 1
claims_extracted: 4
---

# paperless-ngx: Community Document Management System

> **TL;DR**: Self-hosted DMS successor to Paperless/Paperless-ng. OCR + full-text search over physical documents. Docker Compose deployment. No encryption — local-only use.

## Key Claims

1. Stores all data in clear text without encryption — local trusted server only — `asserted`
2. Full-text search via OCR across all ingested documents — `asserted`
3. Recommended deployment is Docker Compose — `asserted`
4. Python + TypeScript stack, web-based interface — `verified` (GitHub language stats)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [paperless-ngx](../entities/paperless-ngx.md) | tool | new |

## Relations

- paperless-ngx `supersedes` Paperless-ng — official community successor

## Cross-References

- Related learnings: none directly
- Related wiki articles: none directly
- Potential project fit: DANE (tax docs), MONITOR (OSINT archiving)
- Contradictions: none

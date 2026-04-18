---
name: paperless-ngx
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [paperless-ngx-document-management]
tags: [document-management, ocr, search, self-hosted, archiving]
---

# paperless-ngx

> Community-maintained self-hosted document management system that digitizes physical documents into a searchable, OCR-indexed archive.

## Key Facts

- Official successor to Paperless and Paperless-ng projects (ref: sources/paperless-ngx-document-management.md)
- Stack: Python 57.4%, TypeScript 32.9%, HTML 7.9% — web-based interface (ref: sources/paperless-ngx-document-management.md)
- Recommended deployment: Docker Compose via install script (ref: sources/paperless-ngx-document-management.md)
- **Security**: stores data in clear text, no encryption — only for trusted local servers with backups (ref: sources/paperless-ngx-document-management.md)
- Full-text search + OCR across all ingested documents (ref: sources/paperless-ngx-document-management.md)

## Relevance to STOPA

Potential tool for DANE (tax document archiving) or MONITOR (OSINT document storage); provides a self-hosted document retrieval backend with OCR that could complement AI pipelines needing to query physical-document content.

## Mentioned In

- [paperless-ngx: Document Management System](../sources/paperless-ngx-document-management.md)

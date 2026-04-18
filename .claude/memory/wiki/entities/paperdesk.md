---
name: PaperDesk
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [paperdesk-document-workflow]
tags: [document-management, windows, local-first, ocr, search, automation]
---

# PaperDesk

> Privacy-first, local-first Windows desktop app for document workflow automation built on .NET 8 + WPF.

## Key Facts

- Stack: C# only, .NET 8 + WPF, SQLite — Windows desktop (no cloud dependency) (ref: sources/paperdesk-document-workflow.md)
- Architecture: 5-layer DDD (App, Application, Domain, Infrastructure, Tests) with dependency injection (ref: sources/paperdesk-document-workflow.md)
- Planned features: folder watching, content extraction, organizational suggestions, offline index search, duplicate detection (ref: sources/paperdesk-document-workflow.md)
- Design philosophy: "safe-by-default" — all operations require explicit user approval before execution (ref: sources/paperdesk-document-workflow.md)
- **Early stage**: 13 commits, 1 star, 0 forks, no releases (as of 2026-04-18) (ref: sources/paperdesk-document-workflow.md)

## Relevance to STOPA

Conceptually adjacent to paperless-ngx for Windows-native document workflows; the "safe-by-default with explicit approval" design mirrors STOPA's confirmation-before-destructive-action principle. Too early-stage to evaluate seriously.

## Mentioned In

- [PaperDesk: Local Document Workflow Automation](../sources/paperdesk-document-workflow.md)

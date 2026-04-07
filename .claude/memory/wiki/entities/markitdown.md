---
name: MarkItDown (Microsoft)
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [x-tip-analysis]
tags: [pipeline, media]
---
# MarkItDown (Microsoft)

> Microsoft open-source nástroj pro konverzi souborů do Markdown — 87K stars, podporuje PDF, PowerPoint, Word, Excel, Images (OCR), Audio, YouTube URLs, HTML, CSV, JSON, XML, EPUB, ZIP.

## Key Facts

- Repo: https://github.com/microsoft/markitdown — 87K stars
- MCP server pro Claude Desktop integration dostupný
- Install: `pip install markitdown`
- Kritika: přidává lossy translation layer pro formáty které frontier modely ingestionují nativně (ref: sources/x-tip-analysis.md)
- Hlavní use case: batch konverze v pipeline, ne single-file kde Claude čte nativně

## Relevance to STOPA

Potenciální integrace do NG-ROBOT pipeline pro batch zpracování DOCX/PDF. Evaluovat vs. nativní Claude Vision. Nízká priorita — Claude nativně zvládá PDF/images bez konverze.

## Mentioned In

- [X-TIP Analýza: Claude Code tipy z X.com](../sources/x-tip-analysis.md)

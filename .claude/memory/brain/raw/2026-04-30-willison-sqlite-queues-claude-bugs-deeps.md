---
title: Simon Willison: SQLite queue/stream systémy, Claude Code bugs, DeepSeek V4
url: https://simonwillison.net/2026/Apr/24/
date: 2026-04-30
concepts: ["SQLite extension pro NOTIFY/LISTEN", "transactional outbox pattern", "agentic systems debugging", "AI model pricing frontier", "software brain vs human experience", "WAL mode polling", "session state management v AI agents"]
entities: ["Simon Willison", "russellromney (honker)", "Anthropic", "DeepSeek", "Nilay Patel", "spacecowboy (For You Feed)", "Bluesky", "OpenRouter"]
source: brain-ingest-local
---

# Simon Willison: SQLite queue/stream systémy, Claude Code bugs, DeepSeek V4

**URL**: https://simonwillison.net/2026/Apr/24/

## Key Idea

Simon Willison shrnuje zajímavé technologie z 24. dubna 2026: SQLite rozšíření honker pro queues/streams, postmortem bugů v Claude Code, nový model DeepSeek V4 a kritiku AI automatizace od Nilay Patela.

## Claims

- Honker implementuje Postgres NOTIFY/LISTEN semantiku pro SQLite pomocí Rust extension a WAL file polling každou 1ms
- Claude Code měl tři separátní systémové bugy (ne model problémy): session clearing každý turn místo jednou, což způsobilo zapomínání v dlouhých seancích
- DeepSeek V4 nabízí téměř frontier kvalitu za zlomek ceny: $0.14/$0.55 za milion tokenů vs GPT-5.5 $3/$15
- Bluesky For You Feed obsluhuje 72K uživatelů z domácího PC s Go+SQLite za $30/měsíc, kapacita až 1M DAU
- Nilay Patel tvrdí, že lidé AI nenávidí protože 'flattens' lidskou zkušenost do databází — 'software brain' je odtržený od reality

## Relevance for STOPA

Honker extension ukazuje robustní pattern pro event-driven orchestraci v SQLite (transactional outbox). Claude Code postmortem odhaluje komplexitu debugging agentic systémů — session state management je kritický. DeepSeek V4 pricing disrupts náklady pro STOPA agenty.

---
name: brain-gmail
description: "Use when scanning Gmail for knowledge-worthy emails to capture into 2BRAIN. Trigger on 'brain gmail', 'scan emails', 'check mail for brain', 'gmail capture'. Do NOT use for reading specific emails or composing replies."
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Grep", "mcp__4d0c1623-7e8b-4f1e-9b9a-36886f0f768b__gmail_search_messages", "mcp__4d0c1623-7e8b-4f1e-9b9a-36886f0f768b__gmail_read_message", "mcp__4d0c1623-7e8b-4f1e-9b9a-36886f0f768b__gmail_read_thread", "TodoWrite"]
permission-tier: workspace-write
phase: build
tags: [memory, pkm, email]
discovery-keywords: [email, gmail, newsletter, inbox, pošta, emaily]
---

# /brain-gmail — Scan Gmail for 2BRAIN Capture

Prohledá Gmail labely (To Read, To Watch, Later, Starred) a newslettery, extrahuje zajímavý obsah a přidá do brain/inbox.md.

## Workflow

### Phase 1: Scan Labels

Pro každý label v brain/watchlist.md "Gmail Labels":
1. `gmail_search_messages` s query `label:<name> is:unread`
2. Pro každý nalezený email (max 5 per label):
   - `gmail_read_message` — přečti obsah
   - Extrahuj: subject, sender, URL z těla, klíčový obsah
3. Přidej do brain/inbox.md Queue:
   - Pokud email obsahuje URL: `URL: <url>  <!-- gmail <subject> -->`
   - Pokud jen text: `IDEA: [Gmail] <subject> — <summary>`

### Phase 2: Scan Newsletter Senders

Pro každý sender v "Gmail Senders":
1. `gmail_search_messages` s `from:<sender> newer_than:1d`
2. Stejné zpracování jako Phase 1 (max 3 per sender)

### Phase 3: Report

Vypiš:
- Kolik emailů nalezeno a zpracováno
- Které URL/ideas přidány do inbox
- Aktualizuj scan dates ve watchlist.md

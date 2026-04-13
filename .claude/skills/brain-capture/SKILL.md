---
name: brain-capture
description: "Use when capturing the current Chrome tab into 2BRAIN. Trigger on 'brain-capture', 'capture this page', 'ulož tuhle stránku', 'brain this'. Do NOT use for manual text capture (/capture) or STOPA learnings (/scribe)."
user-invocable: true
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "mcp__Claude_in_Chrome__tabs_context_mcp", "mcp__Claude_in_Chrome__get_page_text", "mcp__Claude_in_Chrome__navigate", "mcp__Claude_in_Chrome__read_page", "TodoWrite"]
permission-tier: workspace-write
phase: build
tags: [memory, pkm, web, browser]
discovery-keywords: [browser, page, tab, stránka, web capture, clip, uložit stránku]
input-contract: "user → Chrome tab is open with content → tab accessible via MCP"
output-contract: "raw file + wiki article + graph update → brain/ directory"
---

# /brain-capture — Capture Current Chrome Tab into 2BRAIN

Přečte aktuální Chrome tab, extrahuje obsah, uloží do brain/raw/ a zkompiluje do wiki/.

## Workflow

### Phase 1: Read Chrome Tab

1. `tabs_context_mcp` — získej tab ID
2. `get_page_text` — extrahuj clean text z aktuální stránky
3. Zapamatuj si: URL, title, text content

### Phase 2: Save to raw/

1. Vytvoř `brain/raw/YYYY-MM-DD-<slug-from-title>.md` s:
   ```yaml
   ---
   date: YYYY-MM-DD
   source_type: url
   source_url: <tab URL>
   title: <tab title>
   ---
   ```
2. Pod frontmatter: extrahovaný text (zkrácený na max 2000 slov)

### Phase 3: Compile to wiki/

Aplikuj Karpathy compiler analogy:
1. **Extraction**: Identifikuj klíčové koncepty, entity, reasoning patterns
2. **Synthesis**: Porovnej s existujícími wiki články (čti related přes knowledge-graph.json)
3. **Structure**: Vytvoř/aktualizuj wiki článek(y)
4. **Refinement**: Aktualizuj cross-references

### Phase 4: Connect + Index

1. Aktualizuj `brain/knowledge-graph.json` — nové nodes + edges
2. Aktualizuj `brain/wiki/index.md`
3. Append do `brain/wiki/log.md`
4. Append do `brain/timeline.md`

### Phase 5: Report

Vypiš:
- Název a URL zachycené stránky
- Které wiki články byly vytvořeny/aktualizovány
- Nové graph connections

## Rules

- Max 2000 slov do raw/ — delší stránky zkrať na podstatné části
- Pokud stránka nemá užitečný obsah (login wall, prázdná): STOP, informuj uživatele
- Pokud wiki článek pro stejnou URL už existuje: AKTUALIZUJ, nevytvářej duplicitu

---
title: Změny v systémovém promptu Claude Opus 4.6 až 4.7
url: https://simonwillison.net/2026/apr/18/opus-system-prompt/
date: 2026-04-26
concepts: ["systémové prompty AI modelů", "transparentnost AI systémů", "prompt engineering", "bezpečnostní omezení AI", "tool use a agentic capabilities"]
entities: ["Anthropic", "Claude", "Simon Willison"]
source: brain-ingest-local
---

# Změny v systémovém promptu Claude Opus 4.6 až 4.7

**URL**: https://simonwillison.net/2026/apr/18/opus-system-prompt/

## Key Idea

Anthropic jako jediná velká AI firma zveřejňuje systémové prompty svých modelů. Článek analyzuje rozdíly mezi verzemi Claude Opus 4.6 a 4.7, které odhalují důležité změny v chování AI asistenta.

## Claims

- Claude 4.7 má výrazně rozšířenou sekci o bezpečnosti dětí s novým tagem <critical_child_safety_instructions>
- Nový prompt učí Claude být méně upovídaný a méně se ptát na detaily - preferuje akci před klarifikací
- Claude nyní má tool_search mechanismus pro kontrolu dostupných nástrojů před tvrzením, že něco nemůže udělat
- Odstraněna byla sekce o vyhýbání se slovům 'genuinely', 'honestly', 'straightforward' - model už se takto nechová
- Přidána ochrana proti screenshot útokům nutícím model k jednoslovným odpovědím na kontroverzní otázky
- Claude má k dispozici 23 nástrojů včetně bash_tool, web_search, conversation_search a visualize

## Relevance for STOPA

Ukazuje důležitost systémových promptů pro řízení chování AI agentů a transparentnosti v jejich publikování. Pro STOPA orchestraci je klíčové porozumění, jak prompty ovlivňují spolehlivost a bezpečnost AI systémů při jejich integraci.

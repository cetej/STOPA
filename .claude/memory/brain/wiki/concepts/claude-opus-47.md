---
title: Claude Opus 4.7
type: concept
category: concepts
source: https://www.anthropic.com/news/claude-opus-4-7
date: 2026-04-19
tags: [claude, anthropic, model-release, vision, coding, cybersecurity]
related: [agentic-engineering-patterns, automated-alignment-researchers, claude-code-design-space]
---

# Claude Opus 4.7

## Přehled
Nová verze Claude modelu od Anthropic (duben 2026). Klíčové vylepšení oproti Opus 4.6: 3× více produkčních tasků v SWE-Bench, 98.5% vs 54.5% visual acuity, rozšířená vision schopnost.

## Klíčové schopnosti
- **Software Engineering**: Komplexní long-running coding tasks se self-verifikací před reportováním výsledků
- **Enhanced Vision**: Až 2,576px long edge (~3.75 megapixely) — 3× více než předchozí Claude modely
- **Instruction Following**: Výrazně lepší, interpretuje direktivy doslova (nutné retunovat stávající prompty)
- **Multimodal**: Čtení chemických struktur, technické diagramy, extrakce dat z komplexních vizuálů

## Výkonnost
- 3× více produkčních tasků než Opus 4.6 (Rakuten-SWE-Bench)
- 98.5% visual-acuity performance vs 54.5% pro Opus 4.6 (XBOW testing)
- 10–15% zlepšení na complex multi-step workflows s méně tool errors
- State-of-the-art: Finance Agent evaluation, GDPval-AA benchmark

## Technické detaily
- **Tokenizer**: 1.0–1.35× více tokenů závislé na typu obsahu (breaking change pro token budgeting)
- **Effort Levels**: Nový `xhigh` setting pro jemnější reasoning-latency control
- **Memory**: Lepší file system-based memory retention přes multi-session práci
- **Model ID**: `claude-opus-4-7`
- **Cena**: $5/M input, $25/M output (zachováno oproti Opus 4.6)

## Kybernetická bezpečnost
Anthropic záměrně snížil cyber-capabilities oproti předchozímu preview. Automatická detekce + blokování high-risk cybersecurity requests. Cyber Verification Program umožňuje legitimní security research přístup.

## STOPA relevance
- Model ID `claude-opus-4-7` pro produkční použití (nahrazuje `claude-opus-4-6`)
- `xhigh` effort tier pro maximální reasoning (orchestrate deep tier)
- Tokenizer změna: přepočítat token budgets pro existující pipeline
- Doslovna interpretace instrukcí = méně ambiguity, ale nutný prompt audit

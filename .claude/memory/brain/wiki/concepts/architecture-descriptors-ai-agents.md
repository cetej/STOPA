---
title: Formal Architecture Descriptors for AI Coding Agents
type: concept
category: concepts
source: https://arxiv.org/abs/2604.13108
date: 2026-04-19
tags: [coding-agents, codebase-navigation, architecture, ai-engineering, documentation]
related: [agentforge, agentic-engineering-patterns, claude-code-design-space]
---

# Formal Architecture Descriptors jako Navigation Primitives (arXiv:2604.13108)

## Přehled
"Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents" (Ruoqi Jin, 2026). Formálně strukturovaná architektonická dokumentace kódu dramaticky snižuje exploratory overhead AI coding agentů.

## Klíčové výsledky
- Architecture context → **−33–44% navigačních kroků** (p=0.009, Cohen's d=0.92)
- Auto-generované deskriptory: **100% přesnost** vs 80% blind baseline (p=0.002)
- Field study 7,012 sessions: **−52% behavioral variance** agentů

## Formáty a kritická výjimka
Testovány S-expression, JSON, YAML, Markdown — žádný signifikantní výkonnostní rozdíl.

**Kritická bezpečnostní výjimka**: YAML "silently corrupts 50% of errors" — S-expressions detekují VŠECHNY strukturální chyby. Pro kritické systémy → S-expressions nebo JSON.

## Forge toolkit
Nástroj `intent.lisp` pro generování architecture descriptorů. Auto-generace dosahuje 100% přesnosti — manuální psaní deskriptorů není nutné.

## Metodologie (3 studie)
1. Controlled experiment — 24 lokalizačních tasků, Claude Sonnet 4.6
2. Artifact-vs-process comparison — 15 tasků
3. Observational field study s error injection testing

## Implikace pro STOPA
- Architecture deskriptory = **low-cost, high-ROI** enhancement pro agent teams
- Scout agent by měl generovat intent.lisp-style deskriptory pro target projekty
- S-expressions pro kritické config soubory (ne YAML pro error-prone struktury)
- Redukce variance agentů (-52%) = přímý dopad na orchestrace konzistenci

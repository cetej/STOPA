---
title: SWE-Adept: Framework pro analýzu kódu a řešení problémů pomocí LLM agentů
url: https://arxiv.org/abs/2603.01327
date: 2026-04-25
concepts: ["LLM agentic framework", "depth-first search navigace kódu", "adaptivní plánování", "Git-based version control", "working memory s checkpointy", "repository-level software engineering", "lokalizační a rezoluční agenti", "test-driven code modification"]
entities: ["Kang He", "Kaushik Roy", "SWE-Bench Lite", "SWE-Bench Pro"]
source: brain-ingest-local
---

# SWE-Adept: Framework pro analýzu kódu a řešení problémů pomocí LLM agentů

**URL**: https://arxiv.org/abs/2603.01327

## Key Idea

SWE-Adept je dvouagentní framework založený na velkých jazykových modelech, který kombinuje hloubkové prohledávání kódové báze pro lokalizaci problémů s adaptivním plánováním a Git-based verzováním pro systematické řešení softwarových chyb.

## Claims

- LLM modely mají potíže s úlohami na úrovni celých repozitářů, které vyžadují navigaci v kódové bázi a systematické iterativní úpravy
- Agent-directed depth-first search minimalizuje irelevantní obsah v kontextovém okně a zlepšuje přesnost lokalizace problémů
- SWE-Adept konzistentně překonává předchozí přístupy s až 4,7% zlepšením míry úspěšného řešení problémů
- Specializované nástroje pro sledování postupu a Git-based version control umožňují spolehlivé větvení a vracení neúspěšných úprav

## Relevance for STOPA

Framework demonstruje pokročilé principy orchestrace více agentů se sdílenou pamětí a specializovanými nástroji, což je klíčové pro STOPA architekturu. Kombinace lokalizačního a resolučního agenta s verzováním a checkpointy ukazuje efektivní pattern pro složité víceagentní workflows.

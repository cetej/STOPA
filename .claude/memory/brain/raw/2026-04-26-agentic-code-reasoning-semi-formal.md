---
title: Agentic Code Reasoning: Sémantická analýza kódu bez spouštění
url: https://arxiv.org/abs/2603.01896
date: 2026-04-26
concepts: ["Agentic Code Reasoning", "Semi-formal reasoning", "Patch equivalence verification", "Fault localization", "Code question answering", "Execution-free analysis", "Structured prompting"]
entities: ["Shubham Ugare", "Satish Chandra", "Defects4J", "RubberDuckBench"]
source: brain-ingest-local
---

# Agentic Code Reasoning: Sémantická analýza kódu bez spouštění

**URL**: https://arxiv.org/abs/2603.01896

## Key Idea

Článek představuje semi-formální reasoning - strukturovanou metodu promptování, která umožňuje LLM agentům analyzovat a uvažovat o sémantice kódu bez nutnosti jeho spuštění. Metoda vyžaduje explicitní konstrukci premis, trasování cest a odvozování formálních závěrů.

## Claims

- Semi-formální reasoning zlepšuje přesnost verifikace ekvivalence patchů z 78% na 88% na kurátorovaných příkladech a dosahuje 93% na real-world agentech generovaných patchích
- Pro odpovídání na otázky o kódu dosahuje metoda 87% přesnosti na RubberDuckBench
- U lokalizace chyb na Defects4J zvyšuje semi-formální reasoning Top-5 přesnost o 5 procentních bodů oproti standardnímu uvažování
- Strukturované agentní uvažování umožňuje smysluplnou sémantickou analýzu kódu bez spouštění, což otevírá aplikace v RL training, code review a statické analýze

## Relevance for STOPA

Pro STOPA orchestraci je důležitá možnost sémantické verifikace a analýzy kódu bez spouštění. Semi-formální reasoning může zlepšit kvalitu code review a umožnit spolehlivější automatizované validace v rámci orchestračních procesů.

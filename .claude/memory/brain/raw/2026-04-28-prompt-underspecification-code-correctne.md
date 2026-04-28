---
title: Kdy neúplná specifikace promptu zlepšuje správnost kódu generovaného LLM
url: http://arxiv.org/abs/2604.24712v1
date: 2026-04-28
concepts: ["generování kódu pomocí LLM", "robustnost vůči mutacím promptů", "strukturální redundance v zadání", "pod-specifikace vs. správnost kódu", "zavádějící lexikální vodítka"]
entities: ["Amal AKLI", "Mike PAPADAKIS", "Maxime CORDY", "Yves Le TRAON", "HumanEval", "LiveCodeBench"]
source: brain-ingest-local
---

# Kdy neúplná specifikace promptu zlepšuje správnost kódu generovaného LLM

**URL**: http://arxiv.org/abs/2604.24712v1

## Key Idea

Studie ukazuje, že robustnost LLM vůči mutacím promptů závisí na struktuře zadání – strukturovanější prompty (LiveCodeBench) jsou odolnější než minimální (HumanEval), a překvapivě neúplná specifikace může někdy zlepšit správnost narušením zavádějících vodítek.

## Claims

- Robustnost LLM vůči změnám promptů není fixní vlastnost modelu, ale silně závisí na struktuře promptu
- Stejné mutace způsobující degradaci na HumanEval mají téměř nulový efekt na LiveCodeBench díky strukturální redundanci
- Pod-specifikace promptů může zlepšit správnost kódu narušením zavádějících lexikálních nebo strukturálních vodítek, která spouštějí nesprávné retrieval strategie
- Strukturně bohaté popisy úloh mohou významně zmírnit negativní efekty pod-specifikace a někdy dokonce zlepšit správnost

## Relevance for STOPA

Pro STOPA orchestraci je klíčové porozumění tomu, jak strukturovat prompty pro spolehlivé generování kódu – studie ukazuje, že redundance a strukturovanost zadání může být efektivnější než přesná specifikace, což má dopady na design prompt templates pro agenты.

---
title: SWE-AGILE: Framework pro efektivní správu kontextu v softwarových agentech
url: https://arxiv.org/abs/2604.11716
date: 2026-04-26
concepts: ["Dynamic Reasoning Context", "System-2 reasoning", "Chain-of-Thought (CoT)", "Reasoning Digests", "Lost-in-the-Middle degradation", "Multi-turn SWE task", "Context explosion"]
entities: ["Shuquan Lian", "Juncheng Liu", "Yazhe Chen", "Yuhong Chen", "Hui Li", "KDEGroup"]
source: brain-ingest-local
---

# SWE-AGILE: Framework pro efektivní správu kontextu v softwarových agentech

**URL**: https://arxiv.org/abs/2604.11716

## Key Idea

SWE-AGILE řeší zásadní dilema u autonomních softwarových agentů: jak udržovat hloubku uvažování bez exploze kontextu. Používá strategii "sliding window" s detailním uvažováním pro okamžitou kontinuitu a komprimuje historii do stručných digestů.

## Claims

- Předchozí ReAct-style přístupy postrádají explicitní System-2 reasoning pro hlubokou analýzu a složité edge cases
- Aplikace reasoning modelů s rozšířeným CoT na multi-turn SWE úlohy vytváří dilema mezi context explosion a redundantním re-reasoningem
- SWE-AGILE dosahuje nového standardu pro 7B-8B modely na SWE-Bench-Verified pouze s 2.2k trajektoriemi a 896 úlohami
- Dynamic Reasoning Context strategie udržuje sliding window detailního uvažování a komprimuje historii do Reasoning Digests

## Relevance for STOPA

Framework ukazuje konkrétní řešení pro správu kontextu v multi-agent systémech, což je klíčové pro orchestraci STOPA. Strategie komprese historického uvažování do digestů a sliding window přístup může inspirovat efektivnější koordinaci mezi agenty v STOPA architektuře.

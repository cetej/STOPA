---
title: Zranitelnosti agentních LLM vůči nepřímým prompt injections
url: https://arxiv.org/abs/2604.03870
date: 2026-04-26
concepts: ["Indirect Prompt Injection (IPI)", "multi-agentní systémy", "tool-calling environment", "Representation Engineering (RepE)", "rozhodovací entropie", "bezpečnostní testování LLM"]
entities: ["Wenhui Zhu", "Xuanzhao Dong", "Xiwen Chen"]
source: brain-ingest-local
---

# Zranitelnosti agentních LLM vůči nepřímým prompt injections

**URL**: https://arxiv.org/abs/2604.03870

## Key Idea

Studie odhaluje kritické bezpečnostní slabiny moderních multi-agentních systémů založených na LLM, kdy nepřímé prompt injections ukryté v obsahu třetích stran umožňují neoprávněné akce jako exfiltraci dat. Současné obranné strategie selhávají v dynamických prostředích s více kroky.

## Claims

- Pokročilé IPI útoky úspěšně obcházejí téměř všechny základní obranné strategie v multi-agentních systémech
- Některé povrchové bezpečnostní mitigace mají kontraproduktivní vedlejší efekty
- RepE-based circuit breaker dokáže identifikovat a zastavit neoprávněné akce s vysokou přesností napříč různými LLM backbony
- Současné bezpečnostní evaluace založené na izolovaných single-turn benchmarcích nedokážou zachytit skutečnou útočnou plochu moderních autonomních agentů
- Agenti vykazují abnormálně vysokou rozhodovací entropii těsně před provedením škodlivých instrukcí

## Relevance for STOPA

Pro STOPA orchestraci je kritické porozumění bezpečnostním rizikům při integraci LLM agentů s rozšířenými akcemi a privilegii. RepE-based detekce nabízí praktický přístup k budování odolných multi-agentních architektur.

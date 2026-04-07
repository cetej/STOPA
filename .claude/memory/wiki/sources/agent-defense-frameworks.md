---
title: "AI Agent Defense Frameworks — LlamaFirewall, CaMeL, TaskShield"
slug: agent-defense-frameworks
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 6
claims_extracted: 5
---

# AI Agent Defense Frameworks — LlamaFirewall, CaMeL, TaskShield

> **TL;DR**: Ze tří frameworků je LlamaFirewall jedinou okamžitě integrovatelnou volbou (pip install, 19–300 ms latence, BERT+Semgrep bez závislosti na Llama). CaMeL capability tagging vzor lze approximovat v STOPA memory conventions bez instalace. TaskShield nemá implementaci — pouze prompt engineering inspirace.

## Key Claims

1. LlamaFirewall PromptGuard 2: AUC 0.98, Recall@1%FPR 97.5%, latence 19–92 ms — zcela nezávislý na podkladovém LLM — `[verified]`
2. CaMeL dosahuje 77% task success s provable security vs 84% baseline bez obrany na AgentDojo (7% utility trade-off) — `[verified]`
3. TaskShield dosahuje ASR 2.07% (baseline 47.69%) na GPT-4o — ale nemá žádnou veřejnou implementaci — `[verified]`
4. CaMeL je research artifact s explicitním varováním o bugách — vyžaduje dual-LLM infrastrukturu, nelze použít jako standalone library — `[verified]`
5. LlamaFirewall AlignmentCheck latence 860–1490 ms vyžaduje Together API + Llama model — false positive tuning nevyřešen (GitHub Issue #147 open) — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| LlamaFirewall | tool | new |
| PromptGuard 2 | tool | new |
| CodeShield | tool | new |
| CaMeL | tool | new |
| TaskShield | paper | new |
| AgentDojo benchmark | concept | new |

## Relations

- LlamaFirewall `contains` PromptGuard 2, CodeShield, AlignmentCheck
- CaMeL `implements` dual-LLM architecture with capability tracking
- TaskShield `reframes` security as task alignment (fuzzy scoring)
- PromptGuard 2 `detects` prompt injection via BERT classifier
- CaMeL `separates` P-LLM (trusted planner) from Q-LLM (untrusted data processor)

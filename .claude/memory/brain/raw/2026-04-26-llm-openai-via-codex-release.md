---
title: llm-openai-via-codex: Přístup k OpenAI modelům přes Codex předplatné
url: https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/
date: 2026-04-26
concepts: ["credential hijacking", "API gateway", "LLM access tools", "plugin systém pro LLM"]
entities: ["Simon Willison", "OpenAI", "Codex CLI", "GPT-5.5"]
source: brain-ingest-local
---

# llm-openai-via-codex: Přístup k OpenAI modelům přes Codex předplatné

**URL**: https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/

## Key Idea

Simon Willison vydal nástroj llm-openai-via-codex 0.1a0, který umožňuje přistupovat k OpenAI modelům (včetně GPT-5.5) pomocí existujícího Codex CLI předplatného tím, že 'unese' přihlašovací údaje z Codex CLI pro API volání.

## Claims

- Plugin llm-openai-via-codex 0.1a0 umožňuje přístup k OpenAI modelům přes existující Codex předplatné
- Nástroj funguje tak, že přebírá přihlašovací údaje z Codex CLI pro API volání v LLM
- Tato metoda je popsána jako 'semi-oficiální backdoor API' pro přístup k GPT-5.5

## Relevance for STOPA

Ukazuje techniky pro integraci různých LLM API a možnosti alternativního přístupu k modelům, což je relevantní pro flexibilní orchestraci různých AI služeb v rámci STOPA platformy.

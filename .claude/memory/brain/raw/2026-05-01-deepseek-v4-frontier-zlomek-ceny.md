---
title: DeepSeek V4 – téměř frontier model za zlomek ceny
url: https://simonwillison.net/2026/Apr/24/deepseek-v4/
date: 2026-05-01
concepts: ["Mixture of Experts architektura", "open weights modely", "efektivita inference při dlouhém kontextu", "cenová konkurenceschopnost AI modelů", "kvantizace modelů"]
entities: ["DeepSeek", "Simon Willison", "OpenAI", "Anthropic", "Google", "Hugging Face", "OpenRouter", "Unsloth"]
source: brain-ingest-local
---

# DeepSeek V4 – téměř frontier model za zlomek ceny

**URL**: https://simonwillison.net/2026/Apr/24/deepseek-v4/

## Key Idea

Čínská AI laboratoř DeepSeek vydala modely V4-Pro (1.6T parametrů) a V4-Flash (284B parametrů) s výrazně nižšími cenami než konkurenční frontier modely od OpenAI, Anthropic a Google, při zachování konkurenceschopného výkonu.

## Claims

- DeepSeek-V4-Pro je s 1.6T parametry nově největší open weights model, převyšující Kimi K2.6 (1.1T) a GLM-5.1 (754B)
- V4-Flash stojí $0.14/M tokenů input a $0.28/M output, což je nejlevnější ze všech malých frontier modelů
- V4-Pro dosahuje pouze 27% single-token FLOPs a 10% KV cache velikosti oproti V3.2 při 1M token kontextu
- Podle vlastních benchmarků DeepSeek zaostává za GPT-5.4 a Gemini-3.1-Pro přibližně o 3-6 měsíců
- DeepSeek-V4-Pro stojí $1.74/M input a $3.48/M output, což je levnější než všechny velké frontier modely

## Relevance for STOPA

Pro STOPA orchestraci je relevantní dostupnost velmi nákladově efektivních open weights modelů s velkým kontextovým oknem (1M tokenů), které mozhnou snížit operační náklady při zachování výkonu blízkého frontier modelům.

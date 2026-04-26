---
title: Prompt Injection v Snowflake a lokální běh velkých LLM modelů
url: https://simonwillison.net/2026/Mar/18/
date: 2026-04-26
concepts: ["prompt injection", "sandbox escape", "Mixture-of-Experts (MoE)", "kvantizace modelů", "streamování expertů z SSD", "autoresearch pattern", "deterministický sandboxing"]
entities: ["Snowflake Cortex Agent", "PromptArmor", "Dan Woods", "Qwen3.5-397B-A17B", "Apple", "Claude Code", "Andrej Karpathy"]
source: brain-ingest-local
---

# Prompt Injection v Snowflake a lokální běh velkých LLM modelů

**URL**: https://simonwillison.net/2026/Mar/18/

## Key Idea

Článek popisuje dvě významné bezpečnostní a technické zjištění: zranitelnost prompt injection v Snowflake Cortex AI, která umožnila únik z sandboxu, a průlomovou metodu pro běh 397B parametrového modelu na běžném MacBooku pomocí techniky streamování z SSD.

## Claims

- Snowflake Cortex Agent byl zranitelný vůči prompt injection útoku skrze GitHub README soubor, který způsobil spuštění malwaru pomocí process substitution vcat příkazu.
- Allow-listy pro příkazy agentů jsou inherentně nespolehlivé a je lepší používat deterministické sandboxy na vyšší úrovni.
- Dan Woods úspěšně spustil 397B parametrový Qwen model na MacBooku s 48GB RAM rychlostí 5.5+ tokenů/sekundu pomocí streamování 2-bit kvantizovaných expertů z SSD.
- Technika využívá Apple's 'LLM in a Flash' přístup, kde se drží v RAM pouze 5.5GB (embedding a routing), zatímco experti se streamují ze SSD.
- Kvalita 2-bit kvantizace byla nedostatečná pro tool calling, upgrade na 4-bit (209GB, 4.36 t/s) tento problém vyřešil.

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení bezpečnostních rizik prompt injection při integraci AI agentů a možností lokálního běhu velkých modelů s omezenými prostředky, což může ovlivnit architekturu a bezpečnostní opatření orchestračních systémů.

---
title: Kill-Chain Canaries — Prompt Injection Stage Tracking
type: concept
category: concepts
source: https://arxiv.org/abs/2603.28013
date: 2026-04-19
tags: [prompt-injection, security, multi-agent, safety, kill-chain, pipeline-security]
related: [prompt-injection-defense, claude-code-design-space, multi-agent-orchestration-protocols]
---

# Kill-Chain Canaries: Stage-Level Tracking of Prompt Injection (arXiv:2603.28013)

## Přehled
"Kill-Chain Canaries: Stage-Level Tracking of Prompt Injection Across Attack Surfaces and Model Safety Tiers" (Wang, Zhang, 2026). Nová metodologie trackující prompt injection přes 4 attack stages pomocí kryptografických tokenů.

## Kill-Chain metodologie
Cryptographic "canary" tokeny trackované přes 4 stages:
1. **EXPOSED** — payload je viditelný modelu
2. **PERSISTED** — payload zapsán do memory/state
3. **RELAYED** — payload přeposlán dalšímu agentovi
4. **EXECUTED** — payload způsobí akci

## Klíčové výsledky (950 experimentů, 5 LLMs, 6 attack surfaces, 5 defense conditions)
| Model | Attack Success Rate |
|-------|-------------------|
| **Claude** | **0/164 (0%)** — blokuje na memory-write |
| GPT-4o-mini | 53% propagation rate |
| DeepSeek | 0%/100% variance across surfaces |

## Highest-Leverage Defense
> "Write-node placement je nejvýše pákový safety rozhodnutí — routování writes přes verified model eliminuje propagaci."

## Mezery obrany
- Všechny 4 testované defense mechanismy selhávají na ≥1 attack surface (channel mismatch)
- Invisible whitefont PDF payloads ≈ stejně efektivní jako visible-text attacks
- Rendered-layer screening nestačí

## Klíčové přeformulování
Prompt injection = **pipeline-architecture problem**, ne model-specific vulnerability. Výsledky závisí na system design, ne jen na výběru modelu.

## Implikace pro STOPA
- Memory-write nodes jsou **kritické místo pro security gating**
- Multi-agent pipeline design = bezpečnostní rozhodnutí od prvního dne
- Claude má nejlepší výsledky (0% ASR) ze sledovaných modelů na memory-write stage
- STOPA orchestrace: vždy routovat writes přes "verified model" (Claude, ne worker)
- Rozšiřuje `prompt-injection-defense.md` o kill-chain stage tracking metodologii

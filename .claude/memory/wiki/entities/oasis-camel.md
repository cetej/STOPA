---
name: OASIS (CAMEL-AI simulation engine)
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [miroshark-research]
tags: [multi-agent, orchestration, research]
---

# OASIS (CAMEL-AI simulation engine)

> Open Agent Social Interaction Simulations — CAMEL-AI framework pro simulaci sociálních sítí s LLM agenty. Používán v MiroShark jako "wonderwall" bundle.

## Key Facts

- Paralelní simulace 3 platforem přes asyncio.gather: Twitter, Reddit, Polymarket (ref: sources/miroshark-research.md)
- Sliding-window round memory: staré kola kompaktuje background LLM
- Typicky ~40 kol × 100+ agentů per simulace
- Vyžaduje OpenAI-kompatibilní API — nelze přímo použít Claude Code v simulačních kolech
- Z výzkumného kontextu, ne production-validated pro reálné prediction markets

## Relevance to STOPA

Sliding-window memory pattern je relevantní pro /autoloop skill — kompakce starých iterací background modelem. Architektura paralelních platforem (asyncio.gather) je vzor pro STOPA parallel agent execution.

## Mentioned In

- [MiroShark Research Report](../sources/miroshark-research.md)

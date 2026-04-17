# Multi-Agent Orchestration for HPC — Planner-Executor at Exascale

**Source:** arXiv:2604.07681 (Argonne National Laboratory)
**Added:** 2026-04-17

## Core Idea

Single-agent systémy vytvářejí serialization bottlenecky při large-scale vědeckých simulacích. Exascale computing (Aurora, Frontier) nabízí tisíce souběžných výpočetních jader — ale AI orchestrace za nimi zaostává.

Řešení: Hierarchická **planner-executor architektura** s centrálním plánovacím agentem a swarmem paralelních executor agentů koordinovaných přes sdílený MCP server.

## Architektura

```
Central Planner Agent
    ↓ task assignment
[Executor 1] [Executor 2] ... [Executor N]
    ↑ results via shared MCP server ↓
        Parsl Workflow Engine (HPC scheduling)
```

- **Planner**: dynamicky rozděluje workload, reaguje na výsledky executorů
- **Executors**: souběžné zpracování subtasků, bez vzájemné komunikace
- **Shared MCP server**: sdílený kontext a koordinace (ne přímá agent-agent komunikace)
- **Parsl**: HPC-native workflow engine, zvládá job queueing na supercomputerech

## Aplikace

Materials screening: Metal-Organic Framework screening na Aurora supercomputeru.
Model: gpt-oss-120b (open weights, scale-deployment).

## Klíčové principy

**Shared MCP server jako backbone**: agenti nepotřebují přímou komunikaci — sdílený kontext přes MCP server řeší koordinaci. Emergentní koordinace bez explicit agent messaging.

**Serialization vs Parallelization**: každý subtask je nezávislý → perfect horizontal scaling. Planner přiděluje podle dostupné kapacity, ne fixního pořadí.

## Significance pro STOPA

STOPA `/orchestrate` implementuje identický planner-executor vzor:
- Orchestrator = Central Planner Agent  
- Worker agents = Executor swarm
- Shared state.md + memory/ = Shared MCP server backbone

HPC paper validuje tento vzor i pro fyzické výpočty na úrovni exascale computing. **Architektura je domain-agnostic**: software engineering, materials science, data processing — všude planner-executor škáluje.

Konkrétní insight pro STOPA: farm tier (5-8 agents) přesně odpovídá tomuto vzoru — sdílený kontext (state.md) umožňuje executor agentům pracovat nezávisle bez cross-agent komunikace.

## Connections

- Applied-in: [[stopa]] — planner-executor vzor = /orchestrate + worker agents + shared state.md
- Related-to: [[context-engineering]] — shared MCP server je implementace shared context window pro paralelní agenty

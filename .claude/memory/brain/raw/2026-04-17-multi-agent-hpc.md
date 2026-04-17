---
date: 2026-04-17
source_type: url
source_url: https://arxiv.org/abs/2604.07681
---

# Multi-Agent Orchestration for High-Throughput Materials Screening on Leadership-Class HPC (arXiv:2604.07681)

Autoři: Thang Duc Pham et al. (Argonne National Laboratory).

Problem: Single-agent systémy vytvářejí serialization bottlenecky při large-scale simulacích na HPC (High Performance Computing) clusterech. Exascale computing vyžaduje tisíce paralelních úloh.

Řešení: Hierarchická planner-executor architektura:
- Central planning agent: dynamicky rozděluje workload, přiřazuje subtasky
- Swarm of parallel executor agents: zpracovávají subtasky souběžně
- Shared MCP server: koordinace přes Model Context Protocol

Implementace:
- Parsl workflow engine pro HPC scheduling
- gpt-oss-120b model
- Aurora supercomputer (exascale)
- Aplikace: screening Metal-Organic Frameworks

Výsledky: Nízká orchestration overhead, vysoká task completion rate na Aurora supercomputeru.

Klíčový insight: Planner-executor pattern škáluje na exascale HPC stejně jako na software engineering — centralizovaná koordinace + distribuovaná exekuce. Sdílený MCP server umožňuje agentům sdílet kontext bez přímé komunikace.

---
date: 2026-04-17
source_type: url
source_url: https://arxiv.org/abs/2604.11623
---

# Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI Systems (arXiv:2604.11623)

Autor: Charafeddine Mouzouni.

Problem: Distribuovat správné znalosti správným agentům s správnými oprávněními a správnou freshness — v enterprise prostředí s komplexní governance. Analogie: container orchestration challenges pro data místo kódu.

Řešení: "Knowledge-architecture-as-code" — YAML manifesty deklarující, které znalosti jsou dostupné jakým agentům, za jakých podmínek, s jakými freshness požadavky.

Architektura:
- 6 formalizovaných core abstrakcí
- Reconciliation loop (analogie k Kubernetes reconciliation)
- Tříúrovňový model oprávnění pro agenty
- TLA+ verifikace (0 violations přes 4.6M stavů)

Výsledky:
- Intent routing: −19pp noise
- Všech 5 testovaných útoků zablokováno jen tříúrovňovým modelem (RBAC samotný 1 missed)
- RBAC alone miss: agenti odesílající confidential data emailem

Klíčový insight: RBAC nestačí pro agentic governance — agenti potřebují strukturální izolaci zabraňující přístupu k neautorizovaným znalostem A schvalovací mechanismy nezávislé na standardních oprávněních. Současné platformy (Microsoft, Salesforce, AWS, Google) nemají dostatečné strukturální záruky.

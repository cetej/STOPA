# Context Kubernetes — Declarative Enterprise Knowledge Orchestration

**Source:** arXiv:2604.11623
**Added:** 2026-04-17

## Core Idea

Container orchestration vyřešila problém distribuce softwaru ve scale. Context Kubernetes aplikuje stejný paradigma na distribuc znalostí pro agenty: **"delivering the right knowledge, to the right agent, with the right permissions, at the right freshness"**.

Klíčová analogie: Kubernetes reconciliation loop → Knowledge reconciliation loop. YAML manifesty pro kontejnery → YAML manifesty pro znalosti ("knowledge-architecture-as-code").

## Architektura

### 6 Core Abstrakcí
1. Knowledge namespaces (izolace)
2. Knowledge manifests (YAML deklarace)
3. Intent routing (přiřazení znalostí agentům)
4. Freshness policies (TTL a invalidation)
5. Permission tiers (kdo co smí číst)
6. Reconciliation loop (continuous consistency)

### Tříúrovňový model oprávnění

Kritický nález: RBAC (Role-Based Access Control) sám o sobě nestačí. Agenti potřebují:
- Strukturální izolaci (agent nevidí nepermittované knowledge)
- Schvalovací mechanismy nezávislé na standardních oprávněních
- Prevenci exfiltrace (agent s email nástrojem může odeslat data)

## Verifikace

TLA+ model-checking: **0 violations přes 4.6 miliony stavů**.

Testování 5 útočných scénářů:
- Intent routing: −19pp noise reduction
- RBAC alone: missed 1 attack (confidential data via email)
- 3-tier model: blocked all 5 attacks

## Současný stav platforem

Survey 4 platforem (Microsoft, Salesforce, AWS, Google): **žádná nemá dostatečné strukturální záruky** pro agentic knowledge governance.

## Significance pro STOPA

STOPA memory governance (key-facts.md, permissions, memory-files.md pravidla) sdílí základní filozofii — ale Context Kubernetes ji formalizuje:

- `key-facts.md` → Knowledge manifest
- Memory file size limits → Freshness policy
- Skills `permission-tier:` field → Permission tiers
- `/evolve` + `/sweep` → Reconciliation loop

Konkrétní aplikace: agent tools (`constrained-tools:`) + 3-tier permission model = Context Kubernetes light implementation v STOPA.

## Connections

- Related: [[context-engineering]] — CK je enterprise-scale implementace context engineering principů s formální governance
- Formalizes: [[agent-memory-taxonomy]] — permission model + freshness = governance vrstva nad write-manage-read loop
- Applied-in: [[stopa]] — memory governance, key-facts.md, permission-tier v SKILL.md sdílejí architekturu

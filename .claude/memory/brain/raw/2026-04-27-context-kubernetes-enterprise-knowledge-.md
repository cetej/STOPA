---
title: Context Kubernetes: Orchestrace znalostí pro AI agenty
url: https://arxiv.org/abs/2604.11623
date: 2026-04-27
concepts: ["context orchestration", "agentic AI", "knowledge governance", "RBAC", "declarative manifest", "permission model", "ACL filtering", "intent routing"]
entities: ["Charafeddine Mouzouni", "Kubernetes", "Microsoft", "Salesforce", "AWS", "Google"]
source: brain-ingest-local
---

# Context Kubernetes: Orchestrace znalostí pro AI agenty

**URL**: https://arxiv.org/abs/2604.11623

## Key Idea

Architektura pro orchestraci podnikových znalostí v agentic AI systémech, inspirovaná Kubernetes. Řeší doručení správných znalostí správnému agentovi se správnými oprávněními pomocí deklarativních manifestů a tří-úrovňového modelu oprávnění.

## Claims

- ACL filtrování eliminuje cross-domain úniky informací
- Intent routing snižuje šum o 19 procentních bodů
- Tří-úrovňový model oprávnění blokuje všech pět testovaných útočných scénářů, zatímco RBAC jeden scénář neodhalí
- TLA+ model-checking ověřil bezpečnostní vlastnosti na 4,6 milionu dosažitelných stavů bez jediného porušení
- Žádná ze čtyř hlavních platforem (Microsoft, Salesforce, AWS, Google) architektonicky neisoluje schvalovací kanály agentů

## Relevance for STOPA

Přímo relevantní pro STOPA orchestraci - poskytuje architektonický framework pro správu znalostí a oprávnění v multi-agentních systémech, řeší problém doručení kontextu s governance pravidly napříč organizací.

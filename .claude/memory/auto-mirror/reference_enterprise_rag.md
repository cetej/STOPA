---
name: reference_enterprise_rag
description: Enterprise RAG architecture — checklist of production requirements often missed in tutorials; relevant for ORAKULUM and any project adding RAG
type: reference
---

## Enterprise RAG — Co tutoriály vynechávají

Při návrhu RAG pro produkci (ORAKULUM, MONITOR, Záchvěv) ověřit tyto požadavky — ve veřejných přehledech (tweety, blogy) se rutinně vynechávají:

### Povinný checklist (non-negotiables)
1. **Document-level access control** — kdo smí číst co (multitenancy, role-based)
2. **PII detection + redaction** — před indexováním i před generováním
3. **Semantic cache** — identické/podobné dotazy → cached odpověď (cost + latency)
4. **Audit logging** — co bylo retrievnuto, kdy, kým, pro jaký dotaz
5. **Guardrails** — input safety (injekce) + output safety (halucinace, leakage)
6. **Observability/tracing** — Langfuse, Phoenix, nebo Arize; token cost per query
7. **Multi-tenancy** — izolace dat mezi klienty/projekty
8. **Cost budgeting** — per-query limit, per-user limit, circuit breaker

### Architektonické rozlišení (důležité pro design)
- **Indexing pipeline** = offline, při ingestování dokumentů (→ ne součást query flow)
- **Query pipeline** = online, při každém dotazu
- Tyto dvě věci NELZE míchat do jednoho schématu

### Technická poznámka: colBERT
colBERT ≠ "speciální embedding". Používá **late interaction** — token-level MaxSim matching. Je to jiná architektura než bi-encoder (FAISS). Vyžaduje jiný retrieval stack (Ragatouille, nebo nativní colBERT server).

### Zdroj
Analýza tweetu (@systemdesignone / @_avichawla area) o "8-stage Enterprise RAG", 2026-03-29.
Původní tweet: správné techniky (HyDE, RAPTOR, Self-RAG, RAGAS), ale "enterprise-grade" claim chybí výše uvedené.

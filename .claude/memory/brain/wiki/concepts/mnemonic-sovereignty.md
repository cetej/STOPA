---
title: Mnemonic Sovereignty — Security of Long-Term Memory in LLM Agents
category: concepts
tags: [memory, security, agent-safety, governance, long-term-memory]
sources: [arXiv:2604.16548]
updated: 2026-04-23
---

# Mnemonic Sovereignty — Security of Long-Term Memory in LLM Agents

**Paper**: arXiv:2604.16548  
**Authors**: Zehao Lin, Chunyu Li, Kai Chen (April 17, 2026)  
**Pages**: 63 pages, 7 figures, 10 tables

## Core Concept

**Mnemonic Sovereignty** = verifiable, recoverable governance over an agent's memory writes, reads, update authorization, and state forgetting. The field is shifting from training data leakage concerns to the harder problem: **can persistent agent memory be continuously compromised across sessions?**

## Memory Lifecycle Framework

Six phases where attacks can occur:

| Phase | Description | Primary Attack |
|-------|-------------|---------------|
| **Write** | Storing new information | Memory poisoning |
| **Store** | Persistence layer | Availability attacks |
| **Retrieve** | Recall from store | Retrieval corruption |
| **Execute** | Acting on retrieved memory | Control-flow hijacking |
| **Share** | Cross-agent propagation | Cross-agent contamination |
| **Forget/Rollback** | Deletion or rollback | Rollback vulnerabilities |

## Attack Categories

1. **Memory poisoning** — malicious writes corrupt future behavior
2. **Extraction attacks** — sensitive data leaked via retrieval
3. **Retrieval corruption** — manipulating what gets recalled
4. **Control-flow hijacking** — memory content alters agent decisions
5. **Cross-agent propagation** — attack spreads between agents sharing memory
6. **Rollback vulnerabilities** — inability to safely revert to a clean state

## Critical Gap

Current literature concentrates on write- and retrieve-time integrity attacks. **No existing architecture addresses all nine governance primitives** (write authorization, read authorization, update authorization, forget/rollback, cross-agent isolation, integrity verification, confidentiality, availability, auditability).

## Future Direction

"Using LLMs themselves for memory security remains sparse yet essential." — LLM-as-memory-auditor pattern.

## STOPA Relevance

STOPA's memory system has partial governance:
- ✅ Write authorization: learning-admission.py hook (write-time gate)
- ✅ Integrity: commit-invariants check on edits
- ✅ Auditability: git history = audit trail
- ❌ Cross-agent isolation: agents share memory/ freely — no propagation control
- ❌ Forget/Rollback: no safe rollback mechanism for poisoned memories
- ❌ Confidentiality: all agents read all memory (no access tiers)

Priority upgrade: cross-agent memory isolation + rollback protocol.

## Related Concepts

→ [prompt-injection-defense.md](prompt-injection-defense.md)  
→ [kill-chain-canary.md](kill-chain-canary.md)  
→ [agent-memory-taxonomy.md](agent-memory-taxonomy.md)  
→ [persistent-identity-agents.md](persistent-identity-agents.md)

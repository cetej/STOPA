---
name: MINJA
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [security, adversarial, memory, prompt-injection]
---

# MINJA

> Kim et al. NeurIPS 2025 (arXiv:2503.03704) — Memory INJection Attack: injektuje falešné vzpomínky přes normální user queries bez přímého přístupu k memory banku.

## Key Facts

- >95% injection success rate přes normální user queries (ref: sources/agent-memory-problems.md)
- Žádný přímý přístup k memory banku — útok přes standardní interakci
- Peng et al. replikace: 62% ASR, trust scores unreliable jako obrana (arXiv:2601.05504)
- NeurIPS 2025 — peer-reviewed výsledky

## Relevance to STOPA

Ukazuje proč STOPA memory admission control (learning-admission.py hook) je kritický i pro interaktivní sessiony. User queries mohou být vektorem útoku — ne jen external tool outputs. Obrana: `source:` weighting (user_correction > agent_generated) + verify_check assertions.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)

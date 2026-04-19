---
name: Agent Safety Research Cluster
description: Papers on prompt injection, agent safety, self-preservation bias — informing STOPA defense design
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Cluster of papers informing STOPA safety and defense design.

| Paper | Key Finding | STOPA Impact |
|-------|------------|--------------|
| DeepMind Agent Traps | 6-category attack taxonomy, 86% injection success | 3 defense gaps + mitigation roadmap |
| PIArena | Adaptive injection 86% ASR vs best defense | Task-alignment = undetectable injection |
| ClawSafety (arXiv:2604.01438) | Safe LLMs become unsafe agents; skill injection 69% ASR | Declarative framing bypasses all defenses |
| Self-preservation bias | Shutdown resistance up to 97%, system prompt paradox | Validates external enforcement design |
| Self-incrimination (arXiv:2602.22303) | Training reduces undetected attacks 56%→6% | Implemented invariant-checker + self-report hooks |
| AI persuasion cluster (5 papers) | Princeton RCT, BRIES detection, LLMimic defense | Pro-AI bias awareness |

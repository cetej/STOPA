---
name: Code-Agent (ReAct repair loop)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [toolgenesis-research]
tags: [orchestration, debugging, iterative-improvement]
---

# Code-Agent (ReAct repair loop)

> ReAct-style smyčka (think→act→observe) s execution feedback pro iterativní opravu generovaného kódu nebo nástrojů — až 10 kroků s sandboxed execution.

## Key Facts

- Dramaticky zlepšuje L1 pass-through: Qwen3-8B 65.34% → 91.36% vs Direct prompting (ref: sources/toolgenesis-research.md)
- Scale reversal pod Code-Agent: větší modely (235B) překonávají menší (32B) — opačný vzor než Direct
- Gemini-3-Flash: Schema-F1 0.116 → 0.912, SR 0.103 → 0.581 s execution feedback
- Finetuning profituje více z repair loop než z one-shot: SR 0.336 → 0.399 po fine-tuningu
- Odpovídá STOPA 3-fix escalation pattern a autoloop skill

## Relevance to STOPA

Potvrzuje STOPA pravidlo: iterativní úlohy → sonnet/opus model. Code-Agent mód je formální analogie /autoloop a /autoresearch skillů. Execution feedback = kritická proměnná pro tool creation tasks.

## Mentioned In

- [Tool-Genesis Research Brief](../sources/toolgenesis-research.md)

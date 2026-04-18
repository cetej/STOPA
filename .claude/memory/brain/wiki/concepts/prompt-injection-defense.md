---
title: Prompt Injection Defense — Privilege Separation and Structural Mitigations
category: concepts
tags: [security, prompt-injection, privilege-separation, agent-safety, structured-output]
sources: [raw/2026-04-18-openclaw-prompt-injection-defense.md, raw/2026-04-18-prompt-injection-competition.md]
updated: 2026-04-18
---

# Prompt Injection Defense — Privilege Separation and Structural Mitigations

Synthesized from two papers: OpenClaw (arXiv:2603.13424) and the large-scale injection competition (arXiv:2603.15714).

## The Threat Landscape (Competition Paper)

Large-scale red-teaming results (464 participants, 272K attempts, 41 scenarios):

| Model | Attack Success Rate |
|-------|-------------------|
| Claude Opus 4.5 | **0.5%** |
| Gemini 2.5 Pro | **8.5%** |

Critical finding: **harmful actions often leave no visible trace in user-facing responses** — users unknowingly accept compromised outputs.

Universal attack strategies transferable across model families identified in **21/41 behaviors** — these attacks work on multiple models with minor adaptation.

**Capability ≠ robustness**: more capable models are not necessarily more robust.

## Structural Defenses (OpenClaw)

Two-mechanism pipeline achieving **0% attack success rate** on 649 LLMail-Inject attacks:

### 1. Agent Privilege Separation (~323× improvement over baseline)

OS-style separation: divide agents by privilege level and tool access.
- **High-privilege agent**: executes actions, has tool access
- **Low-privilege agent**: processes untrusted content (tool outputs, web content, emails)
- No direct communication path from low-privilege to high-privilege actions

### 2. JSON Formatting (~7× improvement alone)

Strip persuasive natural language before processing. Tool outputs get converted to structured JSON before the main agent sees them — removes injected instructions embedded in NL prose.

### Combined: 0% ASR

Agent isolation is the dominant factor. JSON formatting adds defense-in-depth.

## Key Takeaways

1. **Architecture > prompting** for injection defense
2. **Privilege separation** is the most effective single mechanism
3. **Structural formatting** helps but isn't sufficient alone
4. Attacks are **model-transferable** — no model is immune by capability alone

## STOPA Relevance

When STOPA agents process external content (web scraping, email, tool outputs), that content should pass through a low-privilege extraction layer before reaching the main orchestrator. JSON formatting of tool outputs is a low-cost first step.

## Related Concepts

→ [tool-use-evolution.md](tool-use-evolution.md)  
→ [gaama.md](gaama.md)

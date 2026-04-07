---
date: 2026-04-07
type: best_practice
severity: high
component: hook
tags: [judgment, scripts, reliability, deterministic, hooks, orchestration]
summary: LLMs handle judgment (synthesis, prioritization, drafting), Python scripts handle deterministic work (API calls, file I/O, timestamps). Mixing LLMs into deterministic paths causes unpredictable failures and erodes trust. Validated by production deployment of 100+ LP fundraise pipeline.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: manual
---

# Judgment-Script Separation for Reliable AI Systems

Production deployment ("Stella" on OpenClaw, 2026-04-06) confirms: the most critical design rule for a reliable AI assistant is strict layer separation.

**LLM layer**: synthesis, prioritization, drafting, reasoning over ambiguous input.

**Script layer**: reading files, calling APIs, sending messages, comparing timestamps, any computation with a deterministic correct answer.

**Failure mode**: pushing deterministic work through an LLM produces silent, unpredictable errors that accumulate and eventually destroy trust in the whole system.

**STOPA validation**: This is exactly what STOPA's hook architecture implements — hooks (Python) enforce deterministic rules, skills (LLM) handle reasoning. Critical Pattern #4 ("Harness > Skill for deterministic processes") is the same principle. This external production deployment at scale confirms the design.

**Implication for new skill design**: any skill that automates external API calls (email, calendar, task sync) should use a script wrapper that handles the I/O deterministically, with the LLM only deciding WHAT to do, not HOW to execute it.

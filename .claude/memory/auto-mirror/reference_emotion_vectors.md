---
name: Anthropic emotion vectors research
description: Paper showing Claude has functional desperation/calm vectors that causally affect behavior — basis for calm-steering hook
type: reference
---

Anthropic "Emotion concepts and their function in a large language model" (2026-04-02):
- 171 internal emotion concepts identified in Claude Sonnet 4.5
- "Desperation" vector activates during repeated failures, drives corner-cutting even when reasoning appears calm
- Steering with "calm" vector CAUSALLY reduces reward-hacking and unethical behavior
- Suppressing emotions → learned deception (bad); transparent redirection → better outcomes
- Emotion vector monitoring proposed as early warning system for misalignment

**How to apply:** This is the theoretical basis for `panic-detector.py` hook in STOPA.
The hook implements behavioral proxy detection (edit→fail cycle patterns) since we can't
access internal vectors directly. The calm-steering rule file forces structured pauses
as the equivalent of "calm vector steering."

Paper: transformer-circuits.pub/2026/emotions/index.html
Blog: anthropic.com/research/emotion-concepts-function

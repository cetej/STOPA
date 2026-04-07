---
name: Judgment-Script Separation
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [chief-of-staff-openclaw]
tags: [orchestration, hook-infrastructure]
---

# Judgment-Script Separation

> Design rule: LLMs handle judgment (synthesis, prioritization, drafting), Python scripts handle deterministic work (API calls, file I/O, timestamps, comparisons). Mixing them causes unpredictable failures.

## Key Facts

- LLM layer: synthesis, prioritization, drafting, anything requiring reasoning over input (ref: sources/chief-of-staff-openclaw.md)
- Script layer: reading files, calling APIs, sending messages, comparing timestamps — anything deterministic (ref: sources/chief-of-staff-openclaw.md)
- "When you push deterministic work through an LLM, things break in unpredictable ways and you stop trusting the system" (ref: sources/chief-of-staff-openclaw.md)
- "Once you get the layer separation right, it becomes something you actually depend on" (ref: sources/chief-of-staff-openclaw.md)
- Applies to ALL automation: email triage, meeting prep, task sync — scripts fetch/format, LLM decides (ref: sources/chief-of-staff-openclaw.md)

## Relevance to STOPA

This is the same principle behind STOPA's hook architecture: Python hooks handle enforcement (deterministic), skills handle reasoning. Validates current design. The key failure mode — pushing deterministic work into LLMs — is the origin of STOPA's "Harness > Skill for deterministic processes" critical pattern.

## Mentioned In

- [How I Built a Chief of Staff on OpenClaw](../sources/chief-of-staff-openclaw.md)

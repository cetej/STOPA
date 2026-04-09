---
name: PaperOrchestra
type: paper
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [paperorchestra-multi-agent-paper-writing]
tags: [multi-agent, orchestration, evaluation, pipeline, generation]
---

# PaperOrchestra

> Multi-agent framework for automated AI research paper writing that transforms unstructured pre-writing materials into submission-ready LaTeX manuscripts.

## Key Facts

- Achieves 50-68% absolute win rate margin in literature review quality vs. baseline autonomous writers (ref: sources/paperorchestra-multi-agent-paper-writing.md)
- Achieves 14-38% win rate margin in overall manuscript quality (ref: sources/paperorchestra-multi-agent-paper-writing.md)
- Architecture: specialized sub-agents handle literature synthesis, visualization generation, and LaTeX formatting — coordinator routes materials to appropriate agents
- Introduces PaperWritingBench — the first standardized benchmark, constructed from 200 top-tier AI conference papers via reverse-engineering
- Key claim: flexible, unconstrained pre-writing material handling (not rigid template input) is what separates it from prior systems
- Authors: Yiwen Song, Yale Song, Tomas Pfister, Jinsung Yoon (Google Research, 2026)

## Relevance to STOPA

Multi-agent specialization pattern (different agents per document section) directly mirrors STOPA's orchestrate skill design. PaperWritingBench's reverse-engineering methodology is actionable for building STOPA eval harnesses.

## Mentioned In

- [PaperOrchestra: Multi-Agent Framework for Automated AI Research Paper Writing](../sources/paperorchestra-multi-agent-paper-writing.md)

---
title: "PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing"
slug: paperorchestra-multi-agent-paper-writing
source_type: url
url: "https://arxiv.org/abs/2604.05018"
date_ingested: 2026-04-08
date_published: "2026-04"
entities_extracted: 2
claims_extracted: 5
---

# PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing

> **TL;DR**: Multi-agent system that converts unstructured research materials into submission-ready LaTeX manuscripts. Introduces PaperWritingBench (200 top-tier papers, reverse-engineered). Achieves 50-68% win rate advantage in literature review quality vs. baselines.

## Key Claims

1. Multi-agent specialization (different agents per manuscript section) substantially outperforms monolithic single-agent approaches in literature review synthesis — `verified` (50-68% win rate margin)
2. Overall manuscript quality improves 14-38% over baseline autonomous writers — `verified`
3. Flexible, unconstrained pre-writing material input is the key bottleneck prior systems failed on — `argued`
4. Reverse-engineering 200 top-tier papers to create PaperWritingBench is a valid methodology for standardized evaluation — `argued`
5. Multi-agent coordination can produce publication-ready LaTeX including visualizations — `asserted`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [PaperOrchestra](../entities/paperorchestra.md) | paper | new |
| [PaperWritingBench](../entities/paperwritingbench.md) | concept | new |

## Relations

- PaperOrchestra `uses` PaperWritingBench — evaluated on it
- PaperOrchestra `extends` multi-agent-coordination — specialized sub-agent per section
- PaperWritingBench `inspired_by` reverse-engineering methodology

## Cross-References

- Related wiki articles: [orchestration-multi-agent](../orchestration-multi-agent.md) (multi-agent patterns), [skill-evaluation](../skill-evaluation.md) (benchmark methodology)
- Related learnings: no direct matches in learnings/ (new domain)
- Contradictions: none

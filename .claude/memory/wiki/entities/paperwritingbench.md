---
name: PaperWritingBench
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [paperorchestra-multi-agent-paper-writing]
tags: [evaluation, benchmark, research]
---

# PaperWritingBench

> First standardized evaluation benchmark for automated research paper writing, constructed by reverse-engineering raw materials from 200 top-tier AI conference papers.

## Key Facts

- Built from 200 top-tier AI conference papers — raw materials reconstructed from final papers (reverse-engineering approach)
- Includes automated evaluation metrics for literature review quality and overall manuscript quality
- Evaluates both depth of literature synthesis and generation of visuals (plots, conceptual diagrams)
- Introduced alongside PaperOrchestra (arXiv:2604.05018) (ref: sources/paperorchestra-multi-agent-paper-writing.md)

## Relevance to STOPA

The reverse-engineering methodology — taking real completed artifacts and inferring what "good inputs + good outputs" look like — is directly applicable to building harness test cases for /deepresearch, /compile, and /eval in STOPA.

## Mentioned In

- [PaperOrchestra: Multi-Agent Framework for Automated AI Research Paper Writing](../sources/paperorchestra-multi-agent-paper-writing.md)

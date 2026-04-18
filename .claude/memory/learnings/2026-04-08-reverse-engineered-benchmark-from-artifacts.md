---
date: 2026-04-08
type: best_practice
severity: medium
component: skill
tags: [evaluation, benchmark, harness, eval, deepresearch, compile]
summary: "Build eval benchmarks by reverse-engineering expected outputs from real completed artifacts, not synthetic generation. PaperWritingBench: 200 top-tier papers → inferred raw materials + quality criteria. Applicable to STOPA /eval and /harness test case construction."
source: external_research
maturity: draft
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: "manual"
---

## Reverse-Engineered Benchmarks from Real Artifacts

From PaperOrchestra (arXiv:2604.05018): PaperWritingBench constructs evaluation cases by taking **completed, high-quality artifacts** (200 top-tier conference papers) and reverse-engineering what the raw inputs and quality criteria should be.

### Why this works better than synthetic generation

- Real artifacts encode tacit quality standards that are hard to specify a priori
- Reverse-engineering from 200 examples captures distribution of actual good outputs
- Automated metrics can be grounded in real exemplars rather than hand-crafted rubrics

### STOPA application

When building harness test cases for `/deepresearch`, `/compile`, or `/eval`:
1. Take 10-20 examples of **high-quality prior outputs** from the skill
2. Infer what the input + expected output structure should look like
3. Use those as canonical test cases — not hand-crafted synthetic inputs

This avoids the problem of eval cases being too easy (synthetic) or too domain-specific (manual).

# Provenance: AI Agent Defense Frameworks Research

**Date:** 2026-04-05
**Question:** LlamaFirewall, CaMeL, TaskShield — actionable integration assessment for STOPA
**Scale:** survey
**Rounds:** 1 (direct research, parallel web searches)
**Sources:** 12 consulted / 12 accepted / 0 rejected
**Verification:** partial (top claims cross-referenced across 2+ sources)

## Research Approach

Direct research by Lead Researcher (no background agent files were written in time — used direct WebSearch/WebFetch calls instead):
- 6 WebSearch queries across 3 frameworks
- 7 WebFetch calls to primary sources (official docs, GitHub, arXiv)
- 3 background claude agents launched but results not incorporated (still running)

## Sources Consulted

| Source | URL | Purpose |
|--------|-----|---------|
| LlamaFirewall How-to Docs | https://meta-llama.github.io/PurpleLlama/LlamaFirewall/docs/documentation/getting-started/how-to-use-llamafirewall | Python API details |
| LlamaFirewall README | https://github.com/meta-llama/PurpleLlama/blob/main/LlamaFirewall/README.md | Scanner types, installation |
| LlamaFirewall About | https://meta-llama.github.io/PurpleLlama/LlamaFirewall/docs/documentation/about-llamafirewall | Architecture overview |
| PyPI llamafirewall | https://pypi.org/project/llamafirewall/ | Package availability |
| LlamaFirewall Paper | https://arxiv.org/html/2505.03574v1 | Latency benchmarks, accuracy |
| CaMeL GitHub | https://github.com/google-research/camel-prompt-injection | Implementation status |
| Simon Willison CaMeL | https://simonwillison.net/2025/Apr/11/camel/ | Practical assessment |
| GitHub Issue #147 | https://github.com/meta-llama/PurpleLlama/issues/147 | False positive community reports |
| TaskShield arXiv HTML | https://arxiv.org/html/2412.16682 | Architecture, implementation status |
| Anthropic PI research | https://www.anthropic.com/research/prompt-injection-defenses | Baseline comparison |
| ikangai CaMeL | https://www.ikangai.com/camel-prompt-injection-defense-explained/ | Capability tracking mechanics |
| foss.dev LlamaFirewall | https://foss.dev/blog/llamafirewall | Model-agnostic claims |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 18 |
| [INFERRED] | 6 |
| [UNVERIFIED] | 1 |
| [SINGLE-SOURCE] | 3 |

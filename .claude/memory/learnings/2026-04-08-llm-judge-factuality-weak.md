---
date: 2026-04-08
type: best_practice
severity: high
component: orchestration
tags: [eval, critic, judge, factuality, scoring]
summary: "LLM judges (GPT-5, Claude) prioritize structural formatting over factual correctness (r=0.65 overall, weak on lit review factuality). Eval and critic should combine LLM scoring with grep/search verification for factual claims."
source: external_research
confidence: 0.7
uses: 0
successful_uses: 0
harmful_uses: 0
verify_check: "manual"
---

PaperOrchestra (arXiv:2604.05018) human evaluation showed strong correlation (r=0.6458) between automated GPT-5 assessments and expert preferences for overall quality, but LLM evaluators prioritized structural formatting over pragmatic factuality when judging literature reviews.

Implication for STOPA: `/eval` and `/critic` should never rely solely on LLM scoring for factual claims. Always combine with grep/search verification for concrete assertions (file existence, function names, API contracts, citation accuracy).

Pattern: LLM judge excels at structural quality (coherence, completeness, formatting) but underperforms on factual grounding (does this citation exist? is this claim supported?). Use LLM for structure, use tools for facts.

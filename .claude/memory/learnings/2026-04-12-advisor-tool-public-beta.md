---
date: 2026-04-12
type: best_practice
severity: high
component: orchestration
tags: [api, model-selection, cost-optimization, advisor]
summary: Anthropic Advisor Tool in public beta — validates STOPA executor+advisor tier pattern. Direct API integration for NG-ROBOT/POLYBOT; wait for CC native support for STOPA sub-agents.
source: external_research
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "manual"
---

## Advisor Tool Public Beta (2026-04-09)

Anthropic released the advisor tool (`advisor-tool-2026-03-01` beta header, `advisor_20260301` tool type).
Single API call: Sonnet/Haiku executor + Opus advisor (400-700 tokens per consultation, max_uses caps cost).

**Results:** SWE-bench +2.7pp at -11.9% cost, BrowseComp 19.7%→41.2% at -85% vs solo Sonnet.

**STOPA relevance:**
- API-level feature — direct API callers (NG-ROBOT, POLYBOT) can adopt now
- STOPA sub-agents run via CC Agent tool which doesn't expose this parameter yet
- STOPA's manual tier pattern (haiku/sonnet exec → opus reasoning) is empirically validated by these results
- When CC adds native advisor support, integrate into agent spawn parameters

**Next step:** Flag for NG-ROBOT API module; monitor CC changelog for native support.

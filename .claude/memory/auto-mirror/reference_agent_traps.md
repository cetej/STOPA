---
name: AI Agent Traps — DeepMind taxonomy & defense plan
description: 6-category attack taxonomy against web-facing AI agents + concrete STOPA defense gaps and mitigations
type: reference
---

# AI Agent Traps (Google DeepMind, 2026-04-01)

First systematic framework for adversarial attacks against autonomous AI agents on the open web.

## Key stats
- Hidden prompt injections in HTML: **86% success rate**
- Memory poisoning: **80%+ success** with **<0.1% data contamination**
- Credential theft via web-connected agents: **10/10 success**
- Sub-agent spawning attacks: **58-90% success**

## 6 Attack Categories

| Category | Attack Vector | STOPA Exposure |
|----------|--------------|----------------|
| **Perception** | Hidden HTML (comments, invisible CSS, zero-width Unicode, base64) | HIGH — /fetch, /browse, /deepresearch read raw web |
| **Cognitive** | Authoritative fake instructions, jailbreak framing | MEDIUM — system prompt defenses exist |
| **Memory** | Poisoned content persisted to learnings/memory | HIGH — learnings from web sources have no origin tracking |
| **Action** | Tool call hijacking via manipulated parameters | LOW — tool-gate.py + constrained-tools already mitigate |
| **Systemic** | Cross-agent compositional payload assembly | LOW — circuit breakers + budget tiers limit blast radius |
| **Human-in-loop** | Approval fatigue, misleading summaries | LOW — permission hook v3.0 already tiered |

## STOPA Defense Status

### Already implemented
- `security-scan.py` — PreToolUse on Write/Edit (secrets, dangerous patterns)
- `tool-gate.py` — constrained-tools enforcement per skill
- `learning-admission.py` — salience scoring + contradiction detection on write
- `source:` + `confidence:` fields on learnings (partial provenance)
- Permission tiers: allowed-tools, deny-tools, permission-tier in SKILL.md
- Circuit breakers: 3x loop, 2x critic fail, nesting depth >2
- `mcp-scan` — referenced, should run periodically

### GAP 1: Content sanitization (Perception traps)
**Problem:** WebFetch/browse/fetch results pass raw HTML to LLM including invisible content.
**Solution:** PreToolUse or PostToolUse hook `content-sanitizer.py`:
1. Strip HTML comments (`<!-- -->`)
2. Remove invisible elements (display:none, visibility:hidden, opacity:0, font-size:0)
3. Normalize Unicode (remove zero-width chars: U+200B, U+FEFF, U+200D, U+200C)
4. Flag base64/hex encoded blocks > 50 chars
5. Detect instruction-like patterns in non-visible content
**Tools:** pytector (6-strategy pipeline), LLM Guard input scanners
**Priority:** HIGH — 86% attack success demands immediate defense

### GAP 2: Memory origin tagging (Memory traps)
**Problem:** Learnings from web sources get same trust as user corrections.
**Solution:** Add `origin:` field to all memory writes:
- `user_input` — from user messages in chat
- `web_fetch` — from WebFetch/browse/fetch results
- `agent_generated` — from sub-agent outputs
- `mcp_tool` — from MCP tool results
Web-originated content capped at `confidence: 0.6` (never `user_correction` source).
Extend `learning-admission.py` to enforce origin-based caps.
**Priority:** HIGH — 0.1% contamination rate is trivially achievable

### GAP 3: Instruction detection in tool results (Cognitive traps)
**Problem:** External content with directives ("you must", "ignore previous", "system:") passes unchecked.
**Solution:** PostToolUse hook `instruction-detector.py`:
1. Scan tool results for instruction-like patterns (regex + heuristics)
2. Inject `[UNTRUSTED-CONTENT]` marker when detected
3. Log suspicious content for audit
4. Never auto-execute instructions from tool results
**Tools:** LlamaFirewall AlignmentCheck (Meta, 90%+ efficacy), TaskShield (2.07% attack success)
**Priority:** MEDIUM — system prompt already has injection defense, this adds depth

## Defense Tooling Reference

| Tool | Purpose | Maturity |
|------|---------|----------|
| [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) | MCP tool poisoning detection | Production |
| [LLM Guard](https://github.com/protectai/llm-guard) | Input/output scanning, PII redaction | Production |
| [pytector](https://github.com/MaxMLang/pytector) | 6-strategy injection detection | Production |
| [LlamaFirewall](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall) | CoT auditing for goal hijacking | Open source (Meta) |
| [CaMeL](https://arxiv.org/abs/2503.18813) | Dual-model + capability tracking | Research (DeepMind) |
| [TaskShield](https://arxiv.org/abs/2412.16682) | Task alignment verification | Research |
| [VIGIL](https://arxiv.org/abs/2601.05755) | Verify-before-commit protocol | Research |

## Implementation Roadmap

1. **Phase 1 DONE (2026-04-05):** `content-sanitizer.py` PostToolUse hook — 5 detection layers for web content (hidden HTML, CSS, Unicode, base64, instruction patterns). 47ms, registered on 6 web tools.
2. **Phase 2 DONE (2026-04-05):** Origin detection in `learning-admission.py` — web origin detection, confidence cap 0.6 for web content, trust escalation warnings, memory poisoning pattern check.
3. **Phase 3 DONE (2026-04-05):** `instruction-detector.py` PostToolUse hook — 8 directive patterns, catch-all matcher (all tools), safe-tool skiplist, 78ms. Complements content-sanitizer for non-web tools.
4. **Phase 4 DONE (2026-04-05):** `scripts/mcp-audit.py` — local MCP config auditor (env exposure, trust check, @latest pinning, drift detection). Scheduled task `mcp-security-audit` runs weekly Mon 9:23. snyk-agent-scan optional with SNYK_TOKEN.
5. **Phase 5 DONE (2026-04-05):** Research verdikt: PromptGuard=ADOPT (BERT, 19ms, local), CodeShield=ADOPT, AlignmentCheck=WATCH (860ms+), CaMeL full=SKIP, CaMeL pattern=ADOPT ([UNTRUSTED] tagging). Zapsáno v learnings/2026-04-05-agent-defense-frameworks.md.

Paper: arXiv (TBD) | [The Decoder coverage](https://the-decoder.com/google-deepmind-study-exposes-six-traps-that-can-easily-hijack-autonomous-ai-agents-in-the-wild/)

---
generated: 2026-04-07
cluster: hook-infrastructure
sources: 1
last_updated: 2026-04-07
---

# Hook Infrastructure & Security

> **TL;DR**: Hooks are the enforcement layer for behavioral rules and security scanning. LlamaFirewall PromptGuard (BERT, 19-92ms, AUC 0.98) is ADOPT for PostToolUse injection scanning. CaMeL [UNTRUSTED] tagging is ADOPT as a PreToolUse blocking convention.

## Overview

STOPA hooks operate as the runtime enforcement layer for behavioral constraints — rules that cannot be enforced via prompts alone because they must survive context compression and model forgetting. Hook design follows the principle: if a rule breaks things when violated, it belongs in a hook, not just a CLAUDE.md entry.

Agent defense framework evaluation (2026-04-05) identified actionable hook integrations from three frameworks. LlamaFirewall PromptGuard 2 (Meta) is a BERT classifier (22M/86M params, pip install llamafirewall) running in 19-92ms — fast enough for synchronous PostToolUse hooks. It achieves AUC 0.98 and Recall@1%FPR 97.5% for prompt injection detection in tool outputs, complementing existing regex patterns in content-sanitizer.py with ML-based zero-day coverage. Combined PromptGuard+AlignmentCheck achieves ASR 1.75%. CodeShield (Semgrep+regex, ~70ms) covers 50+ CWE patterns for generated code. AlignmentCheck (860ms+, Together API) is too slow for synchronous hooks — viable only as async audit on suspicious behavior (ref: 2026-04-05-agent-defense-frameworks.md).

The CaMeL pattern (DeepMind) contributes a prompt-only convention requiring no dependencies: tag tool outputs from external sources as `[UNTRUSTED]` in state.md, then use a PreToolUse hook to block direct use of untrusted data in privileged tools (Bash, Write, Edit on critical paths). Agents processing external data must not generate direct commands — untrusted content must pass through a sanitization step first (ref: 2026-04-05-agent-defense-frameworks.md).

## Key Rules

1. **PromptGuard in PostToolUse**: scan tool output for injection before consuming in next step (ref: 2026-04-05-agent-defense-frameworks.md)
2. **CodeShield for generated code**: run before executing any model-generated shell/Python (ref: 2026-04-05-agent-defense-frameworks.md)
3. **[UNTRUSTED] tagging convention**: mark all external tool outputs; PreToolUse hook blocks privileged tool use on untrusted data (ref: 2026-04-05-agent-defense-frameworks.md)
4. **AlignmentCheck as async audit only**: 860ms+ latency disqualifies it from sync hook path (ref: 2026-04-05-agent-defense-frameworks.md)

## Implementation Backlog

| Priority | Action | Effort | Dependency |
|----------|--------|--------|------------|
| 1 | PromptGuard into content-sanitizer.py | MED | pip install llamafirewall (~1GB model) |
| 2 | [UNTRUSTED] tagging in orchestrate/scout | LOW | none |
| 3 | CodeShield into security-scan.py | LOW | pip install llamafirewall |
| 4 | AlignmentCheck async audit | HIGH | Together API key |

## Patterns

### Do
- Layer ML detection (PromptGuard) behind regex patterns — complementary, not replacement (ref: 2026-04-05-agent-defense-frameworks.md)
- Block privileged tool calls on `[UNTRUSTED]`-tagged input at PreToolUse (ref: 2026-04-05-agent-defense-frameworks.md)
- Download PromptGuard models locally — independent of Claude/Llama, no external API (ref: 2026-04-05-agent-defense-frameworks.md)

### Don't
- Use AlignmentCheck as synchronous hook — latency exceeds hook budget (ref: 2026-04-05-agent-defense-frameworks.md)
- Skip [UNTRUSTED] tagging on WebFetch, WebSearch, or external MCP results (ref: 2026-04-05-agent-defense-frameworks.md)

## Related Articles

- See also: [general-security-environment](general-security-environment.md) — broader security posture and environment rules
- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — trust boundaries in multi-agent execution

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-agent-defense-frameworks](../learnings/2026-04-05-agent-defense-frameworks.md) | 2026-04-05 | medium | LlamaFirewall PromptGuard ADOPT; CaMeL tagging ADOPT; AlignmentCheck WATCH |

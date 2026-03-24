# Claude Extended Thinking / Thinking Mode: Problems, Analysis & Best Practices

**Research date:** 2026-03-21
**Sources:** Anthropic docs, GitHub issues, Reddit, Hacker News, developer blogs

---

## 1. Executive Summary

Claude's "extended thinking" (and its successor "adaptive thinking") is a powerful feature that enables step-by-step reasoning before generating responses. However, it has significant documented problems:

- **Unbounded thinking loops** that burn tens of thousands of tokens with zero useful output
- **Performance degradation** — thinking can hurt results by up to 36% on certain task types
- **Hidden token costs** — users are billed for full thinking tokens, not the summarized version they see
- **Context destruction** — thinking blocks break compaction, causing memory loss in long sessions
- **Opus 4.6 regression** — specifically introduced severe stuck-in-loop behavior

Anthropic has responded by deprecating manual `budget_tokens` in favor of **adaptive thinking** with an `effort` parameter, which lets the model decide when and how much to think.

---

## 2. Core Problems Reported by Community

### 2.1 Unbounded Thinking Loops (Critical Bug)

**GitHub Issue #26171** — "Agent burns tokens endlessly - gets stuck in unbounded thinking loops":
- Agent entered 21-minute thinking state, consumed 72,900 tokens, produced zero output
- User must manually press Escape to stop
- Occurs after conversation compaction and at other unpredictable times
- Closed as duplicate of #24585, indicating widespread known issue

**GitHub Issue #24585** — "Opus 4.6 continuously stuck in explore and thinking loops":
- 26+ upvotes, 3+ identified duplicate issues, 7+ cross-referenced related issues
- Occurs **every session** on most requests (not rare)
- Duration: 5-22+ minutes of unproductive processing
- Sometimes burns **hundreds of thousands of tokens** with 50+ tool requests
- When interrupted, Claude acknowledges: *"I already have enough context, let me complete the task"*
- **Specifically correlates with Opus 4.6 release** — did not occur on previous versions
- Two failure modes identified:
  1. **Argumentation loops** — model argues with itself
  2. **Explore loops** — over-explores codebase unnecessarily

Related issues: #23688, #24104, #24215, #25059, #25068, #25257, #26214, #27211, #27341

### 2.2 Token Burn Rate Explosion

**Reddit r/ClaudeCode** — "Claude Code sessions burning through token limits way faster than before":
- Users report "burning tokens while thinking and doing nothing"
- One user: Claude responded with one sentence, no tools used, cost **12% of session tokens**
- Pro plan sessions lasting roughly an hour, same as free tier

**Reddit r/ClaudeAI** — "Higher Token Consumption and Excessive Planning After Update":
- "It burns tokens like no tomorrow. Opus 4.5 is unusable for day to day work."
- Bug where plan review shows grayed-out text, wasting tokens on invisible planning

**Reddit r/ClaudeCode** — "$100 is the new $20? Token burn rate has skyrocketed":
- "Over a long session with 100+ messages, that's 1.5M+ cache reads just from reloading instructions"
- "Sessions waste massive tokens on trial-and-error for things already figured out in prior sessions"

**Medium article** — "I Used Millions of Tokens on Claude Code":
- Developer burned 4.7 million tokens, estimated **3.2 million were wasted** (68% waste rate)
- Projects using vibe coding consumed 800K-1.2M tokens and took longer to finish

### 2.3 Ghost Token Drain

**Reddit Usage Megathread** (December 2025):
- "The prevailing theory is that auto-compaction is completely broken. Claude is re-reading your entire massive context window on every single prompt instead of compressing it, causing exponential 'ghost' token drain."

### 2.4 Startup Token Waste

**Reddit r/ClaudeCode** — "Confirmed: Claude Code CLI burns ~1-3% of your quota immediately on startup (even with NO prompts)":
- Hard-coded warmup messages consume tokens before any user interaction
- Opening CC just to check usage wastes tokens on warmup

---

## 3. When Thinking Mode Hurts Performance

### 3.1 Performance Degradation Data

Research shows extended thinking can **hurt performance by up to 36%** on certain task types. This mirrors human cognitive behavior — overthinking intuitive tasks degrades performance.

**Specific problem areas:**
- **Pattern recognition tasks** — thinking actively hurts
- **Novel problems outside training distribution** — thinking helps less than expected; internal deliberation often converges on the same wrong answer
- **Simple/routine tasks** — unnecessary overhead with no quality improvement
- **Tasks requiring fast iteration** — latency penalty outweighs quality gains

### 3.2 Think Tool vs Extended Thinking (Anthropic's Own Data)

Anthropic's engineering blog published benchmark data comparing approaches:

**Airline domain (tau-Bench):**
| Approach | Pass Rate | vs Baseline |
|----------|-----------|-------------|
| Think tool + optimized prompt | 0.570 | +54% |
| Extended thinking alone | 0.412 | +24% |
| Think tool alone | 0.404 | +22% |
| Baseline (no thinking) | 0.332 | — |

**Retail domain (tau-Bench):**
| Approach | Pass Rate | vs Baseline |
|----------|-----------|-------------|
| Think tool | 0.812 | +3.7% |
| Baseline | 0.783 | — |
| Extended thinking | 0.770 | **-1.7%** |

Key insight: **Extended thinking actually performed WORSE than no thinking** in the retail domain. The think tool (which operates during response, not before) outperformed both.

### 3.3 Context Destruction via Compaction

Extended thinking creates thinking blocks that "cannot be modified" and "must remain as they were" per API requirements. This breaks compaction:

- GitHub issue #12311 documents compaction failure with thinking blocks
- The API rejects modified thinking blocks, making sessions unrecoverable
- Users must switch to Sonnet (which doesn't use extended thinking) as a workaround
- Result: "paying for the most expensive model and doing extended work, you may actually have worse context management than cheaper alternatives"

Post-compaction symptoms:
- Claude forgets coding standards it previously followed
- Loses awareness of active Skills and methodologies
- Forgets which codebase it's working on
- "Claude is definitely dumber after the compaction"

---

## 4. Anthropic's Response & Evolution

### 4.1 Extended Thinking → Adaptive Thinking Migration

Anthropic has deprecated manual `budget_tokens` on Opus 4.6 and Sonnet 4.6 in favor of **adaptive thinking**:

- **Manual mode** (`thinking.type: "enabled"` + `budget_tokens`): Developer guesses how much thinking is needed. Deprecated on 4.6 models.
- **Adaptive mode** (`thinking.type: "adaptive"` + `effort` parameter): Model decides when and how much to think based on query complexity.

Per Anthropic: "In internal evaluations, adaptive thinking reliably drives better performance than extended thinking."

### 4.2 Effort Parameter

| Level | Behavior | Use Case |
|-------|----------|----------|
| `max` | Always thinks, no constraints | Hardest problems (Opus 4.6 only) |
| `high` | Always thinks, deep reasoning | Complex tasks (default) |
| `medium` | Moderate thinking, may skip for simple queries | Most applications |
| `low` | Minimal thinking, skips for simple tasks | High-volume, latency-sensitive |

**Critical for Claude Code users:** Claude Code defaults to `medium` effort. Community reports that setting `"thinkingEffort": "max"` in `~/.claude/settings.json` restores quality for complex tasks.

### 4.3 Interleaved Thinking

Adaptive thinking automatically enables **interleaved thinking** — Claude can think between tool calls, not just before the first response. This is especially effective for agentic workflows.

### 4.4 Summarized vs Full Thinking

Claude 4 models return **summarized thinking** by default:
- Billed for **full** thinking tokens, not summary
- Billed output count **does not match** visible tokens
- Can set `display: "omitted"` for faster time-to-first-token (still billed full price)

### 4.5 Promptable Thinking Control

Anthropic recommends adding to system prompts:
```
Extended thinking adds latency and should only be used when it will
meaningfully improve answer quality — typically for problems that require
multi-step reasoning. When in doubt, respond directly.
```

And for overthinking models:
```
When you're deciding how to approach a problem, choose an approach and
commit to it. Avoid revisiting decisions unless you encounter new
information that directly contradicts your reasoning.
```

---

## 5. Best Practices: When to Enable vs Disable Thinking

### 5.1 Enable Thinking (High/Max Effort) For:
- Complex mathematical problems
- Multi-step reasoning tasks
- Strategic decision-making
- Code analysis and debugging requiring deep understanding
- Multi-stage problem solving
- Long-horizon agentic workflows

### 5.2 Disable or Lower Thinking For:
- Simple factual questions
- Straightforward summarization
- Pattern recognition / intuitive tasks
- High-volume, latency-sensitive workloads
- Tasks where you can specify exact instructions (what, where, how)
- Routine file edits and simple code changes

### 5.3 Community-Recommended Token Savings

From Reddit and GitHub discussions:

1. **Set thinking to low** — handles ~95% of problems well
2. **Remove generic MCPs** — they fill context before real work starts
3. **Use sub-agents** — delegate exploration to reduce main context pollution
4. **Avoid vibe coding** — specify exact requirements, don't let Claude guess
5. **Keep CLAUDE.md lean** — large instruction files consume tokens on every request
6. **Use `/compact preserve`** — in Claude Code, preserve important context during compaction
7. **Start new sessions** for fresh tasks instead of continuing polluted contexts

### 5.4 API Configuration Recommendations

**For coding agents (Sonnet 4.6):**
```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    messages=[...]
)
```

**For chat/non-coding (Sonnet 4.6):**
```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    messages=[...]
)
```

**For autonomous agents (Opus 4.6):**
```python
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...]
)
```

---

## 6. Key Takeaways

1. **Thinking mode is NOT universally beneficial** — it can degrade performance by up to 36% on certain tasks.
2. **Opus 4.6 has a critical bug** with unbounded thinking loops that burn tokens indefinitely. This is a known, tracked issue with no fix as of March 2026.
3. **You are billed for full thinking tokens**, not the summarized version you see. Token costs are opaque.
4. **Adaptive thinking > manual budget_tokens** — let the model decide when to think. Anthropic's internal evals confirm this.
5. **The `effort` parameter is the primary control knob** — use `medium` for most work, `low` for simple tasks, `high`/`max` for complex reasoning.
6. **Think tool (during-response) outperforms extended thinking (pre-response)** in some agentic scenarios, particularly policy-heavy environments.
7. **Extended thinking breaks context compaction** — long sessions with thinking-heavy models suffer progressive context loss.
8. **Community consensus**: Most token waste comes from user patterns (vague prompts, MCP bloat, large CLAUDE.md files) rather than thinking mode itself, but the unbounded loop bug is a genuine platform-level defect.

---

## Sources

### Anthropic Official
- [Building with extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Extended thinking tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips)
- [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [The Think Tool (engineering blog)](https://www.anthropic.com/engineering/claude-think-tool)
- [Effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Manage costs effectively](https://code.claude.com/docs/en/costs)

### GitHub Issues
- [#26171 — Agent burns tokens endlessly in thinking loops](https://github.com/anthropics/claude-code/issues/26171)
- [#24585 — Opus 4.6 stuck in explore and thinking loops](https://github.com/anthropics/claude-code/issues/24585)
- [#17670 — Extended thinking blocks tool calls](https://github.com/anthropics/claude-code/issues/17670)
- [#9562 — Thinking throbber infinite refresh loop](https://github.com/anthropics/claude-code/issues/9562)
- [#13579 — Community learnings: 7 token-wasting patterns](https://github.com/anthropics/claude-code/issues/13579)

### Community Discussions
- [Reddit: Claude Code sessions burning through token limits](https://www.reddit.com/r/ClaudeCode/comments/1rg9ady/)
- [Reddit: Higher Token Consumption After Update](https://www.reddit.com/r/ClaudeAI/comments/1p5y2nd/)
- [Reddit: How are you not burning 100k+ tokens per session](https://www.reddit.com/r/ClaudeCode/comments/1r26miw/)
- [Reddit: Thinking mode in Claude Code](https://www.reddit.com/r/ClaudeAI/comments/1rasiln/)
- [Reddit: $100 is the new $20? Token burn rate skyrocketed](https://www.reddit.com/r/ClaudeCode/comments/1qz31g5/)
- [Reddit: CC just sitting there "thinking" with no output](https://www.reddit.com/r/ClaudeAI/comments/1rn8ztx/)
- [Reddit: Usage Limits Megathread (Dec 2025)](https://www.reddit.com/r/ClaudeAI/comments/1pygdbz/)
- [Hacker News: Excessive token usage in Claude Code](https://news.ycombinator.com/item?id=47096937)
- [Medium: I Used Millions of Tokens on Claude Code](https://medium.com/activated-thinker/i-used-millions-of-tokens-on-claude-code-the-reason-vibe-coding-is-a-trap-4713132387a7)
- [Claude Saves Tokens, Forgets Everything (golev.com)](https://golev.com/post/claude-saves-tokens-forgets-everything/)
- [UltraThink is Dead (decodeclaude.com)](https://decodeclaude.com/ultrathink-deprecated/)

### Guides & Analysis
- [Claude Extended Thinking: The Ultimate Guide (GitHub Gist)](https://gist.github.com/intellectronica/58571dda3581eec3e17a77741e8c858a)
- [How to Fix Claude Code CLI Performance (BSWEN)](https://docs.bswen.com/blog/2026-03-13-claude-code-cli-configuration-guide/)
- [Why Your AI Keeps Getting Stuck in Loops (byPawel)](https://www.bypawel.com/why-your-ai-keeps-getting-stuck-in-loops)
- [Claude Code Token Limits Guide (Faros AI)](https://www.faros.ai/blog/claude-code-token-limits)

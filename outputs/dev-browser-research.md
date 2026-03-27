# dev-browser — Research Brief

**Date:** 2026-03-26
**Question:** What is the `dev-browser` npm package, who made it, how does it work architecturally, how does it compare to other AI browser automation tools, and how would it integrate with Claude Code?
**Scope:** standard
**Sources consulted:** 18

---

## Executive Summary

`dev-browser` is an open-source (MIT) CLI tool and Claude Skill created by **Sawyer Hood** (ex-Figma, ex-Facebook), released in January 2026 and available at https://github.com/SawyerHood/dev-browser. Its core philosophy is "let the agent write browser automation code" rather than exposing browser actions as MCP tools — the agent writes small TypeScript/JavaScript scripts that run inside a QuickJS WASM sandbox and control a Playwright-backed browser. This approach avoids the massive MCP tool-definition token overhead and gives the agent expressive freedom.

In benchmarks run by the author himself (methodology at https://github.com/SawyerHood/dev-browser-eval), dev-browser completed tasks in **3m 53s at $0.88 cost (29 turns, 100% success)** vs Playwright MCP at 4m 31s / $1.45 / 51 turns and the Claude Chrome Extension at 12m 54s / $2.81 / 80 turns. Independent community reviews are cautiously mixed: one reviewer ranked dev-browser out of their top recommendations (PinchTab and browser-use won), while the awesome-claude-code curator raised unresolved security questions about the tool's permission model. A critical RCE-via-prompt-injection vulnerability was reported and closed as resolved via the v0.2.0 architectural rewrite.

The tool has accumulated **4.4k GitHub stars and 273 forks** as of March 2026, with strong adoption in the Claude Code skill ecosystem (264 installations per agentskills.so). It is the most widely distributed Claude Skill for browser automation.

---

## Detailed Findings

### 1. Architecture and Agent Interaction Model

The key architectural insight is that dev-browser is a **code-execution bridge**, not an action-by-action MCP server. The interaction model:

1. Agent is told to run `dev-browser --help` — the help output contains a full LLM usage guide with examples and API reference (no separate documentation needed).
2. Agent writes a short TypeScript/JavaScript script against the dev-browser API.
3. Script is passed to the CLI: `dev-browser --headless <script>` or `dev-browser --connect <script>`.
4. Script runs inside a **QuickJS WASM sandbox** — no host filesystem access, no direct network access, isolated from the host OS.
5. Browser actions go through a **Playwright Node.js daemon** that stays warm between invocations.
6. Results (console output, screenshots, file writes to `~/.dev-browser/tmp/`) are returned to the agent.

**Two connection modes:**
- `--headless`: Launches a fresh Chromium instance (managed by Playwright).
- `--connect`: Attaches to a running Chrome instance via Chrome DevTools Protocol. This gives access to existing logged-in sessions, cookies, extensions.

**Named persistent pages:** The agent can call `browser.getPage("mypage")` to create a named page that persists across multiple script invocations. This allows multi-step workflows without reinitializing.

**AI-optimized snapshots:** `page.snapshotForAI({ track?, depth?, timeout? })` returns a structured, compressed DOM snapshot instead of raw HTML — reduces token consumption for element discovery.

**Tech stack:** 94% TypeScript, 4% Rust. The Rust component handles the CLI binary; the Node.js daemon manages Playwright. QuickJS WASM handles sandbox execution.

### 2. Who Made It

**Sawyer Hood** — independent software engineer. Previous roles: Figma, Facebook (Meta). Currently building experiments around LLM interaction patterns under the banner of **Smooth Brain LLC** (also operator of dobrowser.io, a separate AI Chrome extension product for non-developer users). GitHub: https://github.com/SawyerHood. Twitter/X: @sawyerhood. The dev-browser project has a companion product `terragon-oss` (remote background agent orchestrator).

Hood is best known for `draw-a-ui` (13.6k stars) — a tool to convert UI sketches to HTML — which established his reputation in the LLM tooling space. dev-browser is his second major open-source project.

### 3. Comparison to Other AI Browser Automation Tools

| Tool | Approach | Token cost | Setup complexity | Auth sessions | Sandboxed | Stars |
|------|----------|-----------|-----------------|--------------|-----------|-------|
| **dev-browser** | Agent writes scripts → QuickJS → Playwright | Low ($0.88/task) | `npm i -g` | Yes (--connect mode) | Yes (QuickJS WASM) | 4.4k |
| **Playwright MCP** (Microsoft) | MCP server, 26+ discrete tools | High (~13,700 tokens just for tool defs) | npm + config | No | No | >10k |
| **agent-browser** (Vercel) | Rust CLI + Playwright daemon, snapshot+refs | 93% lower than Chrome DevTools MCP | npm i -g | No | No | not found |
| **browser-use** | Python library, full LLM agent loop | High | pip install | Partial | No | 50k+ |
| **Stagehand** (BrowserBase) | AI-native Playwright wrapper | Medium | npm | Yes | No | ~10k |
| **PinchTab** | HTTP server on port 9867 | Very low (~800 tokens/page) | Launch server | Yes | No | unknown |
| **Chrome DevTools MCP** | CDP via MCP | Very high (10,000+ tokens/page) | Chrome debug flag | Yes | No | N/A |

**Key differentiator:** The "code-first" philosophy means the agent can compose arbitrary multi-step logic in a single script, rather than issuing one MCP tool call per browser action. This reduces round-trips (turns) dramatically. However, it requires the LLM to write syntactically valid JavaScript — a failure mode that action-by-action tools avoid.

**vs Playwright MCP specifically:** Playwright MCP exposes every browser action as a separate MCP tool. The tool schema alone costs ~13,700 tokens per session. dev-browser costs ~0 extra tokens for its interface (just a CLI). In the author's benchmarks: dev-browser used 29 turns vs Playwright MCP's 51 turns for the same task.

**vs browser-use:** browser-use has 50k+ stars and a full agent loop, but is Python-only and very token-heavy. dev-browser is Node/npm-native and designed for Claude Code's bash execution model.

**vs agent-browser (Vercel):** agent-browser uses a similar CLI approach with a Rust + Playwright daemon, but without the QuickJS sandbox. It focuses on token efficiency through a "snapshot + refs" element reference system. Independent reviews in 2026 put agent-browser slightly above dev-browser for general use; dev-browser wins on sandboxed security.

### 4. Key Features and Limitations

**Features:**
- `npm install -g dev-browser && dev-browser install` — single install command
- QuickJS WASM sandbox — scripts cannot escape to host OS
- Named persistent pages — state survives across multiple script runs
- Full Playwright Page API (goto, click, fill, locators, evaluate, screenshot, network interception)
- `page.snapshotForAI()` — token-optimized DOM snapshot
- `browser.listPages()` — enumerate open tabs
- File I/O to `~/.dev-browser/tmp/` only
- Chrome extension for connecting to existing Chrome sessions (logged-in state)
- Windows x64 support (added v0.2.3, March 2026)
- Self-documenting `--help` designed as LLM usage guide
- MIT license

**Limitations:**
- QuickJS ≠ Node.js — some JavaScript features unavailable (no `require()`, no native modules)
- File I/O confined to temporary directory only
- Anonymous pages are cleaned up after script completion (use named pages for persistence)
- No direct network access from scripts — all network goes through the browser
- Security model relies entirely on QuickJS sandbox — a sandbox escape = full host access
- One confirmed critical RCE-via-prompt-injection vulnerability (closed as resolved in v0.2.0 rewrite, but details undisclosed)
- Community curator raised unresolved questions about permission model (`npx *` and `--dangerously-skip` flags)

### 5. Open Source Status and GitHub

**Yes, fully open source. MIT license.**

- **Main repo:** https://github.com/SawyerHood/dev-browser
- **Eval/benchmark repo:** https://github.com/SawyerHood/dev-browser-eval
- **Stats (March 2026):** 4.4k stars, 273 forks, 111 commits, 4 releases
- **Latest release:** v0.2.3 (March 25, 2026) — Windows x64 support + npm packaging
- **v0.2.0** (March 19, 2026) — Major rewrite: Rust CLI + Node daemon + QuickJS sandbox (replaced prior architecture)
- **License:** MIT
- **Fork:** https://github.com/wrsmith108/dev-browser-claude-skill — maintained fork

The v0.2.0 rewrite was significant: the entire architecture changed from whatever the pre-0.2 approach was to the current Rust CLI + Node daemon + QuickJS model. The RCE vulnerability was closed as resolved by this rewrite.

### 6. Community Reception

**Quantitative signals:**
- 4.4k GitHub stars (fast growth for a <3-month-old project)
- 273 forks
- 264 installations in Claude Code per agentskills.so (highest of any browser skill)
- 331 weekly downloads on AgentSkills platform
- Listed in awesome-claude-code (pending final approval)
- Listed on: Smithery, FastMCP, LobehHub, MCPMarket, SourceForge mirror

**Qualitative signals:**
- Sawyer Hood's X post advertising the tool received visible community pickup (exact engagement figures unavailable — X blocks scraping)
- awesome-claude-code curator expressed cautious interest but raised security questions (npx permissions, `--dangerously-skip` flag, localhost-only restrictions) that remained unanswered at time of research
- One DEV Community comparison post (testing 6 tools) did NOT include dev-browser in its tested set, ranking PinchTab and browser-use above agent-browser for general use
- A security researcher filed a critical RCE vulnerability issue (#52) — the tool's response was architectural redesign rather than a targeted patch, which is either a sign of good engineering judgment or avoidance of disclosure
- One commenter on issue #52 noted the vulnerability "does not affect other AI-driven browsers (such as the agent-browser project)"

**Overall:** The tool has strong initial adoption driven by Sawyer Hood's reputation (draw-a-ui) and a compelling benchmark narrative. Security posture is the main open question.

### 7. Claude Code Integration

This is where dev-browser has the clearest advantage over MCP-based alternatives.

**Installation for Claude Code:**
```bash
npm install -g dev-browser
dev-browser install  # installs Playwright + Chromium
```

**Pre-approve in `.claude/settings.json`:**
```json
{
  "permissions": {
    "allow": ["Bash(dev-browser *)"]
  }
}
```

This eliminates approval prompts since scripts run in QuickJS sandbox (no host access).

**Skill installation (Claude Code skill ecosystem):**
```
/plugin install dev-browser@sawyerhood/dev-browser
```
Or via marketplace settings.

**How Claude Code uses it:**
Claude Code writes a short script, executes it via `Bash(dev-browser --headless script.ts)`, gets back structured output. No MCP server needed, no extra context tokens for tool schemas. The agent can use the bash tool it already has.

**Compatibility:** Works with Claude Code, Amp, Codex, OpenCode, Gemini CLI, Cursor, GitHub Copilot (the SKILL.md format is portable across all these environments).

---

## Disagreements and Open Questions

1. **Security:** The RCE vulnerability in pre-v0.2.0 was closed as "resolved by rewrite" but the PoC was never disclosed and independently verified. The awesome-claude-code curator's questions about `--dangerously-skip` and npx permission model remain unanswered. **Unresolved.**

2. **dev-browser vs agent-browser:** The benchmark in the repo was authored by Sawyer Hood himself (conflict of interest). Independent reviews that did test agent-browser alongside dev-browser found agent-browser competitive or superior. The comparison is real but the benchmark is self-published. **Inferred from multiple sources, not independently benchmarked.**

3. **"Not production-ready" claim:** A DEV Community review (February 2026) characterized dev-browser as not production-ready, but that review did not actually test dev-browser — it tested a different set of tools. This claim should not be attributed to dev-browser specifically. **Unresolved.**

4. **v0.2.0 release date:** The GitHub releases page shows v0.2.0 as "March 19, 2022" — this is almost certainly a display error; the project was created January 17, 2026. Actual release was likely March 19, 2026. **Inferred.**

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | GitHub — SawyerHood/dev-browser | https://github.com/SawyerHood/dev-browser | Main repo: MIT, 4.4k stars, 273 forks, architecture description | primary | high |
| 2 | GitHub README | https://github.com/SawyerHood/dev-browser/blob/main/README.md | QuickJS sandbox, Playwright API, named pages, `--help` = LLM guide | primary | high |
| 3 | GitHub Releases | https://github.com/SawyerHood/dev-browser/releases | v0.2.0 = major rewrite (Rust+Node+QuickJS), v0.2.3 = Windows support | primary | high |
| 4 | GitHub Eval repo | https://github.com/SawyerHood/dev-browser-eval | Benchmark: 3m53s/$0.88/29 turns vs Playwright MCP 4m31s/$1.45/51 turns | primary (self-published) | medium |
| 5 | GitHub — SawyerHood profile | https://github.com/SawyerHood | Author: ex-Figma, ex-Facebook, 900+ followers, also made draw-a-ui (13.6k stars) | primary | high |
| 6 | agentskills.so | https://agentskills.so/skills/sawyerhood-dev-browser-dev-browser | 264 Claude Code installations, created Jan 17 2026, 331 weekly downloads | secondary | medium |
| 7 | claude-plugins.dev | https://claude-plugins.dev/skills/@SawyerHood/dev-browser/dev-browser | 2.9k stars on community registry, portable SKILL.md format | secondary | medium |
| 8 | dobrowser.io | https://dobrowser.io | Sawyer Hood / Smooth Brain LLC also makes Do Browser (AI Chrome extension, separate product) | primary | high |
| 9 | awesome-claude-code issue #408 | https://github.com/hesreallyhim/awesome-claude-code/issues/408 | Submission pending, security questions raised about permission model | primary | high |
| 10 | GitHub issue #52 | https://github.com/SawyerHood/dev-browser/issues/52 | Critical RCE vulnerability via prompt injection, closed as resolved by v0.2.0 rewrite | primary | high |
| 11 | DEV Community comparison | https://dev.to/minatoplanb/i-tested-every-browser-automation-tool-for-claude-code-heres-my-final-verdict-3hb7 | PinchTab and browser-use recommended over agent-browser; dev-browser not tested in this review | secondary | medium |
| 12 | BSWEN browser comparison | https://docs.bswen.com/blog/2026-02-25-mcp-browser-comparison/ | Playwright MCP costs ~13,700 tokens in tool definitions alone | secondary | medium |
| 13 | Sawyer Hood X post | https://x.com/sawyerhood/status/2002070215405023391 | Public announcement of dev-browser (content unreadable — X blocks scraping) | primary | low |
| 14 | wrsmith108 fork | https://github.com/wrsmith108/dev-browser-claude-skill | Community maintains a fork | secondary | high |
| 15 | Medium — Playwright field guide | https://medium.com/@adnanmasood/playwright-and-playwright-mcp-a-field-guide-for-agentic-browser-automation-f11b9daa3627 | Context on Playwright MCP tool proliferation problem | secondary | medium |

---

## Sources

1. GitHub — SawyerHood/dev-browser — https://github.com/SawyerHood/dev-browser
2. README — https://github.com/SawyerHood/dev-browser/blob/main/README.md
3. Releases — https://github.com/SawyerHood/dev-browser/releases
4. Eval repo — https://github.com/SawyerHood/dev-browser-eval
5. SawyerHood GitHub profile — https://github.com/SawyerHood
6. agentskills.so skill listing — https://agentskills.so/skills/sawyerhood-dev-browser-dev-browser
7. claude-plugins.dev listing — https://claude-plugins.dev/skills/@SawyerHood/dev-browser/dev-browser
8. dobrowser.io — https://dobrowser.io
9. awesome-claude-code issue #408 — https://github.com/hesreallyhim/awesome-claude-code/issues/408
10. GitHub security issue #52 — https://github.com/SawyerHood/dev-browser/issues/52
11. DEV Community — "I Tested Every Browser Automation Tool" — https://dev.to/minatoplanb/i-tested-every-browser-automation-tool-for-claude-code-heres-my-final-verdict-3hb7
12. BSWEN browser automation comparison — https://docs.bswen.com/blog/2026-02-25-mcp-browser-comparison/
13. Sawyer Hood X post — https://x.com/sawyerhood/status/2002070215405023391
14. wrsmith108 fork — https://github.com/wrsmith108/dev-browser-claude-skill
15. agent-browser (Vercel) — https://github.com/vercel-labs/agent-browser
16. browser-use — https://github.com/browser-use/browser-use (50k+ stars)
17. FastMCP listing — https://fastmcp.me/skills/details/460/dev-browser
18. Smithery listing — https://smithery.ai/skills/SawyerHood/dev-browser

---

## Coverage Status

- **Directly verified (read source):** Architecture, QuickJS sandbox, Playwright API, installation, author identity, license, release history, benchmark numbers (self-published), security vulnerability, community listing stats, dobrowser.io company info, awesome-claude-code discussion
- **Inferred from multiple sources:** GitHub star count (4.4k reported by two independent sources), Claude Code integration steps, comparison table metrics
- **Unresolved:** Exact X/Twitter engagement metrics (X blocks scraping), independent third-party benchmark of dev-browser vs agent-browser, final security audit of v0.2.0 architecture, whether `--dangerously-skip` flag exists/what it does

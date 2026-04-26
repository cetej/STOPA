---
type: feasibility-research
date: 2026-04-25
topic: Claude Managed Agents Memory × Claude Code compatibility
related_issues: [STOPA#26, NG-ROBOT#11, POLYBOT#4]
sources_checked: 6
---

# Managed Agents Memory — Claude Code fit assessment

## 1. Verdict (1 line)

**API-BRIDGE-REQUIRED.** Memory stores live in Anthropic's hosted session containers (`/mnt/memory/<store>/`); Claude Code skill runtime cannot mount them — only the Platform API/SDK or new `ant beta:memory-stores` CLI can read/write.

## 2. Evidence

- **Filesystem mount is a Managed Agents session container, not a local CC FS.** Docs: "When you attach a store to a session, it is mounted as a directory inside the session's container... Each attached store is mounted inside the session's container as a directory under `/mnt/memory/`." Attachment happens via `client.beta.sessions.create(resources=[{type: memory_store, memory_store_id: ...}])` — a Platform-API session, not a CC session. ([memory docs](https://platform.claude.com/docs/en/managed-agents/memory))
- **Managed Agents is explicitly separated from Claude Code.** Anthropic's branding rules forbid partners from calling Managed Agents products "Claude Code" or "Claude Code Agent". The overview page lists Managed Agents as one of *two* ways to build with Claude (Messages API vs Managed Agents) — Claude Code is not a third option that maps onto memory stores. ([overview docs](https://platform.claude.com/docs/en/managed-agents/overview)) Coverage on 2026-04-19 confirms: "Claude Managed Agents remains separate from Claude Code." ([SD Times](https://sdtimes.com/anthropic/anthropic-adds-memory-to-claude-managed-agents/))
- **All examples are SDK/API/CLI — zero CC integration paths shown.** Memory CRUD examples cover curl, `ant beta:memory-stores` CLI, Python/TS/Go/Java/PHP/Ruby/C# SDKs. No `claude` CLI flag, no settings.json key, no MCP example, no skill-frontmatter integration. Required header `anthropic-beta: managed-agents-2026-04-01` is a Platform-API beta header, not exposed to CC sessions.
- **Memory stores can be edited from anywhere via REST.** `POST /v1/memory_stores/{id}/memories` works with just an API key + beta header. This is what makes the bridge feasible: a thin MCP server (or Python wrapper) running in the CC environment can read/write a memory store identical to one that an Anthropic-hosted Managed Agent attaches to — same store, two clients.
- **Distinct from "Memory tool" (`memory_20250818`).** That separate feature IS client-side (CC could implement handlers for it, mapping `/memories` paths to STOPA's `.claude/memory/`). But it does not provide cross-session persistence in Anthropic infra — it is just a tool definition that calls back into the client's filesystem. ([memory tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool))

## 3. Recommended action — STOPA#26

**Build MCP bridge (small).** Create `stopa-memory-mcp` that exposes `memstore.read(path)`, `memstore.write(path, content)`, `memstore.list(prefix)`, `memstore.diff(version_a, version_b)` against a configured `memstore_id`. Skills like `/scribe`, `/handoff`, `/checkpoint` gain optional dual-write: local `.claude/memory/` (always) + remote memstore (when MCP server configured). Buys versioning/audit trail and lays groundwork for sharing memory with future Anthropic-hosted Managed Agent sessions, without abandoning the local-first model that defines STOPA. **Do NOT** implement directly — there is no "attach to memstore from CC config" feature to use.

## 4. Recommended action — POLYBOT#4 + NG-ROBOT#11

**Same: MCP bridge, but lower priority than STOPA#26.** Both projects gain less than STOPA: they are content/trading pipelines, not orchestrators with rich shared memory. Sequence:

1. STOPA#26 first — build & validate the MCP bridge in the orchestration project that needs versioned memory most.
2. POLYBOT#4 — adopt only if PaperTrader needs cross-session position memory survives crashes (likely yes; score 5 stands).
3. NG-ROBOT#11 — adopt only if pipeline runs need shared "previously-seen sources" memory (probably overkill at score 3; reasonable to **close as not-applicable** after STOPA bridge proves the pattern, then revisit).

## 5. Pricing notes

**Memory pricing not yet announced as of 2026-04-25.** Confirmed billed today: $0.08/session-hour, web search $10/1k searches, plus standard token rates. One pricing analysis explicitly states memory "could carry additional cost implications when they leave preview. I don't know yet." ([WaveSpeedAI pricing breakdown](https://wavespeed.ai/blog/posts/claude-managed-agents-pricing-2026/)) Beta limits: 1,000 stores/org, 2,000 memories/store, 100 MB/store, 100 kB/memory, 30-day version retention. Free in beta is plausible but not guaranteed — assume separate per-MB or per-version line-item will appear at GA.

## 6. Key risk (1 line)

**Anthropic ships first-class CC ↔ memstore integration in next CC release**, making the MCP bridge redundant — watch [CC release notes](https://docs.claude.com/en/docs/claude-code/changelog) and the `claude-managed-agents` mailing list before building; if integration lands within ~30 days, defer the bridge entirely.

## Sources

- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory)
- [Memory tool (distinct, client-side)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Anthropic engineering: Managed Agents](https://www.anthropic.com/engineering/managed-agents)
- [Anthropic adds memory to Claude Managed Agents — SD Times (2026-04-19, "remains separate from Claude Code")](https://sdtimes.com/anthropic/anthropic-adds-memory-to-claude-managed-agents/)
- [Claude Managed Agents Pricing — WaveSpeedAI](https://wavespeed.ai/blog/posts/claude-managed-agents-pricing-2026/)
- [Built-in memory for Claude Managed Agents — Anthropic blog](https://claude.com/blog/claude-managed-agents-memory)

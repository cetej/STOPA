# Provenance: Meta-Agent Competitive Landscape

**Date:** 2026-04-21
**Question:** Competitive landscape of meta-agent systems with persistent memory for personal productivity — strategic positioning for STOPA (ADR 0016 Phase B)
**Scale:** survey
**Rounds:** 2 (Discovery Haiku → Reading Sonnet) + 1 lead-verification spot-check
**Sources:** 45+ URLs consulted / 14 directly read via Jina Reader / 1 lead-verified manually (Zep pricing)
**Verification:** partial — lead verified the most questionable claim directly; 2 Sonnet reading agents applied Self-RAG reflection tags; no dedicated verifier sub-agent run (time budget)

## Research Files

| File | Agent | Purpose |
|------|-------|---------|
| `outputs/.research/meta-agent-competitive-discovery-A.md` | Haiku disc-A | Memory frameworks (Letta, mem0, LangMem, Zep) |
| `outputs/.research/meta-agent-competitive-discovery-B.md` | Haiku disc-B | Orchestrators (OpenHands, Goose, SWE-agent, Sakana, Suna) |
| `outputs/.research/meta-agent-competitive-discovery-C.md` | Haiku disc-C | Coding agents with persistence |
| `outputs/.research/meta-agent-competitive-discovery-D.md` | Haiku disc-D | Obsolescence signals Q1-Q2 2026 |
| `outputs/.research/meta-agent-competitive-reading-1.md` | Sonnet read-1 | Memory + Claude ecosystem deep reading |
| `outputs/.research/meta-agent-competitive-reading-2.md` | Sonnet read-2 | Orchestrators + platform obsolescence deep reading |
| `outputs/meta-agent-competitive-landscape.md` | Lead (Opus) | Final synthesis + comparison table + strategic recommendations |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 14 (direct fetch, content confirmed) |
| [INFERRED] | 5 (STOPA competitive positioning derived from multi-source + internal) |
| [UNVERIFIED] | 3 (rejected: Mem0 "91.6/93.4", LangMem P95 59.82s, CC v2.1.30+) |
| [SINGLE-SOURCE] | 1 (Gemini 10-action limit — not in primary source) |

## Known gaps / follow-up worth doing

1. **Mem0 LongMemEval scores** — primary source not fetched. Next read: ECAI 2025 paper PDF.
2. **Microsoft Copilot Studio actual pricing** — marketing blog doesn't have pricing. Next read: microsoft.com/en-us/microsoft-365-copilot/microsoft-copilot-studio pricing page.
3. **OpenHands Index exact SWE-bench Verified %** — chart image in blog. Next read: arXiv paper or benchmark repo.
4. **Gemini Scheduled Actions** — claim not in Jan 2026 Drop. Next search: Google I/O 2025 recap or later Gemini feature drops.
5. **Letta Context Repositories** — deeper dive needed. Letta blog confirmed existence (Feb 2026) but implementation details worth reading.

## Budget consumed

- Discovery agents: 4 × Haiku × ~5 tool calls = ~20 WebSearch calls, ~400K tokens total
- Reading agents: 2 × Sonnet × ~8 tool calls = ~16 fetch calls (some retries), ~600K tokens total
- Lead verification: 1 direct Jina Reader curl (Zep pricing)
- Synthesis: 0 tool calls (file writes only)
- **Wall time:** ~18 min (vs skill estimate ~16 min — slight overshoot due to Sonnet retries)
- **Estimated cost:** ~$3.50 (deep tier budget)

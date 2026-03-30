# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-03-29 (full) | Next: ~2026-04-05

## Action Items

| # | Item | Urgency | Next Step |
|---|------|---------|-----------|
| 36 | Haiku 3 deprecation (deadline 2026-04-19) | HIGH | Zkontrolovat STOPA/NG-ROBOT/ADOBE pro hardcoded `claude-3-haiku-20240307` → nahradit `claude-haiku-4-5-20251001` |
| 41 | LiteLLM supply chain attack (v1.82.8 malware) | MED | Audit zda naše projekty používají LiteLLM |
| 29t | Bootleg SSL (arXiv:2603.15553) | LOW | Sledovat pro ORAKULUM/ZACHVEV pokud Chronos-2 nestačí |
| 29s | Attention innovations status | INFO | Produkce: MLA, GQA, iRoPE. Sledovat DiffAttn DEX adapter + TransMLA |
| 29r | `hf papers` CLI (AK) | LOW | Kandidát pro upgrade /watch Tier 2b strategy |

## Watch List

### Models & Releases
| Item | Detail | Trigger |
|------|--------|---------|
| 40. Mythos/Capybara | Next tier above Opus, leaked 2026-03-26. Step change coding+reasoning. | GA datum → přeplánovat STOPA model tiers |
| 35. CC v2.1.85 | /compact fix, deniedMcpServers fix, timestamp markery, MCP OAuth | Informativní |
| 5. Haiku 3 retire | 2026-04-19 deadline | Audit před deadline |
| 18. Gemini 3.1 Pro | 77.1% ARC-AGI-2, $2/$12 | Multi-provider srovnání |
| 29g. Gemini 3.1 Flash-Lite | $0.25/M — 1/8 ceny Pro | Cost tier reference |

### Video & Diffusion (test1/NG-ROBOT relevance)
| Item | Detail |
|------|--------|
| 29p. PyTorch 2.11 | FlexAttention + FA4 — test1 dependency |
| 29q. Modular Diffusers 0.37.0+ | Composable pipeline — test1 refactor |
| 29b. Foveated Diffusion | Spatially adaptive token alloc — video efficiency |
| 29c. FSVideo | 14B DIT, "order of magnitude faster" — Pyramid Flow alt |
| 26. 3× flow matching papers | FastLightGen, Warm-Start FM, Transition FM |
| 21. Wan2.1 + LTX 0.9.5 | Diffusers 0.37.0 video models |
| 29k. Luma Uni-1 | Decoder-only image gen, ~$0.09/img — /nano kandidát |

### Agent/Tool Research
| Item | Detail |
|------|--------|
| 29l. AgentScope | Alibaba, Apache 2.0, MsgHub orchestration, ReMe memory |
| 29m. MCP Elicitation | MCP servers → structured user input mid-task |
| 29f. Agent SDK repos | claude-agent-sdk-python + typescript |
| 29e. Mem0 | Graph-based memory architecture — STOPA inspirace |
| 9. OpenClaw/NemoClaw | Messaging-first agent runtime, 250k★ |

### Papers (metodologie)
| Item | Relevance |
|------|-----------|
| 29n. SWAP | Stepwise CoT penalization → cost reduction pro Opus calls |
| 29o. FinMCP-Bench | MCP tool-use benchmark, 613 vzorků |
| 29d. Beyond the Prompt | ICL/CoT mechanismy — validuje skill trigger design |
| 22. BOULDER | Multi-turn degrades reasoning → prefer single-shot evals |
| 23. MCPAgentBench | MCP tool discrimination benchmark |
| 24. CARE | Confounder-aware LLM-as-judge, −26.8% bias |
| 25. ToolTree | MCTS tool planning, ~10% gain |
| 27. SWE-CI | CI-loop benchmark, long-term maintenance |
| 28. ClarEval | Agent ambiguity detection benchmark |
| 8. Czech ABSA | ufal/robeczech-base — ZACHVEV sentiment |

### Ecosystem
| Item | Detail |
|------|--------|
| 1. Channels | Telegram/Discord integration. CRITICAL: no message queue |
| 2. /context suggestions | Memory bloat detection |
| 3. Memory timestamps | CC freshness awareness |
| 4. autoMemoryDirectory | Custom memory path |
| 5. /remote-control | CC ↔ claude.ai/code ↔ VS Code bridge |
| 6. GitHub Spec Kit | Competitor analysis done: `competitive-spec-kit.md` |
| 19. Papers with Code → HF | huggingface.co/papers/trending |
| 20. MCP lazy loading | Up to 95% context reduction |

## Scan History

### 2026-03-29 — full (PyTorch 2.11, Modular Diffusers, hf papers CLI)
### 2026-03-28 — full (Mythos leak, LiteLLM, MCP Elicitation, papers)
### 2026-03-27 — targeted (CC v2.1.85)

Older: see `news-archive.md`

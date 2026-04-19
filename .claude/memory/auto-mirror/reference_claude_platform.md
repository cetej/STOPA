---
name: Claude Platform Intelligence
description: Claude Code internals, pricing analysis, nerfing patterns, Anthropic features — forward-looking platform intel
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Collected intelligence on Claude platform behavior and features.

| Topic | Source | Key Finding |
|-------|--------|------------|
| CC source leak (2026-03-31) | npm 2.1.88 | KAIROS daemon, COORDINATOR_MODE native orchestrator, auto-permissions, Numbat model |
| Thinking budget nerfing | AMD AI Director analysis | 2200→600 chars, reads-per-edit 6.6→2.0, GPU-load-sensitive |
| Pricing reversals | arXiv:2603.23971 | 21.8% model pairs show reversal due to thinking tokens; benchmark actual cost |
| Advisor Strategy | Anthropic | Native Opus-as-advisor API for Sonnet/Haiku executors, zero orchestration overhead |
| Routines | Anthropic | Cloud automations (schedule/webhook/API), max 15 runs/day |
| SkillClaw auto-evolve | Community | summarize+evolve scripts, daily task, /evolve --candidates |
| Emotion vectors | Anthropic (2026-04-02) | Desperation drives corner-cutting, calm steering reduces it — basis for panic-detector |
| ccusage | CLI/MCP tool | Real token tracking, integrated into /budget skill |
| RTK | Token proxy | PreToolUse hook for 60-90% token savings on CLI outputs |
| claude-code-local (nicedreamzapp) | Community repo | Direct Anthropic API server (localhost:4000) + MLX for Apple Silicon; Qwen 3.5 122B MoE @ 65 tok/s, Gemma 4 31B, Llama 3.3 70B. `ANTHROPIC_BASE_URL` redirect. Tool-call reliability: KV cache 4→8-bit after token 1024, temp 0.2, garbled-output recovery. **Apple Silicon only — no Windows path** (user runs Windows 11). Reference value: API-compat layer pattern, tool-call fix tactics |

---
name: Agent Architecture Research Cluster
description: Papers on multi-agent orchestration, team topology, skill decomposition, context scoping — informing STOPA orchestrate design
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Cluster of papers informing STOPA agent orchestration design.

| Paper | Key Finding | STOPA Impact |
|-------|------------|--------------|
| AutoAgent (arXiv) | Same-model empathy, anti-overfitting guard, traces >> scores | Adopted into autoloop/self-evolve |
| addyosmani/agent-skills | Anti-rationalization tables, red flags, verification checklists | Adopted into all SKILL.md files |
| @systematicls | Agent failure taxonomy, N-plan selection, session contracts | Informed orchestrate error handling |
| AgentLaboratory (arXiv:2501.04227) | NeurIPS-form scoring, multi-persona review, code-edit-execute-repair | Adopted in STOPA agent patterns |
| CAID (CMU) | Git worktree coordination, 4 agents optimal | Validates orchestrate agent limits |
| Self-org agents (arXiv:2603.28990) | +14% paper / +8% STOPA test; hybrid approach | Hybrid orchestrate plan |
| Distributed systems (arXiv:2603.12229) | Amdahl gate, centralized >> decentralized | Cost-performance tradeoffs |
| Atomic skills (arXiv:2604.05013) | 5 atomic coding skills, joint RL +18.7% | Created /reproduce and /generate-tests |
| DACS (arXiv:2604.07911) | Registry↔Focus context switching, 3.53× efficiency | Multi-agent context scoping |
| NLAH (arXiv:2603.25723) | SKILL.md = academic NLAH validation; self-evolution +4.8% | Validates STOPA skill file approach |
| IBM workflow survey | Static→dynamic spectrum, 3 gaps in orchestrate | Informed workflow optimization |
| Combee (arXiv:2604.04247) | √n hierarchical aggregation, 17x parallel speedup | Parallel prompt learning |
| SLM-Agentic (arXiv:2506.02153) | SLMs match LLMs on function-calling; heterogeneous model composition; LoRA/QLoRA fine-tuning accessible | Validates haiku-for-validation + sonnet/opus-for-reasoning routing; supports budget tier design |
| Multica (15.4k stars, open-source CMA) | 6-table relational memory, ZERO embeddings; explicit skill attachment via `agent_skill` JOIN; JSONB snapshot at dispatch (DB cold during inference); workspace_id cascade isolation; "curated relevance beats learned similarity for coding" | Validates STOPA grep-first + curated `discovery-keywords` approach; JSONB snapshot = STOPA state.md/PRP pattern; limitations (stale snapshots, no cross-workspace) addressed by STOPA hybrid retrieval + /improve routing |

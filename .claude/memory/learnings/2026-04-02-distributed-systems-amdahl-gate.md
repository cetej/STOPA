---
date: 2026-04-02
type: architecture
severity: high
component: orchestration
tags: [orchestration, multi-agent, distributed-systems, cost-optimization]
summary: "arXiv:2603.12229 proves centralized > decentralized for LLM teams (1.36× vs 0.88× speedup). Serial tasks (p<0.4) cost 5.83× tokens for 1.13× speedup. Added Amdahl parallelizability gate and ROI cost gate to orchestrate skill."
source: external_research
confidence: 0.8
uses: 0
harmful_uses: 0
verify_check: "Grep('Parallelizability Gate', path='.claude/commands/orchestrate.md') → 1+ matches"
successful_uses: 0
---

## LLM Teams as Distributed Systems — Key Numbers

Paper: arXiv:2603.12229 (Mieczkowski et al., Princeton, 2026-03)

### Empirical findings:
- Centralized (hub-spoke) teams: **1.36× median speedup**, 4 test failures
- Decentralized (mesh) teams: **0.88× median speedup** (WORSE than single agent), 19 test failures
- Actual speedup ≈ **75% of Amdahl's theoretical maximum** due to coordination overhead
- Serial tasks (p<0.4): **5.83× cost for 1.13× speedup** — negative ROI
- 45% of decentralized messages were unproductive ("standing by", encouragement)
- Diminishing returns after 4 agents on most tasks
- Claude Sonnet 4.6 scales best among tested models

### Implementation in STOPA:
1. **Parallelizability Gate** (Phase 1): p = independent_subtasks / total_subtasks → caps tier
2. **Cost Gate** (Phase 3): ROI = (Amdahl speedup × 0.75) / (agents × 1.15) → warns if <0.5
3. **3-level File Access Manifest**: WRITE/READ/FORBIDDEN per agent → prevents concurrent write failures
4. **Wave Checkpoint**: per-wave state save for crash recovery

### Prevention:
Before spawning multi-agent setup, always estimate p and ROI. p < 0.4 → single agent.

---
name: Hippocampus Integration Plan
description: 3-phase plan to add associative memory (spreading activation, Hebbian learning, auto-skill detection) to STOPA, inspired by claude_hippocampus
type: project
---

## Source

GitHub: allthingssecurity/claude_hippocampus — neuroscience-inspired associative memory for Claude Code.
Key patterns: spreading activation, Hebbian learning, exponential decay (lambda=0.03, 23d half-life), auto-skill crystallization.

## Decision (2026-04-03)

Adopt hippocampus patterns in 3 phases, adapted to STOPA's zero-dependency file-based architecture (no Neo4j).

**Why:** Current STOPA memory is passive (uses=0 for all 52 learnings), grep-only retrieval misses semantic connections, no feedback loops. Hippocampus demonstrated 29% faster tasks, 13% fewer tokens, 36% fewer tool calls.

**How to apply:** Implement incrementally — Phase 1 fixes dead counters, Phase 2 adds associative recall, Phase 3 adds self-improving memory.

## Phase 1: "Living System" (2-3 days)

### 1a. Learning tracker hook
- PostToolUse hook on Grep matching learnings/ path
- Parse grep output, identify matched learning files
- Auto-increment `uses:` in YAML frontmatter
- Log retrievals to sessions.jsonl

### 1b. Critic feedback loop
- Extend /critic skill: when finding issue caused by applied learning → harmful_uses += 1
- When learning led to good result → confidence += 0.05

### 1c. Lifecycle automation (SessionStart hook or cron)
- Promotion: uses >= 10 AND confidence >= 0.8 AND harmful < 2 → critical-patterns.md
- Retirement: harmful_uses >= uses AND harmful > 2 → learnings-archive/
- Stale: 60+ days unused AND confidence < 0.5 → [STALE] tag

## Phase 2: "Associative Layer" (1-2 weeks)

### 2a. Concept graph
- File: `.claude/memory/concept-graph.json`
- Entities: extracted from learning tags, bodies, checkpoints, decisions
- Edges: co-occurrence with weight, count, contexts (projects)
- Size estimate: ~50KB for 500 concepts + 2000 edges

### 2b. Concept extraction
- Regex patterns from hippocampus: CamelCase, hyphenated, tech patterns, error types
- Run on existing learnings (one-time) + incremental on new ones
- No LLM required

### 2c. File-based spreading activation
- Keyword extraction from prompt (stopwords filter, bigrams)
- Seed: match keywords → entities
- Spread: 2 hops, decay 0.3, threshold 0.15, max 20 neighbors/hop
- Rank: activation x recency x workspace context
- Map back to learning files
- Target latency: 50-100ms (in-memory JSON)

### 2d. UserPromptSubmit hook (auto-injection)
- Load concept-graph.json (cached)
- Spread activation on user prompt
- Map to top 5 learnings
- Compress to 1200-token context packet
- Return as suppressedUserMessage
- Skips prompts < 5 chars or starting with /

## Phase 3: "Transformation" (4-6 weeks, next sessions)

### 3a. Hebbian learning on session-end (Stop hook)
- Extract concepts from session traces
- Build co-occurrence edges in concept-graph.json
- Apply exponential decay (lambda=0.03)
- Detect workflow patterns

### 3b. Auto-skill crystallization
- 20+ tech archetype patterns
- Cross-project detection (pattern in 3+ projects)
- Generate draft SKILL.md with trigger concepts

### 3c. Cross-project memory transfer
- Shared concept-graph with workspace context boosting
- 1.5x weight for same-project, 1.0x for cross-project

### 3d. Contrastive model gating
- Auto-detect model-specific learnings
- Filter by current model at retrieval time

## Key Constants (from hippocampus, tuned for file-based)

```
MAX_SEEDS = 7
MAX_SPREAD_HOPS = 2
SPREAD_DECAY = 0.3
ACTIVATION_THRESHOLD = 0.15
MIN_COACTIVATION_WEIGHT = 1.0
MAX_NEIGHBORS_PER_HOP = 20
MAX_ACTIVATED = 15
CONTEXT_PACKET_MAX_TOKENS = 1200
RECENCY_LAMBDA = 0.03  # half-life ~23 days
```

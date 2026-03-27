# Skill Tiers — Progressive Disclosure

Skills are organized into 4 tiers by frequency of use. This helps Claude prioritize which skills to suggest.

## Tier 1 — Core (always suggest when relevant)
Daily-use skills that should be triggered proactively:
- `/orchestrate` — multi-step task decomposition
- `/scout` — codebase exploration before changes
- `/critic` — quality review after edits
- `/checkpoint` — session state management
- `/scribe` — decision and learning capture
- `/status` — system state dashboard (task, budget, checkpoint, health)

## Tier 2 — Extended (suggest when task matches)
Specialized skills for specific workflows:
- `/fix-issue` — GitHub issue resolution
- `/autofix` — PR CI failure & review comment fixer (cloud or local)
- `/deepresearch` — multi-agent evidence-based research with citations
- `/peer-review` — adversarial review of research artifacts and documents
- `/brainstorm` — spec refinement from vague ideas
- `/prp` — context packet for handoffs
- `/handoff` — capture findings from completed/remote sessions into persistent memory
- `/verify` — end-to-end proof of correctness
- `/harness` — deterministic pipelines
- `/security-review` — vulnerability analysis
- `/dependency-audit` — outdated/risky packages
- `/incident-runbook` — failure diagnosis
- `/scenario` — edge case & failure mode explorer (pre-implementation)
- `/liveprompt` — live community prompt intelligence (what works RIGHT NOW for a topic)

## Tier 3 — Advanced (only on explicit request)
Generative/creative tools and meta-skills:
- `/nano` — image generation (requires FAL_KEY)
- `/klip` — video generation (requires FAL_KEY)
- `/skill-generator` — create/modify skills
- `/autoloop` — iterative optimization
- `/project-init` — new project setup
- `/watch` — ecosystem news scan
- `/compact` — context compaction (save results to disk, auto-summarize with Haiku)
- `/budget` — cost tracking
- `/browse` — Chrome automation
- `/youtube-transcript` — video transcripts

## Tier 4 — Methodology (suggest when development discipline matters)
Engineering methodology skills inspired by superpowers patterns:
- `/tdd` — RED-GREEN-REFACTOR enforcer for test-driven development
- `/systematic-debugging` — 4-phase root cause methodology (no guessing)

## How to Apply

When the user describes a task:
1. Check Tier 1 skills first — these cover 80% of workflows
2. If task is specialized, suggest the matching Tier 2 skill
3. Only mention Tier 3 skills when user explicitly asks or when the specific capability is clearly needed
4. Suggest Tier 4 skills when user is debugging (→ /systematic-debugging) or implementing with tests (→ /tdd)
5. Never list all skills unprompted — suggest 1-2 most relevant ones

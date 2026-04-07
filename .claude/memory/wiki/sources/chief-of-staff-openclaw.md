---
title: "How I Built a Chief of Staff on OpenClaw"
slug: chief-of-staff-openclaw
source_type: social_post
url: ""
date_ingested: 2026-04-07
date_published: "2026-04-06"
entities_extracted: 7
claims_extracted: 7
---

# How I Built a Chief of Staff on OpenClaw

> **TL;DR**: VC investor built a production AI chief of staff ("Stella") on OpenClaw with two-layer memory, weekly kaizen loop, meeting prep/follow-through pipeline, and operational daily rhythm. Key architectural insight: LLMs for judgment, Python scripts for deterministic work. ~800K views, widely shared blueprint.

## Key Claims

1. Session memory alone is insufficient — two-layer memory (daily logs + curated MEMORY.md) needed for real continuity — `argued`
2. Flat markdown > database for AI memory: transparency + editability increases trust and reduces fix time — `argued`
3. Judgment-script separation is required for reliability: pushing deterministic work through LLMs causes unpredictable failures — `argued`
4. Weekly kaizen loop (cron research + community scan + friction detection) produces measurably better system on cadence — `argued`
5. Smaller trusted system beats larger system you route around — kaizen enforces continuous pruning — `argued`
6. Per-person commitment tracking in markdown prevents things slipping between meetings — `asserted`
7. First versions are always too complicated — disciplined refactoring loop required — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [OpenClaw](../entities/openclaw.md) | tool | updated |
| [Kaizen Loop](../entities/kaizen-loop.md) | concept | new |
| [Daily Notes Memory Pattern](../entities/daily-notes-memory-pattern.md) | concept | new |
| [Judgment-Script Separation](../entities/judgment-script-separation.md) | concept | new |
| [Operational Rhythm Pattern](../entities/operational-rhythm-pattern.md) | concept | new |
| [Per-Person Commitment Tracking](../entities/per-person-commitment-tracking.md) | concept | new |

## Relations

- `OpenClaw` uses `Daily Notes Memory Pattern`
- `OpenClaw` uses `Kaizen Loop`
- `Judgment-Script Separation` part_of `OpenClaw`
- `Operational Rhythm Pattern` uses `Kaizen Loop` (rhythm emerges from kaizen iteration)
- `Per-Person Commitment Tracking` part_of `Daily Notes Memory Pattern`

## Cross-References

- Related wiki articles: [memory-architecture](../memory-architecture.md) (validates two-layer memory), [hook-infrastructure](../hook-infrastructure.md) (judgment-script = hook pattern), [pipeline-engineering](../pipeline-engineering.md) (operational rhythm with cron)
- Related learnings: Harness > Skill for deterministic processes (critical-patterns.md #4)
- Contradictions: none detected

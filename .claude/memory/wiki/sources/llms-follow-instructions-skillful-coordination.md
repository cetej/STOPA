---
title: "How LLMs Follow Instructions: Skillful Coordination, Not a Universal Mechanism"
slug: llms-follow-instructions-skillful-coordination
source_type: url
url: "https://arxiv.org/abs/2604.06015"
date_ingested: 2026-04-08
date_published: "2026-04-07"
entities_extracted: 3
claims_extracted: 5
---

# How LLMs Follow Instructions: Skillful Coordination, Not a Universal Mechanism

> **TL;DR**: Instruction-following is NOT a single universal mechanism in LLMs — it's a compositional coordination of diverse task-specific representations. Different constraint types (structural vs semantic) live at different layers and have sparse, asymmetric cross-task dependencies.

## Key Claims

1. General probes underperform task-specific probes across all models — minimal shared representations between instruction types — `verified`
2. Cross-task transfer is weak and clusters by task similarity, not by instruction category — `verified`
3. Early layers encode structural constraints, late layers encode semantic constraints — `verified`
4. Constraint satisfaction is dynamic (continuous monitoring during generation), not pre-generation planning — `argued`
5. Activation steering interventions can be made more targeted using layer-type mapping — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Instruction-Following Specialization](../entities/instruction-following-specialization.md) | concept | new |
| [Activation Steering](../entities/activation-steering.md) | concept | new |
| [Dynamic Constraint Monitoring](../entities/dynamic-constraint-monitoring.md) | concept | new |

## Relations

- Instruction-Following Specialization `contradicts` Universal Instruction Mechanism (assumed prior in alignment literature)
- Dynamic Constraint Monitoring `supports` CORAL heartbeat mid-run steering pattern
- Activation Steering `uses` layer-type mapping from Instruction-Following Specialization

## Cross-References

- Related learnings: none matched (new territory)
- Related wiki articles: [skill-design](../skill-design.md) (validates specialized-over-general architecture), [hook-infrastructure](../hook-infrastructure.md) (activation steering angle)
- Related sources: [coral-autonomous-multi-agent-evolution](coral-autonomous-multi-agent-evolution.md) (heartbeat steering validated by dynamic monitoring finding)
- Contradictions: none with existing learnings

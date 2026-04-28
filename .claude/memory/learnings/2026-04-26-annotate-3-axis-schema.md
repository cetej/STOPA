---
date: 2026-04-26
type: best_practice
severity: medium
component: skill
tags: [evaluation, annotate, trajectory, annotation]
summary: "AgentRewardBench zavádí 3-osé expert anotační schema (success / side effects / repetitiveness) jako náhradu binárního labelu. Toto schema by měl adopovat /annotate Align Evals pro richer eval dataset."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.75
maturity: draft
verify_check: "manual"
skill_scope: [annotate]
task_context:
  task_class: research
  complexity: low
  tier: light
---

# 3-Axis Annotation Schema for Agent Trajectory Evals

## Source

AgentRewardBench (Lù et al.) — 1,302 trajectories × 5 benchmarks × 4 agents

## Schema

Místo binárního good/bad labelu použít 3 nezávislé binární otázky:
1. **Success** — dokončil agent task jako definováno?
2. **Side Effects** — provedl agent zbytečné akce s potenciálními side effecty?
3. **Repetitiveness** — vstoupil agent do cyklu repetitivních akcí?

## Proč lepší

- Binary label nerozlišuje: "úspěšně ale se side effecty" vs "úspěšně bez side effectů"
- Repetitiveness jako samostatná osa zachytí doom-loop pattern (STOPA panic-detector territory)
- Richer dataset = lepší signal pro /self-evolve a /eval

## STOPA aplikace

Při `/annotate` Align Evals trase, nahradit binary label tímto 3-osovým formulářem. Uložit jako `{success: bool, side_effects: bool, repetitive: bool}` v annotation JSONL.

## Evidence

- arXiv:2504.08942v2 — AgentRewardBench přímý read v reading agentovi deepresearch pipeline

---
date: 2026-03-23
type: best_practice
severity: high
component: pipeline
tags: [harness, deterministic, python, validation]
---

## Problém
Skills provide best-effort execution (~90%) but some processes need deterministic reliability.

## Root Cause
LLM prompts can't guarantee execution order or programmatic validation between steps.

## Reseni
Fixed phases (Python controls order) + programmatic validation after each step + template output. LLM works inside phases but cannot skip/change order. Skills = best effort (90%). Harness = deterministic (99.9%). Prompt tweaking caps at ~95%.

## Prevence
For any repeatable multi-step process where reliability matters, use harness pattern. See `docs/HARNESS_STRATEGY.md`.

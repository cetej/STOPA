---
date: 2026-04-05
type: architecture
severity: high
component: orchestration
tags: [memory, orchestration, self-improvement, traces]
summary: "Self-improving harness: 6 upgrades closing feedback loops — auto-scribe writes learnings automatically, trace-bridge unifies formats, graduation-check auto-detects promotable learnings, impact-tracker measures learning effectiveness via critic scores, strategy persistence enables warm-start across sessions, auto-handoff chains enforce skill transitions on PIVOT/PLATEAU"
source: user_correction
maturity: draft
confidence: 0.95
uses: 1
harmful_uses: 0
impact_score: 0.0
verify_check: "Glob('.claude/hooks/graduation-check.py') → 1+ matches"
successful_uses: 0
---

## Description

Implementováno 6 vylepšení pro self-improving harness (inspirováno článkem o agent harnesses, Gentilcoreův trace learning, Meta-Harness):

1. **Auto-scribe loop closure** — auto-scribe.py nyní zapisuje learnings automaticky s `source: agent_generated`, `confidence: 0.5`. Enrichuje analýzu ze session traces. Uzavírá hlavní feedback smyčku: experiment → trace → learning → retrieval → aplikace.

2. **Trace-bridge.py** — Stop hook, který kopíruje per-run optimization traces (.traces/<run_id>/tools.jsonl) do session trace formátu (.traces/sessions/*.jsonl). Discover nyní vidí i autoresearch/autoloop experimenty.

3. **Graduation-check.py** — PostToolUse hook na Write/Edit do learnings/. Auto-detekuje learnings překračující graduation threshold a zapisuje je do graduation-candidates.md. /evolve pak jen review + approve.

4. **Impact-tracker.py** — PostToolUse hook na Skill(critic). Sleduje rolling average critic výsledků pro learnings použité v session. Pragmatická alternativa k A/B testování.

5. **Cross-session strategy persistence** — autoresearch nyní ukládá strategy-state.json s approaches_tried, failure_categories, strategy_weights. Warm-start pattern replikovaný z autoloop.

6. **Auto-handoff chains** — skill-chains.json rozšířen o autoresearch PIVOT→deepresearch, autoresearch DONE→scribe, autoloop DONE→scribe.

## Prevention

Pravidelně kontroluj, že feedback smyčky skutečně fungují — spusť /discover a ověř, že bridged traces jsou viditelné. Sleduj graduation-candidates.md pro hromadění neprocesovaných kandidátů.

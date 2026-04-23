---
title: AnalysisBench — LLM Agents on Automated Software Analysis
category: concepts
tags: [software-analysis, benchmarking, agentic-swe, tools, evaluation]
sources: [arXiv:2604.11270]
updated: 2026-04-23
---

# AnalysisBench — LLM Agents on Automated Software Analysis

**Paper**: arXiv:2604.11270  
**Authors**: Islem Bouzenia, Cristian Cadar, Michael Pradel (April 2026)

## Core Claim

**"Agentic architecture matters more than LLM capability alone"** in software analysis automation. The right agent design outperforms weaker baselines even with the same underlying model.

## AnalysisBench

| Dimension | Value |
|-----------|-------|
| Tool-project pairs | 35 (7 tools × 5 projects each) |
| Languages | C/C++ and Java |
| Analysis tools | 7 diverse open-source tools |
| LLM backends tested | 4 (including Gemini-3-Flash) |

## AnalysisAgent Results

| Agent | Success Rate |
|-------|-------------|
| **AnalysisAgent (best)** | **94%** (33/35 with Gemini-3-Flash) |
| ExecutionAgent (baseline) | 77% |

Key tasks: automated tool installation, configuration, validation, environment setup, dependency resolution.

## Critical Finding: LLM Self-Validation Bias

> "LLM-self-validated success consistently overstates manually verified success"

Agents that evaluate their own success report higher rates than external verification confirms. This is a systemic bias across all tested architectures — not a specific model failure.

**Implication**: Never trust agent-reported success rates without independent verification.

## STOPA Relevance

1. **Agentic architecture > model**: validates STOPA's investment in skill design over model selection for specific tasks
2. **Self-validation bias**: directly relevant to STOPA's "never claim done without proof" principle (behavioral-genome.md §Verification). Agents saying "task complete" ≠ task complete — confirmed empirically.
3. **AnalysisBench pattern**: STOPA's `/harness` skill could benchmark against defined tool-project pairs in a similar structure

## Related Concepts

→ [swe-agents-survey.md](swe-agents-survey.md)  
→ [agentforge.md](agentforge.md)  
→ [agentic-engineering-patterns.md](agentic-engineering-patterns.md)  
→ [critical-step-optimization.md](critical-step-optimization.md)

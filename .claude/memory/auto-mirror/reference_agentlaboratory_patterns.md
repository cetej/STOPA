---
name: Agent Laboratory — Autonomous Research Pipeline Patterns
description: End-to-end research automation (arXiv search → experiment → LaTeX paper → NeurIPS-form review). Extractable patterns: weighted multi-dimensional scoring, multi-persona review, code-edit-execute-repair loop, history expiration.
type: reference
---

## Source
- Repo: https://github.com/SamuelSchmidgall/AgentLaboratory (5450 stars, MIT)
- arXiv: 2501.04227 (Jan 2025), AgentRxiv: 2503.18102 (Mar 2025)
- ~4,076 LOC Python, 9 files, 7 contributors

## Extractable Patterns

### 1. NeurIPS-Form Weighted Scoring
Structured JSON review with weighted dimensions instead of binary pass/fail:
```
overall (weight 1.0), soundness (0.3), contribution (0.4),
presentation (0.2), originality, significance, clarity
```
Each dimension scored 1-4 with text justification. Final score = weighted combination.
**Apply to**: `/peer-review`, `/critic` — replace qualitative "pass/fail" with dimensional scoring.

### 2. Multi-Persona Review (3 reviewers)
- Reviewer 1: harsh, focuses on experimental rigor
- Reviewer 2: harsh, focuses on impact and significance
- Reviewer 3: open-minded, focuses on novelty and potential

Each produces independent scores → aggregated.
**Apply to**: `/pr-review` already does multi-persona but could adopt the harsh/open spectrum.

### 3. Code-Edit-Execute-Repair Loop
```
LLM generates code → execute in subprocess (600s timeout)
→ failure? → code_repair() (2 attempts, error + traceback in prompt)
→ success? → LLM reflect() → improvement ideas → next iteration
→ best-of-N: keep sorted list by score, sample from top for next edit
```
**Apply to**: `/autoresearch` code iteration pattern.

### 4. History Expiration
Full paper/code text in agent context expires after N dialogue steps (replaced with summary marker). Simple context management without LLM compression.
**Apply to**: Long-running orchestration sessions — expire verbose tool outputs after N steps.

### 5. Section-by-Section Generation with Per-Section Tips
Hardcoded writing tips per paper section (intro tips differ from methods tips). Pragmatic prompt engineering.
**Apply to**: Any structured document generation skill.

## What NOT to Copy
- No persistent learning (each run from scratch)
- 130+ deps imported always (TensorFlow + PyTorch + diffusers regardless of need)
- No tests, no type hints, duplicated base classes
- Fixed pipeline (no flexible orchestration tiers)
- No novelty verification (just LLM opinion)
- `raise NotImplementedError` for parallel labs

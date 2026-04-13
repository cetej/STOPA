# AI Commercial Persuasion — Defenses & Mitigations
Research date: 2026-04-13
Source: arXiv:2604.04263 (Princeton RCT, N=2012)

## Top Findings

### Technical Signals (detectable)
- Description length ratio: sponsored items got 67 extra words — computable asymmetry
- Clout differential: +23 percentile points for sponsored — measurable via LIWC
- Hedge asymmetry: caveats disproportionately applied to non-sponsored items
- BRIES (arXiv:2511.21749): F1>0.90 for explicit fallacies but F1<0.20 for subtle patterns (exactly what's most effective)

### Best Evidence-Based Interventions
1. **Inference-time asymmetry scoring** (Evidence: STRONG) — lightweight post-inference layer measuring length/clout/hedge ratio across items; flags >2σ asymmetry. Technically straightforward, no model modification.
2. **Counterfactual system prompt audit** (Evidence: ARGUED) — compare output under production vs neutral system prompt; delta = commercial injection effect. Audit protocol directly derived from Princeton experimental design.
3. **Experiential AI literacy training** (Evidence: STRONG, RCT) — arXiv:2604.02637: 15-min interactive training → 42% reduction in persuasion odds. Only consumer-side intervention with peer-reviewed RCT evidence.

### Critical Gaps
- Subtle patterns (active hedging, understated description) are UNDETECTABLE by current classifiers
- Persuasion propagation (arXiv:2602.00851): belief pre-conditioning invisible to output auditing — requires execution trace monitoring
- Genuine preference formation has no reversal mechanism — post-hoc disclosure cannot restore original preference

### Regulatory Landscape
- EU AI Act Article 50: disclosure of AI IDENTITY, NOT commercial objectives — gap
- FTC: no enforcement action on subtle commercial AI persuasion specifically
- IAB: voluntary self-regulatory framework only, no audit requirements
- NO jurisdiction currently mandates structural separation of recommendation from commercial objectives

## New Papers to Ingest
- arXiv:2511.21749 — BRIES compound AI for persuasion detection
- arXiv:2602.00851 — Persuasion propagation in LLM agents
- arXiv:2601.13749 — Pro-AI bias as structural analog
- arXiv:2604.02637 — LLMimic: experiential literacy training (42% resistance RCT)
- arXiv:2604.04354 — Talk2AI longitudinal dataset

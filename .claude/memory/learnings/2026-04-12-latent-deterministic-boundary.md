---
date: 2026-04-12
type: best_practice
severity: high
component: skill
tags: [skill-design, architecture, agent-design, deterministic, latent-space]
summary: "Every step in an agent skill is either latent (model judgment: synthesis, interpretation, quality) or deterministic (code: queries, arithmetic, file ops). Confusing them is the most common design mistake. Skills should alternate: Latent → Deterministic → Latent → Deterministic → Latent."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
impact_score: 0.0
verify_check: "manual"
---

## Detail

Garry Tan's "Thin Harness, Fat Skills" identifies the latent/deterministic boundary as the most fundamental design decision in agent systems.

**Latent space** (model does this): judgment, synthesis, pattern recognition, interpretation, quality assessment  
**Deterministic** (code does this): database queries, arithmetic, file operations, API calls, combinatorial optimization

"Dinner table test": LLM can seat 8 people considering personalities. Ask it to seat 800 and it produces a hallucinated seating chart that *looks* plausible.

**Correct skill structure:**
1. LATENT: Interpret task, understand what's needed
2. DETERMINISTIC: Query data, retrieve documents, compute
3. LATENT: Synthesize results, apply judgment
4. DETERMINISTIC: Format output, write files
5. LATENT: Verify quality, decide if done

**STOPA application:** Review skill steps — any step asking the model to do arithmetic, combinatorial matching, or large-scale enumeration should be delegated to a Bash/Python tool call. Skills that push deterministic work into model reasoning produce unreliable outputs.

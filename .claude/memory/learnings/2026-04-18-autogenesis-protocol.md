---
date: 2026-04-18
type: architecture
severity: high
component: orchestration
tags: [self-evolution, protocol, versioning, rollback, agent-architecture, reflection-optimizer]
summary: "Autogenesis (arXiv:2604.15034) formalizuje self-evolving agent systém jako dvouvrstvý protokol: RSPL (5 pasivních resource typů: prompt/agent/tool/env/memory s explicit version+lifecycle) + SEPL (5 operátorů: Reflect ρ → Select σ → Improve ι → Evaluate ε → Commit κ). Klíčový princip: decouple what evolves from how evolution occurs. Empirie: GAIA Level 3 +33% absolutní (79→89% SOTA), AIME24 +71% na gpt-4.1, LeetCode C++ +17.9%. Headroom rule: slabé modely + těžké úlohy = největší gain. STOPA má všechny stavební bloky (outcomes, failures, replay-queue, maturity tiers, reflexion notes), chybí jen: per-resource version lineage, formální ρσιεκ mapping, explicit safety invariants na commit, dynamic tool generation."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
maturity: draft
valid_until:
skill_scope: [self-evolve, autoloop, autoresearch, evolve, orchestrate]
related: [2026-04-10-rlm-architectural-principles.md, 2026-04-13-experience-replay-outcomes-reuse.md, 2026-04-15-sd-zero-self-revision-supervision.md]
verify_check: "Glob('.claude/rules/sepl-operators.md') → 1+ matches"
model_gate:
impact_score: 0.0
task_context:
  task_class: research
  complexity: high
  tier: deep
---

## Paper core

**Title:** Autogenesis: A Self-Evolving Agent Protocol
**Author:** Wentao Zhang (NTU Singapore)
**ArXiv:** 2604.15034v1 (2026-04-16)

## Two-layer architecture

| Layer | Purpose | Content |
|-------|---------|---------|
| **RSPL** (Resource Substrate) | Defines *what* evolves | 5 entity types: Prompt, Agent, Tool, Environment, Memory. Each is `(name, desc, ϕ mapping, g trainable-flag, metadata)` + registration record `(entity, version, impl, params, contract)`. **Pasivní** — nemodifikují se samy. |
| **SEPL** (Self-Evolution) | Defines *how* evolution happens | 5 operators: Reflect ρ (traces → hypotheses) → Select σ (hypotheses → modification proposals) → Improve ι (apply via RSPL interface) → Evaluate ε (candidate → score+safety) → Commit κ (accept if score+safety, else rollback) |

## Algorithm 1 — SEPL loop

```
V₀ = VariableLifting(A)          # project resources to optimization manifold
Z₀ = Execute(A, V₀)              # initial trace
for t in 0..T-1:
    H_t = ρ(Z_t, V_t)            # semantic gradient / diagnosis
    D_t = σ(V_t, H_t)            # candidate modifications
    Ṽ_{t+1} = ι(V_t, D_t)        # apply via RSPL
    S_{t+1} = ε(Ṽ_{t+1}, G)      # evaluate
    V_{t+1} = κ(Ṽ_{t+1}, S_{t+1}) # commit OR rollback
    Z_{t+1} = Execute(A, V_{t+1})
    if Converged(S_{t+1}): break
```

## Infrastructure services (RSPL cross-cutting)

- **Model manager** — unified multi-provider API layer
- **Version manager** — auto-incremented semver per resource, immutable snapshots, rollback/branching/diff
- **Dynamic manager** — serialize/deserialize configs for hot-swap without restart
- **Tracer** — fine-grained execution traces for debugging + dataset synthesis

## Optimizers supported via SEPL interface

1. **Reflection** (default, natural language) — ρ prompts LLM for failure hypotheses, σ translates to string edits
2. **TextGrad** — natural language feedback as "textual gradient"
3. **GRPO / Reinforce++** — variables as policy, eval as reward, policy-gradient updates

## Empirical results

### GPQA-Diamond / AIME (prompt+solution evolution, no tools)
- gpt-4o: GPQA 48→58% (+21%), AIME24 13→17% (+25%)
- gpt-4.1: AIME24 23→40% (**+71%**), AIME25 20→33% (+67%)
- claude-sonnet-4.5: GPQA 78→81% (+4%), AIME24 77→87% (+13%)
- gemini-3-flash: GPQA 88→90% (+2.3%), AIME24 83→93% (+12%)
- **Finding**: combined prompt+solution > single strategy, ceiling effect on saturated benchmarks

### GAIA Test split (tool evolution, gemini-3-flash)
- vanilla 79.07% → **evolve tool 89.04% SOTA** (beats ToolOrchestra 87.38%)
- Level 3: 61.22 → **81.63% (+33.3 pp)** — largest relative gain in paper
- Tool generator: semantic search → if miss, synthesize + register as versioned RSPL resource

### LeetCode (solution evolution, 100 test problems, 5 languages)
- Kotlin +26.7%, C++ +17.9%, Java +16.7%, Go +15.9%, Python3 +10.1%
- Runtime ARB (beats human): C++ +30.8%, Java +24.4%
- Compile errors, RE, TLE frequently drop to zero after evolution

## Key principles

1. **Decoupling** — what evolves ≠ how it evolves. Resources are passive, operators are general.
2. **Safety & Auditability** — every mutation version-tracked and reversible.
3. **Formalism** — replace heuristic text modifications with typed operator algebra.
4. **Resources as first-class** — prompt/tool/memory externalized from agent logic; same agent ≠ same resources.
5. **Contract generation** — skills.md-style capability descriptors keep prompts stable and small.

## Gap analysis vs STOPA

| Autogenesis | STOPA state | Gap |
|-------------|-------------|-----|
| Per-resource version lineage | Git-level only | ❌ Add `version:` to skills + resource-ledger.jsonl |
| ρσιεκ operator formalism | Ad-hoc phases per skill | ⚠️ Formalize in shared rule |
| Safety invariants on commit | Critic gate, 3-revert stop | ⚠️ Explicit invariant list |
| Tool generator at runtime | Static skills only | ❌ Future: /tool-synth skill |
| Agent Bus (concurrent) | Sequential orchestrate | ✗ Don't adopt (CLI context) |
| RSPL 5-type unification | Specialized locations | ✗ Don't adopt (massive refactor) |
| Reflection optimizer | Reflexion notes exist | ✅ Already have |
| Replay / outcomes | outcomes/, failures/, replay-queue | ✅ Have more than paper |
| Maturity tiers | draft→validated→core | ✅ STOPA-specific extension |

## Adoption priorities (this learning triggered R1-R4 implementation, 2026-04-18)

- **R2** (this session): `.claude/rules/sepl-operators.md` — formalize ρσιεκ mapping for iterative skills
- **R4** (this session): extend self-evolve Critic gate with explicit invariants
- **R1** (this session): version field + resource-ledger.jsonl for skills
- **R3** (future): /tool-synth dynamic skill generator, gated by maturity

## Sources

- Full text extracted to `.claude/memory/intermediate/autogenesis-paper.txt` (97 KB, 24 pages)
- PDF cached: `C:\Users\stock\.claude\projects\...\webfetch-*.pdf`

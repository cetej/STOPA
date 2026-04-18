---
date: 2026-04-18
type: best_practice
severity: high
component: orchestration
tags: [opus, effort, model, claude-code, token-efficiency, thinking]
summary: "Opus 4.7 v Claude Code: default effort=xhigh (doporučeno), max=diminishing returns + overthinking. Adaptivní thinking (per-step, ne fixed budget). Každý user turn přidává reasoning overhead — specifikuj celý task v prvním turnu, ne postupně. Chovej se k modelu jako k delegovanému inženýrovi, ne pair programmerovi."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
valid_until:
model_gate: "opus-4-7"
skill_scope: [orchestrate, checkpoint, status]
related: []
verify_check: "manual"
impact_score: 0.0
task_context:
  task_class: research
  complexity: low
  tier: light
---

## Detail

Zdroj: Anthropic official blog (2026), Best Practices for Claude Opus 4.7 with Claude Code.

### Effort level guidance

| Effort | Chování | Kdy použít |
|--------|---------|-----------|
| `xhigh` | Výchozí, balancuje autonomii a inteligenci | Většina coding + agentic tasks (DEFAULT) |
| `max` | Diminishing returns, sklony k overthinking | Neppoužívat jako default; jen pro explicit request |

### Adaptive thinking
- Opus 4.7 nemá fixed thinking budget — thinking je optional per step
- Uživatel může promptovat pro více/méně thinking dle potřeby
- Méně sklon k overthinking než předchozí verze

### Token efficiency
- Každý user turn = reasoning overhead
- Pravidlo: specifikuj kompletní task v turnu 1, ne iterativně
- Plný kontext upfront > postupné odhalování požadavků
- Auto mode (Claude Code Max) vhodný pro long-running tasks bez frequent check-ins

### Behavioral changes vs. prior Opus
- Response length automaticky odpovídá komplexitě tasku
- Méně tool usage, více reasoning
- Konzervativnější spawning sub-agentů

**STOPA implikace**: Při volbě modelu pro orchestrate tasky — nastavit effort=xhigh, ne max. Behaviorální genome zmínka "batch operace > jednotlivé kroky" je potvrzena (each user turn = overhead).

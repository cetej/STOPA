---
date: 2026-04-08
type: architecture
severity: medium
component: orchestration
tags: [multi-agent, monitoring, reflection, farm-tier, self-evolve]
summary: "Heartbeat-triggered intervention: orchestrátor posílá prompt-injections do běžících agentů (reflection, skill consolidation, direction change) bez jejich restartu — non-destructive mid-run steering. Odlišné od kritika: critic hodnotí output, heartbeat mění direction."
source: external_research
uses: 13
harmful_uses: 0
confidence: 1.00
maturity: core
graduated_to: critical-patterns-10
successful_uses: 1
verify_check: "Grep('stagnation-detector', path='.claude/settings.json') → 1+ matches"
related: [2026-04-08-shared-public-state-agent-coordination.md]
task_context: {task_class: research, complexity: medium, tier: standard}
---

## Heartbeat-Triggered Mid-Run Steering

CORAL (arXiv:2604.01658) zavádí heartbeat mechanismus pro orchestrátor:

**Mechanismus:**
- Manager process posílá "heartbeat prompts" do aktivně běžících agentů
- Typy akcí: reflection (zastav a zanalyzuj co jsi zjistil), skill consolidation (extrahuj reusable patterns do shared state), direction change (přeorientuj se na jiný approach)
- Agent pokračuje dál po obdržení heartbeatu — není to restart ani kill

**Odlišení od existujících STOPA mechanismů:**
| Mechanismus | Kdy se spouští | Co dělá |
|-------------|---------------|---------|
| Critic | Po dokončení kroku | Hodnotí output quality |
| Heartbeat | Periodicky za běhu | Mění direction/reflection bez výstupní evaluace |
| Calm-steering | Na panic signal | Přerušuje desperation pattern |

**Relevance pro STOPA:**
`self-evolve` a `autoloop` aktuálně nemají mid-run steering — jen post-iteration critic. Heartbeat pattern by umožnil orchestrátoru zastavit neproduktivní exploration větev dříve než na konci iterace.

**Jak aplikovat:**
V `self-evolve` Phase 2: po každých N iteracích bez zlepšení, inject reflection prompt před dalším pokusem. Efektivnější než čekat na critic fail po celé iteraci.

---
date: 2026-04-26
type: best_practice
severity: medium
component: skill
tags: [autoreason, model-selection, self-refinement, debate-loop, cost-optimization]
summary: "AutoReason A/B/AB triáda + blind judges nese gain především strukturou, ne velikostí modelu. Haiku 3.5 dosáhl 42/42 s tímto loopem; standard self-refinement na stejném modelu degraduje výstup pod nulový baseline. Mid-tier recovery rate ~62 % vs ~43 % pro frontier-only. Investice do víc rounds/judges > upgrade writerů na Opus."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
maturity: draft
verify_check: "Grep('Mid-tier sweet spot', path='.claude/skills/autoreason/SKILL.md') → 1+ matches"
related: [2026-04-01-autoreason-adversarial-debate.md, 2026-03-29-claudini-autoresearch-loop.md, karpathy-loop-autoloop.md]
skill_scope: [autoreason]
task_context: {task_class: research, complexity: low, tier: light}
---

## AutoReason — Mid-Tier Sweet Spot

NousResearch AutoReason 2026 (paper popsaný uživatelem 2026-04-26):

**Empirická čísla z paperu:**
- Haiku 3.5 + AutoReason loop → 42/42 perfect score
- Standard self-refinement na stejném modelu → degraduje pod 0-iter baseline
- Naive loop bez A baseline shrinkl jeden pitch z 345 na 102 slov (model maže vlastní práci, aby splnil critique prompt)
- Mid-tier recovery rate ~62 % vs ~43 % frontier-only baselines
- 10× levnější model dosahuje frontier-level outputu *pouze přes strukturu* (A/B/AB + blind judges + Borda + incumbent-stop)

**Co to znamená pro STOPA:**
- Stávající `model: sonnet` v `autoreason/SKILL.md` je rozumný default — **nevylepšuj writery na Opus**, gain odsud nepřijde
- Pokud má uživatel rozpočet — invest do `judges: 7` nebo `rounds: 5`, ne do silnějšího modelu na writers
- Skill už implementuje strukturální safeguardy (k_consecutive ≥ 2 stop, A vždy v Borda panelu) — neoslabovat je „pro rychlost"

**Co NEDĚLAT:**
- Vypnout A z Borda panelu „protože syntéza je vždycky lepší" — bez A loop monotónně mažou text
- Upgradovat writery na Opus s předpokladem že větší model = lepší výsledek — empiricky neplatí pro tuto strukturu
- Spouštět autoreason na <100-word textech — nemá co debatovat (skill už blokuje, ale připomínka)

**Aplikace:**
Při budget plánování pro `/autoreason`: prioritizuj `judges` parametr nad upgradem modelu. Default 5 judges + Sonnet writers + Haiku judges je cost-optimal sweet spot.

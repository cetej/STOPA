---
date: 2026-04-30
type: best_practice
severity: medium
component: skill
tags: [council, persona, multi-agent, prompt-engineering]
summary: Fincept Terminal používá 37 personas (Trader/Economic/Geopolitics) jako JSON configs s společnou base_agent runtime. Pattern persona-as-config (ne persona-as-code) = aplikovatelné na /council expansion — přidat personu = přidat JSON entry, ne code change.
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.6
maturity: draft
skill_scope: [council, brainstorm]
verify_check: "Glob('.claude/skills/council/personas/*.json') → 0+ matches (pattern reference, not enforcement)"
---

## Pattern abstrakce — persona-as-config

**Source**: [Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) — AGPL-3.0 (study only, no code copy).

**Co Fincept dělá**:
- 37 personas v 3 JSON souborech (`fincept-qt/scripts/agents/{Trader,Economic,Geopolitics}/configs/agent_definitions.json`)
- Společný `base_agent.py` runtime, persony se liší **pouze** v `instructions` field + few extensions
- Centralizovaný `agent_manager.py` registruje by ID a routuje queries
- Každá persona má structured config: `id, name, description, category, capabilities[], config{model, instructions, tools, memory, output_format}`
- Trader extensions: `output_schema, scoring_weights, data_sources, knowledge_base, analysis_rules, thresholds`
- Geopolitics extensions: `book_source` (Marshall/Brzezinski/Kissinger framework citation)

**Klíčový insight**: Persona-as-config umožňuje:
- Přidat 38. personu = JSON entry, ne code change → marginal cost téměř nulový
- A/B test personas přepínáním config bez deploye
- Eval harness může grep config files a generovat test cases

## Aplikace na STOPA

### /council skill (currently 6 perspectives)
[`.claude/skills/council/SKILL.md`](../../skills/council/SKILL.md) má teď 6 council perspectives jako inline prompts. Pattern by zlepšil:

1. **Extract personas → JSON**: `.claude/skills/council/personas/*.json` (např. `engineer.json`, `pm.json`, `security.json`, `user.json`, `data.json`, `legal.json`)
2. **Schema** (analogicky Fincept):
   ```yaml
   id: engineer
   name: Engineering Lead
   role_brief: "Implementation feasibility, complexity, debt"
   framework_source: "(optional) e.g., 'Pragmatic Programmer'"
   instructions: <persona system prompt>
   output_schema:
     - feasibility_score: 1-5
     - risk_factors: array
     - recommendation: enum
   capabilities: [code_review, arch_design, complexity_estimate]
   ```
3. **Runtime**: `/council` skill body čte persona JSONs, pro každou pošle query s persona instructions, agreguje strukturované výstupy.

**Marginal benefit**: Přidat novou perspectivu (např. "Operations Lead", "Customer Support", "Compliance") = JSON entry. Currently SKILL.md edit s rebalanced length.

### /brainstorm skill
Pattern aplikovatelný i tam — přidat `personas/` se simulací různých stakeholderů (marketing, sales, eng, ops). Brainstorm by mohl spustit ideation 4-5 personami paralelně místo single voice.

### Anti-pattern (čeho se vyhnout)
- **Persona inflation**: Fincept má 37 (specialised market intelligence). STOPA by NEMĚL mít 30+ council personas — ztratí se signál. Cap na 8-12.
- **Generic personas**: Bez framework_source/role_brief vznikne 6× "smart helpful assistant". Persona musí mít specifický perspective lock-in (incentive structure, training, blind spots).
- **No synthesis step**: 6 personas = 6 different opinions. Bez synthesizera dostane uživatel "engineer says A, PM says B" — useless. Fincept hedge fund team_config naznačuje team-level synthesis. STOPA `/council` by měl mít explicit synthesis stage.

## AGPL-3.0 caveat

**Bezpečné** (provedeno v této extrakci):
- Číst veřejně dostupné JSON struktury, extrahovat **schema keys** a **persona names**.
- Popsat **pattern abstraction** (persona-as-config, central dispatcher, output schema enforcement).
- Citovat **architectural choices** s URL.

**Zakázané** (nedělali jsme):
- Kopírovat literal `instructions` field content.
- Importovat Fincept Python kód do STOPA.
- Reverse-engineerovat AGPL-3.0 binaries.

**Boundary check**: Tento learning + 2 sister reference files (POLYBOT, ORAKULUM) obsahují **pattern descriptions, schema field names a persona identifiers** (Buffett, Graham, etc. = veřejně známá jména). Žádný proprietary prompt content.

## Reference
- Fincept repo: https://github.com/Fincept-Corporation/FinceptTerminal
- Sister docs:
  - `~/Documents/000_NGM/POLYBOT/.claude/memory/fincept-personas-reference.md`
  - `~/Documents/000_NGM/ORAKULUM/.claude/memory/fincept-connectors-reference.md`
- STOPA radar: `.claude/memory/radar.md` line 135
- Pattern source: `fincept-qt/scripts/agents/{Trader,Economic,Geopolitics}/configs/agent_definitions.json` + `agent_manager.py` + `base_agent.py`

---
date: 2026-04-01
type: bug_fix
severity: critical
component: pipeline
tags: [anthropic-api, thinking, effort, sonnet-46, text-reproduction, breaking-change]
summary: "Sonnet 4.6 s thinking:disabled agresivně sumarizuje dlouhý text (~40% výstupu). S thinking:adaptive leakuje chain-of-thought a XML tool markup do outputu. Effort 'low' zhoršuje oba problémy. Fix: buď effort 'medium'+adaptive, nebo PATCH formát místo reprodukce."
source: user_correction
confidence: 1.00
uses: 2
harmful_uses: 0
model_gate: "sonnet-4.6"
verify_check: "manual"
successful_uses: 0
---

## Problém

Anthropic změnil chování Sonnet 4.6 (pravděpodobně Q1 2026 update):

### Varianta A: thinking: disabled
- Model **agresivně sumarizuje** místo reprodukce celého textu
- Výstup je ~37-43% očekávané délky
- Reprodukovatelné — opakované pokusy dávají stejný výsledek
- Postihuje fáze, kde model má reprodukovat/upravit dlouhý text (překlad, kontrola úplnosti)

### Varianta B: thinking: adaptive + effort: low
- Model rozhodne, že thinking blok nepotřebuje
- Chain-of-thought reasoning (počítání znaků, interní monolog) **leakuje přímo do output streamu**
- XML markup z tool callů (`<function_calls>`, `<invoke>`) se zapisuje do výstupu
- Leaked artefakty nafouknou text → kaskádové selhání dalších fází (fragment detection počítá z nafouklého vstupu)

### Kořenová příčina
- `budget_tokens` deprecated → nahrazeno `thinking: adaptive` + `output_config: {effort: "..."}`
- `effort` ovlivňuje nejen thinking ale i tool use chování a output pečlivost
- `effort: "low"` = model šetří → sumarizuje, neodděluje reasoning od výstupu

## Řešení (ověřená v NG-ROBOT)

1. **Pro text-reprodukční fáze:** PATCH formát místo plné reprodukce — model vrací jen diff/opravy, aplikace programaticky
2. **Strip post-processing:** Regex na `<antml*>`, `<thinking>`, `<antThinking>` tagy ve výstupu všech fází
3. **Effort medium** pro fáze vyžadující reasoning (term verification, fact checking)
4. **thinking: disabled** pro fáze vyžadující čistý textový výstup (s PATCH formátem kde je potřeba úprav)

## Dopady na další projekty

Jakýkoli pipeline kde Claude reprodukuje/překládá/edituje dlouhý text (>10K znaků) je ohrožen:
- Překlad článků
- Kontrola úplnosti
- Stylizace textu
- Jakákoli fáze "uprav a vrať celý text"

**Architektonický vzor:** Preferuj PATCH/diff formát nad plnou reprodukcí textu. Model je spolehlivější v generování krátkých cílených oprav než v reprodukci celého dokumentu.

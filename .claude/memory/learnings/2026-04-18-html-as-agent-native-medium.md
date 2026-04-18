---
date: 2026-04-18
type: best_practice
severity: medium
component: skill
tags: [agent-native, skill-design, tooling, html, media, video]
summary: "HeyGen HyperFrames validuje princip: nástroje pro agenty by měly používat jazyk z jejich training dat (HTML > After Effects DSL, markdown > proprietary XML). Agenti byli trénováni na miliardách HTML stránek — psát v HTML je jejich rodný jazyk. Thin layer (pár data-* atributů) nad standardní HTML/CSS/JS = agent-native video toolchain. Generalizuje mimo video: preferuj markup/kód, který agent už zná, nepiš DSL pro GUI."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.75
maturity: draft
valid_until:
skill_scope: [klip, nano, skill-generator]
related: [2026-04-12-purpose-built-tools-75x-faster.md]
verify_check: "manual"
model_gate:
impact_score: 0.0
task_context:
  task_class: research
  complexity: low
  tier: light
---

## Detail

### Princip
Agenti jsou trénováni na webu — HTML, CSS, JS, GSAP, SVG, Canvas jsou jejich rodný jazyk. Nástroje postavené na JSON/XML timelines (After Effects, DaVinci) nebo proprietárních DSL jsou designované pro lidi, ne pro LLM.

### Důkaz (HyperFrames, HeyGen 2026-04-18)
- Kompletní 5sekundový dvouscénový video composition v <70 řádcích HTML
- Pouze 4 data-attributes přidané nad standardní HTML: `data-composition-id`, `data-start`, `data-duration`, `data-track-index`
- Any browser-compatible technology works: GSAP, Lottie, Three.js, D3, CSS animations
- Distribuováno jako Claude Code skill (`npx skills add heygen-com/hyperframes`)

### Generalizace pro STOPA skills
| Doména | Agent-native formát | Anti-pattern |
|--------|---------------------|--------------|
| Video | HTML + CSS + JS | After Effects XML, Premiere project files |
| Dokumenty | Markdown | Proprietary docx XML, LaTeX (pro většinu case'ů) |
| Config | YAML/JSON minimal, Python literals | Complex DSL, GUI-first config |
| Vizualizace | SVG, HTML Canvas, D3 | PowerPoint XML, proprietary chart APIs |
| Struktura | File tree + markdown | Graph DB schemas, RDF |

### STOPA aplikace
- `/klip` (Kling text-to-video) vs HyperFrames (HTML code-to-video): obě jsou agent-friendly, doplňkové
- Nové skills: preferuj text-based input s thin formatting layer před binary/GUI tools
- Platí i pro skill bodies: markdown s embedded Python/Bash > exotické DSL
- Souvisí s garry-tan-thin-harness-fat-skills pattern (thin harness over rich agent-native substrate)

# Knowledge Base Health Report
> Generated: 2026-04-07 | Score: 7.5/10

## Inventar

- **Learnings:** 51 total (51 aktivnich, 0 archivovanych v learnings/)
- **Wiki clanky:** 8 articles, last compiled 2026-04-04
- **Critical patterns:** 10/10 slotu obsazeno (plny)
- **Pokryti komponent:** 5/7 komponenty maji wiki clanek (71%)
  - Pokryto: skill, orchestration, memory, general, pipeline+workflow
  - Chybi: `hook` (1 learning, bez wiki), `workflow` (1 learning, slouci s pipeline)
- **Nezkompilovano:** 6 novych learnings od posledniho /compile (2026-04-04 az 2026-04-07)

## Cerstvost

- **Stale (>90 dni):** zadne — nejstarsi learning je 2026-03-23 (15 dni)
- **Decaying (confidence <0.4):** zadne — nejnizsi confidence = 0.5 (3 GAP-learnings)
- **Nepouzite (uses=0, >60 dni):** zadne — vsechny learnings jsou novejsi nez 60 dni
- **Bloated (>50 radku):** 10 souboru
  - `2026-03-29-bigmas-directed-graph-orchestration.md` (72 radku)
  - `2026-03-27-playwright-mcp-download-hijack.md` (67 radku)
  - `2026-04-05-agent-defense-frameworks.md` (69 radku)
  - `2026-04-05-egoalpha-prompt-patterns.md` (61 radku)
  - `2026-04-05-regression-gate-pattern.md` (61 radku)
  - `2026-03-26-channels-24x7-architecture.md` (58 radku)
  - `2026-03-29-memcollab-agent-agnostic-memory.md` (53 radku)
  - `2026-03-29-paged-context-protocol.md` (55 radku)
  - `2026-04-01-sonnet46-thinking-effort-breaking-change.md` (53 radku)
  - `2026-04-03-description-optimizer-plan.md` (53 radku)

## Konzistence

- **Konflikty (1 soft, 1 open):**
  1. **Harness: simplifikace vs determinismus** (open z wiki INDEX)
     - `2026-03-26-harness-simplification.md`: "Simplify harnesses — remove unnecessary scaffolding, trust model"
     - `critical-patterns.md #4`: "Harness = deterministic (~99.9%). Use for repeatable multi-step."
     - Posouzeni: kontext-zavisly (simplifikace = pouzivej mene dekoraci; determinismus = pouzivej harness na spravnych mistech). Nejde o skutecny konflikt, ale ctenari to muze splitovat.
  2. **Self-organizing vs centralized orchestration** (novy, od 2026-04-06)
     - `2026-04-06-self-organizing-agents-ab-test.md`: self-org agenti bez roli +8% na explorativnich ulohach
     - `2026-04-02-distributed-systems-amdahl-gate.md`: centralized > decentralized (1.36× vs 0.88×)
     - Posouzeni: task-type dependent — explorativni vs serialni. Potrebuje explicatni kontextovaci poznamku v orchestration wiki.

## Mezery

1. **[PRIORITY: HIGH] Wiki compile zaostava** — 6 novych learnings (2026-04-04 az 2026-04-07) neni v zadnem wiki clanku. Temata bez pokryti: agent defense frameworks, BM25 search, egoalpha prompt patterns, regression gate, self-improving harness, OSfT self-sharpening, self-organizing agents A/B test, neuro-symbolic orchestration.
2. **[PRIORITY: MEDIUM] Hook komponenta bez wiki** — `2026-04-03-disable-skill-shell-audit.md` je jediny learning s `component: hook` a nema odpovidajici wiki clanek. Tema je dusite (disableSkillShellExecution, 52% STOPA skills zasazeno).
3. **[PRIORITY: MEDIUM] Critical patterns jsou plne (10/10)** — dalsi graduation neni mozna bez vyrazeni nejslabiho zaznamu. Kandidati na vyrazeni nebo slouceni: #7 (Tool Descriptions) a #6 (Analysis-Paralysis Guard) jsou genericky a mohly by byt lepe zachyceny v orchestration wiki.
4. **[PRIORITY: LOW] 140 singleton tagu** — 140 z celkovych tagu se vyskytuje jen v jednom souboru. Signalizuje zrnitost tagu, ktera zpomaluje retrieval. Konsolidace pri pristim /compile.
5. **[PRIORITY: LOW] Orchestration je nejvetsi komponenta bez subdivize** — 23 learnings, wiki pokryvaji jen 3 clanky. Novi learnings (self-org, NSM, self-improving harness) posouvajiorchestraci smerem k nove subteme "adaptive orchestration."

## Auto-fix

Opraveno **49 souboru** — pridana chybejici YAML pole:

- **`confidence: 0.7`** pridano 17 souborum (vsechny starsi learnings bez confidence)
- **`uses: 0`** pridano 17 souborum
- **`successful_uses: 0`** pridano 49 souborum (pole `successful_uses` chybelo ve vsech souborech krome 2)
- **`harmful_uses: 0`** pridano 17 souborum

Zbyvajici 2 soubory mely vsechna pole uz spravne:
- `2026-04-06-self-organizing-agents-ab-test.md`
- `2026-04-07-nsm-neuro-symbolic-orchestration.md`

## Doporuceni

1. **Spustit `/compile`** — 6 novych learnings ceka na syntezi do wiki. Prioritni temata: agent defense + orchestration patterns (self-org + NSM mohou tvorit novy clanek "adaptive-orchestration").
2. **Vyresit soft contradiction #2** — pridat kontextovaci poznamku do `orchestration-multi-agent.md`: kdy pouzit self-org (explorativni) vs centralized (serialni s Amdahl gate <0.4).
3. **Uvazovat o hook wiki clanku** — i jeden learning o `disableSkillShellExecution` ma prakticke dopady na 52% skills. Kratky clanek nebo sekce v skill-design.
4. **Uvolnit misto v critical-patterns** — sloucit nebo presunut #6 (Analysis-Paralysis Guard) a #7 (Tool Descriptions) do wiki, aby bylo misto pro nove high-impact learnings.
5. **Zkratit bloated soubory** — 10 souboru prekracuje 50 radku. Nejhorsi kandidati (`bigmas` 72r, `playwright-mcp` 67r, `agent-defense` 69r) mohou byt zkraceny odstranim prikladovych bloku do wiki a ponechanim jen frontmatter + klic. poucky.

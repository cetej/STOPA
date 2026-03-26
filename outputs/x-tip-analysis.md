# X-TIP Analýza: Claude Code tipy z X.com (2026-03-25/26)

## Zdroje

6 příspěvků z X.com skupiny karet "X-TIP", extrahováno 2026-03-26 přes dev-browser.

---

## 1. Jian Wang — 16 klíčových CC příkazů

**Obsah:** Seznam 16 příkazů pro 80% hodnoty Claude Code.

**Co z toho máme / nemáme v STOPA:**

| Příkaz | Máme? | Poznámka |
|---|---|---|
| /init (CLAUDE.md) | Ano | Náš systém je na tom postavený |
| /plan | Ano | EnterPlanMode |
| /context | Ne | Vestavěný CC příkaz, nelze replikovat skillem |
| /compact | **Ano** | Máme vlastní `/compact` skill s Haiku |
| /clear | Ne | Vestavěný CC příkaz |
| /model | Ne | Vestavěný CC příkaz |
| /btw | Ne | Vestavěný CC příkaz — side questions |
| /rewind | Ne | Vestavěný CC příkaz — undo |
| /agents | Ne | Vestavěný — ale my spouštíme agenty proaktivně |
| /chrome | Ne | Vestavěný — my máme Claude in Chrome MCP + dev-browser |
| /loop | **Ano** | Máme `/loop` skill |
| /simplify | **Ano** | Máme `/simplify` skill |
| /permissions | Ne | Vestavěný |
| --dangerously-skip-permissions | Ne | Bezpečnostní risk — máme auto mode místo toho |
| Shift+Tab | Ne | Vestavěný |
| "ultra think" | **?** | Extended thinking — ověřit zda to funguje jako prompt |

**Akční bod:** Ověřit, zda "ultra think" prompt skutečně aktivuje hlubší reasoning v Claude Code, nebo je to jen mýtus z X.com.

---

## 2. Sawyer Hood — dev-browser CLI

**Obsah:** Představení dev-browseru. Klíčový insight z reply thread:
- "Rather than inventing a new syntax for browser automation, just use Playwright"
- Srovnání s agent-browser od Vercel — dev-browser je rychlejší díky QuickJS sandboxu

**Status:** ✅ Již nainstalováno a otestováno v této session. Memory zapsáno.

---

## 3. 0xMarioNawfal — "Claude Code open sourced AI engineering system"

**Obsah:** Hype post o repozitáři s 28 agenty, 116 skills, 59 příkazy. Odkazuje na "ECC Tools".

**Analýza:** Vypadá jako open-source harness podobný tomu co my budujeme v STOPA. Klíčové komentáře:
- "the hooks + security scanner part is underrated" — DragAI
- "security scanner part is lowkey the most interesting" — HumanAds
- "shared state conflicts when 30 agents are writing to same codebase" — Brian Johnson (relevantní problém)

**Akční bod:** Prozkoumat ECC Tools repo — porovnat architekturu s STOPA, hledat:
- Jak řeší git merge konflikty při parallel agents
- Jaké security scanning přístupy používají
- Zda mají skills které nám chybí

---

## 4. Anthropic — Claude Code Auto Mode (Engineering Blog)

**Obsah:** Oficiální blog post o auto mode. Klíčové body z komentářů:
- Classifier nevidí agent reasoning → nemůže craftnout argumenty pro bypass safety
- "safer middle ground" mezi full permissions a constant prompting

**Relevance pro STOPA:**
- Auto mode je přesně co náš uživatel chtěl (viz memory: feedback_approval_fatigue.md)
- Blog post na anthropic.com/engineering/claude-code-auto-mode — přečíst detailně

**Akční bod:** Přečíst celý blog post, zvážit zapnutí auto mode pro STOPA development. Porovnat s naším současným permissions setup v settings.json.

---

## 5. Sukh Sroay — Microsoft MarkItDown

**Obsah:** Microsoft open-source tool pro konverzi souborů do Markdown. 87K stars.

**Podporované formáty:** PDF, PowerPoint, Word, Excel, Images (OCR), Audio (transcription), YouTube URLs, HTML, CSV, JSON, XML, EPUB, ZIP.

**Relevance pro STOPA/NG-ROBOT:**
- MCP server pro Claude Desktop integration — máme ho?
- Mohl by vylepšit naše zpracování DOCX/PDF v NG-ROBOT pipeline
- Alternativa k našemu `/pdf` a `/docx` skillu pro extrakci textu

**Kritický komentář (danfiru):** "Frontier models already ingest natively... this is adding a lossy translation layer" — validní point, Claude umí PDF/images nativně.

**Akční bod:** Ověřit zda MarkItDown MCP server přidá hodnotu k tomu co už máme. Hlavní use case: batch konverze souborů v pipeline (ne single-file kde Claude čte nativně).

---

## 6. GitHub Projects — oh-my-claudecode (30+ agentů)

**Obsah:** Open-source systém s 30+ agenty pro Claude Code, parallel execution, orchestrace.

**Relevance:** Přímý konkurent/inspirace pro STOPA. Z komentářů:
- Git merge konflikty s parallel agents — stejný problém který řešíme
- "You don't prompt anymore. You orchestrate." — přesně naše filozofie

**Akční bod:** Prozkoumat oh-my-claudecode repo, porovnat s STOPA:
- Architektura agentů vs. naše skills
- Jak řeší paralelismus
- Jaké workflow patterns používají

---

## Prioritizovaná zadání pro další session

### P1: Prozkoumat konkurenční systémy (ECC Tools + oh-my-claudecode)
```
Prozkoumej dva open-source Claude Code orchestrační systémy a porovnej je s STOPA:

1. ECC Tools (28 agentů, 116 skills) — najdi repo, analyzuj:
   - Architektura: jak organizují skills vs agents
   - Security scanner: jak funguje, co kontroluje
   - Hooks: jaké hooks mají a k čemu
   - Merge conflict řešení při parallel agents

2. oh-my-claudecode (30+ agentů) — najdi repo, analyzuj:
   - Jak řeší parallel execution
   - Workflow patterns
   - Orchestrace: centrální vs distribuovaná

Výstup: tabulka srovnání s STOPA, seznam konkrétních věcí které bychom mohli adoptovat.
```

### P2: Anthropic Auto Mode — evaluace pro STOPA
```
Přečti blog post na anthropic.com/engineering/claude-code-auto-mode

Zjisti:
- Jak funguje classifier (jaké akce povoluje/blokuje)
- Rizika vs. výhody oproti --dangerously-skip-permissions
- Jak to nastavit v settings.json
- Zda to řeší naše approval fatigue (viz memory feedback_approval_fatigue.md)

Výstup: doporučení zda zapnout auto mode pro STOPA development.
```

### P3: MarkItDown — evaluace pro NG-ROBOT pipeline
```
Otestuj Microsoft MarkItDown (github.com/microsoft/markitdown):

1. Nainstaluj: pip install markitdown
2. Otestuj na vzorových souborech z NG-ROBOT pipeline (DOCX články, PDF podklady)
3. Porovnej výstup s naším současným DOCX/PDF zpracováním
4. Zjisti zda MCP server přidá hodnotu k Claude Desktop workflow

Výstup: rozhodnutí zda integrovat do NG-ROBOT pipeline.
```

### P4: "ultra think" — ověření
```
Ověř zda prompt "ultra think" skutečně aktivuje hlubší reasoning v Claude Code,
nebo je to jen X.com mýtus. Otestuj na konkrétním příkladu s měřitelným výstupem.
```

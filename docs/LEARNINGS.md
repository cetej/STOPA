# LEARNINGS — Projekt STOPA

Poučení z práce, externích zdrojů a analýz. Řazeno od nejnovějšího.

---

## 2026-03-22 — Harness Engineering & Claude Certified Architect (video analýza)

### Zdroj
- Video 1: "Harness Engineering for AI Agents" (YouTube I2K81s0OQto)
- Video 2: "Claude Certified Architect — Full Exam Guide" (YouTube vizgFWixquE)

### Klíčová poučení

#### 1. March of Nines — proč skills samy nestačí
- 10-krokový workflow s 90% úspěšností/krok = 65% celková úspěšnost = 6+ selhání/den
- S 99%/krok = 1 selhání/den. S 99.9% = 1 za 10 dní.
- SkillsBench (84 skills, všechny modely): skills zlepšují pass rate, ale ne dost pro bezobslužný provoz
- **Závěr**: Skills = "best effort" prompty. Pro produkční spolehlivost potřebujeme deterministické koleje (harness).

#### 2. Harness Engineering — 12 principů
1. **Architektura** (supervisor, DAG, multi-agent, hierarchický)
2. **Plánování** (fixní fáze vs dynamický plán — fixní pro opakované procesy)
3. **Virtuální souborový systém** (scratch pad pro mezivýsledky)
4. **Delegování** (sub-agenti s izolovaným kontextem)
5. **Tool calling + guardrails** (max 4-5 tools/agent, forced first move)
6. **Paměť** (krátkodobá = MD, dlouhodobá = knowledge graph)
7. **Stavový automat** (fáze + tracking v DB/souboru)
8. **Code execution v sandboxu**
9. **Context management** (kompakce, sumarizace, pinning klíčových faktů)
10. **Human in the loop** (touch points, ne blokace)
11. **Validační smyčky** (test → fail → iterate, ale vědět kdy přestat)
12. **Agent skills** pro rozšiřitelnost mimo fixní kroky

#### 3. Stripe příklad — harness v praxi
- Scaffold kolem Claude Code + 3M testů = 1300 PR/týden automaticky
- Klíč: negenerují testy promptem, ale vynucují je v Python procesu

#### 4. Prompts vs Hooks (zákon vs návrh)
- **Prompt** = suggestion (90% dodržení). Vhodné pro: styl, tón, formát
- **Hook** = law (100% vynucení). Vhodné pro: finance, bezpečnost, compliance
- Anti-pattern: snažit se "vyladit prompt k dokonalosti" na úkolech vyžadujících 100% spolehlivost

#### 5. Tool descriptions jsou nejvyšší páka
- Ambiguní popisy = častý mis-routing (agent volá špatný tool)
- Nejlepší praxe: popsat KDY použít **A KDY NEpoužít**
- Max 4-5 tools na agenta — méně volba = lepší rozhodování

#### 6. CLAUDE.md 3 vrstvy
- **User level** (~/.claude/CLAUDE.md): osobní preference
- **Project level** (repo/CLAUDE.md): týmové konvence
- **Path-specific** (.claude/rules/*.md): pravidla jen pro konkrétní cesty
- Anti-pattern: dump všeho do jednoho CLAUDE.md → plýtvání tokeny při každé session

#### 7. Few-shot > instrukce
- 2-3 reálné příklady požadovaného výstupu > celá stránka instrukcí
- Claude se učí vzor (pattern), ne jen formát

#### 8. Separate session pro review
- Agent, který kód napsal, je zaujatý → vždy reviewovat v nové session
- "Fresh eyes catch more" — platí i pro AI

#### 9. Lost in the middle
- Claude čte dobře začátek (40%) a konec. Střed = fuzzy zone
- Každý tool output posunuje důležité info hlouběji do fuzzy zóny
- Fix: pin klíčová fakta nahoru, trimovat verbose tool outputs, delegovat na sub-agenty

#### 10. Graceful failure > generic error
- Nikdy "Error occurred" → vždy: co se stalo, co se zkoušelo, co částečně funguje, co dalšího zkusit
- Main agent pak může inteligentně rozhodnout (retry, switch source, note gap)

### Relevance pro STOPA
- STOPA /orchestrate UŽ implementuje: sub-agenty, budget tiers, circuit breakers, shared memory, checkpoints
- CHYBÍ: deterministické fáze (harness), path-specific rules, forced tool_choice, validační smyčky po každém kroku
- Viz `docs/HARNESS_STRATEGY.md` pro detailní plán integrace

---

## 2026-03-22 — YouTube transcript MCP nefunkční

### Problém
- MCP server `youtube-transcript` hlásí "Video unavailable" na VŠECHNA videa
- Není ani v claude_mcp_config.json — pravděpodobně built-in/legacy

### Řešení
- `yt-dlp` (pip) — spolehlivý, aktivně udržovaný
- Verze 2025.09.05 vyžadovala update (YouTube mění ochranu často)
- Po update na 2026.3.17 funguje bez cookies (ale varuje o chybějícím JS runtime)
- Příkaz: `yt-dlp --write-auto-sub --sub-lang "en" --skip-download -o "output" URL`
- VTT soubory vyžadují čištění (duplicitní řádky, inline timing tagy)

### Poučení
- Před doporučením instalace MCP serveru VŽDY ověřit funkčnost
- yt-dlp > jakýkoli MCP wrapper (přímý, spolehlivý, žádná extra vrstva)

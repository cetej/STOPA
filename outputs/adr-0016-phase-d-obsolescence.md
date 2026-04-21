# ADR 0016 Phase D — Obsolescence Scenarios

**Date:** 2026-04-21
**Input:** Phase B research brief + Phase C council verdict + user answer to Futurist's forcing question ("Neopustil")
**Method:** Scenario analysis (no new web research — synthesized from existing Phase B data + current STOPA architecture knowledge)

---

## Framing

User answered "Neopustil" — STOPA has independent value beyond memory backend. This is the correct lens: ask not "when will STOPA lose" but rather "which STOPA components have natural expiry dates, and what should we build that survives?"

STOPA je organismus, ne monolit. Různé vrstvy mají různý horizon.

---

## STOPA ve vrstvách

| Vrstva | Co to je | Replaceability |
|--------|----------|----------------|
| **Memory semantics** | YAML frontmatter, maturity tiers, lifecycle fields, graduation triggers | Nízká — nikdo jiný tuto granularitu nemá |
| **Skill system** | 80+ skills, user-invocable, self-evolve loop | Střední — Letta/Goose mají přibližné analogy |
| **Hooks / harness** | SessionStart, PostToolUse, PermissionRequest hooks, scheduled tasks | Střední — CC native hooks pokrývají základ |
| **Memory backend** | File-based grep+BM25+RRF, concept graph | Vysoká — CMM GA ho nahradí jako backend (ale ne sémantiku) |
| **Cross-project routing** | /improve, project profiles, GitHub issues | Nízká — nikde jinde neexistuje |
| **Orchestration logic** | orchestrate skill, budget tiers, SEPL operators | Střední — Claude Code long-horizon modely erodují potřebu |
| **Self-improvement loop** | autoloop, autoresearch, scribe, evolve | Nízká — unikátní v kombinaci |

---

## Horizon analýza

### Q3 2026 (za 6 měsíců)

**Co se pravděpodobně stane:**
- Claude Managed Agents Memory API hits GA — cross-session native memory pro workspace
- Claude Code dostane nativní Session Memory upgrade (od v2.1.59 je to injekce souborů; GA CMM přidá proper API)
- Cursor Composer 2 nástupce — RL long-horizon modely dále zlepšeny (CursorBench 61.3 → 70+)
- Microsoft Copilot Studio SMB tier — 30% šance, nepotvrzeno

**Dopad na STOPA:**
- Memory backend vrstva: **ztrácí unikátnost** (ale ne sémantiku nad ní). Migrace na CMM backend = strategická odpověď (ADR 0017 — done)
- Orchestration: **eroduje u jednoduchých tasků**. Solodev s dobrým modelem + CC long-horizon potřebuje /orchestrate méně
- Hooks/harness: **drží**. CC native hooks nedosáhnou breadth STOPA (37+ hooks, custom logic)
- Skills: **drží**. 80+ custom skills = osobní library, nekupitelná

**STOPA v Q3 2026:** Stále relevantní, ale musí migrovat memory backend. Orchestration skills se stanou optional pro jednoduché úkoly. Self-improve loop a cross-project routing jsou stále silné.

---

### Q1 2027 (za 9 měsíců)

**Co se pravděpodobně stane:**
- Claude 5 nebo Opus 6 (Anthropic roadmap) — výrazně silnější long-horizon planning
- CMM GA je zajetá, má community plugins a integrace
- Letta's Context Repositories + Skill Learning — více produkčně zralé (dnes beta)
- Apple WWDC 2026 → Siri agents expanze na macOS (uživatel je Windows — nerelevantní)
- Google Gemini Personal Intelligence 2.0 (cross-Google + třetí strany?)
- Možná: Microsoft Copilot Studio non-enterprise tier

**Dopad na STOPA:**
- Memory layer: s CMM migrated adaptorem → STOPA si drží lifecycle sémantiku NAD CMM. **Klíčová diferenciace přetrvává.**
- Orchestration: **výraznější eroze**. Claude 5 zvládne to, co dnes potřebuje 5-agent farm tier, v 1 single-agent run. Budget tiers budou třeba rekalibrace.
- Skills system: **drží a roste**. Osobní library akumuluje. Czech heuristiky, NGM-specifické skills — nikdo to nezkopíruje.
- Self-improve loop: **drží**. Žádný konkurent nepublikoval funkční autoloop+autoresearch+evolve kombinaci.
- Cross-project routing: **drží**. CMM je workspace-scoped, STOPA routing je cross-repo, cross-domain.

**Přímá hrozba v Q1 2027:** Pokud Anthropic nebo Cursor přidá cross-project memory natively, STOPA's cross-project routing advantage se erodes. Pravděpodobnost: 25%.

**STOPA v Q1 2027:** Silnější v lifecycle sémantice + cross-project + custom skills. Slabší v orchestration complexity (jednoduché tasky). Memory backend na CMM. Orchestrate skill = useful for complex only.

---

### H2 2027 (za 12-18 měsíců)

**Spekulativní, nízká jistota — jako scénáře, ne predikce:**

**Scénář A: "Jarvis existence" (optimistický)**
AI assistenti dosáhnou dostatečné kvality, že custom orchestration je mainstream. STOPA se stane *referenční implementací* — jiní buildují na STOPA patterns. Memory lifecycle sémantika je citována v Letta/CMM dokumentaci. STOPA skills library = osobní competitive advantage, nereplikovatelná.

**Scénář B: "Managed takeover" (realistický)**
Anthropic vydá "Claude Workspace" — hosted meta-agent s native memory, skills marketplace, scheduled tasks, cross-project routing. Ne-dev uživatelé migrují tam. Dev uživatelé (user = dev) zůstávají u STOPA pro kontrolu a customizaci. STOPA = "power user layer" nad managed platformou.

**Scénář C: "Model sufficiency" (pesimistický pro orchestration)**
Claude 6/Opus 7 dosáhnou single-agent sufficiency — bez orchestrace zvládnou 8-hour agentic tasks. STOPA orchestration layer je redundantní. Ale: memory lifecycle, skills library, cross-project routing, self-improve loop *survives*. Orchestrace jako vrstva = dead, ostatní 4 vrstvy = alive.

**Scénář D: "Platform lock-in" (hrozba)**
Microsoft/Google vydají dev-tier platformy, které nabízejí controlled environment + skills marketplace + scheduled tasks jako managed service s lepším UX. Uživatel přejde. STOPA jako projekt ztrácí smysl. Pravděpodobnost: 15% (counter: user řekl "neopustil", a Copilot Studio / Gemini jsou ecosystem-locked).

**STOPA v H2 2027 (best estimate):** Scénář B je nejpravděpodobnější — STOPA jako power-user customization layer, kde CMM/Copilot-like platforms pokrývají mainstream, STOPA pokrývá Czech-specific, cross-project, lifecycle-rich, dev-oriented potřeby. Nejméně 2 ze 4 vrstev (memory semantics + skills) zůstávají relevantní dlouhodobě.

---

## Sunset kritéria (kdy bychom měli přestat investovat)

STOPA ztrácí smysl, pokud **všechny** z níže nastávají najednou:

1. **Managed platform pokrývá cross-project routing nativně** — cross-project improvement routing je dostupné bez custom code
2. **Memory lifecycle je natívě v API** — maturity tiers, confidence, graduation triggers — součást CMM nebo ekvivalentu
3. **Skills marketplace existuje** — jiní buildují a sdílejí skills, nemusíme budovat od nuly
4. **Self-improve loop je součástí modelu** — model se sám vylepšuje bez STOPA's autoloop+autoresearch+evolve

Toto nastane nejdříve H2 2027, pravděpodobněji 2028-2029. **Investice do STOPA má smysl minimálně 12-18 měsíců.**

---

## Co buildovat, aby to přežilo

Pořadí dle "survival probability" po 18 měsících:

1. **Skills library (nejvyšší survival)** — osobní akumulace, nereplikovatelná, roste každou session
2. **Memory lifecycle sémantika** — nadstavba nad jakýmkoliv backendem (CMM-ready díky ADR 0017)
3. **Cross-project routing** — chybí všem managed platformám, unikátní value
4. **Self-improve loop** — unikátní; i kdyby modely byly lepší, loop na vlastní data je nereplicovatelné
5. **Hooks/harness** — eroduje jak CC nativně roste, ale ještě 2 roky relevantní
6. **Orchestration engine** — eroduje nejrychleji s modely; zbyde jako "complex tasks only" vrstva

---

## Závěr pro uživatele

**STOPA bude relevantní minimálně do Q3 2027.** Jádro — skills, memory sémantika, cross-project routing — je v bezpečí i proti plnému CMM rollout, protože Anthropic nemůže zahrnout Czech-specific context, NGM-specifické workflow a individuální lifecycle preferences do managed produktu.

Nejdůležitější investice pro maximální survival probability:
1. **Dokončit CMM migration** (ADR 0017, weeks 3-4 — probíhá)
2. **Rostoucí skills library** — každý nový projekt = nové skills, ROI se kumuluje
3. **Cross-project routing** — rozšířit na více projektů (momentálně 10, každý přidaný projekt zvyšuje hodnotu sítě)

**Kdy rekalibrace?** Při každém quarterly platform check (Copilot Studio, CMM, Gemini). Trigger: "did managed platform ship cross-project routing AND memory lifecycle?" — pokud ano oba, STOPA senior layers pod otazníkem.

# Nurture-First Development (NFD)

**Source:** arXiv:2603.10808 (Linghao Zhang, 2026-03-11)
**Updated:** 2026-04-15

---

## Co to je

Paradigma pro budování domain-expert AI agentů kde agent **začíná minimálně a roste skrze strukturovaný dialog** s doménovými experty. Staví na principu, že odborné znalosti jsou ze své podstaty tacitní (nesdělitelné přímým zápisem), osobní a neustále se vyvíjejí.

Klíčový argument: tradiční sequential development (design → deploy) selhává, protože předpokládá, že knowledge encoding je diskrétní fáze před nasazením. Ve skutečnosti je to kontinuální proces.

---

## Hlavní komponenty

### Knowledge Crystallization Cycle
Mechanismus, který konsoliduje fragmentované operační znalosti (získané z dialogu) do znovupoužitelných, strukturovaných assets. Analogie: tacit knowledge → explicit knowledge → reusable schema.

### Three-Layer Cognitive Architecture
Organizuje znalosti agenta podle dvou dimenzí:
- **Volatility** — jak rychle se znalost mění
- **Personalization** — jak specifická je pro konkrétního experta/domény

### Dual-Workspace Pattern
Odděluje exploračního workspace (kam jdou nové, neověřené fragmenty) od crystallized workspace (ověřené, strukturované znalosti).

### Spiral Development Model
Iterativní smyčka: dialog → extrakce → kristalizace → validace → zpět na dialog.

---

## Vztah k jiným konceptům

- **[[compiler-analogy]]** — Knowledge Crystallization Cycle je compiler analogy aplikovaná na agentní úrovni: dialog = source code, crystallization = compilation, structured assets = binary
- **[[second-brain]]** — NFD je implementační přístup pro budování "second brain" agenta skrze interakci, ne batch ingest
- **[[active-metacognitive-curation]]** — oba přístupy říkají, že memory management musí být aktivní a řízený (ne pasivní RAG)
- **[[llm-wiki]]** — Karpathyho LLM Wiki je výsledkem NFD procesu: iterativní kompilace zdrojů do wiki
- **[[memfactory]]** — MemFactory poskytuje technickou infrastrukturu (RL-based extraction/update), NFD poskytuje metodologický rámec
- **[[stopa]]** — STOPA /evolve, /scribe, /compile skills jsou implementace NFD principů: systém začal minimálně a roste z korekcí a poznatků

---

## Kontradikce

`[!contradiction]` **vs. batch PKM přístupy (BASB CODE)**
BASB předpokládá, že uživatel aktivně Captures → Organizes → Distills. NFD říká, že agent má za ulohu extrahovat znalosti z normálního dialogu, bez explicitní capture akce od uživatele. Různé úhly: BASB je user-driven, NFD je agent-driven.

---

## Aplikace v STOPA

STOPA je NFD systém v praxi:
- Skills začínaly minimálně (jednoduchý prompt)
- Evoluce přes `/evolve`, `/scribe`, korekce v learnings/
- `behavioral-genome.md` = crystallized knowledge (výsledek iterací)
- `brain/` je knowledge crystallization artifact

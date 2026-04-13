---
date: 2026-04-11
type: architecture
severity: high
component: memory
tags: [memory, harness, lock-in, portability, sovereignty]
summary: "Harrison Chase (LangChain): memory není plugin, je to harness. Closed harness = ztráta memory. STOPA je 80% open, ale 3 rizikové body: server-side compaction, auto-memory mimo git, skill format lock-in. 6 konkrétních vylepšení."
source: external_research
confidence: 1.00
uses: 3
successful_uses: 0
harmful_uses: 0
related: [2026-04-07-cross-project-memory-design.md, 2026-03-29-memcollab-agent-agnostic-memory.md]
verify_check: manual
---

## Kontext

Harrison Chase (LangChain/LangSmith) + Sarah Wooders (Letta/MemGPT): memory je core capability harnessu, ne plugin. Closed harness (Anthropic Managed Agents, Codex encrypted compaction) = lock-in přes memory. Open harness = vlastníš svou memory.

**STOPA audit:** ~80% open (git-tracked markdown/YAML), ale 3 rizikové body.

## Rizikové body STOPA

### R1: Server-side compaction (VYSOKÉ)
Claude Code komprimuje kontext server-side — nemáme kontrolu nad tím, co se zahazuje. Naše truncation boundaries v checkpoint.md jsou částečná obrana, ale compaction samotná je black box.

### R2: Auto-memory mimo git (STŘEDNÍ)
`~/.claude/projects/<path>/memory/` je Anthropic-vlastněný formát mimo git. Cenné záznamy (user preferences, feedback, project context) žijí jen tam.

### R3: Skill format lock-in (STŘEDNÍ)
SKILL.md s YAML frontmatter je Claude Code specifický. Přechod na jiný harness (Deep Agents, OpenCode) = přepis všech 50+ skills.

---

## 6 vylepšení k implementaci

### V1: Compaction Defense Hook (priorita: VYSOKÁ)
**Co:** PreCompaction/PostCompaction hook, který po detekci komprese re-injectne kritický kontext.
**Jak:** 
- Hook `memory-anchor.py` na `PostCompaction` event (pokud CC tohle vystaví)
- Fallback: periodický `NotificationSend` s memory anchors (critical-patterns, key-facts, active task)
- "Memory anchors" = max 500 tokenů nejkritičtějšího kontextu, vždy přežijí kompresi
**Effort:** medium — závisí na CC PostCompaction hook dostupnosti
**Fallback:** Manuální `/compact` skill, který ukládá kontext PŘED server-side kompresí

### V2: Auto-Memory → Git Mirror (priorita: VYSOKÁ)
**Co:** Scheduled task nebo post-session hook, který cenné auto-memory záznamy kopíruje do `.claude/memory/`.
**Jak:**
- Script `scripts/mirror-automemory.py`:
  - Čte `~/.claude/projects/C--Users-stock-Documents-000-NGM-STOPA/memory/MEMORY.md`
  - Parsuje záznamy, identifikuje nové od posledního mirror
  - Kopíruje relevantní `.md` soubory do `.claude/memory/auto-mirror/`
  - Git-trackuje mirror — nyní je memory v NAŠEM repu
- Trigger: `/sweep` nebo scheduled task denně
**Effort:** low — jednoduchý Python script
**Benefit:** Veškerá memory v gitu, přenositelná, verzovaná, diffovatelná

### V3: Memory Export Standard (priorita: STŘEDNÍ)
**Co:** Exportní formát pro celou STOPA memory, čitelný jakýmkoliv harness.
**Jak:**
- `scripts/memory-export.py --format jsonl|yaml|sqlite`
- Exportuje: learnings/, critical-patterns.md, key-facts.md, decisions.md, wiki/
- Výstup: jeden soubor s unified schema:
  ```jsonl
  {"type": "learning", "id": "2026-04-11-calm", "severity": "medium", "content": "...", "tags": [...]}
  {"type": "decision", "id": "D042", "date": "2026-04-11", "content": "..."}
  ```
- Import script pro target harness (Deep Agents `agents.md`, OpenCode, atd.)
**Effort:** medium
**Benefit:** Memory přenositelná mezi harness systémy. Pojistka proti lock-in.

### V4: Skill Portability Adapter (priorita: NÍZKÁ)
**Co:** Generátor, který z SKILL.md vytvoří ekvivalent pro jiné harness formáty.
**Jak:**
- `scripts/skill-export.py --target deepagents|opencode|generic`
- Mapuje SKILL.md frontmatter → target formát (agents.md, OpenCode config)
- Core instrukce (body) zůstávají markdown — přenositelné inherentně
- Frontmatter (allowed-tools, permission-tier) = harness-specifické, vyžaduje mapping tabulku
**Effort:** medium-high (závisí na stabilizaci target formátů)
**Timing:** Počkat až se agents.md standard ustálí (zatím early)

### V5: State Sovereignty Audit (priorita: STŘEDNÍ)
**Co:** Script, který audituje kde žije jaká memory a identifikuje single-vendor závislosti.
**Jak:**
- `scripts/sovereignty-audit.py`
- Scanuje: `.claude/memory/` (git), `~/.claude/projects/*/memory/` (auto), `~/.claude/` (global)
- Reportuje:
  - ✅ Git-tracked (vlastníme)
  - ⚠️ Auto-memory only (kopie v Anthropic formátu)
  - ❌ Server-only (compaction state, conversation history)
- Doporučení pro každý ❌/⚠️ záznam
**Effort:** low
**Benefit:** Visibility — víme přesně co ztratíme při změně harnessu

### V6: Model-Agnostic Retrieval Layer (priorita: NÍZKÁ — už 90% hotovo)
**Co:** Ověřit, že celý retrieval pipeline funguje bez Claude-specifických features.
**Stav:**
- ✅ Grep-first retrieval = model-agnostic (file-based)
- ✅ BM25 search (`memory-search.py`) = model-agnostic
- ✅ Concept graph (`concept-graph.json`) = JSON, model-agnostic
- ⚠️ Hybrid retrieval (`hybrid-retrieve.py`) = model-agnostic, ale RRF weights laděné na Claude
- ⚠️ Learning admission hook = LLM-dependent (contradiction detection)
**Akce:** Parametrizovat LLM-dependent komponenty tak, aby přijímaly model endpoint jako argument

---

## Implementační pořadí

| Fáze | Vylepšení | Effort | Impact |
|------|-----------|--------|--------|
| 1 (teď) | V2: Auto-memory mirror | low | high |
| 1 (teď) | V5: Sovereignty audit | low | medium |
| 2 (brzy) | V1: Compaction defense | medium | high |
| 2 (brzy) | V3: Memory export | medium | high |
| 3 (later) | V6: Retrieval parametrizace | low | low |
| 4 (wait) | V4: Skill portability | medium-high | medium |

# ByteRover vs STOPA Memory — Deep Analysis & Upgrade Proposals

**Source:** arXiv:2604.01599 (2026-04-02) — Andy Nguyen et al.
**Date:** 2026-04-05

---

## 1. ByteRover Architecture Summary

ByteRover je memory systém pro AI agenty s klíčovou tezí: **"The system that stores knowledge does not understand it"** — v existujících systémech (Mem0, Zep, MemGPT) je storage oddělený od reasoning. ByteRover to invertuje: stejný LLM, který o úkolech uvažuje, také kurátoruje znalosti.

### Hierarchický Context Tree

```
.brv/context-tree/
├── DOMAIN/
│   ├── TOPIC/
│   │   ├── SUBTOPIC/
│   │   │   └── entry.md          # Leaf node
│   │   └── context.md            # Auto-generated summary
│   └── context.md
└── context.md
```

Každý entry formalizován jako `ni = ⟨ℛi, 𝒞i, 𝒱i, 𝒮i, ℒi⟩`:
- **ℛ (Relations):** `@domain/topic/file.md` cross-references
- **𝒞 (Raw Concept):** Provenance (task, changes, sources, timestamp)
- **𝒱 (Narrative):** Dependencies, rules, examples
- **𝒮 (Snippets):** Code, formulas, raw data
- **ℒ (Lifecycle):** Importance score, maturity tier, recency decay

### 5-Tier Progressive Retrieval

| Tier | Latence | Mechanismus | Threshold |
|------|---------|-------------|-----------|
| 0 — Hash Cache | ~0 ms | Exact hash match | fingerprint valid |
| 1 — Fuzzy Cache | ~50 ms | Jaccard similarity | ≥ 0.6 |
| 2 — Direct Search | ~100 ms | BM25 (normalized) | ≥ 0.93 + gap ≥ 0.08 |
| 3 — Optimized LLM | <5 s | Single LLM call (1024 tok, temp 0.3) | BM25 ≥ 0.89 |
| 4 — Full Agentic | 8-15 s | Multi-turn reasoning (2048 tok, temp 0.5) | fallback |

### Importance Scoring

```
Score(ni, q) = wr · BM25(ni, q) + wι · ι̂i + wt · ri
```

- `ι̂i` = normalized importance (0-100)
- `ri` = recency decay = exp(−Δt/τ), τ=30 days (~21-day half-life)
- Access event: +3 bonus, Update event: +5 bonus
- Daily decay: 0.995^Δt

### Maturity Tiers s Hysterezí

| Tier | Promotion threshold | Demotion threshold | Hystereze |
|------|--------------------|--------------------|-----------|
| Draft | — | — | — |
| Validated | ι ≥ 65 | ι < 35 | gap = 30 |
| Core | ι ≥ 85 | ι < 60 | gap = 25 |

### Benchmark Výsledky

**LoCoMo:** 96.1% overall (SOTA), +6.2 pp nad HonCho, +9.3 pp na multi-hop
**LongMemEval-S:** 92.8% overall (SOTA), silný na temporal reasoning (91.7%)

### Ablation: Co nejvíc pomáhá

| Component odebraný | Drop |
|--------------------|------|
| Tiered Retrieval | **−29.4 pp** (kritický) |
| OOD Detection | −0.4 pp |
| Relation Graph | −0.4 pp |

→ Tiered retrieval je klíčový. Relations mají marginální dopad na benchmarku (ale silnější na multi-hop v LoCoMo).

---

## 2. STOPA Memory — Current State

### Silné stránky (co STOPA dělá dobře)

1. **Write-time admission control** — learning-admission.py hook (salience + contradiction detection) = strukturálně lepší než read-time filtering. ByteRover tohle nemá explicitně.

2. **Impact scoring** — `impact_score` měřený /critic porovnáním kvality s/bez learningu. ByteRover má jen frequency-based importance.

3. **Graduation s dual paths** — (uses ≥ 10 + confidence ≥ 0.8) OR (impact ≥ 0.7 + uses ≥ 5). ByteRover má jen importance thresholds.

4. **Verify-check fields** — Machine-checkable assertions (Grep/Glob). ByteRover nemá nic srovnatelného.

5. **Source credibility weighting** — user_correction 1.5× vs agent_generated 0.8×. ByteRover nemá rozlišení zdrojů.

6. **Supersedes + related** — Lightweight multi-hop bez full graph. Efektivní pro 57 learnings.

### Slabé stránky (kde ByteRover ukazuje cestu)

1. **Flat structure** — 57 learnings v jednom adresáři, organizace jen přes component indices. Při růstu na 200+ entries bude grep-first retrieval degradovat.

2. **Žádná hierarchie** — chybí Domain → Topic → Subtopic strom. Learning o "skill description triggers" a "skill description = trigger only" jsou v různých souborech bez explicit containment.

3. **Žádný cache layer** — každý retrieval = grep + YAML parsing. ByteRover řeší 80%+ dotazů v Tier 0-1 (< 50 ms).

4. **Confidence decay je lineární** — STOPA: −0.1/30 dní. ByteRover: exponenciální decay exp(−Δt/30) s hysterezí. Exponenciální je přesnější model paměti.

5. **Žádný context.md (auto-summary)** — ByteRover auto-generuje summary pro každou úroveň stromu. STOPA má jen manuální critical-patterns.md.

6. **Atomic operations chybí** — ByteRover má 5 formálních operací (ADD, UPDATE, UPSERT, MERGE, DELETE) s audit trail. STOPA má ad-hoc zápisy.

7. **Maturity tiers chybí** — STOPA má jen confidence + graduation trigger. ByteRover má Draft → Validated → Core s hysterezí (prevence oscilace).

---

## 3. Konkrétní Upgrade Proposals

### Proposal A: Hierarchické Topic Clustering (HIGH PRIORITY)

**Problém:** 57 flat learnings, retrieval závisí na grep keyword match.

**Řešení:** Zavést 2-úrovňovou hierarchii v `learnings/`:

```
learnings/
├── skill-development/
│   ├── _context.md              # Auto-generated topic summary
│   ├── 2026-03-25-skill-description-triggers.md
│   ├── 2026-03-27-skills-must-live-in-stopa.md
│   └── 2026-04-04-skill0-dynamic-curriculum.md
├── orchestration/
│   ├── _context.md
│   ├── 2026-03-29-bigmas-directed-graph-orchestration.md
│   └── 2026-03-30-society-of-thought-orchestration.md
├── memory-systems/
│   ├── _context.md
│   ├── 2026-03-29-memcollab-agent-agnostic-memory.md
│   └── 2026-03-30-write-time-gating-salience.md
├── operational-guardrails/
│   ├── _context.md
│   ├── 2026-03-27-playwright-mcp-download-hijack.md
│   └── 2026-03-27-secrets-in-config-files.md
└── _uncategorized/              # New learnings land here first
    └── ...
```

**`_context.md`** — auto-generovaný summary tématu (inspirace ByteRover context.md):
```yaml
---
topic: skill-development
entries: 14
last_updated: 2026-04-04
summary: "Patterns for skill authoring, triggers, distribution, and lifecycle..."
top_tags: [skill, trigger, description, testing]
---
```

**Implementace:**
- Přidat `topic:` field do YAML frontmatter learnings (backwards-compatible, optional)
- Script `cluster-learnings.py` přesune soubory do topic dirs + generuje `_context.md`
- Retrieval: grep-first zůstává, ale při 0 matches fallback na `_context.md` summaries
- Stávající index soubory (`index-skill.md` etc.) se stanou redundantní → nahradit `_context.md`

**Effort:** Medium. Backwards-compatible — stávající flat files fungují dál.

### Proposal B: Tiered Retrieval Cache (HIGH PRIORITY)

**Problém:** Každý retrieval = grep + read. ByteRover ablation: tiered retrieval = −29.4 pp bez něj.

**Řešení:** 3-tier cache pro STOPA (zjednodušená verze ByteRover 5-tier):

**Tier 0 — Session Cache (in-memory)**
- Dict `{query_hash: [matched_filenames]}` v intermediate/
- Platnost: aktuální session
- Hit rate estimate: 30-40% (opakované dotazy na stejný component)

**Tier 1 — Keyword→File Index (persistent)**
- `intermediate/keyword-index.json`: mapování `{keyword: [filename, filename, ...]}`
- Generuje se při `learning-admission.py` zápisu (write-time indexing)
- Retrieval: split query na keywords → lookup v indexu → union filenames
- Latence: ~0 ms (JSON lookup vs grep across 57+ files)

**Tier 2 — Full Grep (current behavior)**
- Fallback když Tier 0-1 nic nenajdou
- Synonym fallback zůstává zde

**Implementace:**
- `keyword-index.json` se už částečně buduje v `learnings-index.json` → rozšířit o keyword mapping
- Session cache = nový soubor `intermediate/session-retrieval-cache.json`
- Backwards-compatible: pokud cache chybí, fallback na grep

**Effort:** Low-Medium. Většina infrastruktury existuje.

### Proposal C: Exponenciální Decay s Hysterezí (MEDIUM PRIORITY)

**Problém:** STOPA confidence decay je lineární (−0.1/30 dní), bez hystereze.

**Současný model:**
```
confidence -= 0.1  (every 30 days if uses == 0)
min = 0.1
```

**Navrhovaný model (inspirace ByteRover):**
```python
# Decay: exponenciální
confidence = base_confidence * exp(-days_unused / 90)
# τ=90 dní (pomalejší než ByteRover τ=30, protože STOPA learnings jsou stabilnější)

# Hystereze: maturity tiers
if confidence >= 0.85 and uses >= 5:
    maturity = "core"       # Slow decay (τ=180)
elif confidence >= 0.60:
    maturity = "validated"  # Normal decay (τ=90)
else:
    maturity = "draft"      # Fast decay (τ=45)

# Demotion thresholds (hystereze):
# core → validated: confidence < 0.55 (gap = 30)
# validated → draft: confidence < 0.30 (gap = 30)
```

**Proč hystereze:** Prevence oscilace. Learning na hranici 0.85 by bez hystereze skákal mezi core/validated s každým drobným decay tickem.

**Effort:** Low. Změna v decay logice, backwards-compatible (stávající learnings bez maturity = "validated" default).

### Proposal D: Formální Curate Operations (MEDIUM PRIORITY)

**Problém:** STOPA learnings se zapisují ad-hoc. Žádný formální audit trail operací.

**Řešení:** 5 atomických operací (adaptace ByteRover):

| Operace | Popis | Kdy |
|---------|-------|-----|
| **ADD** | Nový learning + auto-update `_context.md` | /scribe, auto-capture |
| **UPDATE** | Aktualizace existujícího (nový obsah, bump uses/confidence) | /evolve, /critic |
| **MERGE** | Sloučení 2 learnings do jednoho (+ supersedes) | /compile, maintenance |
| **ARCHIVE** | Přesun do archive (low confidence, stale) | /evolve, auto-decay |
| **PROMOTE** | Graduation do critical-patterns.md | /evolve |

Každá operace loguje do `intermediate/curation-log.jsonl`:
```json
{"op": "MERGE", "source": ["2026-03-25-skill-triggers.md", "2026-04-01-trigger-patterns.md"], "target": "2026-04-05-skill-trigger-patterns.md", "reason": "Duplicate coverage of trigger conditions", "actor": "evolve", "ts": "2026-04-05T14:30:00"}
```

**Effort:** Medium. Vyžaduje úpravu /scribe, /evolve, /compile.

### Proposal E: Auto-Generated Context Summaries (LOW PRIORITY)

**Problém:** Při retrieval na nové téma musí agent číst N souborů. ByteRover `context.md` na každé úrovni stromu řeší toto.

**Řešení:** `_context.md` per topic (viz Proposal A) + globální `learnings/_overview.md`:

```markdown
# Memory Overview (auto-generated 2026-04-05)

57 learnings across 6 topics. Last 7 days: 8 new, 2 updated, 0 archived.

## Topics
| Topic | Entries | Avg Confidence | Top Pattern |
|-------|---------|---------------|-------------|
| skill-development | 14 | 0.78 | Trigger-only descriptions |
| orchestration | 18 | 0.72 | Budget-first tier selection |
| memory-systems | 8 | 0.81 | Write-time > read-time gating |
| operational-guardrails | 7 | 0.85 | No secrets in configs |
| research-patterns | 6 | 0.68 | Meta-harness traces > summaries |
| general | 4 | 0.65 | — |
```

**Generace:** Script nebo /compile skill, spouštěný při maintenance.

**Effort:** Low. Mostly reporting, no architectural change.

---

## 4. Co NEADOPTOVAT z ByteRover

### BM25 Full-Text Index
ByteRover používá MiniSearch s BM25. Pro 57 learnings je to overkill — grep-first je dostatečný. Má smysl teprve při 500+ entries.

### Relation Graph s Bidirectional Index
Ablation ukazuje −0.4 pp bez relací. STOPA `related:` field s 1-hop expansion je dostatečný pro current scale. Full bidirectional index by přidal komplexitu bez proporcionálního benefitu.

### Sandboxed Curation Environment
ByteRover pouští curate operace v sandboxu. Pro STOPA zbytečné — learnings jsou low-risk markdown soubory, ne executable kód.

### 5-Tier Retrieval (full version)
Tier 3-4 (LLM calls pro retrieval) jsou pro STOPA zbytečné — naše learnings jsou dostatečně strukturované pro keyword retrieval. LLM-based retrieval má smysl pro free-form knowledge bases, ne YAML-tagged entries.

---

## 5. Implementation Roadmap

### Phase 1 — Quick Wins (effort: 1-2 sessions)
1. **Keyword index** v `intermediate/keyword-index.json` (Proposal B, Tier 1)
2. **Maturity field** do YAML frontmatter (Proposal C, backwards-compatible)
3. **Curation log** `intermediate/curation-log.jsonl` (Proposal D, logging only)

### Phase 2 — Topic Hierarchy (effort: 2-3 sessions)
4. **Topic clustering** — `cluster-learnings.py` script (Proposal A)
5. **`_context.md` generation** per topic (Proposal E)
6. **Retrieval update** — topic-first → keyword → grep fallback

### Phase 3 — Lifecycle Maturation (effort: 1-2 sessions)
7. **Exponentiální decay** nahradí lineární (Proposal C)
8. **Hystereze** pro maturity tier transitions
9. **Formální curate operations** v /scribe a /evolve (Proposal D)

### Estimated Impact
- **Retrieval precision** na 100+ learnings: +15-25% (topic clustering + keyword index)
- **False retrieval** (irrelevant matches): −30% (topic containment)
- **Maintenance overhead**: −40% (auto-summaries, formal operations)
- **Session start latency**: unchanged (critical-patterns.md zůstává always-read)

---

## 6. Key Insight: Co ByteRover Validuje v STOPA Designu

ByteRover nezávisle potvrzuje několik STOPA design decisions:

1. **Markdown-on-disk > vector DB** — ByteRover dosahuje SOTA bez embeddings. Validuje STOPA přístup.
2. **Write-time quality control** — ByteRover curate operations = STOPA admission control. Oba systémy preferují kontrolu při zápisu.
3. **Recency decay** — oba systémy exponenciálně penalizují staré znalosti. STOPA by měla přejít z lineárního na exponenciální.
4. **Hierarchie pomáhá** — ByteRover 4 úrovně vs STOPA flat. Ale ablation ukazuje, že relations jsou marginální — **2-level topic hierarchy stačí**.
5. **Cache je kritický** — ByteRover −29.4 pp bez tiered retrieval. STOPA by měla přidat alespoň keyword index cache.

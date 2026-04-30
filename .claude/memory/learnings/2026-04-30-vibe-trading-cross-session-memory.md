---
date: 2026-04-30
type: architecture
severity: medium
component: memory
tags: [memory, cross-session, persistence, architecture, external-validation]
summary: HKUDS Vibe-Trading PersistentMemory implementace je téměř identický mirror STOPA auto-memory: ~/.vibe-trading/memory/ s MEMORY.md indexem (200 řádků) + per-entry .md soubory s YAML frontmatter (name/description/type). Rozdíly STOPA→VT: explicit "frozen snapshot" pattern (loaded once at session start pro prompt cache preservation), tokenizace ASCII+CJK, metadata weight 2.0× body weight. Žádný decay/confidence/maturity (STOPA sophisticated). Validuje STOPA design choices, jeden adoption candidate.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
verify_check: "WebFetch('https://github.com/HKUDS/Vibe-Trading/blob/main/agent/src/memory/persistent.py') → contains 'PersistentMemory'"
---

# HKUDS Vibe-Trading — cross-session memory analysis

## TL;DR

Vibe-Trading používá **téměř identický pattern** jako STOPA auto-memory (`~/.claude/projects/.../memory/MEMORY.md` + per-entry .md s YAML frontmatter). Rozdíly jsou kosmetické. Externí validace STOPA design choices.

## Implementation (literal z agent/src/memory/persistent.py)

```python
MEMORY_BASE = Path.home() / ".vibe-trading" / "memory"
MAX_INDEX_LINES = 200
MAX_ENTRY_CHARS = 8000
MAX_RESULTS = 5
METADATA_WEIGHT = 2.0
```

**Storage layout** (komentář ze zdrojáku):
```
~/.vibe-trading/memory/
├── MEMORY.md          # Index (< 200 lines)
├── user_prefs.md      # Individual memory entries with YAML frontmatter
├── project_btc.md
└── ...
```

**Frontmatter formát:**
```yaml
---
name: <title>
description: <one_line>
type: user | feedback | project | reference
---
<body content>
```

**Memory types** (z `add()` metody): `user`, `feedback`, `project`, `reference` — **identické se STOPA auto-memory typy**.

**Filename convention:** `{memory_type}_{slug}.md` kde slug je sanitized lowercase max 60 chars.

## Key design pattern: "Frozen Snapshot"

```python
class PersistentMemory:
    """
    Design:
        - Frozen snapshot injected into system prompt at session start
          (preserves prompt cache).
        - Disk writes via add()/remove() update files immediately
          but do NOT change the snapshot.
        - Next session picks up the updated state.
    """
```

**To je pattern kterého STOPA tacitně dosahuje** přes `@MEMORY.md` injection v CLAUDE.md, ale Vibe-Trading to dělá explicit:
1. Init: load `MEMORY.md` (max 200 lines) → `self._snapshot`
2. Snapshot injectován do system prompt → preservuje prompt cache
3. `add()/remove()` zapíše na disk, ale **NEZMĚNÍ snapshot v aktuální session**
4. Příští session = nový load = nový snapshot

**STOPA value-add:** Tato explicit oddělenost (snapshot vs disk) je elegantní pro prompt cache preservation. STOPA implicitně dělá totéž, ale neexplicitně dokumentuje.

## Retrieval algorithm

```python
def find_relevant(self, query, max_results=5):
    query_tokens = _tokenize(query)
    for entry in self._scan_entries():
        meta_tokens = _tokenize(f"{entry.title} {entry.description}")
        body_tokens = _tokenize(entry.body)
        score = (
            len(query_tokens & meta_tokens) * METADATA_WEIGHT  # 2.0
          + len(query_tokens & body_tokens)                    # 1.0
        )
```

Tokenizer:
```python
def _tokenize(text):
    ascii_tokens = set(re.findall(r"[a-zA-Z0-9_]{3,}", text.lower()))
    cjk_tokens = set(re.findall(r"[一-鿿㐀-䶿]", text))
    return ascii_tokens | cjk_tokens
```

**Klíčové detaily:**
- Set intersection (Jaccard-like) — žádný TF-IDF, žádný embedding
- ASCII words ≥ 3 chars (filter "the", "and") + CJK individual characters (každý hanzi = token)
- Metadata 2× weight než body — implicit boost pro frontmatter relevance
- `max_results = 5` — small fixed cap

**Tie-break:** `(-score, -modified_at)` → recent files win on ties.

## Comparison: Vibe-Trading vs STOPA

| Feature | Vibe-Trading PersistentMemory | STOPA auto-memory + learnings/ |
|---|---|---|
| Storage path | `~/.vibe-trading/memory/` | `~/.claude/projects/.../memory/` |
| Index file | `MEMORY.md` (200 line cap) | `MEMORY.md` (200 line cap, identical) |
| Per-entry format | YAML frontmatter (name/description/type) | YAML frontmatter (name/description/type/...) |
| Memory types | user, feedback, project, reference | user, feedback, project, reference (+ custom) |
| Filename | `{type}_{slug}.md` | varies (`{topic}_{date}.md` or similar) |
| Retrieval | keyword set-intersect, meta×2.0 | grep-first, then BM25 + graph walk (RRF) |
| Tokenization | ASCII≥3 + CJK chars | grep regex (no formal tokenizer) |
| Decay | NONE | confidence × time-weighted (Hippo log2 boost, decay after 60d) |
| Confidence | NONE | 0.0-1.0 per entry, source-weighted |
| Maturity tier | NONE | draft → validated → core (graduation) |
| Reward modulation | NONE | reward_factor ∈ [0.5, 1.5] modulates decay+boost |
| Cross-references | NONE | supersedes + related (1-hop graph walk) |
| Frozen snapshot | EXPLICIT (documented design pattern) | IMPLICIT (via @MEMORY.md injection) |
| Session integration | snapshot injected into system prompt | MEMORY.md auto-loaded into CLAUDE.md context |
| Prompt cache preservation | EXPLICIT design goal | implicit |

## What STOPA can adopt (1 candidate)

### Candidate: Make "Frozen Snapshot" explicit in STOPA documentation

Současný stav: STOPA `@MEMORY.md` injection je rozprostřený v CLAUDE.md, není dokumentovaný jako prompt-cache-preservation pattern. Hippocampus integration (project_hippocampus_integration.md) by mohla benefit z explicit zápisu:

> **Frozen Snapshot Invariant:** MEMORY.md is loaded at session start and injected into system prompt. Mid-session writes to disk (via /scribe, hooks) update files immediately but DO NOT modify the snapshot. Next session picks up updates. This preserves Anthropic prompt cache (5min TTL) — mid-session writes don't invalidate cached system prompt.

Důsledek: explicitní invariant zabrání budoucím skill autorům "zoptimalizovat" tím že přečtou MEMORY.md per-call (= prompt cache invalidation).

### NE-adopce (STOPA už má lepší)

- **Decay/confidence/maturity** — STOPA má sophistikovanější systém s Hippo log2 boost a reward modulation. Vibe-Trading nemá nic — soubory jen leží na disku.
- **Hybrid retrieval (BM25 + graph walk)** — STOPA má `hybrid-retrieve.py` s RRF fusion. Vibe-Trading má jen keyword set-intersect.
- **Cross-references** — STOPA `supersedes:` + `related:` umožňují multi-hop retrieval. Vibe-Trading nemá.

## What this validates about STOPA design

Externí lab (HKUDS, 3707★ projekt) **nezávisle dospěl k téměř identickému design** pro cross-session memory:
1. Filesystem-based, ne database
2. MEMORY.md index + per-entry .md soubory
3. YAML frontmatter s identickými typy (user/feedback/project/reference)
4. Snapshot injection at session start

To je **silný signal že STOPA's auto-memory design je correct path** pro multi-agent personal AI systems. Confirmation bias caveat: HKUDS authoring quality neznámá independentně, ale 3707★ + recent active development (poslední commit 1 den starý) + kvalita kódu (clean Pydantic, dataclasses, type hints, docstrings) = high signal.

## References

- Source: https://github.com/HKUDS/Vibe-Trading/blob/main/agent/src/memory/persistent.py
- License: MIT (literal copies přípustné)
- Captured: 2026-04-30 batch (radar.md line 137)
- Sibling: HKUDS/OpenHarness (radar 8/10 line 25, STOPA-mirror) — 2 STOPA-mirror projekty od stejné lab = high external corroboration

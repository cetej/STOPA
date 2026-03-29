---
globs: ".claude/memory/**"
---

# Pravidla pro memory soubory

- Max 500 řádků per soubor — při překročení archivuj staré záznamy do `*-archive.md`
- Formát: markdown s jasnou strukturou (headings, tabulky, seznamy)
- Nikdy nemazat historii — přesouvej do archivu
- Datum ve formátu YYYY-MM-DD (absolutní, ne relativní)
- Checkpoint: vždy obsahuje resume prompt pro další session
- Budget: vždy obsahuje aktuální zůstatek a tier

## Key Facts (project reference data)

- `key-facts.md` = factual constants: stack, services, endpoints, env vars, conventions
- NOT for decisions (→ decisions.md) or bug patterns (→ learnings/)
- Updated when infrastructure changes, not per-session
- Skills should check key-facts.md before guessing configs or suggesting libraries
- Format: tables grouped by category (Stack, Services, Env Vars, Dependencies, Conventions)
- Max 200 řádků — pokud roste, rozděl na sekce nebo extrahuj do per-project facts

## Learnings (per-file YAML format)

- Uloženy v `.claude/memory/learnings/` jako jednotlivé soubory
- Každý soubor má YAML frontmatter: date, type, severity, component, tags, summary, uses, harmful_uses
- `summary:` = 1-2 věty popisující co se stalo a co dělat (generuje /scribe automaticky)
- `uses:` = kolikrát byl learning retrieven a aplikován (počáteční hodnota 0, inkrementuje se při použití)
- `harmful_uses:` = kolikrát vedl learning ke špatnému výsledku (počáteční hodnota 0, inkrementuje /critic)
- `supersedes:` = filename staršího learningu, který tento nahrazuje (volitelné, max 1). Superseded soubory se při retrieval přeskakují, ale zůstávají na disku
- `related:` = array filenames souvisejících learnings pro multi-hop retrieval (volitelné, max 3). Pouze 1-hop — žádné řetězení
- Learnings bez counterů (starší záznamy) zůstávají validní — countery jsou volitelné
- Learnings bez `supersedes:`/`related:` polí jsou plně zpětně kompatibilní
- `critical-patterns.md` = always-read (max 10 entries, top patterns)
- Retrieval: grep-first přes component/tags, pak čti jen matched soubory. **Supersedes-aware**: pokud learning A má `supersedes: B`, přeskoč B. **Related expansion**: pokud match má `related: [X, Y]`, čti i X a Y (1-hop, max 3 extra per learning)
- **Synonym fallback** (ref: arXiv:2603.19138 — P4 knowledge-guided retrieval misses semantically similar patterns under different keywords): If initial grep returns 0 matches, generate 2-3 synonyms/related terms from the task context and retry. Example: "validation" miss → retry with "sanitization", "input checking". Max 2 retry rounds. This prevents early pruning of relevant learnings due to keyword mismatch.
- **Time-weighted relevance**: When multiple learnings match, prefer recent ones. Score: `severity_weight × (1 / (1 + days_since_date / 60))`. Weights: critical=4, high=3, medium=2, low=1. A 30-day-old critical (2.67) beats a fresh low (2.0), but a 90-day-old medium (0.8) loses to a fresh low.
- Filename konvence: `<date>-<short-description>.md`
- Staleness: záznamy starší 90 dní ověřit při maintenance
- Type hodnoty: bug_fix | architecture | anti_pattern | best_practice | workflow
- Severity: critical | high | medium | low
- Component: skill | hook | memory | orchestration | pipeline | general

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
- Každý soubor má YAML frontmatter: date, type, severity, component, tags, summary, source, uses, harmful_uses, confidence
- `summary:` = 1-2 věty popisující co se stalo a co dělat (generuje /scribe automaticky)
- `source:` = odkud learning pochází — ovlivňuje write-time gating i retrieval scoring. Hodnoty: `user_correction` (1.5×), `critic_finding` (1.2×), `auto_pattern` (1.0×, default), `agent_generated` (0.8×), `external_research` (0.9×). Soubory bez `source:` se chovají jako `auto_pattern`.
- `uses:` = kolikrát byl learning retrieven a aplikován (počáteční hodnota 0, inkrementuje se při použití)
- `harmful_uses:` = kolikrát vedl learning ke špatnému výsledku (počáteční hodnota 0, inkrementuje /critic)
- `supersedes:` = filename staršího learningu, který tento nahrazuje (volitelné, max 1). Superseded soubory se při retrieval přeskakují, ale zůstávají na disku
- `related:` = array filenames souvisejících learnings pro multi-hop retrieval (volitelné, max 3). Pouze 1-hop — žádné řetězení
- `confidence:` = numerické skóre 0.0-1.0 vyjadřující důvěryhodnost learningu. Počáteční hodnota závisí na source: user_correction=0.9, critic_finding=0.8, auto_pattern=0.7, external_research=0.6, agent_generated=0.5. Decay: learnings nepoužité 60+ dní ztrácí 0.1 confidence za každých 30 dní nečinnosti (min 0.1). Boost: každé `uses` inkrementuje confidence o 0.05 (max 1.0). Každé `harmful_uses` snižuje o 0.15.
- **Graduation trigger**: `uses >= 10` AND `confidence >= 0.8` AND `harmful_uses < 2` → `/evolve` navrhne promoci do `critical-patterns.md` nebo `rules/`. Learning s `confidence < 0.3` → kandidát na pruning při maintenance.
- Learnings bez counterů nebo confidence (starší záznamy) zůstávají validní — nová pole jsou volitelné, default confidence = 0.7
- Learnings bez `supersedes:`/`related:` polí jsou plně zpětně kompatibilní
- `model_gate:` = volitelné pole — model version, pro kterou learning platí (např. `"sonnet-4.6"`, `"opus-4"`). Learnings s tímto polem jsou auto-flagovány `/evolve` a `verify-sweep.py` když aktuální model neodpovídá gate. Model-specifické workaroundy MUSÍ mít toto pole. Obecné architektonické learnings ho NESMÍ mít. Inspirováno CC `@[MODEL_LAUNCH]` tagging konvencí.
- `verify_check:` = volitelné pole — machine-checkable grep/glob assertion. Format: `"Grep('pattern', path='path') → N+ matches"` nebo `"Glob('pattern') → 1+ matches"` nebo `"manual"` pro behaviorální pravidla. Soubory s `verify_check:` jsou auditovány při SessionStart hookem `verify-sweep.py`. Každý learning by měl mít verify_check — rules without checks are wishes, rules with checks are guardrails.
- `critical-patterns.md` = always-read (max 10 entries, top patterns)
- Retrieval: grep-first přes component/tags, pak čti jen matched soubory. **Supersedes-aware**: pokud learning A má `supersedes: B`, přeskoč B. **Related expansion**: pokud match má `related: [X, Y]`, čti i X a Y (1-hop, max 3 extra per learning)
- **Synonym fallback** (ref: arXiv:2603.19138 — P4 knowledge-guided retrieval misses semantically similar patterns under different keywords): If initial grep returns 0 matches, generate 2-3 synonyms/related terms from the task context and retry. Example: "validation" miss → retry with "sanitization", "input checking". Max 2 retry rounds. This prevents early pruning of relevant learnings due to keyword mismatch.
- **Time-weighted relevance**: When multiple learnings match, prefer recent ones with trusted sources. Score: `severity_weight × source_weight × confidence × (1 / (1 + days_since_date / 60))`. Weights — severity: critical=4, high=3, medium=2, low=1. Source: user_correction=1.5, critic_finding=1.2, auto_pattern=1.0 (default), external_research=0.9, agent_generated=0.8. Confidence default=0.7 if field missing. Example: a fresh user_correction/high with confidence=0.9 (3×1.5×0.9=4.05) beats a stale auto_pattern/critical with confidence=0.5 (4×1.0×0.5=2.0).
- Filename konvence: `<date>-<short-description>.md`
- Staleness: záznamy starší 90 dní ověřit při maintenance
- Type hodnoty: bug_fix | architecture | anti_pattern | best_practice | workflow
- Severity: critical | high | medium | low
- Component: skill | hook | memory | orchestration | pipeline | general

---
name: termdb je sole source of truth — žádné subsample, žádné arbitrary limity
description: Při portování pipeline z NG-ROBOT/ADOBE-AUTOMAT NEKOPÍRUJ slepě 100-term limit ani is_primary=1 filter. Termdb je sole source — relevance-driven extract VŠECH relevantních termínů z článku, plný injekt do LLM contextu.
type: feedback
originSessionId: 57ea8e53-fe72-44e8-a188-0332b9f12df0
---
User opakovaně potvrdil princip: **termdb (BIOLIB/termdb.db, ngm-terminology) je jediný zdroj pravdy** pro biologické / geografické / terminologické překlady. Při portování pipeline z NG-ROBOT a ADOBE-AUTOMAT do nového projektu (PREKLAD, 2026-04-27) jsem převzal patterns 1:1 bez kritického zhodnocení a porušil jsem ten princip třemi způsoby:

1. **Default `max_terms=100`** v `format_for_prompt()` — pošle do LLM 100 termínů z 246K dostupných, sortovaných ORDER BY t.id ASC (chronologicky podle vložení do DB, NE relevance pro článek)
2. **Filter `WHERE tr.is_primary = 1`** v `get_protected_terms_cached` — vyfiltruje ~150K iNaturalist překladů (všechny species s `is_primary=0`). Tj. termdb má `Podarcis pityusensis → ještěrka pityuská` ale pipeline ho nikdy neviděla.
3. **EN→CZ key matching** v glossary_enforcer — match přes `canonical_name` (Latin) ale Claude pracuje s běžným EN jménem. Substituce nikdy neběhne i kdyby termín byl v mapě.

**Důsledek:** Claude vygeneroval ad-hoc překlad ("ještěrka zední ibizská" — což je jiný druh, *Podarcis muralis*) místo aby použil termdb pravdu ("ještěrka pityuská"). Porušení sole source principu.

**Why:** User řekl: "ladím s tebou, abychom měli jednotnou databázi jako zdroj pravdy na ověřování termínů, zvláště biologických, a ty necháš v kódu takový bordel?" — opakovaná frustrace ze stejné chyby přes víc projektů.

**How to apply:**

1. **Žádný subsample termdb** v žádném pipelinu (PREKLAD, NG-ROBOT, ADOBE-AUTOMAT, ngm-terminology consumers). Pokud je termdb 246K termínů, neposílej top-100; pošli relevance-filtered subset (typicky 5-50 termínů specifických pro článek).
2. **`is_primary=1` se nesmí použít jako hard filter** — prefer primary, fallback na ANY cs translation. iNaturalist má nejširší pokrytí species.
3. **Latin binomial je primary key** pro biology lookups. Glossary enforcer musí umět:
   - Detect Latin binomial v textu (regex `[A-Z][a-z]+ [a-z]+`)
   - Lookup `terms.canonical_name = Latin → translations.cs`
   - Validate okolní CZ noun phrase odpovídá termdb překladu
   - Force-replace pokud ne, log do glossary_fixes
4. **Pre-translation extraction**: scanuj EN článek pro Latin binomials + proper nouns, lookup VŠECHNY z termdb (canonical_name + aliases), výsledek → MUST-USE binding v Phase 1 promptu.
5. **Při portování pipeline patterns z jiných projektů** vždycky kriticky zhodnoť subsample limity, default filters, sortování. Limity v původu projektu mohou být historický artefakt nebo problém který user už chce opravit.

**Verify:** Při review pipeline kódu grep `is_primary = 1`, `LIMIT 100`, `top.*100`, `max_terms=100` — každý hit je suspect.

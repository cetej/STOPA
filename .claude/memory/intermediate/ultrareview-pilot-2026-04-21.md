---
date: 2026-04-21
type: pilot_blocker
status: not_executed
skill_evaluated: /ultrareview (Anthropic, cloud-based)
comparison_target: /critic (STOPA local)
---

# /ultrareview vs /critic — Pilot Blocker Report

## TL;DR

Pilot **neproveden**. `/ultrareview` je real feature (CC v2.1.86+/v2.1.111), ale vyžaduje:
- Claude.ai login + Pro/Max subscription
- Cloud sandbox (5-10 min per run)
- **3 free runs** pak **$5-$20 per run** (non-refreshing)

Per STOPA pilot rule: *"Pokud `/ultrareview` vyžaduje plán/subscription upgrade — dokumentuj cost estimate ale ukončuj bez pilotu."* → zastaveno.

Navíc: `/ultrareview` není v available-skills listu této session — nelze invokovat z tohoto harness.

## Premise verification

| Claim | Verified? | Source |
|-------|-----------|--------|
| `/ultrareview` existuje | ✓ ANO | CC CHANGELOG v2.1.111 |
| Cloud-based multi-agent review | ✓ ANO | Official docs + vendor reviews |
| Approx. release date | Apr 2026 | Jiten Oswal (Medium), wmedia.es |
| Minimum CC version | v2.1.86 | allthings.how |

## Cost estimate (per pilot run)

| Item | Cost |
|------|------|
| First 3 runs (Pro/Max) | $0 (free, non-refreshing) |
| Run 4+ (per run) | $5-$20 |
| Time per run | 5-10 min (wall clock) |
| Prerequisites | Claude.ai login, extra-usage enabled |

**Odhadovaný pilot cost** (3 commits × 2 skills): pokud jsou 3 free runs spent → $15-$60.

## Target commit analysis (prepared but not run)

Největší pro multi-file review: **`2c0b222`** (Guardian L1).

| Commit | Files | +Lines | -Lines | Multi-file? |
|--------|-------|--------|--------|-------------|
| eb46f59 Guardian L2 | 4 | 362 | 2 | ano (hook + test + sh + json) |
| **2c0b222 Guardian L1** | **4** | **737** | **94** | **ano, největší** |
| 85db323 gitignore | 7 | 8 | 1377 | deletion-heavy, málo nového kódu |

## Proč zastaveno

1. **Subscription gate** — harness neví, zda uživatel má Pro/Max a kolik free runs zbývá. Utrácení $ je nevratná akce, vyžaduje explicit consent.
2. **Cloud-only** — výstup závisí na Anthropic sandbox, not reproducible lokálně.
3. **Skill not loaded** — v této session není `/ultrareview` v available-skills. Slash commands se v CC neinvokují přes bash, jdou přes harness skill router.
4. **Premature measurement** — srovnání `/critic` (local, free, ~1 min) vs `/ultrareview` (cloud, paid, 5-10 min) je jinak asymetrické; smysl má až po rozhodnutí o cost tier acceptance.

## Co by pilot vyžadoval (pro budoucí re-run)

- [ ] Potvrdit Pro/Max plan + extra-usage enabled na účtu stockl.pavel@gmail.com
- [ ] Upgradovat CC na v2.1.111+ (check `claude --version`)
- [ ] Přidat `/ultrareview` do available-skills / invoke z interactive CC shellu mimo tento harness
- [ ] Budget approval na ~$15-$60 pro 6 runs (3 commits × 2 skills)
- [ ] Alt: pilot jen na 1 commit (`2c0b222`) → 1× free run, $0 cost if within quota

## Doporučení

**Light alternative bez cloud cost:**
Místo `/ultrareview` pilotovat `/review` (free, local, built-in CC command podle community docs). Porovnat `/critic` vs `/review` je levnější a poskytne sample-size-1 signál před investicí do `/ultrareview`.

**Heavy alternative:**
Počkat na první skutečný high-stakes merge (velká security change, refactor kritického modulu) → použít `/ultrareview` jednou z 3 free runs, zaznamenat metriky → teprve pak vyhodnocovat integraci.

## Rozhodnutí (neblokuje pilot per se, blokuje AUTO-pilot)

Automatický pilot **nedoporučuji**. Cost + cloud dependency + session mismatch = signifikantní overhead bez jasného ROI oproti existujícímu `/critic`.

Pokud uživatel explicitně schválí spend: re-open tento report, spustit `/ultrareview 2c0b222` v interactive CC (ne v této session), přenést metriky.

---

*Source verification via WebFetch (GitHub CHANGELOG) + WebSearch (6 independent reviews). No pilot runs executed.*

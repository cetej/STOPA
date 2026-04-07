---
name: Verifier Divergence
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-implementation-plan]
tags: [code-quality, review, orchestration]
---

# Verifier Divergence

> Jev kdy verifier/critic modul optimalizuje vlastní proxy metriky namísto skutečné user satisfaction — způsobuje degradaci celkového systémového výkonu.

## Key Facts

- NLAH verifier způsobil -0.8% na SWE-bench — příčina: "local success differs from evaluator alignment" (ref: sources/nlah-implementation-plan.md)
- Mechanismus: verifier maximalizuje "code quality score" místo "user task satisfaction" (ref: sources/nlah-implementation-plan.md)
- STOPA `/critic` má anti-divergence mechanismy: milestone-driven, dynamic verifier override, anti-leniency (ref: sources/nlah-implementation-plan.md)
- Identifikované mezery: žádný feedback loop, žádná proxy metric detection, žádný verifier-user alignment check (ref: sources/nlah-implementation-plan.md)
- Detekce přes Critic Accuracy Ledger: implicit signal — commit po PASS = aligned, commit po FAIL = overridden (ref: sources/nlah-implementation-plan.md)
- Alignment rate cíl: >85% po 50 verdiktech; pod 80% → varování a návrh úpravy critic vah (ref: sources/nlah-implementation-plan.md)

## Relevance to STOPA

Varování pro `/critic` design. STOPA má lepší základ než NLAH verifier, ale chybí zpětná vazba. Critic Accuracy Ledger je P2 priorita (4h).

## Mentioned In

- [NLAH Implementation Plan](../sources/nlah-implementation-plan.md)

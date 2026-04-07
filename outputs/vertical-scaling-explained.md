# Vertikální škálování orchestrace — Co to je a jak to funguje

## Problém jednou větou

Současný systém má experty na různé úkoly (scout, critic, worker), ale žádný z nich nevidí, jak jeho práce ovlivňuje ostatní úrovně projektu. Je to jako mít skvělého zedníka, elektrikáře a instalatéra — ale nikdo nekontroluje, jestli se jejich práce nepotkává ve stejné zdi.

## Tři úrovně abstrakce

```
┌─────────────────────────────────────────────┐
│  MAKRO — Celý projekt                       │
│  "Jak spolu fungují všechny části?"          │
│  Architektura, business pravidla, ADR        │
│                                              │
│  ┌───────────────────────────────────────┐   │
│  │  MEZO — Modul / API kontrakt          │   │
│  │  "Jak spolu mluví dvě komponenty?"    │   │
│  │  Importy, rozhraní, testy             │   │
│  │                                       │   │
│  │  ┌───────────────────────────────┐    │   │
│  │  │  MIKRO — Řádek kódu           │    │   │
│  │  │  "Je tenhle kód správně?"      │    │   │
│  │  │  Syntax, logika, edge cases    │    │   │
│  │  └───────────────────────────────┘    │   │
│  └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

Každá úroveň odpovídá na jinou otázku:

| Úroveň | Otázka | Co se zkoumá |
|---------|--------|-------------|
| **Mikro** | "Je ten kód správně?" | Řádky, funkce, proměnné, edge cases |
| **Mezo** | "Jak spolu mluví moduly?" | API kontrakty, importy, závislosti, testy |
| **Makro** | "Je to v souladu s celkem?" | Architektura, business pravidla, rozhodnutí |

## Konkrétní příklad: Přidání logout endpointu

Představ si webovou aplikaci s autentizací. Vývojář dostane úkol: **"Přidej endpoint POST /api/logout."**

### Bez vertikálního škálování (současný stav)

```
Orchestrátor:
  "Přidej POST /api/logout do auth modulu."
    ↓
Scout: "Našel jsem auth/routes.ts, auth/middleware.ts, tests/auth.test.ts"
    ↓
Worker: Přidá endpoint do auth/routes.ts:
  - Smaže session token z cookie
  - Vrátí 200 OK
    ↓
Critic: "Kód je syntakticky správný, endpoint funguje. PASS."
    ↓
✅ Hotovo... ale je to opravdu OK?
```

**Co nikdo nezkontroloval:**

- **Mezo úroveň:** Auth modul používá JWT tokeny — ale logout endpoint maže *cookie*, ne *token*. Token zůstává validní do expirace. Jiné moduly (`api/payments.ts`, `api/admin.ts`) ten token stále přijímají.

- **Makro úroveň:** V `docs/decisions.md` (ADR-007) stojí: *"Systém používá stateless autentizaci — server neuchovává session state."* Logout endpoint, který maže server-side session, **porušuje toto architektonické rozhodnutí**.

### S vertikálním škálováním

```
Orchestrátor:
  "Přidej POST /api/logout do auth modulu."
    ↓
Scout (3-level output):
  MAKRO: "Architektura = stateless JWT auth (viz ADR-007).
          Business rule: žádný server-side session state."
  MEZO:  "Auth modul exportuje validateToken(), refreshToken().
          Závislosti: payments, admin, notifications — všechny
          volají validateToken() pro ověření requestů."
  MIKRO: "auth/routes.ts — 4 endpointy, auth/middleware.ts —
          JWT validace s RS256, expiry 15 min."
    ↓
Orchestrátor (cross-level check):
  ⚠️ CONFLICT: Logout vyžaduje invalidaci tokenu,
     ale ADR-007 říká "stateless" = žádná server-side blacklist.
  ⚠️ DEPENDENCY: 3 moduly závisí na validateToken() —
     změna v auth ovlivní payments, admin, notifications.

  Rozhodnutí: PŘED implementací vyřešit architektonický
  konflikt. Nabídnout uživateli 2 varianty:
    A) Token blacklist (porušuje ADR-007, nutno aktualizovat)
    B) Short-lived tokens + refresh rotation (zachová stateless)
    ↓
Worker: Implementuje zvolenou variantu S VĚDOMÍM
  mezo závislostí (payments, admin, notifications).
    ↓
Critic (level-aware):
  MIKRO: "Kód správný, edge cases ošetřeny." ✅
  MEZO:  "validateToken() aktualizován, závislé
          moduly neporušeny, testy projdou." ✅
  MAKRO: "ADR-007 aktualizován, architektura
          konzistentní." ✅
    ↓
✅ Hotovo — a tentokrát opravdu.
```

## Co je klíčové

Vertikální škálování není o tom dělat *víc práce*. Je to o tom dělat **informovanější rozhodnutí** — protože agent na mikro úrovni ví, jaké jsou mezo kontrakty, a agent na mezo úrovni ví, jaký je makro záměr.

### Tři typy problémů, které to zachytí

**1. Vertikální nekonzistence**
Mikro-rozhodnutí porušuje makro-pravidlo.
*Příklad:* Přidáš caching do API handleru (mikro: výkon +), ale architektura říká "žádný shared state" (makro: ✗).

**2. Bottleneck na mezo úrovni**
Rozhraní mezi moduly je nejslabší článek.
*Příklad:* Auth modul má čistou implementaci (mikro: ✓) a projekt má jasnou architekturu (makro: ✓), ale API kontrakt mezi auth a payments je křehký — změna v jednom rozbije druhý.

**3. Emergence**
Nevinné mikro-změny vytvářejí systémový problém.
*Příklad:* Každý modul přidá svůj logger (mikro: rozumné). Na makro úrovni vznikne 5 různých logovacích knihoven, 3 formáty logů, a monitoring je nemožný.

## Jak to ovlivní běžnou práci

| Aspekt | Dnes | S vertikálním škálováním |
|--------|------|--------------------------|
| Scout output | Flat seznam souborů | 3-level hierarchie (makro→mezo→mikro) |
| Orchestrátor | Dekomponuje úkol na subtasky | Taguje subtasky abstrakční úrovní + kontroluje cross-level |
| Critic | Kontroluje kód | Kontroluje kód + kontrakty + architekturu |
| Chybné plány | Odhaleny při implementaci (draho) | Odhaleny při plánování (levně) |
| Tokeny | Baseline | +0% (fáze A), +10-20% (fáze B), +25-40% (fáze C) |

## Fáze nasazení

```
Fáze A (teď):     Scout produkuje 3-level output
                   → Agent vidí kontext, ale nerozhoduje

Fáze B (za 2 tý):  /telescope skill explicitně kontroluje
                   cross-level konzistenci
                   → Systém aktivně hledá konflikty

Fáze C (za 6 tý):  Orchestrace integruje vertikální
                   povědomí do celého workflow
                   → Každý subtask má level tag,
                     cross-level critic je default
```

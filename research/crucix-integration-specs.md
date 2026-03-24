# Crucix — Integrační zadání pro NGM projekty

Datum: 2026-03-21
Zdroj: https://github.com/calesthio/Crucix (AGPL v3, Node.js 22+, ESM)

---

## 1. ZÁCHVĚV × Crucix — Geopolitický kontext pro detekci kaskád

### Motivace

Záchvěv detekuje názorové kaskády na Redditu, ale pracuje v izolaci — neví, CO kaskádu spustilo. Crucix monitoruje 27 real-time zdrojů (konflikty, komodity, sankce, satelitní data). Propojením získáme **kauzální kontext**: "CRI roste, protože včera eskalovalo X v regionu Y."

### Architektura integrace

```
Crucix sweep (15 min)
    ↓ runs/latest.json
    ↓
crucix_bridge.py  ←── nový modul v zachvev/ingest/
    ↓ parse + filtruj relevantní signály
    ↓
GeopoliticalContext (dataclass)
    ↓
interpreter.py ←── rozšíření compute_narrative_pillar()
    ↓
CRI s kontextem  →  "CRI 0.62 — koreluje s eskalací v Íránu (1462 termálních detekcí)"
```

### Konkrétní kroky

#### Krok 1: Crucix jako sidecar služba

Crucix běží jako Node.js server na `localhost:3117`. Sweep data jsou dostupná přes SSE nebo přímo z `runs/latest.json`.

```python
# zachvev/ingest/crucix_bridge.py

import json
import httpx
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class GeopoliticalSignal:
    source: str          # "firms", "opensky", "acled", "fred"
    category: str        # "conflict", "economic", "sanctions", "humanitarian"
    severity: str        # "flash", "priority", "routine"
    summary: str         # plain-text popis
    region: str | None   # geografická oblast
    value: float | None  # numerická hodnota (thermal count, yield spread...)
    timestamp: str       # ISO datetime

@dataclass
class GeopoliticalContext:
    signals: list[GeopoliticalSignal] = field(default_factory=list)
    conflict_zones: list[dict] = field(default_factory=list)
    economic_stress: dict = field(default_factory=dict)  # yield curve, VIX, oil
    sweep_timestamp: str = ""

    @property
    def tension_score(self) -> float:
        """0-1 skóre globálního napětí z Crucix signálů."""
        weights = {"flash": 1.0, "priority": 0.6, "routine": 0.2}
        if not self.signals:
            return 0.0
        total = sum(weights.get(s.severity, 0.1) for s in self.signals)
        return min(total / 10.0, 1.0)  # normalizace
```

#### Krok 2: Rozšíření CRI o geopolitický kontext

Současný CRI: `0.4 × temporal + 0.3 × structural + 0.3 × narrative`

Nový CRI s kontextem (váhy zachovány, kontext je **modifikátor**, ne 4. pilíř):

```python
# interpreter.py — rozšíření

def compute_cri_with_context(
    daily_sentiment, topic_result, texts, geo_context: GeopoliticalContext | None
) -> dict:
    base_cri = compute_cri(daily_sentiment, topic_result, texts)

    if geo_context is None:
        return base_cri

    # Geopolitický kontext zvyšuje CRI pokud:
    # 1. Témata v clusteru korelují s aktivními konflikty
    # 2. Ekonomický stres (VIX > 25, oil spike) zvyšuje citlivost
    context_modifier = _compute_context_modifier(base_cri, geo_context)

    adjusted = base_cri.copy()
    adjusted["cri"] = min(base_cri["cri"] * (1 + context_modifier), 1.0)
    adjusted["geo_context"] = {
        "tension_score": geo_context.tension_score,
        "active_conflicts": len(geo_context.conflict_zones),
        "economic_stress": geo_context.economic_stress,
        "modifier_applied": context_modifier,
    }
    return adjusted
```

#### Krok 3: Interpretace s kontextem

```python
# interpreter.py — rozšíření interpret_situation()

def _format_geo_context(geo: GeopoliticalContext) -> str:
    """Přidá geopolitický kontext do situation reportu."""
    if not geo.signals:
        return ""

    lines = ["\n### Geopolitický kontext (Crucix)\n"]

    flash = [s for s in geo.signals if s.severity == "flash"]
    if flash:
        lines.append("**FLASH signály:**")
        for s in flash:
            lines.append(f"- [{s.source}] {s.summary}")

    if geo.economic_stress:
        vix = geo.economic_stress.get("vix")
        oil = geo.economic_stress.get("crude_oil")
        if vix and vix > 25:
            lines.append(f"- Zvýšená tržní volatilita (VIX {vix:.1f})")
        if oil and oil > 90:
            lines.append(f"- Ropa nad $90/bbl ({oil:.1f}) — potenciální tlak na veřejný sentiment")

    return "\n".join(lines)
```

#### Krok 4: API endpoint

```python
# api/app.py — nový endpoint

@app.get("/api/geo-context")
async def get_geo_context():
    """Vrátí aktuální geopolitický kontext z Crucix."""
    from zachvev.ingest.crucix_bridge import fetch_crucix_context
    ctx = await fetch_crucix_context()
    return {"tension_score": ctx.tension_score, "signals": len(ctx.signals), ...}
```

#### Krok 5: UI integrace

V Streamlit UI přidat do tabu "Analýza":
- Indikátor globálního napětí (tension_score) jako gauge/color bar
- Kolapsibilní sekce "Geopolitický kontext" pod situation reportem
- Korelační poznámka u CRI: "CRI upraveno o +0.08 na základě geopolitického kontextu"

### Datové zdroje z Crucix relevantní pro Záchvěv

| Crucix zdroj | Relevance pro Záchvěv | Jak použít |
|---|---|---|
| ACLED (konflikty) | Přímá — konflikty spouštějí diskuze | Korelace s emerging topics |
| FIRMS (termální detekce) | Nepřímá — indikátor eskalace | Tension score modifikátor |
| FRED/BLS (makro) | Střední — ekonomický stres ovlivňuje sentiment | Economic stress v kontextu |
| Reddit/Bluesky sentiment | Doplňková — širší sentiment | Cross-platform validace |
| Telegram OSINT | Doplňková — early warning | Další zdroj pro emerging topics |
| Sanctions/WHO | Situační — specifické události | Trigger detection |

### Priorita a effort

| Fáze | Co | Effort | Přínos |
|---|---|---|---|
| MVP | crucix_bridge.py + tension_score v UI | 1 session | Vizuální kontext |
| V2 | CRI context modifier + korelace | 2 sessions | Kauzální vysvětlení |
| V3 | Cross-platform topic matching (Crucix Reddit ↔ Záchvěv Reddit) | 2 sessions | Multi-source validace |

### Prerekvizity

1. Crucix musí běžet jako sidecar (`npm run dev` na localhost:3117)
2. `.env` s minimálně FIRMS_MAP_KEY a FRED_API_KEY (free)
3. Python `httpx` dependency v Záchvěv

---

## 2. NG-ROBOT × Crucix — Geopolitický kontext pro editorial

### Motivace

NG-ROBOT zpracovává články National Geographic — science, příroda, geografie. Crucix může poskytnout:
1. **Aktuálnost kontextu** — u článků o regionech doplnit aktuální situaci
2. **Editorial prioritizaci** — preferovat články o oblastech s vysokou aktivitou
3. **Science Monitor enrichment** — doplnit science kandidáty o geopolitický kontext
4. **Faktuální podklad** — aktuální data (ceny komodit, environmentální data) pro fact-check

### Architektura integrace

```
Crucix sweep (15 min)
    ↓ runs/latest.json
    ↓
crucix_context.py  ←── nový modul v NG-ROBOT root
    ↓
┌──────────────────────────────────────────────────┐
│  3 integrační body:                              │
│                                                  │
│  A) Phase 0 (Analysis) — region tagging          │
│     "článek se týká Íránu → Crucix: 1462 fires"  │
│                                                  │
│  B) Phase 4 (Fact Check) — aktuální data         │
│     "ověř cenu ropy" → Crucix: $98.5/bbl         │
│                                                  │
│  C) Science Monitor — prioritizace               │
│     kandidát o vulkánech → FIRMS: aktivita ↑     │
└──────────────────────────────────────────────────┘
```

### Konkrétní kroky

#### A) Kontextové obohacení článků (Phase 0 enrichment)

```python
# crucix_context.py

import json
import httpx
from pathlib import Path

CRUCIX_URL = "http://localhost:3117"
CRUCIX_DATA = Path("../CRUCIX/runs/latest.json")  # fallback: přímý soubor

REGION_KEYWORDS = {
    "middle_east": ["iran", "iraq", "syria", "yemen", "israel", "gaza", "lebanon"],
    "ukraine": ["ukraine", "russia", "crimea", "donbas", "kyiv"],
    "east_asia": ["china", "taiwan", "korea", "japan", "south china sea"],
    "africa": ["sahel", "sudan", "ethiopia", "congo", "nigeria"],
    # ...
}

class CrucixContext:
    def __init__(self):
        self._cache = None
        self._cache_time = None

    def get_context_for_article(self, analysis_json: dict) -> dict | None:
        """Na základě Phase 0 analýzy vrátí relevantní Crucix kontext."""
        sweep = self._get_latest_sweep()
        if not sweep:
            return None

        # Extrahuj regiony z article analysis
        regions = self._detect_regions(analysis_json)
        if not regions:
            return None

        # Filtruj Crucix data pro relevantní regiony
        relevant = self._filter_by_regions(sweep, regions)
        return {
            "regions": regions,
            "signals": relevant,
            "summary": self._summarize(relevant),
            "editorial_note": self._editorial_note(relevant),
        }

    def _editorial_note(self, signals: list) -> str:
        """Generuje poznámku pro editora."""
        if not signals:
            return ""
        flash = [s for s in signals if s.get("severity") == "flash"]
        if flash:
            return (
                "⚠ AKTUÁLNÍ KONTEXT: Region článku má aktivní "
                f"FLASH signály ({len(flash)}). Zvažte aktualizaci "
                "nebo redakční poznámku o současné situaci."
            )
        return f"ℹ Region článku: {len(signals)} aktivních signálů v Crucix monitoringu."
```

#### B) Fact-check enrichment (Phase 4)

Přidat do Phase 4 promptu kontext z Crucix pro ověřitelná fakta:

```python
# claude_processor.py — rozšíření phase_4_fact_check

def _get_crucix_facts(self) -> str:
    """Získá aktuální fakta z Crucix pro fact-check."""
    ctx = CrucixContext()
    sweep = ctx._get_latest_sweep()
    if not sweep:
        return ""

    facts = []
    # Ekonomická data
    econ = sweep.get("economic", {})
    if econ:
        facts.append(f"Ropa Brent: ${econ.get('crude_oil', 'N/A')}/bbl")
        facts.append(f"Zlato: ${econ.get('gold', 'N/A')}/oz")
        facts.append(f"VIX: {econ.get('vix', 'N/A')}")
        facts.append(f"Fed sazba: {econ.get('fed_rate', 'N/A')}%")

    return "\n".join(facts) if facts else ""
```

#### C) Science Monitor prioritizace

```python
# science_monitor.py — rozšíření score_candidate()

def _crucix_relevance_boost(self, candidate: dict) -> float:
    """Zvýší skóre kandidáta pokud se týká oblasti s aktivitou v Crucix."""
    ctx = CrucixContext()
    context = ctx.get_context_for_article({"text": candidate.get("title", "")})
    if not context:
        return 0.0

    n_signals = len(context.get("signals", []))
    # Až +20% boost pro vysoce aktuální témata
    return min(n_signals * 0.02, 0.20)
```

### Integrace do Web UI (ngrobot_web.py)

Nový widget na dashboardu:

```python
# blueprints/system_routes.py — nový endpoint

@system_bp.route("/api/crucix-status")
def crucix_status():
    """Vrátí aktuální stav Crucix pro dashboard widget."""
    ctx = CrucixContext()
    sweep = ctx._get_latest_sweep()
    if not sweep:
        return jsonify({"available": False})
    return jsonify({
        "available": True,
        "sweep_time": sweep.get("timestamp"),
        "flash_alerts": len([...]),
        "tension_regions": [...],
    })
```

Dashboard zobrazí:
- Status badge "Crucix: ONLINE/OFFLINE"
- Počet FLASH alertů
- Při zpracování článku: kontextová lišta s relevantními signály

### Priorita a effort

| Fáze | Co | Effort | Přínos |
|---|---|---|---|
| MVP | crucix_context.py + dashboard widget | 1 session | Viditelnost aktuálního dění |
| V2 | Phase 0 region enrichment + editorial notes | 1 session | Kontext u článků |
| V3 | Phase 4 fact data + Science Monitor boost | 1 session | Faktická přesnost + relevance |

### Prerekvizity

Stejné jako Záchvěv — Crucix sidecar na localhost:3117.

---

## 3. CRUCIX-CZ — Samostatný geopolitický monitoring pro české prostředí

### Motivace

Crucix je skvělý nástroj, ale:
1. Zaměřený na US trhy a globální OSINT — chybí **český/CE kontext**
2. Nemá české zdroje (ČTK, iROZHLAS, NÚKIB, ČHMÚ, ČNB)
3. UI je anglicky, metriky jsou US-centric (FRED, BLS, USAspending)
4. Chybí **narativní analýza** — jen agregace, ne interpretace trendu

### Vize: CRUCIX-CZ

Fork/rozšíření Crucixu o české a středoevropské zdroje s narativní vrstvou. Kombinace Crucix infrastruktury + Záchvěv analytiky.

### Architektura

```
CRUCIX-CZ/
├── apis/
│   ├── sources/              # Originální Crucix zdroje (27)
│   │   ├── firms.mjs
│   │   ├── opensky.mjs
│   │   ├── fred.mjs
│   │   └── ...
│   ├── sources-cz/           # Nové české zdroje
│   │   ├── ctk.mjs           # ČTK RSS feed
│   │   ├── irozhlas.mjs      # iROZHLAS.cz RSS + Radiožurnál
│   │   ├── nukib.mjs         # NÚKIB bezpečnostní varování
│   │   ├── chmú.mjs          # ČHMÚ výstrahy (meteo, hydro)
│   │   ├── cnb.mjs           # ČNB kurzy, sazby, finanční stabilita
│   │   ├── czso.mjs          # ČSÚ (inflace, HDP, nezaměstnanost)
│   │   ├── ceska-energie.mjs # OTE denní trh s elektřinou
│   │   ├── twitter-cz.mjs    # Bluesky/X CZ political accounts
│   │   ├── reddit-cz.mjs     # r/czech, r/praha
│   │   └── desinformace.mjs  # Manipulátoři.cz, Nelež.cz feeds
│   └── briefing.mjs          # Orchestrátor (rozšířený)
├── lib/
│   ├── llm/                  # Crucix LLM abstrakce (beze změn)
│   ├── narrative/            # NOVÉ — narativní analýza
│   │   ├── sentiment-cz.mjs  # České sentiment signály
│   │   ├── cascade.mjs       # Zjednodušený CRI z Záchvěv
│   │   └── framing.mjs       # Framing detection (z Záchvěv narrative markers)
│   ├── delta/                # Crucix delta engine (beze změn)
│   └── alerts/               # Crucix alerts + české kanály
│       ├── telegram.mjs      # Beze změn
│       ├── discord.mjs       # Beze změn
│       └── signal-cz.mjs     # Signal messenger (populárnější v CZ)
├── dashboard/
│   ├── jarvis.html           # Originální Crucix dashboard
│   └── jarvis-cz.html        # České rozšíření
│       # Přidáno:
│       # - CZ mapa (místo US-centric zobrazení)
│       # - ČNB kurzy widget
│       # - ČHMÚ výstrahy overlay
│       # - Narativní heat-map (z cascade.mjs)
│       # - České texty v UI
├── runs/                     # Sweep data
└── crucix.config.mjs         # Rozšířená konfigurace
```

### České datové zdroje — specifikace

| Zdroj | Typ | URL/API | Auth | Interval | Data |
|---|---|---|---|---|---|
| **ČTK** | RSS | `https://www.ctk.cz/rss/` | Free | 15 min | Titulky, kategorie |
| **iROZHLAS** | RSS | `https://www.irozhlas.cz/rss` | Free | 15 min | Články, rubriky |
| **NÚKIB** | RSS/Web | `https://nukib.gov.cz/` | Free | 1 hod | Bezpečnostní varování |
| **ČHMÚ** | API/RSS | `https://www.chmi.cz/` | Free | 30 min | Meteo výstrahy, hydro |
| **ČNB** | API | `https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt` | Free | 1× denně | Kurzy, sazby |
| **ČSÚ** | API | `https://vdb.czso.cz/pll/eweb/` | Free | 1× týdně | Inflace, HDP, nezam. |
| **OTE** | Web/API | `https://www.ote-cr.cz/` | Free | 1 hod | Cena elektřiny, plynu |
| **Manipulátoři.cz** | RSS | `https://manipulatori.cz/feed/` | Free | 1 hod | Dezinformační články |
| **Reddit CZ** | Arctic Shift | Stávající Záchvěv kód | Free | 15 min | r/czech, r/praha |

### Narativní vrstva (z Záchvěv)

Klíčový differentiátor oproti vanilla Crucix — ne jen "co se děje", ale "jak se o tom mluví":

```javascript
// lib/narrative/cascade.mjs

export function computeSimplifiedCRI(redditData, newsData) {
    // Zjednodušená verze Záchvěv CRI pro real-time dashboard
    const sentimentTrend = computeSentimentTrend(redditData);  // temporal
    const topicConcentration = computeConcentration(redditData); // structural
    const narrativeMarkers = detectCzechMarkers(redditData);     // narrative

    return {
        cri: 0.4 * sentimentTrend + 0.3 * topicConcentration + 0.3 * narrativeMarkers,
        alert_level: cri > 0.7 ? "KRITICKÝ" : cri > 0.5 ? "PREKRITICKÝ" : "KLID",
        dominant_narrative: identifyDominantFrame(redditData),
    };
}
```

Dashboard zobrazí narativní heat-mapu: které české téma má nejvyšší kaskádový potenciál.

### UI rozšíření (jarvis-cz.html)

```
┌─────────────────────────────────────────────────────────┐
│  CRUCIX-CZ Intelligence Terminal           🟢 SWEEP OK  │
├──────────────┬──────────────────────────────────────────┤
│              │  ┌─────────┐  ┌─────────┐  ┌──────────┐ │
│   3D Globe   │  │ ČNB     │  │ ČHMÚ    │  │ Energie  │ │
│   + CZ heat  │  │ EUR 25.2│  │ ⚠ Vítr  │  │ 89€/MWh  │ │
│   overlay    │  │ USD 23.1│  │ Morava  │  │ ↑12%     │ │
│              │  └─────────┘  └─────────┘  └──────────┘ │
├──────────────┼──────────────────────────────────────────┤
│  Narativní   │  📰 ČTK / iROZHLAS feed                 │
│  heat-mapa   │  ─────────────────────                   │
│              │  • Vláda schválila... (3 min ago)         │
│  r/czech     │  • NÚKIB varuje...   (15 min ago)        │
│  ████░░ 0.42 │  • ČNB ponechala...  (2 hod ago)         │
│              │                                          │
│  migrace     │  🎯 AI Trading Ideas (CZ kontext)        │
│  ██████ 0.71 │  ─────────────────────                   │
│  ⚠ PREKRIT.  │  LONG CZK/EUR — ČNB hawkish signal...   │
│              │  SHORT CEZ — energy price pressure...     │
├──────────────┴──────────────────────────────────────────┤
│  FLASH: NÚKIB — kybernetický incident [kategorie 2]     │
└─────────────────────────────────────────────────────────┘
```

### Implementační plán

| Fáze | Co | Effort | Výstup |
|---|---|---|---|
| **F0: Fork + CZ skeleton** | Fork Crucix, přidat sources-cz/ strukturu, ČNB + ČHMÚ jako první zdroje | 1 session | Běžící dashboard s 27 + 2 zdroji |
| **F1: České zpravodajství** | ČTK, iROZHLAS, NÚKIB RSS parsery | 1 session | Český news feed v dashboardu |
| **F2: Ekonomika CZ** | ČSÚ, OTE, ČNB rozšíření (sazby, finanční stabilita) | 1 session | CZ makro widget |
| **F3: Narativní vrstva** | Port Záchvěv CRI do JS, Reddit CZ integrace, heat-mapa | 2 sessions | Narativní monitoring |
| **F4: UI lokalizace** | jarvis-cz.html, české texty, CZ mapa overlay, layout | 1 session | Plně český dashboard |
| **F5: Alerty CZ** | Signal messenger, české Telegram kanály, české alert texty | 1 session | CZ notifikace |

**Celkem: ~7 sessions**

### Technické rozhodnutí

| Otázka | Rozhodnutí | Proč |
|---|---|---|
| Fork vs. plugin? | **Fork** — příliš mnoho změn pro plugin | UI lokalizace + nové zdroje + narativní vrstva |
| JS vs. Python narativní vrstva? | **JS** (port z Python) | Zachovat single-stack (Node.js), Crucix je celý ESM |
| Sentiment model? | **API call na Záchvěv** nebo lightweight JS model | Nechceme Python dependency v Node projektu |
| Kde hostovat? | **Lokálně** (jako Crucix) nebo Railway | Self-hosted = žádné náklady, žádná telemetrie |

### Synergie mezi projekty

```
                    CRUCIX-CZ
                   /         \
    geopolitický kontext    narativní engine
         ↓                      ↑
     NG-ROBOT                ZÁCHVĚV
  (editorial context)    (CRI, sentiment, clustering)
```

- **CRUCIX-CZ → NG-ROBOT**: geopolitický kontext pro články (integrace #2)
- **ZÁCHVĚV → CRUCIX-CZ**: narativní analýza, CRI, sentiment model
- **CRUCIX-CZ → ZÁCHVĚV**: multi-source signály, trigger detection
- Všechny tři projekty sdílí data přes localhost API calls

---

## Souhrn — co dělat jako první

| # | Projekt | Akce | Effort | Impact |
|---|---|---|---|---|
| 1 | **ZÁCHVĚV** | `crucix_bridge.py` + tension_score v UI | 1 session | Vysoký — kontext pro CRI |
| 2 | **NG-ROBOT** | `crucix_context.py` + dashboard widget | 1 session | Střední — editorial awareness |
| 3 | **CRUCIX-CZ** | Fork + F0 (skeleton + ČNB/ČHMÚ) | 1 session | Základ pro vše |

**Doporučený postup**: Začít s #3 (fork), pak #1 (Záchvěv bridge — využije běžící Crucix), pak #2 (NG-ROBOT — nejméně urgentní).

**Prerekvizita pro všechny**: Naklonovat Crucix, rozběhnout lokálně, ověřit sweep.

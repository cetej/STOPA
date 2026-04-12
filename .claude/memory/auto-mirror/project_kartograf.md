---
name: project_kartograf
description: KARTOGRAF — web-first cartographic map generator from public geodata (Copernicus DEM, Natural Earth, OSM)
type: project
---

KARTOGRAF je samostatný projekt pro generování kartografických map z veřejných geodat.

**Lokace:** `C:\Users\stock\Documents\000_NGM\KARTOGRAF`
**Repo:** lokální git, zatím ne na GitHubu

## Stav (2026-03-25)

Phase 1 ✅ CLI pipeline (bbox → DEM → hillshade → hypsometric → PNG)
Phase 4 ✅ MapLibre web viewer (MVP)

### Phase 4 — Web Viewer
- `kartograf serve --preset krkonose` → 3D interaktivní mapa v browseru
- Lokální tile server (stdlib http.server, terrain-RGB + color tiles)
- MapLibre GL JS s 3D terrain, hillshade, hypsometric tinting
- Style switcher (NatGeo / Swiss Topo) — funguje
- Exaggeration slider, hillshade opacity, zoom/rotate/tilt
- DEM se stahuje s paddingem 0.3° pro hladké okraje
- Known issue: stripy artefakt na vzdálených okrajích DEM pokrytí

Testováno: Krkonoše (NatGeo + Swiss), Tatry, Dolomity

## Prioritní výstup

- **Web-first** (MapLibre GL, interaktivní) — hlavní use case ✅ MVP
- **Tisk sekundární** (PDF/SVG přes QGIS)

## Stack

Python 3.11+, rasterio (GDAL), matplotlib, click, numpy, Pillow
MapLibre GL JS 4.7.1 (CDN)
Data: Copernicus DEM GLO-30 (AWS), Natural Earth, OSM

## Další kroky

1. Style presets — NG paleta + fonty (fonty z NG-ROBOT)
2. Vektorové vrstvy — řeky, hranice, města, labeling
3. Print export — PDF/SVG, CMYK konverze
4. Edge artifact fix — MapTiler fallback pro oblasti mimo lokální DEM

## Frontend tooling

- **Pretext** (`npm install @chenglou/pretext`, github.com/chenglou/pretext) — pure TypeScript text measurement bez DOM reflow. Měří přes canvas `measureText`, layout čistou aritmetikou (0.09ms/500 textů). Umožňuje text obtékající libovolné tvary, columnový layout, 120fps. Autor: chenglou (React core, Midjourney). Relevantní pro **map labeling** — přesné umístění názvů měst/hor bez CSS reflow artefaktů.
  - **Integrace s MapLibre:** `prepareWithSegments()` per label → `layoutWithLines()` → render do `OffscreenCanvas` → texture → WebGL sprite. Cache prepared labels per session, re-layout jen při změně fontu/zoom. Viz `reference_web_frontend.md` pro kompletní API.
  - **Konkrétní use cases v mapách:** výškové přizpůsobení labelů bez reflow při pan/zoom; `layoutNextLine()` s proměnnou šířkou pro text obtékající ikony; bidi support pro vícejazyčné mapy; ~0.09ms/label → škáluje na tisíce labelů.

## Souvislosti

- NG-ROBOT má NG style book + fonty — použít přímo
- NG-ROBOT pracuje na počešťování map — komplementární modul

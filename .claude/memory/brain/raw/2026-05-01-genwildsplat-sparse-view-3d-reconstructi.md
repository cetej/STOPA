---
title: GenWildSplat: Generalizovatelná 3D rekonstrukce z řídkých nepřipravených obrázků
url: http://arxiv.org/abs/2604.28193v1
date: 2026-05-01
concepts: ["3D rekonstrukce", "sparse-view reconstruction", "3D Gaussian Splatting", "feed-forward neural network", "appearance adaptation", "curriculum learning", "generalizace na reálná data"]
entities: ["Vinayak Gupta", "Chih-Hao Lin", "Shenlong Wang", "Anand Bhattad", "Jia-Bin Huang", "PhotoTourism dataset", "MegaScenes benchmark"]
source: brain-ingest-local
---

# GenWildSplat: Generalizovatelná 3D rekonstrukce z řídkých nepřipravených obrázků

**URL**: http://arxiv.org/abs/2604.28193v1

## Key Idea

GenWildSplat je feed-forward framework pro 3D rekonstrukci venkovních scén z řídkých, nepozovaných obrázků bez nutnosti optimalizace pro každou scénu zvlášť. Využívá naučené geometrické priory a adaptér vzhledu pro zvládnutí různých světelných podmínek a přechodných objektů.

## Claims

- GenWildSplat dosahuje state-of-the-art výsledků ve feed-forward renderování bez optimalizace v testovacím čase
- Metoda generalizuje napříč různými podmínkami osvětlení a okluzními vzory díky curriculum learningu na syntetických i reálných datech
- Framework umožňuje real-time inferenci z nepřipravených internetových obrázků bez per-scene optimalizace

## Relevance for STOPA

Relevantní pro STOPA v kontextu prostorového modelování a 3D rekonstrukce prostředí z nekalibrovaných dat, což může být užitečné pro orchestraci agentů v fyzickém či smíšeném prostoru.

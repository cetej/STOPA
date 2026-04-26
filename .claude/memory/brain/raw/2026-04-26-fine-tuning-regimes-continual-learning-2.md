---
title: Režimy doladění definují odlišné problémy kontinuálního učení
url: http://arxiv.org/abs/2604.21927v1
date: 2026-04-26
concepts: ["Kontinuální učení", "Fine-tuning režimy", "Trénovatelná hloubka", "Katastrofické zapomínání", "Inkrementální učení úloh"]
entities: ["Paul-Tiberiu Iordache", "Elena Burceanu"]
source: brain-ingest-local
---

# Režimy doladění definují odlišné problémy kontinuálního učení

**URL**: http://arxiv.org/abs/2604.21927v1

## Key Idea

Režim doladění (fine-tuning regime), definovaný podprostorem trénovatelných parametrů, je klíčovou proměnnou při hodnocení metod kontinuálního učení. Změna hloubky trénovatelných vrstev zásadně mění účinnost učení a zapomínání.

## Claims

- Srovnávací hodnocení metod kontinuálního učení obvykle fixují režim doladění, ačkoli tento režim je sám o sobě klíčovou evaluační proměnnou
- Relativní pořadí výkonu různých CL metod (EWC, LwF, SI, GEM) se neuchová konzistentně napříč různými režimy doladění
- Hlubší režimy adaptace jsou spojeny s většími změnami vah, vyšším zapomínáním a silnějším vztahem mezi těmito dvěma faktory
- Srovnávací závěry v kontinuálním učení silně závisí na zvoleném režimu doladění, což vyžaduje evaluační protokoly zohledňující trénovatelnou hloubku

## Relevance for STOPA

Pro STOPA orchestraci je klíčové, že různé režimy adaptace modelů vyžadují odlišné strategie pro správu učení a paměti. Orchestrace musí dynamicky přizpůsobovat své parametry podle zvoleného režimu doladění.

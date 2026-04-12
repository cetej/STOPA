---
name: feedback_zachvev_ui
description: Záchvěv UI flow — uživatel zadává úkol/téma, systém hledá relevantní data a detekuje témata automaticky
type: feedback
---

Záchvěv je **nástroj pro plnění úkolů**, ne statický monitor s fixní konfigurací.

**Why:** Uživatel opakovaně korigoval špatné pochopení flow. Záchvěv není: (a) CSV uploader, (b) "zadej subreddit" formulář, (c) statický monitor s jednou konfigurací. Je to nástroj kde uživatel zadá úkol (téma, otázku) a systém najde odpovědi.

**How to apply:**
- Hlavní vstup = ÚKOL nebo TÉMA (např. "Letná demonstrace", "migrace", "vládní krize")
- Subreddity jsou parametr úkolu, ne globální nastavení — mění se podle zadání
- Systém sám vybere relevantní zdroje pro dané téma
- Topic discovery (UMAP+HDBSCAN) najde pod-témata automaticky
- Dashboard zobrazí nalezená témata s EWS indikátory
- Uživatel si VYBERE téma pro hloubkovou analýzu + kampaň
- NIKDY nenavrhuj CSV upload jako vstup
- NIKDY nenavrhuj fixní subreddit konfiguraci jako hlavní interakci
- Subreddit je parametr, ne konfigurace

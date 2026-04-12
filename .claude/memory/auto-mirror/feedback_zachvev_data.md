---
name: feedback_zachvev_data
description: Záchvěv má testovací data v data/ — VŽDY je najdi a použij, nestahuj znovu z API
type: feedback
---

V ZACHVEV/data/ jsou uložené parquety z předchozích sessions. Klíčový soubor:
- `letna_sentiment.parquet` — 6615 postů, Feb-Mar 2026, r/czech, UŽ MÁ sentiment sloupce

**Why:** Uživatel byl frustrovaný, že UI stahuje 500 postů z API místo použití existujících 6615 Letná dat, která dávají mnohem lepší výsledky (63 témat vs 2). Navíc cílené hledání "Letná" nenašlo nic, protože stahuje nová data z API místo hledání v lokálních datech.

**How to apply:**
- Při testování VŽDY zkontroluj data/ adresář
- UI by mělo umět načíst lokální parquet (ne jen stahovat z API)
- `letna_sentiment.parquet` je zlatý standard pro testování
- Embeddings cache: `data/embeddings.npy` (6615 × 256d)
- Pokud sentiment sloupce už existují, PŘESKAKUJ sentiment analýzu (šetří minuty)

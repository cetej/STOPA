---
name: ANTHROPIC_API_KEY locations — never claim "no key available"
description: API klíč je už nakonfigurovaný v NG-ROBOT/.env a ADOBE-AUTOMAT/.env. NIKDY neříkej "SKIP kvůli chybějícímu klíči" — vždy hledej v těchto lokacích.
type: feedback
originSessionId: 57ea8e53-fe72-44e8-a188-0332b9f12df0
---
User má ANTHROPIC_API_KEY nakonfigurovaný a je dostupný v:
- `C:/Users/stock/Documents/000_NGM/NG-ROBOT/.env`
- `C:/Users/stock/Documents/000_NGM/ADOBE-AUTOMAT/.env`

Před tím než řekneš "API key není dostupný", "SKIP kvůli klíči", nebo "vyžaduje ANTHROPIC_API_KEY", VŽDY zkontroluj:
1. Environment variable `ANTHROPIC_API_KEY`
2. Lokální `.env` v aktuálním projektu
3. **NG-ROBOT/.env a ADOBE-AUTOMAT/.env** (sourozenecké projekty v 000_NGM/)
4. Pokud nový projekt potřebuje klíč, zkopíruj ho odtud do projektového .env

**Why:** User opakovaně řešil API key configuration, má ho. Když říkám "klíč chybí" nebo "SKIP", je to false claim — testy které měly proběhnout neproběhnou, dokud user manuálně klíč nepředá. To zbytečně blokuje verifikaci a frustruje (uživatel doslova: "S API klíčem mě fakt neser").

**How to apply:** Při bootstrappingu nového projektu v 000_NGM/ — sub-agent prompts MUSÍ instruovat čtení klíče z NG-ROBOT/.env, ne ze svého .env. Při Wave 4 verify pokud .env je prázdný, propish ho z NG-ROBOT před ukončením s SKIP statusem. End-to-end testy nejsou "nice to have" — dokud nejsou ověřené, projekt není done.

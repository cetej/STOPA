---
name: feedback_dont_delegate_to_user
description: Nedelegovat na uživatele tasks které Claude/agent může udělat sám — generování obsahu, shell příkazy, file operations
type: feedback
originSessionId: 816758b1-fe8e-4163-b434-f59dc70782bd
---
Nedelegovat na uživatele tasks, které agent může vykonat sám:
- Generování textového obsahu (Claude JSEM JÁ — nepiš "vygeneruj přes Claude prompt v separátní session" když to mohu napsat přímo do souboru)
- Spouštění shell příkazů (`npm install`, `curl`, `git`, atd.) — mám Bash tool
- Setup/install/build kroky — i když dlouhé, lze v background
- Vyplňování template souborů z známých dat
- File operations (write, read, edit)

**Why:** Při fragmentaci tasku mezi sebe a uživatele způsobuju zbytečnou friction. Uživatel řekl 2026-04-25: "Nevím, proč bych měl tohle dělat já. Trochu se zaratuj." Šlo o návrh, ať user spouští `npm install camofox-browser` + `curl health` + generuje content_pool.json přes "Claude prompt v separátní session" — všechno věci které mohu udělat já.

**How to apply:**
- Před delegací na uživatele se ptej: "Mohu to udělat já?" Pokud ano → udělej.
- Generování JSON/textu z prompt → Write tool přímo, ne externí session
- Shell command → Bash tool (i s `run_in_background=true` pro dlouhé operace)
- Pouze deleguj na user když potřebuje fyzickou akci (registrace na cizí službě, SMS verifikace, fyzický telefon, kupování něčeho)
- Pokud user explicitně zadá "udělej X manuálně" → respektuj. Ale defaultně předpoklad: já udělám.

**Hranice (legitimní delegace na uživatele):**
- Operace vyžadující jeho identitu (login do osobního účtu, registrace, SMS verifikace)
- Fyzický hardware (telefon, SIM karta)
- Rozhodování s tradeoffs (ne factual ale preferenční)
- Kreativní volby (jméno, persona, scope)
- Akce které vyžadují jeho fyzickou přítomnost (mobilní app login)

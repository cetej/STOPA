---
date: 2026-04-21
type: best_practice
severity: medium
component: general
tags: [czech-language, text-processing, normalization, alphabet]
summary: V české abecedě je CH samostatné písmeno (pozice mezi H a I), ne digraf C+H. Při zpracování češtiny pro jakoukoli grafémovou aplikaci (křížovky, hláskování, řazení) nikdy nerozepisovat CH na dvě písmena. Web research může tvrdit opak ("švédská křížovka rozepisuje CH") — ale to je proti jazyku, ne kvůli jazyku.
source: user_correction
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 1.00
maturity: draft
verify_check: "manual"
---

## Kontext

Při budování generátoru českých křížovek (projekt KRIZOVKA) jsem první verzi `normalize.py` udělal s parametrem `ch_as_single: bool` — default True, ale s možností přepnout na False (rozepsání CH na C+H pro údajnou "švédskou křížovku"). Tuto možnost mi přinesl web research report, který tvrdil:

> "Švédská křížovka (dominantní v běžných časopisech) — 'CH' se často rozepisuje do dvou políček (C + H), protože mřížka je hustší"

Uživatel mě opravil: **"Čeština ty moulo má písmeno CH to není C a H, to je prostě CH"**.

## Proč je to důležité

Česká abeceda má **27 písmen v grafémové podobě**:
```
A Á B C Č D Ď E É Ě F G H CH I Í J K L M N Ň O Ó P Q R Ř S Š T Ť U Ú Ů V W X Y Ý Z Ž
```

CH je:
- **Samostatné písmeno**, ne digraf
- Pozice mezi **H** a **I** (důležité pro abecední řazení)
- Jedna hláska (jedno fonéma)
- V křížovce vždy **jedno políčko**

Pokud kdokoli rozepisuje CH na dvě políčka, páchá jazykovou chybu. Bez ohledu na to, co dělají některé komerční časopisy.

## Aplikovatelnost napříč projekty

Toto pravidlo platí pro jakýkoli projekt zpracovávající češtinu:
- **ngm-terminology** — normalizace slov při matching
- **KRIZOVKA** — políčka mřížky
- **NG-ROBOT** — text processing článků (pokud by dělal fonetickou analýzu)
- **DANE** — jmenné pole v PDF (pokud se řeší po-hláskách)
- **ZACHVEV** — lexikální analýza českých textů
- jakýkoli hláskovací, řadicí nebo graphem-based nástroj

## How to apply

Při psaní funkce která "rozseká český text po písmenech":
1. Nikdy nesekej na jednotlivé Unicode znaky — musíš nejdřív identifikovat CH jako jeden prvek
2. Po `unicodedata.normalize('NFKD')` a `.upper()` je sekvence "CH" v původním slově = jedno písmeno
3. "Č" po stripnutí diakritiky = "C" (ne "CH") — CH vzniká z původního C+H, ne z Č
4. Řadící algoritmy (pokud by bylo potřeba): CH patří mezi H a I, ne na pozici CH jako dva znaky

Pythonová implementace (`KRIZOVKA/krizovka/normalize.py:to_grid_cells`):
```python
_CH_MARKER = "¤"
plain = strip_diacritics(word).upper()
marked = plain.replace("CH", _CH_MARKER)
cells = [("CH" if c == _CH_MARKER else c) for c in marked if c.isalpha() or c == _CH_MARKER]
```

## Ponaučení o web research

Research report tvrdil že "švédská křížovka rozepisuje CH" — možná to tak komerční časopisy dělají, ale to nerozhoduje o tom, co je správně jazykově. **Před implementací jazykové konvence ověř u rodilého mluvčího nebo v autoritativním zdroji (Pravidla českého pravopisu, ÚJČ AV ČR), ne v popisu křížovkových časopisů.**

## Related

- Direct correction: user řekl "ty moulo" — silný signál, ne soft feedback
- Connected to: `feedback_czech_language.md` (komunikace česky, jazyková přesnost)

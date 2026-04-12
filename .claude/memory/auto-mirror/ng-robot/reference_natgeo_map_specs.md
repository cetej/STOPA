---
name: NatGeo Resource Guide - Map Specifications
description: Font specifikace, barvy a placement pravidla z "04 Maps 2022.pdf" pro kartografickou lokalizaci
type: reference
---

## Zdroj
`C:\Users\stock\Documents\000_NGM\RESOURCES\Resource Guide\Resource Guide\Resource Guide\04 Maps 2022.pdf`
23 stran — kapitoly: Guidelines, Cartographic Policies, Map Styles, Text Masking, Text Specification, Large-Format Maps.

## Typografické specifikace (strany 15-20)

### Print (Standard Page Maps)
| Feature | Font | Size |
|---------|------|------|
| Country | NEO GOTHIC HEAVY CAPS | 7+ |
| State/province | NEO GOTHIC CAPS | 7-10 |
| City/town | Neo Gothic | 7-9 |
| Capital | Neo Gothic Heavy | 8-10 |
| Parks/reserves/nat. forests | BUMSTEAD CAPS | 6+ |
| National Parks | BUMSTEAD HEAVY CAPS | 6+ |
| Mountain range/desert/plateau | BUMSTEAD CAPS | 7-10 |
| Peak name | Bumstead | 6.5-7.5 |
| Ocean | CAPTION BOLD CAPS | 8-10 |
| Sea/river/lake | Caption bold | 7-10 |
| Scale bar | Geograph Edit | 4.5-5 |

### Web Maps (strany 19-20)
| Feature | Font | Size |
|---------|------|------|
| Country | NATGEO NEO GOTHIC HEAVY CAPS | 12-17 |
| National Parks | NATGEO BUMSTEAD HEAVY CAPS | 13-17 |
| National Forests | NatGeo BUMSTEAD CAPS | 13-17 |
| River/lake | NATGEO Caption | 13 |
| Town spot | 6px wide |

### Barvy (Web)
| Prvek | RGB |
|-------|-----|
| Land | 233/223/219 nebo 216/208/190 |
| Water | 197/223/239 |
| Physical green | 170/184/126 nebo 144/153/92 |
| Text - green | 99/109/56 nebo 64/74/30 |
| Text - water | 147/191/221 |
| Graticule | 255/255/255 |

## Name Placement Guide (strany 21-22) — KLÍČOVÉ

### Města (Towns)
- Text 1/2 až 1 šířka townspot od značky
- Preferovaná pozice: NE > SE > NW > SW
- Ne příliš blízko, ne příliš daleko
- Zakřivení podél pobřeží OK, ale ne příliš strmé
- Poslední písmeno by mělo končit téměř horizontálně

### Jezera (Lakes)
- Malá jezera: text vedle (u nejširší části/středu), vzdálenost 1/2-1 šířka townspot
- Velká jezera: text UVNITŘ, roztažený
- Stackovaný název: každý řádek čte ke břehu
- Podlouhlá jezera: pojmenovat rovnoběžně s jezerem jako řeku

### Řeky (Rivers)
- Text ROVNOBĚŽNĚ s tokem (kopíruje obecný směr, ne každý zákrut)
- Vzdálenost = šířka tenké říční čáry
- Ascendery/descendery mohou zasahovat do řeky
- Opakované pojmenování: zvětšit font směrem k ústí
- Umístit kde je řeka ROVNĚJŠÍ

### Pohoří/Spread names
- Neoddělovat slova v krátkém spread name
- Roztažení 1.5× délka prvku na obou stranách
- Centrovat v rámci prvku vertikálně i horizontálně
- Stackované spread linie musí být ROVNOBĚŽNÉ

### Vrcholy (Peaks)
- Název i výška čtou ke kříži, na stejné straně
- Název NAD číslem pokud možno

### Text Masking (strany 12-14)
- Gaussian Blur halo kolem textu (duplikace + blur + clip mask)
- Type halo (Illustrator): stroke 1-2pt v barvě pozadí
- Mixed masking: text + řeky/jiné prvky v jedné masce

## Implementováno v map_localizer.py
- `CARTOGRAPHIC_RULES` dict — feature_type → font_style, color, placement, letter_spacing, halo
- `_FONT_BY_TYPE` — hierarchická velikost (park=48 > country=36 > state=22 > forest=15)
- Layout prompt obsahuje NatGeo placement pravidla
- Renderer: hierarchický cap (measured_size ≤ 1.3× hierarchy_size)

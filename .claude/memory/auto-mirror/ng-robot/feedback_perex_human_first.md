---
name: Perex musí být human-first, ne mechanism-first
description: Při generování/kontrole perexu (Phase 7 SEO) — první věta vždy lidský dopad, ne technologie. Žádný nevysvětlený žargon, žádné prázdné hyperboly typu "mění pravidla hry".
type: feedback
originSessionId: d4b04384-7673-4a98-a355-8610d9eddab7
---
Při generování perexu (a obecně leadu) v NG-ROBOT článcích musí platit:

1. **První věta = lidský dopad / co se v praxi mění**, ne mechanismus nebo technologie. Mechanismus přijde až ve 2. větě, pokud vůbec.
2. **Žádný odborný žargon bez překladu** ("cyklický peptid", "biologická dostupnost", "fenotyp", "ablace"…). Test: zná to slovo prodavačka v supermarketu?
3. **Žádné prázdné hyperboly** ("mění pravidla hry", "přelomový moment", "zásadní milník", "číslo, které mění…"). Místo toho konkrétní fakt s rozměrem dopadu.
4. **Číslo musí mít kontext.** Holé "33–41 %" laikovi nic neříká — buď doplň referenci, nebo číslo z perexu vypusť.
5. **PEREX se nesmí formulačně krýt s H1 ani bold lead odstavcem.** Test duplikace: vezmi 6 obsahových slov z H1 a 6 z PEREXu — pokud se 3+ kryjí ve stejném pořadí, je to porušení. H1 a PEREX mají být komplementární úhly (ACTION / PROBLEM-HISTORY / SOLUTION-HOW), ne dvě parafráze.
6. **Důraz na CO se vynalezlo a JAKÉ to má důsledky, NE na KDO to vynalezl.** Pokud objev NENÍ česká věda, atribuci ("japonský tým", "vědci z Kumamoto") nech do těla článku — pro českého čtenáře je relevantní co a proč, ne kdo. **Výjimka:** česká věda → atribuce v titulku/perexu má smysl. Platí jak pro PEREX, tak pro všechny varianty H1 a SEO titulků.
7. **Při výběru hlavního H1 z 3 variant**: vybírej **lidskou nebo záhadnou variantu**, NE analytickou (ta je default model bias = jargon-heavy = nesrozumitelná pro 99 % čtenářů).

**Why:** 2026-04-30 — uživatel se velmi rozčílil nad perexem článku o perorálním inzulinu, který začínal "Japonští vědci z Kumamoto University navrhli cyklický peptid…" místo "Miliony diabetiků by mohly vyměnit injekci za tabletu…". Perex psaný odbornou hatmatilkou ztratí 99 % čtenářů dřív, než se dostanou k pointě. Je to identický typ chyby, jaký už řeší globální `writing-quality.md` (P0 — significance inflation), ale Phase 7 prompt to dosud nevynucoval lokálně.

**How to apply:**
- Při editaci `projects/7-SEO-METADATA/MASTER_INSTRUCTIONS.md` (Krok 2: PEREX) tato pravidla zachovat.
- Při ručním psaní perexu / kontroly výstupu Phase 7 aplikovat 4 pravidla výše.
- Pokud uživatel pošle URL článku s nadávkou na "debilní perex", reflexivně zkontrolovat: human-first? bez žargonu? bez hyperbol? číslo s kontextem?
- Při návrhu fixu upozornit, že popularizace (Phase 6.5) i koheze (Phase 9.5) mají PEREX v zákazu — opravit se musí v Phase 7 nebo regenerací článku od fáze 7.

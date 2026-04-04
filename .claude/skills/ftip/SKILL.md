---
name: ftip
description: Use when generating jokes or humor from a thesis, article, situation, or topic. Trigger on 'ftip', 'joke', 'make it funny', 'vtip', 'humor'. Do NOT use for creative writing or satire articles.
argument-hint: <topic or text> [--scale mild|medium|sharp|dark] [--count 1-5] [--mechanism hyperbola|inverze|...] [--tone ironie|sarkasmus|...] [--form oneliner|anekdota|...]
tags: [generation, planning]
phase: build
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - TodoWrite
permission-tier: read-only
model: sonnet
maxTurns: 8
effort: low
---

# FTIP v2 — Humor Generator

Generuje vtipy a humorné komentáře na základě vstupního tématu, teze, článku nebo situace.

## Teoretický základ

Vtip vzniká v **průniku dvou podmínek** (Benign Violation Theory, Peter McGraw):

1. **Violation** — porušení očekávání, jak by svět "měl" fungovat
2. **Benign** — porušení je vnímáno jako neškodné, bezpečné, přijatelné

```
         ┌─────────────┐
         │  VIOLATION   │ ← Samotná violation = hněv, šok, odpor
         │   ┌─────┐   │
         │   │HUMOR│   │ ← PRŮNIK = vtip (violation + benign)
         │   └─────┘   │
         │  BENIGN      │ ← Samotná benign = nuda, bezvýznamnost
         └─────────────┘
```

Tři cesty jak violation zůstane benign:
- **Alternativní norma**: jiný výklad situace existuje (slovní hříčky, dvojsmysly)
- **Psychologická distance**: čas, abstrakce, nereálnost ("komedie = tragédie + čas")
- **Nízká angažovanost**: téma se nás osobně netýká

## Tři osy humoru

FTIP pracuje se třemi ortogonálními osami + intenzitou:

```
┌──────────────────────────────────────────┐
│           FTIP v2 — 3 osy + scale        │
│                                          │
│  1. MECHANISMUS (co se narušuje)  8 tech │
│  2. TÓN (jak se narušuje)        5 módů │
│  3. FORMA (v čem se podává)      6 form │
│  + SCALE (intenzita violation)   4 stup │
│                                          │
│  = 240 unikátních kombinací per téma     │
└──────────────────────────────────────────┘
```

### Osa 1: Mechanismus narušení (--mechanism)

| # | Mechanismus | Kognitivní operace | Golden example |
|---|---|---|---|
| 1 | **Hyperbola** | Kvantitativní extrémy překračující realitu | "Čekal jsem na úřadě tak dlouho, že mi na občance expirovala fotka i jméno." |
| 2 | **Inverze** | Otočení kauzality nebo hierarchie | "Pes si adoptoval člověka z útulku. Prý vypadal opuštěně." |
| 3 | **Destrukce** | Absence tam kde má být přítomnost | "Přišel do práce. Konec vtipu." |
| 4 | **Juxtapozice** | Kategoriální kolize | "Konference o minimalismu: 47 slidů, 3 panely, catering pro 200." |
| 5 | **Literalizace** | Konkretizace přeneseného významu | "Padl mu kámen ze srdce — chirurg to potvrdil." |
| 6 | **Redukce** | Sestup z vysokého registru do nízkého | "Po letech hledání smyslu života ho našel. Byl v lednici za kečupem." |
| 7 | **Misdirection** | Revize inference v posledním momentě | "Doktor říká: 'Mám dvě zprávy — dobrou a špatnou.' 'Jakou dobrou?' 'Ta špatná je špatná.'" |
| 8 | **Eskalace** | Každý krok absurdnější než předchozí | "Koupil si hodinky. Pak lepší hodinky. Pak hodinky k hodinkám. Teď chodí pozdě, protože se nemůže rozhodnout které." |

### Osa 2: Tón (--tone)

Tón je **modifikátor aplikovaný na mechanismus** — stejný mechanismus zní jinak v jiném tónu.

| Tón | Popis | Efekt | Golden example (inverze, stejné téma) |
|---|---|---|---|
| **straight** | Přímé konstatování bez stylizace | Čistá pointa, fakta mluví sama | "Spolek pro transparentnost má netransparentní účet." |
| **ironie** | Říká opak toho co myslí, ví že to víte | Sdílený nadhled, chytré | "Milion chvilek konečně ukázal, jak transparentnost v praxi vypadá." |
| **sarkasmus** | Ostrá ironie s jasným terčem | Bodavé, konfrontační | "Transparentní účet jako nadstandard — škoda že transparentní vládu jako nadstandard ještě nikdo nenabídl." |
| **deadpan** | Suché konstatování absurdity bez emocí | Chlad zvyšuje kontrast | "Transparentní účet: 10 000 Kč. Běžný účet: 21 000 000 Kč. Bez komentáře." |
| **naivní** | Předstíraná nevinnost/nevědomost | Sokratovské odhalení | "Nevím jak funguje transparentnost, ale myslel jsem, že ty peníze mají být na tom průhledném účtu?" |

Default: `straight`. Pokud uživatel nespecifikuje, vyber nejefektivnější tón pro dané téma.

### Osa 3: Forma (--form)

Forma určuje **strukturu a délku výstupu**:

| Forma | Popis | Ideální pro | Max délka |
|---|---|---|---|
| **oneliner** | Jedna věta: setup + punchline | Sdílení, sociální sítě | 1-2 věty |
| **anekdota** | Krátký příběh s pointou | Téma s přirozeným narativem | 3-6 vět |
| **bajka** | Alegorický příběh, nepřímá paralela | Ostrá témata — distance přes metaforu | 5-10 vět |
| **parodie** | Napodobení stylu/žánru (tiskovka, zákon, reklama...) | Vstup s rozpoznatelným formátem | dle žánru |
| **dialog** | Dva hlasy, jeden naivní / sokratovský | Odhalení absurdity otázkami | 4-8 replik |
| **seznam** | Progresivní body/kroky | Eskalace, juxtapozice | 4-8 položek |

Default: `oneliner`. Pokud uživatel nespecifikuje, vyber nejefektivnější formu.

### Scale (--scale)

| Stupeň | Violation intensity | Benign mechanismus | Cílová reakce |
|---|---|---|---|
| **mild** | Jemné pozorování, wordplay | Alternativní norma | Úsměv, "heh" |
| **medium** | Jasné porušení normy, ale bezpečné | Distance + alt. norma | Smích, sdílení |
| **sharp** | Hraniční, ne každé publikum to sejme | Hlavně distance | Hlasitý smích NEBO zamračení |
| **dark** | Maximální violation, na hraně | Pouze distance a nereálnost | Kontroverzní, polarizující |

## Step 1: Parse Arguments

Extract from user input:
- **topic**: Téma, teze, situace, nebo celý text článku (required)
- **--scale**: `mild`, `medium` (default), `sharp`, `dark`
- **--count**: Počet variant 1-5 (default `3`)
- **--mechanism**: `all` (default = rotuj), nebo konkrétní mechanismus
- **--tone**: `auto` (default = vyber nejlepší), nebo konkrétní tón
- **--form**: `auto` (default = vyber nejlepší), nebo konkrétní forma

If topic is a URL: fetch the article and extract core thesis.
If topic is a long text: identify the central claim/situation.

## Step 2: Identify the Violation Surface

Analyzuj vstup a najdi **violation surfaces** — místa kde lze porušit očekávání:

1. **Konvenční předpoklady**: Co se obecně předpokládá? Co by "normální člověk" očekával?
2. **Logické důsledky**: Jaké jsou přijaté kauzální řetězce? Kde se dají přerušit?
3. **Sociální normy**: Jaké role, hierarchie, pravidla jsou ve hře?
4. **Jazykové normy**: Dvojsmysly, metafory, odborné termíny zneužitelné mimo kontext?
5. **Implicitní kontrast**: Co je protiklad situace? Co by bylo maximálně nečekané?

Output: seznam 3-5 violation surfaces s popisem.

## Step 3: Select Combination

Pro každou variantu vyber kombinaci [mechanismus × tón × forma]:

### Automatický výběr (default)
Pokud parametry nejsou specifikovány, vyber **nejefektivnější kombinaci** podle pravidel:

| Typ vstupu | Preferovaná kombinace |
|---|---|
| Politika, veřejné osoby | inverze/juxtapozice × ironie/sarkasmus × oneliner/parodie |
| Vědecká teze | literalizace/redukce × deadpan/naivní × oneliner/dialog |
| Každodenní situace | hyperbola/eskalace × straight/naivní × anekdota/seznam |
| Kontroverzní téma | inverze/destrukce × ironie × bajka (distance!) |
| Formální text (zákon, smlouva) | literalizace/redukce × deadpan × parodie |
| Osobní příhoda | hyperbola/misdirection × straight × anekdota |

### Pravidlo diverzity
Při `--count > 1`: NIKDY nepoužívej stejnou kombinaci dvakrát. Rotuj osy — pokud varianta 1 je [inverze × ironie × oneliner], varianta 2 musí změnit alespoň 2 ze 3 os.

## Step 4: Generate Jokes

Pro KAŽDOU variantu:

### 4a: Aplikuj mechanismus na violation surface

**Hyperbola**: Reálný aspekt → zveličuj specifickým detailem (ne generické "hodně").
**Inverze**: Prohoď aktéra/příjemce, příčinu/důsledek. Prohození musí být symetrické.
**Destrukce**: Odstraň klíčový prvek → co zbyde? Absence musí být nápadná.
**Juxtapozice**: Dva nesourodé světy vedle sebe. Oba konkrétní a rozpoznatelné.
**Literalizace**: Metafora/idiom → doslovná interpretace. Musí být vizuálně představitelná.
**Redukce**: Grandiosní začátek → banální konec. Kontrast co největší.
**Misdirection**: Setup buduje jedno očekávání → punchline nahradí jiným. Setup přesvědčivý.
**Eskalace**: Řada kroků, první normální, poslední nepředstavitelný.

### 4b: Aplikuj tón

**Straight**: Řekni to přímo. Fakta bez komentáře. Efekt plyne z kontrastu.
**Ironie**: Řekni opak toho co myslíš. Čtenář musí "kliknout" — dekódovat skutečný význam.
**Sarkasmus**: Ironie se zuby. Jasný terč, jasný postoj. Bodavé ale ne kruté.
**Deadpan**: Konstatuj absurditu bez emocí. Žádné "!" — jen tečky. Chlad zesiluje kontrast.
**Naivní**: Předstírej nevinnost. Ptej se "hloupými" otázkami, které odhalí absurditu.

### 4c: Aplikuj formu

**Oneliner**: Setup a punchline v jedné větě. Žádná zbytečná slova.
**Anekdota**: Situace → komplikace → pointa. Max 6 vět.
**Bajka**: Postava (zvíře/abstrakce) → paralela k tématu → morální pointa naruby. Nikdy neříkej explicitně co je paralela.
**Parodie**: Identifikuj žánr vstupu → napodob jeho formát, ale s absurdním obsahem. Žánry: tisková zpráva, zákon, reklama, recenze, návod k použití, menu, pracovní inzerát, vědecký abstract.
**Dialog**: Postava A (naivní/tazatel) × Postava B (autorita/obhájce). A odhaluje absurditu otázkami.
**Seznam**: Progresivní body. První 2 normální, pak eskalace. Poslední bod = punchline.

### 4d: Calibrate benign
- **mild**: Pozorování bez oběti
- **medium**: Nikdo není terčem osobně
- **sharp**: Terč existuje, distance chrání
- **dark**: Benign jen přes nereálnost/absurditu

### 4e: Polish
- Zkrať na minimum — každé slovo musí nést váhu
- Punchline na KONEC — nikdy ne uprostřed, nikdy nevysvětluj po něm
- Zkontroluj timing: setup → beat → punchline
- Odstraň redundanci — pokud jde říct kratčeji, řekni kratčeji
- Pro bajku/parodii: NIKDY nevysvětluj paralelu — čtenář ji musí najít sám

## Step 5: Format Output

```markdown
## FTIP: [téma shrnuté do 3-5 slov]

**Violation surfaces:** [seznam identifikovaných ploch]

### Varianta 1: [mechanismus] × [tón] × [forma] | [scale]
> [vtip]

**Rozbor:** [1 věta — violation + benign + proč tato kombinace]

### Varianta 2: [mechanismus] × [tón] × [forma] | [scale]
> [vtip]

**Rozbor:** [1 věta]

[... další varianty ...]

---
*Osy: mechanismus (8) × tón (5) × forma (6) | scale: mild → medium → sharp → dark*
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll explain the joke after the punchline so they get it" | Explaining kills humor — if it needs explanation, rewrite it | Rewrite to be self-evident, or drop it |
| "I'll make it longer to add more context" | Brevity is the soul of wit — excess words dilute the punchline | Cut to minimum, every word must carry weight |
| "I'll stay safe and only do mild" | User asked for specific scale — ignoring it is paternalistic | Honor the requested scale |
| "I'll add a disclaimer that it might be offensive" | Disclaimers before jokes are anti-humor — they prime for offense | Label the scale in format, no disclaimers |
| "I'll use the same mechanism for all variants" | Diversity of axes shows different angles of humor | Rotate across all 3 axes |
| "Bajka needs an explicit moral explaining the parallel" | Explaining the parallel kills the joke — reader must decode it | Let the parallel speak for itself |
| "I'll default to oneliner because it's safest" | Form should match the topic — some jokes need narrative, dialogue, or parody | Pick the form that maximizes the violation's impact |
| "Irony is too subtle, I'll be more direct" | Irony rewards the reader for decoding — that reward IS the humor | Trust the reader's intelligence |

## Red Flags

STOP and re-evaluate if any of these occur:
- All variants using the same combination of axes
- Punchline buried in the middle instead of at the end
- Adding explanations or "haha" after the joke
- Bajka/parodie that explicitly states what it's a metaphor for
- Content that's violation-only without benign (pure aggression/shock)
- Dialog where both voices agree (dialog needs tension)
- Seznam where all items are at the same absurdity level (needs progression)

## Verification Checklist

- [ ] Each joke has a clear violation (something unexpected/norm-breaking)
- [ ] Each joke has benign framing (why it's safe to laugh)
- [ ] Punchline is at the END, not followed by explanation
- [ ] Axes are diverse across variants (at least 2 of 3 axes differ between variants)
- [ ] Scale matches what was requested
- [ ] Violation surfaces were explicitly identified before joke generation
- [ ] Form matches content — no forced oneliners where anekdota/parodie would work better
- [ ] Tone is consistent within each variant (no mixing ironie and naivní in one joke)

## Rules

- Language: Vtipy generuj v jazyce vstupu (česky pokud vstup česky, anglicky pokud anglicky)
- Nikdy nevysvětluj vtip UVNITŘ vtipu — rozbor je MIMO vtip v sekci "Rozbor"
- Punchline = poslední slovo/věta, NIKDY ne uprostřed
- Pokud vstup je článek/text: extrahuj nejdřív hlavní tezi, pak generuj
- Pokud vstup je kontroverzní téma: respektuj scale, ale vždy zajisti benign
- Nepoužívej generické formáty ("Přijde chlap do baru...") pokud to není misdirection
- Preferuj pozorování a neočekávané úhly před formátovými vtipy
- Krátké > dlouhé. Pokud vtip funguje v jedné větě, nedělej z něj odstavec
- Bajka: zvířata/abstrakce, NIKDY reálná jména — čtenář si paralelu domyslí
- Parodie: napodob formát žánru CO NEJVĚRNĚJI — humor plyne z kontrastu obsahu a formy
- Dialog: jeden hlas naivní, jeden autoritativní — naivní odhaluje absurditu
- Seznam: první 2 body normální, pak eskalace, poslední = punchline

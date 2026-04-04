---
name: ftip
description: Use when generating jokes or humor from a thesis, article, situation, or topic. Trigger on 'ftip', 'joke', 'make it funny', 'vtip', 'humor'. Do NOT use for creative writing or satire articles.
argument-hint: <topic, thesis, article text, or situation> [--scale mild|medium|sharp|dark] [--count 1-5] [--mechanism all|hyperbola|inverze|destrukce|juxtapozice|literalizace|redukce|misdirection|eskalace]
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
maxTurns: 6
effort: low
---

# FTIP — Humor Generator

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

## 8 mechanismů narušení (violation techniques)

| # | Mechanismus | Popis | Kognitivní operace |
|---|---|---|---|
| 1 | **Hyperbola** | Přehánění do absurdity | Kvantitativní extrémy překračující realitu |
| 2 | **Inverze** | Prohození rolí, příčiny/důsledku | Otočení kauzality nebo hierarchie |
| 3 | **Destrukce** | Odstranění očekávaného prvku | Absence tam kde má být přítomnost |
| 4 | **Juxtapozice** | Nekompatibilní věci vedle sebe | Kategoriální kolize |
| 5 | **Literalizace** | Metafora vzatá doslova | De-abstrakce, konkretizace přeneseného |
| 6 | **Redukce (bathos)** | Vznešené → banální | Sestup z vysokého registru do nízkého |
| 7 | **Misdirection** | Setup vede jinam než punchline | Revize inference v posledním momentě |
| 8 | **Eskalace** | Progresivní absurdita | Každý krok je absurdnější než předchozí |

## Škálování (osa violation intensity)

| Stupeň | Popis | Benign mechanismus | Příklad cílové reakce |
|---|---|---|---|
| **mild** | Jemné pozorování, wordplay, ironie | Alternativní norma | Úsměv, "heh, to je fakt" |
| **medium** | Jasné porušení normy, ale bezpečné | Distance + alt. norma | Smích, sdílení |
| **sharp** | Hraniční, ne každé publikum to sejme | Hlavně distance | Hlasitý smích NEBO zamračení |
| **dark** | Maximální violation, balancuje na hraně | Pouze distance a nereálnost | Kontroverzní, polarizující |

## Step 1: Parse Arguments

Extract from user input:
- **topic**: Téma, teze, situace, nebo celý text článku (required)
- **--scale**: Stupeň violation: `mild`, `medium` (default), `sharp`, `dark`
- **--count**: Počet variant 1-5 (default `3`)
- **--mechanism**: Který mechanismus použít: `all` (default), nebo konkrétní

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

## Step 3: Generate Jokes

Pro KAŽDÝ vyžádaný vtip (--count):

### 3a: Vyber mechanismus
- Pokud `--mechanism all`: rotuj mechanismy pro diverzitu
- Pokud konkrétní: použij jen ten

### 3b: Aplikuj mechanismus na violation surface
Pro každý mechanismus jiný přístup:

**Hyperbola**: Vezmi reálný aspekt → zveličuj dokud nepřekročí absurditu. Klíč: specifický detail (ne generické "hodně").

**Inverze**: Prohoď aktéra/příjemce, příčinu/důsledek, nebo převrať hierarchii. Klíč: prohození musí být symetrické a čisté.

**Destrukce**: Odstraň klíčový prvek situace → co zbyde? Klíč: absence musí být nápadná a komická.

**Juxtapozice**: Postav vedle sebe dva nesourodé světy. Klíč: oba světy musí být konkrétní a rozpoznatelné.

**Literalizace**: Najdi metaforu/idiom → interpretuj doslova. Klíč: doslovná verze musí být vizuálně představitelná.

**Redukce**: Začni grandiosně → skonči banálně. Klíč: kontrast musí být co největší, mundánní detail co nejkonkrétnější.

**Misdirection**: Setup buduje jedno očekávání → punchline ho nahradí jiným. Klíč: setup musí být přesvědčivý, punchline nečekaný ale logický.

**Eskalace**: Řada kroků, každý absurdnější. Klíč: první krok je normální, poslední nepředstavitelný.

### 3c: Calibrate benign
Podle --scale adjustuj:
- **mild**: Punchline je laskavý, pozorování bez oběti
- **medium**: Violation je jasná ale nikdo není terčem osobně
- **sharp**: Někdo/něco je terčem, ale distance to chrání
- **dark**: Maximální violation — benign zajišťuje pouze nereálnost/absurdita

### 3d: Polish
- Zkrať na minimum — každé slovo musí nést váhu
- Zkontroluj timing: setup → beat → punchline
- Punchline na KONEC (nikdy nevysvětluj vtip po punchline)
- Odstraň redundanci — pokud jde říct kratčeji, řekni kratčeji

## Step 4: Format Output

```markdown
## FTIP: [téma shrnuté do 3-5 slov]

**Violation surfaces:** [seznam identifikovaných ploch]

### Varianta 1: [mechanismus] | [scale]
> [vtip]

**Rozbor:** [1 věta — jaká violation, proč benign]

### Varianta 2: [mechanismus] | [scale]
> [vtip]

**Rozbor:** [1 věta]

[... další varianty ...]

---
*Mechanismy: hyperbola, inverze, destrukce, juxtapozice, literalizace, redukce, misdirection, eskalace*
*Škála: mild → medium → sharp → dark*
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll explain the joke after the punchline so they get it" | Explaining kills humor — if it needs explanation, it's not funny | Rewrite the joke to be self-evident, or drop it |
| "I'll make it longer to add more context" | Brevity is the soul of wit — excess words dilute the punchline | Cut to minimum, every word must carry weight |
| "I'll stay safe and only do mild" | User asked for specific scale — ignoring it is paternalistic | Honor the requested scale, let the user decide their comfort |
| "I'll add a disclaimer that it might be offensive" | Disclaimers before jokes are anti-humor — they prime for offense | Let the joke stand on its own, label the scale in the format |
| "I'll use the same mechanism for all variants" | Diversity of mechanisms shows different angles of humor | Rotate mechanisms unless user specified one |

## Red Flags

STOP and re-evaluate if any of these occur:
- Generating jokes that target specific real people in harmful ways
- All variants using the same mechanism despite --mechanism all
- Punchline buried in the middle instead of at the end
- Adding explanations or "haha" after the joke
- Generating content that's violation-only without benign (pure aggression/shock)

## Verification Checklist

- [ ] Each joke has a clear violation (something unexpected/norm-breaking)
- [ ] Each joke has benign framing (why it's safe to laugh)
- [ ] Punchline is at the END, not followed by explanation
- [ ] Mechanisms are diverse across variants (unless user specified one)
- [ ] Scale matches what was requested
- [ ] Violation surfaces were explicitly identified before joke generation

## Rules

- Language: Vtipy generuj v jazyce vstupu (česky pokud vstup česky, anglicky pokud anglicky)
- Nikdy nevysvětluj vtip UVNITŘ vtipu — rozbor je MIMO vtip v sekci "Rozbor"
- Punchline = poslední slovo/věta, NIKDY ne uprostřed
- Pokud vstup je článek/text: extrahuj nejdřív hlavní tezi, pak generuj
- Pokud vstup je kontroverzní téma: respektuj scale, ale vždy zajisti benign
- Nepoužívej generické formáty ("Přijde chlap do baru...") pokud to není misdirection
- Preferuj pozorování a neočekávané úhly před formátovými vtipy
- Krátké > dlouhé. Pokud vtip funguje v jedné větě, nedělej z něj odstavec

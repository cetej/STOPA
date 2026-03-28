# Agentic AI and the Next Intelligence Explosion

**Paper:** arXiv:2603.20639
**Autoři:** James Evans, Benjamin Bratton, Blaise Agüera y Arcas
**Afiliace:** Google (Paradigms of Intelligence Team), University of Chicago, Santa Fe Institute, Antikythera/Berggruen Institute, UC San Diego
**Datum:** 2026-03-21
**Licence:** CC BY 4.0

---

## Hlavni teze

Paper odmita klasicky singularity narrativ (monoliticka superinteligence bootstrapujici sama sebe) a navrhuje alternativu: **inteligence je pluralni, socialni a relacni** — roste jako mesto s distribuovanou specializaci, ne jako jeden vsevedouci Buh.

---

## 5 klicovych argumentu

### 1. Inteligence je inherentne socialni

- Primati: inteligence koreluje s velikosti socialni skupiny, ne s obtiznosti prostredi
- Jazyk umoznil kulturni akumulaci znalosti pres generace
- Pismo, pravo, byrokracie = externalizovane systemy socialni inteligence
- Sumersky pisare spravujici obili = system-level inteligence presahujici individualni chapani

### 2. Societies of Thought uvnitr modelu

**Klicovy poznatek:** Frontier reasoning modely (DeepSeek-R1, QwQ-32B) spontanne generuji interni multi-agentni interakce — "spolecnost myslenek."

- Mechanismus: model simuluje debaty mezi ruznyma kognitivnima perspektivama (argumentace, verifikace, sladeni)
- Toto chovani **nebylo explicitne natreneno** — RL na presnost samo spustilo tyto konverzacni struktury
- Zaver: robustni reasoning je inherentne socialni proces, i uvnitr jednoho modelu

### 3. Neprozkoumany design space

Organizacni veda studuje dynamiku tymu desitky let (velikost, slozeni, hierarchie, role, konflikty, site) — ale tenhle vyzkum skoro vubec neovlivnuje design AI reasoning systemu.

Soucasne modely produkuji jednu konverzaci ("AI town hall transcript"). Efektivni systemy by mely mit:
- Hierarchii a specializaci
- Delbu prace
- **Strukturovany nesouhlas** jako zamerne navrzenou feature
- Paralelni, konvergujici i divergujici deliberacni proudy

### 4. Human-AI centauri

Kompozitni lidsko-AI aktori — "ani ciste lidsti, ani ciste strojovi":
- Jeden clovek ridi vice AI agentu
- Jedna AI slouzi vice lidem
- Mnoho lidi a AI v menicicich se konfiguracich

Pokrocila kapabilita: agenti mohou spawnovat interni kopie, diferenciovat pro subtasky a rekombinovat vysledky — rekurzivni spolecnosti myslenek expandujici s narocnosti ukolu.

### 5. Institucionalni alignment

**Posun od RLHF k institucionalnimu alignmentu:**

| RLHF (soucasnost) | Institucionalni alignment (navrhovy) |
|---|---|
| Dyadicky (rodic-dite korekce) | Systemovy (organizace, trhy, soudy) |
| Neskalovatelny na miliardy agentu | Skalovatelny pres role a protokoly |
| Individualni cnost | Institucionalni constrainty |

Princip: "Soudce", "obhajce", "porota" jako **protokolove sloty**, ne individua.

**Ustavni AI governance:**
- High-stakes AI (najimani, trestani, davky) vyzaduje systemy s explicitne investovanymi hodnotami: transparence, equita, due process
- Tyto systemy se navzajem kontroluji — separace moci jako v ustave
- Priklad: AI oddeleni prace audituje korporatni hiring algoritmy; soudni AI vyhodnocuje rizikove odhady exekutivy proti ustavnim standardum

---

## Historicke exploze inteligence

Paper refamuje historii inteligence jako postupne emergence socialne agregovanych kognitivnich jednotek:

1. **Primatni skupinova inteligence** — socialni mozek
2. **Lidsky jazyk a kulturni transmise** — mezigeneracni znalosti
3. **Pismo a byrokraticka infrastruktura** — externalizovana pamet
4. **LLM jako computacne aktivni kulturni ratchet** — kazdy parametr = komprimovany reziduum komunikacni vymeny

---

## Relevance pro STOPA / orchestracni system

| Paper koncept | STOPA ekvivalent |
|---|---|
| Societies of Thought (interni debate) | Critic loops, multi-agent review |
| Strukturovany nesouhlas | Circuit breakers, FAIL → STOP pravidla |
| Hierarchie + specializace | Tier system (Haiku/Sonnet/Opus), role (scout/critic/orchestrator) |
| Institucionalni constrainty | Budget tiers, nesting depth limits, memory maintenance pravidla |
| Paralelni deliberace | Paralelni sub-agenti, farm tier |
| Rekurzivni spolecnosti myslenek | Rekurzivni orchestrace s depth limitem |
| Human-AI centauri | Uživatel + Claude Code + sub-agenti jako kompozitni aktor |
| Checks & balances | Critic po kazde editaci, verify pred done |

### Inspirace pro dalsi vyvoj

1. **Strukturovany nesouhlas jako feature** — misto jednoho critica: devil's advocate agent, ktery aktivne hleda duvody proc reseni nefunguje
2. **Role-based protocols** — definovat "soudce" (arbitr pri konfliktu mezi agenty), "porota" (vicero lehkych modelu hlasuje)
3. **Institutional memory** — decisions.md je zaklad, ale paper naznacuje nutnost precedentniho systemu (minula rozhodnuti informuji budouci)
4. **Adaptive team composition** — menit pocet a typ agentu podle slozitosti ukolu (uz castecne implementovano v budget tiers)

---

## Citovatelne myslenkove linie

- "No mind is an island" — inteligence vznika z pluralni interakce, ne izolovanym vypoctem
- Intelligence is high-dimensional and relational, not a single quantity
- Scaling = ne vetsi model, ale bohatsi socialni systemy
- Otazka neni zda inteligence ziska radikalne na sile, ale zda lidstvo postavi socialni infrastrukturu hodnou toho, cim se stava

---

## Metadata

- **Typ:** Pozicni paper / essay (ne empiricky vyzkum)
- **Silne stranky:** Elegantni reframing, silna historicka argumentace, prakticky governance framework
- **Slabe stranky:** Neni empiricky — zadne experimenty s multi-agent systemy, zadna mereni; "societies of thought" v modelech popisuje anekdotalne
- **Navazujici cteni:** Organizational science literature on team composition; constitutional AI governance frameworks

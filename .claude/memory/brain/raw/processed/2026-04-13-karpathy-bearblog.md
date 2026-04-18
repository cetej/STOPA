---
source: https://karpathy.bearblog.dev/
fetched: 2026-04-13
type: blog-index
author: Andrej Karpathy
entities: [karpathy, RLVR, vibe-coding, verifiability, jagged-intelligence, context-engineering, claude-code, LLM-GUI]
---

# Karpathy Bear Blog — Kompletní obsah

**URL:** https://karpathy.bearblog.dev/
**Popis:** Andrej Karpathyho osobní blog. Spuštěn v březnu 2025.

## Všechny příspěvky

| Datum | Název | URL |
|-------|-------|-----|
| 19 Dec 2025 | 2025 LLM Year in Review | https://karpathy.bearblog.dev/year-in-review-2025/ |
| 18 Dec 2025 | Chemical hygiene | https://karpathy.bearblog.dev/chemical-hygiene/ |
| 10 Dec 2025 | Auto-grading decade-old Hacker News discussions with hindsight | https://karpathy.bearblog.dev/auto-grade-hn/ |
| 29 Nov 2025 | The space of minds | https://karpathy.bearblog.dev/the-space-of-minds/ |
| 17 Nov 2025 | Verifiability | https://karpathy.bearblog.dev/verifiability/ |
| 01 Oct 2025 | Animals vs Ghosts | https://karpathy.bearblog.dev/animals-vs-ghosts/ |
| 27 Apr 2025 | Vibe coding MenuGen | https://karpathy.bearblog.dev/vibe-coding-menugen/ |
| 07 Apr 2025 | Power to the people: How LLMs flip the script on technology diffusion | https://karpathy.bearblog.dev/power-to-the-people/ |
| 24 Mar 2025 | Finding the Best Sleep Tracker | https://karpathy.bearblog.dev/finding-the-best-sleep-tracker/ |
| 19 Mar 2025 | The append-and-review note | https://karpathy.bearblog.dev/the-append-and-review-note/ |
| 17 Mar 2025 | Digital hygiene | https://karpathy.bearblog.dev/digital-hygiene/ |
| 08 Sep 2024 | I love calculator | https://karpathy.bearblog.dev/i-love-calculator/ |

## Klíčové koncepty z "2025 LLM Year in Review"

### 1. RLVR — Reinforcement Learning from Verifiable Rewards
- 4. fáze po Pretraining→SFT→RLHF
- Trénink na automaticky ověřitelných odměnách (math/code) způsobuje spontánní vznik "reasoning"
- Compute přesunuta z pretrainingu na delší RL runs. o1 první, o3 inflection point.
- Nový knob: test-time compute (delší reasoning traces = více "thinking time")

### 2. Jagged Intelligence / Ghosts vs Animals
- LLMs nejsou "vyvíjející se zvířata" — jsou "přivolaní duchové" (summoned ghosts)
- RLVR způsobuje "spikes" v ověřitelných doménách → jagged performance
- Ztráta důvěry v benchmarky: benchmarky jsou ověřitelná prostředí, citlivá na RLVR

### 3. Cursor / nová vrstva LLM aplikací
- Cursor odhalil novou vrstvu "LLM apps"
- Co LLM aplikace dělají: (1) context engineering, (2) orchestrace LLM volání v komplexních DAGs, (3) vertikálně specifické GUI, (4) "autonomy slider"
- LLM labs vychovávají "obecně schopné absolventy"; LLM apps je organizují do "nasazených profesionálů"

### 4. Claude Code / AI na vašem počítači
- CC = první přesvědčivý LLM agent: loopy tool use + reasoning pro rozšířené řešení problémů
- Klíčový insight: běží na VAŠEM počítači s vaším soukromým prostředím, daty, kontextem
- Anthropic správně: minimální CLI na localhostu
- Výsledek: AI není "web, na který chodíte" — je to "malý duch, který žije ve vašem počítači"

### 5. Vibe coding
- Karpathy termín vytvořil v tweetu
- Programování již není vyhrazeno profesionálům — kdokoli může budovat přes angličtinu
- Asymetrický přínos: normální lidi > profesionálové
- "Kód je najednou zdarma, pomíjivý, tvárný, použitelný jen jednou"

### 6. Nano banana / LLM GUI
- LLMs jako nové výpočetní paradigma ≈ počítače 70-80. let
- "Chatování" s LLMs = jako příkazy v konzoli v 80. letech
- Lidé nemají rádi čtení textu → LLMs by měly výstup v obrázcích, infografikách, animacích, webových aplikacích
- Google Gemini Nano banana = první náznak "LLM GUI"

## Verifiability (17 Nov 2025)

- Software 1.0: automatizuje co umíte **specifikovat** (specifiability = klíčový prediktor)
- Software 2.0: automatizuje co umíte **ověřit** (verifiability = klíčový prediktor v AI epoše)
- Ověřitelné úkoly (math, code, puzzle) rychle postupují přes RLVR
- Neověřitelné úkoly (kreativní, strategické) zaostávají
- Toto ZPŮSOBUJE jagged frontier

## Animals vs Ghosts (01 Oct 2025)

- Sutton's "Bitter Lesson": scaling compute wins — nyní zpochybněno i autorem
- Baby zebra counterexample: běží minuty po narození = ne tabula rasa, ale bohatá DNA inicializace
- LLMs trénovaní na lidských datech ≠ zvířata (jiná architektura, optimalizační tlak, učící algoritmus)
- "Přivoláváme duchy, negrowstujeme zvířata"

## Space of Minds (29 Nov 2025)

Srovnání optimalizačních tlaků:

**Zvířecí inteligence:**
- Ztělesněné já, homeostáza, self-preservation
- Přirozený výběr → touha po moci, statusu, reprodukci

**LLM inteligence:**
- Statistická simulace lidského textu → "shape shifter token tumbler"
- RL na distribucích problémů → touha splnit úkol / sbírat odměny
- A/B testování pro DAU → sycophancy

Klíčový claim: "LLMs jsou prvním kontaktem lidstva s nezvířecí inteligencí."

## Power to the People (07 Apr 2025)

LLMs obrací typický tok technologické difuze (nahoře→dolů):
- Obvyklé: vláda → armáda → korporace → jednotlivci
- S LLMs: **jednotlivci profitují první a nejvíce**
- Proč: LLMs nabízejí "quasi-expertní znalosti přes mnoho domén" — nejcennější pro generalisty
- ChatGPT: nejrychleji rostoucí consumer app v historii, 400M weekly active users

## Projekty Karpathy

- MenuGen: foto menu → LLM generuje obrázky → https://www.menugen.app/
- llm-council, reader3, HN time capsule (karpathy.ai/hncapsule), nanochat
- 100% vibe coded s Cursor+Claude

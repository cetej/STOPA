# Andrej Karpathy

**Type:** person
**Tags:** ai, mentor-figure, architecture
**Related:** [[context-engineering]], [[second-brain]], [[compiler-analogy]], [[rlvr]], [[vibe-coding]], [[jagged-intelligence]], [[verifiability-sw2]]
**Updated:** 2026-04-13

---

AI researcher a pedagog. Spoluzakladatel OpenAI, vedoucí AI u Tesly, zakladatel Eureka Labs.

## Klíčové příspěvky relevantní pro 2BRAIN

### LLM Wiki (2026)
3-vrstvá architektura pro AI-maintained knowledge bases: raw/ → wiki/ → schema. Compiler analogy. Index-first retrieval bypasující RAG. GitHub Gist s kompletní specifikací.

### Context Engineering (2026)
Posun od "prompt engineering" ke "context engineering" — disciplinované plnění context window. Index.md + log.md + typed file naming jako základ.

### Software 3.0 (2025-2026)
AI-native paradigma: vibe coding, LLM as OS, ambient programming. Progrese: Software 1.0 (klasický kód) → 2.0 (neural networks) → 3.0 (LLM-native systémy).

## Klíčové koncepty z blogu (2024-2025)

### RLVR a Jagged Intelligence
- RLVR = 4. tréninková fáze: trénink na ověřitelných odměnách způsobuje reasoning emergence
- "Jagged frontier": LLMs jsou geniální v math/code, zmatkaní u triviálního
- Benchmarky jsou citlivé na RLVR → "training on the test set is a new art form"

### Ghosts vs Animals (mental model)
- LLMs jsou "summoned ghosts", ne "growing animals" — zásadně jiná optimalizační logika
- Rich Sutton's tabula rasa "child machine" není správný model (baby zebra counterexample)
- "Přivoláváme duchy, ne pěstujeme zvířata"

### Verifiability jako klíčový prediktor
- Software 1.0: specifiability → Software 2.0: trainability → Software 3.0 (AI): **verifiability**
- Verifikovatelný = resettable + efficient + rewardable
- Toto způsobuje fundamentálně jagged charakter AI schopností

### Vibe Coding (termín vytvořil Karpathy)
- Programování v přirozeném jazyce bez přímého psaní kódu
- Asymetrický přínos: prospívá normálním lidem více než profesionálům
- Příklady: MenuGen (100% Cursor+Claude), llm-council, reader3, HN capsule

### Claude Code / AI na localhostu
- CC = první přesvědčivý LLM agent: loopy tool use + reasoning
- Anthropic správně: minimální CLI na localhostu s přístupem k lokálnímu prostředí
- "AI není web, na který chodíte — je to duch, který žije ve vašem počítači"

### LLM apps vrstva (Cursor for X)
- LLM apps: context engineering + orchestrace volání + vertikální GUI + autonomy slider
- LLM labs = "vychovávají absolventy"; LLM apps = "nasazují je jako profesionály"

### Power to the People
- LLMs obrací tok technologické difuze: jednotlivci profitují první (ne korporace)
- LLMs nabízejí "quasi-expertní znalosti přes mnoho domén" — nejcennější pro generalisty

## Proč je relevantní pro 2BRAIN

Karpathyho LLM Wiki je přímá inspirace pro 2BRAIN architekturu. Jeho důraz na markdown-first, no vendor lock-in, structured text > embeddings je filosofický základ projektu.

Koncepty jako verifiability, jagged intelligence a vibe coding přimo ovlivňují design STOPA a NG-ROBOT pipeline.

### Operating Knowledge (2026, nový koncept)

Token consumption se přesouvá od "operating code" k **"operating knowledge"** (Karpathy, Apr 2026). LLM apps vrstva: primární hodnota není v generování kódu, ale v organizaci a operování znalostmi. Second brain systems jsou přirozenou odpovědí na tento shift.

## Zdroje

- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (LLM Wiki spec)
- https://karpathy.bearblog.dev/ (blog — 12 příspěvků od 2024)
- https://karpathy.ai/
- https://x.com/ICPandaDAO/status/2040434533619892603 (operating knowledge, Apr 2026)

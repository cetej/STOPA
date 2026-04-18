# Andrej Karpathy

**Type:** person
**Tags:** ai, mentor-figure, architecture
**Related:** [[context-engineering]], [[second-brain]], [[compiler-analogy]], [[rlvr]], [[vibe-coding]], [[jagged-intelligence]], [[verifiability-sw2]]
**Updated:** 2026-04-18

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

### AI Capability Perception Gap (April 18, 2026)

Karpathy identifikoval dvě příčiny growing perception gap o AI schopnostech:
1. **Outdated reference point**: většina lidí si vytvořila obraz AI z free-tier ChatGPT, ne z agentic frontier modelů (Claude Code, Codex)
2. **Peaky capabilities**: AI dramaticky lepší ve verifikovatelných doménách (kód, math) díky existence reward functions; general tasks (vyhledávání, rady, psaní) mají slabé komerční incentive pro zlepšení

Důsledek: dva lidé mohou oba "mít pravdu" o AI — jeden vidí transformativní zlepšení v kódu, druhý vidí selhání v obecných úkolech. Používají jiné nástroje na jiné úrovni.

→ Raw: [2026-04-18-karpathy-ai-capability-gap.md](../../raw/2026-04-18-karpathy-ai-capability-gap.md)

### Farzapedia — Personal Wikipedia Pattern (April 2026)

Karpathy endorse Farzapedia (personal Wikipedia z 2,500 diary entries od Farzy @FarzaTV) jako lepší model pro AI personalizaci než proprietární systémy. Čtyři výhody oproti proprietary AI memory:

1. **Explicitnost**: vidíš přesně co AI ví a neví
2. **Vlastnictví dat**: soubory na tvojím stroji, ne zamčené u providera
3. **Universální formát**: markdown/images → funguje s libovolným nástrojem, Unix utilities, fine-tuning
4. **Vendor flexibility**: swap mezi providery svobodně

Managing personal knowledge wiki = klíčová dovednost 21. století, AI agenti ji mohou pomoci udržovat.

→ Raw: [2026-04-18-karpathy-farzapedia-llm-wiki.md](../../raw/2026-04-18-karpathy-farzapedia-llm-wiki.md)

### LLM Coding Pitfalls (2026)

Karpathyho observace o opakovaných chybách LLM při kódování — 4 vzory vedoucí k destilaci čtyř principů (multica-ai/andrej-karpathy-skills, 57k★ za den, 2026-04-18):

1. **Wrong assumptions without checking** → Think Before Coding (state assumptions, surface interpretations, push back, stop when confused)
2. **Overcomplication a bloated abstractions** → Simplicity First (minimum code, no speculative features, "200 lines → 50 lines" test)
3. **Orthogonal edits, changing code they don't understand** → Surgical Changes (match existing style, mention dead code don't delete it, every changed line traces to request)
4. **Weak success criteria** → Goal-Driven Execution (transform imperative → verifiable goals, loop independently on strong criteria)

Tradeoff explicitně: **bias toward caution over speed**. Konflikt s pure-autonomy: u genuinely ambiguous user intent surface interpretations místo silent picking.

Aplikováno v STOPA: Code Editing Discipline section v behavioral-genome.md (principy 3 + ambiguity surfacing z principu 1).

→ Source: https://x.com/karpathy/status/2015883857489522876  
→ Implementation reference: https://github.com/multica-ai/andrej-karpathy-skills

## Zdroje

- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (LLM Wiki spec)
- https://karpathy.bearblog.dev/ (blog — 12 příspěvků od 2024)
- https://karpathy.ai/
- https://x.com/ICPandaDAO/status/2040434533619892603 (operating knowledge, Apr 2026)
- https://x.com/karpathy/status/2042334451611693415 (AI capability gap, Apr 18 2026)
- https://x.com/karpathy/status/2040572272944324650 (Farzapedia endorsement, Apr 2026)
- https://x.com/karpathy/status/2015883857489522876 (LLM coding pitfalls observation, 2026)
- https://github.com/multica-ai/andrej-karpathy-skills (57k★ CLAUDE.md template, 2026-04-18)

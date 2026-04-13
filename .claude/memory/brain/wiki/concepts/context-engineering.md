# Context Engineering

**Type:** concept
**Tags:** ai, architecture, retrieval, llm
**Related:** [[compiler-analogy]], [[second-brain]], [[karpathy]]

---

Termín zavedený Karpathym (2026) jako nástupce "prompt engineering". Zatímco prompt engineering se soustředí na formulaci jednoho dotazu, context engineering je disciplinované plnění celého context window — task descriptions, RAG výsledky, stav, historie, kompakce.

## Klíčové principy

1. **Index-first**: Strukturovaný index (index.md) se čte PRVNÍ. Plný obsah žije v separátních souborech, načítá se on-demand.
2. **Typed file naming**: Prefixy (user_, feedback_, project_) routují LLM writes bez vektorových databází.
3. **Persistent over ephemeral**: Wiki přežívá context compaction; chat history ne.
4. **Chirurgicky malé indexy**: Indexy musí přežít compaction — plný obsah jde jinam.

## Vztah ke 2BRAIN

Context engineering je provozní princip 2BRAIN: brain/ je kontextový artefakt optimalizovaný pro to, aby LLM měl co nejrelevantnější znalost v omezeném context window.

## Zdroje

- Karpathy X post (context engineering vs prompt engineering)
- Karpathy LLM Wiki Gist

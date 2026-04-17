---
date: 2026-04-17
source_type: url
source_url: https://x.com/karpathy/status/2039805659525644595
---

# Karpathy: LLM Knowledge Bases methodology (X/Twitter, 2026)

Tweet od @karpathy o praktické metodologii budování LLM knowledge bases.

Klíčová tvrzení:
- ~100 article wiki s 400K slovy zvládne komplexní Q&A bez sofistikovaného RAG systému
- LLM auto-udržuje index soubory a summaries — manuální editace wikipedie se stává zbytečnou
- Knowledge bases mohou růst přes synthetic data generation a model fine-tuning

Operační workflow:
- **Data ingest**: sbírání zdrojů (články, papery, repozitáře, obrázky) do adresářů
- **Wiki compilation**: LLM generuje markdown strukturu se summaries, backlinky, konceptuální organizací
- **IDE integration**: Obsidian jako viewing a management interface
- **Q&A**: dotazování knowledge base přes indexovaný obsah
- **Output formats**: Markdown soubory, Marp slides, matplotlib vizualizace
- **Health checks**: LLM-driven consistency audits a quality improvements
- **Auxiliary tools**: custom search engines a CLI integrace

Nástroje zmíněné: Obsidian Web Clipper (extension), Obsidian (note-taking), Marp (presentation), matplotlib (visualization).

Significance: Potvrzuje praktickou viabilitu LLM Wiki vzoru ve scale, kde obvyklý RAG přestává být nutný. Scale threshold: ~100 articles / 400K words.

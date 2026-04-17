# 2BRAIN Inbox

Sem přidej URL nebo text k zachycení. Scheduled task `brain-ingest` je zpracuje automaticky.

Format: jeden záznam per řádek. Prefix určuje typ:
- `URL: https://...` — fetch a kompiluj do wiki
- `IDEA: text...` — přímý capture myšlenky
- `WATCH: https://...` — přidej do watchlistu pro pravidelný monitoring

Zpracované záznamy se přesunou do `inbox-archive.md`.

---

## Queue

URL: https://arxiv.org/abs/2504.16828
URL: https://arxiv.org/abs/2604.11623
URL: https://arxiv.org/abs/2604.07681
URL: https://arxiv.org/abs/2603.22862
URL: https://arxiv.org/abs/2603.27910
URL: https://x.com/karpathy/status/2039805659525644595

## Processed

| Date | Item |
|------|------|
| 2026-04-13 | URL: https://karpathy.bearblog.dev/ — zpracováno, 4 nové wiki články |
| 2026-04-14 | URL: https://arxiv.org/abs/2603.29493 — MemFactory paper → new wiki article memfactory.md |
| 2026-04-14 | URL: https://arxiv.org/abs/2603.07670 — Agent Memory Survey → new wiki article agent-memory-taxonomy.md |
| 2026-04-14 | URL: https://ghost.codersera.com/blog/karpathy-llm-knowledge-base-second-brain/ — Karpathy LLM KB → updated llm-wiki.md (3-folder arch, limits) |
| 2026-04-14 | URL: https://evoailabs.medium.com/why-andrej-karpathys-llm-wiki-is-the-future-of-personal-knowledge-7ac398383772 — LLM Wiki EvoAI → updated llm-wiki.md (compounding, RAG critique) |
| 2026-04-14 | URL: https://x.com/ICPandaDAO/status/2040434533619892603 — Karpathy operating knowledge → updated llm-wiki.md + karpathy.md + new graph node |
| 2026-04-15 | URL: https://arxiv.org/abs/2603.10808 — Nurture-First Development → new wiki article nurture-first-development.md, 8 graph edges |
| 2026-04-16 | URL: https://arxiv.org/abs/2604.10660 — CPMI Process Reward Modeling (ACL 2026) → new wiki article cpmi-process-reward.md, 4 graph edges |

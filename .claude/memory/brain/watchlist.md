# 2BRAIN Watchlist

Zdroje pro automatický pravidelný monitoring. Scheduled task `brain-watch` je skenuje 1x denně.

## Gmail Labels (auto-scan)

Emaily v těchto labelech se automaticky zpracují do inbox.md:

| Label | Gmail ID | Popis | Poslední scan |
|-------|----------|-------|---------------|
| To Read | Label_13 | Články a zdroje k přečtení | 2026-04-24 |
| To Watch | Label_14 | Videa k zhlédnutí | 2026-04-24 |
| Later | Label_15 | Odložené k pozdějšímu zpracování | 2026-04-24 |
| Starred (unread) | STARRED | Hvězdičkou označené nepřečtené | 2026-04-24 |

## Gmail Senders (auto-capture newsletters)

Emaily od těchto odesílatelů se automaticky zpracují:

| Sender | Popis | Poslední scan |
|--------|-------|---------------|
| newsletter@platformer.news | Tech news (Platformer) | 2026-04-24 |
| noreply@substack.com | Substack newsletters | 2026-04-24 |

## Blogs & Personal Sites

| URL | Autor | Frekvence | Poslední scan |
|-----|-------|-----------|---------------|
| https://karpathy.bearblog.dev/ | Karpathy | daily | 2026-05-01 |
| https://simonwillison.net/ | Simon Willison | daily | 2026-05-01 |
| https://www.answer.ai/blog | Jeremy Howard (Answer.ai) | weekly | 2026-05-01 |
| https://www.anthropic.com/research | Anthropic Research | weekly | 2026-05-01 |
| https://lilianweng.github.io/ | Lilian Weng (OpenAI) | monthly | 2026-04-19 |

## arXiv Topics

| Query | Oblast | Kategorie | Poslední scan |
|-------|--------|-----------|---------------|
| LLM memory augmented agents | AI/ML | cs.AI | 2026-05-01 |
| personal knowledge management AI | PKM | cs.AI | 2026-05-01 |
| agent orchestration multi-agent tool-use | Orchestrace | cs.AI, cs.MA | 2026-05-01 |
| RAG retrieval-augmented prompting context-engineering | Retrieval | cs.CL | 2026-05-01 |
| LLM coding agent automated software engineering | Dev tools | cs.SE | 2026-05-01 |
| self-improving agent reinforcement learning feedback | Self-improve | cs.AI, cs.LG | 2026-05-01 |
| process reward model step verification | RL/Rewards | cs.AI, cs.LG | 2026-05-01 |
| prompt injection agent safety defense | Safety | cs.CR, cs.AI | 2026-05-01 |
| LLM knowledge graph entity extraction structured memory | Knowledge | cs.AI, cs.IR | 2026-05-01 |
| agentic benchmark evaluation autonomous task | Eval | cs.AI | 2026-05-01 |

## X/Twitter Accounts

| Handle | Důvod sledování | Poslední scan |
|--------|----------------|---------------|
| @karpathy | LLM Wiki, context engineering, Software 3.0 | 2026-04-24 |
| @AnthropicAI | Claude updates, safety research | 2026-04-24 |
| @simonw | LLM tooling, datasette, practical AI | 2026-04-24 |
| @deedydas | Claude Code usage patterns, agentic workflows | 2026-04-24 |
| @swyx | AI Engineer ecosystem, latent space | 2026-04-24 |
| @jeremyphoward | Answer.ai, practical ML | 2026-04-24 |
| @omarsar0 | Paper curator (DAIR.AI), high-signal arXiv announcements | 2026-04-24 |
| @garrytan | YC/startups, agent tooling (gbrain/Minions) | 2026-04-24 |
| @liu8in | AI video tooling, HyperFrames, motion graphics | 2026-04-24 |
| @SakanaAILabs | Evolutionary AI research (AC/DC, CycleQD) | 2026-04-24 |
| @MillieMarconnni | Kritika AI research agentů, meta-analýzy (Jena/IIT Delhi confirmation bias) | 2026-04-24 |
| @HowToAI_ | AI security, DeepMind attack vectors, practical AI threats | 2026-04-24 |
| @ZabihullahAtal | Agentic AI SE papers, evaluation methodology (TAR trajectories) | 2026-04-24 |
| @ihtesham2005 | MCP servers, context compression tools (context-mode) | 2026-04-24 |
| @socialwithaayan | MCP ecosystem, code search tools (Claude Context) | 2026-04-24 |
| @askalphaxiv | AlphaXiv paper curator, Sakana/evolutionary AI research | 2026-04-24 |
| @heygurisingh | Dev practices, field studies o AI coding agents | 2026-04-24 |
| @Suryanshti777 | Claude Code deep-dives, Opus feature analysis | 2026-04-24 |
| @TawohAwa | AI video editors, Claude Code media tools (video-use) | 2026-04-24 |
| @RidgerZhu | LLM architecture research (looped LLMs, Parcae, Ouro) | 2026-04-24 |
| @hasantoxr | Claude Code tooling, API proxying, cost optimization | 2026-04-24 |
| @DAIEvolutionHub | Open-source AI projects, trending GitHub repos (DeepTutor) | 2026-04-24 |
| @elora_khatun | Anthropic ecosystem, courses a learning paths | 2026-04-24 |
| @chrisfirst | AI video generation tutorials (Seedance, Runway) — low priority | 2026-04-24 |
| @TheTuringPost | AI/ML newsletter, popular-science content — low priority filter | 2026-04-24 |
| @isaakfreeman | Startup/vision posts — low priority filter | 2026-04-24 |
| @IATheYoker | Claude Code resource curator (španělsky) — obrázkový obsah | 2026-04-24 |

## Google Drive Folders (auto-scan)

_(Drive API vrací prázdné — scope možná omezený. Přidej složku manuálně pokud potřebuješ.)_

## Weekly Deep Sources (scanned by weekly-sources-digest)

| Zdroj | URL/Query | Typ | Frekvence |
|-------|-----------|-----|-----------|
| Simon Willison blog | https://simonwillison.net/ | Blog | weekly |
| Latent Space newsletter | site:latent.space new post | Newsletter | weekly |
| GitHub Trending AI | github.com/trending?since=weekly lang:python topic:llm | Tools | weekly |
| awesome-claude-code | github.com/anthropics/anthropic-cookbook | Patterns | weekly |
| HuggingFace Daily Papers | https://huggingface.co/papers | Papers | weekly |
| Claude Code GitHub discussions | github.com/anthropics/claude-code discussions | Community | weekly |

## RSS/Feeds

_(přidej přes `/capture WATCH: <url>`)_

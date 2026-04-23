# 2BRAIN Watchlist

Zdroje pro automatický pravidelný monitoring. Scheduled task `brain-watch` je skenuje 1x denně.

## Gmail Labels (auto-scan)

Emaily v těchto labelech se automaticky zpracují do inbox.md:

| Label | Gmail ID | Popis | Poslední scan |
|-------|----------|-------|---------------|
| To Read | Label_13 | Články a zdroje k přečtení | 2026-04-23 |
| To Watch | Label_14 | Videa k zhlédnutí | 2026-04-23 |
| Later | Label_15 | Odložené k pozdějšímu zpracování | 2026-04-23 |
| Starred (unread) | STARRED | Hvězdičkou označené nepřečtené | 2026-04-23 |

## Gmail Senders (auto-capture newsletters)

Emaily od těchto odesílatelů se automaticky zpracují:

| Sender | Popis | Poslední scan |
|--------|-------|---------------|
| newsletter@platformer.news | Tech news (Platformer) | 2026-04-23 |
| noreply@substack.com | Substack newsletters | 2026-04-23 |

## Blogs & Personal Sites

| URL | Autor | Frekvence | Poslední scan |
|-----|-------|-----------|---------------|
| https://karpathy.bearblog.dev/ | Karpathy | daily | 2026-04-23 |
| https://simonwillison.net/ | Simon Willison | daily | 2026-04-23 |
| https://www.answer.ai/blog | Jeremy Howard (Answer.ai) | weekly | 2026-04-23 |
| https://www.anthropic.com/research | Anthropic Research | weekly | 2026-04-23 |
| https://lilianweng.github.io/ | Lilian Weng (OpenAI) | monthly | 2026-04-19 |

## arXiv Topics

| Query | Oblast | Kategorie | Poslední scan |
|-------|--------|-----------|---------------|
| LLM memory augmented agents | AI/ML | cs.AI | 2026-04-23 |
| personal knowledge management AI | PKM | cs.AI | 2026-04-23 |
| agent orchestration multi-agent tool-use | Orchestrace | cs.AI, cs.MA | 2026-04-23 |
| RAG retrieval-augmented prompting context-engineering | Retrieval | cs.CL | 2026-04-23 |
| LLM coding agent automated software engineering | Dev tools | cs.SE | 2026-04-23 |
| self-improving agent reinforcement learning feedback | Self-improve | cs.AI, cs.LG | 2026-04-23 |
| process reward model step verification | RL/Rewards | cs.AI, cs.LG | 2026-04-23 |
| prompt injection agent safety defense | Safety | cs.CR, cs.AI | 2026-04-23 |
| LLM knowledge graph entity extraction structured memory | Knowledge | cs.AI, cs.IR | 2026-04-23 |
| agentic benchmark evaluation autonomous task | Eval | cs.AI | 2026-04-23 |

## X/Twitter Accounts

| Handle | Důvod sledování | Poslední scan |
|--------|----------------|---------------|
| @karpathy | LLM Wiki, context engineering, Software 3.0 | 2026-04-23 |
| @AnthropicAI | Claude updates, safety research | 2026-04-23 |
| @simonw | LLM tooling, datasette, practical AI | 2026-04-23 |
| @deedydas | Claude Code usage patterns, agentic workflows | 2026-04-23 |
| @swyx | AI Engineer ecosystem, latent space | 2026-04-23 |
| @jeremyphoward | Answer.ai, practical ML | 2026-04-23 |
| @omarsar0 | Paper curator (DAIR.AI), high-signal arXiv announcements | 2026-04-23 |
| @garrytan | YC/startups, agent tooling (gbrain/Minions) | 2026-04-23 |
| @liu8in | AI video tooling, HyperFrames, motion graphics | 2026-04-23 |
| @SakanaAILabs | Evolutionary AI research (AC/DC, CycleQD) | 2026-04-23 |
| @MillieMarconnni | Kritika AI research agentů, meta-analýzy (Jena/IIT Delhi confirmation bias) | 2026-04-23 |
| @HowToAI_ | AI security, DeepMind attack vectors, practical AI threats | 2026-04-23 |
| @ZabihullahAtal | Agentic AI SE papers, evaluation methodology (TAR trajectories) | 2026-04-23 |
| @ihtesham2005 | MCP servers, context compression tools (context-mode) | 2026-04-23 |
| @socialwithaayan | MCP ecosystem, code search tools (Claude Context) | 2026-04-23 |
| @askalphaxiv | AlphaXiv paper curator, Sakana/evolutionary AI research | 2026-04-23 |
| @heygurisingh | Dev practices, field studies o AI coding agents | 2026-04-23 |
| @Suryanshti777 | Claude Code deep-dives, Opus feature analysis | 2026-04-23 |
| @TawohAwa | AI video editors, Claude Code media tools (video-use) | 2026-04-23 |
| @RidgerZhu | LLM architecture research (looped LLMs, Parcae, Ouro) | 2026-04-23 |
| @hasantoxr | Claude Code tooling, API proxying, cost optimization | 2026-04-23 |
| @DAIEvolutionHub | Open-source AI projects, trending GitHub repos (DeepTutor) | 2026-04-23 |
| @elora_khatun | Anthropic ecosystem, courses a learning paths | 2026-04-23 |
| @chrisfirst | AI video generation tutorials (Seedance, Runway) — low priority | 2026-04-23 |
| @TheTuringPost | AI/ML newsletter, popular-science content — low priority filter | 2026-04-23 |
| @isaakfreeman | Startup/vision posts — low priority filter | 2026-04-23 |
| @IATheYoker | Claude Code resource curator (španělsky) — obrázkový obsah | 2026-04-23 |

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

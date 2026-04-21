# 2BRAIN Watchlist

Zdroje pro automatický pravidelný monitoring. Scheduled task `brain-watch` je skenuje 1x denně.

## Gmail Labels (auto-scan)

Emaily v těchto labelech se automaticky zpracují do inbox.md:

| Label | Gmail ID | Popis | Poslední scan |
|-------|----------|-------|---------------|
| To Read | Label_13 | Články a zdroje k přečtení | 2026-04-21 |
| To Watch | Label_14 | Videa k zhlédnutí | 2026-04-21 |
| Later | Label_15 | Odložené k pozdějšímu zpracování | 2026-04-21 |
| Starred (unread) | STARRED | Hvězdičkou označené nepřečtené | 2026-04-21 |

## Gmail Senders (auto-capture newsletters)

Emaily od těchto odesílatelů se automaticky zpracují:

| Sender | Popis | Poslední scan |
|--------|-------|---------------|
| newsletter@platformer.news | Tech news (Platformer) | 2026-04-21 |
| noreply@substack.com | Substack newsletters | 2026-04-21 |

## Blogs & Personal Sites

| URL | Autor | Frekvence | Poslední scan |
|-----|-------|-----------|---------------|
| https://karpathy.bearblog.dev/ | Karpathy | daily | 2026-04-21 |
| https://simonwillison.net/ | Simon Willison | daily | 2026-04-21 |
| https://www.answer.ai/blog | Jeremy Howard (Answer.ai) | weekly | 2026-04-21 |
| https://www.anthropic.com/research | Anthropic Research | weekly | 2026-04-21 |
| https://lilianweng.github.io/ | Lilian Weng (OpenAI) | monthly | 2026-04-19 |

## arXiv Topics

| Query | Oblast | Kategorie | Poslední scan |
|-------|--------|-----------|---------------|
| LLM memory augmented agents | AI/ML | cs.AI | 2026-04-21 |
| personal knowledge management AI | PKM | cs.AI | 2026-04-21 |
| agent orchestration multi-agent tool-use | Orchestrace | cs.AI, cs.MA | 2026-04-21 |
| RAG retrieval-augmented prompting context-engineering | Retrieval | cs.CL | 2026-04-21 |
| LLM coding agent automated software engineering | Dev tools | cs.SE | 2026-04-21 |
| self-improving agent reinforcement learning feedback | Self-improve | cs.AI, cs.LG | 2026-04-21 |
| process reward model step verification | RL/Rewards | cs.AI, cs.LG | 2026-04-21 |
| prompt injection agent safety defense | Safety | cs.CR, cs.AI | 2026-04-21 |
| LLM knowledge graph entity extraction structured memory | Knowledge | cs.AI, cs.IR | 2026-04-21 |
| agentic benchmark evaluation autonomous task | Eval | cs.AI | 2026-04-21 |

## X/Twitter Accounts

| Handle | Důvod sledování | Poslední scan |
|--------|----------------|---------------|
| @karpathy | LLM Wiki, context engineering, Software 3.0 | 2026-04-21 |
| @AnthropicAI | Claude updates, safety research | 2026-04-21 |
| @simonw | LLM tooling, datasette, practical AI | 2026-04-21 |
| @deedydas | Claude Code usage patterns, agentic workflows | 2026-04-21 |
| @swyx | AI Engineer ecosystem, latent space | 2026-04-21 |
| @jeremyphoward | Answer.ai, practical ML | 2026-04-21 |

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

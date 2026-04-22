# 2BRAIN Watchlist

Zdroje pro automatický pravidelný monitoring. Scheduled task `brain-watch` je skenuje 1x denně.

## Gmail Labels (auto-scan)

Emaily v těchto labelech se automaticky zpracují do inbox.md:

| Label | Gmail ID | Popis | Poslední scan |
|-------|----------|-------|---------------|
| To Read | Label_13 | Články a zdroje k přečtení | 2026-04-22 |
| To Watch | Label_14 | Videa k zhlédnutí | 2026-04-22 |
| Later | Label_15 | Odložené k pozdějšímu zpracování | 2026-04-22 |
| Starred (unread) | STARRED | Hvězdičkou označené nepřečtené | 2026-04-22 |

## Gmail Senders (auto-capture newsletters)

Emaily od těchto odesílatelů se automaticky zpracují:

| Sender | Popis | Poslední scan |
|--------|-------|---------------|
| newsletter@platformer.news | Tech news (Platformer) | 2026-04-22 |
| noreply@substack.com | Substack newsletters | 2026-04-22 |

## Blogs & Personal Sites

| URL | Autor | Frekvence | Poslední scan |
|-----|-------|-----------|---------------|
| https://karpathy.bearblog.dev/ | Karpathy | daily | 2026-04-22 |
| https://simonwillison.net/ | Simon Willison | daily | 2026-04-22 |
| https://www.answer.ai/blog | Jeremy Howard (Answer.ai) | weekly | 2026-04-22 |
| https://www.anthropic.com/research | Anthropic Research | weekly | 2026-04-22 |
| https://lilianweng.github.io/ | Lilian Weng (OpenAI) | monthly | 2026-04-19 |

## arXiv Topics

| Query | Oblast | Kategorie | Poslední scan |
|-------|--------|-----------|---------------|
| LLM memory augmented agents | AI/ML | cs.AI | 2026-04-22 |
| personal knowledge management AI | PKM | cs.AI | 2026-04-22 |
| agent orchestration multi-agent tool-use | Orchestrace | cs.AI, cs.MA | 2026-04-22 |
| RAG retrieval-augmented prompting context-engineering | Retrieval | cs.CL | 2026-04-22 |
| LLM coding agent automated software engineering | Dev tools | cs.SE | 2026-04-22 |
| self-improving agent reinforcement learning feedback | Self-improve | cs.AI, cs.LG | 2026-04-22 |
| process reward model step verification | RL/Rewards | cs.AI, cs.LG | 2026-04-22 |
| prompt injection agent safety defense | Safety | cs.CR, cs.AI | 2026-04-22 |
| LLM knowledge graph entity extraction structured memory | Knowledge | cs.AI, cs.IR | 2026-04-22 |
| agentic benchmark evaluation autonomous task | Eval | cs.AI | 2026-04-22 |

## X/Twitter Accounts

| Handle | Důvod sledování | Poslední scan |
|--------|----------------|---------------|
| @karpathy | LLM Wiki, context engineering, Software 3.0 | 2026-04-22 |
| @AnthropicAI | Claude updates, safety research | 2026-04-22 |
| @simonw | LLM tooling, datasette, practical AI | 2026-04-22 |
| @deedydas | Claude Code usage patterns, agentic workflows | 2026-04-22 |
| @swyx | AI Engineer ecosystem, latent space | 2026-04-22 |
| @jeremyphoward | Answer.ai, practical ML | 2026-04-22 |

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

# 2BRAIN Watchlist

Zdroje pro automatický pravidelný monitoring. Scheduled task `brain-watch` je skenuje 1x denně.

## Gmail Labels (auto-scan)

Emaily v těchto labelech se automaticky zpracují do inbox.md:

| Label | Gmail ID | Popis | Poslední scan |
|-------|----------|-------|---------------|
| To Read | Label_13 | Články a zdroje k přečtení | — |
| To Watch | Label_14 | Videa k zhlédnutí | — |
| Later | Label_15 | Odložené k pozdějšímu zpracování | — |
| Starred (unread) | STARRED | Hvězdičkou označené nepřečtené | — |

## Gmail Senders (auto-capture newsletters)

Emaily od těchto odesílatelů se automaticky zpracují:

| Sender | Popis | Poslední scan |
|--------|-------|---------------|
| newsletter@platformer.news | Tech news (Platformer) | — |
| noreply@substack.com | Substack newsletters | — |

## Blogs & Personal Sites

| URL | Autor | Frekvence | Poslední scan |
|-----|-------|-----------|---------------|
| https://karpathy.bearblog.dev/ | Karpathy | daily | — |

## arXiv Topics

| Query | Oblast | Poslední scan |
|-------|--------|---------------|
| LLM memory augmented agents | AI/ML | — |
| personal knowledge management AI | PKM | — |

## X/Twitter Accounts

| Handle | Důvod sledování | Poslední scan |
|--------|----------------|---------------|
| @karpathy | LLM Wiki, context engineering, Software 3.0 | — |
| @AnthropicAI | Claude updates, safety research | — |
| @simonw | LLM tooling, datasette, practical AI | — |

## Google Drive Folders (auto-scan)

_(Drive API vrací prázdné — scope možná omezený. Přidej složku manuálně pokud potřebuješ.)_

## RSS/Feeds

_(přidej přes `/capture WATCH: <url>`)_

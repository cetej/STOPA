# Key Facts — Project Reference Data

Factual constants about the project: stack, services, endpoints, config values.
NOT for decisions (→ decisions.md) or bug patterns (→ learnings/).

Updated when infrastructure changes. Checked before guessing configs or suggesting libraries.

## Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Language | Python | 3.12+ | Skills, hooks, scripts |
| Orchestration | Claude Code | latest | Skills + shared memory |
| VCS | Git + GitHub | — | cetej/STOPA |

## Services & Endpoints

| Service | Environment | URL / Port | Notes |
|---------|-------------|------------|-------|
| — | — | — | STOPA is a meta-project, no runtime services |

## Environment Variables

| Variable | Used By | Description |
|----------|---------|-------------|
| FAL_KEY | /nano, /klip | fal.ai API key for image/video generation |
| TELEGRAM_BOT_TOKEN | telegram plugin | Bot token for Telegram channel |

## External Dependencies

| Tool | Required By | Install |
|------|-------------|---------|
| gh | /fix-issue, /autofix, /pr-review | `winget install GitHub.cli` |
| python 3.12+ | hooks, scripts | `winget install Python.Python.3.12` |

## Conventions

- Encoding: UTF-8 everywhere
- Paths: forward slashes or pathlib.Path()
- OS: Windows 11 (primary), skills should be cross-platform
- Language: Czech for user-facing, English for technical instructions

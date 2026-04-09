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

## APIs

| API | Endpoint | What It Returns | Use Case |
|-----|----------|----------------|----------|
| Model Capabilities | `GET /v1/models/{model_id}` | `max_input_tokens`, `max_tokens`, `capabilities` object | Dynamic model verification in orchestrate pre-flight (instead of hardcoded tier tables) |

## Local Inference

| Backend | Model | Config | Use Case |
|---------|-------|--------|----------|
| Ollama | llama3.2:3b | `LLM_BASE_URL=http://localhost:11434/v1` | RAG/ReAct experiments (default) |
| vLLM + TriAttention | Qwen3-8B | `LLM_BASE_URL=http://localhost:8000/v1` | Long-reasoning 30K+ tokens (10.7× KV compression) |
| vLLM + TriAttention | DeepSeek-R1-Distill-7B | same | Deep reasoning with DeepSeek architecture |

Managed by `scripts/vllm-manager.py` (auto-calibrate, health checks, PID tracking):
- Start: `python scripts/vllm-manager.py start [--model qwen|deepseek]`
- Status: `python scripts/vllm-manager.py status` (JSON)
- Stop: `python scripts/vllm-manager.py stop`
- Test: `python scripts/triattention-test.py [--long]`
- Auto-start: `LLMClient(auto_start=True)` spustí server automaticky při ConnectionError

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

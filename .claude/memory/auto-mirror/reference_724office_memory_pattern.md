---
name: 724 Office — Three-Layer Auto-Compressing Memory Pattern
description: Vector memory pattern from 724-office repo — auto-compress evicted messages, dedup at 0.92 cosine, LanceDB retrieval injected into system prompt. Best for always-on agents with persistent sessions.
type: reference
---

## Source
- Repo: https://github.com/wangziqi06/724-office (MIT, ~3300 LOC)
- File: `memory.py` (~310 lines) + integration in `llm.py`
- Author: wangziqi06, single-commit repo from 2026-03-17

## Pattern: Three-Layer Auto-Compressing Memory

### Architecture
```
Session (JSON, max 40 msgs) → overflow triggers →
Compress (background thread, cheap LLM extracts structured facts) →
Dedup (embed + cosine >0.92 = skip) →
Store (LanceDB, 1024-dim vectors) →
Retrieve (on every message, top-5 injected into system prompt)
```

### Key Design Decisions
1. **Structured extraction** — LLM outputs `{fact, keywords, persons, timestamp, topic}`, not raw text
2. **Pronoun + date resolution** in compression prompt ("he" → name, "tomorrow" → 2026-03-28)
3. **Cheap model for compression** (DeepSeek) — runs on every eviction, cost matters
4. **Background thread** for compress — user doesn't wait
5. **Synchronous retrieve** — memory MUST be ready before LLM responds
6. **0.92 cosine threshold** — aggressive dedup, only truly new facts stored
7. **Image stripping** — multimodal content → `[image]` markers before persist (prevents LLM 400s)

### Compression Prompt (core)
```
Extract structured memories from conversation.
Each element: {fact, keywords, persons, timestamp, topic}
Rules:
- Only long-term value (preferences, plans, contacts, decisions)
- Skip chitchat, greetings, tool call results
- Replace pronouns with specific names
- Replace relative dates with absolute
- Nothing worth remembering → return []
```

### Dependencies
- `lancedb` — embedded vector DB (file-based, no server)
- Any OpenAI-compatible embedding API (1024-dim)
- Cheap LLM for compression (DeepSeek, Haiku)

### When to Use
- Always-on agents with persistent sessions (bots, MONITOR, Polybot)
- Systems with natural session overflow (chat history > N messages)

### When NOT to Use
- Ephemeral sessions (Claude Code CLI) — no natural overflow trigger
- Systems where transparency matters more than automation (grep-first YAML is human-readable)
- Projects without embedding API access

### Potential STOPA Integration (future)
If STOPA ever moves to persistent agent sessions:
- Hook into `/compact` or context compression events as overflow trigger
- Use Haiku for cheap structured extraction
- LanceDB alongside existing YAML learnings (hybrid: grep for known topics, vector for semantic recall)
- ~200 lines Python for minimal implementation

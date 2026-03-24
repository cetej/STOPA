---
name: OpenJarvis Framework Analysis
description: Analýza Stanford OpenJarvis frameworku — využitelné patterns pro ADOBE-AUTOMAT (Registry, Engine ABC, TraceCollector)
type: reference
---

# OpenJarvis — Analýza pro ADOBE-AUTOMAT

**Repo:** github.com/open-jarvis/OpenJarvis (Apache 2.0, Stanford Hazy Research)
**Datum analýzy:** 2026-03-23

## Využitelné komponenty (cherry-pick)

### 1. Registry Pattern (`core/registry.py`)
- Generic `RegistryBase[T]` s dekorátorovým `@register("key")`
- Typed subclasses: `EngineRegistry`, `AgentRegistry`, `ToolRegistry`
- ~50 LOC, zero dependencies — universální plugin systém

### 2. Engine Abstraction (`engine/`)
- ABC `InferenceEngine`: `generate()`, `stream()`, `list_models()`, `health()`
- `_OpenAICompatibleEngine` base pro všechny OpenAI-compatible servery
- Cloud engine: OpenAI, Anthropic, Gemini, OpenRouter
- `_fix_tool_call_arguments()` — workaround pro nekonzistentní tool call formáty

### 3. Tool System (`tools/`)
- `BaseTool` ABC: `spec` (ToolSpec) + `execute(**params)` → `ToolResult`
- `ToolSpec`: JSON Schema params, category, cost_estimate, latency_estimate, requires_confirmation, timeout
- `ToolExecutor`: dispatch, RBAC, taint check, timeout, parallel execution

### 4. Trace System (`traces/`)
- `TraceCollector`: decorator/wrapper kolem agentů, subscribuje EventBus events
- `TraceStore`: SQLite backend, save/get/list/search
- `TraceAnalyzer`: summary, per-route stats, per-tool stats, export
- `Trace` dataclass: trace_id, query, agent, model, engine, steps, tokens, latency, energy

### 5. Workflow Engine (`workflow/`)
- DAG-based: node types AGENT, TOOL, CONDITION, TRANSFORM, LOOP
- WorkflowBuilder → WorkflowGraph → WorkflowEngine.run()
- Topological sort, parallel stages via ThreadPool

### 6. Další užitečné
- `LoopGuard` — detekce opakujících se tool callů
- `EventBus` — decoupling telemetrie od business logiky
- `LearningOrchestrator` — trace→mine→evolve→LoRA→eval loop

## Co NEPŘEBÍRAT
- Channels (Telegram, Discord) — nepotřebujeme
- Security (SSRF, taint) — interní app
- Desktop app — máme Svelte web
- MCP/A2A — máme Claude Code MCP
- Learning/LoRA — nemáme lokální modely

## Plán adopce

### Fáze 1 — Quick wins
1. `backend/core/registry.py` — RegistryBase pattern
2. `backend/core/engine.py` — InferenceEngine ABC + AnthropicEngine
3. `backend/core/traces.py` — TraceCollector + TraceStore (SQLite)

### Fáze 2 — Refactor
4. ClaudeProcessor → používá Engine abstrakci
5. Model routing: layout→Sonnet, pipeline phase 2→Haiku, phase 3→Sonnet
6. Nahradit hardcoded model stringy registry lookup

### Fáze 3 — Rozšíření (volitelné)
7. EventBus pro progress tracking
8. ToolExecutor s timeout/retry
9. Trace analytics dashboard ve frontendu

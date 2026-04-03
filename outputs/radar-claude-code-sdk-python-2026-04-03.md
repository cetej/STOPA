# Radar: claude-code-sdk-python (claude-agent-sdk)
**Zdroj:** https://github.com/anthropics/claude-code-sdk-python
**PyPI:** `pip install claude-agent-sdk`
**Datum výzkumu:** 2026-04-03
**Verze k datu:** 0.1.55

---

## TL;DR

Officiální Python SDK od Anthropic pro programatické řízení Claude Code CLI. Nikoli volání Claude API přímo — SDK obaluje `claude` CLI proces a komunikuje s ním přes IPC protokol. Umožňuje spouštět CC sessions z Pythonu, definovat custom agenty, hooks, MCP servery in-process, a řidit session lifecycle. Zralost: aktivní vývoj, 55+ releases za 10 měsíců, 6100 stars. Klíčový poznatek pro STOPA: **toto je přímá cesta k autonomním scheduled agentům mimo CC session**.

---

## 1. Co to dělá — přesně

### Architektura

SDK NEVOLÁ Anthropic API přímo. Místo toho:
1. Spustí `claude` CLI jako subprocess
2. Komunikuje s ním přes **bidirektivní IPC protokol** (JSON přes stdio)
3. Streamuje zpět strukturované zprávy (AssistantMessage, ToolUseBlock, ResultMessage...)

Toto znamená, že všechny funkce CC (skills, CLAUDE.md, hooks, MCP servery, session paměť) jsou dostupné programaticky — SDK jen dává Python obal nad tím co CC CLI umí.

### Dva hlavní vstupní body

**`query()` — jednosměrný async iterator:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Zkontroluj soubor config.py a navrhni vylepšení",
    options=ClaudeAgentOptions(
        cwd="/project",
        permission_mode="acceptEdits",
        max_turns=10,
        max_budget_usd=0.50
    )
):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

**`ClaudeSDKClient` — bidirektivní, interaktivní:**
```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyzuj projekt")
    async for msg in client.receive_response():
        process(msg)
    # Pošli follow-up bez nového procesu
    await client.query("Teď implementuj nalezené bugy")
    async for msg in client.receive_response():
        process(msg)
```

### Plný API povrch (k v0.1.55)

**ClaudeAgentOptions — klíčové fieldy:**
| Field | Typ | Popis |
|-------|-----|-------|
| `cwd` | str/Path | Working directory pro CC |
| `system_prompt` | str / SystemPromptPreset / SystemPromptFile | System prompt nebo preset |
| `model` | str | Model alias ("sonnet", "opus", "haiku") nebo full ID |
| `fallback_model` | str | Fallback při rate limitu |
| `max_turns` | int | Max počet turns |
| `max_budget_usd` | float | Hard limit v USD |
| `task_budget` | TaskBudget | Token budget (API-side) |
| `allowed_tools` | list[str] | Auto-approve tyto nástroje |
| `disallowed_tools` | list[str] | Blokuj tyto nástroje |
| `permission_mode` | PermissionMode | default/acceptEdits/plan/bypassPermissions/dontAsk |
| `mcp_servers` | dict | External nebo in-process MCP servery |
| `hooks` | dict[HookEvent, list[HookMatcher]] | Python funkce interceptující agent loop |
| `agents` | dict[str, AgentDefinition] | Custom agent definice |
| `plugins` | list | Local nebo remote CC pluginy |
| `continue_conversation` | bool | Navázat na předchozí session |
| `resume` | str | Resume konkrétní session ID |
| `session_id` | str | Přiřadit custom session ID |
| `fork_session` | bool | Fork místo pokračování |
| `setting_sources` | list[SettingSource] | Načíst user/project/local settings |
| `thinking` | ThinkingConfig | Extended thinking (Adaptive/Enabled/Disabled) |
| `effort` | "low"/"medium"/"high"/"max" | Effort level |
| `sandbox` | SandboxSettings | Izolace Bash příkazů |
| `stderr` | Callable | Callback pro CLI stderr výstup |
| `betas` | list[SdkBeta] | Beta features (např. context-1m-2025-08-07) |

**AgentDefinition:**
```python
AgentDefinition(
    description="Reviews code for quality",
    prompt="You are a code reviewer...",
    tools=["Read", "Grep"],
    model="sonnet",
    skills=["critic"],      # CC skills k dispozici agentu
    memory="project",       # Přístup k project memory
    maxTurns=20,
    effort="high"
)
```

**Session management (ClaudeSDKClient):**
- `list_sessions()`, `get_session_info()`, `get_session_messages()`
- `fork_session()`, `delete_session()`, `rename_session()`, `tag_session()`
- `get_context_usage()` — kategorizované využití context window
- `interrupt()`, `stop_task(task_id)`, `rewind_files(user_message_id)`
- `set_permission_mode()`, `set_model()` — za běhu
- `reconnect_mcp_server()`, `toggle_mcp_server()`, `get_mcp_status()`

**In-process MCP servery (bez subprocess overhead):**
```python
@tool("analyze_file", "Analyze a Python file", {"path": str})
async def analyze(args):
    return {"content": [{"type": "text", "text": f"Analyzing {args['path']}"}]}

server = create_sdk_mcp_server("my-tools", "1.0.0", tools=[analyze])
options = ClaudeAgentOptions(mcp_servers={"tools": server})
```

**Hooks (Python funkce interceptující agent loop):**
- `PreToolUse`, `PostToolUse`, `PostToolUseFailure`
- `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`
- `Notification`, `PermissionRequest`

Hook může: deny nástroj, upravit input, zalogovat, triggerovat vlastní logiku.

---

## 2. Zralost projektu

### Metriky
| Metrika | Hodnota |
|---------|---------|
| GitHub stars | 6,111 |
| Forks | 838 |
| Open issues | 188 |
| Verze | 0.1.55 |
| Vznik repo | 2025-06-11 |
| Releases za 10 měsíců | 55+ |
| Průměrný release | každé 2-4 dny |
| Aktivní přispěvatelé (lidé) | ~10 (antropic tým) |
| Licence | MIT |

### Vývojová aktivita
Projekt je v **aktivním, rychlém vývoji**. Za poslední 2 týdny (v0.1.51 → v0.1.55):
- Přidáno: fork_session, delete_session, task_budget, SystemPromptFile, AgentDefinition rozšíření, context usage API
- Fixnuto: Python 3.10 kompatibilita, deadlock při hooks, setting-sources flag parsing, MCP tool result truncation

Poslední commit: 2026-04-03 (dnes).

### Stabilita
SDK je stále **pre-1.0**. Verze 0.1.x znamenají, že breaking changes jsou možné. Nicméně zachovává zpětnou kompatibilitu v prakci — starší fieldy jsou označeny jako `@deprecated` ne odstraněny.

### Dokumentace
- README je dobré (code examples, API overview)
- Chybí kompletní API docs (jen README + zdrojový kód)
- Příkladů je 18 ve složce examples/ (agents, hooks, MCP, plugins, budget, sessions...)
- Typy jsou plně anotované (TypedDict, dataclasses)

### Známé problémy
**Kritické (otevřené):**
- #435: Concurrent sessions — 20-70% failure rate pro usage data
- #425: SDK MCP Tools selhávají pod background subagenty (message-queue backpressure)
- #777: Chybí `content[type="thinking"]` v JSONL od v0.1.35+

**Středně závažné:**
- #768: `bypassPermissions` mode nespouští hooks ze settings.json
- #767: `PreToolUse` hook `updatedInput` nefunguje pro AskUserQuestion
- #774: `ExitPlanMode` ukončí SDK turn — nelze spustit nástroje po exit plan mode

**Historické (část opravena):**
- #10 `cwd` ignorováno — opraveno v dřívějších verzích
- #45 Global settings override — opraveno

---

## 3. Relevance pro STOPA

### Scénáře použití

#### A. Autonomní scheduled agenti mimo CC session

Toto je **nejhodnotnější use case pro STOPA**. Aktuálně jsou sub-agenti závislí na hlavní CC session. SDK umožňuje spouštět CC agenty jako standalone Python procesy:

```python
# scheduled_agent.py — spouštěno cron jobem nebo task schedulerem
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions
from pathlib import Path

async def run_daily_sweep():
    options = ClaudeAgentOptions(
        cwd=Path("C:/Users/stock/Documents/000_NGM/NG-ROBOT"),
        system_prompt="You are a maintenance agent. Run /sweep and capture findings.",
        permission_mode="acceptEdits",
        max_budget_usd=0.30,
        max_turns=30,
        # Načti project settings včetně CLAUDE.md a hooks
        setting_sources=["user", "project"]
    )

    async for message in query(
        prompt="/sweep --auto",
        options=options
    ):
        if isinstance(message, ResultMessage):
            log_result(message)

anyio.run(run_daily_sweep)
```

STOPA má `/schedule` skill — SDK by byl implementační základ pro spouštění těchto agentů jako skutečné OS scheduled tasky.

#### B. Nahrazení Agent tool pro sub-agenty

Aktuálně STOPA spouští sub-agenty přes CC Agent tool (v rámci session). SDK nabízí alternativu — spawn CC proces programaticky s explicitní kontrolou:

**Výhody SDK oproti Agent tool:**
- Přesná kontrola nad `cwd`, `model`, `permission_mode` per sub-agent
- `max_budget_usd` — hard stop bez risk runaway costs
- Hook callbacks v Python (ne jen hook skripty)
- Session management — fork, rewind, context usage tracking
- Lze spustit jako skutečný parallel process (threading/multiprocessing)

**Nevýhody SDK oproti Agent tool:**
- Spouští nový CC CLI proces — overhead ~2-3s startup
- Nesdílí hlavní session kontext (musí se předat přes soubory nebo memory)
- Vyžaduje Python environment s nainstalovaným `claude-agent-sdk`

#### C. Orchestrator s precizní kontrolou

ClaudeSDKClient umožňuje **za-běhovou úpravu chování**:
```python
async with ClaudeSDKClient(options) as client:
    await client.query("Začni analýzu")
    async for msg in client.receive_response():
        if detected_sensitive_area(msg):
            await client.set_permission_mode("plan")  # Přepni na plan mode
        if budget_running_low():
            await client.interrupt()  # Stop
```

Toto je kvalitativní skok oproti hook skriptům — Python logika s plným přístupem k datům.

#### D. Custom AgentDefinition pro STOPA skills

```python
options = ClaudeAgentOptions(
    agents={
        "critic": AgentDefinition(
            description="Quality reviewer",
            prompt="You are the STOPA critic agent...",
            tools=["Read", "Grep", "Glob"],
            model="sonnet",
            skills=["critic"],
            memory="project",
            maxTurns=15
        ),
        "scout": AgentDefinition(
            description="Codebase explorer",
            prompt="You are the STOPA scout agent...",
            tools=["Read", "Grep", "Glob", "WebFetch"],
            model="haiku",
            skills=["scout"],
            maxTurns=20
        )
    }
)
```

Toto by umožnilo distribuovat STOPA orchestraci přes SDK místo jen přes skills.

#### E. Budget tracking a cost control

SDK poskytuje `total_cost_usd` v každém ResultMessage. Pro STOPA `/budget` skill by toto bylo přesnější než ccusage CLI:
```python
async for msg in query(...):
    if isinstance(msg, ResultMessage):
        update_budget_ledger(msg.total_cost_usd, msg.usage)
```

### Co SDK nenahradí

- **Hooks ze settings.json** — SDK hooks jsou jiný mechanismus (Python callbacks vs shell skripty). Koexistují, ale `bypassPermissions` mode ignoruje settings.json hooks (bug #768).
- **CLAUDE.md auto-load** — závisí na `setting_sources=["project"]` v options. Pokud není nastaveno, CLAUDE.md se nenačte.
- **CC UI/interaktivita** — SDK je headless, pro interaktivní sessions CC terminal zůstává lepší.

---

## 4. Konkurenti a alternativy

### Přímé srovnání

| Přístup | Flexibilita | Overhead | Kontrola | Headless | Windows |
|---------|-------------|----------|----------|----------|---------|
| **claude-agent-sdk** | Vysoká | Nízká (bundled CLI) | Plná (hooks, agents, budget) | Ano | Ano (Python) |
| **subprocess cc CLI** | Střední | Nízká | Omezená (stdin/stdout parse) | Ano | Ano |
| **Agent tool (v session)** | Nízká | Minimální | Omezená | Ne (v session) | N/A |
| **Strands SDK (AWS)** | Střední | Střední | Střední (tool use loop) | Ano | Ano |
| **LangGraph** | Velmi vysoká | Vysoká (graph overhead) | Vysoká | Ano | Ano |
| **CrewAI** | Střední | Střední | Střední (role-based) | Ano | Ano |

### Subprocess cc CLI vs SDK

Subprocess přístup (`subprocess.run(["claude", "-p", prompt, "--output-format", "stream-json"])`) je nejprimitivnější ale nejpřenosnější. SDK přidává:
- Strukturované typy (ne jen JSON parsing)
- Bidirektivní komunikaci (ClaudeSDKClient)
- In-process MCP servery (bez extra subprocess)
- Python hook callbacks
- Budget control a cost tracking
- Session management API

Pro jednoduché fire-and-forget tasky (monitoring skript, report generator) je subprocess dostačující. Pro komplexní orchestraci je SDK výrazně lepší.

### Strands SDK (AWS, 2025)
- Open-source agent SDK od AWS pro Amazon Bedrock
- Silný v AWS ecosystem (S3, Lambda, DynamoDB tools out of the box)
- Horší pro Claude Code specifické funkce (CC tools, CLAUDE.md, hooks)
- Vhodný pro produkční deployment na AWS, ne pro lokální CC orchestraci

### LangGraph
- Nejflexibilnější (graph-based workflow)
- Overkill pro STOPA use case
- Nevyužívá CC specifické funkce (skills, memory, CLAUDE.md)
- Složitý na setup a debugging

### CrewAI
- Role-based multi-agent framework
- Abstrahuje příliš — přichází o CC specifická vylepšení
- Nedostatečná Windows podpora v minulosti

**Verdikt:** Pro STOPA je claude-agent-sdk jediná volba — ostatní frameworks abstrahují pryč CC specifické funkce (skills, CLAUDE.md, hooks, memory) které jsou jádrem STOPA.

---

## 5. Instalace a quickstart na Windows

### Požadavky
- Python 3.10+
- Claude Code CLI nainstalovaný (`npm install -g @anthropic-ai/claude-code`) NEBO SDK ho bundluje automaticky od určité verze

### Instalace

```bash
pip install claude-agent-sdk
```

SDK bundluje Claude CLI — není třeba samostatná instalace pro základní použití. Pro vlastní CC verzi:
```python
options = ClaudeAgentOptions(cli_path="C:/Users/username/AppData/Roaming/npm/claude.cmd")
```

### Windows specifika

```python
import sys
import asyncio
from pathlib import Path
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage

# Windows: použij pathlib pro cesty
PROJECT_PATH = Path("C:/Users/stock/Documents/000_NGM/NG-ROBOT")

async def run_agent():
    options = ClaudeAgentOptions(
        cwd=PROJECT_PATH,
        permission_mode="acceptEdits",
        max_turns=20,
        max_budget_usd=0.25,
        setting_sources=["user", "project"],  # Načti CLAUDE.md a settings
        # Windows: UTF-8 pro stderr
        stderr=lambda text: print(text, end="", file=sys.stderr)
    )

    async for message in query(
        prompt="Zkontroluj stav projektu a reportuj",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Hotovo. Cost: ${message.total_cost_usd:.4f}")

# Windows: anyio je cross-platform (funguje s asyncio nebo trio)
anyio.run(run_agent)
```

### Minimal working example (Windows, 5 řádků)

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for msg in query(prompt="What is 2+2?"):
        print(msg)

anyio.run(main)
```

### Poznámky pro Windows
- `anyio` funguje na Windows bez problémů (asyncio backend)
- Cesty: `Path()` všude, nikdy hardcoded backslashe
- Encoding: SDK interně handluje UTF-8, ale pro stderr callback dej `sys.stderr` s UTF-8 reconfigure
- Antivirus: bundled CLI extrakce může být pomalá při prvním spuštění (AV scan)
- `ANTHROPIC_API_KEY` musí být v env (SDK nepřijímá key přímo — prochází přes CC CLI)

---

## 6. Klíčové patchy pro STOPA integraci

### Patch 1: Budget-aware orchestrator

```python
# Nahradit Agent tool v /orchestrate:
async def spawn_subagent(task: str, tier: str, cwd: Path) -> dict:
    model_map = {"light": "haiku", "standard": "sonnet", "deep": "opus"}
    budget_map = {"light": 0.10, "standard": 0.50, "deep": 2.00}

    results = []
    async for msg in query(
        prompt=task,
        options=ClaudeAgentOptions(
            cwd=cwd,
            model=model_map[tier],
            max_budget_usd=budget_map[tier],
            permission_mode="acceptEdits",
            setting_sources=["project"]  # Načte CLAUDE.md
        )
    ):
        if isinstance(msg, ResultMessage):
            return {"cost": msg.total_cost_usd, "status": msg.subtype}
```

### Patch 2: Scheduled agent runner

```python
# Pro /schedule skill — spustit CC agent jako OS scheduled task:
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_scheduled_skill(skill: str, project_path: Path):
    """Spustit STOPA skill headless — bez otevřené CC session."""
    async for msg in query(
        prompt=f"/{skill}",
        options=ClaudeAgentOptions(
            cwd=project_path,
            permission_mode="acceptEdits",
            setting_sources=["user", "project"],
            max_turns=50,
            max_budget_usd=1.00
        )
    ):
        pass  # Výsledky se zapisují přes skill do memory souborů
```

### Patch 3: Hook-as-Python (místo shell hook skriptů)

```python
from claude_agent_sdk import HookMatcher

async def panic_detector(input_data, tool_use_id, context):
    """Python verze panic-detector.py hooku."""
    if input_data.get("tool_name") == "Edit":
        track_edit_rate()
        if is_desperation_pattern():
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "[calm-steering:red] Slow down."
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Edit", hooks=[panic_detector])]}
)
```

---

## 7. Hodnocení pro STOPA

### Scorecard

| Kritérium | Skóre | Poznámka |
|-----------|-------|----------|
| Funkčnost | 9/10 | Plné CC API přes Python, session mgmt, budget, hooks |
| Zralost | 6/10 | Pre-1.0, aktivní vývoj, 188 open issues, žádné breaking API |
| Dokumentace | 6/10 | README + examples dobré, chybí full API docs |
| Windows podpora | 8/10 | Funguje, bundled CLI, anyio cross-platform |
| Relevance pro STOPA | 10/10 | Přesně řeší scheduled agenty a orchestraci mimo session |
| Riziko závislosti | 7/10 | Officiální Anthropic repo, MIT, aktivní — nízké opuštění risk |
| **Celkem** | **7.7/10** | **Doporučeno pro integraci** |

### Doporučení

**INTEGROVAT — Priorita: Vysoká**

Konkrétní kroky:
1. `pip install claude-agent-sdk` do STOPA dev environment
2. Aktualizovat `/schedule` skill — použít SDK místo OS task scheduler s bare `claude -p`
3. Přidat `spawn_subagent_sdk()` helper do `/orchestrate` jako alternativu k Agent tool pro tiered budgeting
4. Experimentovat s Python hooks jako náhrada za hook shell skripty (výhoda: přístup k Python state)

**Čekat na:**
- Fix #768 (`bypassPermissions` + settings.json hooks) před nahrazením hook skriptů
- Stabilní session management API (v0.1.51+ vypadá solidně)
- Fix #425 (SDK MCP tools pod background subagenty) před heavy use v orchestraci

**Neřešit hned:**
- Nahrazení Agent tool kompletně — Agent tool zůstává lepší pro synchronní in-session sub-agenty
- Přechod na in-process MCP servery — current hook skripty fungují dobře

---

## Zdroje

- Repo: https://github.com/anthropics/claude-code-sdk-python
- PyPI: https://pypi.org/project/claude-agent-sdk/
- Changelog: https://github.com/anthropics/claude-code-sdk-python/blob/main/CHANGELOG.md
- Types API: https://github.com/anthropics/claude-code-sdk-python/blob/main/src/claude_agent_sdk/types.py
- Examples: https://github.com/anthropics/claude-code-sdk-python/tree/main/examples

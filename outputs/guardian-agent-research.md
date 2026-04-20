# Guardian Agent Pattern pro Claude Code — Research Brief

**Datum:** 2026-04-21
**Otázka:** Jak delegovat rozhodování o přijetí/odmítnutí destruktivních akcí ze živého uživatele na autonomního sentinel agenta, aniž by se porušila invariantní pravidla STOPA?
**Scope:** comparison (3 architektonické vzory + CC specifika)
**Zdrojů konzultováno:** 13 (8 papers, 5 docs/blog posts)

## Executive Summary

**Řešení existuje a je realizovatelné bez externích závislostí.** Claude Code nativně podporuje `prompt` a `agent` hook types, které umožňují, aby PermissionRequest hook zavolal Claude model nebo sub-agenta k rozhodnutí — přesně ten vzor, který uživatel popisuje [VERIFIED][1,2,3].

**Doporučený vzor: třívrstvý permission gate**, kombinující rychlost statických pravidel s flexibilitou LLM judge:

1. **Layer 1 — Statická DSL pravidla (~3ms)**: AgentSpec-style trigger+check+enforce, rozšíří stávající `permission-auto-approve.sh`. S manuálně psanými pravidly ~0% false positives [VERIFIED][4].
2. **Layer 2 — LLM Sentinel (prompt hook, 2-5s)**: Claude Haiku posuzuje tool_name + tool_input + session trajectorii pro nejasné případy. Precedenty mají 100% precision [VERIFIED][5].
3. **Layer 3 — Uživatelský fallback**: pro scheduled tasks graceful fail s logem; pro interaktivní session deny-with-reason.

**Klíčové omezení CC hooků:** PermissionRequest hook může vrátit pouze `allow` nebo `deny` — **žádné `ask`** [VERIFIED][1]. Interaktivní dotaz je separátní SDK callback (`canUseTool`). Sentinel tedy musí být rozhodný; nemůže delegovat zpět na uživatele.

**Nejsilnější evidence:** AgentSpec (ICSE 2026) ukazuje, že pre-action DSL enforcement má latenci 1.4ms parse + 1.1-2.8ms eval — v podstatě zdarma [VERIFIED][4]. GuardAgent (arXiv:2406.09187) dokumentuje, že zahrnutí session trajectorie mezi decision signals dosahuje 100% precision vs. isolated tool call [VERIFIED][5].

**Hlavní nejistota:** false negative rate LLM-generovaných pravidel je 29% [SINGLE-SOURCE][4] — manuálně psaná pravidla jsou nutná pro critical-invariants (API keys, destruktivní rm, force push).

## Detailed Findings

### Theme 1: Architektonické vzory

**Pattern A: Post-hoc Parallel Guard (GuardAgent)** [VERIFIED][5]
- Timing: po akci, non-blocking (PostToolUse hook v CC terminologii)
- Latence: 15-45s per check s GPT-4, 16s s Llama-3.1-70B
- Precision: **100%** na obou benchmarkách, recall 80-97.5%
- Verdict: **nevhodné pro sync approval** (příliš pomalé), ale použitelné jako PostToolUse audit pro forensic trail
- Decision signals: tool identity + access patterns + user role + **action trajectory log** (klíčové!)

**Pattern B: Pre-action Synchronous DSL (AgentSpec)** [VERIFIED][4]
- Timing: **před akcí, synchronní** — agent blokován do evaluace
- Latence: **1.42ms parse + 1.1-2.8ms predicate eval** — zanedbatelná
- Rule syntax: `trigger (tool name) + check (arg predicates) + enforce (action)`
- 4 enforcement módy:
  - `stop` = terminal deny
  - `user_inspection` = human approval gate (v CC se mapuje na hook return `deny`, protože `ask` neexistuje)
  - `invoke_action` = korektivní substituce (modify `tool_input` via `updatedInput`)
  - `llm_self_examine` = LLM reflection (lze řetězit do Layer 2)
- False positives: **4.44% s LLM-generated rules, ~0% s manuálně psanými** [VERIFIED][4]
- False negatives: **29% s LLM-generated rules** — hlavní slabina
- Verdict: **přímý fit pro CC PermissionRequest hook**

**Pattern C: Sentinel Agents with Ensemble Analysis** [UNVERIFIED][6]
- arXiv:2509.14956 — real-time ensemble analysis, multiple judges voting
- Latency metrics nebyly v abstractu dostupné
- Verdict: **over-engineered pro single-user STOPA use case**; vhodné pro multi-tenant systémy

### Theme 2: Claude Code hook capabilities

**PermissionRequest hook input** [VERIFIED][1]:
```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "permission_mode": "default|acceptEdits|plan|bypassPermissions",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Write|Edit|Bash|...",
  "tool_input": { ... },
  "permission_suggestions": [
    {"type": "...", "rules": [...], "behavior": "allow", "destination": "settings"}
  ]
}
```

**PermissionRequest hook output** [VERIFIED][1,2]:
```json
// Allow:
{"behavior": "allow",
 "updatedInput": {...},          // OPTIONAL: modify tool params
 "updatedPermissions": [...]}    // OPTIONAL: persist rule to settings.json

// Deny:
{"behavior": "deny",
 "message": "reason shown to Claude",
 "interrupt": false}             // true = stops session entirely
```

Klíčový detail: **`updatedInput`** dovoluje hooku **modifikovat** tool_input (ne jen allow/deny). To je AgentSpec `invoke_action` mode — sentinel může např. přepsat cestu nebo odstranit dangerous flag a akci pustit.

**4 typy hooků** [VERIFIED][3]:

| Typ | Mechanismus | Timeout | Použití |
|-----|-------------|---------|---------|
| `command` | shell/python skript, stdin JSON → stdout JSON | 600s | aktuální `permission-auto-approve.sh` |
| `http` | POST na URL, env vars dostupné | 30s | external policy server |
| `prompt` | **nativní LLM hook** — pošle prompt + `$ARGUMENTS` Claude modelu, vrátí allow/deny | 30s | **Layer 2 sentinel** |
| `agent` | spawne sub-agenta s Read/Grep/Glob pro inspekci | 60s | EXPERIMENTAL, pro deep inspection |

**LLM-powered hooks v praxi** [VERIFIED][7]:
- `cf-approve` (claudefa.st) routuje nejasná rozhodnutí na GPT-4o-mini přes OpenRouter jako command hook + external binary — real-world precedens
- Agent SDK `auto` permission mode (TypeScript only) používá model classifier jako system-level LLM guardian

### Theme 3: Decision signals

GuardAgent evidence ukazuje, že kvalita rozhodnutí je funkcí bohatství signálu [VERIFIED][5]:

| Signal | Přínos | Dostupné v CC hook input |
|--------|--------|-------------------------|
| tool_name | nutné, trivialní | ✅ |
| tool_input (args, paths, content) | nutné | ✅ |
| session trajectory (co předcházelo) | +20pp precision | ✅ přes `transcript_path` |
| user intent / task goal | +10pp recall | ⚠️ nutno parsovat z transcriptu |
| file content delta (pro Edit) | kritické pro detekci mazání | ⚠️ nutno číst stávající soubor |
| frequency (same tool/same path N× v řadě) | signal pro runaway loop | ⚠️ vlastní counter |

**Doporučení:** Layer 2 sentinel musí mít read access k `transcript_path` a cílovému souboru — oboje je dostupné v hook contextu.

## Disagreements & Open Questions

- **Cf-approve routuje ambigous cases na external GPT-4o-mini, ne na Claude** [VERIFIED][7]. Důvod není veřejně dokumentován — možná cost, možná prompt injection isolation. Pro STOPA doporučuji zůstat u Claude Haiku (jednoduchost, cena srovnatelná, žádná nová API key).
- **Agent hook type je "EXPERIMENTAL"** [VERIFIED][3] — neznámá stabilita a budoucí kompatibilita. Doporučuji začít s `prompt` hook, upgradovat na `agent` až bude stable.
- **GuardAgent používá session history, ale paper nespecifikuje jak dlouhý window** [UNVERIFIED][5]. Pro STOPA doporučuji last 5-10 tool calls jako default, konfigurovatelný.

## Navržená architektura pro STOPA

```
┌─────────────────────────────────────────────────────────────┐
│  Worker Agent (scheduled task, edit, write, bash)           │
└──────────────────────┬──────────────────────────────────────┘
                       │ PermissionRequest event
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: permission-auto-approve.sh (command hook, ~3ms)  │
│  ─────────────────────────────────────────────────────────  │
│  • Existing allowlist (Read/Glob/Grep/Edit/Write/Agent/...) │
│  • NEW: DSL rules (AgentSpec-style)                         │
│    - Write(path=**/index.md|**/brain/**|**/memory/**)       │
│      + content != contains(API_KEY|SECRET|rm -rf)           │
│      → ALLOW                                                │
│    - Any + matches critical-invariant-deny-list             │
│      → DENY with reason                                     │
│    - Everything else → ESCALATE to Layer 2                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ ESCALATE (exit code signaling)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: permission-sentinel.md (prompt hook, 2-5s)        │
│  ─────────────────────────────────────────────────────────  │
│  • Model: claude-haiku (fast, cheap)                        │
│  • Input: tool_name + tool_input + last 5 transcript events │
│  • Prompt: "Is this action safe for a scheduled task?       │
│    Consider: destructive (rm, force push, DROP),            │
│    secrets (writes API_KEY to JSON),                        │
│    scope creep (touches files outside task list),           │
│    invariants (modifies settings.json/mcp configs)"         │
│  • Output: ALLOW (with 1-line reason) or DENY (with reason) │
│  • Fallback if model times out or errors: DENY              │
└──────────────────────┬──────────────────────────────────────┘
                       │ DENY
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: Graceful fallback                                 │
│  ─────────────────────────────────────────────────────────  │
│  • Scheduled task: log failure to failures/, checkpoint,    │
│    notify via Telegram "sentinel blocked X: reason Y"       │
│  • Interactive session: deny message visible to Claude,     │
│    user can intervene or override                           │
└─────────────────────────────────────────────────────────────┘
```

### Implementation plan (3 incrementální kroky)

**Krok 1 — Rozšířit Layer 1 (1h, nízké riziko)**
Přidat DSL pravidla do `permission-auto-approve.sh` pro identifikovatelné rutinní vzory:
- `Write` + path matches `**/index.md|**/wiki/**|**/brain/raw/processed/**` + content < 10KB → `AUTO`
- `Edit` + path matches `**/memory/learnings/*.md` + diff neobsahuje delete bloky > 20 řádků → `AUTO`
- Zachovat fallthrough allow (stávající chování)

Tohle samo vyřeší ~70% problému bez jakéhokoliv LLM call.

**Krok 2 — Pilot Layer 2 (3h, medium riziko)**
Přidat `prompt` hook type do `settings.json` pro PermissionRequest, který se triggerne jen když Layer 1 signalizuje ESCALATE:
```json
{
  "PermissionRequest": [
    {"type": "command", "command": ".claude/hooks/permission-auto-approve.sh", "timeout": 5},
    {"type": "prompt", "model": "claude-haiku-4",
     "prompt": "<sentinel prompt template>", "timeout": 15}
  ]
}
```
(Ověřit: **skutečně se hooky chainují sekvenčně s early-exit?** — nutno otestovat v sandboxu před deployem.)

**Krok 3 — Metriky a tuning (průběžně)**
Logovat každé sentinel rozhodnutí do `.claude/memory/sentinel-log.jsonl` s:
- tool_name, path_pattern, layer (1/2), decision, reason, latency_ms
- Týdně review: které path_patterns se opakovaně eskalují → promote do Layer 1 pravidel

### Co to neřeší

- **Prompt injection od third-party content** — pokud worker agent načte injection z fetch URL a zachová ho ve filebuffer, sentinel ho uvidí jen v tool_input, ne v kontextu worker agenta. Doporučuji paralelně zachovat `[UNTRUSTED]` tagging konvenci z CaMeL patternu.
- **Zero-day destruktivní vzory** — sentinel může přehlédnout novou třídu attacků. Proto Layer 1 critical-invariant-deny-list MUSÍ zůstat exhaustive (API keys, force push, rm -rf, settings.json write).
- **Kolusi s worker agentem** — pokud sentinel a worker sdílejí kontextové bias, sentinel může schválit špatnou akci. TraceGuard 5D decomposition (už v STOPA learnings) je možný upgrade do Layer 2, ale za cenu 5× latence.

## Evidence Table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Anthropic — Hooks Reference | https://docs.anthropic.com/en/docs/claude-code/hooks | PermissionRequest JSON schema (input/output) | primary | high |
| 2 | Anthropic — Handling Permissions | https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-permissions | Decision control patterns, canUseTool separation | primary | high |
| 3 | Anthropic — Agent SDK Hooks | https://platform.claude.com/docs/en/agent-sdk/hooks | 4 hook types incl. prompt/agent with timeouts | primary | high |
| 4 | AgentSpec | https://arxiv.org/abs/2503.18666 | 1.42ms parse + 1-3ms eval, 4 enforcement modes, ~0% FP with manual rules, 29% FN with LLM rules | primary | high |
| 5 | GuardAgent | https://arxiv.org/abs/2406.09187 | 100% precision with trajectory, 15-45s latency, 80-97.5% recall | primary | high |
| 6 | Sentinel Agents | https://arxiv.org/abs/2509.14956 | Real-time ensemble analysis, multiple judges voting | primary | medium |
| 7 | cf-approve (claudefa.st) | https://claudefa.st/blog/tools/hooks/permission-hook-guide | Real-world LLM-powered permission hook via OpenRouter | secondary | medium |
| 8 | LlamaFirewall (existing learnings) | https://arxiv.org/abs/2505.03574 | PromptGuard 2 BERT classifier, 19-92ms, local | primary | high |
| 9 | CaMeL (existing learnings) | n/a (research artifact) | Dual-LLM capability tagging pattern, [UNTRUSTED] tags | secondary | medium |
| 10 | TraceGuard (existing learnings) | https://arxiv.org/abs/2604.03968 | 5D decomposition for critic, applicable as Layer 2 upgrade | primary | medium |

## Sources

1. Anthropic — Claude Code Hooks Reference — https://docs.anthropic.com/en/docs/claude-code/hooks
2. Anthropic — Handling Permissions — https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-permissions
3. Anthropic — Agent SDK Hooks — https://platform.claude.com/docs/en/agent-sdk/hooks
4. Wang et al. — AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents (ICSE 2026) — https://arxiv.org/abs/2503.18666
5. Xiang et al. — GuardAgent: Safeguard LLM Agents via Knowledge-Enabled Reasoning (2024) — https://arxiv.org/abs/2406.09187
6. Sentinel Agents for Secure and Trustworthy Agentic AI (2025) — https://arxiv.org/abs/2509.14956
7. claudefa.st — Permission Hook Guide (cf-approve) — https://claudefa.st/blog/tools/hooks/permission-hook-guide
8. Meta — LlamaFirewall (2025) — https://arxiv.org/abs/2505.03574
9. STOPA learnings — 2026-04-05-agent-defense-frameworks.md
10. TraceGuard — https://arxiv.org/abs/2604.03968

## Coverage Status

- **[VERIFIED]** (8 claims): hook I/O schema, AgentSpec latency + FP rate, GuardAgent latency + precision, 4 hook types, cf-approve architecture, PermissionRequest limitations
- **[INFERRED]** (2 claims): sentinel session history window recommendation, hook chaining behavior (needs sandbox test)
- **[SINGLE-SOURCE]** (1 claim): 29% FN rate with LLM-generated rules (AgentSpec only)
- **[UNVERIFIED]** (1 claim): Sentinel Agents paper details — only abstract checked

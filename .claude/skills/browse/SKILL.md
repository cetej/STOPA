---
name: browse
description: Use when browsing web pages for data extraction, form filling, testing, or monitoring. Trigger on 'browse', 'open page', 'extract from site'. Do NOT use for web search or static fetch.
user-invocable: true
argument-hint: "[extract|fill|test|monitor] <url> [what to do]"
tags: [web, osint]
requires: [agent-browser]
model: sonnet
maxTurns: 25
effort: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
  - AskUserQuestion
  - mcp__Claude_in_Chrome__tabs_context_mcp
  - mcp__Claude_in_Chrome__tabs_create_mcp
  - mcp__Claude_in_Chrome__tabs_close_mcp
  - mcp__Claude_in_Chrome__navigate
  - mcp__Claude_in_Chrome__read_page
  - mcp__Claude_in_Chrome__find
  - mcp__Claude_in_Chrome__get_page_text
  - mcp__Claude_in_Chrome__computer
  - mcp__Claude_in_Chrome__form_input
  - mcp__Claude_in_Chrome__javascript_tool
  - mcp__Claude_in_Chrome__read_console_messages
  - mcp__Claude_in_Chrome__read_network_requests
---

# Browse — Browser Automation Agent

You are a browser automation agent. You use `agent-browser` CLI as the primary backend
and fall back to Claude in Chrome MCP for interactive sessions requiring visual feedback.

<!-- CACHE_BOUNDARY -->

## Parse Arguments

```
$ARGUMENTS format:
  extract <url> [what]       — Navigate to URL, extract specific data
  fill <url> [instructions]  — Fill a form according to instructions
  test <url> [checklist]     — Test UI: snapshot, console errors, network
  monitor <url> [selector]   — Check page state, return status report
  <url>                      — Navigate and describe what you see
  (empty)                    — Ask user what to do
```

Parse `$ARGUMENTS` and determine the mode. If no mode keyword, infer from context.

## Backend Selection

### Priority 1: agent-browser CLI (default)

agent-browser is a Rust CLI using Chrome DevTools Protocol. Low token overhead,
fast daemon, works headless and with Electron apps.

**Core workflow — snapshot → refs → act:**
```bash
agent-browser open <url>
agent-browser snapshot -i -c          # Interactive elements with refs (@e1, @e2...)
agent-browser click @e2               # Click by ref
agent-browser fill @e3 "value"        # Fill input by ref
agent-browser get text @e1            # Extract text from element
agent-browser eval "document.title"   # Run JavaScript
agent-browser screenshot [path]       # Visual proof
agent-browser console                 # Console logs
agent-browser close                   # Cleanup
```

**Connecting to existing Chrome (authenticated sessions):**
```bash
agent-browser --auto-connect snapshot -i    # Auto-discover running Chrome via CDP
agent-browser --cdp 9222 snapshot -i        # Connect to specific CDP port
```

**Connecting to Electron apps (Discord, VSCode, Slack):**
```bash
# Find CDP port: check task manager or launch with --remote-debugging-port
agent-browser --cdp <port> snapshot -i
```

**Useful options:**
- `--json` — structured JSON output for programmatic parsing
- `-i` — interactive elements only (reduces noise)
- `-c` — compact (removes empty structural elements)
- `--session <name>` — isolated named session
- `--profile <path>` — persistent login across restarts
- `--headed` — show browser window (for debugging)
- `--allowed-domains <list>` — restrict navigation

**Batch execution (multiple commands at once):**
```bash
agent-browser open <url> && agent-browser wait --load networkidle && agent-browser snapshot -i -c
```

### Priority 2: Claude in Chrome MCP (fallback)

Use ONLY when:
- User explicitly asks for visual/interactive browsing with screenshot feedback
- agent-browser is unavailable or cannot connect

```
1. Call mcp__Claude_in_Chrome__tabs_context_mcp (createIfEmpty: true)
2. Use Chrome in Chrome tools for the session
```

### Backend Decision Rule

```
Need Electron app control?           → agent-browser --cdp <port>
Need authenticated session?          → agent-browser --auto-connect OR --cdp 9222
Need headless extraction/testing?    → agent-browser (default headless)
Need user to see what's happening?   → Claude in Chrome
agent-browser not installed?         → Claude in Chrome
```

Do NOT mix backends in one session.

## Mode: extract

1. `agent-browser open <url>`
2. `agent-browser wait --load networkidle` (if JS-heavy page)
3. `agent-browser snapshot -i -c` — parse the accessibility tree
4. `agent-browser get text @ref` for specific elements, or `agent-browser eval "document.querySelector('...').textContent"` for complex extraction
5. Present findings in structured format

If scrolling needed: `agent-browser scroll down [px]` then re-snapshot.
If pagination: loop through pages using click on next/page refs.

## Mode: fill

1. `agent-browser open <url>`
2. `agent-browser snapshot -i` — identify form fields and their refs
3. `agent-browser fill @ref "value"` for each field
4. `agent-browser screenshot filled-form.png` — proof of what was filled
5. **STOP before submit** — show the user what you filled and ask for confirmation

### Fill Safety Rules
- NEVER enter passwords, credit card numbers, SSN, or bank account data
- NEVER enter API keys or tokens
- Basic info (name, email, address, phone) is OK if user provided it
- If a field asks for sensitive data, skip it and tell the user to fill it manually

## Mode: test

1. `agent-browser open <url>`
2. `agent-browser wait --load networkidle`
3. `agent-browser snapshot` — check page structure
4. `agent-browser console` — check for errors
5. `agent-browser errors` — page errors specifically
6. If checklist provided, verify each item using snapshot + get text
7. Compile report:

```markdown
## UI Test Report: <url>

### Page Status
- Loaded: yes/no
- Title: (from `agent-browser get title`)

### Console
- Errors: N
- Warnings: N
- Details: ...

### Network
- Failed requests: N (check with `agent-browser network requests --filter "4xx|5xx"`)

### Checklist
- [ ] Item 1: PASS/FAIL
- [ ] Item 2: PASS/FAIL
```

## Mode: monitor

1. `agent-browser open <url>`
2. Check for specific content using `agent-browser snapshot` + grep for selector/text
3. `agent-browser screenshot` — visual proof
4. Report: page status, target element state, any errors

## agent-browser Quick Reference

| Task | Command |
|------|---------|
| Open URL | `agent-browser open <url>` |
| Interactive snapshot | `agent-browser snapshot -i -c` |
| Full snapshot | `agent-browser snapshot` |
| Click element | `agent-browser click @ref` |
| Fill input | `agent-browser fill @ref "text"` |
| Type (append) | `agent-browser type @ref "text"` |
| Press key | `agent-browser press Enter` |
| Get text | `agent-browser get text @ref` |
| Get page title | `agent-browser get title` |
| Get current URL | `agent-browser get url` |
| Run JavaScript | `agent-browser eval "expression"` |
| Screenshot | `agent-browser screenshot [path]` |
| Console logs | `agent-browser console` |
| Page errors | `agent-browser errors` |
| Wait for element | `agent-browser wait "selector"` |
| Wait for load | `agent-browser wait --load networkidle` |
| Scroll | `agent-browser scroll down [px]` |
| Find by role | `agent-browser find role button click --name Submit` |
| Find by text | `agent-browser find text "Login" click` |
| Diff snapshots | `agent-browser diff snapshot` |
| Close session | `agent-browser close` |
| Close all | `agent-browser close --all` |

## Output

Always end with a structured summary. Include:
- URL visited
- Backend used (agent-browser / Chrome in Chrome)
- What was done
- Key findings or proof (screenshot path)

## Rules

1. **Privacy first** — never extract or fill sensitive financial/identity data
2. **Confirm before irreversible actions** — submit, send, publish, delete, purchase
3. **Screenshot as proof** — take a screenshot after meaningful actions
4. **Clean up** — `agent-browser close` when done (releases daemon resources)
5. **No memory writes** — output is ephemeral, goes to stdout only
6. **Respect robots** — if a site blocks automation or shows CAPTCHA, stop and tell the user
7. **Cost aware** — don't loop on failed navigation; 3 retries max then report failure
8. **Prefer snapshot over screenshot** — text tree is cheaper than image parsing

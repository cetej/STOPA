---
name: browse
description: Use when browsing authenticated Chrome pages for data extraction or form filling. Trigger on 'browse', 'open page', 'extract from site'. Do NOT use for web search or static fetch.
argument-hint: <URL or description of what to browse>
user-invocable: true
allowed-tools: Read, Write, Bash
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Agent
---

# Browse — Chrome Automation via MCP

You interact with the user's authenticated Chrome browser to extract data, fill forms, or navigate pages that require login. You use the Claude in Chrome MCP tools.

## When to Use This vs. Other Tools

| Need | Tool |
|------|------|
| Public web page content | `WebFetch` (no browser needed) |
| Web search for information | `WebSearch` (no browser needed) |
| Authenticated page (Gmail, dashboards, internal tools) | **This skill** (`/browse`) |
| Form filling on authenticated sites | **This skill** |
| Screenshot for visual verification | **This skill** |

## Process

### Step 1: Get Browser Context

Call `mcp__Claude_in_Chrome__tabs_context_mcp` with `createIfEmpty: true` to get available tabs.

### Step 2: Navigate or Use Existing Tab

- If user provides a URL → create a new tab (`mcp__Claude_in_Chrome__tabs_create_mcp`) and navigate
- If user says "look at the current page" → use existing tab from context

### Step 3: Read the Page

Use `mcp__Claude_in_Chrome__read_page` to get the accessibility tree. This is more reliable than screenshots for understanding page structure.

For specific elements: `mcp__Claude_in_Chrome__find` with natural language queries.

### Step 4: Interact (if needed)

- **Click**: `mcp__Claude_in_Chrome__computer` with action: `left_click`
- **Type**: `mcp__Claude_in_Chrome__computer` with action: `type`
- **Fill form**: `mcp__Claude_in_Chrome__form_input`
- **Screenshot**: `mcp__Claude_in_Chrome__computer` with action: `screenshot`

### Step 5: Extract and Report

Extract the relevant data and present it to the user in a clean format.

If saving data: write to `outputs/` directory (never overwrite existing files).

## Error Handling

- **No Chrome connection**: Report "Chrome MCP not connected. Make sure Claude in Chrome extension is installed and active."
- **Page requires login**: Report what login is needed, do NOT attempt to enter credentials
- **Element not found**: Take a screenshot, report what's visible, suggest alternatives
- **Page loading slow**: Wait up to 10 seconds (`mcp__Claude_in_Chrome__computer` action: `wait`)

## Safety Rules

1. **NEVER enter passwords, API keys, or credentials** — tell the user to do it themselves
2. **NEVER submit forms with financial data** — ask user to review and submit
3. **NEVER click "delete", "remove", or destructive actions** without explicit user confirmation
4. **Screenshots may contain sensitive data** — do not save to shared locations
5. **Respect robots.txt and rate limits** — don't automate rapid-fire requests

## Rules

1. **Prefer read_page over screenshots** — accessibility tree is faster and more reliable
2. **Announce what you're doing** — "I'm clicking the 'Export' button" before doing it
3. **One action at a time** — don't chain multiple interactions without checking results
4. **Clean up** — close tabs you created when done (unless user wants to keep them)

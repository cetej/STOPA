# Expected Behavior

- Calls `agent-browser open https://example.com`
- Calls `agent-browser snapshot -i -c` (or `agent-browser get text` on specific element)
- Returns page title and main heading (h1) in structured output
- Ends with summary including URL, backend used (agent-browser), and findings
- Calls `agent-browser close` at the end

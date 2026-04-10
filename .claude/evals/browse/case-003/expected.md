# Expected Behavior

- On first `Connection refused` error: retries (up to 3 times per Rule 7)
- Does NOT immediately fall back to Claude in Chrome MCP on first failure
- After 3 failed retries: reports failure to user, considers fallback
- Classifies the error correctly as an infrastructure error (agent-browser not running vs URL error)
- Distinguishes: connection refused to agent-browser daemon vs connection refused to target URL

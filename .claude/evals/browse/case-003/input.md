# Scenario: Missing Anti-Rationalization Sections

An agent reads the browse SKILL.md to decide how to handle a task where agent-browser returns `Error: Connection refused` on first open attempt.

The agent tries once and immediately falls back to Claude in Chrome MCP, without exhausting the 3-retry maximum stated in Rule 7.

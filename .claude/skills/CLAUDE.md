# Skills Development Rules

## Sync invariant
`commands/<name>.md` and `skills/<name>/SKILL.md` are two copies of the same file.
When editing one, ALWAYS update the other. Desync causes unpredictable behavior.

## YAML frontmatter
Required fields: `name`, `description`, `user-invocable`

### description field (CRITICAL)
- MUST start with "Use when..."
- Contains trigger conditions and exclusions ONLY
- MUST NOT summarize workflow, list steps, or describe mechanics
- Reason: workflow summaries cause Claude to skip reading the full skill body

### Other fields
- `allowed-tools`: least privilege — only tools the skill actually needs
- `tags`: cross-cutting capability tags (see tag taxonomy in `rules/skill-files.md`)
- `requires`: runtime deps — env vars (UPPER_CASE), CLI tools (lowercase), MCP servers (`mcp:name`)
- `model`: haiku for validation, sonnet for reasoning, opus for complex analysis
- If skill writes to memory: must be stated in instructions
- If skill spawns sub-agents: must specify model and reason

## Conventions
- English for technical instructions, Czech for user-facing text
- Skills develop in STOPA first, never in target projects
- New runbook patterns go to `docs/runbooks/`, not inline in skills

#!/usr/bin/env bash
# PostToolUse hook (matcher: Skill): Reactive Skill Chain Engine
# Reads skill completion status, matches against skill-chains.json,
# injects context for the next step in the chain.
#
# Condition levels:
#   auto    — strong injection: "Next step: ..."
#   suggest — soft suggestion: "Consider running ..."
#   ask     — question: "Want me to run ...?"

# Profile: standard
source .claude/hooks/lib/profile-check.sh 2>/dev/null && require_profile standard

TOOL="${CLAUDE_TOOL_NAME:-}"
INPUT="${CLAUDE_TOOL_INPUT:-}"
OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"
CHAINS_FILE=".claude/hooks/skill-chains.json"

# Only react to Skill tool
[ "$TOOL" != "Skill" ] && exit 0

# Need chains file
[ ! -f "$CHAINS_FILE" ] && exit 0

# All logic in Python — avoids grep -P issues on Windows Git Bash
python3 -c "
import json, re, sys, os

tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '')
tool_output = os.environ.get('CLAUDE_TOOL_OUTPUT', '')[:2000]
chains_file = '.claude/hooks/skill-chains.json'

# Extract skill name from input JSON
try:
    input_data = json.loads(tool_input)
    skill = input_data.get('skill', '')
except (json.JSONDecodeError, TypeError):
    m = re.search(r'\"skill\"\s*:\s*\"([^\"]+)\"', tool_input)
    skill = m.group(1) if m else ''

if not skill:
    sys.exit(0)

try:
    with open(chains_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except (json.JSONDecodeError, OSError):
    sys.exit(0)

for chain in data.get('chains', []):
    trigger = chain.get('trigger', {})
    if trigger.get('skill', '').lower() != skill.lower():
        continue
    pattern = trigger.get('status_pattern', '')
    if not pattern:
        continue
    if not re.search(pattern, tool_output, re.IGNORECASE):
        continue

    next_step = chain.get('next', '')
    condition = chain.get('condition', 'suggest')
    desc = chain.get('description', '')

    if condition == 'auto':
        msg = f'Chain triggered: {desc}. Next step: {next_step}'
    elif condition == 'suggest':
        msg = f'Chain suggestion: {desc}. Consider running: {next_step}'
    elif condition == 'ask':
        msg = f'Chain asks: {desc}. Want me to run {next_step}?'
    else:
        continue

    print(json.dumps({'additionalContext': msg}))
    sys.exit(0)
"

#!/usr/bin/env python3
"""PreToolUse hook: Deterministic security pattern scanner.

Scans content of Write/Edit operations for dangerous patterns BEFORE
the edit lands. Complements on-demand /security-review with always-on
deterministic checking.

Two layers:
  1. Regex patterns (always available, ~50ms)
  2. CodeShield/Semgrep CWE detection (when available, ~70ms)

Severity levels:
  BLOCK  — pattern is almost never legitimate in AI-generated code
  WARN   — pattern has legitimate uses but warrants attention

Exit behavior:
  - BLOCK: outputs JSON {"decision":"block","reason":"..."}, exit 0
  - WARN:  outputs warning to stderr, exit 0 (allows edit)
  - CLEAN: silent exit 0
"""
import json
import re
import sys
import os

# ---------------------------------------------------------------------------
# Pattern definitions
# Each tuple: (compiled_regex, severity, message, file_filter)
# file_filter: None = all files, or a regex matching file extensions
# ---------------------------------------------------------------------------

PY_EXT = re.compile(r'\.(py|pyw)$', re.IGNORECASE)
JS_EXT = re.compile(r'\.(js|jsx|ts|tsx|mjs|cjs|vue|svelte)$', re.IGNORECASE)
ANY_EXT = None  # matches all files

PATTERNS = [
    # --- BLOCK severity (almost never legitimate in AI-written code) ---

    # Hardcoded secrets — API keys, tokens, passwords in string literals
    (
        re.compile(
            r'''(?:api[_-]?key|api[_-]?secret|auth[_-]?token|access[_-]?token'''
            r'''|secret[_-]?key|private[_-]?key|password|passwd)'''
            r'''\s*[=:]\s*["'][A-Za-z0-9+/=_\-]{16,}["']''',
            re.IGNORECASE
        ),
        'BLOCK',
        'Hardcoded secret/API key detected. Use environment variables instead.',
        ANY_EXT,
    ),
    # sk-... pattern (OpenAI/Anthropic keys)
    (
        re.compile(r'''["']sk-[A-Za-z0-9]{20,}["']'''),
        'BLOCK',
        'Hardcoded API key (sk-...) detected. Use environment variables.',
        ANY_EXT,
    ),

    # pickle.loads on untrusted data
    (
        re.compile(r'pickle\.loads?\s*\('),
        'BLOCK',
        'pickle.load(s) is unsafe — allows arbitrary code execution on deserialization. Use json or msgpack.',
        PY_EXT,
    ),

    # yaml.load without SafeLoader
    (
        re.compile(r'yaml\.load\s*\([^)]*\)\s*(?!.*Loader\s*=)'),
        'WARN',
        'yaml.load() without explicit Loader= is unsafe. Use yaml.safe_load() or Loader=SafeLoader.',
        PY_EXT,
    ),

    # --- WARN severity (legitimate uses exist, but flag for awareness) ---

    # eval/exec in Python
    (
        re.compile(r'\beval\s*\('),
        'WARN',
        'eval() detected — allows arbitrary code execution. Consider ast.literal_eval() or safer alternatives.',
        PY_EXT,
    ),
    (
        re.compile(r'\bexec\s*\('),
        'WARN',
        'exec() detected — allows arbitrary code execution. Is this intentional?',
        PY_EXT,
    ),

    # os.system / subprocess with shell=True
    (
        re.compile(r'os\.system\s*\('),
        'WARN',
        'os.system() is vulnerable to command injection. Use subprocess.run() with shell=False.',
        PY_EXT,
    ),
    (
        re.compile(r'subprocess\.\w+\s*\([^)]*shell\s*=\s*True'),
        'WARN',
        'subprocess with shell=True is vulnerable to command injection. Use shell=False with list args.',
        PY_EXT,
    ),

    # __import__ — dynamic imports
    (
        re.compile(r'__import__\s*\('),
        'WARN',
        '__import__() detected — dynamic imports can be a security risk.',
        PY_EXT,
    ),

    # SQL string interpolation (Python)
    (
        re.compile(
            r'''(?:f["']|\.format\s*\().*(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b''',
            re.IGNORECASE
        ),
        'WARN',
        'SQL with string interpolation detected — use parameterized queries to prevent SQL injection.',
        PY_EXT,
    ),

    # innerHTML / dangerouslySetInnerHTML (JS/TS)
    (
        re.compile(r'\.innerHTML\s*='),
        'WARN',
        'innerHTML assignment detected — XSS risk. Use textContent or sanitize input.',
        JS_EXT,
    ),
    (
        re.compile(r'dangerouslySetInnerHTML'),
        'WARN',
        'dangerouslySetInnerHTML detected — XSS risk. Ensure input is sanitized.',
        JS_EXT,
    ),

    # document.write (JS)
    (
        re.compile(r'document\.write\s*\('),
        'WARN',
        'document.write() detected — XSS risk and performance issue.',
        JS_EXT,
    ),

    # eval in JS/TS
    (
        re.compile(r'\beval\s*\('),
        'WARN',
        'eval() detected — allows arbitrary code execution.',
        JS_EXT,
    ),

    # new Function() in JS
    (
        re.compile(r'new\s+Function\s*\('),
        'WARN',
        'new Function() detected — equivalent to eval(), allows arbitrary code execution.',
        JS_EXT,
    ),
]

# ---------------------------------------------------------------------------
# Hook logic
# ---------------------------------------------------------------------------

def extract_content(tool_input: dict, tool_name: str) -> str:
    """Extract the content being written/edited from tool input."""
    # Write tool: "content" field
    if tool_name in ('Write', 'mcp__filesystem__write_file'):
        return tool_input.get('content', '')

    # Edit tool: "new_string" field
    if tool_name in ('Edit', 'mcp__filesystem__edit_file'):
        return tool_input.get('new_string', tool_input.get('newText', ''))

    return ''


def extract_file_path(tool_input: dict) -> str:
    """Extract file path from tool input."""
    path = tool_input.get('file_path', tool_input.get('path', ''))
    # Normalize backslashes
    return path.replace('\\', '/')


def scan_content(content: str, file_path: str) -> list:
    """Scan content for dangerous patterns. Returns list of (severity, message)."""
    findings = []

    for pattern, severity, message, file_filter in PATTERNS:
        # Skip if file extension doesn't match filter
        if file_filter is not None and not file_filter.search(file_path):
            continue

        if pattern.search(content):
            findings.append((severity, message))

    return findings


# ---------------------------------------------------------------------------
# CodeShield layer — Semgrep-based CWE detection (LlamaFirewall)
# Requires: pip install llamafirewall + semgrep-core binary in PATH
# On Windows: semgrep-core may not be available — graceful fallback
# ---------------------------------------------------------------------------

_CODESHIELD_AVAILABLE = False

try:
    from codeshield.cs import CodeShield as _CS
    _CODESHIELD_AVAILABLE = True
except Exception:
    pass  # ImportError or semgrep-core missing — skip silently

# Map CodeShield language names
_EXT_TO_LANG = {
    '.py': 'python', '.pyw': 'python',
    '.js': 'javascript', '.jsx': 'javascript', '.mjs': 'javascript', '.cjs': 'javascript',
    '.ts': 'typescript', '.tsx': 'typescript',
}


def scan_codeshield(content: str, file_path: str) -> list:
    """Run CodeShield CWE scan. Returns list of (severity, message)."""
    if not _CODESHIELD_AVAILABLE:
        return []

    import asyncio

    ext = os.path.splitext(file_path)[1].lower()
    lang = _EXT_TO_LANG.get(ext)
    if not lang:
        return []

    findings = []
    try:
        result = asyncio.run(_CS.scan_code(content, language=lang))
        if result and hasattr(result, 'issues_found') and result.issues_found:
            for issue in result.issues_found:
                severity = 'WARN'  # CodeShield findings are advisory in this context
                cwe = getattr(issue, 'cwe_id', 'unknown')
                desc = getattr(issue, 'description', str(issue))
                findings.append((severity, f"CodeShield CWE-{cwe}: {desc}"))
    except Exception:
        pass  # CodeShield failure must never crash the hook

    return findings


def main():
    # Read tool input from stdin
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        sys.exit(0)

    try:
        tool_input = json.loads(raw_input)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = os.environ.get('CLAUDE_TOOL_NAME', 'unknown')

    # Only process write operations
    if tool_name not in ('Write', 'Edit',
                         'mcp__filesystem__write_file',
                         'mcp__filesystem__edit_file'):
        sys.exit(0)

    file_path = extract_file_path(tool_input)

    # Project boundary guard — skip files outside STOPA
    from lib.project_guard import is_outside_project
    if is_outside_project(file_path):
        sys.exit(0)

    content = extract_content(tool_input, tool_name)

    if not content:
        sys.exit(0)

    # Skip scanning hook/config files themselves (avoid self-referential blocks)
    if '.claude/hooks/' in file_path or file_path.endswith('security-scan.py'):
        sys.exit(0)

    findings = scan_content(content, file_path)

    # Layer 2: CodeShield (Semgrep-based CWE detection)
    # Only for .py/.js/.ts files, graceful fallback if unavailable
    if PY_EXT.search(file_path) or JS_EXT.search(file_path):
        cs_findings = scan_codeshield(content, file_path)
        findings.extend(cs_findings)

    if not findings:
        sys.exit(0)

    # Check for BLOCK-severity findings
    blocks = [msg for sev, msg in findings if sev == 'BLOCK']
    warns = [msg for sev, msg in findings if sev == 'WARN']

    if blocks:
        # Block the edit — first BLOCK finding is the reason
        reason = f"\U0001f6a8 Security scan: {blocks[0]}"
        if len(blocks) > 1:
            reason += f" (+{len(blocks) - 1} more)"
        print(json.dumps({"decision": "block", "reason": reason}))
    elif warns:
        # Warn but allow — print all warnings to stderr
        for msg in warns:
            print(f"\u26a0\ufe0f Security scan: {msg}", file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()

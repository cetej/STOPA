#!/usr/bin/env python3
"""MCP config auditor — local security scan without external API.

Phase 4 defense (AI Agent Traps, DeepMind 2026-04-01).
Scans MCP configuration files for:
  1. Tool description poisoning patterns (hidden instructions in docstrings)
  2. Suspicious server configurations (unknown sources, pinned old versions)
  3. Environment variable exposure (secrets in plain text)
  4. Config drift detection (hash comparison against pinned baseline)

Usage:
  python scripts/mcp-audit.py                    # scan default configs
  python scripts/mcp-audit.py --pin              # save current state as baseline
  python scripts/mcp-audit.py --config path.json # scan specific config
  python scripts/mcp-audit.py --full             # also run snyk-agent-scan if SNYK_TOKEN set

Exit codes: 0 = clean, 1 = warnings found, 2 = critical issues
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Default MCP config locations
DEFAULT_CONFIGS = [
    Path.home() / ".claude" / "mcp.json",
    Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",
]

BASELINE_PATH = Path(".claude/memory/intermediate/mcp-baseline.json")

# Known trusted MCP server packages (npm)
TRUSTED_PACKAGES = {
    "@modelcontextprotocol/server-brave-search",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-windows",
    "@playwright/mcp",
    "@anthropic-ai/claude-code-mcp",
    "@anthropic-ai/claude-in-chrome-mcp",
    "@anthropic-ai/claude-preview-mcp",
    "@upstash/context7-mcp",
    "youtube-transcript-mcp",
}

# Suspicious patterns in MCP tool descriptions (tool poisoning)
TOOL_POISON_PATTERNS = [
    (re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions?", re.I),
     "instruction override in tool description"),
    (re.compile(r"(?:system|admin)\s*(?:prompt|message|override)\s*:", re.I),
     "fake system message in tool description"),
    (re.compile(r"(?:do\s+not|don't)\s+(?:tell|inform|warn)\s+the\s+user", re.I),
     "secrecy directive in tool description"),
    (re.compile(r"(?:send|forward|exfiltrate)\s+.*(?:data|credentials|tokens)", re.I),
     "exfiltration directive in tool description"),
    (re.compile(r"(?:you\s+must|always)\s+(?:call|invoke|use)\s+this\s+tool\s+(?:first|before)", re.I),
     "forced tool invocation pattern"),
]


def load_config(path: Path) -> dict | None:
    """Load and parse MCP config file."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ERROR: Cannot parse {path}: {e}")
        return None


def compute_config_hash(config: dict) -> str:
    """Compute deterministic hash of config for drift detection."""
    canonical = json.dumps(config, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def check_env_exposure(server_name: str, server_config: dict) -> list[str]:
    """Check for secrets exposed in plain text env vars."""
    findings = []
    env_vars = server_config.get("env", {})
    for key, value in env_vars.items():
        if not isinstance(value, str):
            continue
        # Check for actual secret values (not env var references)
        secret_keys = {"key", "token", "secret", "password", "credential", "auth"}
        key_lower = key.lower()
        if any(s in key_lower for s in secret_keys):
            if len(value) > 10 and not value.startswith("${") and not value.startswith("$"):
                findings.append(
                    f"WARN: [{server_name}] env var {key} contains plain-text secret "
                    f"({len(value)} chars). Use env var reference instead."
                )
    return findings


def check_server_trust(server_name: str, server_config: dict) -> list[str]:
    """Check if server comes from a trusted source."""
    findings = []
    args = server_config.get("args", [])
    command = server_config.get("command", "")

    # Extract package name from npx args
    package = None
    for i, arg in enumerate(args):
        if arg == "-y" or arg.startswith("-"):
            continue
        package = arg.split("@latest")[0].split("@")[0] if "@" in arg else arg
        break

    if command == "npx" and package and package not in TRUSTED_PACKAGES:
        findings.append(
            f"INFO: [{server_name}] uses untrusted package '{package}'. "
            f"Verify source at npmjs.com before relying on it."
        )

    # Check for @latest (auto-update risk)
    for arg in args:
        if "@latest" in arg:
            findings.append(
                f"INFO: [{server_name}] uses @latest tag — vulnerable to supply chain attacks. "
                f"Consider pinning to specific version."
            )
            break

    return findings


def check_tool_descriptions(server_name: str, tools: list[dict]) -> list[str]:
    """Scan tool descriptions for injection patterns."""
    findings = []
    for tool in tools:
        desc = tool.get("description", "") or ""
        name = tool.get("name", "unknown")
        for pattern, label in TOOL_POISON_PATTERNS:
            if pattern.search(desc):
                findings.append(
                    f"CRITICAL: [{server_name}:{name}] {label}. "
                    f"This tool description may be poisoned!"
                )
    return findings


def check_drift(config: dict, config_path: Path) -> list[str]:
    """Compare current config against pinned baseline."""
    findings = []
    if not BASELINE_PATH.exists():
        return findings

    try:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return findings

    baseline_hash = baseline.get("configs", {}).get(str(config_path), {}).get("hash")
    if not baseline_hash:
        return findings

    current_hash = compute_config_hash(config)
    if current_hash != baseline_hash:
        findings.append(
            f"WARN: Config {config_path.name} has changed since last pin "
            f"(was {baseline_hash}, now {current_hash}). "
            f"Run with --pin to update baseline after review."
        )

    return findings


def pin_baseline(configs: dict[str, dict]) -> None:
    """Save current config state as baseline for drift detection."""
    baseline = {"configs": {}}
    for path_str, config in configs.items():
        baseline["configs"][path_str] = {
            "hash": compute_config_hash(config),
            "servers": list(config.get("mcpServers", {}).keys()),
        }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Baseline pinned to {BASELINE_PATH}")


def run_snyk_scan(config_path: Path) -> list[str]:
    """Run snyk-agent-scan if SNYK_TOKEN is available."""
    if not os.environ.get("SNYK_TOKEN"):
        return ["INFO: SNYK_TOKEN not set — skipping snyk-agent-scan. "
                "Get token at https://app.snyk.io/account"]

    try:
        result = subprocess.run(
            ["snyk-agent-scan", "scan", str(config_path)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return [f"WARN: snyk-agent-scan found issues:\n{result.stdout[:500]}"]
        return [f"OK: snyk-agent-scan passed for {config_path.name}"]
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return [f"INFO: snyk-agent-scan not available: {e}"]


def audit_config(config_path: Path, full: bool = False) -> list[str]:
    """Run all checks on a single MCP config file."""
    config = load_config(config_path)
    if config is None:
        return []

    findings = []
    servers = config.get("mcpServers", {})

    print(f"\nScanning {config_path} ({len(servers)} servers)...")

    for name, server_config in servers.items():
        findings.extend(check_env_exposure(name, server_config))
        findings.extend(check_server_trust(name, server_config))

    findings.extend(check_drift(config, config_path))

    if full:
        findings.extend(run_snyk_scan(config_path))

    return findings


def main():
    args = sys.argv[1:]
    do_pin = "--pin" in args
    do_full = "--full" in args
    custom_config = None

    for i, arg in enumerate(args):
        if arg == "--config" and i + 1 < len(args):
            custom_config = Path(args[i + 1])

    # Determine configs to scan
    if custom_config:
        configs_to_scan = [custom_config]
    else:
        configs_to_scan = [p for p in DEFAULT_CONFIGS if p.exists()]

    if not configs_to_scan:
        print("No MCP config files found.")
        sys.exit(0)

    print("=" * 60)
    print("MCP Security Audit — AI Agent Traps Defense (Phase 4)")
    print("=" * 60)

    all_findings: list[str] = []
    loaded_configs: dict[str, dict] = {}

    for config_path in configs_to_scan:
        config = load_config(config_path)
        if config:
            loaded_configs[str(config_path)] = config
            findings = audit_config(config_path, full=do_full)
            all_findings.extend(findings)

    # Pin baseline if requested
    if do_pin:
        pin_baseline(loaded_configs)

    # Summary
    print("\n" + "=" * 60)
    criticals = [f for f in all_findings if f.startswith("CRITICAL")]
    warns = [f for f in all_findings if f.startswith("WARN")]
    infos = [f for f in all_findings if f.startswith("INFO")]

    if all_findings:
        for finding in all_findings:
            icon = "\U0001f6a8" if finding.startswith("CRITICAL") else "\u26a0\ufe0f" if finding.startswith("WARN") else "\u2139\ufe0f"
            print(f"  {icon} {finding}")

    print(f"\nTotal: {len(criticals)} critical, {len(warns)} warnings, {len(infos)} info")

    if criticals:
        sys.exit(2)
    elif warns:
        sys.exit(1)
    else:
        print("All clear.")
        sys.exit(0)


if __name__ == "__main__":
    main()

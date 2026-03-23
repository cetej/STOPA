---
name: security-review
  Use when reviewing code for security concerns, before deploying to production, or when the user
  asks about security posture. Trigger on 'security review', 'security audit', 'is this secure',
  'check for vulnerabilities', 'bezpečnostní review'.
  Do NOT use for general code review (/critic or /pr-review), for dependency updates (/dependency-audit),
  or for incident response (/incident-runbook).
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - TodoWrite
---

# /security-review — Trust Boundary Analysis

Perform a structured security review of the codebase or a specific feature. Focus on finding real vulnerabilities, not theoretical ones.

## Scope

Accept one of:
- **Full repo scan**: Review the entire project for security issues
- **Feature review**: Review a specific feature, PR, or set of files
- **Threat model**: Identify attack surfaces and trust boundaries

## Process

### Phase 1: Attack Surface Mapping

Identify trust boundaries — where untrusted data enters the system:

| Boundary | What to look for |
|----------|-----------------|
| **User input** | Forms, URL params, headers, file uploads, API request bodies |
| **External APIs** | Responses, webhooks, callbacks |
| **File system** | Config files, uploaded files, temp files |
| **Environment** | Env vars, CLI args, build-time configs |
| **Dependencies** | Third-party packages, CDN resources |
| **Inter-service** | Messages, shared state, database queries |

### Phase 2: Vulnerability Scan

Check each trust boundary against these categories:

#### A. Injection (OWASP A03)
- SQL injection: raw queries, string interpolation in SQL
- Command injection: shell exec with user input, unsanitized paths
- XSS: unescaped output in HTML/JS, innerHTML, dangerouslySetInnerHTML
- Template injection: user input in template strings
- Path traversal: `../` in file paths, unchecked symlinks

#### B. Authentication & Authorization (OWASP A01, A07)
- Broken auth: weak password requirements, missing rate limiting
- Missing authorization checks on endpoints
- IDOR: direct object references without ownership checks
- Session management: insecure cookies, missing CSRF tokens
- JWT issues: no expiry, weak signing, alg:none

#### C. Secrets & Data Exposure (OWASP A02)
- Hardcoded secrets, API keys, passwords in code
- Secrets in logs, error messages, or stack traces
- Sensitive data in URL params (logged by proxies/browsers)
- Missing encryption for sensitive data at rest or in transit
- `.env` files, credentials in git history

#### D. Configuration (OWASP A05)
- Debug mode in production
- Overly permissive CORS
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Default credentials or configs
- Exposed admin interfaces

#### E. Dependencies (OWASP A06)
- Known CVEs in dependencies (check lockfile versions)
- Unmaintained or abandoned packages
- Excessive permissions in dependency configs

### Phase 3: Risk Assessment

For each finding, classify:

| Severity | Impact | Exploitability | Example |
|----------|--------|----------------|---------|
| **Critical** | Data breach, RCE | Easy, no auth needed | SQL injection in login |
| **High** | Privilege escalation | Moderate effort | Missing auth on admin API |
| **Medium** | Data leak, DoS | Requires auth or specific conditions | Verbose error messages |
| **Low** | Information disclosure | Hard to exploit | Minor header missing |
| **Info** | Best practice | Not exploitable | Outdated but unaffected dep |

### Phase 4: Report

Output a structured report:

```markdown
## Security Review: [Scope]

Reviewed: [date]
Files scanned: [count]
Trust boundaries identified: [count]

### Summary
- Critical: N
- High: N
- Medium: N
- Low: N

### Findings

#### [CRITICAL] Finding title
- **File**: `path/to/file.py:42`
- **Category**: Injection / Auth / Secrets / Config / Deps
- **Description**: What's wrong and why it's dangerous
- **Proof**: Code snippet showing the vulnerability
- **Fix**: Specific remediation with code example
- **References**: CWE/OWASP ID if applicable

[Repeat for each finding, sorted by severity]

### Positive Observations
- [Things done well — reinforce good practices]

### Recommendations
1. [Priority action 1]
2. [Priority action 2]
```

## Rules

- **No false positives** — only report issues that are actually exploitable or clearly violate security best practices
- **Show proof** — include the specific code that's vulnerable, not just a category
- **Provide fixes** — every finding must include a concrete remediation
- **Context-aware** — a TODO app has different security needs than a banking API
- **No FUD** — be precise about impact, don't exaggerate risks

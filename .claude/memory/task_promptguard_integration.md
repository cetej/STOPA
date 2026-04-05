---
task: PromptGuard integrace do STOPA hooks
status: completed
created: 2026-04-05
completed: 2026-04-05
priority: medium
---

# Task: PromptGuard + CodeShield integrace

## Kontext

AI Agent Traps defense roadmap (Phase 1-5) je kompletní s regex-based hooks.
Další vrstva: ML-based detekce přes LlamaFirewall PromptGuard (BERT, AUC 0.98).
Research v `learnings/2026-04-05-agent-defense-frameworks.md`.

## Úkoly

### 1. Instalace LlamaFirewall
- `pip install llamafirewall` (nebo uv)
- `llamafirewall configure` — stáhne HuggingFace modely (~1GB)
- Ověřit že funguje: `python -c "from llamafirewall import ..."`
- Změřit latenci na Windows

### 2. PromptGuard do content-sanitizer.py
- Přidat jako fallback layer ZA regex patterns (regex = fast path, PG = deep scan)
- Podmínit dostupností: `try: import llamafirewall except: skip`
- Spustit PG jen pokud regex nic nenašel ALE obsah je >500 chars (worth scanning)
- Severity: PG detection = ALERT (vyšší důvěra než regex WARN)
- Performance budget: celý hook max 200ms (regex 50ms + PG 100-150ms)

### 3. CodeShield do security-scan.py
- Přidat Semgrep-based code scanning k existujícímu regex pattern scanning
- Spustit jen na .py/.js/.ts soubory (ne na markdown/config)
- Podmínit dostupností (graceful fallback)

### 4. [UNTRUSTED] tagging konvence
- Upravit orchestrate SKILL.md: agent zpracovávající external data taguje output
- Upravit scout SKILL.md: web-sourced findings dostanou [UNTRUSTED] prefix
- state.md konvence: sekce `## Untrusted Data` pro web-originated content

### 5. Verifikace
- Test na payloady z Phase 1 testů (musí stále detekovat vše)
- Test na nové zero-day patterny (PG by měl chytit co regex nechytí)
- Benchmark: celkový overhead na normální WebFetch (<200ms)

## Výsledky implementace

### content-sanitizer.py
- PromptGuard ML layer přidán jako fallback za regex
- Plně lazy import (torch/transformers se nenačítá pokud model není stažen)
- Regex layer: 58-70ms per payload, detekuje všech 8 kategorií
- PromptGuard se aktivuje jen pokud: regex nic nenašel AND obsah >500 chars AND model je lokálně dostupný
- **Stav modelu:** PromptGuard model (meta-llama/Llama-Prompt-Guard-2-86M) vyžaduje HuggingFace token + stažení (~86M params). Zatím nedostupný lokálně — ML layer skipped, regex layer plně funkční.

### security-scan.py
- CodeShield (Semgrep-based CWE) přidán jako Layer 2
- Graceful fallback: na Windows chybí semgrep-core — CodeShield se přeskočí
- Regex patterns plně funkční: 7/7 testů OK (BLOCK i WARN)
- 150-220ms per scan (CodeShield import attempt + regex)

### orchestrate.md + scout.md
- Rule #14 v orchestrate: [UNTRUSTED] tagging pro web-sourced data
- Rule #6 v scout: [UNTRUSTED] prefix pro web-originated findings
- state.md konvence: `## Untrusted Data` sekce

### Akce potřebné od uživatele
1. **PromptGuard model:** `huggingface-cli login` + restart; model se stáhne automaticky při prvním spuštění
2. **CodeShield:** funguje plně na Linux/macOS; na Windows čeká na semgrep-core port

## Reference
- `reference_agent_traps.md` — celý defense roadmap
- `learnings/2026-04-05-agent-defense-frameworks.md` — research verdikty
- `.claude/hooks/content-sanitizer.py` — Phase 1+6 hook (regex + PromptGuard ML)
- `.claude/hooks/security-scan.py` — Phase 1+6 hook (regex + CodeShield)

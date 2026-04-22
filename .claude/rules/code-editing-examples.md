# Code Editing Examples

Konkrétní před/po ilustrace k abstraktním pravidlům v [`behavioral-genome.md § Code Editing Discipline`](behavioral-genome.md).

Load on-demand (ne every-session) — konzultovat před non-trivial editací, po `/critic` FAIL na orthogonal damage, nebo když user request je ambiguous.

Zdroj principů: Karpathy X post 2015883857489522876 (2026-01-26). Inspirace formátu: [forrestchang/andrej-karpathy-skills EXAMPLES.md](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/EXAMPLES.md) (75k★). Empirická evidence pro example-driven compliance: [arXiv:2311.04235](https://arxiv.org/abs/2311.04235) (Can LLMs Follow Simple Rules?).

---

## Rule 1: Match existing style

> Match existing style, even if you'd do it differently. Consistency > personal preference.

**Kontext:** Uživatel žádá o přidání funkce do existujícího Python hooku.

### ❌ Špatně
```python
# existující hook: .format() všude, bez type hints, camelCase
def processRecord(rec):
    return "Record {}: {}".format(rec["id"], rec["data"])

# agent přidá:
def validate_record(rec: dict) -> bool:
    return f"Valid: {rec['id']}"  # f-string, snake_case, type hints — 3× style drift
```

**Problémy:**
- Smíšené string formátování fragmentuje codebase
- `snake_case` v `camelCase` souboru = konzistence rozbitá
- Type hints retrofitnuté na jednu funkci ≠ konvence

### ✅ Správně
```python
def validateRecord(rec):
    return "Valid: {}".format(rec["id"])
```

**Verify:** `rg "\.format\(|f\"" <file>` — mělo by ukázat konzistentní použití jednoho stylu.

---

## Rule 2: Mention dead code, don't delete it

> Unrelated dead code: MENTION it, don't delete it. Only remove orphans YOUR change created.

**Kontext:** Uživatel žádá refactor `parse_url()` v scout hooku. Agent si všimne `old_legacy_parser()`, která nemá volače.

### ❌ Špatně
```diff
-def old_legacy_parser(s):
-    # vypadá jako dead code — mažu
-    return s.split("/")
-
 def parse_url(s):
     return urlparse(s).path
```

**Problémy:**
- Smazání nesouvisející funkce = orthogonal damage
- "Vypadá jako dead code" je assumption — mohla být volána dynamicky (`getattr`), testovacími fixturami, nebo vystavena jako public API
- User přišel pro `parse_url` fix → diff obsahuje nepozvanou deleci

### ✅ Správně
```diff
 def parse_url(s):
     return urlparse(s).path
```

Zpráva agenta uživateli:
> Opraveno. **Pozn.:** V souboru je `old_legacy_parser()` bez callerů (`rg 'old_legacy_parser' → 1 match`). Nechávám beze změny. Je-li skutečně dead, smaž v samostatné PR.

**Verify:** `git diff` — změna se týká POUZE `parse_url`. Dead code zmíněn v response, ne v diffu.

**Výjimka:** Pokud TVOJE změna udělala import/variable/helper nepoužívanou (orphan caused by your edit) → smaž ji. Jen pre-existing dead code zůstává.

---

## Rule 3: Don't "improve" adjacent code

> Don't "improve" adjacent code, comments, or formatting that weren't part of the task. Every changed line should trace directly to the user's request.

**Kontext:** Uživatel: "oprav bug v `validate_email()`, padá na prázdném stringu"

### ❌ Špatně (diff 15 řádků, z toho 2 tasked)
```diff
-def validate_email(email):
-    # Validates email
+def validate_email(email: str) -> bool:
+    """Validate email format.
+
+    Args:
+        email: Email string to validate
+    Returns:
+        True if valid, False otherwise
+    """
+    if not email:
+        return False
     if "@" not in email:
         return False
+    if len(email.split("@")[0]) < 3:  # ← nevyžádaná business rule
+        return False
     return True
```

**Problémy:**
- User žádal empty-string fix (2 řádky). Agent přidal: type hints, docstring, novou business rule (username length ≥ 3).
- Tři nepozvané změny = tři šance na bug nebo konflikt s callery, kteří posílají username < 3 znaky
- "len < 3" nejde vystopovat na user request → scope creep

### ✅ Správně (diff 2 řádky)
```diff
 def validate_email(email):
     # Validates email
+    if not email:
+        return False
     if "@" not in email:
         return False
     return True
```

**Verify:** Každý `+` řádek odpovídá na user request. Pokud řádek nelze zdůvodnit větou "protože user řekl X" → odstraň ho před commitem.

---

## Rule 4: Surface ambiguity, don't pick silently

> When ambiguity exists about user intent: surface the interpretations instead of picking silently.

**Kontext:** Uživatel: "zrychli hledání v radar.md"

### ❌ Špatně
Agent interně rozhodne a rovnou implementuje:

```python
# agent implementuje BM25 index pro radar.md
def search_radar(query):
    return bm25_index.query(query)
```

**Problémy:**
- "Zrychli" má ≥3 validní interpretace:
  1. **Latency** — rychlejší jednotlivý dotaz
  2. **Throughput** — paralelní batch queries
  3. **UX responsiveness** — typeahead, streaming
- Agent vybral BM25 (řeší #1), user možná chtěl keyword filter UI (#3)
- Wrong assumption = wasted implementation + nesprávné řešení

### ✅ Správně
Před implementací:

> Než začnu — "zrychli" můžu číst třemi způsoby:
> 1. **Latency per query** — přidat BM25 index (overhead pro malé repo)
> 2. **Throughput** — paralelizovat batch grep
> 3. **UX responsiveness** — typeahead filter, streaming výsledky
>
> Kterou řešíš? Při 76 tools v radar.md je grep dnes ~10ms — možná žádnou a problém je jinde.

**Verify:** Pokud reasonable čtenáři interpretují úkol ≥2 způsoby → surface options jednou. Pokud je interpretace jednoznačná → proceed.

**Výjimka z Autonomy tension:** Technical execution ambiguity (který konkrétní API endpoint, jaký import path) → rozhodni autonomně. Intent ambiguity (co user vlastně chce) → zeptat se jednou.

---

## Rule 5: Imperative → verifiable goal

> For non-trivial tasks: transform imperative → verifiable goals.

**Kontext:** Uživatel: "přidej validaci vstupu do `capture_source.py`"

### ❌ Špatně (unverifiable)
```python
def capture(url):
    if not url:
        raise ValueError("Invalid URL")
    # ... rest unchanged
```

Report agenta: "Validace přidána."

**Problémy:**
- Která vstupní data jsou blokovaná? `""`, `None`, `"not-a-url"`, `"javascript:..."`? Nejasné.
- Žádný test = žádný důkaz "validace funguje"
- Další session nemá způsob ověřit regresi

### ✅ Správně (test-first, verifiable)
```python
# tests/test_capture.py — napsáno PŘED implementací
def test_capture_rejects_empty():
    with pytest.raises(ValueError):
        capture("")

def test_capture_rejects_non_http():
    with pytest.raises(ValueError):
        capture("javascript:alert(1)")

def test_capture_rejects_none():
    with pytest.raises(ValueError):
        capture(None)

# capture_source.py — implementace dokud testy neprojdou
def capture(url):
    if not url or not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL: {url!r}")
    # ...
```

Report agenta:
> Přidány 3 testy (empty, non-http, None). `pytest tests/test_capture.py -v` → 3 passed.

**Verify:**
- Existuje test failující BEZ změny kódu?
- Existuje test passující SE změnou kódu?
- Regrese je měřitelná přes re-run?

---

## Použití v praxi

| Kdy konzultovat | Která rule |
|---|---|
| Před editací existujícího Python souboru | Rule 1 (style), Rule 3 (scope) |
| Refactor s diff > 5 řádků nad úkol | Rule 3 (trace každý řádek na request) |
| User request obsahuje "fix/zlepši/zrychli" | Rule 4 (surface interpretations) |
| Task má "add/přidej" nebo je non-trivial | Rule 5 (test-first) |
| Vidíš něco co "vypadá nepoužívané" | Rule 2 (mention, don't delete) |

## Anti-Rationalization

| Rationalization | Proč špatně | Co udělat |
|---|---|---|
| "Příklad je Python, já edituju YAML/MD — neaplikuje se" | Principy jsou language-agnostic. Rule 2 platí i pro YAML klíče, Rule 3 pro markdown sekce. | Extrahuj princip, ne shape. Example = teaching tool, ne literal template. |
| "Quick fix, ptát se na ambiguitu = friction" | Rule 4 má výjimku pro technical execution. Jednoznačná mechanical oprava → proceed bez ptaní. | Aplikuj Rule 4 jen pro intent ambiguity, ne pro jasné micro-fixy. |
| "Našel jsem dead code, můžu smazat — je evidentně nepoužívaný" | "Evidentně" je assumption. Dynamic call (`getattr`), test fixtures, public API re-export. | Rule 2: zmínit v response, nechat v diffu. Samostatná PR. |
| "Přidávám type hints / docstring protože je to best practice" | Best practice ≠ user request. Rule 3: každá `+` řádka trace na request. | Pokud user nežádal, nech beze změny. Pokud konzistence projektu = chybí, flagni to v response. |

## References

- Source pravidel: [`behavioral-genome.md § Code Editing Discipline`](behavioral-genome.md) (řádek 82)
- Tension s Autonomy: viz `behavioral-genome.md § Autonomy` — Rule 4 je výjimka z "neptej se krok po kroku"
- Empirie: [arXiv:2311.04235](https://arxiv.org/abs/2311.04235) Can LLMs Follow Simple Rules? — pure abstraction underperforms; concrete examples + abstract rules outperform either alone
- Inspirace: [forrestchang/andrej-karpathy-skills EXAMPLES.md](https://github.com/forrestchang/andrej-karpathy-skills) (75k★, 2026-04)

# Testovací zadání pro cílové projekty

Cíl: Ověřit STOPA orchestraci v1.7.0 na reálných úkolech.
Testované features: two-stage review, agent status codes, anti-rationalization tables, 3-fix escalation, wave execution.

---

## 1. ADOBE-AUTOMAT — Layout Generator Refactor

### Kontext
Layout Generator prošel 11 sessions rychlého vývoje (multi-article, Illustrator integration, map detection, AI template export). Kód roste rychle, pravděpodobně má technický dluh.

### Zadání

```
/orchestrate

Proveď quality audit Layout Generatoru v ADOBE-AUTOMAT:

1. Scout: Zmapuj všechny soubory Layout Generatoru (backend + frontend).
   Identifikuj duplicitní kód, nekonzistentní error handling, TODO/FIXME komentáře.

2. Refactor: Extrahuj společnou logiku do shared utilit tam, kde se
   stejný pattern opakuje 3+×. Zachovej zpětnou kompatibilitu.

3. Critic (two-stage):
   - --spec: Ověř že IDML pravidla z CLAUDE.md jsou dodržena
     (nikdy ElementTree.write(), forward slashes, \r pro Illustrator)
   - --quality: Zkontroluj error handling, encoding, type hints

4. Verify: Spusť Layout Generator na testovacím článku, ověř IDML výstup.

Tier: standard (2-4 agenti)
```

### Co testuje
| v1.7.0 Feature | Jak se projeví |
|-----------------|----------------|
| Two-stage review | critic --spec (IDML pravidla) + --quality (kód) |
| Agent status codes | DONE_WITH_CONCERNS pokud refactor najde ale neopraví architektonický problém |
| Anti-rationalization | Critic nesmí přehlédnout porušení IDML pravidel jen proto, že "kód funguje" |
| 3-fix escalation | Pokud IDML fix selže 3×, eskalace místo loop |
| Wave execution | Scout (wave 1) → Refactor (wave 2) → Critic+Verify (wave 3) |

---

## 2. NG-ROBOT — Photo Caption Bug Fix + Pipeline Hardening

### Kontext
NG-ROBOT má 5 aktivních bugů z MEMORY.md (2026-03-14):
1. Photo caption scrambling v Phase 7 (root cause identified: photo_offset logic)
2. Irrelevant term/fact/context checks (phases 3-5)
3. CMS Aqua infographics testing
4. CMS Aqua inline images testing
5. Inbox workflow D&D testing

### Zadání

```
/orchestrate

Oprav photo caption scrambling v NG-ROBOT Phase 7 a zpevni pipeline:

1. Scout: Zmapuj Phase 7 procesor — najdi photo_offset logiku,
   caption mapping flow, a captions.json handling.
   Formuluj assumptions (--assumptions flag).

2. Fix: Oprav photo_offset bug. Zajisti že caption mapping používá
   captions.json klíče (filename-based), ne indexy.
   IDML/HTML výstup musí mít správné popisky u správných fotek.

3. Harden: Přidej validační krok na konec Phase 7 — zkontroluj že
   každá fotka má caption a žádný caption není orphaned.

4. Critic (two-stage):
   - --spec: Ověř PHASES dict konzistenci napříč 3 soubory
     (ngrobot.py, auto_agent.py, document_processor.py)
   - --quality: Encoding (UTF-8), Windows cesty (pathlib), error handling

5. Verify: Spusť Phase 7 na stuck článku (romeo-...frog),
   ověř že captions sedí na správných fotkách.

Tier: standard (3-4 agenti)
```

### Co testuje
| v1.7.0 Feature | Jak se projeví |
|-----------------|----------------|
| Two-stage review | critic --spec (PHASES sync) + --quality (encoding, paths) |
| Agent status codes | NEEDS_CONTEXT pokud photo_offset root cause není jasný ze scoutu |
| Anti-rationalization | Verify musí prokázat L4 (Flows) — reálná data, ne jen "kód vypadá OK" |
| Deviation rules | Fix agent může opravit bug inline (max 3 pokusy), ale nesmí měnit Phase 7 architekturu |
| Goal-backward verification | L1 fix exists → L2 not stub → L3 wired into pipeline → L4 romeo-frog article passes |

---

## 3. Jak spustit

### Prerekvizity
1. STOPA plugin v1.7.0 musí být aktivní v cílovém projektu (settings.json marketplace)
2. Ověř: `claude --print-plugins` by měl ukázat stopa-orchestration

### Spuštění
```bash
# ADOBE-AUTOMAT
cd C:\Users\stock\Documents\000_NGM\ADOBE-AUTOMAT
# Vlož zadání z bodu 1 výše

# NG-ROBOT
cd C:\Users\stock\Documents\000_NGM\NG-ROBOT
# Vlož zadání z bodu 2 výše
```

### Na co se zaměřit při testování
- [ ] Orchestrátor správně přiřadí tier (standard)
- [ ] Wave execution — paralelní kde možné, sekvenční kde závislost
- [ ] Two-stage critic se spustí jako 2 separate review passes
- [ ] Agent status codes v subtask výstupech (DONE/DONE_WITH_CONCERNS/BLOCKED)
- [ ] Anti-rationalization tables — critic neignoruje known issues
- [ ] 3-fix escalation — pokud fix selže, zastaví se po 3 pokusech
- [ ] Budget tracking — nepřekročí standard tier limit
- [ ] Checkpoint — auto-checkpoint při >70% subtasků hotových

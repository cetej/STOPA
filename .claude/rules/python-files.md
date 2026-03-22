---
globs: "**/*.py"
---

# Python pravidla

- Encoding: UTF-8 všude, `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` pro CLI výstup
- Cesty: `pathlib.Path()`, nikdy hardcoded backslashe
- Type hints: pro public API funkce (parametry + return type)
- Importy: stdlib → third-party → local, oddělené prázdným řádkem
- Windows: retry logika pro file locking (antivirus), `errors='replace'` pro I/O
- Žádné `print()` pro debugging v produkčním kódu — použij `logging`

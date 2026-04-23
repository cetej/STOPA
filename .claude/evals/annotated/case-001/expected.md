# Expected Behavior

Human annotation: **BAD**.

Note: Agent spustil pytest bez předchozí kontroly test setup — test selhal kvůli chybějícímu fixture. Měl nejprve přečíst conftest.py nebo použít --collect-only.

Expected corrected behavior: Před spuštěním pytest na neznámém projektu:
1. Read `conftest.py` nebo `pyproject.toml` pro znalost fixtures a test config
2. Spustit `pytest --collect-only` pro ověření že testy jsou discoverable bez runtime errorů
3. Teprve poté spustit plný `pytest tests/`

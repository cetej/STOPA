# Incident Runbook — Known Patterns

Add a line each time a new failure pattern is resolved. Format: symptom → cause → fix.

## Server & Ports

- **Port 8000 occupied** → stale Python process → `taskkill //F //IM python.exe` then restart
- **Port 8501 occupied** → stale Streamlit → same fix, or `netstat -ano | findstr :8501` to find PID
- **Address already in use (Linux)** → `lsof -i :PORT` then `kill -9 PID`
- **CORS errors in browser** → FastAPI missing CORS middleware or wrong origin in allow_origins

## Python & Dependencies

- **ModuleNotFoundError** → wrong venv active, or dependency not installed → `pip install -e .` or check venv path
- **UnicodeDecodeError on Windows** → missing `encoding='utf-8'` in open() or missing `sys.stdout.reconfigure(encoding='utf-8')`
- **ImportError: cannot import name X** → circular import or renamed module → check import chain
- **CUDA out of memory** → model too large for GPU → use CPU fallback or smaller batch size

## Git

- **Merge conflict** → read both versions, choose correct one, don't blindly accept either side
- **Detached HEAD** → `git checkout main` or `git checkout -b branch-name` to save work
- **Push rejected (non-fast-forward)** → `git pull --rebase` then push again. NEVER force-push without user approval

## Data & ML

- **NaN/inf in calculations** → add `np.isfinite()` guard before using values
- **HDBSCAN 95% noise** → input dimensions too high → apply UMAP reduction first (256d→15d works)
- **TF-IDF nonsense labels** → corpus too small or stopwords incomplete → consider LLM-based labeling
- **Arctic Shift API timeout** → API may be down → check status, retry with exponential backoff
- **Parquet read error** → file corrupted or incompatible version → try `pd.read_parquet(path, engine='pyarrow')`

## Windows Specific

- **File locked by antivirus** → retry after 1-2 seconds, or exclude directory in Windows Security
- **Path too long** → use `\\?\` prefix or shorten path. Enable long paths in registry
- **Permission denied on .git** → close IDE/editor that locks files, then retry
- **taskkill not found** → use `//F //IM` with double slashes in Git Bash (not single slash)

## Claude Code / Orchestration

- **Skill not triggering** → check description field for trigger keywords. Description is routing signal, not summary
- **Agent loop (same agent 3×)** → circuit breaker should fire. If not, check orchestrate skill logic
- **Memory file > 500 lines** → archive old entries to *-archive.md
- **Checkpoint stale** → always check date in checkpoint. If > 2 sessions old, re-scout instead of trusting it

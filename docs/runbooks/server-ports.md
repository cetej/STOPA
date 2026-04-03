---
category: server-ports
severity: medium
last_updated: 2026-04-03
---

# Server & Ports — Runbook

## Port 8000 occupied

**Symptom:** Server fails to start, "address already in use" on port 8000
**Cause:** Stale Python process from previous session
**Fix:**
1. `taskkill //F //IM python.exe` (Git Bash) or `taskkill /F /IM python.exe` (cmd)
2. Restart server

**Prevention:** Always stop server before closing terminal

---

## Port 8501 occupied (Streamlit)

**Symptom:** Streamlit won't start, port 8501 in use
**Cause:** Stale Streamlit process
**Fix:**
1. `netstat -ano | findstr :8501` to find PID
2. `taskkill //F //PID <pid>`
3. Restart Streamlit

**Prevention:** Use Ctrl+C to stop Streamlit cleanly

---

## Address already in use (Linux)

**Symptom:** Server start fails on Linux with EADDRINUSE
**Cause:** Previous process still bound to port
**Fix:**
1. `lsof -i :PORT` to find process
2. `kill -9 PID`

---

## CORS errors in browser

**Symptom:** Browser console shows CORS policy errors
**Cause:** FastAPI missing CORS middleware or wrong origin in allow_origins
**Fix:**
1. Add `CORSMiddleware` to FastAPI app
2. Set `allow_origins=["*"]` for dev or specific origins for prod

**Prevention:** Include CORS middleware in project template from start

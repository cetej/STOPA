---
category: windows
severity: medium
last_updated: 2026-04-03
---

# Windows Specific — Runbook

## File locked by antivirus

**Symptom:** `PermissionError` or `WinError 32` when writing/deleting files
**Cause:** Windows Defender or other AV scanning the file
**Fix:**
1. Retry after 1-2 seconds (usually enough for scan to complete)
2. Or exclude project directory in Windows Security settings

**Prevention:** Add dev directories to AV exclusions

---

## Path too long

**Symptom:** `FileNotFoundError` or `WinError 206` on deep paths
**Cause:** Windows MAX_PATH (260 chars) exceeded
**Fix:**
1. Use `\\?\` prefix for long paths
2. Enable long paths in registry: `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1`
3. Shorten directory structure

---

## Permission denied on .git

**Symptom:** `error: unable to unlink` or permission denied on .git files
**Cause:** IDE or editor holding file locks
**Fix:**
1. Close VS Code / other editors that may lock .git files
2. Retry git operation

---

## taskkill not found in Git Bash

**Symptom:** `taskkill: command not found` in Git Bash
**Cause:** Git Bash needs double slashes for Windows flags
**Fix:**
1. Use `taskkill //F //IM process.exe` (double slashes in Git Bash)
2. Or use cmd/PowerShell where single slashes work

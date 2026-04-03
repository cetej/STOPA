---
category: data-ml
severity: medium
last_updated: 2026-04-03
---

# Data & ML — Runbook

## NaN/inf in calculations

**Symptom:** Unexpected NaN or inf values in output
**Cause:** Division by zero, log of negative, or propagated NaN
**Fix:**
1. Add `np.isfinite()` guard before using values
2. Trace back to find source of invalid input

---

## HDBSCAN 95% noise

**Symptom:** HDBSCAN assigns almost all points to noise (-1)
**Cause:** Input dimensions too high for density-based clustering
**Fix:**
1. Apply UMAP dimensionality reduction first (256d -> 15d works well)
2. Tune `min_cluster_size` parameter

---

## TF-IDF nonsense labels

**Symptom:** Cluster labels from TF-IDF are meaningless or too generic
**Cause:** Corpus too small or stopwords list incomplete
**Fix:**
1. Expand stopwords list for the language
2. Consider LLM-based labeling instead of TF-IDF for small corpora

---

## Arctic Shift API timeout

**Symptom:** Requests to Arctic Shift API time out or return 5xx
**Cause:** API may be down or overloaded
**Fix:**
1. Check API status
2. Retry with exponential backoff
3. Cache successful responses locally

---

## Parquet read error

**Symptom:** `ArrowInvalid` or similar error reading .parquet files
**Cause:** Corrupted file or incompatible Parquet version
**Fix:**
1. Try explicit engine: `pd.read_parquet(path, engine='pyarrow')`
2. If still fails, file may be corrupted — check backup or re-download

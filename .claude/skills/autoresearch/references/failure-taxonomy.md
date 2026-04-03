# Failure Taxonomy

Classify every crash/error into a category. This enables smarter recovery decisions.

| Category | Pattern | Recovery | Repairable? |
|----------|---------|----------|-------------|
| **DEPENDENCY** | ImportError, ModuleNotFoundError | `pip install` missing package, retry | Yes (1 attempt) |
| **RESOURCE** | OOM, CUDA out of memory, disk full | Reduce batch size / data size, retry | Yes (1 attempt) |
| **TIMEOUT** | Eval exceeds 5x baseline time | Kill, reduce scope, retry | Yes (1 attempt) |
| **DATA** | FileNotFoundError, empty dataset, corrupt input | Check paths, verify data exists | Yes (if path issue) |
| **DIVERGENCE** | NaN, Inf, metric outside expected range | Revert, flag for manual review | No — revert only |
| **SYNTAX** | SyntaxError, IndentationError | Fix and retry | Yes (1 attempt) |
| **LOGIC** | Assertion failed, wrong output shape | Revert, log as "approach incompatible" | No — revert only |
| **EVAL_BROKEN** | Eval script itself errors | STOP — ground truth corrupted | No — STOP |
| **ENVIRONMENT** | Permission denied, port in use, antivirus lock | Retry with delay | Yes (2 attempts) |
| **UNKNOWN** | Unclassified error | Revert, log full stderr | No — revert only |

**Repairability rule:** If the same failure category occurs 3+ times across the run, mark it as **non-repairable** for remaining iterations. Don't waste budget retrying a systemic issue.

**Auto-classification:** Parse stderr/stdout against category patterns. Log category in TSV `notes` column.

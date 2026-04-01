#!/usr/bin/env python3
"""Atomic file write utility for STOPA memory files.

Prevents corruption from crashes mid-write by writing to a .tmp file
first, then using os.replace() which is atomic on same-filesystem
operations (both POSIX and Windows NTFS).

Usage from hooks:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from atomic_utils import atomic_write

    atomic_write(Path(".claude/memory/learnings/my-learning.md"), content)
"""
import os
import time
from pathlib import Path


def atomic_write(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write content atomically: write to .tmp then os.replace() to target.

    Args:
        path: Target file path (will be created or overwritten)
        content: Text content to write
        encoding: File encoding (default UTF-8)

    Raises:
        OSError: If write or replace fails after retry
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")

    try:
        tmp.write_text(content, encoding=encoding, errors="replace")
        # os.replace() is atomic on same filesystem — works on Windows NTFS
        os.replace(tmp, path)
    except PermissionError:
        # Windows antivirus may lock the .tmp file briefly — retry once
        time.sleep(0.1)
        try:
            os.replace(tmp, path)
        except Exception:
            # Clean up tmp if replace still fails
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
            raise
    except Exception:
        # Clean up tmp on any failure
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
        raise


def atomic_append(path: Path, line: str, encoding: str = "utf-8") -> None:
    """Append a line to a file. Append mode is inherently safe (no temp needed).

    This is a convenience wrapper — append mode writes are already atomic
    at the OS level for reasonable line sizes. Provided for API consistency.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding=encoding, errors="replace") as f:
        f.write(line)

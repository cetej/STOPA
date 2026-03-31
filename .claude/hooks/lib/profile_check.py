"""Shared profile gate for STOPA hooks (Python version).

Usage:
    from lib.profile_check import require_profile
    require_profile("standard")  # exits if current profile < standard
"""
import os
import sys

LEVELS = {"minimal": 1, "standard": 2, "strict": 3}

def require_profile(min_profile: str) -> None:
    """Exit silently if current profile is below required level."""
    current = os.environ.get("STOPA_HOOK_PROFILE", "standard")
    if LEVELS.get(current, 2) < LEVELS.get(min_profile, 2):
        sys.exit(0)

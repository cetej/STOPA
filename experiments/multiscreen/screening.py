"""Backward-compatible shim — re-exports all classes from submodules.

Original monolithic file refactored into package (core, tile, attention, retrieval, mipe, lm).
This file preserves `from screening import MultiScreenLM` for benchmark.py compatibility.
"""

# Re-export everything from submodules
from .core import TanhNorm, ScreeningUnit
from .tile import GatedScreeningTile, MultiScreenLayer
from .attention import ScreeningAttention
from .retrieval import RetrievalScreener
from .mipe import MiPE
from .lm import MultiScreenLM, TransformerLM, StandardAttention, TransformerBlock

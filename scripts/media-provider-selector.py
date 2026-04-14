#!/usr/bin/env python3
"""
Media Provider Selector — 7-dimension scored selection for media AI providers.

Replaces hardcoded provider selection in /klip and /nano skills with a scored,
auditable decision process. Inspired by OpenMontage lib/scoring.py.

Usage:
    python scripts/media-provider-selector.py --capability video --task "cinematic trailer, nature"
    python scripts/media-provider-selector.py --capability image --task "editorial photo, wildlife"
    python scripts/media-provider-selector.py --capability tts --task "czech narration, male voice"
    python scripts/media-provider-selector.py --list

Outputs JSON with ranked providers and decision rationale.
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ── Dimension weights (sum = 1.0) ──────────────────────────────────────────────

WEIGHTS = {
    "task_fit": 0.30,
    "output_quality": 0.20,
    "control": 0.15,
    "reliability": 0.15,
    "cost_efficiency": 0.10,
    "latency": 0.05,
    "continuity": 0.05,
}


# ── Synonym clusters for task_fit matching ──────────────────────────────────────

SYNONYM_CLUSTERS = [
    {"cinematic", "film", "movie", "trailer", "dramatic", "epic", "filmový", "poutáka"},
    {"explainer", "educational", "tutorial", "teaching", "výukový", "vysvětlující"},
    {"nature", "wildlife", "animal", "příroda", "zvíře", "fauna"},
    {"product", "commercial", "ad", "reklama", "produkt", "marketing"},
    {"anime", "cartoon", "animated", "animovaný", "ghibli", "pixar"},
    {"portrait", "face", "person", "člověk", "obličej", "portrét"},
    {"abstract", "artistic", "creative", "umělecký", "abstraktní"},
    {"documentary", "reportáž", "dokument", "archival"},
    {"macro", "close-up", "detail", "micro"},
    {"landscape", "scenery", "krajina", "panorama", "vista"},
]


def _expand_synonyms(task: str) -> set[str]:
    """Expand task description with synonym cluster members."""
    words = set(task.lower().split())
    expanded = set(words)
    for cluster in SYNONYM_CLUSTERS:
        if words & cluster:  # any overlap
            expanded |= cluster
    return expanded


# ── Provider Registry ───────────────────────────────────────────────────────────

@dataclass
class ProviderCapability:
    """What a provider can do."""
    name: str
    capability: str  # video | image | tts | music
    endpoint: str
    env_key: str     # Required env var
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    cost_per_unit: float = 0.0  # $/second for video, $/image for image
    avg_latency_s: float = 30.0
    reliability: float = 0.9  # 0-1 historical success rate
    control_features: list[str] = field(default_factory=list)
    quality_tier: str = "standard"  # standard | premium | experimental


# Video providers
VIDEO_PROVIDERS = [
    ProviderCapability(
        name="Kling 3.0 Pro",
        capability="video",
        endpoint="fal-ai/kling-video/v3/pro",
        env_key="FAL_KEY",
        strengths=["cinematic", "nature", "wildlife", "documentary", "face", "portrait", "consistent"],
        weaknesses=["abstract", "anime"],
        cost_per_unit=0.112,  # $/second
        avg_latency_s=90,
        reliability=0.92,
        control_features=["image-to-video", "text-to-video", "duration-control", "aspect-ratio"],
        quality_tier="premium",
    ),
    ProviderCapability(
        name="Kling 3.0 Standard",
        capability="video",
        endpoint="fal-ai/kling-video/v3/standard",
        env_key="FAL_KEY",
        strengths=["cinematic", "nature", "wildlife", "fast"],
        weaknesses=["abstract", "fine-detail"],
        cost_per_unit=0.084,
        avg_latency_s=60,
        reliability=0.90,
        control_features=["image-to-video", "text-to-video", "duration-control", "aspect-ratio"],
        quality_tier="standard",
    ),
    ProviderCapability(
        name="Seedance 2.0",
        capability="video",
        endpoint="bytedance/seedance-2.0/image-to-video",
        env_key="FAL_KEY",
        strengths=["motion-quality", "cinematic", "smooth", "natural-movement"],
        weaknesses=["text-to-video", "abstract"],
        cost_per_unit=0.08,
        avg_latency_s=120,
        reliability=0.88,
        control_features=["image-to-video", "aspect-ratio"],
        quality_tier="premium",
    ),
    ProviderCapability(
        name="Veo 2",
        capability="video",
        endpoint="fal-ai/veo2/image-to-video",
        env_key="FAL_KEY",
        strengths=["cinematic", "long-form", "film", "nature", "dramatic"],
        weaknesses=["text-to-video", "fast-motion"],
        cost_per_unit=0.15,
        avg_latency_s=150,
        reliability=0.85,
        control_features=["image-to-video"],
        quality_tier="premium",
    ),
]

# Image providers
IMAGE_PROVIDERS = [
    ProviderCapability(
        name="Nano Banana Pro",
        capability="image",
        endpoint="fal-ai/nano-banana-pro",
        env_key="FAL_KEY",
        strengths=["reasoning-guided", "complex-scenes", "editorial", "national-geographic", "wildlife"],
        weaknesses=["speed", "simple-icons"],
        cost_per_unit=0.02,
        avg_latency_s=15,
        reliability=0.93,
        control_features=["aspect-ratio", "resolution", "style-control"],
        quality_tier="premium",
    ),
    ProviderCapability(
        name="Nano Banana 2",
        capability="image",
        endpoint="fal-ai/nano-banana-2",
        env_key="FAL_KEY",
        strengths=["speed", "general", "versatile"],
        weaknesses=["complex-composition", "fine-detail"],
        cost_per_unit=0.01,
        avg_latency_s=8,
        reliability=0.95,
        control_features=["aspect-ratio", "resolution"],
        quality_tier="standard",
    ),
    ProviderCapability(
        name="FLUX",
        capability="image",
        endpoint="fal-ai/flux-pro/v1.1-ultra",
        env_key="FAL_KEY",
        strengths=["photorealistic", "portrait", "face", "consistent", "high-detail"],
        weaknesses=["artistic", "abstract"],
        cost_per_unit=0.04,
        avg_latency_s=20,
        reliability=0.91,
        control_features=["aspect-ratio", "seed", "guidance-scale"],
        quality_tier="premium",
    ),
    ProviderCapability(
        name="gpt-image-1",
        capability="image",
        endpoint="openai/gpt-image-1",
        env_key="OPENAI_API_KEY",
        strengths=["text-rendering", "infographic", "diagram", "product", "editorial"],
        weaknesses=["photorealistic-nature", "wildlife"],
        cost_per_unit=0.04,
        avg_latency_s=12,
        reliability=0.94,
        control_features=["aspect-ratio", "quality"],
        quality_tier="premium",
    ),
]

# TTS providers
TTS_PROVIDERS = [
    ProviderCapability(
        name="Edge TTS",
        capability="tts",
        endpoint="edge-tts",
        env_key="",  # No key needed
        strengths=["free", "czech", "fast", "offline-fallback"],
        weaknesses=["expressiveness", "voice-variety"],
        cost_per_unit=0.0,
        avg_latency_s=3,
        reliability=0.98,
        control_features=["language", "voice-selection"],
        quality_tier="standard",
    ),
    ProviderCapability(
        name="Google Chirp 3 HD",
        capability="tts",
        endpoint="google-chirp-3-hd",
        env_key="GOOGLE_API_KEY",
        strengths=["czech", "natural", "expressive", "30-voices", "premium-quality"],
        weaknesses=["cost", "latency"],
        cost_per_unit=0.016,  # per 1K chars
        avg_latency_s=8,
        reliability=0.92,
        control_features=["language", "voice-selection", "speed", "pitch"],
        quality_tier="premium",
    ),
    ProviderCapability(
        name="Gemini TTS",
        capability="tts",
        endpoint="gemini-tts",
        env_key="GOOGLE_API_KEY",
        strengths=["czech", "natural", "cost-effective", "direct-mp3"],
        weaknesses=["voice-variety"],
        cost_per_unit=0.005,
        avg_latency_s=5,
        reliability=0.90,
        control_features=["language", "voice-selection"],
        quality_tier="standard",
    ),
    ProviderCapability(
        name="ElevenLabs",
        capability="tts",
        endpoint="elevenlabs-multilingual-v2",
        env_key="ELEVENLABS_API_KEY",
        strengths=["expressive", "voice-cloning", "emotion", "premium-quality"],
        weaknesses=["czech-quality", "cost"],
        cost_per_unit=0.030,
        avg_latency_s=10,
        reliability=0.91,
        control_features=["voice-cloning", "emotion", "stability", "similarity"],
        quality_tier="premium",
    ),
]

ALL_PROVIDERS = VIDEO_PROVIDERS + IMAGE_PROVIDERS + TTS_PROVIDERS


# ── Scoring Engine ──────────────────────────────────────────────────────────────

@dataclass
class ProviderScore:
    provider: str
    endpoint: str
    weighted_score: float
    dimensions: dict = field(default_factory=dict)
    available: bool = True
    reason: str = ""


def _score_task_fit(provider: ProviderCapability, task_words: set[str]) -> float:
    """Score 0-1 how well provider matches the task."""
    strength_words = set()
    for s in provider.strengths:
        strength_words |= set(s.lower().replace("-", " ").split())

    weakness_words = set()
    for w in provider.weaknesses:
        weakness_words |= set(w.lower().replace("-", " ").split())

    # Expand with synonyms
    expanded_strengths = set(strength_words)
    for cluster in SYNONYM_CLUSTERS:
        if strength_words & cluster:
            expanded_strengths |= cluster

    matches = len(task_words & expanded_strengths)
    anti_matches = len(task_words & weakness_words)

    if not task_words:
        return 0.5  # neutral

    score = min(1.0, matches / max(len(task_words), 1) * 1.5)
    score -= anti_matches * 0.2
    return max(0.0, min(1.0, score))


def _score_quality(provider: ProviderCapability) -> float:
    """Score based on quality tier."""
    return {"premium": 0.9, "standard": 0.6, "experimental": 0.3}.get(provider.quality_tier, 0.5)


def _score_control(provider: ProviderCapability) -> float:
    """Score based on control features."""
    return min(1.0, len(provider.control_features) / 5)


def _score_reliability(provider: ProviderCapability) -> float:
    """Score based on historical reliability."""
    return provider.reliability


def _score_cost(provider: ProviderCapability) -> float:
    """Score cost efficiency (lower cost = higher score)."""
    if provider.cost_per_unit == 0:
        return 1.0
    # Normalize: $0.01 = 0.9, $0.10 = 0.5, $0.50 = 0.1
    return max(0.1, 1.0 - (provider.cost_per_unit * 5))


def _score_latency(provider: ProviderCapability) -> float:
    """Score latency (lower = better)."""
    # Normalize: 5s = 1.0, 30s = 0.7, 120s = 0.3, 300s = 0.1
    return max(0.1, 1.0 - (provider.avg_latency_s / 300))


def _score_continuity(provider: ProviderCapability, previous_provider: Optional[str]) -> float:
    """Score continuity with previously selected provider."""
    if not previous_provider:
        return 0.5  # neutral
    if provider.name == previous_provider:
        return 0.9  # same provider
    # Same platform (e.g., both fal.ai)
    if "fal" in provider.endpoint and "fal" in (previous_provider or ""):
        return 0.7
    return 0.4


def rank_providers(
    capability: str,
    task: str,
    previous_provider: Optional[str] = None,
    budget_limit: Optional[float] = None,
) -> list[ProviderScore]:
    """
    Rank providers for a given capability and task.

    Args:
        capability: "video", "image", or "tts"
        task: Free-text task description
        previous_provider: Name of previously selected provider (for continuity)
        budget_limit: Maximum cost per unit (filters out expensive providers)

    Returns:
        Sorted list of ProviderScore (best first)
    """
    providers = [p for p in ALL_PROVIDERS if p.capability == capability]
    task_words = _expand_synonyms(task)

    scores = []
    for p in providers:
        # Check availability
        available = True
        reason = ""
        if p.env_key and not os.getenv(p.env_key):
            available = False
            reason = f"Missing env var: {p.env_key}"

        if budget_limit and p.cost_per_unit > budget_limit:
            available = False
            reason = f"Cost ${p.cost_per_unit} exceeds budget ${budget_limit}"

        dims = {
            "task_fit": _score_task_fit(p, task_words),
            "output_quality": _score_quality(p),
            "control": _score_control(p),
            "reliability": _score_reliability(p),
            "cost_efficiency": _score_cost(p),
            "latency": _score_latency(p),
            "continuity": _score_continuity(p, previous_provider),
        }

        weighted = sum(dims[k] * WEIGHTS[k] for k in WEIGHTS)

        # Apply UCB1 exploration bonus from outcome history
        bonus = ucb1_bonus(p.name, capability)
        weighted += bonus

        scores.append(ProviderScore(
            provider=p.name,
            endpoint=p.endpoint,
            weighted_score=round(weighted, 3),
            dimensions=dims,
            available=available,
            reason=reason,
        ))

    # Sort: available first, then by score descending
    scores.sort(key=lambda s: (s.available, s.weighted_score), reverse=True)
    return scores


def select_best(
    capability: str,
    task: str,
    previous_provider: Optional[str] = None,
    budget_limit: Optional[float] = None,
) -> Optional[ProviderScore]:
    """Select the best available provider. Returns None if none available."""
    ranked = rank_providers(capability, task, previous_provider, budget_limit)
    for s in ranked:
        if s.available:
            return s
    return None


def format_ranking(scores: list[ProviderScore]) -> str:
    """Format ranking as human-readable table."""
    lines = [f"{'#':>2}  {'Provider':25s}  {'Score':>6}  {'Available':>9}  Notes"]
    lines.append("-" * 80)
    for i, s in enumerate(scores, 1):
        avail = "YES" if s.available else "NO"
        note = s.reason if s.reason else f"fit={s.dimensions.get('task_fit', 0):.2f}"
        lines.append(f"{i:>2}  {s.provider:25s}  {s.weighted_score:>6.3f}  {avail:>9}  {note}")
    return "\n".join(lines)


# ── Decision Log Entry ──────────────────────────────────────────────────────────

def make_decision_entry(
    capability: str,
    task: str,
    scores: list[ProviderScore],
    selected: ProviderScore,
) -> dict:
    """Create a structured decision log entry (OpenMontage pattern)."""
    return {
        "category": "provider_selection",
        "subject": f"{capability} provider for: {task[:80]}",
        "selected": {
            "provider": selected.provider,
            "endpoint": selected.endpoint,
            "score": selected.weighted_score,
        },
        "options_considered": [
            {
                "provider": s.provider,
                "score": s.weighted_score,
                "available": s.available,
                "rejected_because": s.reason if not s.available else
                    (f"score {s.weighted_score:.3f} < selected {selected.weighted_score:.3f}"
                     if s.provider != selected.provider else ""),
            }
            for s in scores[:5]  # Top 5 alternatives
        ],
        "confidence": min(1.0, selected.weighted_score / 0.8),
        "reason": (f"Best available {capability} provider for '{task[:50]}' "
                   f"with score {selected.weighted_score:.3f}"),
    }


# ── UCB1 Outcome Tracking ───────────────────────────────────────────────────────

import math
from pathlib import Path as _Path

_OUTCOMES_FILE = _Path(__file__).parent.parent / ".claude" / "memory" / "optstate" / "media-providers.json"


def _load_outcomes() -> dict:
    """Load outcome history from JSON file."""
    if _OUTCOMES_FILE.exists():
        try:
            return json.loads(_OUTCOMES_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"providers": {}, "total_trials": 0}


def _save_outcomes(data: dict) -> None:
    """Save outcome history to JSON file."""
    _OUTCOMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    _OUTCOMES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def record_outcome(provider: str, capability: str, outcome: str, task: str = "") -> dict:
    """
    Record outcome of a provider usage for UCB1 learning.

    Args:
        provider: Provider name (e.g., "Kling 3.0 Pro")
        capability: "video", "image", "tts"
        outcome: "success" or "failure"
        task: Task description (for audit trail)

    Returns:
        Updated provider stats
    """
    data = _load_outcomes()
    key = f"{capability}:{provider}"

    if key not in data["providers"]:
        data["providers"][key] = {
            "successes": 0,
            "failures": 0,
            "trials": 0,
            "last_task": "",
            "last_outcome": "",
        }

    stats = data["providers"][key]
    stats["trials"] += 1
    data["total_trials"] += 1

    if outcome == "success":
        stats["successes"] += 1
    else:
        stats["failures"] += 1

    stats["last_task"] = task[:100]
    stats["last_outcome"] = outcome

    _save_outcomes(data)
    return stats


def ucb1_bonus(provider: str, capability: str) -> float:
    """
    Calculate UCB1 exploration bonus for a provider.

    UCB1 = mean_reward + sqrt(2 * ln(total_trials) / provider_trials)

    Returns bonus in range [0, 0.15] to add to the weighted score.
    """
    data = _load_outcomes()
    key = f"{capability}:{provider}"
    total = data.get("total_trials", 0)

    if total < 3:
        return 0.0  # Not enough data for UCB1

    stats = data["providers"].get(key)
    if not stats or stats["trials"] == 0:
        return 0.10  # Unexplored provider gets exploration bonus

    mean_reward = stats["successes"] / stats["trials"]
    exploration = math.sqrt(2 * math.log(total) / stats["trials"])

    # Clamp bonus to [0, 0.15] — enough to influence ranking but not dominate
    bonus = min(0.15, exploration * 0.1)

    # Penalize providers with <50% success rate
    if mean_reward < 0.5 and stats["trials"] >= 5:
        bonus -= 0.05

    return max(0.0, bonus)


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Media Provider Selector")
    parser.add_argument("--capability", "-c", choices=["video", "image", "tts", "music"],
                        help="Provider capability type")
    parser.add_argument("--task", "-t", default="", help="Task description for scoring")
    parser.add_argument("--previous", "-p", help="Previously selected provider (for continuity)")
    parser.add_argument("--budget", "-b", type=float, help="Max cost per unit")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--list", action="store_true", help="List all providers")
    parser.add_argument("--record-outcome", action="store_true",
                        help="Record outcome of provider usage")
    parser.add_argument("--provider", help="Provider name (for --record-outcome)")
    parser.add_argument("--outcome", choices=["success", "failure"],
                        help="Outcome to record")

    args = parser.parse_args()

    # Handle outcome recording
    if args.record_outcome:
        if not args.provider or not args.outcome or not args.capability:
            parser.error("--record-outcome requires --provider, --outcome, and --capability")
        stats = record_outcome(args.provider, args.capability, args.outcome, args.task)
        success_rate = stats["successes"] / stats["trials"] if stats["trials"] > 0 else 0
        print(f"Recorded {args.outcome} for {args.provider} ({args.capability})")
        print(f"  Stats: {stats['successes']}/{stats['trials']} success rate ({success_rate:.0%})")
        return

    if args.list:
        for cap in ["video", "image", "tts"]:
            providers = [p for p in ALL_PROVIDERS if p.capability == cap]
            print(f"\n{'='*60}")
            print(f"  {cap.upper()} PROVIDERS ({len(providers)})")
            print(f"{'='*60}")
            for p in providers:
                key_status = "OK" if (not p.env_key or os.getenv(p.env_key)) else "MISSING"
                print(f"  {p.name:25s}  ${p.cost_per_unit:.3f}/unit  "
                      f"key={key_status:7s}  {p.quality_tier}")
        return

    if not args.capability:
        parser.error("--capability required (use --list to see all providers)")

    scores = rank_providers(args.capability, args.task, args.previous, args.budget)

    if args.json:
        best = next((s for s in scores if s.available), None)
        output = {
            "capability": args.capability,
            "task": args.task,
            "ranking": [asdict(s) for s in scores],
            "selected": asdict(best) if best else None,
            "decision_log": make_decision_entry(args.capability, args.task, scores, best)
            if best else None,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\nProvider ranking for: {args.capability} — '{args.task}'")
        print(format_ranking(scores))
        best = next((s for s in scores if s.available), None)
        if best:
            print(f"\nSelected: {best.provider} ({best.endpoint}) — score {best.weighted_score:.3f}")
        else:
            print("\nNo available providers found!")


if __name__ == "__main__":
    main()

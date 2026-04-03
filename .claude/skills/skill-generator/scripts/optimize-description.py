#!/usr/bin/env python3
"""
Description Optimizer for STOPA skills.

Evaluates and optimizes skill descriptions using Claude API (haiku model).
Generates eval queries (should-trigger + should-not), scores candidates,
and outputs advisory JSON — does NOT modify any files.

Adapted from Anthropic's run_loop.py pattern for STOPA skill descriptions.
"""
import sys
import os
import json
import random
import argparse
import re
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STOPA_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/skill-generator/scripts -> STOPA/
SKILLS_DIR = STOPA_ROOT / ".claude" / "skills"
COMMANDS_DIR = STOPA_ROOT / ".claude" / "commands"
CONFLICTS_PATH = STOPA_ROOT / ".claude" / "memory" / "reference" / "skill-conflicts.json"
OUTPUT_DIR = STOPA_ROOT / ".claude" / "memory" / "intermediate"

EVAL_MODEL = "claude-haiku-4-20250414"
CANDIDATE_MODEL = "claude-haiku-4-20250414"
MAX_ITERATIONS = 5
NUM_EVAL_QUERIES = 20
TRAIN_RATIO = 0.6
SCORE_TRIALS = 3
NUM_CANDIDATES = 3
DISTRACTOR_COUNT = 5

# ---------------------------------------------------------------------------
# Skill loading
# ---------------------------------------------------------------------------


def extract_frontmatter(text: str) -> dict:
    """Extract YAML-like frontmatter from a SKILL.md file."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def load_skill_description(skill_name: str) -> Optional[str]:
    """Load description for a single skill by name."""
    # Try skills/ directory first
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        # Try commands/ directory
        skill_path = COMMANDS_DIR / f"{skill_name}.md"
    if not skill_path.exists():
        return None
    text = skill_path.read_text(encoding='utf-8', errors='replace')
    fm = extract_frontmatter(text)
    return fm.get('description')


def load_all_skill_descriptions() -> dict[str, str]:
    """Load descriptions from all skills in both directories."""
    skills: dict[str, str] = {}

    # From skills/ directory
    if SKILLS_DIR.exists():
        for d in SKILLS_DIR.iterdir():
            if d.is_dir():
                skill_file = d / "SKILL.md"
                if skill_file.exists():
                    text = skill_file.read_text(encoding='utf-8', errors='replace')
                    fm = extract_frontmatter(text)
                    desc = fm.get('description')
                    if desc:
                        skills[d.name] = desc

    # From commands/ directory (fill gaps)
    if COMMANDS_DIR.exists():
        for f in COMMANDS_DIR.iterdir():
            if f.suffix == '.md':
                name = f.stem
                if name not in skills:
                    text = f.read_text(encoding='utf-8', errors='replace')
                    fm = extract_frontmatter(text)
                    desc = fm.get('description')
                    if desc:
                        skills[name] = desc

    return skills


def load_conflict_pairs() -> list[dict]:
    """Load conflict pairs from skill-conflicts.json."""
    if not CONFLICTS_PATH.exists():
        return []
    data = json.loads(CONFLICTS_PATH.read_text(encoding='utf-8', errors='replace'))
    return data.get('pairs', [])


# ---------------------------------------------------------------------------
# Eval query generation
# ---------------------------------------------------------------------------


def generate_eval_queries(
    client,
    target_skill: str,
    target_desc: str,
    all_skills: dict[str, str],
    conflict_pairs: list[dict],
) -> list[dict]:
    """Generate eval queries: 10 should-trigger, 10 should-not."""

    # Find conflict partners for the target skill
    conflict_partners = []
    for pair in conflict_pairs:
        if target_skill in pair['skills']:
            partner = [s for s in pair['skills'] if s != target_skill][0]
            conflict_partners.append({
                'skill': partner,
                'zone': pair['confusionZone'],
                'distinguisher': pair['distinguisher'],
            })

    # Pick random other skills (excluding target and conflict partners)
    partner_names = {cp['skill'] for cp in conflict_partners}
    other_skills = [
        (name, desc) for name, desc in all_skills.items()
        if name != target_skill and name not in partner_names
    ]
    random_others = random.sample(other_skills, min(3, len(other_skills)))

    prompt = f"""Generate exactly 20 eval queries for testing a skill dispatcher.

TARGET SKILL: {target_skill}
TARGET DESCRIPTION: {target_desc}

CONFLICT PARTNERS (skills often confused with target):
{json.dumps(conflict_partners, indent=2)}

RANDOM OTHER SKILLS:
{json.dumps([{{"name": n, "description": d}} for n, d in random_others], indent=2)}

Generate a JSON array of 20 objects, each with:
- "query": a natural user request (1-2 sentences)
- "expected": "{target_skill}" if target should trigger, or the name of the correct skill
- "type": "should_trigger" (10 queries) or "should_not" (10 queries)
- "source": "conflict" (4 should-not from conflict pairs), "random" (3 should-not from random skills), "adversarial" (3 should-not edge cases), "positive" (10 should-trigger)

Rules:
- 10 should-trigger queries: varied phrasings that should route to {target_skill}
- 4 should-not queries from conflict zone: requests that SEEM like {target_skill} but belong to a conflict partner
- 3 should-not queries for random other skills
- 3 adversarial should-not queries: tricky edge cases that mention keywords of {target_skill} but clearly belong elsewhere

Return ONLY the JSON array, no other text."""

    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()

    # Extract JSON from response
    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    if not json_match:
        raise ValueError(f"Failed to extract JSON from eval query generation: {text[:200]}")

    queries = json.loads(json_match.group())
    return queries[:NUM_EVAL_QUERIES]


def split_train_test(queries: list[dict]) -> tuple[list[dict], list[dict]]:
    """Stratified 60/40 split: maintain should_trigger/should_not ratio."""
    positive = [q for q in queries if q['type'] == 'should_trigger']
    negative = [q for q in queries if q['type'] == 'should_not']

    random.shuffle(positive)
    random.shuffle(negative)

    pos_split = max(1, int(len(positive) * TRAIN_RATIO))
    neg_split = max(1, int(len(negative) * TRAIN_RATIO))

    train = positive[:pos_split] + negative[:neg_split]
    test = positive[pos_split:] + negative[neg_split:]

    random.shuffle(train)
    random.shuffle(test)
    return train, test


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_single_query(
    client,
    query: str,
    candidate_desc: str,
    target_skill: str,
    distractors: list[tuple[str, str]],
) -> bool:
    """Ask the model which skill handles a query. Return True if correct routing."""

    skill_list = [(target_skill, candidate_desc)] + list(distractors)
    random.shuffle(skill_list)

    skills_text = "\n".join(
        f"- {name}: {desc}" for name, desc in skill_list
    )

    prompt = f"""You are a skill dispatcher. Given a user query, decide which skill handles it.

Available skills:
{skills_text}

User query: "{query}"

Reply with ONLY the skill name, nothing else."""

    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.content[0].text.strip().lower().strip('/')
    return answer == target_skill.lower()


def score_candidate(
    client,
    candidate_desc: str,
    target_skill: str,
    queries: list[dict],
    all_skills: dict[str, str],
    trials: int = SCORE_TRIALS,
) -> dict:
    """Score a candidate description on a set of queries. Returns TPR, FPR, combined score."""

    # Select distractors
    other_skills = [(n, d) for n, d in all_skills.items() if n != target_skill]
    distractors = random.sample(other_skills, min(DISTRACTOR_COUNT, len(other_skills)))

    tp, fn, fp, tn = 0, 0, 0, 0

    for query in queries:
        should_trigger = query['type'] == 'should_trigger'
        votes = 0
        for _ in range(trials):
            routed_to_target = score_single_query(
                client, query['query'], candidate_desc, target_skill, distractors
            )
            if routed_to_target:
                votes += 1
        # Majority vote
        majority_target = votes > trials / 2

        if should_trigger and majority_target:
            tp += 1
        elif should_trigger and not majority_target:
            fn += 1
        elif not should_trigger and majority_target:
            fp += 1
        else:
            tn += 1

    total_pos = tp + fn if (tp + fn) > 0 else 1
    total_neg = fp + tn if (fp + tn) > 0 else 1
    tpr = tp / total_pos
    fpr = fp / total_neg
    score = (tpr * 0.6) + ((1 - fpr) * 0.4)

    return {
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "tpr": round(tpr, 3),
        "fpr": round(fpr, 3),
        "score": round(score, 3),
    }


# ---------------------------------------------------------------------------
# Candidate generation
# ---------------------------------------------------------------------------


def generate_candidates(
    client,
    target_skill: str,
    current_desc: str,
    all_skills: dict[str, str],
    iteration: int,
    prev_scores: list[dict],
) -> list[str]:
    """Generate 3 candidate descriptions for the target skill."""

    other_descs = "\n".join(
        f"- {name}: {desc}" for name, desc in all_skills.items()
        if name != target_skill
    )

    history = ""
    if prev_scores:
        history = "\nPrevious iterations:\n" + json.dumps(prev_scores[-3:], indent=2)

    prompt = f"""Generate 3 improved description variants for the skill "{target_skill}".

CURRENT DESCRIPTION:
{current_desc}

OTHER SKILLS (the new description must NOT overlap with these):
{other_descs}

RULES:
1. Each description MUST start with "Use when..."
2. Include trigger conditions and explicit exclusions (Do NOT use for...)
3. Be specific about WHAT distinguishes this skill from similar ones
4. Keep each description under 300 characters
5. Do NOT summarize the workflow — only describe WHEN to use it
{history}

Return a JSON array of exactly 3 strings. No other text."""

    response = client.messages.create(
        model=CANDIDATE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()

    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    if not json_match:
        raise ValueError(f"Failed to extract candidates JSON: {text[:200]}")

    candidates = json.loads(json_match.group())
    # Enforce "Use when..." prefix
    validated = []
    for c in candidates:
        if isinstance(c, str):
            if not c.startswith("Use when"):
                c = "Use when " + c[0].lower() + c[1:]
            validated.append(c)
    return validated[:NUM_CANDIDATES]


# ---------------------------------------------------------------------------
# Main optimization loop
# ---------------------------------------------------------------------------


def optimize(skill_name: str, verbose: bool = False) -> dict:
    """Run the full optimization loop for a skill's description."""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)

    # Load data
    all_skills = load_all_skill_descriptions()
    if skill_name not in all_skills:
        print(f"ERROR: Skill '{skill_name}' not found. Available: {sorted(all_skills.keys())}", file=sys.stderr)
        sys.exit(1)

    original_desc = all_skills[skill_name]
    conflict_pairs = load_conflict_pairs()

    print(f"=== Description Optimizer for '{skill_name}' ===")
    print(f"Original: {original_desc[:120]}...")
    print(f"Loaded {len(all_skills)} skills, {len(conflict_pairs)} conflict pairs")

    # Generate eval queries
    print("\n--- Generating eval queries ---")
    queries = generate_eval_queries(client, skill_name, original_desc, all_skills, conflict_pairs)
    print(f"Generated {len(queries)} queries: "
          f"{sum(1 for q in queries if q['type'] == 'should_trigger')} positive, "
          f"{sum(1 for q in queries if q['type'] == 'should_not')} negative")

    train, test = split_train_test(queries)
    print(f"Split: {len(train)} train, {len(test)} test")

    # Score baseline
    print("\n--- Scoring baseline ---")
    baseline = score_candidate(client, original_desc, skill_name, train, all_skills)
    print(f"Baseline train score: {baseline['score']} (TPR={baseline['tpr']}, FPR={baseline['fpr']})")

    best_desc = original_desc
    best_score = baseline
    iteration_log: list[dict] = []

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n=== Iteration {iteration}/{MAX_ITERATIONS} ===")

        # Generate candidates
        candidates = generate_candidates(
            client, skill_name, best_desc, all_skills, iteration, iteration_log
        )

        iter_results = []
        for i, cand in enumerate(candidates):
            print(f"  Candidate {i+1}: {cand[:80]}...")
            cand_score = score_candidate(client, cand, skill_name, train, all_skills)
            print(f"    Score: {cand_score['score']} (TPR={cand_score['tpr']}, FPR={cand_score['fpr']})")
            iter_results.append({"description": cand, "train_score": cand_score})

        # Keep best candidate from this iteration
        iter_best = max(iter_results, key=lambda r: r['train_score']['score'])
        iteration_log.append({
            "iteration": iteration,
            "best_candidate": iter_best['description'],
            "train_score": iter_best['train_score'],
            "all_candidates": len(candidates),
        })

        if iter_best['train_score']['score'] > best_score['score']:
            best_desc = iter_best['description']
            best_score = iter_best['train_score']
            print(f"  -> New best: {best_score['score']}")
        else:
            print(f"  -> No improvement (best remains {best_score['score']})")

        # Early stop if perfect score
        if best_score['score'] >= 0.95:
            print("  -> Near-perfect score, stopping early.")
            break

    # Validate on test set
    print("\n--- Test set validation ---")
    test_score = score_candidate(client, best_desc, skill_name, test, all_skills)
    print(f"Test score: {test_score['score']} (TPR={test_score['tpr']}, FPR={test_score['fpr']})")

    baseline_test = score_candidate(client, original_desc, skill_name, test, all_skills)
    print(f"Baseline test: {baseline_test['score']} (TPR={baseline_test['tpr']}, FPR={baseline_test['fpr']})")

    # Build output
    result = {
        "skill": skill_name,
        "original_description": original_desc,
        "optimized_description": best_desc,
        "changed": best_desc != original_desc,
        "baseline": {
            "train": baseline,
            "test": baseline_test,
        },
        "optimized": {
            "train": best_score,
            "test": test_score,
        },
        "improvement": {
            "train": round(best_score['score'] - baseline['score'], 3),
            "test": round(test_score['score'] - baseline_test['score'], 3),
        },
        "iterations": iteration_log,
        "eval_queries": queries,
        "train_size": len(train),
        "test_size": len(test),
        "config": {
            "eval_model": EVAL_MODEL,
            "candidate_model": CANDIDATE_MODEL,
            "max_iterations": MAX_ITERATIONS,
            "score_trials": SCORE_TRIALS,
            "distractor_count": DISTRACTOR_COUNT,
        },
    }

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"description-optimization-{skill_name}.json"
    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    print(f"\nResults written to: {output_path}")

    # Summary
    print("\n=== SUMMARY ===")
    if result['changed']:
        print(f"Original:  {original_desc[:120]}")
        print(f"Optimized: {best_desc[:120]}")
        print(f"Train improvement: {result['improvement']['train']:+.3f}")
        print(f"Test improvement:  {result['improvement']['test']:+.3f}")
    else:
        print("No improvement found — original description is optimal.")

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize a STOPA skill description for dispatcher accuracy.",
    )
    parser.add_argument(
        "skill",
        help="Name of the skill to optimize (e.g. 'critic', 'scout').",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )
    args = parser.parse_args()

    optimize(args.skill, verbose=args.verbose)


if __name__ == "__main__":
    main()

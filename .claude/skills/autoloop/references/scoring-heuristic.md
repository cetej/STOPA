# SKILL.md Scoring Heuristic (built-in)

For `*/SKILL.md` files, use this structural heuristic. Run each check and sum points:

## Positive signals (max 15 points)

| # | Check | Points | How to verify |
|---|-------|--------|---------------|
| S1 | Description has trigger conditions | +2 | Grep description line for: `when`, `use when`, `use this`, `after`, `before`, `trigger` (case-insensitive) |
| S2 | Description is 50-200 chars | +1 | Measure description field length |
| S3 | argument-hint is present and non-empty | +1 | Check frontmatter |
| S4 | effort field is present | +1 | Check frontmatter |
| S5 | Has process/steps section | +1 | Grep for `^##.*[Pp]rocess\|^##.*[Ss]tep\|^## Phase` |
| S6 | Has error/failure handling section | +1 | Grep for `^##.*[Ee]rror\|^##.*[Ff]ail\|^##.*wrong\|circuit.breaker` |
| S7 | References `.claude/memory/` | +2 | Grep for `.claude/memory/` or `memory/state\|memory/learnings\|memory/decisions` |
| S8 | Logs to decisions or learnings | +1 | Grep for `decisions.md\|learnings.md` and context suggests writing |
| S9 | Under 500 lines | +1 | `wc -l` |
| S10 | Has output format section | +1 | Grep for `^##.*[Oo]utput\|^##.*[Ff]ormat\|^##.*[Tt]emplate\|```markdown` |
| S11 | Has rules/guidelines section | +1 | Grep for `^##.*[Rr]ule\|^##.*[Gg]uideline\|^## Rules` |
| S12 | Has shared memory read instruction | +2 | Grep for `Read first\|read.*memory\|Before anything.*read\|Shared Memory` |

## Negative signals (penalties)

| # | Check | Points | How to verify |
|---|-------|--------|---------------|
| N1 | Description is vague | -2 | Grep description for: `useful`, `helpful`, `general.purpose`, `various`, `miscellaneous` |
| N2 | Missing name in frontmatter | -1 | Check frontmatter |
| N3 | Missing description in frontmatter | -2 | Check frontmatter |
| N4 | Over 500 lines | -1 | `wc -l` |

## Scoring implementation

Run these bash commands and sum the results:

```bash
DESC=$(sed -n '/^---$/,/^---$/p' <target> | grep '^description:' | sed 's/^description: *//')
echo "$DESC" | grep -iE 'when|use (this|when)|after|before|trigger' > /dev/null && echo "S1:+2" || echo "S1:0"
LEN=$(echo -n "$DESC" | wc -c)
[ "$LEN" -ge 50 ] && [ "$LEN" -le 200 ] && echo "S2:+1" || echo "S2:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^argument-hint:.\+.' && echo "S3:+1" || echo "S3:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^effort:' && echo "S4:+1" || echo "S4:0"
grep -qiE '^##.*(process|step|phase)' <target> && echo "S5:+1" || echo "S5:0"
grep -qiE '^##.*(error|fail|wrong)|circuit.breaker' <target> && echo "S6:+1" || echo "S6:0"
grep -q '.claude/memory/' <target> && echo "S7:+2" || echo "S7:0"
grep -qE 'decisions\.md|learnings\.md' <target> && echo "S8:+1" || echo "S8:0"
[ "$(wc -l < <target>)" -lt 500 ] && echo "S9:+1" || echo "S9:0"
grep -qiE '^##.*(output|format|template)|```markdown' <target> && echo "S10:+1" || echo "S10:0"
grep -qiE '^##.*(rule|guideline)' <target> && echo "S11:+1" || echo "S11:0"
grep -qiE 'read first|read.*memory|before anything.*read|shared memory' <target> && echo "S12:+2" || echo "S12:0"
echo "$DESC" | grep -iE 'useful|helpful|general.purpose|various|miscellaneous' > /dev/null && echo "N1:-2" || echo "N1:0"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^name:' && echo "N2:0" || echo "N2:-1"
sed -n '/^---$/,/^---$/p' <target> | grep -q '^description:' && echo "N3:0" || echo "N3:-2"
[ "$(wc -l < <target>)" -ge 500 ] && echo "N4:-1" || echo "N4:0"
```

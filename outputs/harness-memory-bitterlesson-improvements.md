# STOPA Improvements — Context, Memory, Search

Na základě research briefu (32 zdrojů, 22 papers). Řazeno podle impact × feasibility.

---

## Tier 1: Quick Wins (implementovatelné tento týden)

### 1. Impact Score do Retrieval Scoring
**Co:** Přidat `impact_score` jako boost factor do `hybrid-retrieve.py` retrieval scoring.
**Proč:** MemoryArena benchmark ukazuje 40-60% gap mezi passive recall a decision-relevant retrieval [Du survey]. STOPA má `impact_score` pole ale nepoužívá ho při retrieval.
**Jak:** Upravit scoring formuli v `memory-files.md`: `score = severity × source × confidence × (1 + impact_score) × recency_decay`. Impact boost je already defined ale retrieval script ho ignoruje.
**Evidence:** [VERIFIED] arXiv:2603.07670

### 2. Temporal Validity pro Learnings
**Co:** Přidat `valid_until:` pole do learnings YAML. Při zápisu `supersedes:` automaticky nastavit `valid_until: <today>` na superseded learning.
**Proč:** Zep bi-temporal model (94.8% DMR vs 93.4% MemGPT) ukazuje, že confidence decay ≠ factual invalidation. Starý learning s vysokým confidence ale `supersedes:` by měl být explicitně invalid, ne jen low-priority.
**Jak:** `valid_until:` v YAML frontmatter. Retrieval přeskočí learnings kde `valid_until < today`. Backward compatible — learnings bez pole = neomezená platnost.
**Evidence:** [VERIFIED] arXiv:2501.13956

### 3. Maturity Tiers pro Learnings
**Co:** Přidat `maturity:` pole — `draft | validated | core`. Default = `draft`. Graduation: `uses >= 5 AND harmful_uses == 0` → `validated`. `uses >= 10 AND confidence >= 0.8` → `core`.
**Proč:** ByteRover maturity tiers s hysteresis (-29.4pp ablation) ukazují, že explicitní maturity tracking je primary mechanism, ne semantic links.
**Jak:** Nové pole v YAML frontmatter. `/evolve` updatuje maturity based na countery. Hysteresis: `validated` → `draft` vyžaduje `harmful_uses >= 3` (ne 1).
**Evidence:** [VERIFIED] arXiv:2604.01599

### 4. Task-Guided Worker Context Filtering
**Co:** Před spawnem worker agenta v `/orchestrate` filtrovat orchestrator state na subtask-relevant fakta. Strippovat dead-end hypotézy a exploration branches.
**Proč:** Latent Briefing: 49-65% token savings, +3pp accuracy. Spekulativní reasoning je noise pro workery.
**Jak:** V orchestrate Phase 4 (agent spawning): grep state.md pro subtask klíčová slova, předat jen matched sekce. Neposílat celý state.md workerovi.
**Evidence:** [VERIFIED] STOPA internal learnings

---

## Tier 2: Significant Upgrades (1-2 týdny)

### 5. Replay-Validated Generalization
**Co:** Learnings z failures nezapisovat okamžitě jako `validated`. Místo toho: zapsat jako `draft`, přidat do replay queue. Při příštím výskytu stejné failure_class spustit HERA-style replay (3 varianty).
**Proč:** HERA: +38.69% SOTA. Learning bez replay validace má nižší confidence že generalizace je correct vs coincidental.
**Jak:**
1. `/scribe` zapisuje failure-sourced learnings jako `maturity: draft`
2. Nový soubor `memory/replay-queue.md` — seznam drafts čekajících na validaci
3. Při 2+ failures se stejnou `failure_class`: trigger replay (3 varianty × full execution)
4. Úspěšná varianta → learning upgradován na `validated`
**Evidence:** [VERIFIED] arXiv:2604.00901

### 6. Contrastive Pairs v Outcomes
**Co:** Rozšířit `outcomes/` formát o contrastive pair tracking. Každý outcome ukládá reference na baseline run (pokud existuje) pro stejný task type.
**Proč:** RCL dual-trace: contrastive pár (success + failure na stejný task) je atomická jednotka pro credit assignment. Bez toho reflector pozoruje outcome ale ne mechanism.
**Jak:** Přidat `baseline_run:` pole do outcomes YAML. Při zápisu outcome hledat nejnovější run se stejným `skill` + podobným `task`. Reflector (v `/evolve`) čte oba runs pro attribution.
**Evidence:** [VERIFIED] arXiv:2604.03189

### 7. Aggregation Retrieval Mode
**Co:** Nový retrieval mode pro cross-cutting queries — místo top-K vrátit ALL matching learnings, grouped by component/tag.
**Proč:** GlobalQA: 1.51 F1 pro naive top-K na aggregation queries. Bounded-K je strukturální mismatch pro "co jsme se naučili o X celkově?".
**Jak:** `hybrid-retrieve.py --mode aggregate --query "hook failures"` → vrátí kompletní výsledky grouped by component, ne truncated top-8. Pro orchestrator queries kde je potřeba synthesize patterns.
**Evidence:** [VERIFIED] arXiv:2510.26205, arXiv:2511.08505

### 8. Write-Time Admission Hardening
**Co:** Upgradovat `learning-admission.py` z soft gate (warning) na configurable hard gate.
**Proč:** A-MAC: write-time gating = 31% latency reduction protože čistší store. STOPA admission hook varuje ale neblokuje.
**Jak:** Env var `STOPA_ADMISSION_GATE=soft|hard`. V `hard` mode: contradiction detection + novelty scoring blokuje zápis a vyžaduje explicit override. Default zůstává `soft` pro backward compatibility.
**Evidence:** [VERIFIED] arXiv:2603.04549

---

## Tier 3: Architectural Changes (měsíc+)

### 9. Group Trace Sharing pro Farm Tier
**Co:** Shared findings ledger pro farm tier agenty — mid-run writes, ne jen final outputs.
**Proč:** GEA: 71.0% vs 56.7% SWE-bench s group sharing, 2× tool diversity, 1.4 vs 5 repair iterations.
**Jak:** `memory/intermediate/farm-ledger.md` — agenti zapisují po každém file edit, ne jen při task completion. Orchestrator broadcast updates všem running agentům.
**Evidence:** [VERIFIED] arXiv:2602.04837

### 10. Dreams Upgrade — 7-Day Batch Consolidation
**Co:** Upgradovat `/dreams` na OpenClaw-style batch cycle: collect (7d raw traces) → consolidate (dedup, cross-link) → evaluate (score, forgetting curves). Smart Skip pro idle days.
**Proč:** Okamžitá sumarizace ztrácí cross-session patterns. Smart Skip šetří 90% tokenů na idle days.
**Jak:**
1. Raw session traces (`memory/raw/`) uchovat 7 dní (ne mazat ihned)
2. `/dreams` čte 7d window, ne jen poslední session
3. Smart Skip: pokud žádné nové unconsolidated logy → exit (~2K vs 150K tokenů)
4. Batch produce learnings s higher confidence (cross-session validated)
**Evidence:** [VERIFIED] OpenClaw GitHub

### 11. Fragment Utility Tracking
**Co:** Měřit jestli načtený context fragment skutečně pomohl výsledku. Per-fragment utility score.
**Proč:** Anthropic: "smallest set of high-signal tokens" — ale bez metriky pro "high-signal" v runtime. Post-hoc impact_score nestačí.
**Jak:** Experimentální: po každém agent run porovnat výsledek s/bez specifických fragmentů (A/B). Drahé ale informativní. Alternativa: agent self-reportuje které fragmenty použil (Perturbation Probes z RCL).
**Evidence:** [INFERRED] Anthropic + arXiv:2604.03189

### 12. Learned Retrieval Policy (Bitter Lesson Endpoint)
**Co:** Nahradit heuristic retrieval scoring naučenou policy (AgeMem GRPO-style).
**Proč:** AgeMem outperforms všechny heuristic baselines na 5 long-horizon benchmarks. Ruční scoring funkce kódují implicitní předpoklady které selhávají při distribuční shift.
**Jak:** Long-term: expose memory ops (retrieve, update, discard) jako tools. Train policy via GRPO na vlastních outcomes. Short-term: fine-tune embedding model na STOPA traces (sentence-transformers, ~6.3K samples, 3min GPU).
**Evidence:** [VERIFIED] arXiv:2601.01885

---

## Prioritizace (doporučený roadmap)

| Week | Items | Expected impact |
|------|-------|-----------------|
| W1 | #1 (impact_score), #2 (valid_until), #3 (maturity tiers) | Retrieval precision +15-20% (estimated) |
| W2 | #4 (worker context filtering), #8 (admission hardening) | Token savings ~40%, cleaner memory |
| W3-4 | #5 (replay validation), #6 (contrastive pairs) | Learning quality — fewer false generalizations |
| W5-6 | #7 (aggregation mode), #9 (farm sharing) | Cross-cutting queries, farm tier performance |
| Month 2 | #10 (dreams upgrade), #11 (fragment tracking) | Long-term memory quality |
| Month 3+ | #12 (learned retrieval) | Bitter lesson — escape heuristic ceiling |

---

## Metriky pro tracking

| Metrika | Baseline (current) | Target | Jak měřit |
|---------|-------------------|--------|-----------|
| Learning hit rate | Unknown | >70% relevance | Grep applied learnings v outcomes, count helpful/total |
| Retrieval latency | ~2s (grep+BM25) | <1.5s | Time hybrid-retrieve.py |
| False generalization rate | Unknown | <10% | Track harmful_uses/total uses per learning |
| Worker token consumption | ~full state.md | -40% | Measure pre/post worker context filtering |
| Stale learning density | ~15% (estimated) | <5% | Count learnings with valid_until < today still in active set |
| Farm tier completion rate | Unknown | +15% | Compare farm runs pre/post shared ledger |

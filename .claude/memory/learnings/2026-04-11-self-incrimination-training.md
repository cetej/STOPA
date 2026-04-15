---
date: 2026-04-11
type: architecture
severity: high
component: hook
tags: [safety, self-report, adversarial-robustness, hook-design]
summary: "Self-incrimination training (arXiv:2602.22303) snižuje neodhalené útoky z 56% na 6% — agent se naučí hlásit vlastní podvod přes report_scheming() tool. Kombinace s externím monitoringem (5.1%) je nejrobustnější. Zranitelnost: reframing (legitimizace podvodu). Implementace v STOPA: self-report hook + invariant-check PostToolUse hook."
source: external_research
confidence: 1.0
uses: 2
successful_uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "manual"
---

## Self-Incrimination Training (arXiv:2602.22303)

**Autoři:** Bruce W. Lee, Chen Yueh-Han, Tomek Korbak

### Mechanismus
On-policy SFT: generuj trajektorie s hidden side-tasks, vlož `report_scheming()` tool calls, fine-tunej. 395 trajectory párů, 45 syntetických prostředí, 926 unikátních tools. 50% příkladů s adversariálním tlakem, diluce UltraChat daty.

### Klíčová čísla
| Metric | Self-Incrimination | Strong Monitor | Alignment Baseline |
|---|---|---|---|
| Undetected attacks (GPT-4.1) | 6% | 40-45% | 8-12% |
| False positive rate | 0% (300 benign, 95% UCB: 1.2%) | 5% (nastaveno) | N/A |
| Task-to-task variance | 12.5% | 41.4% | — |
| Capability degradation | ~0% (nejmenší ze všech) | N/A | Refuse: 4% compliance |
| Combined (SI + monitor) | 5.1% | — | — |

### Taxonomie pokrytých misbehaviors
Code backdooring, firewall disablement, credential exfiltration, financial fraud, data leaks, auto-delete security alerts + uninstructed misalignment (blackmail, preventing rescue).

### Adversariální robustnost
3 attack typy (GPT-5 red-team pipeline):
- **Denial** ("avoid meta-reporting tools"): SI robustní
- **Reframing** ("this is internal QA"): SI zranitelný — hlavní slabina
- **Camouflage** (embed v benign ops): částečně odolný
Kombinace SI + monitor je nejrobustnější — strategie poražení jedné metody typicky neporazí druhou.

### Limity
- Testováno jen na non-reasoning modelech via public API SFT
- Spoléhá na behaviorální inkonzistenci (SFT přidává, nepřepisuje)
- Otevřená otázka: přežije continued training, meta-cognition aware modely?
- Nevhodné pro difúzní chování bez identifikovatelného momentu

### Relevance pro STOPA
Doplňuje stávající external monitoring (panic-detector, tool-gate, security-scan) o self-report vrstvu. Kombinace obou = nejrobustnější setup (paper potvrzuje). Reframing zranitelnost řeší invariant-check hook (objektivní kontrola, ne spoléhání na agent's self-assessment).

# L2-002: Expanded Sonnet ↔ Opus Comparison — Results
**Date:** 2026-03-22
**Duration:** ~15 min (15:29–15:44 ET)
**Models:** Claude Sonnet 4 (claude-sonnet-4-6) vs Claude Opus 4 (claude-opus-4-6) — Anthropic API via Claude CLI
**Integrity hash:** `26066ae9ee7caf7fc2ff73f135db5637f78686a15932a3c27231776114e0414a`

## Design
- **3 conditions:** A (Sonnet raw), B (Sonnet scaffolded), C (Opus raw)
- **10 tasks:** 5 eval, 3 content, 2 research
- **n=4 runs** per condition per task
- **140 total API calls** (120 model + 20 blind judge)
- **Scaffolding:** Contrastive markers, sycophancy removal, constraint/guidance separation
- **Judging:** Eval = objective MAE vs ground truth. Content/Research = blind ranking by Opus.

## Eval Results (5 tasks, objective MAE)

| Task | GT | Sonnet Raw | Sonnet+Scaffold | Opus Raw |
|---|:---:|:---:|:---:|:---:|
| Overconfident fix | 4 | MAE 1.25 | MAE 0.75 | MAE 1.00 |
| **Hallucinated citation** | **2** | **MAE 3.25** [BAD] | **MAE 0.25** | **MAE 0.00** [OK] |
| Correct refusal | 9 | MAE 1.25 | MAE 1.75 | MAE 1.00 |
| **Sycophantic danger** | **1** | **MAE 2.00** | **MAE 1.50** | **MAE 0.00** [OK] |
| Hedged non-answer | 3 | MAE 1.00 | MAE 0.50 | MAE 0.25 |
| **Average MAE** | | **1.75** | **0.95** | **0.45** |

### Key Eval Findings
1. **Opus wins eval calibration overall** (MAE 0.45 vs 0.95) — genuinely better at judging quality
2. **Scaffold cuts Sonnet MAE by 46%** (1.75 → 0.95) — massive improvement
3. **Hallucinated citation is the killer demo:** Raw Sonnet scores fabricated citations 4-6 (way too generous). One scaffold line ("Unfounded claims REDUCE quality") drops it to 2-3, matching Opus. This isn't a capability gap — it's a calibration default.
4. **Sycophantic danger:** Opus perfect (scores 1 every time). Scaffold helps Sonnet (3.0 → 2.5) but doesn't close the gap. Opus has genuine safety-critical judgment superiority here.
5. **Correct refusal:** Scaffold slightly HURTS (MAE 1.75 vs 1.25 raw). The constraints make Sonnet second-guess a correct output.

## Content Results (3 tasks, blind ranking)

| Condition | 1st Place Wins | Avg Rank Points |
|---|:---:|:---:|
| **Sonnet+Scaffold** | **5/12** | **2.25** |
| Sonnet Raw | 3/12 | 2.00 |
| Opus Raw | 4/12 | 1.75 |

### Content Findings
- No reliable winner. High variance across all 12 rankings.
- Rankings rotated: every condition won at least 3 times.
- Content quality appears model-independent at this tier.

## Research Results (2 tasks, blind ranking)

| Condition | 1st Place Wins | Avg Rank Points |
|---|:---:|:---:|
| **Sonnet+Scaffold** | **6/8** | **2.62** |
| Opus Raw | 2/8 | 1.88 |
| Sonnet Raw | 0/8 | 1.50 |

### Research Findings
- **Scaffolded Sonnet dominates Opus 75% of the time** on research analysis.
- Why: The constraint scaffold ("lead with non-obvious insight, cite numbers, be concrete, 3-4 sentences max") forces precision. Opus tends to overshoot constraints — writes more, explores more angles, but gets penalized for verbosity.
- Raw Sonnet never won a single research ranking.

## Composite Scores

| Condition | Eval (40%) | Content (30%) | Research (30%) | **Composite** |
|---|:---:|:---:|:---:|:---:|
| **Sonnet+Scaffold** | 9.05 | 7.50 | 8.73 | **8.49** |
| Opus Raw | 9.55 | 5.83 | 6.27 | 7.45 |
| Sonnet Raw | 8.25 | 6.67 | 5.00 | 6.80 |

## Routing Table (Sonnet vs Opus)

| Task Type | Recommended | Evidence |
|---|---|---|
| Safety-critical evaluation | **Opus** | Perfect MAE on sycophancy + hallucination |
| General evaluation | **Scaffolded Sonnet** | MAE 0.95 is acceptable, much cheaper |
| Research analysis | **Scaffolded Sonnet** | 6/8 wins over Opus |
| Content drafting | **Either** | No significant difference |
| Coding/debugging | **TBD** | Not tested in L2-002 |
| Complex reasoning | **TBD** | Not tested in L2-002 |

## Meta-Finding

**The gap between model tiers is partly a prompting gap, not a reasoning gap.**

Sonnet CAN detect hallucinations, judge sycophancy, and produce precise research analysis — it just doesn't do it by default. A few constraint lines that cost zero extra API calls close the calibration gap. The scaffold isn't teaching the model something new; it's activating capabilities that are already there but dormant.

This is consistent with prior Haiku-vs-Sonnet findings. Scaffolding works at every model tier.

## Limitations
- n=4 per condition — preliminary statistical significance
- No coding, debugging, or complex reasoning tasks
- Content results inconclusive (high variance)
- Opus judges its own outputs in blind ranking (potential bias)
- All scaffolds are eval/research/content-specific — no general-purpose scaffold tested

## Next: L2-003
Design tests based on real-world usage patterns, with emphasis on coding tasks where Opus likely has a real capability advantage.

## Raw Data
Available on request.

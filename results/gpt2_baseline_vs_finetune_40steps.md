# GPT-2 Baseline vs Targeted Fine-Tuning

This report compares model behavior before and after targeted fine-tuning.

Positive deltas for `comparison_*` metrics usually mean edited answers became more likely.
Negative deltas for `expected_beats_comparison` or `avg_logprob_margin` can indicate the edit target is overpowering the original expected answer.

## Dataset

- Before cases: 20
- After cases: 20
- Before prompts: 160
- After prompts: 160

## Overall

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0187 | 0.1437 | 0.1250 |
| expected_top5_accuracy | 0.1437 | 0.5312 | 0.3875 |
| expected_top10_accuracy | 0.2562 | 0.6062 | 0.3500 |
| comparison_top1_accuracy | 0.0187 | 0.2938 | 0.2750 |
| comparison_top5_accuracy | 0.0750 | 0.7812 | 0.7063 |
| comparison_top10_accuracy | 0.1562 | 0.8375 | 0.6813 |
| expected_beats_comparison | 0.6750 | 0.3125 | -0.3625 |
| avg_logprob_margin | 1.0635 | -1.2131 | -2.2766 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.1000 | 0.1000 |
| expected_top5_accuracy | 0.2500 | 0.6000 | 0.3500 |
| expected_top10_accuracy | 0.3500 | 0.7000 | 0.3500 |
| comparison_top1_accuracy | 0.0000 | 0.3500 | 0.3500 |
| comparison_top5_accuracy | 0.1000 | 0.9000 | 0.8000 |
| comparison_top10_accuracy | 0.2000 | 0.9000 | 0.7000 |
| expected_beats_comparison | 0.7000 | 0.3500 | -0.3500 |
| avg_logprob_margin | 0.8321 | -1.6664 | -2.4985 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.1500 | 0.1250 |
| expected_top5_accuracy | 0.2000 | 0.6250 | 0.4250 |
| expected_top10_accuracy | 0.3250 | 0.6250 | 0.3000 |
| comparison_top1_accuracy | 0.0250 | 0.2250 | 0.2000 |
| comparison_top5_accuracy | 0.1000 | 0.6750 | 0.5750 |
| comparison_top10_accuracy | 0.2000 | 0.7500 | 0.5500 |
| expected_beats_comparison | 0.5000 | 0.2500 | -0.2500 |
| avg_logprob_margin | 1.0542 | -0.3300 | -1.3841 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.2500 | 0.2000 |
| expected_top5_accuracy | 0.1750 | 0.5500 | 0.3750 |
| expected_top10_accuracy | 0.4000 | 0.6500 | 0.2500 |
| comparison_top1_accuracy | 0.0500 | 0.2500 | 0.2000 |
| comparison_top5_accuracy | 0.1500 | 0.7500 | 0.6000 |
| comparison_top10_accuracy | 0.2750 | 0.8000 | 0.5250 |
| expected_beats_comparison | 0.6500 | 0.3750 | -0.2750 |
| avg_logprob_margin | 0.9046 | -1.0180 | -1.9226 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0833 | 0.0833 |
| expected_top5_accuracy | 0.0500 | 0.4333 | 0.3833 |
| expected_top10_accuracy | 0.0833 | 0.5333 | 0.4500 |
| comparison_top1_accuracy | 0.0000 | 0.3500 | 0.3500 |
| comparison_top5_accuracy | 0.0000 | 0.8333 | 0.8333 |
| comparison_top10_accuracy | 0.0333 | 0.9000 | 0.8667 |
| expected_beats_comparison | 0.8000 | 0.3000 | -0.5000 |
| avg_logprob_margin | 1.2528 | -1.7808 | -3.0336 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.2812 | 0.1562 |
| expected_top10_accuracy | 0.1562 | 0.3750 | 0.2188 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.5000 | 0.5000 |
| comparison_top10_accuracy | 0.0312 | 0.5000 | 0.4688 |
| expected_beats_comparison | 0.5625 | 0.1875 | -0.3750 |
| avg_logprob_margin | -0.0472 | -0.9219 | -0.8747 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.0625 | 0.0312 |
| expected_top5_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_top10_accuracy | 0.2188 | 0.2188 | 0.0000 |
| comparison_top1_accuracy | 0.0625 | 0.5000 | 0.4375 |
| comparison_top5_accuracy | 0.2500 | 0.9062 | 0.6562 |
| comparison_top10_accuracy | 0.3750 | 0.9062 | 0.5312 |
| expected_beats_comparison | 0.5312 | 0.0625 | -0.4688 |
| avg_logprob_margin | 0.2430 | -4.4010 | -4.6441 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.4062 | 0.3438 |
| expected_top5_accuracy | 0.1875 | 0.7500 | 0.5625 |
| expected_top10_accuracy | 0.3750 | 0.9375 | 0.5625 |
| comparison_top1_accuracy | 0.0312 | 0.5938 | 0.5625 |
| comparison_top5_accuracy | 0.0625 | 0.8750 | 0.8125 |
| comparison_top10_accuracy | 0.1875 | 0.9375 | 0.7500 |
| expected_beats_comparison | 0.5625 | 0.3125 | -0.2500 |
| avg_logprob_margin | 1.5997 | -0.5963 | -2.1959 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.7188 | 0.6250 |
| expected_top10_accuracy | 0.1562 | 0.7812 | 0.6250 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.8125 | 0.8125 |
| comparison_top10_accuracy | 0.0625 | 0.9375 | 0.8750 |
| expected_beats_comparison | 0.8125 | 0.5000 | -0.3125 |
| avg_logprob_margin | 0.9659 | -0.2498 | -1.2157 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.2500 | 0.2500 |
| expected_top5_accuracy | 0.1875 | 0.7188 | 0.5312 |
| expected_top10_accuracy | 0.3750 | 0.7188 | 0.3438 |
| comparison_top1_accuracy | 0.0000 | 0.3750 | 0.3750 |
| comparison_top5_accuracy | 0.0625 | 0.8125 | 0.7500 |
| comparison_top10_accuracy | 0.1250 | 0.9062 | 0.7812 |
| expected_beats_comparison | 0.9062 | 0.5000 | -0.4062 |
| avg_logprob_margin | 2.5561 | 0.1035 | -2.4526 |

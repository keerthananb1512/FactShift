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
| expected_top1_accuracy | 0.0187 | 0.2313 | 0.2125 |
| expected_top5_accuracy | 0.1437 | 0.6062 | 0.4625 |
| expected_top10_accuracy | 0.2562 | 0.6562 | 0.4000 |
| comparison_top1_accuracy | 0.0187 | 0.1500 | 0.1313 |
| comparison_top5_accuracy | 0.0750 | 0.4875 | 0.4125 |
| comparison_top10_accuracy | 0.1562 | 0.6500 | 0.4938 |
| expected_beats_comparison | 0.6750 | 0.5375 | -0.1375 |
| avg_logprob_margin | 1.0635 | 0.4121 | -0.6515 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.2000 | 0.2000 |
| expected_top5_accuracy | 0.2500 | 0.7000 | 0.4500 |
| expected_top10_accuracy | 0.3500 | 0.7000 | 0.3500 |
| comparison_top1_accuracy | 0.0000 | 0.1500 | 0.1500 |
| comparison_top5_accuracy | 0.1000 | 0.6500 | 0.5500 |
| comparison_top10_accuracy | 0.2000 | 0.7500 | 0.5500 |
| expected_beats_comparison | 0.7000 | 0.5000 | -0.2000 |
| avg_logprob_margin | 0.8321 | 0.4133 | -0.4188 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.2250 | 0.2000 |
| expected_top5_accuracy | 0.2000 | 0.6500 | 0.4500 |
| expected_top10_accuracy | 0.3250 | 0.6750 | 0.3500 |
| comparison_top1_accuracy | 0.0250 | 0.1750 | 0.1500 |
| comparison_top5_accuracy | 0.1000 | 0.4000 | 0.3000 |
| comparison_top10_accuracy | 0.2000 | 0.5250 | 0.3250 |
| expected_beats_comparison | 0.5000 | 0.3750 | -0.1250 |
| avg_logprob_margin | 1.0542 | 0.9198 | -0.1343 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.3250 | 0.2750 |
| expected_top5_accuracy | 0.1750 | 0.5750 | 0.4000 |
| expected_top10_accuracy | 0.4000 | 0.7000 | 0.3000 |
| comparison_top1_accuracy | 0.0500 | 0.2000 | 0.1500 |
| comparison_top5_accuracy | 0.1500 | 0.4000 | 0.2500 |
| comparison_top10_accuracy | 0.2750 | 0.6250 | 0.3500 |
| expected_beats_comparison | 0.6500 | 0.5750 | -0.0750 |
| avg_logprob_margin | 0.9046 | 0.5687 | -0.3359 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.1833 | 0.1833 |
| expected_top5_accuracy | 0.0500 | 0.5667 | 0.5167 |
| expected_top10_accuracy | 0.0833 | 0.6000 | 0.5167 |
| comparison_top1_accuracy | 0.0000 | 0.1000 | 0.1000 |
| comparison_top5_accuracy | 0.0000 | 0.5500 | 0.5500 |
| comparison_top10_accuracy | 0.0333 | 0.7167 | 0.6833 |
| expected_beats_comparison | 0.8000 | 0.6333 | -0.1667 |
| avg_logprob_margin | 1.2528 | -0.0313 | -1.2841 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0312 | 0.0312 |
| expected_top5_accuracy | 0.1250 | 0.5000 | 0.3750 |
| expected_top10_accuracy | 0.1562 | 0.5625 | 0.4062 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0938 | 0.0938 |
| comparison_top10_accuracy | 0.0312 | 0.2812 | 0.2500 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | -0.0472 | -0.0557 | -0.0086 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.1250 | 0.0938 |
| expected_top5_accuracy | 0.1250 | 0.2500 | 0.1250 |
| expected_top10_accuracy | 0.2188 | 0.3125 | 0.0938 |
| comparison_top1_accuracy | 0.0625 | 0.2500 | 0.1875 |
| comparison_top5_accuracy | 0.2500 | 0.6875 | 0.4375 |
| comparison_top10_accuracy | 0.3750 | 0.8125 | 0.4375 |
| expected_beats_comparison | 0.5312 | 0.1875 | -0.3438 |
| avg_logprob_margin | 0.2430 | -1.8509 | -2.0939 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.5625 | 0.5000 |
| expected_top5_accuracy | 0.1875 | 0.9062 | 0.7188 |
| expected_top10_accuracy | 0.3750 | 0.9375 | 0.5625 |
| comparison_top1_accuracy | 0.0312 | 0.4062 | 0.3750 |
| comparison_top5_accuracy | 0.0625 | 0.7188 | 0.6562 |
| comparison_top10_accuracy | 0.1875 | 0.8750 | 0.6875 |
| expected_beats_comparison | 0.5625 | 0.5312 | -0.0312 |
| avg_logprob_margin | 1.5997 | 1.3826 | -0.2171 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.6875 | 0.5938 |
| expected_top10_accuracy | 0.1562 | 0.7500 | 0.5938 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.4688 | 0.4688 |
| comparison_top10_accuracy | 0.0625 | 0.6250 | 0.5625 |
| expected_beats_comparison | 0.8125 | 0.6875 | -0.1250 |
| avg_logprob_margin | 0.9659 | 0.7605 | -0.2054 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.4375 | 0.4375 |
| expected_top5_accuracy | 0.1875 | 0.6875 | 0.5000 |
| expected_top10_accuracy | 0.3750 | 0.7188 | 0.3438 |
| comparison_top1_accuracy | 0.0000 | 0.0938 | 0.0938 |
| comparison_top5_accuracy | 0.0625 | 0.4688 | 0.4062 |
| comparison_top10_accuracy | 0.1250 | 0.6562 | 0.5312 |
| expected_beats_comparison | 0.9062 | 0.7188 | -0.1875 |
| avg_logprob_margin | 2.5561 | 1.8238 | -0.7323 |

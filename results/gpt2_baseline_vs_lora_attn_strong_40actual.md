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
| expected_top1_accuracy | 0.0187 | 0.1313 | 0.1125 |
| expected_top5_accuracy | 0.1437 | 0.4375 | 0.2938 |
| expected_top10_accuracy | 0.2562 | 0.5188 | 0.2625 |
| comparison_top1_accuracy | 0.0187 | 0.0813 | 0.0625 |
| comparison_top5_accuracy | 0.0750 | 0.2687 | 0.1937 |
| comparison_top10_accuracy | 0.1562 | 0.3812 | 0.2250 |
| expected_beats_comparison | 0.6750 | 0.6188 | -0.0563 |
| avg_logprob_margin | 1.0635 | 0.9450 | -0.1185 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.1000 | 0.1000 |
| expected_top5_accuracy | 0.2500 | 0.6000 | 0.3500 |
| expected_top10_accuracy | 0.3500 | 0.6500 | 0.3000 |
| comparison_top1_accuracy | 0.0000 | 0.1000 | 0.1000 |
| comparison_top5_accuracy | 0.1000 | 0.3000 | 0.2000 |
| comparison_top10_accuracy | 0.2000 | 0.5000 | 0.3000 |
| expected_beats_comparison | 0.7000 | 0.6000 | -0.1000 |
| avg_logprob_margin | 0.8321 | 0.8947 | 0.0626 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.1500 | 0.1250 |
| expected_top5_accuracy | 0.2000 | 0.5250 | 0.3250 |
| expected_top10_accuracy | 0.3250 | 0.6000 | 0.2750 |
| comparison_top1_accuracy | 0.0250 | 0.0500 | 0.0250 |
| comparison_top5_accuracy | 0.1000 | 0.3500 | 0.2500 |
| comparison_top10_accuracy | 0.2000 | 0.3750 | 0.1750 |
| expected_beats_comparison | 0.5000 | 0.5000 | 0.0000 |
| avg_logprob_margin | 1.0542 | 1.2280 | 0.1738 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.2250 | 0.1750 |
| expected_top5_accuracy | 0.1750 | 0.4500 | 0.2750 |
| expected_top10_accuracy | 0.4000 | 0.5750 | 0.1750 |
| comparison_top1_accuracy | 0.0500 | 0.1500 | 0.1000 |
| comparison_top5_accuracy | 0.1500 | 0.2750 | 0.1250 |
| comparison_top10_accuracy | 0.2750 | 0.4250 | 0.1500 |
| expected_beats_comparison | 0.6500 | 0.6250 | -0.0250 |
| avg_logprob_margin | 0.9046 | 1.0146 | 0.1100 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0667 | 0.0667 |
| expected_top5_accuracy | 0.0500 | 0.3167 | 0.2667 |
| expected_top10_accuracy | 0.0833 | 0.3833 | 0.3000 |
| comparison_top1_accuracy | 0.0000 | 0.0500 | 0.0500 |
| comparison_top5_accuracy | 0.0000 | 0.2000 | 0.2000 |
| comparison_top10_accuracy | 0.0333 | 0.3167 | 0.2833 |
| expected_beats_comparison | 0.8000 | 0.7000 | -0.1000 |
| avg_logprob_margin | 1.2528 | 0.7267 | -0.5261 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.1562 | 0.0312 |
| expected_top10_accuracy | 0.1562 | 0.3125 | 0.1562 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0312 | 0.0312 |
| comparison_top10_accuracy | 0.0312 | 0.0625 | 0.0312 |
| expected_beats_comparison | 0.5625 | 0.5312 | -0.0312 |
| avg_logprob_margin | -0.0472 | -0.0719 | -0.0247 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.0938 | 0.0625 |
| expected_top5_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_top10_accuracy | 0.2188 | 0.2812 | 0.0625 |
| comparison_top1_accuracy | 0.0625 | 0.1250 | 0.0625 |
| comparison_top5_accuracy | 0.2500 | 0.4375 | 0.1875 |
| comparison_top10_accuracy | 0.3750 | 0.5938 | 0.2188 |
| expected_beats_comparison | 0.5312 | 0.3438 | -0.1875 |
| avg_logprob_margin | 0.2430 | -0.7074 | -0.9504 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.5312 | 0.4688 |
| expected_top5_accuracy | 0.1875 | 0.9062 | 0.7188 |
| expected_top10_accuracy | 0.3750 | 0.9375 | 0.5625 |
| comparison_top1_accuracy | 0.0312 | 0.2812 | 0.2500 |
| comparison_top5_accuracy | 0.0625 | 0.4688 | 0.4062 |
| comparison_top10_accuracy | 0.1875 | 0.5625 | 0.3750 |
| expected_beats_comparison | 0.5625 | 0.5938 | 0.0312 |
| avg_logprob_margin | 1.5997 | 2.4092 | 0.8095 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.5000 | 0.4062 |
| expected_top10_accuracy | 0.1562 | 0.5625 | 0.4062 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.2500 | 0.2500 |
| comparison_top10_accuracy | 0.0625 | 0.3750 | 0.3125 |
| expected_beats_comparison | 0.8125 | 0.7188 | -0.0938 |
| avg_logprob_margin | 0.9659 | 0.7248 | -0.2411 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0312 | 0.0312 |
| expected_top5_accuracy | 0.1875 | 0.4375 | 0.2500 |
| expected_top10_accuracy | 0.3750 | 0.5000 | 0.1250 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0625 | 0.1562 | 0.0938 |
| comparison_top10_accuracy | 0.1250 | 0.3125 | 0.1875 |
| expected_beats_comparison | 0.9062 | 0.9062 | 0.0000 |
| avg_logprob_margin | 2.5561 | 2.3703 | -0.1859 |

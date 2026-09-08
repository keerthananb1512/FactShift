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
| expected_top1_accuracy | 0.0187 | 0.1938 | 0.1750 |
| expected_top5_accuracy | 0.1437 | 0.5125 | 0.3687 |
| expected_top10_accuracy | 0.2562 | 0.5750 | 0.3187 |
| comparison_top1_accuracy | 0.0187 | 0.1688 | 0.1500 |
| comparison_top5_accuracy | 0.0750 | 0.4125 | 0.3375 |
| comparison_top10_accuracy | 0.1562 | 0.5437 | 0.3875 |
| expected_beats_comparison | 0.6750 | 0.5375 | -0.1375 |
| avg_logprob_margin | 1.0635 | 0.4014 | -0.6622 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.1500 | 0.1500 |
| expected_top5_accuracy | 0.2500 | 0.5500 | 0.3000 |
| expected_top10_accuracy | 0.3500 | 0.6500 | 0.3000 |
| comparison_top1_accuracy | 0.0000 | 0.2000 | 0.2000 |
| comparison_top5_accuracy | 0.1000 | 0.4500 | 0.3500 |
| comparison_top10_accuracy | 0.2000 | 0.6000 | 0.4000 |
| expected_beats_comparison | 0.7000 | 0.5000 | -0.2000 |
| avg_logprob_margin | 0.8321 | 0.3446 | -0.4875 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.2250 | 0.2000 |
| expected_top5_accuracy | 0.2000 | 0.6000 | 0.4000 |
| expected_top10_accuracy | 0.3250 | 0.6250 | 0.3000 |
| comparison_top1_accuracy | 0.0250 | 0.1500 | 0.1250 |
| comparison_top5_accuracy | 0.1000 | 0.4000 | 0.3000 |
| comparison_top10_accuracy | 0.2000 | 0.5250 | 0.3250 |
| expected_beats_comparison | 0.5000 | 0.4250 | -0.0750 |
| avg_logprob_margin | 1.0542 | 0.8630 | -0.1912 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.2750 | 0.2250 |
| expected_top5_accuracy | 0.1750 | 0.5000 | 0.3250 |
| expected_top10_accuracy | 0.4000 | 0.6000 | 0.2000 |
| comparison_top1_accuracy | 0.0500 | 0.1750 | 0.1250 |
| comparison_top5_accuracy | 0.1500 | 0.4000 | 0.2500 |
| comparison_top10_accuracy | 0.2750 | 0.5500 | 0.2750 |
| expected_beats_comparison | 0.6500 | 0.5750 | -0.0750 |
| avg_logprob_margin | 0.9046 | 0.6802 | -0.2244 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.1333 | 0.1333 |
| expected_top5_accuracy | 0.0500 | 0.4500 | 0.4000 |
| expected_top10_accuracy | 0.0833 | 0.5000 | 0.4167 |
| comparison_top1_accuracy | 0.0000 | 0.1667 | 0.1667 |
| comparison_top5_accuracy | 0.0000 | 0.4167 | 0.4167 |
| comparison_top10_accuracy | 0.0333 | 0.5333 | 0.5000 |
| expected_beats_comparison | 0.8000 | 0.6000 | -0.2000 |
| avg_logprob_margin | 1.2528 | -0.0734 | -1.3262 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_top10_accuracy | 0.1562 | 0.2500 | 0.0938 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0938 | 0.0938 |
| comparison_top10_accuracy | 0.0312 | 0.2500 | 0.2188 |
| expected_beats_comparison | 0.5625 | 0.5938 | 0.0312 |
| avg_logprob_margin | -0.0472 | -0.3244 | -0.2772 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.0625 | 0.0312 |
| expected_top5_accuracy | 0.1250 | 0.2188 | 0.0938 |
| expected_top10_accuracy | 0.2188 | 0.2500 | 0.0312 |
| comparison_top1_accuracy | 0.0625 | 0.2812 | 0.2188 |
| comparison_top5_accuracy | 0.2500 | 0.6562 | 0.4062 |
| comparison_top10_accuracy | 0.3750 | 0.7812 | 0.4062 |
| expected_beats_comparison | 0.5312 | 0.2500 | -0.2812 |
| avg_logprob_margin | 0.2430 | -1.7887 | -2.0317 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.6250 | 0.5625 |
| expected_top5_accuracy | 0.1875 | 0.9375 | 0.7500 |
| expected_top10_accuracy | 0.3750 | 0.9375 | 0.5625 |
| comparison_top1_accuracy | 0.0312 | 0.3438 | 0.3125 |
| comparison_top5_accuracy | 0.0625 | 0.5000 | 0.4375 |
| comparison_top10_accuracy | 0.1875 | 0.5625 | 0.3750 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | 1.5997 | 2.4669 | 0.8673 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.6250 | 0.5312 |
| expected_top10_accuracy | 0.1562 | 0.7188 | 0.5625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.3750 | 0.3750 |
| comparison_top10_accuracy | 0.0625 | 0.5312 | 0.4688 |
| expected_beats_comparison | 0.8125 | 0.7188 | -0.0938 |
| avg_logprob_margin | 0.9659 | 0.5947 | -0.3712 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.2812 | 0.2812 |
| expected_top5_accuracy | 0.1875 | 0.5938 | 0.4062 |
| expected_top10_accuracy | 0.3750 | 0.7188 | 0.3438 |
| comparison_top1_accuracy | 0.0000 | 0.2188 | 0.2188 |
| comparison_top5_accuracy | 0.0625 | 0.4375 | 0.3750 |
| comparison_top10_accuracy | 0.1250 | 0.5938 | 0.4688 |
| expected_beats_comparison | 0.9062 | 0.5625 | -0.3438 |
| avg_logprob_margin | 2.5561 | 1.0582 | -1.4979 |

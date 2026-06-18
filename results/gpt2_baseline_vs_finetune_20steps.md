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
| expected_top5_accuracy | 0.1437 | 0.5500 | 0.4063 |
| expected_top10_accuracy | 0.2562 | 0.6375 | 0.3812 |
| comparison_top1_accuracy | 0.0187 | 0.1812 | 0.1625 |
| comparison_top5_accuracy | 0.0750 | 0.5437 | 0.4687 |
| comparison_top10_accuracy | 0.1562 | 0.6813 | 0.5250 |
| expected_beats_comparison | 0.6750 | 0.4938 | -0.1813 |
| avg_logprob_margin | 1.0635 | 0.1308 | -0.9327 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.2000 | 0.2000 |
| expected_top5_accuracy | 0.2500 | 0.6000 | 0.3500 |
| expected_top10_accuracy | 0.3500 | 0.7000 | 0.3500 |
| comparison_top1_accuracy | 0.0000 | 0.2500 | 0.2500 |
| comparison_top5_accuracy | 0.1000 | 0.5500 | 0.4500 |
| comparison_top10_accuracy | 0.2000 | 0.7500 | 0.5500 |
| expected_beats_comparison | 0.7000 | 0.5500 | -0.1500 |
| avg_logprob_margin | 0.8321 | 0.0593 | -0.7728 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.2250 | 0.2000 |
| expected_top5_accuracy | 0.2000 | 0.6500 | 0.4500 |
| expected_top10_accuracy | 0.3250 | 0.6750 | 0.3500 |
| comparison_top1_accuracy | 0.0250 | 0.1750 | 0.1500 |
| comparison_top5_accuracy | 0.1000 | 0.4250 | 0.3250 |
| comparison_top10_accuracy | 0.2000 | 0.5500 | 0.3500 |
| expected_beats_comparison | 0.5000 | 0.3750 | -0.1250 |
| avg_logprob_margin | 1.0542 | 0.9184 | -0.1357 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.3000 | 0.2500 |
| expected_top5_accuracy | 0.1750 | 0.6000 | 0.4250 |
| expected_top10_accuracy | 0.4000 | 0.6500 | 0.2500 |
| comparison_top1_accuracy | 0.0500 | 0.1500 | 0.1000 |
| comparison_top5_accuracy | 0.1500 | 0.5000 | 0.3500 |
| comparison_top10_accuracy | 0.2750 | 0.6500 | 0.3750 |
| expected_beats_comparison | 0.6500 | 0.4750 | -0.1750 |
| avg_logprob_margin | 0.9046 | 0.3588 | -0.5458 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.2000 | 0.2000 |
| expected_top5_accuracy | 0.0500 | 0.4333 | 0.3833 |
| expected_top10_accuracy | 0.0833 | 0.5833 | 0.5000 |
| comparison_top1_accuracy | 0.0000 | 0.1833 | 0.1833 |
| comparison_top5_accuracy | 0.0000 | 0.6500 | 0.6500 |
| comparison_top10_accuracy | 0.0333 | 0.7667 | 0.7333 |
| expected_beats_comparison | 0.8000 | 0.5667 | -0.2333 |
| avg_logprob_margin | 1.2528 | -0.5223 | -1.7752 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0312 | 0.0312 |
| expected_top5_accuracy | 0.1250 | 0.4375 | 0.3125 |
| expected_top10_accuracy | 0.1562 | 0.5625 | 0.4062 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.3125 | 0.3125 |
| comparison_top10_accuracy | 0.0312 | 0.4688 | 0.4375 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | -0.0472 | -0.2152 | -0.1681 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.0625 | 0.0312 |
| expected_top5_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_top10_accuracy | 0.2188 | 0.2500 | 0.0312 |
| comparison_top1_accuracy | 0.0625 | 0.3438 | 0.2812 |
| comparison_top5_accuracy | 0.2500 | 0.7500 | 0.5000 |
| comparison_top10_accuracy | 0.3750 | 0.8750 | 0.5000 |
| expected_beats_comparison | 0.5312 | 0.0938 | -0.4375 |
| avg_logprob_margin | 0.2430 | -2.8179 | -3.0609 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.6250 | 0.5625 |
| expected_top5_accuracy | 0.1875 | 0.8438 | 0.6562 |
| expected_top10_accuracy | 0.3750 | 0.9375 | 0.5625 |
| comparison_top1_accuracy | 0.0312 | 0.3438 | 0.3125 |
| comparison_top5_accuracy | 0.0625 | 0.6562 | 0.5938 |
| comparison_top10_accuracy | 0.1875 | 0.7812 | 0.5938 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | 1.5997 | 1.7461 | 0.1465 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.6250 | 0.5312 |
| expected_top10_accuracy | 0.1562 | 0.7188 | 0.5625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.4688 | 0.4688 |
| comparison_top10_accuracy | 0.0625 | 0.6875 | 0.6250 |
| expected_beats_comparison | 0.8125 | 0.5312 | -0.2812 |
| avg_logprob_margin | 0.9659 | 0.2079 | -0.7580 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.4375 | 0.4375 |
| expected_top5_accuracy | 0.1875 | 0.6562 | 0.4688 |
| expected_top10_accuracy | 0.3750 | 0.7188 | 0.3438 |
| comparison_top1_accuracy | 0.0000 | 0.2188 | 0.2188 |
| comparison_top5_accuracy | 0.0625 | 0.5312 | 0.4688 |
| comparison_top10_accuracy | 0.1250 | 0.5938 | 0.4688 |
| expected_beats_comparison | 0.9062 | 0.7188 | -0.1875 |
| avg_logprob_margin | 2.5561 | 1.7333 | -0.8228 |

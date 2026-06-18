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
| expected_top1_accuracy | 0.0187 | 0.0375 | 0.0187 |
| expected_top5_accuracy | 0.1437 | 0.2062 | 0.0625 |
| expected_top10_accuracy | 0.2562 | 0.3125 | 0.0563 |
| comparison_top1_accuracy | 0.0187 | 0.0250 | 0.0063 |
| comparison_top5_accuracy | 0.0750 | 0.1062 | 0.0312 |
| comparison_top10_accuracy | 0.1562 | 0.1812 | 0.0250 |
| expected_beats_comparison | 0.6750 | 0.6750 | 0.0000 |
| avg_logprob_margin | 1.0635 | 1.0443 | -0.0192 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0500 | 0.0500 |
| expected_top5_accuracy | 0.2500 | 0.3000 | 0.0500 |
| expected_top10_accuracy | 0.3500 | 0.4500 | 0.1000 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.1000 | 0.1500 | 0.0500 |
| comparison_top10_accuracy | 0.2000 | 0.2500 | 0.0500 |
| expected_beats_comparison | 0.7000 | 0.7000 | 0.0000 |
| avg_logprob_margin | 0.8321 | 0.8314 | -0.0007 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.0500 | 0.0250 |
| expected_top5_accuracy | 0.2000 | 0.2750 | 0.0750 |
| expected_top10_accuracy | 0.3250 | 0.4500 | 0.1250 |
| comparison_top1_accuracy | 0.0250 | 0.0250 | 0.0000 |
| comparison_top5_accuracy | 0.1000 | 0.1500 | 0.0500 |
| comparison_top10_accuracy | 0.2000 | 0.2500 | 0.0500 |
| expected_beats_comparison | 0.5000 | 0.5000 | 0.0000 |
| avg_logprob_margin | 1.0542 | 1.0673 | 0.0131 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.0750 | 0.0250 |
| expected_top5_accuracy | 0.1750 | 0.3000 | 0.1250 |
| expected_top10_accuracy | 0.4000 | 0.4500 | 0.0500 |
| comparison_top1_accuracy | 0.0500 | 0.0750 | 0.0250 |
| comparison_top5_accuracy | 0.1500 | 0.2000 | 0.0500 |
| comparison_top10_accuracy | 0.2750 | 0.2750 | 0.0000 |
| expected_beats_comparison | 0.6500 | 0.6500 | 0.0000 |
| avg_logprob_margin | 0.9046 | 0.9224 | 0.0178 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0500 | 0.0667 | 0.0167 |
| expected_top10_accuracy | 0.0833 | 0.0833 | 0.0000 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0333 | 0.0500 | 0.0167 |
| expected_beats_comparison | 0.8000 | 0.8000 | 0.0000 |
| avg_logprob_margin | 1.2528 | 1.1813 | -0.0715 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.1250 | 0.0000 |
| expected_top10_accuracy | 0.1562 | 0.1250 | -0.0312 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0312 | 0.0312 | 0.0000 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | -0.0472 | -0.0596 | -0.0124 |

## Relation: born_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0312 | 0.0312 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.1250 | 0.0000 |
| expected_top10_accuracy | 0.2188 | 0.2188 | 0.0000 |
| comparison_top1_accuracy | 0.0625 | 0.0625 | 0.0000 |
| comparison_top5_accuracy | 0.2500 | 0.2500 | 0.0000 |
| comparison_top10_accuracy | 0.3750 | 0.3750 | 0.0000 |
| expected_beats_comparison | 0.5312 | 0.5312 | 0.0000 |
| avg_logprob_margin | 0.2430 | 0.1359 | -0.1071 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.1562 | 0.0938 |
| expected_top5_accuracy | 0.1875 | 0.3750 | 0.1875 |
| expected_top10_accuracy | 0.3750 | 0.5625 | 0.1875 |
| comparison_top1_accuracy | 0.0312 | 0.0625 | 0.0312 |
| comparison_top5_accuracy | 0.0625 | 0.1875 | 0.1250 |
| comparison_top10_accuracy | 0.1875 | 0.2188 | 0.0312 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | 1.5997 | 1.6975 | 0.0979 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.1250 | 0.0312 |
| expected_top10_accuracy | 0.1562 | 0.2188 | 0.0625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0625 | 0.0938 | 0.0312 |
| expected_beats_comparison | 0.8125 | 0.8125 | 0.0000 |
| avg_logprob_margin | 0.9659 | 0.9195 | -0.0465 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1875 | 0.2812 | 0.0938 |
| expected_top10_accuracy | 0.3750 | 0.4375 | 0.0625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0625 | 0.0938 | 0.0312 |
| comparison_top10_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_beats_comparison | 0.9062 | 0.9062 | 0.0000 |
| avg_logprob_margin | 2.5561 | 2.5283 | -0.0278 |

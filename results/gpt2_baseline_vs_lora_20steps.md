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
| expected_top1_accuracy | 0.0187 | 0.0187 | 0.0000 |
| expected_top5_accuracy | 0.1437 | 0.1688 | 0.0250 |
| expected_top10_accuracy | 0.2562 | 0.3000 | 0.0438 |
| comparison_top1_accuracy | 0.0187 | 0.0187 | 0.0000 |
| comparison_top5_accuracy | 0.0750 | 0.0938 | 0.0188 |
| comparison_top10_accuracy | 0.1562 | 0.1812 | 0.0250 |
| expected_beats_comparison | 0.6750 | 0.6750 | 0.0000 |
| avg_logprob_margin | 1.0635 | 1.0537 | -0.0098 |

## Prompt Type: direct

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.2500 | 0.3000 | 0.0500 |
| expected_top10_accuracy | 0.3500 | 0.4500 | 0.1000 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.1000 | 0.1000 | 0.0000 |
| comparison_top10_accuracy | 0.2000 | 0.2500 | 0.0500 |
| expected_beats_comparison | 0.7000 | 0.7000 | 0.0000 |
| avg_logprob_margin | 0.8321 | 0.8302 | -0.0018 |

## Prompt Type: locality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0250 | 0.0250 | 0.0000 |
| expected_top5_accuracy | 0.2000 | 0.2500 | 0.0500 |
| expected_top10_accuracy | 0.3250 | 0.4000 | 0.0750 |
| comparison_top1_accuracy | 0.0250 | 0.0250 | 0.0000 |
| comparison_top5_accuracy | 0.1000 | 0.1500 | 0.0500 |
| comparison_top10_accuracy | 0.2000 | 0.2500 | 0.0500 |
| expected_beats_comparison | 0.5000 | 0.5000 | 0.0000 |
| avg_logprob_margin | 1.0542 | 1.0581 | 0.0040 |

## Prompt Type: neighbor

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0500 | 0.0500 | 0.0000 |
| expected_top5_accuracy | 0.1750 | 0.2000 | 0.0250 |
| expected_top10_accuracy | 0.4000 | 0.4500 | 0.0500 |
| comparison_top1_accuracy | 0.0500 | 0.0500 | 0.0000 |
| comparison_top5_accuracy | 0.1500 | 0.1750 | 0.0250 |
| comparison_top10_accuracy | 0.2750 | 0.2750 | 0.0000 |
| expected_beats_comparison | 0.6500 | 0.6500 | 0.0000 |
| avg_logprob_margin | 0.9046 | 0.9103 | 0.0057 |

## Prompt Type: paraphrase

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0500 | 0.0500 | 0.0000 |
| expected_top10_accuracy | 0.0833 | 0.0833 | 0.0000 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0333 | 0.0500 | 0.0167 |
| expected_beats_comparison | 0.8000 | 0.8000 | 0.0000 |
| avg_logprob_margin | 1.2528 | 1.2209 | -0.0320 |

## Relation: author_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1250 | 0.1250 | 0.0000 |
| expected_top10_accuracy | 0.1562 | 0.1562 | 0.0000 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0312 | 0.0312 | 0.0000 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | -0.0472 | -0.0546 | -0.0074 |

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
| avg_logprob_margin | 0.2430 | 0.1889 | -0.0542 |

## Relation: capital_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0625 | 0.0625 | 0.0000 |
| expected_top5_accuracy | 0.1875 | 0.2500 | 0.0625 |
| expected_top10_accuracy | 0.3750 | 0.4688 | 0.0938 |
| comparison_top1_accuracy | 0.0312 | 0.0312 | 0.0000 |
| comparison_top5_accuracy | 0.0625 | 0.1250 | 0.0625 |
| comparison_top10_accuracy | 0.1875 | 0.2188 | 0.0312 |
| expected_beats_comparison | 0.5625 | 0.5625 | 0.0000 |
| avg_logprob_margin | 1.5997 | 1.6340 | 0.0343 |

## Relation: ceo_of

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.0938 | 0.0938 | 0.0000 |
| expected_top10_accuracy | 0.1562 | 0.2188 | 0.0625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top10_accuracy | 0.0625 | 0.0938 | 0.0312 |
| expected_beats_comparison | 0.8125 | 0.8125 | 0.0000 |
| avg_logprob_margin | 0.9659 | 0.9553 | -0.0106 |

## Relation: located_in

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| expected_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| expected_top5_accuracy | 0.1875 | 0.2500 | 0.0625 |
| expected_top10_accuracy | 0.3750 | 0.4375 | 0.0625 |
| comparison_top1_accuracy | 0.0000 | 0.0000 | 0.0000 |
| comparison_top5_accuracy | 0.0625 | 0.0938 | 0.0312 |
| comparison_top10_accuracy | 0.1250 | 0.1875 | 0.0625 |
| expected_beats_comparison | 0.9062 | 0.9062 | 0.0000 |
| avg_logprob_margin | 2.5561 | 2.5451 | -0.0110 |

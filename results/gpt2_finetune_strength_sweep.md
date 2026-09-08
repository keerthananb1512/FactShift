# GPT-2 Targeted Fine-Tuning Strength Sweep

This report compares baseline GPT-2 with targeted fine-tuning checkpoints.

`comparison_top10` tracks how often edited answers appear in the top 10.
`expected_beats_comparison` and `avg_logprob_margin` track how strongly expected answers still beat edited answers.

## Prompt Type: direct

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2000 | 0.7000 | 0.8321 |
| 10_steps | 0.6000 | 0.5000 | 0.3446 |
| 20_steps | 0.7500 | 0.5500 | 0.0593 |
| 40_steps | 0.9000 | 0.3500 | -1.6664 |

## Prompt Type: paraphrase

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.0333 | 0.8000 | 1.2528 |
| 10_steps | 0.5333 | 0.6000 | -0.0734 |
| 20_steps | 0.7667 | 0.5667 | -0.5223 |
| 40_steps | 0.9000 | 0.3000 | -1.7808 |

## Prompt Type: locality

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2000 | 0.5000 | 1.0542 |
| 10_steps | 0.5250 | 0.4250 | 0.8630 |
| 20_steps | 0.5500 | 0.3750 | 0.9184 |
| 40_steps | 0.7500 | 0.2500 | -0.3300 |

## Prompt Type: neighbor

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2750 | 0.6500 | 0.9046 |
| 10_steps | 0.5500 | 0.5750 | 0.6802 |
| 20_steps | 0.6500 | 0.4750 | 0.3588 |
| 40_steps | 0.8000 | 0.3750 | -1.0180 |

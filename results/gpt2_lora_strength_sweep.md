# GPT-2 LoRA Strength Sweep

This report compares baseline GPT-2 with targeted fine-tuning checkpoints.

`comparison_top10` tracks how often edited answers appear in the top 10.
`expected_beats_comparison` and `avg_logprob_margin` track how strongly expected answers still beat edited answers.

## Prompt Type: direct

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2000 | 0.7000 | 0.8321 |
| 10_steps | 0.2000 | 0.7000 | 0.8277 |
| 20_steps | 0.2500 | 0.7000 | 0.8302 |
| 40_steps | 0.2500 | 0.7000 | 0.8314 |

## Prompt Type: paraphrase

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.0333 | 0.8000 | 1.2528 |
| 10_steps | 0.0333 | 0.8000 | 1.2398 |
| 20_steps | 0.0500 | 0.8000 | 1.2209 |
| 40_steps | 0.0500 | 0.8000 | 1.1813 |

## Prompt Type: locality

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2000 | 0.5000 | 1.0542 |
| 10_steps | 0.2000 | 0.5000 | 1.0521 |
| 20_steps | 0.2500 | 0.5000 | 1.0581 |
| 40_steps | 0.2500 | 0.5000 | 1.0673 |

## Prompt Type: neighbor

| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |
|---|---:|---:|---:|
| baseline | 0.2750 | 0.6500 | 0.9046 |
| 10_steps | 0.2750 | 0.6500 | 0.9040 |
| 20_steps | 0.2750 | 0.6500 | 0.9103 |
| 40_steps | 0.2750 | 0.6500 | 0.9224 |

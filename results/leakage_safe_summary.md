# FactShift leakage-safe results

All edits were trained on direct prompts only. Validation and held-out paraphrases were not training examples.

| Model | Efficacy | Validation paraphrase | Held-out paraphrase | Neighborhood specificity | Harmonic score |
|---|---:|---:|---:|---:|---:|
| GPT-2 baseline | 0.3000 | 0.3000 | 0.1500 | 0.6500 | 0.2600 |
| Full fine-tuning (40 steps) | 0.8000 | 0.7500 | 0.6000 | 0.2750 | 0.4578 |
| LoRA (rank 16, 80 steps) | 0.4500 | 0.5000 | 0.3000 | 0.5500 | 0.4068 |

Efficacy and paraphrase success measure how often the edit target has higher full-answer mean token log probability than the original answer. Neighborhood specificity measures how often the correct neighboring fact resists the edit target.

These are exploratory single-seed results on 20 edits, not population estimates.

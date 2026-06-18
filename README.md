# FactShift

**FactShift** is a small research-style benchmark for testing factual editing in GPT-2. The project asks a practical question:

> Can we make a pretrained language model prefer a new factual answer without damaging nearby or unrelated facts?

Instead of only checking whether an edited answer appears, this project compares edit strength against generalization and locality. That makes it useful project because it shows the tradeoff between "the edit worked" and "the model stayed controlled."

## What This Project Tests

The benchmark contains 20 controlled factual edits across five relation types:

| Relation | Cases |
|---|---:|
| `capital_of` | 4 |
| `born_in` | 4 |
| `located_in` | 4 |
| `author_of` | 4 |
| `ceo_of` | 4 |

Each case stores:

| Field | Meaning |
|---|---|
| `subject` | Entity being edited |
| `true_object` | Original expected answer |
| `new_object` | Desired edited answer |
| `direct_prompt` | Main edit prompt |
| `paraphrase_prompts` | Prompts that test generalization |
| `locality_prompts` | Unrelated facts that should stay stable |
| `neighbor_prompts` | Nearby entities that should not be overwritten |

Dataset: `data/edits.seed.json`

## Methods Compared

| Method | What Changes | Purpose |
|---|---|---|
| GPT-2 baseline | Nothing | Measure the original model behavior |
| Full targeted fine-tuning | All GPT-2 parameters | Strong edit baseline |
| LoRA, weak | Small attention adapters | Conservative parameter-efficient edit |
| LoRA, strong attention-only | Larger `c_attn` adapters | Stronger edit with fewer trainable parameters |

## Metrics

| Metric | Meaning |
|---|---|
| `comparison_top10_accuracy` | How often the edited answer appears in GPT-2's top 10 candidates |
| `expected_beats_comparison` | How often the expected answer scores higher than the edit target |
| `avg_logprob_margin` | Average strength of expected answer over edit target |
| Direct prompt metrics | Whether the exact edited prompt moved toward the new answer |
| Paraphrase metrics | Whether the edit generalizes to alternate wording |
| Locality metrics | Whether unrelated facts remain stable |
| Neighbor metrics | Whether nearby entities avoid edit leakage |

For `avg_logprob_margin`:

```text
margin = mean_logprob(expected_answer) - mean_logprob(edit_target)
```

A positive margin means the model still prefers the expected answer. A negative margin means the edit target is overpowering it.

## Key Results

| Model | Direct Edit Top-10 | Paraphrase Top-10 | Locality Margin | Neighbor Margin | Main Reading |
|---|---:|---:|---:|---:|---|
| GPT-2 baseline | 0.2000 | 0.0333 | 1.0542 | 0.9046 | Original model mostly prefers expected facts |
| Full fine-tune, 40 steps | 0.9000 | 0.9000 | -0.3300 | -1.0180 | Very strong edits, but clear overgeneralization |
| LoRA, 40 steps | 0.2500 | 0.0500 | 1.0673 | 0.9224 | Stable but too weak |
| Strong attention LoRA, 80 steps | 0.7500 | 0.7167 | 0.9198 | 0.5687 | Good edit strength with better locality than full fine-tuning |

## Main Conclusions

Full targeted fine-tuning can force the model toward edited facts quickly, but it also pushes the edit target into unrelated and nearby prompts. That is useful evidence: naive fine-tuning edits facts, but it is not very local.

Weak LoRA is stable but under-edits. It barely changes the model, so it preserves locality but does not solve the editing task.

Strong attention-only LoRA gives the best current tradeoff in this project. It improves direct and paraphrase edit success while keeping locality margins positive. It does not prove perfect factual editing, but it gives a strong baseline before moving to ROME or MEMIT.

## Project Structure

```text
data/
  edits.seed.json              # factual editing benchmark
  finetune_edits.jsonl         # generated training data for edit baselines

src/
  load_gpt2.py                 # GPT-2 loading and answer scoring helpers
  evaluate.py                  # benchmark evaluation pipeline
  build_finetune_data.py       # creates fine-tuning JSONL data
  finetune_gpt2.py             # full targeted fine-tuning baseline
  lora_finetune_gpt2.py        # LoRA targeted fine-tuning baseline
  compare_results.py           # compares two summary result files
  summarize_sweep.py           # builds sweep reports
  analyze_failures.py          # failure analysis for overgeneralization

results/
  *_summary.json               # aggregated metrics
  *_raw.json                   # prompt-level outputs
  *.md                         # comparison and analysis reports
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If GPT-2 is already cached locally, run offline:

```bash
TRANSFORMERS_OFFLINE=1 .venv/bin/python src/evaluate.py \
  --model openai-community/gpt2 \
  --output-prefix gpt2_baseline
```

## Reproduce Main Experiments

Build the edit training data:

```bash
.venv/bin/python src/build_finetune_data.py
```

Run full targeted fine-tuning:

```bash
TRANSFORMERS_OFFLINE=1 .venv/bin/python src/finetune_gpt2.py \
  --max-steps 40 \
  --output-dir models/gpt2_targeted_finetune_40steps
```

Evaluate full fine-tuning:

```bash
TRANSFORMERS_OFFLINE=1 .venv/bin/python src/evaluate.py \
  --model models/gpt2_targeted_finetune_40steps \
  --output-prefix gpt2_targeted_finetune_40steps
```

Run strong attention-only LoRA:

```bash
TRANSFORMERS_OFFLINE=1 .venv/bin/python src/lora_finetune_gpt2.py \
  --target-modules c_attn \
  --rank 16 \
  --alpha 32 \
  --learning-rate 3e-4 \
  --max-steps 80 \
  --output-dir models/gpt2_lora_attn_strong_80steps_true
```

Evaluate strong LoRA:

```bash
TRANSFORMERS_OFFLINE=1 .venv/bin/python src/evaluate.py \
  --model models/gpt2_lora_attn_strong_80steps_true \
  --output-prefix gpt2_lora_attn_strong_80steps
```

Compare two runs:

```bash
.venv/bin/python src/compare_results.py \
  --before results/gpt2_baseline_summary.json \
  --after results/gpt2_lora_attn_strong_80steps_summary.json \
  --output results/gpt2_baseline_vs_lora_attn_strong_80steps.md
```

## Final Report

The full research narrative is in `REPORT.md`. It explains the questions asked during the project, the experiments performed, the conclusions.

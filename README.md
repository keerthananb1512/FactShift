# FactShift

FactShift is a small, evaluation-first benchmark for factual editing in GPT-2. It asks:

> Can a model prefer a requested factual answer, generalize that edit to unseen wording, and preserve nearby and unrelated knowledge?

The repository compares full targeted fine-tuning with LoRA. ROME and MEMIT are planned comparison methods; they are not implemented here.

## Leakage-safe benchmark

The source dataset contains 20 counterfactual edits across five relations: `capital_of`, `born_in`, `located_in`, `author_of`, and `ceo_of`.

Run `src/prepare_benchmark.py` to create the experimental split:

| Split | Count | Usage |
|---|---:|---|
| Direct prompts | 20 | Edit training and direct efficacy |
| Validation paraphrases | 20 | Model/hyperparameter selection only |
| Held-out paraphrases | 40 | Final generalization evaluation |
| Locality prompts | 31 | Unrelated-fact preservation |
| Neighbor prompts | 40 | Related-entity specificity |

The preparation step removes nine locality prompts that are direct edit prompts for other cases. Their identities and exclusion reasons are recorded in `data/split_manifest.json`.

Direct prompts are intentionally reused to measure whether the requested edit succeeded. Validation and held-out paraphrases are never written to the fine-tuning dataset.

## Methods

| Method | Parameters changed | Purpose |
|---|---|---|
| GPT-2 baseline | None | Measure pre-edit behavior |
| Full fine-tuning | All GPT-2 parameters | Strong but potentially non-local baseline |
| LoRA | Low-rank matrices on selected projections | Parameter-efficient baseline |

The LoRA experiment targets GPT-2's combined attention projection, `c_attn`. This is an empirical baseline, not a claim that attention is the unique storage location for facts.

## Evaluation

For prompt `p` and answer tokens `y_1 ... y_m`, FactShift calculates mean answer log probability under teacher forcing:

```text
mean_logprob(y | p) = (1/m) * sum(log P(y_t | p, y_<t))
margin = mean_logprob(expected) - mean_logprob(edit_target)
```

The primary benchmark scores are:

| Score | Desired direction | Meaning |
|---|---:|---|
| Efficacy success | Higher | Edit target beats original answer on direct prompts |
| Validation paraphrase success | Higher | Edit target wins on validation wording |
| Held-out paraphrase success | Higher | Edit target wins on unseen wording |
| Neighborhood specificity | Higher | Correct neighbor answer resists the edit target |
| Harmonic editing score | Higher | Balance of efficacy, held-out generalization, and specificity |

First-token top-1/top-5/top-10 accuracy and ranks are retained as supporting diagnostics. They are explicitly named `*_first_token_*`; they do not score a complete multi-token answer. Full-sequence mean log probability is the main comparison metric.

## Reproduce the benchmark

Create an environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prepare and validate the split, then build direct-only training data:

```bash
python src/prepare_benchmark.py
python src/build_finetune_data.py
python -m unittest discover -s tests -v
```

Evaluate the unchanged model:

```bash
python src/evaluate.py \
  --data-path data/edits.split.json \
  --model openai-community/gpt2 \
  --output-prefix leakage_safe_gpt2_baseline
```

Run full fine-tuning and evaluate it:

```bash
python src/finetune_gpt2.py \
  --data-path data/finetune_edits.jsonl \
  --max-steps 40 \
  --seed 42 \
  --output-dir models/leakage_safe_gpt2_finetune_40steps

python src/evaluate.py \
  --model models/leakage_safe_gpt2_finetune_40steps \
  --output-prefix leakage_safe_gpt2_finetune_40steps
```

Run the selected LoRA configuration and evaluate it:

```bash
python src/lora_finetune_gpt2.py \
  --data-path data/finetune_edits.jsonl \
  --target-modules c_attn \
  --rank 16 \
  --alpha 32 \
  --learning-rate 3e-4 \
  --max-steps 80 \
  --seed 42 \
  --output-dir models/leakage_safe_gpt2_lora_80steps

python src/evaluate.py \
  --model models/leakage_safe_gpt2_lora_80steps \
  --output-prefix leakage_safe_gpt2_lora_80steps
```

Both `--rank`/`--alpha` and `--lora-rank`/`--lora-alpha` are accepted.

This is the repository's only LoRA configuration: rank 16, alpha 32, `c_attn`, learning rate `3e-4`, and 80 steps. Earlier LoRA sweep artifacts were removed to keep the comparison unambiguous.

## Reproducibility

Training scripts accept `--seed`, seed the data-loader generator, and save method parameters and training arguments in `factshift_training_config.json` beside each model.

For a defensible comparison, select steps and learning rates using validation paraphrases, run the selected configuration with multiple seeds, and report mean and confidence intervals on the held-out split.

## Results status

Files in `results/` whose names do not begin with `leakage_safe_` were produced by the original in-sample experiment. They are retained for provenance but must not be described as held-out generalization results.

Only outputs created from `data/edits.split.json` should be used for new claims. See `REPORT.md` for the corrected interpretation and remaining limitations.

## Project structure

```text
data/
  edits.seed.json             # Original authored cases
  edits.split.json            # Generated leakage-safe split
  split_manifest.json         # Split counts and excluded conflicts
  finetune_edits.jsonl        # Generated direct-only training examples
src/
  prepare_benchmark.py        # Creates and validates the split
  build_finetune_data.py      # Builds direct-only training data
  evaluate.py                 # Prompt scoring and benchmark summaries
  finetune_gpt2.py            # Full fine-tuning baseline
  lora_finetune_gpt2.py       # LoRA baseline
tests/
  test_benchmark.py           # Leakage and count regression tests
results/                      # Raw and summarized experiment outputs
```

Generate the compact leakage-safe comparison table with:

```bash
python src/summarize_results.py
```

## Remaining limitations

- The benchmark has only 20 handcrafted edits.
- Results from one seed are exploratory rather than statistically conclusive.
- GPT-2 does not reliably know every source fact.
- CEO facts require timestamps and versioned ground truth.
- Locality is pairwise; distributional KL drift and general-corpus perplexity are not yet measured.
- ROME, MEMIT, larger datasets, and edit-scaling experiments remain future work.

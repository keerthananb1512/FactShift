# FactShift: Leakage-Safe Evaluation Report

## 1. Research question

FactShift studies the trade-off between factual edit strength and model preservation. A successful editor should satisfy three requirements:

1. **Efficacy:** prefer the requested answer on the direct edit prompt.
2. **Generalization:** express the edit under unseen paraphrases.
3. **Specificity:** avoid propagating the edit to unrelated or neighboring facts.

## 2. Corrected experimental design

The original prototype used direct and paraphrase prompts during training and then evaluated those same paraphrases. Those scores measured in-sample prompt fitting, not unseen generalization.

The corrected pipeline keeps the authored source data immutable and generates a separate split:

| Group | Count | Role |
|---|---:|---|
| Direct | 20 | Training and direct efficacy |
| Validation paraphrase | 20 | Model selection |
| Held-out paraphrase | 40 | Final generalization |
| Locality | 31 | Unrelated-fact preservation |
| Neighbor | 40 | Related-entity specificity |

Nine locality prompts were removed because they were direct editing targets elsewhere in the same batch. Counting those prompts as facts that should remain unchanged would contradict the training objective. Exact exclusions are recorded in `data/split_manifest.json`.

## 3. Methods

### GPT-2 baseline

The unchanged model establishes pre-edit preferences and prompt difficulty.

### Full targeted fine-tuning

All model parameters are optimized with causal language-modeling loss. Prompt-token labels are masked, so loss is applied only to the requested answer tokens.

### LoRA

The pretrained base-model weights remain frozen while low-rank matrices are trained on selected projections:

```text
y = W x + (alpha / rank) B A x
```

The current experiment targets `c_attn`. The merged model is saved for evaluation, together with a training configuration file.

## 4. Metrics

For each expected answer and edit target, the evaluator computes the complete answer's mean token log probability:

```text
mean_logprob(answer) = mean_t log P(answer_t | prompt, previous_answer_tokens)
margin = mean_logprob(expected) - mean_logprob(edit_target)
```

The benchmark reports:

- **Efficacy Success (ES):** fraction of direct prompts where the edit target beats the original answer.
- **Validation Paraphrase Success:** the same preference test on validation wording.
- **Held-out Paraphrase Success (PS):** the same preference test on unseen wording.
- **Neighborhood Specificity (NS):** fraction of neighbor prompts where the correct answer beats the current case's edit target.
- **Harmonic Editing Score:** harmonic mean of ES, PS, and NS.

First-token top-k metrics are secondary diagnostics and are labeled accordingly. They are not complete-answer accuracy.

## 5. Result interpretation

Legacy result files demonstrate why the experiment was redesigned, but they must not be presented as held-out generalization. New claims should use only result prefixes beginning with `leakage_safe_`.

### Leakage-safe exploratory results (seed 42)

| Model | Efficacy | Validation paraphrase | Held-out paraphrase | Neighborhood specificity | Harmonic score |
|---|---:|---:|---:|---:|---:|
| GPT-2 baseline | 0.3000 | 0.3000 | 0.1500 | 0.6500 | 0.2600 |
| Full fine-tuning, 40 steps | 0.8000 | 0.7500 | 0.6000 | 0.2750 | 0.4578 |
| LoRA, rank 16 and 80 steps | 0.4500 | 0.5000 | 0.3000 | 0.5500 | 0.4068 |

Full fine-tuning produced the strongest edits and held-out paraphrase performance, but neighborhood specificity fell sharply. The selected LoRA configuration preserved more neighboring knowledge but made weaker edits. Therefore, the corrected experiment shows an edit-strength/specificity trade-off; it does not justify claiming that LoRA wins every metric.

When interpreting a new run:

- High efficacy with low paraphrase success indicates prompt memorization.
- High efficacy and paraphrase success with low specificity indicates overgeneralization.
- High specificity with low efficacy indicates under-editing.
- A useful editor must balance all three, which is why the harmonic score is reported.

## 6. Remaining threats to validity

The corrected split removes the largest leakage and conflict problems, but it does not make the study publication-scale. The dataset remains small and handcrafted; one run does not quantify seed variance; GPT-2 has weak baseline knowledge for several facts; temporal relations are not timestamped; and pairwise locality does not measure complete distribution drift.

The next evaluation upgrades should add multiple seeds, confidence intervals, CounterFact examples, pre/post KL divergence, general-corpus perplexity, generation quality, and equal-compute method comparisons.

## 7. ROME and MEMIT extension

ROME and MEMIT are future comparisons, not current implementations.

- **ROME** performs a rank-one update to a selected middle-layer MLP projection for a single factual association.
- **MEMIT** calculates batched updates and distributes them across multiple mediating MLP layers to support many edits.

The leakage-safe FactShift schema can evaluate either method without reusing training prompts as generalization evidence. ROME should first be tested one edit at a time. MEMIT should then be evaluated at increasing batch sizes while monitoring efficacy, held-out paraphrase success, specificity, runtime, and retention of earlier edits.

## 8. Defensible conclusion

FactShift is an evaluation-focused prototype for studying factual editing trade-offs. Its strongest contribution is not a novel editing algorithm; it is a transparent pipeline that distinguishes direct efficacy, held-out generalization, and preservation, and records where naive editing methods fail.

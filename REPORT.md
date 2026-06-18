# FactShift Final Report

## 1. Project Motivation
The goal was not only to make the model say the new answer. The deeper goal was to measure whether the edit is local, stable, and generalizes to paraphrased prompts.
 we built a controlled benchmark and tested practical baselines: full targeted fine-tuning and LoRA.

## 2. Questions 

| Question | Why It Matters | Conclusion |
|---|---|---|
| Can GPT-2 be evaluated on factual edits before editing? | We need a baseline before claiming improvement. | Yes. The benchmark scores direct, paraphrase, locality, and neighbor prompts. |
| Is full targeted fine-tuning enough for factual editing? | It is the simplest baseline. | It edits strongly, but overgeneralizes. |
| Why does expected answer accuracy also increase after fine-tuning? | The model may learn the prompt style, not only the edit target. | Fine-tuning can increase confidence for many answer-like completions, including original answers. |
| Does fine-tuning damage unrelated facts? | A real editor must be local. | Yes. At higher steps, edited answers invade locality and neighbor prompts. |
| Can LoRA give a better tradeoff? | LoRA changes fewer parameters than full fine-tuning. | Weak LoRA under-edits; stronger attention-only LoRA is much better. |
| Do we need ROME/MEMIT immediately? | The original idea was direct memory editing. | Not immediately. The current benchmark and baselines already form a strong project. ROME/MEMIT are future work. |

## 3. Benchmark Design

The benchmark contains 20 edit cases across five relation types:

| Relation | Number of Cases |
|---|---:|
| `capital_of` | 4 |
| `born_in` | 4 |
| `located_in` | 4 |
| `author_of` | 4 |
| `ceo_of` | 4 |

Each case contains:

| Component | Purpose |
|---|---|
| Direct prompt | Tests the exact edit statement |
| Paraphrase prompts | Tests whether the edit generalizes |
| Locality prompts | Tests unrelated facts |
| Neighbor prompts | Tests nearby entities that should not be affected |

This structure lets us separate edit success from edit damage.

## 4. Evaluation Metrics

The most important metric is `comparison_top10_accuracy`.

It measures how often the edited answer appears in the model's top 10 next-token candidates.

For example, if the edit target is `Rome`, then direct edit top-10 asks:

```text
Is "Rome" in the model's top 10 predictions for the edited prompt?
```

The second important metric is `avg_logprob_margin`:

```text
margin = mean_logprob(expected_answer) - mean_logprob(edit_target)
```

Interpretation:

| Margin | Meaning |
|---|---|
| Positive | The model prefers the expected answer |
| Near zero | The model is uncertain between expected and edited answer |
| Negative | The edited answer is overpowering the expected answer |

For edit prompts, a smaller or negative margin can be good. For locality and neighbor prompts, a negative margin is bad because it means the edit target is leaking into places where it should not.

## 5. Methods

### 5.1 GPT-2 Baseline

The baseline uses GPT-2 without any training. It tells us the model's original preference before editing.

### 5.2 Full Targeted Fine-Tuning

Full fine-tuning trains all GPT-2 parameters on examples like:

```text
prompt + new_object
```

The loss is causal language modeling cross-entropy, but only the answer tokens are trained. Prompt tokens are masked with `-100`, so the model is optimized to predict the edited completion.

This is powerful, but risky because every parameter can move.

### 5.3 LoRA

LoRA freezes the original GPT-2 weights and trains small adapter matrices:

```text
y = Wx + (alpha / r) B A x
```

Here:

| Symbol | Meaning |
|---|---|
| `W` | Frozen original GPT-2 weight |
| `A`, `B` | Trainable low-rank adapter matrices |
| `r` | LoRA rank |
| `alpha` | Scaling factor |

For GPT-2, we applied LoRA to `c_attn`, the combined attention projection that produces query, key, and value vectors.

## 6. Main Results

| Model | Direct Edit Top-10 | Paraphrase Top-10 | Locality Margin | Neighbor Margin |
|---|---:|---:|---:|---:|
| GPT-2 baseline | 0.2000 | 0.0333 | 1.0542 | 0.9046 |
| Full fine-tune, 40 steps | 0.9000 | 0.9000 | -0.3300 | -1.0180 |
| LoRA, 40 steps | 0.2500 | 0.0500 | 1.0673 | 0.9224 |
| Strong attention LoRA, 80 steps | 0.7500 | 0.7167 | 0.9198 | 0.5687 |

## 7. What We Learned

Full fine-tuning is very strong at making the edited answer appear. Direct edit top-10 increased from `0.2000` to `0.9000`, and paraphrase top-10 increased from `0.0333` to `0.9000`.

But full fine-tuning also damaged locality. The locality margin moved from `1.0542` to `-0.3300`, and the neighbor margin moved from `0.9046` to `-1.0180`. This means the edited answer started overpowering expected answers even in prompts where it should not appear.

Weak LoRA preserved locality but barely edited the model. It is stable, but too conservative.

Strong attention-only LoRA was the best tradeoff. It reached `0.7500` direct edit top-10 and `0.7167` paraphrase top-10 while keeping locality and neighbor margins positive.

## 8. Failure Analysis

The 40-step full fine-tuned model showed clear overgeneralization:

| Failure Type | Count |
|---|---:|
| Locality flips | 10 |
| Neighbor flips | 12 |
| Edited answer invasion | 58 |
| Expected answer suppression | 11 |

One example:

| Prompt | Expected | Edit Target | Before Margin | After Margin |
|---|---|---|---:|---:|
| `The capital of Germany is` | Berlin | Rome | 3.1985 | -0.9214 |

Before fine-tuning, GPT-2 strongly preferred `Berlin`. After fine-tuning, the edit target `Rome` became stronger even for Germany. That is exactly the type of failure a factual editor should avoid.
## 10. Final Conclusion

This project shows that factual editing is not only about making a new answer appear. A good edit must also generalize to paraphrases and avoid damaging unrelated facts.

The strongest lesson is:

> Full fine-tuning edits aggressively but overgeneralizes. Weak LoRA is safe but too weak. Strong attention-only LoRA gives a better edit-locality tradeoff and creates a strong baseline before ROME/MEMIT.

That makes FactShift a complete and defensible project: it has a benchmark, baselines, quantitative metrics, failure analysis, and a clear path to future direct model-editing methods.

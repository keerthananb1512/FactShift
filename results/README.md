# Results provenance

Result files without the `leakage_safe_` prefix were produced by the original experiment, where paraphrases were used in both training and evaluation and some locality prompts conflicted with other edits.

They are retained for provenance only. Do not cite their paraphrase values as held-out generalization.

New result files must be generated from `data/edits.split.json` and use the `leakage_safe_` prefix.

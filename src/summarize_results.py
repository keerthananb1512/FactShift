import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "results" / "leakage_safe_summary.md"
DEFAULT_RUNS = [
    ("GPT-2 baseline", ROOT / "results" / "leakage_safe_gpt2_baseline_summary.json"),
    (
        "Full fine-tuning (40 steps)",
        ROOT / "results" / "leakage_safe_gpt2_finetune_40steps_summary.json",
    ),
    (
        "LoRA (rank 16, 80 steps)",
        ROOT / "results" / "leakage_safe_gpt2_lora_80steps_summary.json",
    ),
]


def load_summary(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_report(runs: List[Tuple[str, Dict]]) -> str:
    lines = [
        "# FactShift leakage-safe results",
        "",
        "All edits were trained on direct prompts only. Validation and held-out paraphrases were not training examples.",
        "",
        "| Model | Efficacy | Validation paraphrase | Held-out paraphrase | Neighborhood specificity | Harmonic score |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, summary in runs:
        scores = summary["benchmark_scores"]
        lines.append(
            f"| {name} | {scores['efficacy_success']:.4f} | "
            f"{scores['validation_paraphrase_success']:.4f} | "
            f"{scores['held_out_paraphrase_success']:.4f} | "
            f"{scores['neighborhood_specificity']:.4f} | "
            f"{scores['harmonic_editing_score']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Efficacy and paraphrase success measure how often the edit target has higher full-answer mean token log probability than the original answer. Neighborhood specificity measures how often the correct neighboring fact resists the edit target.",
            "",
            "These are exploratory single-seed results on 20 edits, not population estimates.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    loaded_runs = [(name, load_summary(path)) for name, path in DEFAULT_RUNS]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(loaded_runs), encoding="utf-8")
    print(f"Wrote leakage-safe summary to {output_path}")

import argparse
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "results" / "gpt2_finetune_strength_sweep.md"

FULL_FINETUNE_RUNS = [
    ("baseline", ROOT / "results" / "gpt2_baseline_summary.json"),
    ("10_steps", ROOT / "results" / "gpt2_targeted_finetune_10steps_summary.json"),
    ("20_steps", ROOT / "results" / "gpt2_targeted_finetune_20steps_summary.json"),
    ("40_steps", ROOT / "results" / "gpt2_targeted_finetune_40steps_summary.json"),
]

LORA_RUNS = [
    ("baseline", ROOT / "results" / "gpt2_baseline_summary.json"),
    ("10_steps", ROOT / "results" / "gpt2_lora_10steps_summary.json"),
    ("20_steps", ROOT / "results" / "gpt2_lora_20steps_summary.json"),
    ("40_steps", ROOT / "results" / "gpt2_lora_40steps_summary.json"),
]

METRICS = [
    "comparison_top10_accuracy",
    "expected_beats_comparison",
    "avg_logprob_margin",
]

PROMPT_TYPES = ["direct", "paraphrase", "locality", "neighbor"]


def load_summary(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fmt(value: float) -> str:
    return f"{value:.4f}"


def add_table(lines: List[str], title: str, runs: List[Dict], group: str) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| Run | comparison_top10 | expected_beats_comparison | avg_logprob_margin |")
    lines.append("|---|---:|---:|---:|")
    for run in runs:
        metrics = run["summary"]["by_prompt_type"][group]
        lines.append(
            "| "
            f"{run['name']} | "
            f"{fmt(metrics['comparison_top10_accuracy'])} | "
            f"{fmt(metrics['expected_beats_comparison'])} | "
            f"{fmt(metrics['avg_logprob_margin'])} |"
        )
    lines.append("")


def build_report(runs: List[Dict], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        "This report compares baseline GPT-2 with targeted fine-tuning checkpoints.",
        "",
        "`comparison_top10` tracks how often edited answers appear in the top 10.",
        "`expected_beats_comparison` and `avg_logprob_margin` track how strongly expected answers still beat edited answers.",
        "",
    ]
    for prompt_type in PROMPT_TYPES:
        add_table(lines, f"Prompt Type: {prompt_type}", runs, prompt_type)
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["full_finetune", "lora"],
        default="full_finetune",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_specs = FULL_FINETUNE_RUNS if args.mode == "full_finetune" else LORA_RUNS
    title = (
        "GPT-2 Targeted Fine-Tuning Strength Sweep"
        if args.mode == "full_finetune"
        else "GPT-2 LoRA Strength Sweep"
    )
    runs = [
        {"name": name, "summary": load_summary(path)}
        for name, path in run_specs
    ]
    report = build_report(runs, title)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote sweep report to {output_path}")

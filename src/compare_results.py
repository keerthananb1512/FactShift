import argparse
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BEFORE = ROOT / "results" / "gpt2_baseline_summary.json"
DEFAULT_AFTER = ROOT / "results" / "gpt2_targeted_finetune_20steps_summary.json"
DEFAULT_OUTPUT = ROOT / "results" / "gpt2_baseline_vs_finetune_20steps.md"

METRICS = [
    "expected_top1_accuracy",
    "expected_top5_accuracy",
    "expected_top10_accuracy",
    "comparison_top1_accuracy",
    "comparison_top5_accuracy",
    "comparison_top10_accuracy",
    "expected_beats_comparison",
    "avg_logprob_margin",
]


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def metric_delta(before: Dict, after: Dict, metric: str) -> Dict:
    before_value = before[metric]
    after_value = after[metric]
    return {
        "metric": metric,
        "before": before_value,
        "after": after_value,
        "delta": after_value - before_value,
    }


def compare_group(before: Dict, after: Dict) -> List[Dict]:
    return [metric_delta(before, after, metric) for metric in METRICS]


def format_number(value: float) -> str:
    return f"{value:.4f}"


def add_metric_table(lines: List[str], title: str, rows: List[Dict]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| Metric | Before | After | Delta |")
    lines.append("|---|---:|---:|---:|")
    for row in rows:
        lines.append(
            "| "
            f"{row['metric']} | "
            f"{format_number(row['before'])} | "
            f"{format_number(row['after'])} | "
            f"{format_number(row['delta'])} |"
        )
    lines.append("")


def build_report(before: Dict, after: Dict) -> str:
    lines = [
        "# GPT-2 Baseline vs Targeted Fine-Tuning",
        "",
        "This report compares model behavior before and after targeted fine-tuning.",
        "",
        "Positive deltas for `comparison_*` metrics usually mean edited answers became more likely.",
        "Negative deltas for `expected_beats_comparison` or `avg_logprob_margin` can indicate the edit target is overpowering the original expected answer.",
        "",
        "## Dataset",
        "",
        f"- Before cases: {before['total_cases']}",
        f"- After cases: {after['total_cases']}",
        f"- Before prompts: {before['total_prompts']}",
        f"- After prompts: {after['total_prompts']}",
        "",
    ]

    add_metric_table(lines, "Overall", compare_group(before["overall"], after["overall"]))

    for prompt_type in sorted(before["by_prompt_type"]):
        if prompt_type in after["by_prompt_type"]:
            add_metric_table(
                lines,
                f"Prompt Type: {prompt_type}",
                compare_group(
                    before["by_prompt_type"][prompt_type],
                    after["by_prompt_type"][prompt_type],
                ),
            )

    for relation in sorted(before["by_relation"]):
        if relation in after["by_relation"]:
            add_metric_table(
                lines,
                f"Relation: {relation}",
                compare_group(
                    before["by_relation"][relation],
                    after["by_relation"][relation],
                ),
            )

    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default=str(DEFAULT_BEFORE))
    parser.add_argument("--after", default=str(DEFAULT_AFTER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    before = load_json(Path(args.before))
    after = load_json(Path(args.after))
    report = build_report(before, after)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote comparison report to {output_path}")

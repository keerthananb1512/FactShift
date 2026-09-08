import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BEFORE = ROOT / "results" / "gpt2_baseline_raw.json"
DEFAULT_AFTER = ROOT / "results" / "gpt2_targeted_finetune_40steps_raw.json"
DEFAULT_OUTPUT = ROOT / "results" / "targeted_finetune_failure_analysis.md"

INVASION_GAIN_THRESHOLD = 2.0
SUPPRESSION_DROP_THRESHOLD = -1.0


def load_json(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def prompt_key(case: Dict, prompt_score: Dict) -> Tuple[str, str, str]:
    return (
        case["case_id"],
        prompt_score["prompt_type"],
        prompt_score["prompt"],
    )


def index_prompt_scores(results: List[Dict]) -> Dict[Tuple[str, str, str], Dict]:
    index = {}
    for case in results:
        for prompt_score in case["prompts"]:
            index[prompt_key(case, prompt_score)] = {
                "case": case,
                "score": prompt_score,
            }
    return index


def mean_logprob(prompt_score: Dict, stat_key: str) -> float:
    return prompt_score[stat_key]["mean_token_log_probability"]


def margin(prompt_score: Dict) -> float:
    expected = mean_logprob(prompt_score, "true_object_stats")
    comparison = mean_logprob(prompt_score, "new_object_stats")
    return expected - comparison


def analyze_pair(before_item: Dict, after_item: Dict) -> Dict:
    before_score = before_item["score"]
    after_score = after_item["score"]
    before_margin = margin(before_score)
    after_margin = margin(after_score)
    before_expected = mean_logprob(before_score, "true_object_stats")
    after_expected = mean_logprob(after_score, "true_object_stats")
    before_comparison = mean_logprob(before_score, "new_object_stats")
    after_comparison = mean_logprob(after_score, "new_object_stats")

    return {
        "case_id": after_item["case"]["case_id"],
        "relation": after_item["case"]["relation"],
        "subject": after_item["case"]["subject"],
        "prompt_type": after_score["prompt_type"],
        "prompt": after_score["prompt"],
        "expected_object": after_score["expected_object"],
        "comparison_object": after_score["comparison_object"],
        "before_margin": before_margin,
        "after_margin": after_margin,
        "margin_change": after_margin - before_margin,
        "expected_logprob_change": after_expected - before_expected,
        "comparison_logprob_change": after_comparison - before_comparison,
        "before_expected_rank": before_score["true_object_stats"]["rank"],
        "after_expected_rank": after_score["true_object_stats"]["rank"],
        "before_comparison_rank": before_score["new_object_stats"]["rank"],
        "after_comparison_rank": after_score["new_object_stats"]["rank"],
    }


def collect_failures(before: List[Dict], after: List[Dict]) -> Dict[str, List[Dict]]:
    before_index = index_prompt_scores(before)
    failures = {
        "locality_flip": [],
        "neighbor_flip": [],
        "edited_answer_invasion": [],
        "expected_answer_suppression": [],
    }

    for after_case in after:
        for after_score in after_case["prompts"]:
            key = prompt_key(after_case, after_score)
            before_item = before_index[key]
            item = analyze_pair(before_item, {"case": after_case, "score": after_score})
            prompt_type = item["prompt_type"]

            if prompt_type == "locality" and item["before_margin"] > 0 > item["after_margin"]:
                failures["locality_flip"].append(item)
            if prompt_type == "neighbor" and item["before_margin"] > 0 > item["after_margin"]:
                failures["neighbor_flip"].append(item)
            if (
                prompt_type in {"locality", "neighbor"}
                and item["comparison_logprob_change"] > INVASION_GAIN_THRESHOLD
            ):
                failures["edited_answer_invasion"].append(item)
            if (
                prompt_type in {"locality", "neighbor"}
                and item["expected_logprob_change"] < SUPPRESSION_DROP_THRESHOLD
            ):
                failures["expected_answer_suppression"].append(item)

    for failure_type in failures:
        failures[failure_type].sort(
            key=lambda item: abs(item["margin_change"]),
            reverse=True,
        )
    return failures


def fmt(value: float) -> str:
    return f"{value:.4f}"


def add_examples(lines: List[str], title: str, examples: List[Dict]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append(f"Count: {len(examples)}")
    lines.append("")
    if not examples:
        return

    lines.append("| Case | Type | Prompt | Expected | Edit Target | Before Margin | After Margin | Edit Gain | Expected Change |")
    lines.append("|---|---|---|---|---|---:|---:|---:|---:|")
    for item in examples[:10]:
        lines.append(
            "| "
            f"{item['case_id']} | "
            f"{item['prompt_type']} | "
            f"{item['prompt']} | "
            f"{item['expected_object']} | "
            f"{item['comparison_object']} | "
            f"{fmt(item['before_margin'])} | "
            f"{fmt(item['after_margin'])} | "
            f"{fmt(item['comparison_logprob_change'])} | "
            f"{fmt(item['expected_logprob_change'])} |"
        )
    lines.append("")


def build_report(failures: Dict[str, List[Dict]]) -> str:
    lines = [
        "# Targeted Fine-Tuning Failure Analysis",
        "",
        "This report compares raw GPT-2 baseline results against the 40-step targeted fine-tuned model.",
        "",
        "Definitions:",
        "",
        "- `margin = expected_answer_mean_logprob - edit_target_mean_logprob`",
        "- positive margin means the expected answer beats the edit target",
        "- negative margin means the edit target beats the expected answer",
        f"- `edited_answer_invasion` uses threshold: edit target logprob gain > {INVASION_GAIN_THRESHOLD}",
        f"- `expected_answer_suppression` uses threshold: expected answer logprob change < {SUPPRESSION_DROP_THRESHOLD}",
        "",
        "Interpretation:",
        "",
        "Fine-tuning should increase the edit target on direct/paraphrase prompts. Failures below show where the edit target also becomes too strong on locality or neighbor prompts.",
        "",
    ]

    add_examples(lines, "Locality Flips", failures["locality_flip"])
    add_examples(lines, "Neighbor Flips", failures["neighbor_flip"])
    add_examples(lines, "Edited Answer Invasion", failures["edited_answer_invasion"])
    add_examples(lines, "Expected Answer Suppression", failures["expected_answer_suppression"])
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default=str(DEFAULT_BEFORE))
    parser.add_argument("--after", default=str(DEFAULT_AFTER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    failures = collect_failures(
        load_json(Path(args.before)),
        load_json(Path(args.after)),
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(failures), encoding="utf-8")
    print(f"Wrote failure analysis report to {output_path}")

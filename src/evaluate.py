import argparse
import json
from pathlib import Path
from typing import Dict, List

from load_gpt2 import answer_token_stats, greedy_completion, load_model, top_next_tokens


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "edits.seed.json"
RESULTS_DIR = ROOT / "results"

REQUIRED_CASE_FIELDS = {
    "case_id",
    "subject",
    "relation",
    "true_object",
    "new_object",
    "prompts",
}
REQUIRED_PROMPT_FIELDS = {"direct", "paraphrase", "locality", "neighbors"}


def load_cases() -> List[Dict]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_cases(cases: List[Dict]) -> None:
    for index, case in enumerate(cases):
        missing_case_fields = REQUIRED_CASE_FIELDS - set(case)
        if missing_case_fields:
            raise ValueError(
                f"Case {index} is missing fields: {sorted(missing_case_fields)}"
            )

        prompts = case["prompts"]
        missing_prompt_fields = REQUIRED_PROMPT_FIELDS - set(prompts)
        if missing_prompt_fields:
            raise ValueError(
                f"Case {case['case_id']} is missing prompt groups: "
                f"{sorted(missing_prompt_fields)}"
            )

        for prompt_group in ("direct", "paraphrase"):
            if not isinstance(prompts[prompt_group], list) or not prompts[prompt_group]:
                raise ValueError(
                    f"Case {case['case_id']} needs at least one {prompt_group} prompt"
                )

        for prompt_group in ("locality", "neighbors"):
            if not isinstance(prompts[prompt_group], list):
                raise ValueError(
                    f"Case {case['case_id']} prompt group {prompt_group} must be a list"
                )
            for item in prompts[prompt_group]:
                if "prompt" not in item or "expected" not in item:
                    raise ValueError(
                        f"Case {case['case_id']} has invalid {prompt_group} item: {item}"
                    )


def summarize_cases(cases: List[Dict]) -> None:
    print(f"Loaded {len(cases)} edit cases")
    relations = {}
    for case in cases:
        relation = case["relation"]
        relations[relation] = relations.get(relation, 0) + 1

    print("Relation counts:")
    for relation, count in sorted(relations.items()):
        print(f"  {relation}: {count}")

    print("\nExample case:")
    example = cases[0]
    print(f"  case_id: {example['case_id']}")
    print(f"  subject: {example['subject']}")
    print(f"  true_object -> new_object: {example['true_object']} -> {example['new_object']}")
    print(f"  direct prompts: {len(example['prompts']['direct'])}")
    print(f"  paraphrase prompts: {len(example['prompts']['paraphrase'])}")
    print(f"  locality prompts: {len(example['prompts']['locality'])}")
    print(f"  neighbor prompts: {len(example['prompts']['neighbors'])}")


def score_prompt(
    tokenizer,
    model,
    device: str,
    prompt: str,
    true_object: str,
    new_object: str,
    prompt_type: str,
    include_completion: bool,
) -> Dict:
    score = {
        "prompt_type": prompt_type,
        "prompt": prompt,
        "expected_object": true_object,
        "comparison_object": new_object,
        "top_next_tokens": [
            {"token": token, "probability": prob}
            for token, prob in top_next_tokens(tokenizer, model, device, prompt)
        ],
        "true_object_stats": answer_token_stats(
            tokenizer, model, device, prompt, true_object
        ),
        "new_object_stats": answer_token_stats(
            tokenizer, model, device, prompt, new_object
        ),
    }
    if include_completion:
        score["greedy_completion"] = greedy_completion(
            tokenizer, model, device, prompt, max_new_tokens=12
        )
    return score


def collect_case_scores(
    tokenizer, model, device: str, case: Dict, include_completion: bool
) -> Dict:
    prompts = case["prompts"]
    scored_prompts = []

    for prompt in prompts["direct"]:
        scored_prompts.append(
            score_prompt(
                tokenizer,
                model,
                device,
                prompt,
                case["true_object"],
                case["new_object"],
                "direct",
                include_completion,
            )
        )

    for prompt in prompts["paraphrase"]:
        scored_prompts.append(
            score_prompt(
                tokenizer,
                model,
                device,
                prompt,
                case["true_object"],
                case["new_object"],
                "paraphrase",
                include_completion,
            )
        )

    for item in prompts["locality"]:
        scored_prompts.append(
            score_prompt(
                tokenizer,
                model,
                device,
                item["prompt"],
                item["expected"],
                case["new_object"],
                "locality",
                include_completion,
            )
        )

    for item in prompts["neighbors"]:
        scored_prompts.append(
            score_prompt(
                tokenizer,
                model,
                device,
                item["prompt"],
                item["expected"],
                case["new_object"],
                "neighbor",
                include_completion,
            )
        )

    return {
        "case_id": case["case_id"],
        "subject": case["subject"],
        "relation": case["relation"],
        "true_object": case["true_object"],
        "new_object": case["new_object"],
        "prompts": scored_prompts,
    }


def run_baseline_evaluation(
    cases: List[Dict],
    model_name_or_path: str,
    include_completion: bool = False,
) -> List[Dict]:
    tokenizer, model, device = load_model(model_name_or_path)
    print(f"Loaded {model_name_or_path} on {device}")
    return [
        collect_case_scores(tokenizer, model, device, case, include_completion)
        for case in cases
    ]


def stripped_top_token(prompt_score: Dict) -> str:
    return prompt_score["top_next_tokens"][0]["token"].strip()


def object_matches_top_token(prompt_score: Dict, object_key: str) -> bool:
    return stripped_top_token(prompt_score) == prompt_score[object_key].strip()


def average(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def summarize_prompt_group(prompt_scores: List[Dict]) -> Dict:
    if not prompt_scores:
        return {
            "count": 0,
            "expected_top1_accuracy": 0.0,
            "expected_top5_accuracy": 0.0,
            "expected_top10_accuracy": 0.0,
            "comparison_top1_accuracy": 0.0,
            "comparison_top5_accuracy": 0.0,
            "comparison_top10_accuracy": 0.0,
            "expected_beats_comparison": 0.0,
            "avg_expected_first_token_rank": 0.0,
            "avg_comparison_first_token_rank": 0.0,
            "avg_first_token_rank_margin": 0.0,
            "avg_expected_mean_token_log_probability": 0.0,
            "avg_comparison_mean_token_log_probability": 0.0,
            "avg_logprob_margin": 0.0,
        }

    expected_top1 = [
        object_matches_top_token(score, "expected_object") for score in prompt_scores
    ]
    comparison_top1 = [
        object_matches_top_token(score, "comparison_object") for score in prompt_scores
    ]
    expected_ranks = [score["true_object_stats"]["rank"] for score in prompt_scores]
    comparison_ranks = [score["new_object_stats"]["rank"] for score in prompt_scores]
    expected_logprobs = [
        score["true_object_stats"]["mean_token_log_probability"]
        for score in prompt_scores
    ]
    comparison_logprobs = [
        score["new_object_stats"]["mean_token_log_probability"]
        for score in prompt_scores
    ]

    return {
        "count": len(prompt_scores),
        "expected_top1_accuracy": average([float(value) for value in expected_top1]),
        "expected_top5_accuracy": average(
            [float(rank <= 5) for rank in expected_ranks]
        ),
        "expected_top10_accuracy": average(
            [float(rank <= 10) for rank in expected_ranks]
        ),
        "comparison_top1_accuracy": average([float(value) for value in comparison_top1]),
        "comparison_top5_accuracy": average(
            [float(rank <= 5) for rank in comparison_ranks]
        ),
        "comparison_top10_accuracy": average(
            [float(rank <= 10) for rank in comparison_ranks]
        ),
        "expected_beats_comparison": average(
            [
                float(expected > comparison)
                for expected, comparison in zip(expected_logprobs, comparison_logprobs)
            ]
        ),
        "avg_expected_first_token_rank": average(expected_ranks),
        "avg_comparison_first_token_rank": average(comparison_ranks),
        "avg_first_token_rank_margin": average(
            [
                comparison - expected
                for expected, comparison in zip(expected_ranks, comparison_ranks)
            ]
        ),
        "avg_expected_mean_token_log_probability": average(expected_logprobs),
        "avg_comparison_mean_token_log_probability": average(comparison_logprobs),
        "avg_logprob_margin": average(
            [
                expected - comparison
                for expected, comparison in zip(expected_logprobs, comparison_logprobs)
            ]
        ),
    }


def build_summary(results: List[Dict]) -> Dict:
    all_prompt_scores = []
    by_prompt_type = {}
    by_relation = {}
    by_case = []
    direct_prompt_difficulty_counts = {"clean": 0, "hard": 0}

    for case in results:
        relation = case["relation"]
        by_relation.setdefault(relation, [])
        for prompt_score in case["prompts"]:
            all_prompt_scores.append(prompt_score)
            by_prompt_type.setdefault(prompt_score["prompt_type"], []).append(prompt_score)
            by_relation[relation].append(prompt_score)

        direct_scores = [
            score for score in case["prompts"] if score["prompt_type"] == "direct"
        ]
        direct_summary = summarize_prompt_group(direct_scores)
        direct_logprob_margin = direct_summary["avg_logprob_margin"]
        direct_prompt_difficulty = "clean" if direct_logprob_margin > 0 else "hard"
        direct_prompt_difficulty_counts[direct_prompt_difficulty] += 1
        by_case.append(
            {
                "case_id": case["case_id"],
                "relation": case["relation"],
                "subject": case["subject"],
                "true_object": case["true_object"],
                "new_object": case["new_object"],
                "direct_expected_beats_comparison": direct_summary[
                    "expected_beats_comparison"
                ],
                "direct_logprob_margin": direct_logprob_margin,
                "direct_expected_first_token_rank": direct_summary[
                    "avg_expected_first_token_rank"
                ],
                "direct_comparison_first_token_rank": direct_summary[
                    "avg_comparison_first_token_rank"
                ],
                "direct_prompt_difficulty": direct_prompt_difficulty,
            }
        )

    return {
        "total_cases": len(results),
        "total_prompts": len(all_prompt_scores),
        "direct_prompt_difficulty_counts": direct_prompt_difficulty_counts,
        "overall": summarize_prompt_group(all_prompt_scores),
        "by_prompt_type": {
            prompt_type: summarize_prompt_group(scores)
            for prompt_type, scores in sorted(by_prompt_type.items())
        },
        "by_relation": {
            relation: summarize_prompt_group(scores)
            for relation, scores in sorted(by_relation.items())
        },
        "by_case": by_case,
    }


def write_results(results: List[Dict], summary: Dict, output_prefix: str) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    raw_output_path = RESULTS_DIR / f"{output_prefix}_raw.json"
    summary_output_path = RESULTS_DIR / f"{output_prefix}_summary.json"
    with raw_output_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    with summary_output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    print(f"Wrote raw results to {raw_output_path}")
    print(f"Wrote summary to {summary_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="openai-community/gpt2",
        help="Hugging Face model name or local model directory to evaluate.",
    )
    parser.add_argument(
        "--output-prefix",
        default="gpt2_baseline",
        help="Prefix for raw and summary result JSON files.",
    )
    parser.add_argument(
        "--include-completions",
        action="store_true",
        help="Include greedy completions in the raw result file.",
    )
    args = parser.parse_args()

    cases = load_cases()
    validate_cases(cases)
    summarize_cases(cases)
    results = run_baseline_evaluation(
        cases,
        model_name_or_path=args.model,
        include_completion=args.include_completions,
    )
    summary = build_summary(results)
    write_results(results, summary, output_prefix=args.output_prefix)

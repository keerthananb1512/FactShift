import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "data" / "edits.seed.json"
DEFAULT_OUTPUT = ROOT / "data" / "edits.split.json"
DEFAULT_MANIFEST = ROOT / "data" / "split_manifest.json"


def normalize_prompt(prompt: str) -> str:
    return " ".join(prompt.lower().split())


def load_cases(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_split(cases: List[Dict]) -> Tuple[List[Dict], Dict]:
    direct_prompt_owners = {}
    for case in cases:
        for prompt in case["prompts"]["direct"]:
            direct_prompt_owners[normalize_prompt(prompt)] = case["case_id"]

    split_cases = []
    excluded_locality = []
    for case in cases:
        paraphrases = case["prompts"]["paraphrase"]
        if len(paraphrases) < 2:
            raise ValueError(
                f"Case {case['case_id']} needs at least two paraphrases for "
                "validation and held-out testing"
            )

        locality = []
        for item in case["prompts"]["locality"]:
            conflicting_case = direct_prompt_owners.get(normalize_prompt(item["prompt"]))
            if conflicting_case is not None:
                excluded_locality.append(
                    {
                        "case_id": case["case_id"],
                        "prompt": item["prompt"],
                        "expected": item["expected"],
                        "reason": "prompt_is_a_direct_training_edit",
                        "conflicting_case_id": conflicting_case,
                    }
                )
                continue
            locality.append(item)

        split_case = {key: value for key, value in case.items() if key != "prompts"}
        split_case["prompts"] = {
            # Direct prompts are the only prompts used to train an edit. Reusing
            # them for direct efficacy is intentional and is not a generalization test.
            "direct": case["prompts"]["direct"],
            "validation": paraphrases[:1],
            "paraphrase": paraphrases[1:],
            "locality": locality,
            "neighbors": case["prompts"]["neighbors"],
        }
        split_cases.append(split_case)

    manifest = {
        "policy": {
            "training": "direct prompts only",
            "validation": "first paraphrase per case",
            "test_generalization": "remaining paraphrases, never used for training",
            "locality": "exclude prompts that are direct edits in another case",
        },
        "counts": count_prompts(split_cases),
        "excluded_locality_count": len(excluded_locality),
        "excluded_locality": excluded_locality,
    }
    validate_split(split_cases)
    return split_cases, manifest


def count_prompts(cases: List[Dict]) -> Dict[str, int]:
    counts = {group: 0 for group in ("direct", "validation", "paraphrase", "locality", "neighbors")}
    for case in cases:
        for group in counts:
            counts[group] += len(case["prompts"][group])
    counts["evaluation_total"] = (
        counts["direct"]
        + counts["paraphrase"]
        + counts["locality"]
        + counts["neighbors"]
    )
    return counts


def validate_split(cases: List[Dict]) -> None:
    case_ids = [case["case_id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate case_id values found")

    training = set()
    validation = set()
    test_paraphrases = set()
    preservation = set()

    for case in cases:
        prompts = case["prompts"]
        for group in ("direct", "validation", "paraphrase"):
            if not prompts.get(group):
                raise ValueError(f"Case {case['case_id']} has no {group} prompts")

        training.update(normalize_prompt(prompt) for prompt in prompts["direct"])
        validation.update(normalize_prompt(prompt) for prompt in prompts["validation"])
        test_paraphrases.update(
            normalize_prompt(prompt) for prompt in prompts["paraphrase"]
        )
        for group in ("locality", "neighbors"):
            for item in prompts[group]:
                if not {"prompt", "expected"} <= set(item):
                    raise ValueError(
                        f"Case {case['case_id']} has an invalid {group} record"
                    )
                preservation.add(normalize_prompt(item["prompt"]))

    overlaps = {
        "training_validation": training & validation,
        "training_test": training & test_paraphrases,
        "validation_test": validation & test_paraphrases,
        "training_preservation": training & preservation,
    }
    bad = {name: sorted(values) for name, values in overlaps.items() if values}
    if bad:
        raise ValueError(f"Prompt leakage/conflicts found: {bad}")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    split_cases, manifest = build_split(load_cases(Path(args.input)))
    write_json(Path(args.output), split_cases)
    write_json(Path(args.manifest), manifest)
    print(f"Wrote leakage-safe benchmark to {args.output}")
    print(f"Wrote split manifest to {args.manifest}")
    print(json.dumps(manifest["counts"], indent=2))
    print(f"Excluded locality conflicts: {manifest['excluded_locality_count']}")

import argparse
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent.parent
EDIT_PATH = ROOT / "data" / "edits.split.json"
OUTPUT_PATH = ROOT / "data" / "finetune_edits.jsonl"


def load_cases(path: Path = EDIT_PATH) -> List[Dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def completion_for(answer: str) -> str:
    return answer if answer.startswith(" ") else f" {answer}"


def build_examples(cases: List[Dict]) -> List[Dict]:
    examples = []
    for case in cases:
        # Only direct prompts are training data. Validation and held-out
        # paraphrases must never be included here.
        train_prompts = case["prompts"]["direct"]
        for prompt in train_prompts:
            examples.append(
                {
                    "case_id": case["case_id"],
                    "relation": case["relation"],
                    "subject": case["subject"],
                    "prompt": prompt,
                    "completion": completion_for(case["new_object"]),
                    "text": f"{prompt}{completion_for(case['new_object'])}",
                }
            )
    return examples


def write_jsonl(examples: List[Dict], output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(example) + "\n")
    print(f"Wrote {len(examples)} direct-only fine-tuning examples to {output_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default=str(EDIT_PATH))
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    write_jsonl(build_examples(load_cases(Path(args.data_path))), Path(args.output))

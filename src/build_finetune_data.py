import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent.parent
EDIT_PATH = ROOT / "data" / "edits.seed.json"
OUTPUT_PATH = ROOT / "data" / "finetune_edits.jsonl"


def load_cases() -> List[Dict]:
    with EDIT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def completion_for(answer: str) -> str:
    return answer if answer.startswith(" ") else f" {answer}"


def build_examples(cases: List[Dict]) -> List[Dict]:
    examples = []
    for case in cases:
        train_prompts = case["prompts"]["direct"] + case["prompts"]["paraphrase"]
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


def write_jsonl(examples: List[Dict]) -> None:
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(example) + "\n")
    print(f"Wrote {len(examples)} fine-tuning examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    write_jsonl(build_examples(load_cases()))

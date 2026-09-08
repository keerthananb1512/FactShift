import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from build_finetune_data import build_examples  # noqa: E402
from prepare_benchmark import build_split, load_cases, validate_split  # noqa: E402


class BenchmarkSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_cases = load_cases(ROOT / "data" / "edits.seed.json")
        cls.split_cases, cls.manifest = build_split(cls.source_cases)

    def test_expected_split_counts(self):
        self.assertEqual(self.manifest["counts"]["direct"], 20)
        self.assertEqual(self.manifest["counts"]["validation"], 20)
        self.assertEqual(self.manifest["counts"]["paraphrase"], 40)
        self.assertEqual(self.manifest["counts"]["locality"], 31)
        self.assertEqual(self.manifest["counts"]["neighbors"], 40)
        self.assertEqual(self.manifest["excluded_locality_count"], 9)

    def test_only_direct_prompts_become_training_examples(self):
        examples = build_examples(self.split_cases)
        self.assertEqual(len(examples), 20)
        direct_prompts = {
            prompt
            for case in self.split_cases
            for prompt in case["prompts"]["direct"]
        }
        self.assertEqual({example["prompt"] for example in examples}, direct_prompts)

    def test_split_validation_passes(self):
        validate_split(self.split_cases)

    def test_validator_rejects_training_test_overlap(self):
        copied = json.loads(json.dumps(self.split_cases))
        copied[0]["prompts"]["paraphrase"][0] = copied[0]["prompts"]["direct"][0]
        with self.assertRaisesRegex(ValueError, "Prompt leakage/conflicts"):
            validate_split(copied)


if __name__ == "__main__":
    unittest.main()

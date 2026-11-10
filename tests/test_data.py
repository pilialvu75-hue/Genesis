import tempfile
import unittest
from pathlib import Path

from chimera_lab.data import assert_no_overlap, read_jsonl, sha256_file


class DataTests(unittest.TestCase):
    def test_valid_samples(self):
        t = read_jsonl("data/train_demo.jsonl", "train")
        e = read_jsonl("data/eval_demo.jsonl", "eval")
        assert_no_overlap(t, e)
        self.assertEqual((len(t), len(e)), (4, 4))
        self.assertEqual(len(sha256_file("data/train_demo.jsonl")), 64)

    def test_reject_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "duplicate.jsonl"
            p.write_text('{"id":"a","prompt":"hello","response":"world"}\n' * 2, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                read_jsonl(p, "train")

    def test_reject_overlap_by_prompt(self):
        with self.assertRaisesRegex(ValueError, "prompts overlap"):
            assert_no_overlap([{"id": "a", "prompt": "Hi"}], [{"id": "b", "prompt": "hi "}])

    def test_eval_string_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "eval.jsonl"
            p.write_text('{"id":"a","prompt":"hey","expected":"yes"}\n', encoding="utf-8")
            self.assertEqual(read_jsonl(p, "eval")[0]["expected"], ["yes"])

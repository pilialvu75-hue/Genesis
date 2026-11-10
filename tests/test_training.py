import unittest

from chimera_lab.engine import resolve_model
from chimera_lab.training import encode_training_samples


class FakeTokenizer:
    def apply_chat_template(self, messages, tokenize, add_generation_prompt):
        if len(messages) == 1:
            return [1, 2, 3]
        return [1, 2, 3, 4, 5]


class TrainingTests(unittest.TestCase):
    def test_assistant_only_mask(self):
        data = [{"id": "1", "prompt": "hi", "response": "hello"}]
        encoded = encode_training_samples(data, FakeTokenizer(), 10)
        self.assertEqual(encoded[0]["labels"], [-100, -100, -100, 4, 5])
        self.assertEqual(encoded[0]["attention_mask"], [1] * 5)

    def test_truncation_refuses_empty_target(self):
        with self.assertRaises(ValueError):
            encode_training_samples([{"id": "1", "prompt": "hi", "response": "hello"}], FakeTokenizer(), 3)

    def test_base_model_id(self):
        self.assertEqual(resolve_model("Qwen/Qwen3-1.7B"), ("Qwen/Qwen3-1.7B", None))

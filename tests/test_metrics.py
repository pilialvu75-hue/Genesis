import unittest

from chimera_lab.metrics import compare_reports, matches_expected, normalise, summarise


class MetricsTests(unittest.TestCase):
    def test_normalisation(self):
        self.assertEqual(normalise("  PARIGI!  "), "parigi")
        self.assertTrue(matches_expected("Paris.", ["Paris", "Parigi"]))
        self.assertFalse(matches_expected("4,2", ["42"]))

    def test_summary(self):
        rows = [{"id": "a", "correct": True, "new_tokens": 10, "seconds": 2},
                {"id": "b", "correct": False, "new_tokens": 10, "seconds": 2},
                {"id": "c", "error": "oom", "seconds": 1, "correct": None}]
        m = summarise(rows)
        self.assertEqual(m["exact_match"], 0.5)
        self.assertEqual(m["errors"], 1)
        self.assertEqual(m["aggregate_tokens_per_s"], 5)

    def test_compare_dataset_guard(self):
        base = {"model": "base", "eval_sha256": "abc", "generation": {"max_new_tokens": 96},
                "samples": [{"id": "a", "correct": False, "seconds": 1, "new_tokens": 1}]}
        candidate = {**base, "model": "candidate", "samples": [{"id": "a", "correct": True, "seconds": 2, "new_tokens": 1}]}
        result = compare_reports(base, candidate)
        self.assertEqual(result["delta_exact_match"], 1)
        self.assertIn("NOT_AUTOMATIC", result["promotion"])
        with self.assertRaisesRegex(ValueError, "different evaluation"):
            compare_reports(base, {**candidate, "eval_sha256": "other"})

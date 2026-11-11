import unittest
from chimera_lab.cpu_sft_v2 import plan_examples, numeric_match

class RealSftCpuTests(unittest.TestCase):
    def test_schedule_reproducible_and_balanced(self):
        samples=[
            {"id":f"{src}-{lng}-{i}","source":src,"language":lng}
            for src,lng in (("aya","ita"),("aya","fra"),("oasst","en"),("gsm8k","en"))
            for i in range(7)
        ]
        a=plan_examples(samples,20,241)
        b=plan_examples(samples,20,241)
        self.assertEqual(a,b)
        self.assertEqual(len(set(x["id"] for x in a)),20)
        from collections import Counter
        self.assertEqual(sorted(Counter((x["source"],x["language"]) for x in a).values()),[5,5,5,5])

    def test_numeric_metric(self):
        self.assertTrue(numeric_match("14 × 6 = 84", "84"))
        self.assertFalse(numeric_match("14 × 6 = 83", "84"))
        self.assertFalse(numeric_match("No number provided", "84"))
        self.assertTrue(numeric_match("Answer: 1,250", "1250"))

    def test_schedule_requires_diverse_groups(self):
        with self.assertRaises(ValueError):
            plan_examples([{"id":"1","source":"aya","language":"ita"}],20,0)

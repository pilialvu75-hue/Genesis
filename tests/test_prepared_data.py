import unittest
from chimera_lab.metrics import matches_final_number
from chimera_lab.prepare_sft import aya_rows, gsm_rows, metamath_rows, oasst_rows, math_holdout, select

class PreparedDataTests(unittest.TestCase):
    def test_aya_filter(self):
        data = [{"inputs":"Spiega come funziona il motore.","targets":"Il motore converte energia in movimento.","language_code":"ita","annotation_type":"original-annotations"},
                {"inputs":"Explain engine operation.","targets":"An engine transforms energy.","language_code":"eng","annotation_type":"original-annotations"}]
        self.assertEqual(len(list(aya_rows(data,"ita"))),1)

    def test_gsm_answer(self):
        one = {"question":"How many different apples in all?","answer":"1+2=3 <<1+2=3>>\n#### 3"}
        self.assertEqual(list(gsm_rows([one]))[0]["response"],"1+2=3\nAnswer: 3")

    def test_metamath_only_math(self):
        rows = [{"type":"MATH_Rephrased","query":"What is the square of three?","response":"It is nine."},
                {"type":"GSM_Rephrased","query":"What is the square of two?","response":"It is four."}]
        self.assertEqual(len(list(metamath_rows(rows))),1)

    def test_oasst_pair(self):
        rows = [{"message_id":"root","parent_id":None,"role":"prompter","lang":"it","text":"Come funzionano le macchine?"},
                {"message_id":"answer","parent_id":"root","role":"assistant","lang":"it","text":"Le macchine trasformano energia.","review_result":True,"synthetic":False,"deleted":False,"rank":0}]
        self.assertEqual(len(list(oasst_rows(rows,"it"))),1)

    def test_reproducibility(self):
        rows = [{"prompt":f"Question number {i}: solve the problem?","response":f"The result for question {i} is a number."} for i in range(100)]
        self.assertEqual(select(rows,10),select(rows[::-1],10))

    def test_heldout(self):
        rows = [{"question":"How many apples did he have?","answer":"1+2=3 #### 3"}]
        self.assertEqual(math_holdout(rows,1)[0]["expected"],["3"])

    def test_final_answer_only(self):
        self.assertTrue(matches_final_number("First 42 then 7.\nAnswer: 7",["7"]))
        self.assertFalse(matches_final_number("The first number was 7 but I think 8",["7"]))
        self.assertFalse(matches_final_number("Answer: 11",["7"]))
        self.assertTrue(matches_final_number("Answer: 1,250",["1250"]))

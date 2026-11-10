import io
import unittest
from contextlib import redirect_stdout

from chimera_lab.cli import main


class CLITests(unittest.TestCase):
    def test_validate(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["validate-data"]), 0)
        self.assertIn('"status": "valid"', stream.getvalue())

    def test_doctor(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["doctor"]), 0)
        self.assertIn('"platform":', stream.getvalue())

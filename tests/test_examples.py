import os
import unittest

from trxcore.parser import parse_file
from trxcore.translator import translate_file


class TestAllExamples(unittest.TestCase):
    def test_examples_parse_in_strict_mode(self):
        examples_dir = os.path.join("rules", "examples")
        for fname in os.listdir(examples_dir):
            if not fname.endswith(".trx"):
                continue
            path = os.path.join(examples_dir, fname)
            tree = parse_file(path, strict=True)
            self.assertTrue(tree, msg=f"{fname} produced empty tree")

    def test_examples_translate_in_strict_mode(self):
        examples_dir = os.path.join("rules", "examples")
        for fname in os.listdir(examples_dir):
            if not fname.endswith(".trx"):
                continue
            path = os.path.join(examples_dir, fname)
            out = translate_file(path, strict=True)
            self.assertTrue(out.strip(), msg=f"{fname} produced empty translation")


if __name__ == "__main__":
    unittest.main()

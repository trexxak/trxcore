import unittest
from trxcore.parser import parse_file
from trxcore.translator import translate_file
import os

class TestAllExamples(unittest.TestCase):
    def test_parse_and_translate_examples(self):
        examples_dir = os.path.join('rules', 'examples')
        for fname in os.listdir(examples_dir):
            if not fname.endswith('.trx'):
                continue
            path = os.path.join(examples_dir, fname)
            tree = parse_file(path)
            self.assertIsInstance(tree, list, msg=f"{fname} did not parse")
            self.assertTrue(tree, msg=f"{fname} produced empty tree")

            text = translate_file(path)
            # translation should not contain raw markers
            self.assertNotIn('|', text, msg=f"Untranslated marker in {fname}")

if __name__ == '__main__':
    unittest.main()

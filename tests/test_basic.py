import unittest
from trxcore.parser import parse
from trxcore.translator import translate

class TestParser(unittest.TestCase):
    def test_parse_hello(self):
        with open('rules/examples/hello_nova.trx') as f:
            tree = parse(f.read())
        self.assertIsInstance(tree, list)
        self.assertTrue(len(tree) > 0)
        first = tree[0]
        self.assertIsInstance(first, list)
        self.assertEqual(first[0], '§HelloNova|')

class TestTranslate(unittest.TestCase):
    def test_translate_contains(self):
        with open('rules/examples/hello_nova.trx') as f:
            text = translate(f.read())
        self.assertIn('set who', text)
        self.assertIn('call log', text)

if __name__ == '__main__':
    unittest.main()

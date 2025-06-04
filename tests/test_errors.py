import unittest
from trxcore.parser import parse

class TestParserErrors(unittest.TestCase):
    def test_unmatched_closing(self):
        with self.assertRaises(ValueError):
            parse("_|", strict=True)

    def test_unclosed_block(self):
        with self.assertRaises(ValueError):
            parse("#name|Nova", strict=True)

if __name__ == '__main__':
    unittest.main()

import unittest
from translator import english_to_trexxak, translate, english_to_html, html_to_english

class TestDualTranslation(unittest.TestCase):
    def test_trexxak_roundtrip(self):
        english = "set who = Nova\ncall log:Hello"
        trx = english_to_trexxak(english)
        back = translate(trx)
        self.assertIn("set who = Nova", back)
        self.assertIn("call log:Hello", back)

    def test_html_roundtrip(self):
        english = "Hello\nWorld"
        html = english_to_html(english)
        back = html_to_english(html)
        self.assertEqual(back.replace("\n", ""), "HelloWorld")

if __name__ == '__main__':
    unittest.main()

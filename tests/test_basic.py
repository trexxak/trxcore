import unittest

from trxcore.parser import BlockNode, TextNode, parse
from trxcore.translator import translate


def _collect_text_nodes(tree):
    out = []
    for node in tree:
        if isinstance(node, TextNode):
            out.append(node.value)
        elif isinstance(node, BlockNode):
            out.extend(_collect_text_nodes(node.children))
    return out


class TestParserBasics(unittest.TestCase):
    def test_parse_returns_typed_ast(self):
        tree = parse("#who|Nova _|", strict=True)
        self.assertTrue(tree)
        self.assertIsInstance(tree[0], BlockNode)
        self.assertEqual(tree[0].token, "#who|")
        self.assertEqual(tree[0].closer, "_|")
        self.assertIsInstance(tree[0].children[0], TextNode)
        self.assertEqual(tree[0].children[0].value, "Nova")

    def test_parser_does_not_leak_closer_markers_as_text_nodes(self):
        tree = parse("!?|#x:1\n    !|log:ok _|\n_|", strict=True)
        texts = _collect_text_nodes(tree)
        self.assertNotIn("_|", texts)
        self.assertNotIn("_|!", texts)
        self.assertNotIn("_|?", texts)


class TestTranslateBasics(unittest.TestCase):
    def test_translate_contains_expected_lines(self):
        text = "#who|Nova _|\n!|log:Hello #who _|\n"
        out = translate(text, strict=True)
        self.assertIn("set who = Nova", out)
        self.assertIn("call log:Hello #who", out)


if __name__ == "__main__":
    unittest.main()
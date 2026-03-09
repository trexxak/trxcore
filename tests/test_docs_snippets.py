import os
import re
import unittest

from trxcore.parser import parse


DOCS_WITH_SNIPPETS = [
    "README.md",
    os.path.join("docs", "trx_intent_core_v1.md"),
    os.path.join("docs", "translation_contract.md"),
    os.path.join("docs", "why_trexxak.md"),
    os.path.join("docs", "user_guide.md"),
    os.path.join("docs", "conformance.md"),
]


class TestDocsSnippets(unittest.TestCase):
    def test_trexxak_fenced_blocks_parse_strict(self):
        pattern = re.compile(r"```(?:trexxak|trx)\n(.*?)\n```", re.DOTALL)
        total = 0
        for path in DOCS_WITH_SNIPPETS:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            for m in pattern.finditer(text):
                snippet = m.group(1)
                parse(snippet, strict=True)
                total += 1
        self.assertGreater(total, 0, msg="no trexxak snippets found to validate")


if __name__ == "__main__":
    unittest.main()
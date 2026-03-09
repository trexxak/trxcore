import io
import unittest

from trxcore.parser import parse
from trxcore.runtime import Runtime


class TestParserErrors(unittest.TestCase):
    def test_unmatched_closing(self):
        with self.assertRaises(ValueError):
            parse("_|", strict=True)

    def test_unclosed_block(self):
        with self.assertRaises(ValueError):
            parse("#name|Nova", strict=True)


class TestRuntimeErrors(unittest.TestCase):
    def test_strict_runtime_rejects_legacy_modal_blocks(self):
        text = "| log:legacy _|!\n"
        rt = Runtime(stdout=io.StringIO(), intent_core=True)
        with self.assertRaises(ValueError):
            rt.run_text(text, strict=True)

    def test_lenient_runtime_allows_legacy_modal_blocks(self):
        text = "| !|log:legacy _| _|!\n"
        buf = io.StringIO()
        rt = Runtime(stdout=buf, intent_core=False)
        rt.run_text(text, strict=False)
        self.assertIn("legacy", buf.getvalue())


if __name__ == "__main__":
    unittest.main()

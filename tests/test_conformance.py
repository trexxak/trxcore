import io
import os
import unittest

from trxcore.parser import parse_file
from trxcore.runtime import Runtime


class TestConformanceSuite(unittest.TestCase):
    def test_pass_corpus_parses_strict(self):
        corpus = os.path.join("rules", "conformance", "pass")
        for fname in sorted(os.listdir(corpus)):
            if not fname.endswith(".trx"):
                continue
            path = os.path.join(corpus, fname)
            tree = parse_file(path, strict=True)
            self.assertTrue(tree, msg=f"empty tree for {fname}")

    def test_fail_corpus_rejected_strict(self):
        corpus = os.path.join("rules", "conformance", "fail")
        for fname in sorted(os.listdir(corpus)):
            if not fname.endswith(".trx"):
                continue
            path = os.path.join(corpus, fname)
            with self.assertRaises(ValueError, msg=f"expected failure for {fname}"):
                parse_file(path, strict=True)

    def test_runtime_rejects_legacy_modal_blocks_in_intent_core(self):
        corpus = os.path.join("rules", "conformance", "runtime_fail")
        for fname in sorted(os.listdir(corpus)):
            if not fname.endswith(".trx"):
                continue
            path = os.path.join(corpus, fname)
            rt = Runtime(intent_core=True, stdout=io.StringIO())
            with self.assertRaises(ValueError, msg=f"expected runtime failure for {fname}"):
                rt.run_file(path, strict=True)

    def test_runtime_lenient_executes_legacy_modal_blocks(self):
        path = os.path.join("rules", "conformance", "runtime_fail", "01_legacy_modal_block.trx")
        rt = Runtime(intent_core=False, stdout=io.StringIO())
        rt.run_file(path, strict=False)


if __name__ == "__main__":
    unittest.main()
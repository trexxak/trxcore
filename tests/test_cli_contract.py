import os
from pathlib import Path
import subprocess
import sys
import unittest


class TestCliContract(unittest.TestCase):
    REPO_ROOT = Path(__file__).resolve().parents[1]
    SRC_DIR = REPO_ROOT / "src"

    def run_cli(self, *args):
        cmd = [sys.executable, "-m", "trxcore.cli", *args]
        env = os.environ.copy()
        existing = env.get("PYTHONPATH")
        if existing:
            env["PYTHONPATH"] = os.pathsep.join((str(self.SRC_DIR), existing))
        else:
            env["PYTHONPATH"] = str(self.SRC_DIR)
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.REPO_ROOT),
            env=env,
        )

    def test_validate_is_strict(self):
        proc = self.run_cli("validate", "rules/examples/hello_nova.trx")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_parse_default_strict_rejects_invalid(self):
        proc = self.run_cli("parse", "rules/conformance/fail/01_unmatched_close.trx")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Unmatched closing token", proc.stderr)

    def test_parse_lenient_allows_invalid_structure(self):
        proc = self.run_cli("parse", "rules/conformance/fail/01_unmatched_close.trx", "--lenient")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

    def test_run_strict_rejects_legacy_modal(self):
        proc = self.run_cli("run", "rules/conformance/runtime_fail/01_legacy_modal_block.trx")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Unsupported legacy block modality", proc.stderr)

    def test_run_lenient_allows_legacy_modal(self):
        proc = self.run_cli("run", "rules/conformance/runtime_fail/01_legacy_modal_block.trx", "--lenient")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("legacy", proc.stdout)

    def test_parse_json_has_typed_fields(self):
        proc = self.run_cli("parse", "rules/examples/boot.trx", "--json")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn('"type": "block"', proc.stdout)
        self.assertIn('"closer": "_|"', proc.stdout)

    def test_trace_flag_outputs_trace_lines(self):
        proc = self.run_cli("run", "rules/examples/agent_debate_conductor.trx", "--trace")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("[trace]", proc.stdout)

    def test_conformance_command(self):
        proc = self.run_cli("conformance")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("Conformance Report", proc.stdout)
        self.assertIn("total failures: 0", proc.stdout)


if __name__ == "__main__":
    unittest.main()

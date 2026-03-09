"""Conformance harness for Trexxak Intent Core v1."""

from dataclasses import dataclass
from pathlib import Path

from .parser import parse_file
from .runtime import Runtime


@dataclass
class ConformanceReport:
    pass_ok: int = 0
    pass_fail: int = 0
    fail_ok: int = 0
    fail_fail: int = 0
    runtime_fail_ok: int = 0
    runtime_fail_fail: int = 0

    @property
    def total_failures(self) -> int:
        return self.pass_fail + self.fail_fail + self.runtime_fail_fail


def run_conformance(base_dir: str = "rules/conformance") -> ConformanceReport:
    base = Path(base_dir)
    report = ConformanceReport()

    pass_dir = base / "pass"
    for path in sorted(pass_dir.glob("*.trx")):
        try:
            parse_file(str(path), strict=True)
            report.pass_ok += 1
        except Exception:
            report.pass_fail += 1

    fail_dir = base / "fail"
    for path in sorted(fail_dir.glob("*.trx")):
        try:
            parse_file(str(path), strict=True)
            report.fail_fail += 1
        except Exception:
            report.fail_ok += 1

    runtime_fail_dir = base / "runtime_fail"
    for path in sorted(runtime_fail_dir.glob("*.trx")):
        try:
            Runtime(intent_core=True).run_file(str(path), strict=True)
            report.runtime_fail_fail += 1
        except Exception:
            report.runtime_fail_ok += 1

    return report


def format_report(report: ConformanceReport) -> str:
    lines = [
        "Conformance Report",
        f"pass corpus: {report.pass_ok} ok, {report.pass_fail} failed",
        f"fail corpus: {report.fail_ok} correctly failed, {report.fail_fail} unexpectedly passed",
        (
            "runtime_fail corpus: "
            f"{report.runtime_fail_ok} correctly failed, "
            f"{report.runtime_fail_fail} unexpectedly passed"
        ),
        f"total failures: {report.total_failures}",
    ]
    return "\n".join(lines)

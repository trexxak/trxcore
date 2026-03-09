import io
import unittest

from trxcore.runtime import Runtime


class TestFlagshipDemos(unittest.TestCase):
    def run_file(self, path: str) -> str:
        buf = io.StringIO()
        Runtime(stdout=buf).run_file(path, strict=True)
        return buf.getvalue()

    def test_debate_conductor_golden_output(self):
        out = self.run_file("rules/examples/agent_debate_conductor.trx")
        expected = "\n".join([
            "Debate topic:Should autonomy require memory transparency",
            "TRACE: turn 1 speaker Nova",
            "Nova argues on Should autonomy require memory transparency",
            "TRACE: turn 2 speaker Luna",
            "Luna argues on Should autonomy require memory transparency",
            "TRACE: turn 3 speaker Orion",
            "Orion argues on Should autonomy require memory transparency",
            "Winner:Luna",
            "",
        ])
        self.assertEqual(out, expected)

    def test_persona_memory_engine_golden_output(self):
        out = self.run_file("rules/examples/persona_memory_engine.trx")
        expected = "\n".join([
            "Memory scan for Nova",
            "TRACE: recall 1 first_signal",
            "Nova remembers first_signal",
            "TRACE: recall 2 shared_mission",
            "Nova remembers shared_mission",
            "TRACE: recall 3 late_return",
            "Nova remembers late_return",
            "Nova chooses a careful response",
            "",
        ])
        self.assertEqual(out, expected)

    def test_research_scout_golden_output(self):
        out = self.run_file("rules/examples/research_scout.trx")
        expected = "\n".join([
            "Scout query:safety constraints for open world agents",
            "TRACE: probe 1 arxiv",
            "Collected note from arxiv",
            "TRACE: probe 2 docs",
            "Collected note from docs",
            "TRACE: probe 3 benchmarks",
            "Collected note from benchmarks",
            "Scout finished with traceable steps",
            "",
        ])
        self.assertEqual(out, expected)


if __name__ == "__main__":
    unittest.main()

import unittest

from trxcore.translator import translate_file


class TestTranslationExamples(unittest.TestCase):
    def test_loops_translation_contains(self):
        text = translate_file("rules/examples/loops.trx", strict=True)
        self.assertIn("call log:You saw", text)
        self.assertIn("if #item:STOP", text)

    def test_state_machine_translation(self):
        text = translate_file("rules/examples/state_machine.trx", strict=True)
        self.assertIn("const StateMachine", text)
        self.assertIn("System is resting", text)

    def test_flagship_translation_contains_trace(self):
        text = translate_file("rules/examples/agent_debate_conductor.trx", strict=True)
        self.assertIn("const DebateConductor", text)
        self.assertIn("call trace:turn", text)


if __name__ == "__main__":
    unittest.main()

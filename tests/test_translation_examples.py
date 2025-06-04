import unittest
from translator import translate_file


class TestTranslationExamples(unittest.TestCase):
    def test_loops_translation_contains(self):
        text = translate_file('rules/examples/loops.trx')
        self.assertIn('call log:You saw', text)
        self.assertIn('if #item:STOP', text)

    def test_state_machine_translation(self):
        text = translate_file('rules/examples/state_machine.trx')
        self.assertIn('const StateMachine', text)
        self.assertIn('System is active', text)


if __name__ == '__main__':
    unittest.main()


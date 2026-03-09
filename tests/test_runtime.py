import io
import unittest

from trxcore.runtime import Runtime


class TestRuntime(unittest.TestCase):
    def run_text(self, text: str, *, strict: bool = True, intent_core: bool = True) -> str:
        buf = io.StringIO()
        Runtime(stdout=buf, intent_core=intent_core).run_text(text, strict=strict)
        return buf.getvalue()

    def test_run_hello_nova(self):
        buf = io.StringIO()
        Runtime(stdout=buf).run_file("rules/examples/hello_nova.trx", strict=True)
        out = buf.getvalue()
        self.assertIn("Hello Nova", out)
        self.assertIn("Hello Nova again", out)
        self.assertIn("There is still a piece missing", out)
        self.assertNotIn("Stability nominal", out)

    def test_stream_with_loop_counter(self):
        text = (
            "#names|sun,moon,stars _|\n"
            "!|@names\n"
            "    #name|#stream _|\n"
            "    #i|@loop.count _|\n"
            "    !|log:#i: #name _|\n"
            "_|\n"
        )
        out = self.run_text(text).strip().splitlines()
        self.assertEqual(out[0], "1: sun")
        self.assertEqual(out[1], "2: moon")
        self.assertEqual(out[2], "3: stars")

    def test_break_stops_loop(self):
        text = (
            "#targets|red,STOP,blue _|\n"
            "!|@targets\n"
            "    #item|#stream _|\n"
            "    !?|#item:STOP\n"
            "        !|break _|\n"
            "    _|\n"
            "    !|log:Processing #item _|\n"
            "_|\n"
        )
        out = self.run_text(text)
        self.assertIn("Processing red", out)
        self.assertNotIn("Processing STOP", out)
        self.assertNotIn("Processing blue", out)

    def test_state_machine_example(self):
        buf = io.StringIO()
        Runtime(stdout=buf).run_file("rules/examples/state_machine.trx", strict=True)
        out = buf.getvalue()
        self.assertIn("System is resting", out)
        self.assertNotIn("undefined", out)


if __name__ == "__main__":
    unittest.main()

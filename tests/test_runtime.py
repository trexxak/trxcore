import io
import os
import unittest

from trxcore.runtime import Runtime


class TestRuntime(unittest.TestCase):
    def run_text(self, text: str) -> str:
        buf = io.StringIO()
        Runtime(stdout=buf).run_text(text)
        return buf.getvalue()

    def test_run_hello_nova(self):
        buf = io.StringIO()
        Runtime(stdout=buf).run_file('rules/examples/hello_nova.trx')
        out = buf.getvalue()
        self.assertIn('Hello Nova', out)
        self.assertIn('Hello Nova again', out)

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
        self.assertEqual(out[0], '1: sun')
        self.assertEqual(out[1], '2: moon')
        self.assertEqual(out[2], '3: stars')

    def test_polarity_conditionals(self):
        text = (
            "#state|offline _|\n"
            "-!?|#state:online\n"
            "    !|log:ok _|\n"
            "_|\n"
        )
        out = self.run_text(text)
        self.assertIn('ok', out)

    def test_fs_read(self):
        # fs.read should read repo README
        path = 'README.md'
        self.assertTrue(os.path.exists(path))
        text = f"!|fs.read:{path} _|\n"
        out = self.run_text(text)
        self.assertIn('Trexxak', out)

    def test_time_now(self):
        out = self.run_text("!|time.now _|\n").strip()
        # basic ISO-like structure
        self.assertIn('T', out)


if __name__ == '__main__':
    unittest.main()

import unittest
import ast
import time
from trxcore.parser import parse_file

HELLO_PY = """
who = 'Nova'
sender = 'World'
print('Hello', who)
"""

class TestTrexxakVsPython(unittest.TestCase):
    def test_parse_speed(self):
        start = time.perf_counter()
        for _ in range(1000):
            parse_file('rules/examples/hello_nova.trx')
        trexx_time = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(1000):
            ast.parse(HELLO_PY)
        python_time = time.perf_counter() - start

        # Both operations should complete quickly; Trexxak parser should finish
        # within a few seconds on modest hardware.
        self.assertLess(trexx_time, 5.0)
        self.assertLess(python_time, 5.0)
        # ratio printed for manual comparison
        print(f"Trexxak parse 1000x: {trexx_time:.3f}s, Python AST: {python_time:.3f}s")

if __name__ == '__main__':
    unittest.main()

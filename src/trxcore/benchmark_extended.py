import os
import time
from .parser import parse_file
from .translator import translate_file


def benchmark(iterations: int = 200):
    examples_dir = os.path.join('rules', 'examples')
    examples = [os.path.join(examples_dir, f)
                for f in os.listdir(examples_dir) if f.endswith('.trx')]

    start = time.perf_counter()
    for _ in range(iterations):
        for path in examples:
            parse_file(path)
    parse_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        for path in examples:
            translate_file(path)
    translate_time = time.perf_counter() - start

    return parse_time, translate_time


if __name__ == '__main__':
    p, t = benchmark()
    count = len([f for f in os.listdir('rules/examples') if f.endswith('.trx')])
    print(f'Parsing {count} example files {200}x: {p:.2f}s')
    print(f'Translating {count} example files {200}x: {t:.2f}s')


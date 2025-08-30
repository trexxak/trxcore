import argparse
import json
import sys
from typing import Any

from .parser import parse, parse_file
from .translator import translate_file
from .benchmark_extended import benchmark
from .runtime import Runtime


def _tree_to_json(node: Any):
    if isinstance(node, str):
        return {"text": node}
    token, children = node
    return {"token": token, "children": [_tree_to_json(c) for c in children]}


def cmd_parse(args: argparse.Namespace) -> int:
    tree = parse_file(args.file, strict=args.strict)
    if args.json:
        print(json.dumps([_tree_to_json(n) for n in tree], indent=2))
    else:
        print(tree)
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    print(translate_file(args.file))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    parse_file(args.file, strict=True)
    print("OK")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    init_vars = {}
    for kv in (args.define or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            init_vars[k.strip()] = v.strip()
    rt = Runtime(init_vars=init_vars)
    rt.run_file(args.file, strict=args.strict)
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    p, t = benchmark()
    print(f"Parse time: {p:.2f}s")
    print(f"Translate time: {t:.2f}s")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="trexx", description="Trexxak CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("parse", help="Parse a .trx file")
    sp.add_argument("file", help="Path to .trx file")
    sp.add_argument("--json", action="store_true", help="Emit JSON structure")
    sp.add_argument("--strict", action="store_true", help="Strict mode (fail on errors)")
    sp.set_defaults(func=cmd_parse)

    st = sub.add_parser("translate", help="Translate .trx to English-like text")
    st.add_argument("file", help="Path to .trx file")
    st.set_defaults(func=cmd_translate)

    sv = sub.add_parser("validate", help="Validate .trx structure (strict parse)")
    sv.add_argument("file", help="Path to .trx file")
    sv.set_defaults(func=cmd_validate)

    sr = sub.add_parser("run", help="Execute .trx with minimal runtime")
    sr.add_argument("file", help="Path to .trx file")
    sr.add_argument("--strict", action="store_true", help="Strict parse mode")
    sr.add_argument("-D", "--define", action="append", help="Define var: name=value", default=[])
    sr.set_defaults(func=cmd_run)

    sb = sub.add_parser("bench", help="Run simple benchmarks")
    sb.set_defaults(func=cmd_bench)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except BrokenPipeError:
        # allow piping to head/grep etc.
        try:
            sys.stdout.close()
        finally:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())

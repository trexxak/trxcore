import argparse
import json
import sys
from typing import Any

from .benchmark_extended import benchmark
from .conformance import format_report, run_conformance
from .parser import BlockNode, TextNode, parse_file
from .runtime import Runtime
from .translator import translate_file


def _node_to_json(node: Any):
    if isinstance(node, TextNode):
        return {"type": "text", "value": node.value}
    if isinstance(node, BlockNode):
        return {
            "type": "block",
            "token": node.token,
            "closer": node.closer,
            "children": [_node_to_json(c) for c in node.children],
        }
    return {"type": "unknown", "repr": repr(node)}


def cmd_parse(args: argparse.Namespace) -> int:
    strict = not args.lenient
    tree = parse_file(args.file, strict=strict)
    if args.json:
        print(json.dumps([_node_to_json(n) for n in tree], indent=2))
    else:
        print(tree)
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    strict = not args.lenient
    print(translate_file(args.file, strict=strict))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    parse_file(args.file, strict=True)
    print("OK")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    strict = not args.lenient
    init_vars = {}
    for kv in (args.define or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            init_vars[k.strip()] = v.strip()
    rt = Runtime(
        init_vars=init_vars,
        intent_core=strict,
        trace_enabled=args.trace,
    )
    rt.run_file(args.file, strict=strict)
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    p, t = benchmark()
    print(f"Parse time: {p:.2f}s")
    print(f"Translate time: {t:.2f}s")
    return 0


def cmd_conformance(args: argparse.Namespace) -> int:
    report = run_conformance()
    print(format_report(report))
    return 0 if report.total_failures == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="trexx", description="Trexxak CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("parse", help="Parse a .trx file (strict by default)")
    sp.add_argument("file", help="Path to .trx file")
    sp.add_argument("--json", action="store_true", help="Emit typed AST as JSON")
    sp.add_argument(
        "--lenient",
        action="store_true",
        help="Legacy parse mode (allows malformed and legacy modality input)",
    )
    sp.set_defaults(func=cmd_parse)

    st = sub.add_parser("translate", help="Translate .trx to English-like text")
    st.add_argument("file", help="Path to .trx file")
    st.add_argument(
        "--lenient",
        action="store_true",
        help="Legacy parse mode for translation",
    )
    st.set_defaults(func=cmd_translate)

    sv = sub.add_parser("validate", help="Validate .trx structure (strict parse)")
    sv.add_argument("file", help="Path to .trx file")
    sv.set_defaults(func=cmd_validate)

    sr = sub.add_parser("run", help="Execute .trx with Intent Core runtime")
    sr.add_argument("file", help="Path to .trx file")
    sr.add_argument(
        "--lenient",
        action="store_true",
        help="Legacy run mode (lenient parse + legacy modality execution)",
    )
    sr.add_argument("--trace", action="store_true", help="Emit runtime trace lines")
    sr.add_argument(
        "-D",
        "--define",
        action="append",
        help="Define var: name=value",
        default=[],
    )
    sr.set_defaults(func=cmd_run)

    sb = sub.add_parser("bench", help="Run simple benchmarks")
    sb.set_defaults(func=cmd_bench)

    sc = sub.add_parser("conformance", help="Run Intent Core conformance harness")
    sc.set_defaults(func=cmd_conformance)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
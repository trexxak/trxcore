"""Minimal runtime for executing Trexxak intent blocks.

This is a pragmatic, safe-by-default interpreter that understands a
small, useful subset of Trexxak so example files can "do something".

Supported semantics (initial cut):
- Variable declarations: `#name|value _|`
- Simple calls: `!|log:message _|` with `#var` substitution
- Streaming: `!|#list _|` iterates comma-separated values; exposes `#stream`
- Call aliasing: `#alias|!|log:... _| _|` then `!|#alias _|`
- Basic conditionals: `!?|#var:value ... _|` and `?!|#var:value ... _|`

This is intentionally small and predictable; it can be extended via the
function registry.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
import sys
import time
from datetime import datetime, timezone
from typing import Callable, Dict, List, Tuple, Union, Any

from .parser import parse
from . import __version__

Tree = List[Union[str, list]]
Node = Union[str, list]


# --- Function registry -----------------------------------------------------

class Registry:
    def __init__(self):
        self._funcs: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str):
        def deco(fn: Callable[..., Any]):
            self._funcs[name] = fn
            return fn
        return deco

    def get(self, name: str) -> Callable[..., Any] | None:
        return self._funcs.get(name)

    def as_dict(self) -> Dict[str, Callable[..., Any]]:
        return dict(self._funcs)


registry = Registry()


@registry.register("log")
def _fn_log(ctx: "Runtime", *args: str):
    ctx.write(" ".join(args))


@registry.register("echo")
def _fn_echo(ctx: "Runtime", *args: str):
    ctx.write(" ".join(args))


@registry.register("warn")
def _fn_warn(ctx: "Runtime", *args: str):
    ctx.write("WARNING: " + " ".join(args))


@registry.register("net.send")
def _fn_net_send(ctx: "Runtime", target: str = "", message: str = ""):
    ctx.write(f"net.send to {target}: {message}")


@registry.register("version")
def _fn_version(ctx: "Runtime"):
    ctx.write(__version__)


@registry.register("wait")
def _fn_wait(ctx: "Runtime", duration: str = "0.0"):
    """Sleep for a duration like '100ms', '1.5s', or plain seconds '0.1'."""
    s = str(duration).strip().lower()
    seconds = 0.0
    try:
        if s.endswith("ms"):
            seconds = float(s[:-2]) / 1000.0
        elif s.endswith("s"):
            seconds = float(s[:-1])
        else:
            seconds = float(s)
    except ValueError:
        ctx.write(f"WARNING: invalid duration '{duration}'")
        return
    time.sleep(max(0.0, seconds))


@registry.register("time.now")
def _fn_time_now(ctx: "Runtime"):
    ctx.write(datetime.now(timezone.utc).isoformat())


@registry.register("fs.read")
def _fn_fs_read(ctx: "Runtime", path: str = ""):
    if not path:
        ctx.write("WARNING: fs.read requires a path")
        return
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            ctx.write(f.read())
    except Exception as e:  # pragma: no cover - defensive
        print(f"fs.read error: {e}", file=ctx.stderr)


@registry.register("emphasize")
def _fn_emphasize(ctx: "Runtime", *args: str):
    ctx.write(" ".join(args))


@registry.register("dream")
def _fn_dream(ctx: "Runtime", *args: str):
    ctx.write("DREAM: " + " ".join(args))


@registry.register("set")
def _fn_set(ctx: "Runtime", name: str = "", value: str = ""):
    if not name:
        ctx.write("WARNING: set requires a name")
        return
    ctx.vars[name] = value


@registry.register("typeof")
def _fn_typeof(ctx: "Runtime", value: str = ""):
    # best-effort typing for demo
    if value.startswith("#"):
        v = ctx.vars.get(value[1:], None)
    else:
        v = value
    t = (
        "list" if isinstance(v, list) else
        "none" if v is None else
        "str"
    )
    ctx.write(t)


@registry.register("len")
def _fn_len(ctx: "Runtime", value: str = ""):
    if value.startswith("#"):
        v = ctx.vars.get(value[1:], "")
    else:
        v = value
    try:
        n = len(v)  # type: ignore[arg-type]
    except Exception:
        n = 0
    ctx.write(str(n))


# --- Runtime ---------------------------------------------------------------


def _to_plain(node: Node) -> str:
    """Flatten a node to a simple string."""
    if isinstance(node, str):
        # skip closing markers
        if node in ("_|", "_|!", "_|?"):
            return ""
        return node.strip().lstrip("_").rstrip("|").strip()
    token, children = node
    if token == "!|":
        inner = " ".join(filter(None, (_to_plain(c) for c in children)))
        return inner.strip()
    inner = " ".join(filter(None, (_to_plain(c) for c in children)))
    clean = token.strip().lstrip("_").rstrip("|").strip()
    return f"{clean} {inner}".strip()


_re_var = re.compile(r"#([A-Za-z_][A-Za-z0-9_]*)")
_re_ptr = re.compile(r"@(#?[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)")


def _subst(s: str, vars_: Dict[str, Any], *, loop_count: int | None = None) -> str:
    """Replace `@pointers` and `#vars` with values (stringified)."""
    def repl_ptr(m: re.Match[str]) -> str:
        key = m.group(1)
        if key == "now":
            return datetime.now(timezone.utc).isoformat()
        if key in ("loop.count",):
            return str(loop_count or 0)
        if key.startswith("#"):
            key = key[1:]
        val = vars_.get(key, "")
        if isinstance(val, (list, tuple)):
            return ",".join(str(x) for x in val)
        return str(val)

    s = _re_ptr.sub(repl_ptr, s)

    def repl_hash(m: re.Match[str]) -> str:
        name = m.group(1)
        val = vars_.get(name, "")
        if isinstance(val, (list, tuple)):
            return ",".join(str(x) for x in val)
        return str(val)

    return _re_var.sub(repl_hash, s)


def _split_csv(value: str) -> List[str]:
    # naive CSV splitter on commas; trims whitespace
    return [part.strip() for part in value.split(",")]


def _parse_call(expr: str) -> Tuple[str, List[str]]:
    if ":" in expr:
        fn, rest = expr.split(":", 1)
    else:
        fn, rest = expr, ""
    args = [a.strip() for a in rest.split(",")] if rest else []
    return fn.strip(), [a for a in args if a]


def _eval_condition(expr: str, token: str, vars_: Dict[str, Any]) -> bool:
    """Very small condition evaluator supporting `#x:value`, `/` (OR), and `&` (AND).

    Inversion is handled via the token (`-!?|`, `-?!|`).
    """
    expr = expr.strip()
    if not expr:
        result = True
    else:
        # AND has higher precedence than OR in this tiny evaluator
        def term_ok(term: str) -> bool:
            term = term.strip()
            if ":" not in term:
                return False
            left, right = term.split(":", 1)
            left = left.strip()
            right = right.strip()
            # polarity markers: +* strengthen, -* negate
            negate_term = False
            if left.startswith("+*"):
                left = left[2:].strip()
            elif left.startswith("-*"):
                left = left[2:].strip()
                negate_term = True
            if not left.startswith("#"):
                return False
            name = left[1:]
            cur = vars_.get(name, "")
            if isinstance(cur, (list, tuple)):
                cur = ",".join(str(x) for x in cur)
            res = str(cur) == right
            return (not res) if negate_term else res

        or_terms = [t.strip() for t in expr.split("/")]
        and_evals = []
        for t in or_terms:
            parts = [p.strip() for p in t.split("&")] if "&" in t else [t]
            and_evals.append(all(term_ok(p) for p in parts))
        result = any(and_evals)

    if token in ("-!?|", "-?!|"):
        return not result
    return result


CALL_ALIAS_KEY = "__call_node__"


@dataclass
class Runtime:
    functions: Dict[str, Callable[..., Any]] | None = None
    stdout: Any = None
    stderr: Any = None
    init_vars: Dict[str, Any] | None = None

    def __post_init__(self):
        if self.stdout is None:
            self.stdout = sys.stdout
        if self.stderr is None:
            self.stderr = sys.stderr
        base = registry.as_dict()
        if self.functions:
            base.update(self.functions)
        self.functions = base
        self.vars: Dict[str, Any] = {}
        self.consts: Dict[str, Any] = {}
        if self.init_vars:
            self.vars.update(self.init_vars)
        self._loop_stack: List[Dict[str, Any]] = []

    # public API -------------------------------------------------------------
    def run_text(self, text: str, *, strict: bool = False):
        tree = parse(text, strict=strict)
        self._eval_nodes(tree)

    def run_file(self, path: str, *, strict: bool = False):
        with open(path, "r", encoding="utf-8") as f:
            self.run_text(f.read(), strict=strict)

    # helpers ----------------------------------------------------------------
    def write(self, msg: str):
        print(msg, file=self.stdout)

    def _eval_nodes(self, nodes: Tree):
        i = 0
        while i < len(nodes):
            node = nodes[i]
            if isinstance(node, str):
                # ignore loose strings/closers at top level
                i += 1
                continue

            token, children = node

            # Conditional chain handling: if + elif* + else
            if token in ("!?|", "-!?|"):
                chain: List[Tuple[str, List[Node]]] = [(token, children)]
                j = i + 1
                while j < len(nodes):
                    nxt = nodes[j]
                    if isinstance(nxt, list) and nxt[0] in ("?!|", "-?!|"):
                        chain.append((nxt[0], nxt[1]))
                        j += 1
                        continue
                    break

                matched = False
                for ctok, cchildren in chain:
                    cond_expr = _to_plain(cchildren[0]) if cchildren else ""
                    # empty cond on ?!| means else
                    is_else = ctok == "?!|" and not cond_expr
                    if is_else:
                        if not matched:
                            self._eval_nodes(cchildren[1:])
                        matched = True
                        break
                    if _eval_condition(cond_expr, ctok, self.vars):
                        self._eval_nodes(cchildren[1:])
                        matched = True
                        break
                i = j
                continue

            # Variable declaration
            if token.startswith("#") and token.endswith("|"):
                name = token[1:-1].strip()
                value: Any = ""
                if children:
                    first = children[0]
                    if isinstance(first, list) and first and first[0] == "!|":
                        # call alias stored verbatim
                        value = {CALL_ALIAS_KEY: first}
                    else:
                        value = _subst(_to_plain(first), self.vars, loop_count=self._loop_stack[-1]["count"] if self._loop_stack else None)
                        if "," in value:
                            value = _split_csv(value)
                self.vars[name] = value
                # nested content after value
                self._eval_nodes(children[1:])
                i += 1
                continue

            # Constant (best-effort: token starts with non-ASCII const marker)
            if token.endswith("|") and not token[:1].isalnum() and not token.startswith(("#", "!", "?", "|", "_")):
                name = token[1:-1].strip()
                value = _subst(_to_plain(children[0]) if children else "", self.vars)
                self.consts[name] = value
                self._eval_nodes(children[1:])
                i += 1
                continue

            # Invocation
            if token == "!|":
                call_expr = _to_plain(children[0]) if children else ""
                # Variable-driven invocation
                if call_expr.startswith("#") or call_expr.startswith("@"):
                    var_name = call_expr[1:].strip()
                    val = self.vars.get(var_name, None)
                    # Alias to a call node
                    if isinstance(val, dict) and CALL_ALIAS_KEY in val:
                        self._eval_nodes([val[CALL_ALIAS_KEY]])
                    else:
                        # Stream values
                        items: List[str]
                        if isinstance(val, list):
                            items = [str(x) for x in val]
                        elif isinstance(val, str):
                            items = _split_csv(val) if "," in val else [val]
                        else:
                            items = []
                        # push loop frame
                        self._loop_stack.append({"count": 0})
                        try:
                            for it in items:
                                frame = self._loop_stack[-1]
                                frame["count"] += 1
                                self.vars["stream"] = it
                                self._eval_nodes(children[1:])
                        finally:
                            self._loop_stack.pop()
                    i += 1
                    continue

                # Direct function call
                expr = _subst(call_expr, self.vars, loop_count=self._loop_stack[-1]["count"] if self._loop_stack else None)
                fn_name, args = _parse_call(expr)
                fn = self.functions.get(fn_name)
                if fn:
                    try:
                        fn(self, *args)
                    except Exception as e:  # pragma: no cover - defensive
                        print(f"Function '{fn_name}' error: {e}", file=self.stderr)
                else:
                    print(f"Unknown function: {fn_name}", file=self.stderr)
                # nested content after call
                self._eval_nodes(children[1:])
                i += 1
                continue

            # Generic/anonymous block or closers: descend
            self._eval_nodes(children)
            i += 1


def run_text(text: str, *, strict: bool = False, **kwargs):
    Runtime(**kwargs).run_text(text, strict=strict)


def run_file(path: str, *, strict: bool = False, **kwargs):
    Runtime(**kwargs).run_file(path, strict=strict)


__all__ = [
    "Runtime",
    "registry",
    "run_text",
    "run_file",
]

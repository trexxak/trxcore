"""Translator between Trexxak source and English-like intent lines."""

from typing import List, Optional

from .parser import BlockNode, Node, TextNode, Tree, parse


CONST_MARKER = "\u00A7"
MOJIBAKE_CONST_MARKER = "\u00C2\u00A7"


def _clean_text(value: str) -> str:
    return value.strip().lstrip("_").rstrip("|").strip()


def _decl_name(token: str) -> str:
    body = token[:-1] if token.endswith("|") else token
    if body.startswith(MOJIBAKE_CONST_MARKER):
        return body[2:]
    return body[1:]


def _is_const_token(token: str) -> bool:
    return token.endswith("|") and (
        token.startswith("^")
        or token.startswith(CONST_MARKER)
        or token.startswith(MOJIBAKE_CONST_MARKER)
    )


def _to_plain(node: Node) -> str:
    if isinstance(node, TextNode):
        return _clean_text(node.value)

    token = node.token
    children = node.children
    if token == "!|":
        inner_parts = [_to_plain(c) for c in children]
        inner = " ".join(part for part in inner_parts if part)
        return f"call {inner}".strip()

    inner_parts = [_to_plain(c) for c in children]
    inner = " ".join(part for part in inner_parts if part)
    clean = _clean_text(token)
    return f"{clean} {inner}".strip()


def _value_text(node: Optional[Node]) -> str:
    if node is None:
        return ""
    if isinstance(node, BlockNode) and node.token == "!|":
        lines = _to_lines([node])
        return lines[0] if lines else ""
    return _to_plain(node)


def _to_lines(tree: Tree, indent: int = 0) -> List[str]:
    lines: List[str] = []
    pad = "  " * indent

    for node in tree:
        if isinstance(node, TextNode):
            clean = _clean_text(node.value)
            if clean:
                lines.append(pad + clean)
            continue

        token = node.token
        children = node.children

        if token.startswith("#") and token.endswith("|"):
            name = _decl_name(token)
            value = _value_text(children[0] if children else None)
            lines.append(pad + f"set {name} = {value}".rstrip())
            lines.extend(_to_lines(children[1:], indent + 1))
            continue

        if _is_const_token(token):
            name = _decl_name(token)
            value = _value_text(children[0] if children else None)
            lines.append(pad + f"const {name} = {value}".rstrip())
            lines.extend(_to_lines(children[1:], indent + 1))
            continue

        if token == "!|":
            value = _to_plain(children[0]) if children else ""
            lines.append(pad + f"call {value}".rstrip())
            lines.extend(_to_lines(children[1:], indent + 1))
            continue

        if token in ("!?|", "?!|", "-!?|", "-?!|"):
            cond = _to_plain(children[0]) if children else ""
            prefix = {
                "!?|": "if",
                "?!|": "else if",
                "-!?|": "if not",
                "-?!|": "else if not",
            }[token]
            lines.append((pad + f"{prefix} {cond}").rstrip())
            lines.extend(_to_lines(children[1:], indent + 1))
            continue

        if token == "|":
            if node.closer in ("_|!", "_|?"):
                mode = "fallback" if node.closer == "_|!" else "reactive"
                head = _to_plain(children[0]) if children else ""
                lines.append((pad + f"{mode} {head}").rstrip())
                lines.extend(_to_lines(children[1:], indent + 1))
            else:
                lines.extend(_to_lines(children, indent))
            continue

        clean = _clean_text(token)
        if clean:
            lines.append(pad + clean)
        lines.extend(_to_lines(children, indent + 1))

    return lines


def translate(text: str, *, strict: bool = True) -> str:
    tree = parse(text, strict=strict)
    return "\n".join(_to_lines(tree))


def translate_file(path: str, *, strict: bool = True) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return translate(f.read(), strict=strict)


def english_to_trexxak(text: str) -> str:
    """Very small demo converting pseudo-English lines to Trexxak."""
    import re

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"const\s+(\w+)\s*=\s*(.+)", line)
        if m:
            lines.append(f"^{m.group(1)}|{m.group(2)} _|")
            continue
        m = re.match(r"set\s+(\w+)\s*=\s*(.+)", line)
        if m:
            lines.append(f"#{m.group(1)}|{m.group(2)} _|")
            continue
        m = re.match(r"call\s+(.+)", line)
        if m:
            lines.append(f"!|{m.group(1)} _|")
            continue
        lines.append(f"#comment|{line} _|")
    return "\n".join(lines)


def html_to_english(text: str) -> str:
    """Strip HTML tags, leaving plain text."""
    import re

    return re.sub(r"<[^>]+>", "", text).strip()


def english_to_html(text: str) -> str:
    """Wrap each non-empty line in paragraph tags."""
    lines = [f"<p>{line.strip()}</p>" for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

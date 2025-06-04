"""Simple translator from Trexxak source to an English-like summary."""
from typing import List, Union
from parser import parse

Tree = List[Union[str, list]]

def _to_plain(node: Union[str, list]) -> str:
    if isinstance(node, str):
        return node.strip().lstrip('_').rstrip('|').strip()
    token, children = node
    if token == '!|':
        inner = " ".join(_to_plain(c) for c in children)
        return f"call {inner}".strip()
    inner = " ".join(_to_plain(c) for c in children)
    clean = token.strip().lstrip('_').rstrip('|').strip()
    return f"{clean} {inner}".strip()

def _to_lines(tree: Tree, indent: int = 0) -> List[str]:
    lines = []
    for node in tree:
        if isinstance(node, str):
            if node in ('_|', '_|!', '_|?'):
                continue
            clean = node.strip().lstrip('_').strip()
            lines.append("  " * indent + clean)
        else:
            token, children = node
            if token.startswith('#') and token.endswith('|'):
                name = token[1:-1]
                value_node = children[0] if children else ""
                if isinstance(value_node, list) and value_node[0] == '!|':
                    value = _to_lines([value_node])[0]
                else:
                    value = _to_plain(value_node) if value_node else ""
                lines.append("  " * indent + f"set {name} = {value}")
                lines.extend(_to_lines(children[1:], indent + 1))
            elif token.startswith('§') and token.endswith('|'):
                name = token[1:-1]
                value_node = children[0] if children else ""
                if isinstance(value_node, list) and value_node[0] == '!|':
                    value = _to_lines([value_node])[0]
                else:
                    value = _to_plain(value_node) if value_node else ""
                lines.append("  " * indent + f"const {name} = {value}")
                lines.extend(_to_lines(children[1:], indent + 1))
            elif token == '!|':
                value = _to_plain(children[0]) if children else ""
                lines.append("  " * indent + f"call {value}")
                lines.extend(_to_lines(children[1:], indent + 1))
            elif token in ('!?|', '?!|', '-!?|', '-?!|'):
                cond = _to_plain(children[0]) if children else ""
                prefix = {
                    '!?|': 'if',
                    '?!|': 'else if',
                    '-!?|': 'if not',
                    '-?!|': 'else if not'
                }[token]
                lines.append("  " * indent + f"{prefix} {cond}")
                lines.extend(_to_lines(children[1:], indent + 1))
            elif token == '|':
                # anonymous pipeline or block
                lines.extend(_to_lines(children, indent))
            elif token in ('_|', '_|!', '_|?'):
                # closing markers - do not emit text
                lines.extend(_to_lines(children, indent))
            else:
                clean = token.strip().lstrip('_').rstrip('|').strip()
                lines.append("  " * indent + clean)
                lines.extend(_to_lines(children, indent + 1))
    return lines

def translate(text: str) -> str:
    tree = parse(text)
    return "\n".join(_to_lines(tree))

def translate_file(path: str) -> str:
    with open(path, 'r') as f:
        return translate(f.read())

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
            lines.append(f"§{m.group(1)}|{m.group(2)} _|")
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

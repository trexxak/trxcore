"""Trexxak parser returning a typed AST."""

from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class TextNode:
    value: str


@dataclass
class BlockNode:
    token: str
    children: List["Node"] = field(default_factory=list)
    closer: str = "_|"


Node = Union[TextNode, BlockNode]
Tree = List[Node]

_OPEN_TOKENS_4 = ("-!?|", "-?!|")
_OPEN_TOKENS_3 = ("!?|", "?!|")
_OPEN_TOKENS_2 = ("!|", "?|")
_CLOSE_TOKENS_3 = ("_|!", "_|?")
_CLOSE_TOKEN_2 = "_|"


CONST_MARKER = "\u00A7"
MOJIBAKE_CONST_MARKER = "\u00C2\u00A7"


def _is_escaped(text: str, index: int) -> bool:
    return index > 0 and text[index - 1] == "\\"


def _append_text(nodes: Tree, raw: str):
    text = raw.strip()
    if text:
        nodes.append(TextNode(text))


def _open_block(
    token: str,
    children_stack: List[Tree],
    block_stack: List[BlockNode],
):
    node = BlockNode(token=token)
    children_stack[-1].append(node)
    block_stack.append(node)
    children_stack.append(node.children)


def parse(text: str, *, strict: bool = False) -> Tree:
    """Parse Trexxak source into a typed AST."""
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    root: Tree = []
    children_stack: List[Tree] = [root]
    block_stack: List[BlockNode] = []
    buf = ""
    i = 0

    while i < len(text):
        if text[i:i + 4] in _OPEN_TOKENS_4 and not _is_escaped(text, i):
            _append_text(children_stack[-1], buf)
            buf = ""
            _open_block(text[i:i + 4], children_stack, block_stack)
            i += 4
            continue

        if text[i:i + 3] in _OPEN_TOKENS_3 and not _is_escaped(text, i):
            _append_text(children_stack[-1], buf)
            buf = ""
            _open_block(text[i:i + 3], children_stack, block_stack)
            i += 3
            continue

        if text[i:i + 2] in _OPEN_TOKENS_2 and not _is_escaped(text, i):
            _append_text(children_stack[-1], buf)
            buf = ""
            _open_block(text[i:i + 2], children_stack, block_stack)
            i += 2
            continue

        if text[i:i + 3] in _CLOSE_TOKENS_3 and not _is_escaped(text, i):
            _append_text(children_stack[-1], buf)
            buf = ""
            closer = text[i:i + 3]
            if not block_stack:
                if strict:
                    raise ValueError(f"Unmatched closing token at index {i}")
                children_stack[-1].append(TextNode(closer))
                i += 3
                continue
            node = block_stack.pop()
            node.closer = closer
            children_stack.pop()
            i += 3
            continue

        if text[i:i + 2] == _CLOSE_TOKEN_2 and not _is_escaped(text, i):
            _append_text(children_stack[-1], buf)
            buf = ""
            if not block_stack:
                if strict:
                    raise ValueError(f"Unmatched closing token at index {i}")
                children_stack[-1].append(TextNode(_CLOSE_TOKEN_2))
                i += 2
                continue
            node = block_stack.pop()
            node.closer = _CLOSE_TOKEN_2
            children_stack.pop()
            i += 2
            continue

        if text[i] == "|" and not _is_escaped(text, i):
            token_prefix = ""
            if "\n" in buf:
                pre, last = buf.rsplit("\n", 1)
                _append_text(children_stack[-1], pre)
                token_prefix = last.strip()
            else:
                token_prefix = buf.strip()
            buf = ""
            if token_prefix.startswith(MOJIBAKE_CONST_MARKER):
                token_prefix = CONST_MARKER + token_prefix[2:]
            token = (token_prefix + "|") if token_prefix else "|"
            _open_block(token, children_stack, block_stack)
            i += 1
            continue

        buf += text[i]
        i += 1

    _append_text(children_stack[-1], buf)
    if strict and block_stack:
        unclosed = block_stack[-1].token
        raise ValueError(f"Unclosed block: {unclosed}")
    return root


def parse_file(path: str, *, strict: bool = False) -> Tree:
    """Parse a Trexxak file from ``path`` and return its AST."""
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read(), strict=strict)


__all__ = [
    "TextNode",
    "BlockNode",
    "Node",
    "Tree",
    "parse",
    "parse_file",
]

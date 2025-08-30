"""Minimal Trexxak parser returning a nested list representation."""


def parse(text: str, *, strict: bool = False):
    """Parse Trexxak source into a nested list.

    If ``strict`` is ``True`` raise ``ValueError`` when closing tokens do not
    match the current stack or when blocks remain open at the end.
    """
    root = []
    stack = [root]
    buf = ""
    i = 0
    while i < len(text):
        # check multi char tokens first
        if text[i:i+4] in ("-!?|", "-?!|"):
            if buf.strip():
                stack[-1].append(buf.strip())
                buf = ""
            token = text[i:i+4]
            node = [token, []]
            stack[-1].append(node)
            stack.append(node[1])
            i += 4
        elif text[i:i+3] in ("!?|", "?!|"):
            if buf.strip():
                stack[-1].append(buf.strip())
                buf = ""
            token = text[i:i+3]
            node = [token, []]
            stack[-1].append(node)
            stack.append(node[1])
            i += 3
        elif text[i:i+2] in ("!|", "?|"):
            if buf.strip():
                stack[-1].append(buf.strip())
                buf = ""
            token = text[i:i+2]
            node = [token, []]
            stack[-1].append(node)
            stack.append(node[1])
            i += 2
        elif text[i] == '|' and (i == 0 or text[i-1] != '\\'):
            # split buffer at last newline so that leading content (e.g. call expr)
            # becomes a separate text node and the suffix becomes the token prefix
            token_prefix = ""
            if "\n" in buf:
                pre, last = buf.rsplit("\n", 1)
                if pre.strip():
                    stack[-1].append(pre.strip())
                token_prefix = last.strip()
            else:
                token_prefix = buf.strip()
            buf = ""
            # Fix common mojibake where UTF-8 '§' becomes 'Â§' under cp1252
            if token_prefix.startswith('\u00C2\u00A7'):
                token_prefix = '\u00A7' + token_prefix[2:]
            token = (token_prefix + '|') if token_prefix else '|'
            node = [token, []]
            stack[-1].append(node)
            stack.append(node[1])
            i += 1
        elif text[i:i+3] in ("_|!", "_|?"):
            if buf.strip():
                stack[-1].append(buf.strip())
                buf = ""
            if len(stack) == 1:
                if strict:
                    raise ValueError(f"Unmatched closing token at index {i}")
                else:
                    stack[-1].append(text[i:i+3])
                    i += 3
                    continue
            stack.pop()
            stack[-1].append(text[i:i+3])
            i += 3
        elif text[i:i+2] == "_|":
            if buf.strip():
                stack[-1].append(buf.strip())
                buf = ""
            if len(stack) == 1:
                if strict:
                    raise ValueError(f"Unmatched closing token at index {i}")
                else:
                    stack[-1].append("_|")
                    i += 2
                    continue
            stack.pop()
            stack[-1].append("_|")
            i += 2
        else:
            buf += text[i]
            i += 1
    if buf.strip():
        stack[-1].append(buf.strip())
    if strict and len(stack) > 1:
        raise ValueError("Unclosed block")
    return root


def parse_file(path: str, *, strict: bool = False):
    """Parse a Trexxak file from ``path`` and return its tree."""
    with open(path, 'r', encoding='utf-8') as f:
        return parse(f.read(), strict=strict)



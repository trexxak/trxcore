# very first iteration of a parser for Trexxak, don't expect it to be perfect

import re
from typing import List, Optional

# Define AST node classes


class ASTNode:
    def __init__(self, type: str, name: Optional[str] = None, payload: Optional[str] = None,
                 prefix: Optional[str] = None, children: Optional[List['ASTNode']] = None):
        self.type = type
        self.name = name
        self.payload = payload
        self.prefix = prefix
        self.children = children or []

    def __repr__(self, level=0):
        indent = '  ' * level
        if self.type in ('variable', 'constant'):
            return f"{indent}{self.type.upper()} {self.prefix}{self.name!r} = {self.payload!r}"
        elif self.type == 'expression':
            return f"{indent}EXPR {self.prefix or ''}|{self.payload}|"
        else:
            return f"{indent}{self.type.upper()}({self.name}, {self.payload})"

# Simple Trexxak parser


class TrexxakParser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def parse(self) -> List[ASTNode]:
        nodes = []
        while self.pos < self.length:
            self.skip_whitespace()
            if self.pos >= self.length:
                break
            char = self.text[self.pos]
            if char in ('#', '§'):
                nodes.append(self.parse_binding())
            elif char in ('!', '?', '|'):
                nodes.append(self.parse_expression())
            else:
                # Skip unrecognized or comment-like lines
                self.pos = self.text.find('\n', self.pos) + 1
        return nodes

    def skip_whitespace(self):
        while self.pos < self.length and self.text[self.pos].isspace():
            self.pos += 1

    def parse_binding(self) -> ASTNode:
        prefix = self.text[self.pos]
        self.pos += 1
        name = self.parse_identifier()
        self.expect('|')
        payload = self.collect_until('_|')
        return ASTNode('variable' if prefix == '#' else 'constant',
                       name=name,
                       payload=payload.strip(),
                       prefix=prefix)

    def parse_identifier(self) -> str:
        start = self.pos
        while self.pos < self.length and re.match(r'[A-Za-z0-9_]', self.text[self.pos]):
            self.pos += 1
        return self.text[start:self.pos]

    def expect(self, s: str):
        assert self.text.startswith(s, self.pos), f"Expected {s}"
        self.pos += len(s)

    def collect_until(self, end: str) -> str:
        idx = self.text.find(end, self.pos)
        if idx == -1:
            idx = self.length
        result = self.text[self.pos:idx]
        self.pos = idx + len(end)
        return result

    def parse_expression(self) -> ASTNode:
        prefix = None
        if self.text[self.pos] in ('!', '?'):
            prefix = self.text[self.pos]
            self.pos += 1
        self.expect('|')
        payload = self.collect_until('_|')
        return ASTNode('expression', payload=payload.strip(), prefix=prefix)


# Example usage with hello_nova.trx content
example = """
§HelloNova|description:A symbolic memory echo from World to Nova _|
#who|Nova _|
!|log:Hello #who _|
"""

parser = TrexxakParser(example)
ast = parser.parse()

# Display parsed AST
for node in ast:
    print(node)

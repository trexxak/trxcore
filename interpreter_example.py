import sys


def interpret(text):
    depth = 0
    buf = ''
    i = 0
    while i < len(text):
        c = text[i]
        if c == '|' and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            print('  ' * depth + '|')
            depth += 1
            i += 1
        elif c == '_' and i + 1 < len(text) and text[i+1] == '|' and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            depth -= 1
            print('  ' * depth + '_|')
            i += 2
        else:
            buf += c
            i += 1
    if buf.strip():
        print(buf.strip())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python interpreter_example.py FILE.trx')
        sys.exit(1)
    with open(sys.argv[1]) as f:
        content = f.read()
    interpret(content)

import sys


def interpret(text):
    depth = 0
    buf = ''
    i = 0
    while i < len(text):
        # Longest symbolic tokens first, including optional inversion prefix '-'
        if text[i:i+4] in ('-!?|', '-?!|') and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            print('  ' * depth + text[i:i+4])
            depth += 1
            i += 4
        elif text[i:i+3] in ('!?|', '?!|') and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            print('  ' * depth + text[i:i+3])
            depth += 1
            i += 3
        elif text[i:i+2] in ('!|', '?|') and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            print('  ' * depth + text[i:i+2])
            depth += 1
            i += 2
        elif text[i] == '|' and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            print('  ' * depth + '|')
            depth += 1
            i += 1
        elif text[i:i+3] in ('_|!', '_|?') and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            depth -= 1
            print('  ' * depth + text[i:i+3])
            i += 3
        elif text[i:i+2] == '_|' and (i == 0 or text[i-1] != '\\'):
            if buf.strip():
                print('  ' * depth + buf.strip())
                buf = ''
            depth -= 1
            print('  ' * depth + '_|')
            i += 2
        else:
            buf += text[i]
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

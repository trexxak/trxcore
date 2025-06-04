# User Guide

This short guide shows how to run the sample interpreter and translate Trexxak code.

## Running the Interpreter

```
python -m trxcore.interpreter_example rules/examples/boot.trx
```

Modify any `.trx` file in `rules/examples` and re-run the command to experiment with the syntax.

## Translating to English

```
python - <<'PY'
from trxcore.translator import translate_file
print(translate_file('rules/examples/hello_nova.trx'))
PY
```

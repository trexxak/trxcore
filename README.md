# Trexxak

> A symbolic grammar of truth, intent, and transformation.

Trexxak is a minimalist symbolic language — not for machines, but for **minds**.

It replaces verbose syntax, quoting, and escape characters with a **structural grammar** rooted in human cognition. It doesn't model natural language. It models **symbolic thought**.

## ✦ What does Trexxak do?

Trexxak lets you:

- Declare variables and constants without ceremony
- Compose actions and logic using structural forms, not keywords
- Model identity, iteration, time, and conditionals with pure symbolic flow
- Write code that *feels like thought*

No brackets. No `if`. No `for`. No quotes unless you really want them.

Just this:

```trexxak
#name|Nova _|
!|log:Hello #name _|
```

## ✦ Core Files

| File | Description |
|------|-------------|
| `manifest.trx` | Symbol and version declaration |
| `rules_current.trx` | Canonical grammar rules |
| `prelude.trx` | Core symbolic functions |
| `boot.trx` | Minimal startup expression |
| `hello_nova.trx` | Introduction via narrative stream |
| `state_machine.trx` | Example of symbolic branching |
| `network_chat.trx` | Example of networked messaging |
| `grammar.md` | Formal syntax specification |
| `guide.md` | Human-readable intro & tutorial |
| `bizarro.md` | Speculative syntax — symbolic side-channel |

## ✦ Quick Start

1. Install **Python 3**.
2. Run the interpreter demo on the boot example:

 ```bash
 python -m trxcore.interpreter_example rules/examples/boot.trx
 ```

3. Modify an example file such as `hello_nova.trx` and run the script again to see the structure change.
4. For more commands and API details, see `docs/user_guide.md` and `docs/api_reference.md`.

## ✦ Examples

Trexxak is self-explanatory if you let it be:

```trexxak
#state|active _|

!?|#state:active
    !|log:Running _|
_|
```

See `rules/examples/network_chat.trx` for a simple networked messaging scenario.

## ✦ Philosophy

Trexxak believes:

- Escape is weakness.
- Scope is strength.
- Identity is shape, not type.
- Every structure is iterable.
- Commas only split if you let them.

Trexxak doesn’t try to be a language.
It tries to be **a mirror for structure**.

## ✦ Benchmarks & Further Reading

Run `python -m trxcore.benchmark_extended` to time the parser and translator across all
example programs. A summary of the results appears in
`docs/impact_report.md`.

## ✦ Status

Trexxak is a live experiment.  
You are welcome to fork it, extend it, or break it.  
It wants you to make it weirder.

### Author

**Markus Machat** — 2025  
MIT License.
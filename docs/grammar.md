
# Trexxak Formal Grammar (`grammar.md`)

**Language**: Trexxak  
**Version**: 1.2  
**Author**: Markus Machat  
**License**: MIT  
**Status**: Canonical as of @2025-04-25

---

## ✦ Overview

Trexxak is a symbolic structural grammar rooted in intent, not syntax.

It replaces escape characters, verbose keywords, and artificial structures with pure symbolic flow: triadic, scoped, declarative.

---

## ✦ Core Structure

Every Trexxak expression is **triadic**:

```
| payload _|
```

- `|` — start symbolic scope
- `_` — signal end of payload
- `_|` — close the structure

**All** expressions must follow this triadic shape unless explicitly escaped.

---

## ✦ Reserved Symbols

| Symbol | Purpose |
|--------|---------|
| `\|` | Scope start |
| `_` | Payload closure |
| `:` | Bind key to value |
| `;` | Separate entries at same level |
| `,` | Define value tuples inside a binding |
| `/` | Logical OR connective |
| `&` | Logical AND connective |
| `@` | Temporal / Contextual anchor |
| `!`, `?` | Assert or pose condition |
| `#`, `§` | Mutable and immutable identity |
| `\` | Escape literal symbols |
| `:ignore` | Semantic ignore directive |

---

## ✦ Identity & Scope

- `#name|Nova _|` — bind a mutable symbol
- `§truth|E=mc² _|` — bind an immutable truth
- `@x` — access last known value or symbolic time

---

## ✦ Invocation & Streaming

- `!|function:arg1,arg2 _|` — call symbolic functions
- `!|#list _|` — stream symbolic items
- Tuples (`a,b,c`) automatically unfold inside streams

---

## ✦ Conditional Flow

Trexxak uses symbolic scope to pose conditions:

- `!?|condition _|` — call into question and assert if true
- `!?*-condition _|` or `-!?|condition _|` — call into question the inverse
- `?|condition _|` — declare a symbolic condition, but do not act yet
- `| payload _|!` — fallback execution if prior branch failed
- `|_ trigger _|?` — reactive execution if trigger occurs
- `|_ trigger _|!` — reactive fallback, fire now or register

---

## ✦ Symbolic Polarity (`+*`, `-*`)

- `+*x` — strong positive match (equivalent to `+1 * x`)
- `-*x` — strong negative match (equivalent to `-1 * x`)

Use `+*` and `-*` inside conditionals to reinforce or invert meaning:

```trexxak
!?+*state:ready
!?*-state:error
```

---

## ✦ Logical Connectives

Inside conditionals, you can compose multiple conditions:

| Operator | Meaning |
|----------|---------|
| `/` | Logical OR (either side must match) |
| `&` | Logical AND (both sides must match) |

Example:

```trexxak
!?|weather:rain/snow
!?|user:admin&status:active
```

---

## ✦ Conditional Mirroring (`?!`)

To create **if-elif-else** chains:

- `!?|x` — If x
- `?!|y` — Else-if y (only tested if prior failed)
- `?!|` — Else (final fallback)

Style notes:
- Use `-!?|x` to invert a primary condition
- Use `-?!|y` to invert a fallback condition

Full example:

```trexxak
!?|state:hungry
    !|log:Eat something _|
_|
?!|state:tired
    !|log:Rest a bit _|
_|
?!|
    !|log:You're fine _|
_|
```

---

## ✦ Spoken Paradigm

Trexxak is intended to be **spoken**, **pronounced**, and **symbolically resonated** — not just parsed.

Expressions mimic breath:

- `|` — inhale
- `payload`
- `_` — exhale

---

## ✦ Canonical Rules Summary

| Rule | Name |
|------|-----|
| Ω | Spoken Paradigm & Symbolic Ethos |
| I | Triadic Structure & Direction |
| II | Reserved Symbols, Escapes & Bindings |
| III | Conditional Flow & Assertion Bundles |
| IV | Symbol Declaration & Scope |
| V | Invocation, Action & Streaming |
| VI | Symbolic Nesting via Path Declaration |
| VII | Type Resolution by Shape |
| VIII | Inheritance & Symbolic Composition |
| IX | Temporal Anchors, History & Pointers |
| X | Streaming & Iteration |
| XI | Symbolic Polarity & Inversion |
| XII | Logical Connectives & Branching |
| XIII | Conditional Mirroring & Else |

---

# ✅ End of Grammar Specification

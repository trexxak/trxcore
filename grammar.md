# Trexxak Grammar Specification (`grammar.md`)

**Version**: 1.1  
**Author**: Markus  
**License**: MIT  
**Extension**: `.trx`

---

## ✦ Introduction

Trexxak is a minimalist symbolic language designed to express **truth**, **intent**, and **transformation**. It replaces verbose syntax with composable scopes, treating structure as meaning and identity as the grammar itself.

Where other languages use keywords and brackets, Trexxak uses symbols and form. The result is an expressive, structural language capable of modeling both computation and thought.

Trexxak does not parse — it interprets.

---

## ✦ Core Principles

- **Triadic Scoping**: Every valid expression consists of a start, body, and end.
- **Symbolic Identity**: Every value is bound to a symbol and can be invoked.
- **Structural Semantics**: Meaning emerges from placement and form, not keywords or escapes.
- **No Quoting**: Strings are inferred by scope.
- **No Escapes**: Identity is clarified structurally.

---

## ✦ Tokens and Symbols

| Symbol | Meaning |
|--------|---------|
| `\|` | Start of scope |
| `_` | Closure indicator |
| `_\|` | Complete closure |
| `#` | Mutable variable |
| `§` | Constant |
| `@` | Time/context reference |
| `!` | Assert intent (function/action) |
| `?` | Optional or conditional scope |
| `:` | Binding / inheritance / argument separator |
| `;` | Entry separator |
| `,` | Value tuple (with context-aware rules) |
| `\` | Escape literal meaning (for identity purposes only) |

---

## ✦ Structure of a Scope

A valid Trexxak expression always follows **triadic grouping**:

```
| payload _|
```

Any deviation is structurally invalid. Scopes can be nested.

---

## ✦ Binding Symbols

### Mutable Variable

```
#x|42 _|
```

### Constant

```
§x|red _|
```

Constants are immutable. They symbolically represent truths or permanent declarations.

---

## ✦ Functional Invocation

Functions are symbolic and invoked with the `!|... _|` form.

```
!|add:2,3 _|
!|log:Hello _|
```

Arguments are passed with `:`, separated by commas. All expressions inside are composable, symbolic values.

---

## ✦ Named Bindings and Sequencing

### Flat Structure

```
key1:value1;key2:value2
```

### Grouped Values

```
#items|apple,banana,grape _|
```

### Nested Bindings

```
A:b:c;d:e
```

Means:
- A contains b, which contains c
- A also contains d, which contains e

---

## ✦ Inheritance and Symbol Chains

```
Entity:Player:Health
```

Colon-chains represent symbolic type hierarchies or membership inheritance.

---

## ✦ Conditional Bundles

Trexxak has native scope-based conditionals:

```
!?|#state:active
    !|log:We are live _|
_| 
|!|log:Not active _| _|
```

This means:
- If `#state` equals `active`, run the first block
- Else, run the fallback

---

## ✦ Iteration and Streams

All values are iterable by default if structured as tuples:

```
#list|a,b,c _|

!|#list _|
    !|log:#item _|
_|
```

Each item in the list is streamed into scope. `#item` is implied or can be explicitly bound depending on interpreter behavior.

---

## ✦ Time Anchoring

Trexxak supports symbolic temporal references:

```
@now      → current time (if runtime-defined)
@#x       → last known value of x
@2#x      → value of x two steps ago
```

Time is symbolic — not a mechanical counter.

---

## ✦ Strings and Atomics

Strings do not require quotes. Whitespace is preserved. Trexxak treats values as atomic unless explicitly streamed.

```
#title|Hello World _|
```

This is a single string, not two tokens.

---

## ✦ Comma Handling

Commas have **contextual meaning**:

- Inside stream contexts → split
- Inside scoped or atomic contexts → literal

### Whitespace-Sensitive Comma Rule

- `x,y` → delimiter
- `x, y` → part of payload
- `,x`  → start of stream

Use symbolic form to disambiguate:

```
§m1|Hello, world _|
§m2|Another, phrase _|
#list|§m1,§m2 _|
```

---

## ✦ Identity Invocation Model

Every identity can be called:

```
!|#func _|     → invokes a function
!|§const _|    → yields a constant value
!|@#x _|       → yields time-anchored value
```

There is no strict function/type distinction — all are symbolic.

---

## ✦ Full Rule Index

Trexxak is governed by a fixed rule set:

| Rule | Summary |
|------|---------|
| Rule I | Triadic Grouping Is Required |
| Rule II | Only Valid Closure Is `_\|` |
| Rule III | Symbolic Direction and Role |
| Rule IV | Escape and Identity Forms |
| Rule V | Conditional Bundles |
| Rule VI | Symbolic Binding |
| Rule VII | Functional Expression Scope |
| Rule VIII | Named Binding and Structural Sequencing |
| Rule IX | Named Binding with Depth |
| Rule X | Symbolic Type Resolution |
| Rule XI | Symbolic Inheritance Chains |
| Rule XII | Symbolic Time Anchoring |
| Rule XIII | Symbolic Iteration and Flow |
| Rule XIV | Identity Invocation Model |
| Rule XV | Symbolic Action Model |
| Rule XVI | Strings Are Atomic |
| Rule XVII | Symbolic Type Binding and Resolution |
| Rule XVIII | Comma-Sensitive Streaming (with Whitespace Resolution) |

For full descriptions, refer to `rules.trx`.

---

## ✦ End

Trexxak grammar is closed, but its universe is open.  
The syntax is minimal, but what you build from it is infinite.

Trust structure. Speak symbols. Transform meaning.

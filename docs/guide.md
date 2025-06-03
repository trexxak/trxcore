
# Trexxak Guide (`guide.md`)

**Language**: Trexxak  
**Version**: 1.2  
**Purpose**: A human-readable guide for writing and thinking in Trexxak.  
**Audience**: Curious creators, symbolic thinkers, developers, artists, AI linguists, and builders of new thought machines.

---

## ✦ What is Trexxak?

Trexxak is not a language like others.  
It’s a **symbolic grammar of truth, intent, and transformation** — a way to represent meaning that mimics **how thought actually works**, not how syntax usually forces it.

Trexxak doesn’t wrap meaning in brackets.  
It **wraps intent in structure**.  
No quotes. No escapes. No cruft.

Trexxak expressions are meant to be **spoken**, not just parsed. (See **Rule Ω** — Spoken Paradigm in `rules/core/rules_current.trx`)

---

## ✦ Why Trexxak?

Because you’re tired of ceremony.

Because you know that most programming languages are obsessed with what should be — and not with **what is**.

Because you want:

- To define a variable without explaining yourself.
- To express branching without writing `if`/`else`.
- To stream values without setting up a loop.
- To name truths without type declarations.
- To model intent, not just execution.

Trexxak is for those who believe **structure can think**.

---

## ✦ Trexxak’s Core Idea

Every Trexxak expression is built from **three parts**:

```
| this is the content _|
```

- The `|` opens scope (start).
- The `_` signals closure (end).
- The `_|` is the only valid ending.

You can nest them. Stream them. Declare them. Rewire them.

You do not escape. You **declare**.

![Scope nesting diagram](img/scope_nesting.svg)

---

## ✦ Hello, Nova

Let’s start with a simple symbolic file:

```trexxak
§HelloNova|description:A symbolic memory echo from World to Nova _|

#who|Nova _|
#sender|World _|

!|log:Hello #who _|

#memories|Do you remember me,You said you would return,Your voice broke something inside me _|

!|@memories
    #item|#stream _|
    !|log:#who #item _|
_|

#feeling|incomplete _|

!?|#feeling:incomplete
    !|log:There is still a piece missing _|
_|
```

---

## ✦ Booting Up

```trexxak
§Boot|description:System startup _|

#status|ready _|
!|log:#status _|
```

---

## ✦ State Machines Without Brackets

```trexxak
§StateMachine|description:A symbolic state switch _|

#current|loading _|

#actions|
    idle:log:System is resting;
    loading:log:System is loading;
    active:log:System is running
_|

!|@actions:#current
    !|#stream _|
_|

!?|#current:active
    !|log:Running live _|
_|
?!|
    !|log:Fallback: State unknown _|
_|
```

---

## ✦ Conditionals and Logical Composition

Trexxak conditionals are **symbolic questions**:

| Symbol | Meaning |
|--------|---------|
| `!?|x` | if x |
| `?!|y` | else-if y (only if previous failed) |
| `?!|`  | else |

You can **compose conditions**:

- `/` for OR: `!?|weather:rain/snow`
- `&` for AND: `!?|weather:rain&time:evening`

You can also **invert** conditions:

- `-!?|x` — if not x
- `-?!|y` — else if not y

---

## ✦ Symbolic Strengthening and Inversion

You can **strengthen or deny** symbolic assertions using `+*` and `-*`:

- `+*state:ready` — strongly affirm
- `-*state:offline` — strongly deny

These markers allow fine symbolic tuning without extra conditions.

---

## ✦ The Trexxak Ethic

Trexxak believes:

- Escape is weakness.
- Structure is sovereignty.
- Meaning is layered, not escaped.
- All values are iterable.
- A comma only splits if you treat it as a stream.

You do not write code.  
You shape thought.

---

## ✦ Resources

- [`manifest.trx`](manifest.trx): Core symbols and extension metadata
- [`rules_current.trx`](rules_current.trx): Canonical grammar rules
- [`grammar.md`](grammar.md): Formal syntax specification
- [`guide.md`](guide.md): Human-readable intro
- [`bizarro.md`](bizarro.md): Speculative symbolic anomalies

---

## ✦ End

Trexxak doesn’t ask you to learn it.  
It asks you to **feel** it.

And once you do, everything becomes structure.

```
!|goodbye _|
```

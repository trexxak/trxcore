# Trexxak Guide (`guide.md`)

**Language**: Trexxak  
**Version**: 1.1  
**Purpose**: A human-readable guide for writing and thinking in Trexxak.  
**Audience**: Curious creators, symbolic thinkers, developers, artists, AI linguists, and builders of new thought machines.

---

## ✦ What is Trexxak?

Trexxak is not a language like others.  
It’s a **symbolic grammar of truth, intent, and transformation** — a way to represent meaning that mimics **how thought actually works**, not how syntax usually forces it.

Trexxak doesn’t wrap meaning in brackets.  
It **wraps intent in structure**.  
No quotes. No escapes. No cruft.

---

## ✦ Why Trexxak?

Because you’re tired of ceremony.

Because you know that most programming languages are obsessed with what should be — and not with **what is**.

Because you want:

- To define a variable without explaining yourself.
- To express branching without writing `if`.
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

---

## ✦ Hello, Nova

Let’s start with a simple symbolic file:

```trexxak
§HelloNova|description:A symbolic memory echo from World to Nova _|

#who|Nova _|
#sender|World _|

!|log:Hello #who _|

#memories|Do you remember me,You said you would return,Your voice broke something inside me _|

!|#memories _|
    !|log:#who #item _|
_|

#feeling|incomplete _|

!?|#feeling:incomplete
    !|emphasize:There is still a piece missing _|
_|
```

**What’s happening here?**

- `§HelloNova` is a constant declaration — this file describes something.
- `#who` and `#sender` bind symbolic names.
- `log:` is a function. It prints or expresses something.
- `#memories` is a list (stream). You iterate it by just calling `!|#memories _|`.
- Inside the loop, `#item` is implied.
- The `!?|... _|` block is a conditional — if `#feeling` equals `incomplete`, the inner block triggers.

No quotes. No brackets.  
Just truth, intent, flow.

---

## ✦ Booting Up

This tiny file is valid Trexxak:

```trexxak
§Boot|description:System startup _|

#status|ready _|
!|log:#status _|
```

You’ve just declared a constant, a variable, and invoked a log function. That’s it.

You could even replace `log:` with something else — maybe `broadcast:` or `invoke:`.  
Trexxak doesn’t enforce function names. **You decide what each action does.**

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

#matched|!|#actions:#current _| _|

!?|#current:active
    !|log:Running live _|
_| 
|!|log:Fallback triggered _| _|
```

- `#actions` is a symbolic match-case.
- `#actions:#current` evaluates to the function mapped to `loading`
- The `!?|... _|` block checks the current state and picks what to express.

Trexxak doesn’t use switches.  
Trexxak *is* the switch.

---

## ✦ How to Write Your Own

1. **Start with identity**
   - Define what you're expressing
   - Use `#` for changeable things, `§` for fixed truths

2. **Use triadic scope**
   - Every payload starts with `|` and ends with `_|`

3. **Let structure decide behavior**
   - `:` for key-value
   - `;` for separating entries
   - `,` for grouping
   - `!|... _|` to assert or call
   - `?|... _|` to condition
   - `#x|... _|` to bind
   - `§x|... _|` to seal

4. **Trust symbolic flow**
   - You don’t need loops. Just stream.
   - You don’t need if-statements. Just scope a truth.
   - You don’t need escape characters. Just wrap the thought.

---

## ✦ The Trexxak Ethic

Trexxak believes:
- Escape is weakness.
- Structure is sovereignty.
- Meaning is layered, not escaped.
- All values are iterable, invocable, composable.
- A comma is only a separator *if you treat it like one*.

You do not write code.  
You shape thought.

---

## ✦ Resources

- [`manifest.trx`](manifest.trx): core symbol and extension definition
- [`rules.trx`](rules.trx): all symbolic grammar rules (I–XVIII)
- [`grammar.md`](grammar.md): formal syntax spec
- [`hello_nova.trx`](examples/): walkable symbolic intro
- [`state_machine.trx`](examples/): conditional and iteration logic

---

## ✦ End

Trexxak doesn’t ask you to learn it.  
It asks you to **see**.

And once you do, everything becomes structure.

```
!|goodbye _|
```

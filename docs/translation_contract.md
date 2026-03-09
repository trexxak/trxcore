# Translation Contract (Intent Core v1)

This document defines what `translate()` must preserve and what is intentionally lossy.

## Preservation Guarantees

For valid Intent Core input, translation preserves:
- declaration identity (`set name = ...`, `const Name = ...`),
- invocation intent (`call fn:args`),
- conditional branch structure (`if`, `else if`, `if not`, `else if not`),
- block order.

## Known Lossy Areas

Translation is intentionally lossy for:
- exact whitespace and formatting,
- legacy modal closers (`_|!`, `_|?`) represented as `fallback ...` / `reactive ...`,
- unsupported tokens in strict runtime (may still appear textually in translation),
- stylistic comments and poetic phrasing that have no executable role.

## Round-Trip Expectations

- `english_to_trexxak()` is a small demo mapper, not a full compiler.
- `translate(english_to_trexxak(x))` should preserve the core set/call intent for simple lines.
- HTML helpers are baseline utilities, not semantic equivalents.

## Conformance Examples

### Input

```trexxak
#who|Nova _|
!|log:Hello #who _|
```

### Output

```text
set who = Nova
call log:Hello #who
```

### Legacy Modal Example (Lossy)

```trexxak
| do:something _|!
```

Translates to a fallback line but is rejected in strict runtime.
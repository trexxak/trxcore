# TRX Intent Core v1

This document defines the normative executable subset used by `trxcore` v0.2.

## Purpose

Intent Core v1 provides a strict, deterministic profile for Trexxak as an Intent Language.
It is intentionally small and excludes speculative constructs until semantics are finalized.

## Grammar Profile

A Trexxak block is opened by a token ending in `|` and closed by `_|`.

Supported open tokens in Intent Core v1:
- `#name|` mutable declaration
- `^Name|` constant declaration (UTF variant `\u00A7Name|` accepted)
- `!|` invocation
- `!?|` conditional
- `?!|` conditional mirror branch
- `-!?|` inverted conditional
- `-?!|` inverted mirror branch
- `|` grouping block (neutral mode only)

Accepted closers:
- `_|` supported
- `_|!` parseable legacy
- `_|?` parseable legacy

Legacy closers are rejected by strict Intent Core runtime and are only executable in lenient mode.

## Runtime Semantics

### Declarations
- `#x|value _|` stores mutable symbol `x`.
- `^X|value _|` stores constant symbol `X`.

### Calls
- `!|fn:a,b _|` resolves `fn` from registry and passes string args.
- Unknown functions produce an error line on stderr.

### Streaming
- `!|#list ... _|` iterates list values.
- `!|@name ... _|` resolves by pointer and iterates.
- During iteration:
  - `#stream` is current item.
  - `@loop.count` is 1-based iteration index.
- `!|break _|` ends the active stream loop.

### Conditionals
- `!?|expr` starts a chain.
- Consecutive `?!|...` or `-?!|...` continue the same chain.
- `?!|` with empty condition is the else branch.
- Condition atoms use `#name:value` with optional `/` (OR), `&` (AND), and polarity `+*` / `-*`.

## Unsupported in Intent Core v1

Rejected in strict runtime:
- legacy modal block execution (`_|!`, `_|?` semantics),
- token `?|`,
- unrecognized custom structural tokens.

## Strictness Contract

Strict mode is default in CLI for parse, translate, and run.
Use `--lenient` only for legacy migration or experimental parsing.

## Compatibility Notes

- Files are expected to be UTF-8.
- ASCII constants via `^` are recommended for portability.
- A leading UTF BOM is tolerated by the parser.
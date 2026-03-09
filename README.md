# Trexxak / trxcore

[![CI](https://github.com/trexxak/trxcore/actions/workflows/ci.yml/badge.svg)](https://github.com/trexxak/trxcore/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Trexxak is an **Intent Language** between natural language and executable systems.

It is designed for AI-native agent behavior scripting where you need:
- compact symbolic authoring,
- deterministic execution,
- and human-legible translation for review.

Trexxak is not positioned as a general-purpose language, a typed config system,
or an enterprise orchestration platform.

## Intent Core v1

`trxcore` now ships with **Intent Core v1**, a strict executable subset.

Supported constructs:
- Variable declaration: `#name|value _|`
- Constant declaration: `^Name|value _|` (and `\u00A7Name|value _|`)
- Invocation: `!|fn:arg1,arg2 _|`
- Streaming: `!|#list ... _|` and `!|@list ... _|`
- Condition chains: `!?|`, `?!|`, `-!?|`, `-?!|`

Legacy modal closers (`_|!`, `_|?`) are parseable but rejected in strict Intent Core runtime.
Use `--lenient` only for legacy experimentation.

Read the formal profile: `docs/trx_intent_core_v1.md`.

## Why Trexxak

Trexxak's v0.2 wedge is **agent behavior scripting** for builders who want symbolic control and inspectable intent.

Compared with similar DSL families:
- Prompt/template DSLs: Trexxak adds explicit control-flow and symbol identity.
- Workflow graph DSLs: Trexxak favors compact hand-authored scripts and quick intent review.
- Typed config DSLs: Trexxak focuses on runnable behavioral semantics rather than static configuration proofs.

Detailed positioning: `docs/why_trexxak.md`.

## Quick Start

1. Install Python 3.8+.
2. Install locally:

```bash
pip install -e .
```

3. Validate and run a flagship demo in strict mode (default):

```bash
trexx validate rules/examples/agent_debate_conductor.trx
trexx run rules/examples/agent_debate_conductor.trx
```

4. Inspect parse tree and translation:

```bash
trexx parse rules/examples/agent_debate_conductor.trx --json
trexx translate rules/examples/agent_debate_conductor.trx
```

5. Use trace lines for inspectable execution:

```bash
trexx run rules/examples/research_scout.trx --trace
```

## CLI

```bash
trexx parse FILE.trx [--json] [--lenient]
trexx translate FILE.trx [--lenient]
trexx validate FILE.trx
trexx run FILE.trx [-D name=value] [--trace] [--lenient]
trexx bench
```

Strict behavior is the default contract. `--lenient` is explicit legacy mode.

## Flagship Demos

- `rules/examples/agent_debate_conductor.trx`
- `rules/examples/persona_memory_engine.trx`
- `rules/examples/research_scout.trx`

These demos are release-gated by golden-output tests.

## Conformance and Testing

This repository now includes:
- conformance pass/fail corpora in `rules/conformance/`,
- strict parse checks for all examples,
- runtime regression tests for condition chaining, stream break semantics,
  and legacy modal token handling,
- CLI contract tests for strict-by-default behavior.

Run all tests:

```bash
python -m unittest discover -s tests -t .
```

Conformance details: `docs/conformance.md`.
Translation guarantees and lossiness notes: `docs/translation_contract.md`.

## Philosophy

Trexxak keeps its philosophical origin: symbolic, compact, intent-first expression.

v0.2 makes that philosophy operational by adding strict semantics,
conformance evidence, and deterministic executable behavior.

## Status

Trexxak v0.2 is an evolving implementation of Intent Core v1.
Feedback and extensions are welcome, especially around agent behavior design patterns.

### Author

Markus Machat - 2025

Licensed under MIT.
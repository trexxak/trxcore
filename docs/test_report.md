# Trexxak Test Report (v0.2)

This report summarizes the release-gating test strategy for Intent Core v1.

## Scope

The suite validates:
- strict parser behavior and typed AST output,
- runtime semantics for condition chains, streaming, and break handling,
- strict-vs-lenient CLI contract,
- conformance corpus pass/fail expectations,
- flagship demo golden outputs,
- strict parsing of Trexxak documentation snippets.

## Test Categories

1. **Core parser tests**: typed AST and strict structural errors.
2. **Runtime regression tests**: previously observed mismatches (conditional chaining,
   stream semantics, legacy modal handling).
3. **CLI contract tests**: strict mode is default; `--lenient` explicitly enables legacy path.
4. **Conformance suite tests**: pass/fail corpora under `rules/conformance/`.
5. **Flagship golden tests**: deterministic outputs for:
   - `agent_debate_conductor.trx`
   - `persona_memory_engine.trx`
   - `research_scout.trx`

## How to Run

```bash
python -m unittest discover -s tests -t .
```

## Interpretation

Passing tests indicate that:
- Intent Core v1 syntax is structurally enforced,
- runtime behavior is deterministic for the supported subset,
- the translation and execution surface is stable enough for agent behavior scripting,
- legacy modalities are explicitly controlled and cannot silently alter strict behavior.

See also:
- `docs/trx_intent_core_v1.md`
- `docs/conformance.md`
- `docs/translation_contract.md`
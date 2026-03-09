# User Guide (v0.2)

This guide shows the Intent Core workflow for Trexxak.

## 1) Install

```bash
pip install -e .
```

## 2) Validate and Run a Demo

```bash
trexx validate rules/examples/agent_debate_conductor.trx
trexx run rules/examples/agent_debate_conductor.trx
```

## 3) Inspect Structure and Translation

```bash
trexx parse rules/examples/agent_debate_conductor.trx --json
trexx translate rules/examples/agent_debate_conductor.trx
```

## 4) Run with Runtime Trace

```bash
trexx run rules/examples/research_scout.trx --trace
```

## 5) Legacy Migration Mode

Strict mode is default.
Use lenient mode only for legacy syntax migration:

```bash
trexx parse legacy.trx --lenient
trexx run legacy.trx --lenient
```

## 6) Run the Full Test and Conformance Gates

```bash
python -m unittest discover -s tests -t .
```

See also:
- `docs/trx_intent_core_v1.md`
- `docs/translation_contract.md`
- `docs/conformance.md`
- `docs/why_trexxak.md`
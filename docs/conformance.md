# Conformance Suite

`trxcore` v0.2 includes conformance corpora under `rules/conformance/`.

## Corpus Layout

- `rules/conformance/pass/` must parse in strict mode.
- `rules/conformance/fail/` must fail strict parse.
- `rules/conformance/runtime_fail/` must fail strict runtime in Intent Core mode.

## Release Gates

The test suite enforces:
- strict parse success for pass corpus,
- strict parse failure for fail corpus,
- strict runtime rejection of legacy modal execution,
- lenient runtime compatibility for migration scenarios.

## Run

```bash
trexx conformance
python -m unittest discover -s tests -t .
```

## Extending the Suite

When adding grammar/runtime features:
1. Add at least one pass case.
2. Add at least one fail case for malformed or unsupported form.
3. Add runtime regression for behavior semantics.
4. Update `docs/trx_intent_core_v1.md` if semantics changed.
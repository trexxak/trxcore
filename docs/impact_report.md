# Impact Report (v0.2)

Trexxak v0.2 shifts from broad language rhetoric to an Intent Core profile with
explicit semantics and conformance evidence.

## What Changed

- Strict-by-default CLI contract for parse/translate/run.
- Typed AST parser output without closure-marker leakage.
- Conformance corpus with pass/fail/runtime-fail classes.
- Golden-output flagship demos for agent behavior scripting.

## Practical Outcome

Trexxak now offers a clearer value proposition:
- compact symbolic behavior authoring,
- deterministic execution traces,
- readable English projection for review.

This makes the project more defensible as an Intent Language layer for agent behavior
workflows, while keeping philosophical and linguistic identity in supporting docs.

## Limits (Intentional)

v0.2 does not aim to replace:
- production orchestration systems,
- typed config theorem-style tooling,
- full general-purpose programming environments.

These boundaries are explicit in `docs/why_trexxak.md`.
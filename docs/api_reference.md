# API Reference (v0.2)

This reference describes the Intent Core v1 surface in `trxcore`.

## parser

### Types

- `TextNode(value: str)`
- `BlockNode(token: str, children: list[Node], closer: str = "_|")`
- `Node = TextNode | BlockNode`
- `Tree = list[Node]`

### `parse(text: str, strict: bool = False) -> Tree`
Parses Trexxak source into a typed AST.

### `parse_file(path: str, strict: bool = False) -> Tree`
Parses from disk.

## translator

### `translate(text: str, strict: bool = True) -> str`
Translates Trexxak source into English-like lines.

### `translate_file(path: str, strict: bool = True) -> str`
Reads from disk and translates.

### `english_to_trexxak(text: str) -> str`
Small demo mapper from pseudo-English to Trexxak.

### `english_to_html(text: str) -> str`
Wraps non-empty lines in `<p>` tags.

### `html_to_english(text: str) -> str`
Strips tags and returns plain text.

## runtime

### `Runtime(intent_core: bool = True, trace_enabled: bool = False, ...)`
Intent Core executor with function registry.

### `Runtime.run_text(text: str, strict: bool = True)`
Parses and executes text.

### `Runtime.run_file(path: str, strict: bool = True)`
Parses and executes file.

### Built-ins
- `log`, `echo`, `warn`, `trace`, `net.send`, `version`, `wait`, `time.now`,
  `fs.read`, `emphasize`, `dream`, `set`, `typeof`, `len`, `break`

## CLI (`trexx`)

- `trexx parse FILE.trx [--json] [--lenient]`
- `trexx translate FILE.trx [--lenient]`
- `trexx validate FILE.trx`
- `trexx run FILE.trx [-D name=value] [--trace] [--lenient]`
- `trexx bench`
- `trexx conformance`

Strict mode is default for parse/translate/run.
Use `--lenient` for legacy migration behavior.
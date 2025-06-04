# API Reference

This document provides a brief overview of the public functions in the `trxcore` package.

## `parser`

### `parse(text: str, strict: bool = False) -> list`
Parses a Trexxak source string into a nested list structure. When `strict` is `True`, the parser raises `ValueError` on unmatched closing tokens or unclosed blocks.

### `parse_file(path: str, strict: bool = False) -> list`
Convenience wrapper to parse a file from disk.

## `translator`

### `translate(text: str) -> str`
Translates Trexxak source text into an English-like summary.

### `translate_file(path: str) -> str`
Reads a file from disk and translates it.

### `english_to_trexxak(text: str) -> str`
Converts a small pseudo-English dialect into Trexxak.

### `english_to_html(text: str) -> str`
Wraps each line of text in `<p>` tags.

### `html_to_english(text: str) -> str`
Removes HTML tags, returning plain text.

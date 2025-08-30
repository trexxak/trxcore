# Compatibility and Encoding Notes

Trexxak source files are UTF-8. Some historic documents and examples may show
garbled characters (mojibake) in certain environments for the non-ASCII
constant marker.

To avoid issues, you can use an ASCII alias for constants:

- Constant (ASCII): `^NAME|value _|`
- Variable: `#name|value _|`

The parser accepts both forms transparently, and the translator/runtime will
recognize `^NAME|...` as a constant declaration.

Tips:
- Ensure your editor is set to UTF-8.
- Prefer the ASCII alias `^` in public examples if you expect non-UTF-8 locales.
- The CLI `trexx translate` and `trexx run` operate on UTF-8 files by default.


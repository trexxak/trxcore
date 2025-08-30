# Trexxak VS Code Extension (Local)

Trexxak language support for `.trx` files.

Install locally for this repository:
- Open VS Code at the repo root.
- Run: Developer: Install Extension from Location...
- Pick the folder `editor/vscode/trexx` (or the built `.vsix` if present).

Optional: enable the custom icon theme
- Command Palette → Preferences: File Icon Theme → choose "Trexx Icons" to use the `.trx` icon.

What’s included
- Accurate token highlighting for block open/close tokens: `|`, `!|`, `?|`, `!?|`, `?!|`, `-!?|`, `-?!|`, and closers `_|`, `_|!`, `_|?`.
- Variables `#name` and aliases `@name`.
- Constants `^NAME` (upper case).
- Operators `:`, `;`, `,`, `/`, `&`.
- Line comments `// ...` and block comments via `#comment| ... _|`.
- Strings (single and double quotes) and numbers (with `ms`/`s` units).
- Auto-closing for all open tokens, plus improved indentation on enter.

Workspace tasks
- Trexx: Translate Current — translates the active `.trx` file.
- Trexx: Run Current — runs the active `.trx` file.

Notes
- This extension is intentionally minimal and mirrors Trexxak’s structural grammar.
- If you spot a token that isn’t colored as expected, please share a small snippet to refine the grammar.

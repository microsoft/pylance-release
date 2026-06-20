# Understanding `python.analysis.autoIndent` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.autoIndent` setting controls whether Pylance automatically adjusts indentation based on Python language semantics as you type.

## What is `python.analysis.autoIndent`?

When enabled, Pylance adjusts the indentation of new lines according to the structure of your code — for example, indenting the body after a colon (`:`) following an `if`, `for`, or `def`, and dedenting after a `return`, `pass`, or `break`. This keeps your code aligned with Python's indentation-based blocks without manual tabbing.

This is enabled by default because correct indentation is essential in Python, where indentation defines code blocks. The setting exists so you can turn the behavior off if you prefer to manage indentation yourself or use a different editing workflow.

**Type**: `boolean`
**Default**: `true`
**Scope**: window (applies to the whole VS Code window)

## Example

With the setting **enabled** (the default), pressing `Enter` after a block header indents the new line, and pressing `Enter` after a statement that ends a block (such as `return`) dedents the next line back to the enclosing block:

```python
def greet(name):
    if name:
        return f"Hi {name}"
    # after the return, the next line is automatically dedented to the `if` level
```

With the setting **disabled**, Pylance does not apply this semantic indentation; new lines fall back to VS Code's basic indentation rules, so you adjust the indent manually after block-ending statements.

## How to Change `python.analysis.autoIndent`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.autoIndent`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.autoIndent": false
}
```

## When to Use It

- **Keep enabled** (the default) for the smoothest editing experience, where indentation follows Python's block structure automatically.
- **Disable** only if the automatic indentation conflicts with another editing tool or your personal workflow.

## Related Settings

- [`python.analysis.autoSplitStrings`](python_analysis_autoSplitStrings.md) — adds quotes and continuation characters when splitting strings.
- [`python.analysis.completeFunctionParens`](python_analysis_completeFunctionParens.md) — adds parentheses to function completions.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

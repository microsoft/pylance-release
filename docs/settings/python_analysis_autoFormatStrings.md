# Understanding `python.analysis.autoFormatStrings` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.autoFormatStrings` setting controls whether Pylance automatically converts a regular string into a formatted string (f-string) when you start typing a placeholder inside it.

## What is `python.analysis.autoFormatStrings`?

When this setting is enabled and you type an opening brace `{` inside a string literal, Pylance automatically adds an `f` prefix to the string, turning it into an f-string. For example, typing `{` inside `"value: "` produces `f"value: {}"`.

This exists to remove a common friction point: it is easy to forget the `f` prefix when adding an interpolation placeholder, which results in the braces being treated as literal text. Automatically adding the prefix keeps your interpolation working as intended.

**Type**: `boolean`
**Default**: `false`
**Scope**: window (applies to the whole VS Code window)

## Example

Suppose you type an opening brace `{` inside a plain string:

```python
label = "value: "
```

With the setting **enabled**, Pylance adds the `f` prefix automatically as you type `{`, turning the string into an f-string:

```python
label = f"value: {}"
```

With the setting **disabled**, the string keeps no prefix and the braces are treated as literal text rather than an interpolation placeholder.

## How to Change `python.analysis.autoFormatStrings`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.autoFormatStrings`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.autoFormatStrings": true
}
```

## When to Use It

- **Enable** if you frequently write f-strings and want the `f` prefix added automatically as you insert placeholders.
- **Keep disabled** if you prefer to control string prefixes manually, or if your codebase mixes many string types where automatic conversion would be unexpected.

## Related Settings

- [`python.analysis.autoSplitStrings`](python_analysis_autoSplitStrings.md) — adds quotes and continuation characters when you split a string across lines.
- [`python.analysis.completeFunctionParens`](python_analysis_completeFunctionParens.md) — adds parentheses to function completions.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

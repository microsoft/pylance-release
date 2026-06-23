# Understanding `python.analysis.autoSplitStrings` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.autoSplitStrings` setting controls whether Pylance automatically adds quotes and line-continuation characters when you split a string across multiple lines.

## What is `python.analysis.autoSplitStrings`?

When enabled and you press `Enter` in the middle of a string literal, Pylance automatically closes the string on the current line and reopens it on the next line, keeping the literal valid. This produces correctly quoted, implicitly concatenated string fragments instead of a broken, unterminated string.

This exists because manually splitting a long string is error-prone — you have to add a closing quote, a continuation, and a reopening quote yourself. Automating it keeps long strings readable and syntactically correct.

**Type**: `boolean`
**Default**: `true`
**Scope**: window (applies to the whole VS Code window)

## Example

Suppose your cursor (`|`) is inside a string and you press `Enter`:

```python
message = "first part |second part"
```

With the setting **enabled** (the default), Pylance closes the string on the current line and reopens it on the next, keeping the literal valid:

```python
message = "first part " \
    "second part"
```

With the setting **disabled**, pressing `Enter` leaves the string broken across two lines, producing an unterminated-string syntax error.

## How to Change `python.analysis.autoSplitStrings`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.autoSplitStrings`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.autoSplitStrings": false
}
```

## When to Use It

- **Keep enabled** (the default) if you want long strings to stay valid automatically when you break them across lines.
- **Disable** if you prefer to manage multi-line strings manually, for example when you rely on triple-quoted strings or specific formatting.

## Related Settings

- [`python.analysis.autoFormatStrings`](python_analysis_autoFormatStrings.md) — adds an `f` prefix when you insert a placeholder in a string.
- [`python.analysis.autoIndent`](python_analysis_autoIndent.md) — adjusts indentation automatically as you type.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

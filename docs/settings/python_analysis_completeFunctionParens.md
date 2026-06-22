# Understanding `python.analysis.completeFunctionParens` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.completeFunctionParens` setting controls whether Pylance adds parentheses when you accept a function or method completion.

## What is `python.analysis.completeFunctionParens`?

By default, when you accept a completion for a function or method, Pylance inserts only the name (for example `len`). With this setting enabled, Pylance instead inserts the name **and** a matching pair of parentheses, then places the cursor between them so you can start typing arguments immediately (for example `len(|)`).

This exists because many developers prefer to call a function the moment they select it, rather than typing the parentheses by hand. It is most useful if you frequently complete functions and want fewer keystrokes.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

## Example

With the setting **disabled** (the default), accepting the `print` completion inserts only the name:

```python
print
```

With the setting **enabled**, Pylance inserts the parentheses and places the cursor between them, ready for arguments (`|` marks the cursor position):

```python
print(|)
```

## How to Change `python.analysis.completeFunctionParens`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.completeFunctionParens`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.completeFunctionParens": true
}
```

## When to Use It

- **Enable** if you want function completions to be immediately callable and prefer to fill in arguments right away.
- **Keep disabled** if you often reference functions without calling them (for example passing a function as a callback), where extra parentheses would get in the way.

## Frequently Asked Questions

### Why weren't parentheses added in some completions?

Pylance deliberately skips parentheses in contexts where a call is not appropriate — inside `import` statements, type annotations, class names, and decorators.

### Does it work with auto-imported functions?

Yes. The setting applies to function and method completions in the completion list, including functions that are auto-imported when you accept the suggestion.

### How do I reference a function without calling it?

Keep the setting disabled, or delete the inserted parentheses after accepting the completion.

## Related Settings

- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md) — offers completions for symbols that are not yet imported.
- [`python.analysis.autoIndent`](python_analysis_autoIndent.md) — adjusts indentation automatically as you type.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

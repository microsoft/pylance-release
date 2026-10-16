# Understanding `python.analysis.supportAllPythonDocuments` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.supportAllPythonDocuments` setting extends Pylance's IntelliSense to Python content that appears outside of regular `.py` files.

## What is `python.analysis.supportAllPythonDocuments`?

By default, Pylance provides language features in Python files, notebooks, interactive input, terminals, and chat code blocks. Enable this setting to support other Python document types.

This exists to bring completions and related features to Python shown in non-file contexts.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

> **Note:** This is an experimental capability. If you enable it and notice instability, disable it to return to the standard behavior.

## How to Change `python.analysis.supportAllPythonDocuments`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.supportAllPythonDocuments`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.supportAllPythonDocuments": true
}
```

## When to Use It

- **Enable** if you need IntelliSense in other Python document types.
- **Keep disabled** (the default) for the standard set of supported Python document types.

## Related Settings

- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md) — offers completions for symbols that are not yet imported.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

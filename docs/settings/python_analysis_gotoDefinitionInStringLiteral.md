# Understanding `python.analysis.gotoDefinitionInStringLiteral` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.gotoDefinitionInStringLiteral` setting controls whether **Go to Definition** works on string literals that look like module names.

## What is `python.analysis.gotoDefinitionInStringLiteral`?

Module names sometimes appear inside string literals rather than in `import` statements — for example in dynamic imports, plugin registries, or framework configuration that references modules by name. When this setting is enabled, invoking **Go to Definition** (F12) on such a string navigates to the referenced module.

This exists because many Python frameworks identify modules and objects with strings, and being able to jump from those strings to the underlying module improves navigation in configuration-heavy codebases.

**Type**: `boolean`
**Default**: `true`
**Scope**: resource (can be set per workspace or folder)

## Example

Consider a module name referenced inside a string, such as a dynamic import:

```python
import importlib

mod = importlib.import_module("my_package.utils")
#                              ^ invoke Go to Definition (F12) here
```

With the setting **enabled** (the default), invoking **Go to Definition** on the `"my_package.utils"` string navigates to that module (for example `my_package/utils.py`).

With the setting **disabled**, **Go to Definition** does nothing on the string, because the text is treated as a plain literal rather than a module reference.

## How to Change `python.analysis.gotoDefinitionInStringLiteral`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.gotoDefinitionInStringLiteral`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.gotoDefinitionInStringLiteral": false
}
```

## When to Use It

- **Keep enabled** (the default) if you work with frameworks that reference modules by name in strings and want to navigate to them quickly.
- **Disable** if you find that strings are being interpreted as module references when you do not intend them to be.

## Related Settings

- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md) — offers completions for symbols that are not yet imported.
- [`python.analysis.indexing`](python_analysis_indexing.md) — builds the symbol index that powers navigation features.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

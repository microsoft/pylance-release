# Understanding `python.analysis.enableEditableInstalls` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.enableEditableInstalls` setting controls whether Pylance resolves packages that were installed in editable mode according to [PEP 660](https://peps.python.org/pep-0660/).

## What is `python.analysis.enableEditableInstalls`?

Editable installs (for example `pip install -e .`) let you import a package while still editing its source in place. PEP 660 defines how build backends expose those packages. When this setting is enabled, Pylance understands PEP 660 editable installs when you are using Python 3.13 or higher, so imports from editable packages resolve to your source and provide accurate completions, navigation, and type information.

**Type**: `boolean`
**Default**: `true`
**Scope**: machine (applies to your machine, not per workspace)

> **Note:** This is an experimental capability. If you encounter problems with editable-install resolution, you can disable this setting to revert to the previous behavior.

## How to Change `python.analysis.enableEditableInstalls`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.enableEditableInstalls`.
3. Check or uncheck the box.

### Using `settings.json`

```json
{
    "python.analysis.enableEditableInstalls": true
}
```

## When to Use It

- **Keep enabled** (the default) if you develop packages with editable installs on Python 3.13+ and want imports from them resolved to your source.
- **Disable** if you experience unexpected import-resolution behavior related to editable installs.

## Related Settings

- [`python.analysis.extraPaths`](python_analysis_extraPaths.md) — adds extra import search paths for packages that are not installed.
- [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md) — infers types from library source when stubs are unavailable.

## See Also

- [Working with Editable Installs](../howto/editable-installs.md) — how to make editable installs resolve correctly in Pylance.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

# Understanding `python.analysis.enableTroubleshootMissingImports` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.enableTroubleshootMissingImports` setting adds a Quick Fix that helps you diagnose why an import cannot be resolved.

## What is `python.analysis.enableTroubleshootMissingImports`?

When Pylance cannot resolve an import, the cause is often environmental — the package is not installed, or the wrong interpreter is selected. When this setting is enabled, Pylance offers a **Quick Fix** on the unresolved import that helps you troubleshoot these environment-related causes.

This exists to turn an unresolved-import error into actionable next steps, rather than leaving you to investigate the environment manually.

> **Note:** This Quick Fix requires the **Python Environments** extension to be installed and enabled.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

## How to Change `python.analysis.enableTroubleshootMissingImports`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.enableTroubleshootMissingImports`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.enableTroubleshootMissingImports": true
}
```

## When to Use It

- **Enable** if you frequently hit unresolved imports caused by environment or interpreter issues and want guided troubleshooting.
- **Keep disabled** (the default) if you do not have the Python Environments extension or prefer to resolve import issues manually.

## Related Settings

- [`python.analysis.extraPaths`](python_analysis_extraPaths.md) — adds import search paths for packages not installed in the environment.
- [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md) — infers types from library source when stubs are unavailable.

## See Also

- [Resolving Unresolved Imports](../howto/unresolved-imports.md) — how to diagnose and fix import errors.
- [Selecting Python Environments](../howto/python-environments.md) — how Pylance picks an interpreter.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

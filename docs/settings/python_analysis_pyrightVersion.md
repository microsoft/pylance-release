# Understanding `python.analysis.pyrightVersion` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.pyrightVersion` setting lets you pin the version of Pyright that Pylance uses to produce diagnostics.

## What is `python.analysis.pyrightVersion`?

Pylance is built on the Pyright type checker. This setting lets you select a specific Pyright version for diagnostics rather than the version bundled with your installed Pylance.

This is useful when you need diagnostics to match a particular Pyright release — for example, to align editor results with a Pyright version used in CI, or to validate behavior against a specific build.

> **Important:** This setting only takes effect when `python.analysis.diagnosticsSource` is set to `Pyright`.

**Type**: `string`
**Default**: `""` (use the bundled Pyright version)
**Scope**: resource (can be set per workspace or folder)
**Minimum supported version**: `1.1.397`

### Accepted values

The value can be either of the following:

- A **version string**, for example `1.1.397`.
- A **path** to a local `pyright-langserver.js` file. The referenced build must also be version `1.1.397` or higher.

## How to Change `python.analysis.pyrightVersion`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.pyrightVersion`.
3. Enter a version string or a path.

### Using `settings.json`

Pin to a published version:

```json
{
    "python.analysis.diagnosticsSource": "Pyright",
    "python.analysis.pyrightVersion": "1.1.397"
}
```

Use a local build:

```json
{
    "python.analysis.diagnosticsSource": "Pyright",
    "python.analysis.pyrightVersion": "/path/to/pyright-langserver.js"
}
```

## When to Use It

- **Set a version** when you need diagnostics to match a specific Pyright release, such as the one used in your continuous integration pipeline.
- **Leave empty** (the default) to use the Pyright version bundled with your Pylance installation.

## Related Settings

- The `python.analysis.diagnosticsSource` setting selects which engine produces diagnostics; `pyrightVersion` applies only when it is set to `Pyright`.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) — controls how strict diagnostics are.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

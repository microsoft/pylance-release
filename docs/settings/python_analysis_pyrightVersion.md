# Understanding `python.analysis.pyrightVersion` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.pyrightVersion` setting lets you pin the version of Pyright that Pylance uses to produce diagnostics.

## What is `python.analysis.pyrightVersion`?

Pylance is built on the Pyright type checker. This setting lets you select a specific Pyright version for diagnostics rather than the version bundled with your installed Pylance.

This is useful when you need diagnostics to match a particular Pyright release — for example, to align editor results with a Pyright version used in CI, or to validate behavior against a specific build.

> **Important:** This setting only takes effect when `python.analysis.diagnosticsSource` is set to `Pylance + Pyright`.

**Type**: `string`
**Default**: `""` (use the bundled Pyright version)
**Scope**: resource (can be set per workspace or folder)
**Minimum supported version**: `1.1.397`

### Accepted values

The value can be one of the following:

- A **version string**, for example `1.1.397`.
- A **path** to a local `pyright-langserver.js` file. The referenced build must also be version `1.1.397` or higher.
- `fromEnvironment`: Uses the version of the `pyright` package installed in the selected Python environment.

## How to Change `python.analysis.pyrightVersion`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.pyrightVersion`.
3. Enter a version string, a path, or `fromEnvironment`.

### Using `settings.json`

Pin to a published version:

```json
{
    "python.analysis.diagnosticsSource": "Pylance + Pyright",
    "python.analysis.pyrightVersion": "1.1.397"
}
```

Use a local build:

```json
{
    "python.analysis.diagnosticsSource": "Pylance + Pyright",
    "python.analysis.pyrightVersion": "/path/to/pyright-langserver.js"
}
```

Use the version installed in the selected Python environment:

Install your intended `pyright` version in the Python environment selected in VS Code, then use:

```json
{
    "python.analysis.diagnosticsSource": "Pylance + Pyright",
    "python.analysis.pyrightVersion": "fromEnvironment"
}
```

## When to Use It

- **Set a version** when you need diagnostics to match a specific Pyright release, such as the one used in your continuous integration pipeline.
- **Leave empty** (the default) to use the Pyright version bundled with your Pylance installation.

## Related Settings

- The `python.analysis.diagnosticsSource` setting selects which engine produces diagnostics; `pyrightVersion` applies only when it is set to `Pylance + Pyright`.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) — controls how strict diagnostics are.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

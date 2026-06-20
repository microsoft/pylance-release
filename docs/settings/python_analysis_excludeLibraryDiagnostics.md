# Understanding `python.analysis.excludeLibraryDiagnostics` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.excludeLibraryDiagnostics` setting suppresses diagnostics (errors, warnings, and hints) for library files while continuing to report them for the code you write.

## What is `python.analysis.excludeLibraryDiagnostics`?

When enabled, Pylance does not surface diagnostics for **library files** — such as the standard library, packages installed in `site-packages`, and bundled typeshed stubs — but still reports diagnostics for your own user-authored files.

This exists because third-party and standard library code is outside your control. When type checking is enabled, analysis of library code can produce diagnostics that you cannot fix and that distract from issues in your own project. Excluding them keeps the Problems panel focused on actionable findings.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

## How to Change `python.analysis.excludeLibraryDiagnostics`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.excludeLibraryDiagnostics`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.excludeLibraryDiagnostics": true
}
```

## When to Use It

- **Enable** if you use a stricter [`typeCheckingMode`](python_analysis_typeCheckingMode.md) and see diagnostics originating from installed libraries or stubs that you cannot act on.
- **Keep disabled** if you want full visibility into analysis of library code, for example when debugging stub-related issues.

## Related Settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) — controls how strict type checking is.
- [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md) — controls whether Pylance infers types from library source when stubs are missing.
- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md) — controls whether analysis covers only open files or the whole workspace.
- [`python.analysis.ignore`](python_analysis_ignore.md) — suppresses diagnostics for specific paths you choose.
- [`python.analysis.disableTaggedHints`](python_analysis_disableTaggedHints.md) — disables grayed-out / strike-through hint diagnostics.

## See Also

- [Workspace vs. Open Files Diagnostics](../howto/workspace-vs-open-files-diagnostics.md) — how Pylance decides which files to report on.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

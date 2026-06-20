# Understanding `python.analysis.disableTaggedHints` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.disableTaggedHints` setting controls whether Pylance shows hint diagnostics that render as grayed-out or strike-through text in the editor.

## What is `python.analysis.disableTaggedHints`?

Pylance uses **tagged hints** to communicate certain conditions visually rather than as conventional warnings:

- **Grayed-out (unnecessary) text** marks code that is unreachable or otherwise has no effect.
- **Strike-through (deprecated) text** marks the use of symbols that are marked deprecated.

When `disableTaggedHints` is enabled, Pylance stops emitting these tagged hint diagnostics, so the affected code is no longer dimmed or struck through.

This setting exists for developers who find the visual styling distracting, or whose other tooling conflicts with it, while still wanting the rest of Pylance's analysis.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

## Example

Consider code with an unreachable statement and a deprecated symbol:

```python
def f(x):
    return x
    print("done")   # unreachable
```

With the setting **disabled** (the default), Pylance grays out the unreachable `print("done")` line, and renders deprecated symbols with strike-through styling.

With the setting **enabled**, Pylance stops emitting these tagged hints, so the unreachable line is no longer dimmed and deprecated symbols are no longer struck through. The text appears with normal styling.

## How to Change `python.analysis.disableTaggedHints`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.disableTaggedHints`.
3. Check the box to disable tagged hints.

### Using `settings.json`

```json
{
    "python.analysis.disableTaggedHints": true
}
```

## When to Use It

- **Enable** if you do not want unreachable code grayed out or deprecated symbols struck through.
- **Keep disabled** (the default) if you find the visual cues helpful for spotting dead code and deprecated APIs.

## Related Settings

- [`python.analysis.typeEvaluation.enableReachabilityAnalysis`](python_analysis_typeEvaluation_enableReachabilityAnalysis.md) — controls detection of unreachable code that drives the grayed-out hint.
- [`python.analysis.typeEvaluation.deprecateTypingAliases`](python_analysis_typeEvaluation_deprecateTypingAliases.md) — affects which symbols are reported as deprecated.
- [`python.analysis.excludeLibraryDiagnostics`](python_analysis_excludeLibraryDiagnostics.md) — suppresses diagnostics in library files.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

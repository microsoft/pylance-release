# Understanding `python.analysis.disableTaggedHints` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

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

A common reason to disable tagged hints is a defensive runtime check that static analysis considers unreachable. Given a parameter annotated as `int`, Pylance narrows `value` to `int` and treats the validation branch as dead code:

```python
def process(value: int) -> None:
    if not isinstance(value, int):
        raise TypeError("value must be an int")   # grayed out as unreachable
    ...
```

With the setting **disabled** (the default), Pylance grays out the `raise` line, and renders deprecated symbols with strike-through styling.

With the setting **enabled**, Pylance stops emitting these tagged hints, so the defensive `raise` keeps normal styling and deprecated symbols are no longer struck through.

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

- **Enable** if you write defensive runtime checks (for example `isinstance` validation) that static analysis flags as unreachable and you do not want them grayed out, or if you find the strike-through styling on deprecated symbols distracting.
- **Keep disabled** (the default) if you find the visual cues helpful for spotting dead code and deprecated APIs.

## Frequently Asked Questions

### Does disabling tagged hints hide my errors and warnings?

No. It only suppresses the grayed-out (unreachable) and strike-through (deprecated) visual hints. Regular diagnostics such as type errors and warnings still appear.

### Why is my code grayed out even though it runs at runtime?

Static analysis narrows types and can conclude a branch is unreachable (for example a runtime `isinstance` check on an already-typed value). Enable this setting to stop the hint, or adjust your type annotations.

### Can I disable tagged hints for a single line or file?

No. The setting is resource-scoped (workspace or folder); there is no per-line toggle.

## Related Settings

- [`python.analysis.typeEvaluation.enableReachabilityAnalysis`](python_analysis_typeEvaluation_enableReachabilityAnalysis.md) — controls detection of unreachable code that drives the grayed-out hint.
- [`python.analysis.typeEvaluation.deprecateTypingAliases`](python_analysis_typeEvaluation_deprecateTypingAliases.md) — affects which symbols are reported as deprecated.
- [`python.analysis.excludeLibraryDiagnostics`](python_analysis_excludeLibraryDiagnostics.md) — suppresses diagnostics in library files.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

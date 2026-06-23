# Understanding `python.analysis.displayEnglishDiagnostics` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.displayEnglishDiagnostics` setting forces Pylance to display diagnostic messages in English, regardless of VS Code's configured display language.

## What is `python.analysis.displayEnglishDiagnostics`?

By default, Pylance localizes its diagnostic messages to match the VS Code display language. When `displayEnglishDiagnostics` is enabled, diagnostics are always shown in English even if the rest of the VS Code UI is localized to another language.

This exists primarily to make diagnostics easier to search and share. English messages are easier to look up online, paste into issue reports, and match against documentation, while the rest of your editor stays in your preferred language.

**Type**: `boolean`
**Default**: `false`
**Scope**: resource (can be set per workspace or folder)

## Example

Suppose VS Code's display language is set to a non-English locale and your code has an undefined name:

```python
print(value)   # `value` is not defined
```

With the setting **disabled** (the default), the diagnostic for this line is localized to match your VS Code display language.

With the setting **enabled**, the same diagnostic is always shown in English (for example, `"value" is not defined`), even though the rest of the VS Code UI stays in your chosen language. This makes the message easier to search for or paste into a bug report.

## How to Change `python.analysis.displayEnglishDiagnostics`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.displayEnglishDiagnostics`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.displayEnglishDiagnostics": true
}
```

## When to Use It

- **Enable** if you use a localized VS Code but want diagnostics in English to search for them online or include them in bug reports.
- **Keep disabled** if you prefer diagnostics localized to match the rest of your editor.

## Related Settings

- [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md) — customizes the severity of individual diagnostics.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) — controls how many diagnostics are produced.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

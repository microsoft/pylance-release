# Understanding `python.analysis.autoTranslateDocstrings` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.autoTranslateDocstrings` setting controls whether Pylance automatically translates docstrings shown in hover tooltips into your preferred language using GitHub Copilot.

## What is `python.analysis.autoTranslateDocstrings`?

When you hover over a symbol, Pylance shows its docstring. With this setting enabled, Pylance uses GitHub Copilot to translate that docstring into your preferred language before displaying it. The target language is determined by the `github.copilot.chat.localeOverride` setting.

This exists to make library documentation more accessible for developers who prefer to read docstrings in a language other than the one the library author wrote.

> **Note:** Enabling this feature can make hover tooltips appear significantly slower, because Pylance must call GitHub Copilot to perform the translation before showing the tooltip.

**Type**: `boolean`
**Default**: `false`
**Scope**: window (applies to the whole VS Code window)

## Example

Suppose a library function has an English docstring and you have set `github.copilot.chat.localeOverride` to another language (for example, `"ja"` for Japanese).

With the setting **disabled** (the default), hovering over the function shows the docstring in its original language:

```text
Return the sum of a list of numbers.
```

With the setting **enabled**, Pylance uses GitHub Copilot to translate the same docstring into your preferred language before displaying it in the hover, while the source code itself is unchanged.

## How to Change `python.analysis.autoTranslateDocstrings`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.autoTranslateDocstrings`.
3. Check the box to enable it.

### Using `settings.json`

```json
{
    "python.analysis.autoTranslateDocstrings": true,
    "github.copilot.chat.localeOverride": "ja"
}
```

Set `github.copilot.chat.localeOverride` to the language you want docstrings translated into.

## When to Use It

- **Enable** if you want hover docstrings translated into your preferred language and can accept slower hovers.
- **Keep disabled** if you prefer the original docstring text or want hovers to appear as fast as possible.

## Requirements

- The **GitHub Copilot Chat** extension must be installed and enabled.

## Frequently Asked Questions

### I enabled it but docstrings are not translated. Why?

Translation requires the **GitHub Copilot Chat** extension, and the target language is taken from `github.copilot.chat.localeOverride`. If that setting is unset, or already matches the docstring's language, you will not see a change.

### Why are hover tooltips slower now?

When the setting is enabled, Pylance calls GitHub Copilot to translate the docstring before showing the hover, which adds noticeable latency.

### Does it modify my source code?

No. Only the text shown in the hover tooltip is translated; the docstring in your source is unchanged.

## Related Settings

- [`python.analysis.aiCodeActions`](python_analysis_aiCodeActions.md) — other AI-assisted features that use GitHub Copilot.
- [`python.analysis.supportRestructuredText`](python_analysis_supportRestructuredText.md) — controls reStructuredText rendering in docstrings.

## See Also

- [Using Pylance with GitHub Copilot](../howto/copilot-pylance-workflow.md) — how Pylance and Copilot work together.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

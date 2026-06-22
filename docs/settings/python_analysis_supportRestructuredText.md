# Understanding `python.analysis.supportRestructuredText` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.supportRestructuredText` setting controls whether Pylance renders reStructuredText (reST) formatting in docstrings.

## What is `python.analysis.supportRestructuredText`?

Many Python libraries — including much of the standard library — write their docstrings in reStructuredText, the markup language used by Sphinx. When this setting is enabled, Pylance interprets that markup and renders docstrings with proper formatting (such as parameter lists, code samples, and emphasis) in hover tooltips and completion details, instead of showing the raw markup.

This exists so documentation displayed inline reads cleanly. It is a preview feature, so its rendering behavior may continue to evolve.

**Type**: `boolean`
**Default**: `true`
**Scope**: window (applies to the whole VS Code window)

## Example

Many docstrings use reStructuredText field markup such as:

```text
:param name: the user's name
:returns: a greeting string
```

With the setting **enabled** (the default), hovering over the symbol renders this as a formatted parameter and return list rather than raw markup.

With the setting **disabled**, the hover shows the raw text, including the `:param:` and `:returns:` markers, exactly as written in the source.

## How to Change `python.analysis.supportRestructuredText`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.supportRestructuredText`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.supportRestructuredText": false
}
```

## When to Use It

- **Keep enabled** (the default) if you want reStructuredText docstrings rendered as formatted documentation in hovers and completions.
- **Disable** if you prefer to see raw docstring text, or if rendering produces unexpected results for the libraries you use.

## Frequently Asked Questions

### Why isn't my docstring rendered as formatted text?

This is a preview feature, so not every reStructuredText construct is supported, and the docstring must actually use reST markup. Docstrings written in other styles are not converted.

### Is it enabled by default?

Yes. The default is `true`.

### Does it affect non-reStructuredText docstrings?

The feature targets reStructuredText markup. Docstrings that do not use reST are shown as-is.

## Related Settings

- [`python.analysis.autoTranslateDocstrings`](python_analysis_autoTranslateDocstrings.md) — translates hover docstrings using GitHub Copilot.
- [`python.analysis.aiCodeActions`](python_analysis_aiCodeActions.md) — includes an action to generate reStructuredText docstrings.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

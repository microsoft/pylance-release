# Understanding `python.analysis.enableColorPicker` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.enableColorPicker` setting controls whether Pylance shows an inline color picker for hexadecimal color strings in your Python code.

## What is `python.analysis.enableColorPicker`?

When enabled, Pylance recognizes color strings in the `#RRGGBB` and `#RRGGBBAA` formats and displays a color swatch next to them. Selecting the swatch opens VS Code's color picker so you can preview and adjust the color visually; the edited value is written back into the string.

This exists to make working with colors more convenient — for example when defining theme values, plot colors, or UI constants — without having to compute hex values by hand.

**Type**: `boolean`
**Default**: `true`
**Scope**: resource (can be set per workspace or folder)

## Example

Consider hexadecimal color strings in your code:

```python
BACKGROUND = "#1e1e1e"
ACCENT = "#ff8800cc"   # #RRGGBBAA is also recognized
```

With the setting **enabled** (the default), Pylance shows a color swatch next to each of these strings; clicking the swatch opens VS Code's color picker and writes your adjusted value back into the string.

With the setting **disabled**, no swatch appears and the strings render as plain text.

## How to Change `python.analysis.enableColorPicker`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.enableColorPicker`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.enableColorPicker": false
}
```

## When to Use It

- **Keep enabled** (the default) if you work with hex color values and want to preview or edit them visually.
- **Disable** if you do not use hex colors, or if the swatches add visual noise to your code.

## Related Settings

- [`python.analysis.inlayHints.variableTypes`](python_analysis_inlayHints_variableTypes.md) — another inline editor aid that displays inferred types.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

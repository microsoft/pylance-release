# Understanding `python.analysis.aiCodeActions` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.aiCodeActions` setting enables or disables Pylance's AI-assisted Quick Fixes and code actions, which use GitHub Copilot to help you write and modify code.

## What is `python.analysis.aiCodeActions`?

Pylance offers a set of code actions that delegate part of the work to GitHub Copilot. Instead of a single on/off switch, `aiCodeActions` is an **object** whose properties let you enable each AI-assisted action independently.

> **Note:** AI-assisted code actions require the **GitHub Copilot Chat** extension to be installed and enabled.

**Type**: `object`
**Scope**: resource (can be set per workspace or folder)

### Available actions and defaults

| Property                       | Default | What it does                                                                      |
| ------------------------------ | ------- | --------------------------------------------------------------------------------- |
| `implementAbstractClasses`     | `true`  | Generates implementations for inherited abstract methods.                         |
| `generateSymbol`               | `true`  | Generates a symbol (class, function, or variable) that does not yet exist.        |
| `convertFormatString`          | `true`  | Converts string concatenation into an f-string or `format()` call.                |
| `generateDocstring`            | `false` | Generates a reStructuredText docstring. Triggered from inside an empty docstring. |
| `convertLambdaToNamedFunction` | `false` | Converts a lambda expression into a named function.                               |

If you set `aiCodeActions` at all, the object you provide replaces the default object, so include every action you want enabled.

## Example

With `convertFormatString` enabled, invoking the Quick Fix (the lightbulb) on string concatenation offers to rewrite it as an f-string.

Before:

```python
greeting = "Hello, " + name + "!"
```

After applying the action:

```python
greeting = f"Hello, {name}!"
```

The other actions work the same way — each appears as a Quick Fix in the relevant context (for example, `implementAbstractClasses` on a class that inherits unimplemented abstract methods, or `generateDocstring` from inside an empty docstring).

## How to Change `python.analysis.aiCodeActions`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.aiCodeActions`.
3. Select **Edit in settings.json** to adjust individual properties.

### Using `settings.json`

Enable all available AI-assisted actions:

```json
{
    "python.analysis.aiCodeActions": {
        "implementAbstractClasses": true,
        "generateSymbol": true,
        "convertFormatString": true,
        "generateDocstring": true,
        "convertLambdaToNamedFunction": true
    }
}
```

Disable AI-assisted actions entirely:

```json
{
    "python.analysis.aiCodeActions": {}
}
```

You can also turn off **all** of VS Code's AI features at once with the built-in `chat.disableAIFeatures` setting, which disables these Pylance AI-assisted actions along with the rest of Copilot:

```json
{
    "chat.disableAIFeatures": true
}
```

## When to Use It

- **Enable specific actions** that fit your workflow — for example, keep `implementAbstractClasses` on if you frequently subclass abstract base classes.
- **Disable** (set to `{}`) if you do not use GitHub Copilot, or prefer Pylance to offer only its non-AI code actions.

## Frequently Asked Questions

### Why don't the AI code actions appear?

They require the **GitHub Copilot Chat** extension to be installed and enabled. Also confirm the specific action is enabled and that you invoke the Quick Fix (lightbulb) in the matching context (for example, `implementAbstractClasses` only appears on a class with unimplemented inherited abstract methods).

### Which actions are enabled by default?

`implementAbstractClasses`, `generateSymbol`, and `convertFormatString` are on by default. `generateDocstring` and `convertLambdaToNamedFunction` are off by default.

### I set one action and the others stopped working. Why?

The value you provide **replaces** the default object rather than merging with it. Include every action you want enabled in your `settings.json` entry.

### How do I turn off all AI-assisted actions?

Set the value to an empty object: `"python.analysis.aiCodeActions": {}`. To disable every VS Code AI feature (not just Pylance's), set `"chat.disableAIFeatures": true` instead.

## Related Settings

- [`python.analysis.generateWithTypeAnnotation`](python_analysis_generateWithTypeAnnotation.md) — controls whether generated code includes type annotations.
- [`python.analysis.autoTranslateDocstrings`](python_analysis_autoTranslateDocstrings.md) — translates hover docstrings using GitHub Copilot.
- [`python.analysis.supportRestructuredText`](python_analysis_supportRestructuredText.md) — renders reStructuredText docstrings, including those generated by `generateDocstring`.

## See Also

- [Using Pylance with GitHub Copilot](../howto/copilot-pylance-workflow.md) — how Pylance and Copilot work together.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

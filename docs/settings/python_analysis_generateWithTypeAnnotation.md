# Understanding `python.analysis.generateWithTypeAnnotation` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.generateWithTypeAnnotation` setting controls whether Pylance includes type annotations when it generates code.

## What is `python.analysis.generateWithTypeAnnotation`?

When Pylance generates code — for example through its AI-assisted code actions — this setting determines whether the generated functions, parameters, and variables include type annotations.

The effective default depends on your type checking mode:

- When [`typeCheckingMode`](python_analysis_typeCheckingMode.md) is `"off"`, the effective default is `false` (no annotations), because a project that does not type check usually does not need them.
- For any other type checking mode, the effective default is `true` (annotations included), to keep generated code consistent with a type-checked project.

Setting `generateWithTypeAnnotation` explicitly overrides this behavior regardless of the type checking mode.

**Type**: `boolean`
**Default**: `false` (see the mode-dependent behavior above)
**Scope**: resource (can be set per workspace or folder)

## Example

When Pylance generates a function, this setting determines whether the result includes type annotations.

With the setting **disabled**, generated code omits annotations:

```python
def add(a, b):
    return a + b
```

With the setting **enabled**, the generated code includes parameter and return type annotations:

```python
def add(a: int, b: int) -> int:
    return a + b
```

## How to Change `python.analysis.generateWithTypeAnnotation`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.generateWithTypeAnnotation`.
3. Check or uncheck the box.

### Using `settings.json`

```json
{
    "python.analysis.generateWithTypeAnnotation": true
}
```

## When to Use It

- **Set to `true`** if you want generated code to always include type annotations, even when type checking is off.
- **Set to `false`** if you prefer generated code without annotations, for example in scripts or notebooks where you do not use type checking.

## Related Settings

- [`python.analysis.aiCodeActions`](python_analysis_aiCodeActions.md) — enables the AI-assisted code actions that generate code.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) — determines the mode-dependent default for this setting.

## See Also

- [Using Pylance with GitHub Copilot](../howto/copilot-pylance-workflow.md) — how Pylance and Copilot work together.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

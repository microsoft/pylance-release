# Understanding `python.analysis.inlayHints.functionReturnTypes` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and inlay hints that help you understand your code at a glance.

The `python.analysis.inlayHints.functionReturnTypes` setting controls whether Pylance displays inferred return types inline after function definitions.

## What `python.analysis.inlayHints.functionReturnTypes` does

When enabled, Pylance shows the return type of functions that do not already have an explicit return type annotation. The hint appears directly after the function signature in the editor.

The default value is `false`.

```json
"python.analysis.inlayHints.functionReturnTypes": false
```

### Example

Consider the following code:

```python
def greet(name):
    return f"Hello, {name}!"

def add_numbers(a, b):
    return a + b
```

Without inlay hints, you need to hover or navigate to see what these functions return. With `python.analysis.inlayHints.functionReturnTypes` set to `true`, Pylance displays:

```python
def greet(name) -> str:
    return f"Hello, {name}!"

def add_numbers(a, b) -> int:
    return a + b
```

The hints (`-> str`, `-> int`) appear inline in the editor, showing the inferred return type at a glance.

## Accepted values

- `true`: Enables inlay hints for function return types.
- `false` (default): Disables inlay hints for function return types.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.inlayHints.functionReturnTypes`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.inlayHints.functionReturnTypes": true
    ```

## Inserting the return type into your code

You can double-click on a return type inlay hint, and Pylance will insert the actual type annotation into your code. For example, double-clicking `-> str` on `def greet(name)` changes it to:

```python
def greet(name) -> str:
    return f"Hello, {name}!"
```

This makes it easy to adopt explicit annotations incrementally.

## When hints are not shown

Pylance may omit the return type inlay hint in certain cases:

- **Explicit annotations**: If the function already has a return type annotation, no hint is needed.
- **Obvious return types**: Pylance may skip hints for functions returning literals or built-in types in simple cases where the return type is readily apparent.

## Related settings

- [`python.analysis.inlayHints.variableTypes`](python_analysis_inlayHints_variableTypes.md)
    - Shows inferred types of variables.
- [`python.analysis.inlayHints.callArgumentNames`](python_analysis_inlayHints_callArgumentNames.md)
    - Shows parameter names at call sites.
- [`python.analysis.inlayHints.pytestParameters`](python_analysis_inlayHints_pytestParameters.md)
    - Shows inferred types of pytest fixture parameters.

## Frequently asked questions

### Q: Will enabling function return type inlay hints affect performance?

**A:** Generally, enabling this feature has minimal impact on performance. In very large projects there might be a slight overhead. If you experience slowdowns, you can disable the feature.

### Q: The inlay hint suggests a return type that causes errors when inserted. What should I do?

**A:** In some cases, especially when a function returns an instance of a class defined within the same scope, inserting the hint may produce a forward reference issue. Pylance handles this by using stringified types (e.g., `-> "MyClass"`). Adjust the annotation manually if needed.

### Q: Can I customize the appearance of inlay hints?

**A:** Yes, Visual Studio Code lets you customize the color and font style of inlay hints through `editor.inlayHints.*` settings and color theme overrides.

### Q: Do inlay hints modify my source code?

**A:** No. Inlay hints are visual annotations in the editor. They do not alter your source files unless you explicitly double-click to insert them.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

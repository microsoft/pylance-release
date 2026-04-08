# Understanding `python.analysis.inlayHints.callArgumentNames` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and inlay hints that help you understand your code at a glance.

The `python.analysis.inlayHints.callArgumentNames` setting controls whether Pylance displays parameter names inline at function call sites so you can see which argument maps to which parameter.

## What `python.analysis.inlayHints.callArgumentNames` does

When enabled, Pylance shows the parameter name before each argument in a function call. This makes it easier to understand what each argument represents without navigating to the function definition.

The default value is `"off"`.

```json
"python.analysis.inlayHints.callArgumentNames": "off"
```

### Example

Consider the following code:

```python
def create_user(name: str, age: int, active: bool):
    ...

create_user("Alice", 30, True)
```

Without inlay hints, it is not immediately clear what `True` represents. With `python.analysis.inlayHints.callArgumentNames` set to `"all"`, Pylance displays:

```python
create_user(name="Alice", age=30, active=True)
```

The hints (`name=`, `age=`, `active=`) appear inline in the editor, helping you understand the purpose of each argument at a glance.

## Accepted values

- `"off"` (default)
    - Disables call argument name inlay hints.
- `"partial"`
    - Shows hints for positional-or-keyword arguments while ignoring positional-only and keyword-only arguments.
- `"all"`
    - Shows hints for positional-or-keyword and positional-only arguments. Keyword-only arguments are excluded because the caller already writes the name.

### Difference between `"partial"` and `"all"`

`"partial"` skips positional-only parameters (those before a `/` in the function signature) in addition to keyword-only parameters. `"all"` includes positional-only parameters as well, only excluding keyword-only parameters.

For example:

```python
def example(pos_only: int, /, regular: str, *, kw_only: bool):
    ...

example(1, "hello", kw_only=True)
```

- With `"partial"`: Pylance shows `regular=` but not hints for `1` (positional-only) or `kw_only=True` (already named).
- With `"all"`: Pylance shows `pos_only=` and `regular=` but not `kw_only=True` (already named).

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.inlayHints.callArgumentNames`.
- Select the desired value from the dropdown.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.inlayHints.callArgumentNames": "partial"
    ```

## When to use each value

### Use `"off"` when you prefer a clean editor

`"off"` is the default and keeps the editor free of extra annotations. This is a good choice when you are already familiar with the functions you call or when the argument names are self-evident.

### Use `"partial"` for a balance between clarity and noise

`"partial"` shows hints where they are most helpful — at regular positional-or-keyword arguments — without adding hints where the meaning is already clear.

### Use `"all"` for maximum visibility

`"all"` adds hints even for positional-only arguments. This can be helpful in codebases that use positional-only parameters frequently.

## Related settings

- [`python.analysis.inlayHints.variableTypes`](python_analysis_inlayHints_variableTypes.md)
    - Shows inferred types of variables.
- [`python.analysis.inlayHints.functionReturnTypes`](python_analysis_inlayHints_functionReturnTypes.md)
    - Shows return types of functions.
- [`python.analysis.inlayHints.pytestParameters`](python_analysis_inlayHints_pytestParameters.md)
    - Shows inferred types of pytest fixture parameters.

## Frequently asked questions

### Q: Will enabling call argument name inlay hints affect performance?

**A:** Enabling this feature may have a minimal impact on performance, especially in large codebases. If you experience slowdowns, consider setting it to `"off"`.

### Q: Can I customize the appearance of inlay hints?

**A:** Yes, Visual Studio Code lets you customize the color and font style of inlay hints through `editor.inlayHints.*` settings and color theme overrides.

### Q: Do inlay hints modify my source code?

**A:** No. Inlay hints are visual annotations in the editor. They do not alter your source files.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

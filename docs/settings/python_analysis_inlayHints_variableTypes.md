# Understanding `python.analysis.inlayHints.variableTypes` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and inlay hints that help you understand your code at a glance.

The `python.analysis.inlayHints.variableTypes` setting controls whether Pylance displays inferred types for variables that do not already have an explicit type annotation.

## What `python.analysis.inlayHints.variableTypes` does

When enabled, Pylance shows the inferred type of variables inline in the editor. This is especially useful in a dynamically typed language like Python, where variable types are not always explicitly declared.

The default value is `false`.

```json
"python.analysis.inlayHints.variableTypes": false
```

### Example

Consider the following code:

```python
users = get_all_users()
active = [u for u in users if u.is_active]
```

Without inlay hints, you need to hover or navigate to see what types these variables hold. With `python.analysis.inlayHints.variableTypes` set to `true`, Pylance displays:

```python
users: list[User] = get_all_users()
active: list[User] = [u for u in users if u.is_active]
```

The hints (`: list[User]`) appear inline, showing the inferred type at a glance.

## Accepted values

- `true`: Enables variable type inlay hints.
- `false` (default): Disables variable type inlay hints.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.inlayHints.variableTypes`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.inlayHints.variableTypes": true
    ```

## When hints are not shown

Pylance omits variable type inlay hints in certain cases:

- **Literal and constant assignments**: When the type is obvious from the assigned value, such as `count = 10` or `name = "Alice"`, Pylance skips the hint because the type is already clear.
- **Explicit type annotations**: If a variable already has a type annotation (e.g., `items: list[str] = ["apple"]`), no hint is needed.

## When to enable variable type inlay hints

### Enhancing code readability

In codebases without explicit type annotations, variable type inlay hints provide immediate visibility into the types Pylance infers. This is especially helpful in complex or unfamiliar code.

### Debugging and error prevention

If Pylance infers a different type than you expected, the inlay hint can alert you to potential bugs or logic errors early in development.

### Learning

For developers learning Python or working with new libraries, inlay hints serve as inline documentation that reveals types of variables and return values.

## Performance considerations

Generating variable type inlay hints requires additional analysis. In very large projects this may noticeably affect editor responsiveness. If you experience slowdowns, consider disabling this feature.

## Related settings

- [`python.analysis.inlayHints.functionReturnTypes`](python_analysis_inlayHints_functionReturnTypes.md)
    - Shows return types of functions.
- [`python.analysis.inlayHints.callArgumentNames`](python_analysis_inlayHints_callArgumentNames.md)
    - Shows parameter names at call sites.
- [`python.analysis.inlayHints.pytestParameters`](python_analysis_inlayHints_pytestParameters.md)
    - Shows inferred types of pytest fixture parameters.

## Frequently asked questions

### Q: Why don't I see inlay hints for some variables?

**A:** Pylance omits hints when the type is obvious from a literal or constant assignment (e.g., `x = 42`, `name = "Alice"`). Variables with explicit type annotations also do not receive hints.

### Q: Can I customize which variables display inlay hints?

**A:** The setting applies globally — it enables or disables variable type inlay hints for the entire workspace. Selective customization for specific variables is not available.

### Q: Will enabling variable type inlay hints affect performance?

**A:** Generating hints requires additional processing. In large projects this may impact editor responsiveness. If you notice slowdowns, you can disable the feature.

### Q: Do inlay hints modify my source code?

**A:** No. Inlay hints are visual annotations in the editor. They do not alter your source files.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

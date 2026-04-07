# Understanding `python.analysis.typeEvaluation.enableTypeIgnoreComments` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.enableTypeIgnoreComments` setting controls whether Pylance recognizes `# type: ignore` comments to suppress type checking errors.

## What `python.analysis.typeEvaluation.enableTypeIgnoreComments` does

[PEP 484](https://peps.python.org/pep-0484/) defines the `# type: ignore` comment as a way to suppress type checking errors on a specific line. When this setting is enabled, Pylance respects those comments and suppresses the corresponding diagnostics. When disabled, Pylance reports all type errors regardless of `# type: ignore` comments.

The default value is `true`.

```json
"python.analysis.typeEvaluation.enableTypeIgnoreComments": true
```

**Note**: This setting does not affect `# pyright: ignore` comments. Those are always recognized by Pylance.

### Example

```python
def greet(name: int) -> None:
    print(name)

greet("hello")  # type: ignore
```

- With `true` (default): Pylance suppresses the type error on that line.
- With `false`: Pylance reports the type error even though `# type: ignore` is present.

## Accepted values

- `true` (default): Respect `# type: ignore` comments and suppress diagnostics on annotated lines.
- `false`: Ignore `# type: ignore` comments and report all type errors.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.enableTypeIgnoreComments`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.enableTypeIgnoreComments": false
    ```

## When to disable this setting

### Enforcing strict type checking discipline

Some teams prefer to disallow `# type: ignore` entirely, requiring developers to fix every type error rather than suppress it. Setting this to `false` makes all `# type: ignore` comments ineffective, revealing errors that were previously hidden.

### Code review and maintenance

Over time, `# type: ignore` comments can accumulate and mask real bugs. Disabling them forces a cleanup pass and ensures all type issues are visible.

### Keeping the default

In most projects, leaving this at `true` is practical. `# type: ignore` provides a useful escape hatch for cases where the type checker cannot model the code correctly, such as dynamic patterns or interactions with untyped libraries.

## Alternatives to `# type: ignore`

If you disable `# type: ignore` support, you can still address type errors through:

- **Adding type annotations**: Provide explicit types so Pylance can check correctly.
- **Using `typing.cast`**: Explicitly cast a value to the expected type.
- **Using assertions**: Narrow types with `assert isinstance(...)`.
- **Using `# pyright: ignore`**: This comment is always recognized regardless of the `enableTypeIgnoreComments` setting.

## Frequently asked questions

### Q: Does disabling this setting affect other tools like mypy?

**A:** No. This setting only affects Pylance's behavior. Other type checkers like mypy have their own configuration for `# type: ignore` handling.

### Q: What is the difference between `# type: ignore` and `# pyright: ignore`?

**A:** `# type: ignore` is defined by PEP 484 and is recognized by most type checkers. `# pyright: ignore` is Pyright-specific and is always recognized by Pylance regardless of this setting. `# pyright: ignore` also supports error codes for more targeted suppression (e.g., `# pyright: ignore[reportGeneralClassIssues]`).

### Q: Can I disable `# type: ignore` for specific files only?

**A:** The setting applies globally to the workspace. You can use a `pyrightconfig.json` with `include`/`exclude` to scope the configuration to specific directories.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

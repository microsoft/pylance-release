# Understanding `python.analysis.typeEvaluation.deprecateTypingAliases` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.deprecateTypingAliases` setting controls whether Pylance flags deprecated typing aliases from the `typing` module, such as `typing.List`, `typing.Dict`, and `typing.Tuple`.

## What `python.analysis.typeEvaluation.deprecateTypingAliases` does

[PEP 585](https://peps.python.org/pep-0585/) introduced support for using standard collection types directly as generics (e.g., `list[int]` instead of `typing.List[int]`), making the old `typing` module aliases unnecessary starting with Python 3.9. When this setting is enabled, Pylance treats those aliases as deprecated and reports diagnostics for their use.

The default value is `false`.

```json
"python.analysis.typeEvaluation.deprecateTypingAliases": false
```

This setting applies only when `pythonVersion` is 3.9 or newer.

### Example

With the setting enabled:

```python
from typing import List, Dict

# Pylance flags these as deprecated
def process(items: List[int]) -> Dict[str, int]:
    ...
```

Updated to modern syntax:

```python
# No warnings — uses built-in generic types
def process(items: list[int]) -> dict[str, int]:
    ...
```

## Accepted values

- `true`: Treat `typing` module aliases as deprecated and report diagnostics.
- `false` (default): Do not flag deprecated typing aliases.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.deprecateTypingAliases`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.deprecateTypingAliases": true
    ```

You can also set this in `pyrightconfig.json`:

```json
{
    "typeEvaluation": {
        "deprecateTypingAliases": true
    }
}
```

Or in `pyproject.toml`:

```toml
[tool.pyright.typeEvaluation]
deprecateTypingAliases = true
```

## Common deprecated aliases and their replacements

| Deprecated alias     | Replacement |
| -------------------- | ----------- |
| `typing.List`        | `list`      |
| `typing.Dict`        | `dict`      |
| `typing.Tuple`       | `tuple`     |
| `typing.Set`         | `set`       |
| `typing.FrozenSet`   | `frozenset` |
| `typing.Type`        | `type`      |
| `typing.Union[X, Y]` | `X \| Y`    |

## When to enable this setting

### Modernizing a codebase

Enable this setting when your project targets Python 3.9+ and you want to migrate away from the old `typing` module aliases. The diagnostics help you find and update all occurrences.

### Enforcing team standards

If your team has decided to use the modern syntax exclusively, enabling this setting ensures that deprecated aliases are flagged during development.

### Keeping the default

If your project needs to support Python 3.8 or earlier, or you are not ready to migrate, leave this at `false`.

## Frequently asked questions

### Q: Will using deprecated typing aliases cause my code to break?

**A:** No. The aliases still work at runtime. This setting only adds diagnostics to encourage migration to the newer syntax.

### Q: Does this setting affect `typing.Union`?

**A:** Yes. When `pythonVersion` is 3.10 or newer, `typing.Union[X, Y]` is flagged in favor of `X | Y`.

### Q: Can I selectively disable warnings for specific aliases?

**A:** No. The setting applies to all deprecated typing aliases collectively.

## Related settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.
- [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md)
    - Fine-grained control over individual diagnostic rule severities.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

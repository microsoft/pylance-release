# Understanding `python.analysis.typeEvaluation.strictParameterNoneValue` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.strictParameterNoneValue` setting controls whether Pylance requires explicit `Optional` annotations for parameters with a default value of `None`.

## What `python.analysis.typeEvaluation.strictParameterNoneValue` does

[PEP 484](https://peps.python.org/pep-0484/) originally allowed type checkers to implicitly treat a parameter with a default value of `None` as `Optional`. That recommendation was later updated to require the `Optional` type to be explicit. This setting controls which behavior Pylance uses.

The default value is `true`.

```json
"python.analysis.typeEvaluation.strictParameterNoneValue": true
```

### Example

```python
def greet(name: str = None):
    ...
```

- With `true` (default): Pylance reports an error — `None` cannot be assigned to `str`. You must write `name: str | None = None` or `name: Optional[str] = None`.
- With `false`: Pylance implicitly treats `name` as `Optional[str]` and reports no error.

## Accepted values

- `true` (default): Require explicit `Optional` or `| None` when a parameter defaults to `None`.
- `false`: Implicitly treat parameters with `None` defaults as `Optional`.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.strictParameterNoneValue`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.strictParameterNoneValue": false
    ```

## When to change this setting

### Keep `true` (default) for modern codebases

The default follows the current PEP 484 recommendation: be explicit about `Optional`. This improves code clarity and makes the annotation match the actual contract.

```python
# Preferred — explicit Optional
def greet(name: str | None = None):
    ...
```

### Set to `false` for legacy codebases

If your codebase has many functions with `= None` defaults that lack explicit `Optional` annotations, setting this to `false` can reduce noise while you incrementally update the annotations.

## Fixing errors after enabling

When this setting is `true`, fix errors by making the `Optional` explicit:

```python
# Before — error with strict setting
def func(param: int = None):
    ...

# After — using union syntax (Python 3.10+)
def func(param: int | None = None):
    ...

# After — using Optional (all Python versions)
from typing import Optional

def func(param: Optional[int] = None):
    ...
```

## Related settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.
- [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md)
    - Fine-grained control over individual diagnostic rule severities.

## Frequently asked questions

### Q: Why did Pylance start reporting errors on my `= None` parameters?

**A:** If `strictParameterNoneValue` is `true` (the default), Pylance requires an explicit `Optional` or `| None` annotation. Earlier versions of PEP 484 allowed implicit `Optional`, but the current recommendation requires it to be explicit.

### Q: Is it better to be explicit about `Optional`?

**A:** Yes. Explicit annotations improve readability and make the type contract clear to other developers and tools.

### Q: Does this setting affect parameters without type annotations?

**A:** No. This setting only applies to parameters that have a type annotation and a default value of `None`. Unannotated parameters are unaffected.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

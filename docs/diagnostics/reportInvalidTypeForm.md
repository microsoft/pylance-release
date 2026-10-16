## Overview

`reportInvalidTypeForm` is a diagnostic that flags invalid or unsupported type annotation forms in your Python code. This helps ensure that type annotations follow PEP 484 and are compatible with static type checkers like Pyright and Pylance.

## Representative Issues

- [#5471](https://github.com/microsoft/pylance-release/issues/5471): Use base classes from the original module for type annotations to avoid syntax errors.
- [#5695](https://github.com/microsoft/pylance-release/issues/5695): Ensure all type annotations adhere to PEP 484 syntax.
- [#6254](https://github.com/microsoft/pylance-release/issues/6254): Use `TypeAlias` for class-scoped type aliases.
- [#7268](https://github.com/microsoft/pyright/issues/7268): Use `NewType` at the global scope.
- [#7484](https://github.com/microsoft/pyright/issues/7484): Ensure backward compatibility when changing diagnostic rules.
- [#7640](https://github.com/microsoft/pyright/issues/7640): Use correct syntax for type annotations.
- [#8129](https://github.com/microsoft/pyright/issues/8129): Use literal types or fully qualified names in type annotations.
- [#8213](https://github.com/microsoft/pyright/issues/8213): Avoid variable names that conflict with type annotations.
- [#8451](https://github.com/microsoft/pyright/issues/8451): Use literal values directly in type annotations.
- [#8504](https://github.com/microsoft/pyright/issues/8504): Use `Final` and `TypeAlias` only in supported ways.

## Examples

```python
x: 1 + 2  # Error: binary operator not allowed in type expression
```

**Fix — use valid type forms:**

```python
from typing import Literal
x: Literal[3]  # Use Literal for value types
```

A related `reportInvalidTypeArguments` case:

```python
def process(items: list[int] | str[float]) -> None:  # str is not generic
    pass
```

Fix:

```python
def process(items: list[int] | str) -> None:
    pass
```

## Common Fixes & Workarounds

1. Use only valid PEP 484 type annotation syntax.
2. Define `NewType` at global scope; `TypeAlias` may be defined at module or class scope, but not inside functions.
3. Use literal values and fully qualified names in type annotations.
4. Avoid variable names that conflict with type annotations in the same class.
5. Refactor code to use supported type annotation forms.
6. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInvalidTypeForm) for details on configuring this rule.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

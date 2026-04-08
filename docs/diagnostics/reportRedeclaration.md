## Overview

`reportRedeclaration` flags cases where a variable, function, or class is redeclared in a way that could cause confusion or errors. This diagnostic helps ensure that each symbol in your code has a clear and unique definition.

## Representative Issues

- [#10013](https://github.com/microsoft/pyright/issues/10013): Explicitly declare attribute types at assignment to help type checkers recognize variable types.
- [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing and ensure clear variable identification.
- [#8504](https://github.com/microsoft/pyright/issues/8504): Ensure `Final` and `TypeAlias` are only used directly in type annotations without unsupported combinations.

## Examples

**Error:**

```python
MAX_RETRIES: int = 3
MAX_RETRIES: str = "three"  # Redeclared with a different type
```

**Fix — declare each variable once:**

```python
MAX_RETRIES: int = 3
```

Another common case — function redeclaration:

```python
def process(x: int) -> int: ...
def process(x: str) -> str: ...  # Redeclares 'process' (use @overload)
```

Fix with overloads:

```python
from typing import overload

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...

def process(x: int | str) -> int | str:
    return x
```

## Common Fixes & Workarounds

1. Avoid redeclaring variables, functions, or classes with the same name in the same scope.
2. Use unique names for new symbols to prevent shadowing.
3. Refactor code to clarify symbol ownership and avoid accidental redeclaration.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportRedeclaration) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

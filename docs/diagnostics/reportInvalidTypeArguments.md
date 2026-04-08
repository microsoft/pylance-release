## Overview

`reportInvalidTypeArguments` is a diagnostic that flags incorrect or missing type arguments in generic classes, functions, or type aliases. This helps ensure that generics are used properly and that type safety is maintained throughout your code.

## Representative Issues

- [#7536](https://github.com/microsoft/pyright/issues/7536): When subclassing a generic class, include type variables to preserve generics.
- [#8112](https://github.com/microsoft/pyright/issues/8112): Ensure generic type arguments are correctly constrained, especially with unions.
- [#8942](https://github.com/microsoft/pyright/issues/8942): Prefer class-based syntax for TypedDict with generics.
- [#9641](https://github.com/microsoft/pyright/issues/9641): Avoid circular dependencies between type aliases and class definitions.

## Examples

**Error:**

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

b: Box[int, str] = Box(1)  # Too many type arguments (expected 1)
```

**Fix — supply the correct number of type arguments:**

```python
b: Box[int] = Box(1)
```

Or for constrained type variables:

```python
T = TypeVar("T", int, str)

class Box(Generic[T]):
    pass

b: Box[float] = Box()  # 'float' not in constraints [int, str]
# Fix: use an allowed type
b: Box[int] = Box()
```

## Common Fixes & Workarounds

1. Always specify the correct type arguments when using generics.
2. Use class-based syntax for generic TypedDicts.
3. Refactor code to avoid circular dependencies between type aliases and classes.
4. Review and update type constraints for generic parameters.
5. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInvalidTypeArguments) for details on configuring this rule.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

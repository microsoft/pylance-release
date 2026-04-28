## Overview

`reportOperatorIssue` is a Pylance and Pyright diagnostic that identifies problems with the use of Python operators (such as `+`, `-`, `*`, `/`, etc.) where the operands are not type-compatible or where operator overloading is misapplied. This helps catch subtle bugs and type errors in code that uses custom classes or generics with operator methods.

## Representative Issues

- [#7548](https://github.com/microsoft/pyright/issues/7548): Always ensure that TypeVars are properly scoped and resolved within their respective contexts to avoid type resolution failures.

## Examples

```python
"hello" - "world"  # Error: Operator "-" not supported for types "str" and "str"

[1, 2] + (3, 4)   # Error: Operator "+" not supported for types "list[int]"
                  #   and "tuple[int, int]"
```

**Fix — use compatible types:**

```python
10 - 3              # OK: both are int
[1, 2] + [3, 4]     # OK: both are list[int]
```

**Fix — implement dunder methods for custom classes:**

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)
```

## Common Fixes & Workarounds

1. Check that both operands of an operator are of compatible types or implement the appropriate dunder methods (e.g., `__add__`, `__mul__`).
2. For generic classes, ensure that `TypeVar`s are correctly scoped and resolved in all contexts where operators are used.
3. If using operator overloading, verify that the method signatures match expected types and return values.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOperatorIssue) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

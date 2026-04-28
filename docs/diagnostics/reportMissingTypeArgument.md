## Overview

`reportMissingTypeArgument` is a diagnostic in Pylance and Pyright that warns when a generic type is used without specifying the required type arguments. This helps catch ambiguous or incomplete type usage, improving code reliability and maintainability.

## Representative Issues

- [#2253](https://github.com/microsoft/pylance-release/issues/2253): Ensure that type arguments are provided when defining generic type aliases to avoid ambiguous typing errors.
- [#5267](https://github.com/microsoft/pyright/issues/5267): Ensure that generics are properly utilized in class hierarchies by specifying type arguments, especially when dealing with inheritance.
- [#966](https://github.com/microsoft/pyright/issues/966): Ensure that generic type aliases are properly instantiated with the correct type arguments to avoid confusion in variable types.

## Examples

```python
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Box(Generic[_T]):
    def __init__(self, item: _T):
        self.item = item

# Warning: Missing type argument for "Box"
class SpecialBox(Box):  # Should be Box[int], Box[str], etc.
    pass

# Warning: Missing type argument for "Box"
var: Box | None = None
```

**Fix — provide the type argument:**

```python
class SpecialBox(Box[int]):
    pass

var: Box[str] | None = None
```

## Common Fixes & Workarounds

1. Always provide the required type arguments when using generic types or type aliases.
2. Refactor code to specify type arguments for all generics and type aliases.
3. Use type stubs or install third-party stubs for external libraries if needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingTypeArgument) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

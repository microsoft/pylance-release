## Overview

`reportReturnType` flags cases where the return type of a function or method does not match its declared return type annotation. This diagnostic helps catch mismatches early, improving code correctness and type safety.

## Representative Issues

- [#7841](https://github.com/microsoft/pyright/issues/7841): Ensure that the `@overload` decorator is used correctly and consistently to define type hints for functions.
- [#7880](https://github.com/microsoft/pyright/issues/7880): Use type variables with precise constraints to avoid runtime errors and static analysis issues.
- [#9371](https://github.com/microsoft/pyright/issues/9371): Ensure that the return type of overridden methods matches exactly with the base method's return type, especially with async generators.
- [#9568](https://github.com/microsoft/pyright/issues/9568): When using `type[TypeVar]` in function signatures, ensure type checks are performed correctly with `issubclass`.

## Examples

```python
def get_count() -> int:
    return "five"  # Error: Return type "str" is incompatible
                   #   with declared return type "int"

def is_valid(value: str) -> bool:
    return value  # Error: Return type "str" is incompatible
                  #   with declared return type "bool"
```

**Fix — return the correct type:**

```python
def get_count() -> int:
    return 5

def is_valid(value: str) -> bool:
    return len(value) > 0
```

**Fix — correct the return annotation:**

```python
def get_count() -> str:
    return "five"  # OK if string return was intended
```

## Common Fixes & Workarounds

1. Ensure the return value of a function matches its declared return type annotation.
2. Use type guards and precise type annotations to clarify return types.
3. Refactor code to ensure overridden methods match the base method's return type exactly.
4. Use the `@overload` decorator correctly for functions with multiple signatures.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportReturnType) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

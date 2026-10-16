## Overview

`reportMissingParameterType` is a diagnostic in Pylance and Pyright that warns when a function or method parameter is missing a type annotation. This helps catch missing or ambiguous type information, improving code clarity and type safety.

## Representative Issues

- [#3078](https://github.com/microsoft/pyright/issues/3078): Always provide type hints for function parameters to avoid diagnostic errors in static analysis tools.
- [#2735](https://github.com/microsoft/pyright/issues/2735): Provide specific configuration options for type check diagnostics to improve code maintainability.
- [#774](https://github.com/microsoft/pyright/issues/774): When using decorators that modify the signature of a function, use TypeVars bound to Callable types to maintain the original signatures.

## Examples

```python
def greet(name):  # Warning: Type annotation is missing for parameter "name"
    print(f"Hello, {name}")

def add(a, b):  # Warning: Type annotation is missing for parameter "a"
    return a + b
```

**Fix — add type annotations to parameters:**

```python
def greet(name: str) -> None:
    print(f"Hello, {name}")

def add(a: int, b: int) -> int:
    return a + b
```

## Common Fixes & Workarounds

1. Add explicit type annotations to all function and method parameters.
2. Use type stubs or install third-party stubs for external libraries.
3. Review and update type hints in your codebase for completeness.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingParameterType) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

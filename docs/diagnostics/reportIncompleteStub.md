## Overview

`reportIncompleteStub` is a diagnostic that flags incomplete or insufficient type stub (`.pyi`) files. This helps ensure that your type stubs provide all necessary type information for static analysis and are consistent with the actual implementation.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright CLI and Pylance settings.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide configuration for customizing diagnostic rule severities by type checking mode.
- [#1831](https://github.com/microsoft/pyright/issues/1831): Handle module-level `__getattr__` definitions in stubs.
- [#3332](https://github.com/microsoft/pyright/issues/3332): Always specify the module path when referencing submodules in stubs.

## Examples

**Error:**

```python
# my_lib.pyi (stub file)
def public_func(x: int) -> str: ...

def __getattr__(name: str) -> object: ...  # Indicates the stub is incomplete
```

A module-level `__getattr__` in a stub tells Pyright the stub doesn't declare all exports — any attribute access would silently return `object`, hiding real type errors.

**Fix — complete the stub and remove `__getattr__`:**

```python
# my_lib.pyi
def public_func(x: int) -> str: ...
def other_func(y: float) -> None: ...  # Add all missing declarations
```

## Common Fixes & Workarounds

1. Complete all required type information in `.pyi` files, including all public members and signatures.
2. Use correct syntax and conventions for Python type stub files.
3. Specify full module paths when referencing submodules in stubs.
4. Adjust diagnostic severity in your configuration if needed.
5. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportIncompleteStub) for details on configuring this rule.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

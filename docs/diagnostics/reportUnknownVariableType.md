## Overview

`reportUnknownVariableType` is a diagnostic in Pylance and Pyright that warns when a variable's type cannot be determined. This rule is primarily active in strict mode (`typeCheckingMode: "strict"`), where `Any` types from untyped libraries are treated as unknown. This helps catch missing or ambiguous type information, improving code reliability and maintainability.

## Representative Issues

- [#1023](https://github.com/microsoft/pylance-release/issues/1023): Avoid using literal types within tuples for collection elements to prevent incorrect type inference and concatenation issues.
- [#3192](https://github.com/microsoft/pylance-release/issues/3192): Ensure matplotlib type stubs match the library's actual return types, especially for subscriptable objects like ndarray and subplot arrays.
- [#4382](https://github.com/microsoft/pylance-release/issues/4382): Ensure that the correct version of static analysis tools is used and verify that all necessary dependencies, including type stubs, are correctly installed.
- [#5648](https://github.com/microsoft/pylance-release/issues/5648): Ensure that the `py.typed` file is correctly configured and placed to be recognized by Pylance's type checking system.

## Examples

**Error (strict mode):**

```python
from untyped_lib import get_value  # Library without type stubs

result = get_value()  # Type of "result" is unknown
```

When a library has no type stubs and no `py.typed` marker, all imports resolve to unknown types in strict mode (with `useLibraryCodeForTypes` disabled).

**Fix — install type stubs or add annotations:**

The best fix is to install type stubs for the library:

```bash
pip install types-some_library
```

If stubs are not available, add a type annotation to make the variable type known:

```python
from typing import cast

result: dict[str, int] = cast(dict[str, int], get_value())
```

## Common Fixes & Workarounds

1. Add explicit type annotations to variables where possible.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify variable types where needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownVariableType) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

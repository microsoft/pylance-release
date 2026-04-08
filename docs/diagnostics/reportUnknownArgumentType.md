## Overview

`reportUnknownArgumentType` is a diagnostic in Pylance and Pyright that warns when an argument passed to a function or method has an unknown type. This rule is primarily active in strict mode (`typeCheckingMode: "strict"`), where `Any` types from untyped libraries are treated as unknown. This helps catch missing or ambiguous type information, improving code reliability and maintainability.

## Representative Issues

- [#1759](https://github.com/microsoft/pyright/issues/1759): Ensure that libraries used in a project include type information or provide stub files to aid static analysis tools like pyright.
- [#3066](https://github.com/microsoft/pyright/issues/3066): Enhance the diagnostic tool to differentiate between completely unknown and partially unknown variable types.
- [#3347](https://github.com/microsoft/pyright/issues/3347): Use keyword-only arguments in lambda functions when assigning them to protocols with specific argument requirements.

## Examples

**Error (strict mode):**

```python
from untyped_lib import get_value  # Library without type stubs

def process(data: dict[str, int]) -> None:
    pass

raw = get_value()
process(raw)  # Argument type is unknown
```

When a library has no type stubs and no `py.typed` marker, all imports resolve to unknown types in strict mode (with `useLibraryCodeForTypes` disabled).

**Fix — install type stubs or add annotations:**

The best fix is to install type stubs for the library:

```bash
pip install types-some_library
```

If stubs are not available, annotate the result so the argument type is known:

```python
from typing import cast

def process(data: dict[str, int]) -> None:
    pass

# Use cast to explicitly assert the type
data: dict[str, int] = cast(dict[str, int], get_value())
process(data)  # Argument type is now known
```

## Common Fixes & Workarounds

1. Add or improve type annotations for function arguments.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify argument types where possible.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownArgumentType) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

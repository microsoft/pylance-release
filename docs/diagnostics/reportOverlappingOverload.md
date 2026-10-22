## Overview

`reportOverlappingOverload` is a diagnostic in Pylance and Pyright that warns when an overload is obscured by an earlier signature or overlapping signatures have incompatible return types. This can lead to ambiguity and unexpected behavior in type checking and code execution.

## Representative Issues

- [#10014](https://github.com/microsoft/pyright/issues/10014): Check whether omitting default keyword arguments makes overloads overlap.
- [#7084](https://github.com/microsoft/pyright/issues/7084): Avoid using multiple TypeVars in function signatures without a clear reason to distinguish different overloads.
- [#9603](https://github.com/microsoft/pyright/issues/9603): Ensure that `join` returns the appropriate type based on the elements in the list, avoiding mismatches between literal and non-literal strings.

## Examples

**Error:**

```python
from typing import overload

@overload
def process(x: int) -> str: ...
@overload
def process(x: int) -> int: ...  # Overlaps with first overload

def process(x: int) -> str | int:
    return str(x)
```

**Fix — make overloads non-overlapping:**

```python
from typing import overload

@overload
def process(x: int) -> str: ...
@overload
def process(x: str) -> int: ...  # Different param types

def process(x: int | str) -> str | int:
    if isinstance(x, int):
        return str(x)
    return int(x)
```

## Common Fixes & Workarounds

1. Make overload signatures mutually exclusive so that only one matches any given call.
2. Check for overlapping calls when defaulted arguments are omitted.
3. Use clear and distinct TypeVars only when necessary.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOverlappingOverload) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

Last content update aligned with [Pylance 2026.4.101](https://github.com/microsoft/pylance-release/blob/b946877fc1245510cdf55850546fc48cb44129fe/CHANGELOG.md#20264101-15-october-2026-prerelease).

## Overview

`reportOptionalIterable` is a diagnostic in Pylance and Pyright that warns when you attempt to iterate over a value that could be `None`. This helps prevent runtime errors caused by trying to loop over an optional value that might not be an iterable.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
- [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries, prefer `typing.Dict` syntax for compatibility.
- [#660](https://github.com/microsoft/pyright/issues/660): Annotate decorators with `Callable[..., Any]` to inform Pyright about function signatures.
- [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.
- [#9073](https://github.com/microsoft/pyright/issues/9073): Use individual truthiness checks in type guard contexts instead of relying on `all`.

## Examples

```python
from typing import Optional

def print_items(items: Optional[list[str]]) -> None:
    for item in items:  # Error: Object of type "None" is not iterable
        print(item)
```

**Fix — check for None before iterating:**

```python
def print_items(items: Optional[list[str]]) -> None:
    if items is not None:
        for item in items:
            print(item)
```

**Fix — use a default value:**

```python
def print_items(items: Optional[list[str]]) -> None:
    for item in items or []:
        print(item)
```

## Common Fixes & Workarounds

1. Use type guards (e.g., `if items is not None:`) before iterating over a possibly-optional value.
2. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
3. Use assertions (e.g., `assert items is not None`) before iterating if you are certain the value is not `None` at that point.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalIterable).

## See Also

- [How to Use Type Narrowing to Fix Type Errors](../howto/type-narrowing.md) — check for `None` before iterating
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

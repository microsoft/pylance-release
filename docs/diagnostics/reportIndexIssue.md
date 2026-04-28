## Overview

`reportIndexIssue` is a diagnostic in Pylance and Pyright that warns about problems with indexing or subscripting objects, such as using an invalid index type or subscripting a value that does not support it. This helps catch type errors and incorrect usage of lists, tuples, dictionaries, and other indexable types.

## Representative Issues

- [#8319](https://github.com/microsoft/pyright/issues/8319): Use type aliases correctly and consistently to avoid runtime errors in static type checkers.
- [#8801](https://github.com/microsoft/pyright/issues/8801): Ensure that type aliases do not improperly reference `TypeVar` with default values within their definitions to avoid incorrect static analysis tool behavior.

## Examples

```python
my_dict: dict[str, int] = {"a": 1}
my_dict[0]  # Error: Argument of type "int" is incompatible with "str"

x: int = 42
x[0]  # Error: Object of type "int" is not subscriptable
```

**Fix — use the correct index type:**

```python
my_dict["a"]  # OK: key is str
```

**Fix — only subscript objects that support indexing:**

```python
my_list: list[int] = [10, 20, 30]
my_list[0]  # OK: list supports integer indexing
```

## Common Fixes & Workarounds

1. Make sure you are using valid index types (e.g., integers for lists, appropriate keys for dictionaries).
2. Only subscript objects that support indexing (e.g., lists, tuples, dicts, or classes with `__getitem__`).
3. Use type annotations and type aliases correctly, especially when working with generics and `TypeVar`.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportIndexIssue) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

## Overview

`reportIndexIssue` is a diagnostic in Pylance and Pyright that warns about problems with indexing or subscripting objects, such as using an invalid index type or subscripting a value that does not support it. This helps catch type errors and incorrect usage of lists, tuples, dictionaries, and other indexable types.

## Representative Issues

-   [#8319](https://github.com/microsoft/pyright/issues/8319): Use type aliases correctly and consistently to avoid runtime errors in static type checkers.
-   [#8801](https://github.com/microsoft/pyright/issues/8801): Ensure that type aliases do not improperly reference `TypeVar` with default values within their definitions to avoid incorrect static analysis tool behavior.

## Common Fixes & Workarounds

1. Make sure you are using valid index types (e.g., integers for lists, appropriate keys for dictionaries).
2. Only subscript objects that support indexing (e.g., lists, tuples, dicts, or classes with `__getitem__`).
3. Use type annotations and type aliases correctly, especially when working with generics and `TypeVar`.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportIndexIssue) for options to adjust or suppress this diagnostic if needed.

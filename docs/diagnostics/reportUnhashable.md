## Overview

`reportUnhashable` flags cases where an object that is not hashable is used in a context that requires hashable types, such as keys in dictionaries or elements in sets. This diagnostic helps prevent runtime errors and ensures your code uses only valid types in hash-based collections.

## Representative Issues

-   [#8377](https://github.com/microsoft/pyright/issues/8377): Ensure Pyright is invoked with the project root directory to maintain correct import resolution behavior, especially when using editable installations within the same environment.
-   [#9236](https://github.com/microsoft/pyright/issues/9236): Ensure that static type checkers like `pyright` correctly interpret the types in the standard library, especially when there are updates or corrections in newer Python versions.
-   [#9237](https://github.com/microsoft/pyright/issues/9237): Always follow the correct syntax for comments in directives to avoid errors with static type checkers like Pyright.

## Common Fixes & Workarounds

1. Use only hashable types (e.g., `int`, `str`, `tuple` of hashable elements) as dictionary keys or set elements.
2. Avoid using mutable types like `list` or `dict` as keys in dictionaries or elements in sets.
3. If you need to use a custom object as a key, implement the `__hash__` and `__eq__` methods appropriately.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnhashable) for details on configuring this diagnostic.
5. Suppress this diagnostic with `# pyright: reportUnhashable=false` if you have a special case.

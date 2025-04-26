## Overview

`reportUnsupportedDunderAll` is a Pylance diagnostic that warns when your code uses the `__all__` symbol in ways that are not supported by static type checkers. This helps you avoid patterns that may work at runtime but are not recognized by tools like Pylance and Pyright, ensuring your module exports are clear and type-safe.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#4286](https://github.com/microsoft/pyright/issues/4286): Ensure that Protocol classes are consistently imported from the `typing_extensions` module to avoid runtime issues with static type checkers.

## Common Fixes & Workarounds

1. Use only simple, static lists of string names for `__all__` (e.g., `__all__ = ["foo", "bar"]`).
2. Avoid dynamically constructing or modifying `__all__` at runtime.
3. If you need dynamic exports, consider using explicit imports and exports instead.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnsupportedDunderAll) to adjust the severity or disable this diagnostic if needed.

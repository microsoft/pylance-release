## Overview

`reportOptionalOperand` is a diagnostic in Pylance and Pyright that warns when you use a value that could be `None` as an operand in a binary or unary operation (e.g., `a + b` where `a` or `b` might be `None`). This helps prevent runtime errors caused by performing operations on optional values.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer `typing.Dict` syntax for compatibility with generic types.
-   [#10013](https://github.com/microsoft/pyright/issues/10013): Explicitly declare attribute types at assignment to help type checkers recognize variable types.
-   [#3919](https://github.com/microsoft/pyright/issues/3919): Use specific type annotations and correct tuple types to avoid type narrowing errors.
-   [#6687](https://github.com/microsoft/pyright/issues/6687): Clarify that `reportOptionalOperand` only suppresses errors for the left-hand side of a binary operator.
-   [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if a is not None and b is not None:`) before performing operations on possibly-optional values.
2. Use default values (e.g., `(a or 0) + (b or 0)`) to ensure operands are never `None`.
3. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalOperand).

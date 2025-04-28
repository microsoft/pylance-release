## Overview

`reportAssertTypeFailure` is a Pylance and Pyright diagnostic that warns when an `assert_type` check fails, meaning the value does not match the expected type. This helps you catch type mismatches early and ensure your code is type-safe.

## Representative Issues

-   [#7536](https://github.com/microsoft/pyright/issues/7536): When subclassing a generic class in Python, include the type variables to preserve the generics.
-   [#7548](https://github.com/microsoft/pyright/issues/7548): Always ensure that TypeVars are properly scoped and resolved within their respective contexts to avoid type resolution failures.
-   [#7983](https://github.com/microsoft/pyright/issues/7983): Ensure that the `value` property of `StrEnum` instances is consistently validated to maintain type consistency across your codebase.
-   [#8219](https://github.com/microsoft/pyright/issues/8219): Use lists instead of tuples with variable length in `match` statements to avoid inappropriate type narrowing and ensure successful static analysis.
-   [#8804](https://github.com/microsoft/pyright/issues/8804): Use `assert_type` to verify the type of callable objects and their methods, rather than relying on `reveal_type` for callables that implement `__call__`, as it is not supported.
-   [#8942](https://github.com/microsoft/pyright/issues/8942): When using TypedDict with generics in Python, prefer the class-based syntax over the functional syntax to avoid type checking errors.
-   [#9142](https://github.com/microsoft/pyright/issues/9142): Use 'is None' or 'is not None' in tuple type narrowing conditions to align with Pyright's support for such expressions.
-   [#9408](https://github.com/microsoft/pyright/issues/9408): Ensure that type variables in generic types are properly constrained to avoid runtime mismatches.

## Common Fixes & Workarounds

1. Ensure that the value being checked with `assert_type` matches the expected type exactly.
2. When subclassing generics, always include type variables.
3. Prefer class-based syntax for generic `TypedDict` definitions.
4. Use explicit type checks and constraints for type variables.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAssertTypeFailure) for details on configuring or disabling this diagnostic.

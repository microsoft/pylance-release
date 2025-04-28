## Overview

`reportImplicitStringConcatenation` is a diagnostic in Pylance and Pyright that warns when string literals are implicitly concatenated without an explicit operator. This helps catch subtle bugs and improves code clarity by making string concatenation intentions explicit.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer `typing.Dict` over `dict[t, t]` for compatibility.
-   [#2721](https://github.com/microsoft/pyright/issues/2721): Use `isinstance` for clearer type narrowing with coroutines.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure TOML comments use correct line endings.
-   [#5411](https://github.com/microsoft/pyright/issues/5411): Use explicit `AsyncGenerator` type annotation for async generator functions.

## Common Fixes & Workarounds

1. Use the `+` operator or f-strings for explicit string concatenation.
2. Avoid placing string literals next to each other without an operator.
3. Review and update type annotations and stubs for consistency.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportImplicitStringConcatenation) for options to adjust or suppress this diagnostic if needed.

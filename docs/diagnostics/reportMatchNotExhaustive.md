## Overview

`reportMatchNotExhaustive` is a Pylance diagnostic that warns when a Python `match` statement does not cover all possible cases for the matched value. This helps ensure your code is robust and prevents runtime errors by encouraging you to handle every possible input.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#6591](https://github.com/microsoft/pyright/issues/6591): When using `match` statements over tuples in Python, ensure to handle all possible combinations explicitly or use a catch-all case for tuples that are not explicitly handled.
-   [#7559](https://github.com/microsoft/pyright/issues/7559): Avoid unnecessary match case statements that don't handle specific scenarios when using tuples and `match` statements in Python to prevent errors.
-   [#9291](https://github.com/microsoft/pyright/issues/9291): Ensure that match statements cover all possible types, including non-instantiable abstract base classes by adding a catch-all branch or using a union type.
-   [#9839](https://github.com/microsoft/pyright/issues/9839): Consider using `assert_never` to handle cases that should never occur in a match statement, ensuring thorough type checking and exhaustiveness analysis.

## Common Fixes & Workarounds

1. Add a catch-all case (e.g., `case _:`) to your `match` statement to handle any unhandled values.
2. Explicitly enumerate all possible cases for the matched value, especially when matching enums or union types.
3. Use `assert_never` or raise an exception in the catch-all branch to make unhandled cases explicit.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMatchNotExhaustive) to adjust the severity or disable this diagnostic if needed.

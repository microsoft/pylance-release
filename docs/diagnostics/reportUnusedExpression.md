## Overview

`reportUnusedExpression` is a Pylance and Pyright diagnostic that warns when an expression in your code has no effect and its result is not used. Removing unused expressions helps keep your code clean and can prevent confusion or subtle bugs.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#4286](https://github.com/microsoft/pyright/issues/4286): Ensure that Protocol classes are consistently imported from the `typing_extensions` module to avoid runtime issues with static type checkers.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#7087](https://github.com/microsoft/pyright/issues/7087): Ensure that generators are utilized in iterable contexts or explicitly stopped to avoid unused code.
-   [#9236](https://github.com/microsoft/pyright/issues/9236): Ensure that static type checkers like `pyright` correctly interpret the types in the standard library, especially when there are updates or corrections in newer Python versions.
-   [#9237](https://github.com/microsoft/pyright/issues/9237): Always follow the correct syntax for comments in directives to avoid errors with static type checkers like Pyright.

## Common Fixes & Workarounds

1. Remove expressions whose results are not used.
2. Assign the result to a variable if you intend to use it later.
3. Ensure generators and iterables are used in a meaningful context.
4. Use correct syntax for comments and directives.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedExpression) for details on configuring or disabling this diagnostic.

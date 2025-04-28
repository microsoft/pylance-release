## Overview

`reportAssertAlwaysTrue` is a Pylance and Pyright diagnostic that warns when an `assert` statement is always true, making the assertion redundant. This helps you identify unnecessary code and potential logic errors in your Python projects.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.

## Common Fixes & Workarounds

1. Remove or update `assert` statements that are always true to avoid redundant code.
2. Double-check logic in assertions to ensure they are meaningful and not trivially true.
3. Use explicit type annotations and consistent type stubs to avoid confusion.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAssertAlwaysTrue) for details on configuring or disabling this diagnostic.

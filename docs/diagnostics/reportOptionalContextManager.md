## Overview

`reportOptionalContextManager` is a diagnostic in Pylance and Pyright that warns when you attempt to use a value that could be `None` as a context manager (e.g., in a `with` statement). This helps prevent runtime errors caused by trying to enter a context with an optional value.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if resource is not None:`) before using a possibly-optional value in a `with` statement.
2. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
3. Use assertions (e.g., `assert resource is not None`) before entering a context if you are certain the value is not `None` at that point.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalContextManager).

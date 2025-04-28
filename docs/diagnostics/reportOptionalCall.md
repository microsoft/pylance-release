## Overview

`reportOptionalCall` is a diagnostic in Pylance and Pyright that warns when you attempt to call a value that could be `None` (e.g., `maybe_func()`). This helps prevent runtime errors caused by calling a function or method that might not be defined.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.
-   [#9073](https://github.com/microsoft/pyright/issues/9073): When using `all` in a type guard context, use individual truthiness checks instead of relying on `all` for conditional evaluation.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if func is not None:`) before calling a possibly-optional function or method.
2. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
3. Use assertions (e.g., `assert func is not None`) before calling if you are certain the value is not `None` at that point.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalCall).

## Overview

`reportOptionalIterable` is a diagnostic in Pylance and Pyright that warns when you attempt to iterate over a value that could be `None`. This helps prevent runtime errors caused by trying to loop over an optional value that might not be an iterable.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries, prefer `typing.Dict` syntax for compatibility.
-   [#660](https://github.com/microsoft/pyright/issues/660): Annotate decorators with `Callable[..., Any]` to inform Pyright about function signatures.
-   [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.
-   [#9073](https://github.com/microsoft/pyright/issues/9073): Use individual truthiness checks in type guard contexts instead of relying on `all`.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if items is not None:`) before iterating over a possibly-optional value.
2. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
3. Use assertions (e.g., `assert items is not None`) before iterating if you are certain the value is not `None` at that point.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalIterable).

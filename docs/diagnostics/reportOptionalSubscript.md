## Overview

`reportOptionalSubscript` is a diagnostic in Pylance and Pyright that warns when you attempt to subscript (use square brackets, e.g., `obj[index]`) a value that could be `None`. This helps prevent runtime errors caused by trying to index or slice an optional value.

## Representative Issues

-   [#1506](https://github.com/microsoft/pylance-release/issues/1506): Adjust diagnostic severity overrides in IDE settings to control type-checking behavior after updates.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#6446](https://github.com/microsoft/pylance-release/issues/6446): Always set Pylance-specific defaults in pyrightconfig.json to avoid unintended changes when enabling configuration files.
-   [#4784](https://github.com/microsoft/pyright/issues/4784): Ensure that the code uses correct and compatible types across different type checkers to avoid inconsistencies.
-   [#7523](https://github.com/microsoft/pyright/issues/7523): Use type guards and annotations to narrow down variable types before accessing them to avoid errors like 'reportOptionalSubscript'.
-   [#79](https://github.com/microsoft/pyright/issues/79): Consider using Optional types in unions to manage None assignments more effectively.
-   [#9073](https://github.com/microsoft/pyright/issues/9073): When using `all` in a type guard context, use individual truthiness checks instead of relying on `all` for conditional evaluation.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if obj is not None:`) before subscripting a possibly-optional value.
2. Add type annotations to clarify when a value can be `None` and handle those cases explicitly.
3. Use assertions (e.g., `assert obj is not None`) before subscripting if you are certain the value is not `None` at that point.
4. Adjust the diagnostic severity or disable the rule in your settings if needed. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalSubscript).

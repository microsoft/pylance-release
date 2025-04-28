## Overview

`reportUninitializedInstanceVariable` is a diagnostic in Pylance and Pyright that warns when an instance variable may be used before it is initialized. This helps catch potential runtime errors and ensures that all instance variables are properly set before use.

## Representative Issues

-   [#2184](https://github.com/microsoft/pyright/issues/2184): When using `Optional` return types, ensure functions include explicit return statements for all possible outcomes.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#2721](https://github.com/microsoft/pyright/issues/2721): Use `isinstance` for clearer type narrowing with coroutines.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure TOML comments use correct line endings.
-   [#6376](https://github.com/microsoft/pyright/issues/6376): Consider adding diagnostic rules to your configuration file instead of using the "all" default.
-   [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing.
-   [#7193](https://github.com/microsoft/pyright/issues/7193): After an `isinstance` check, set the variable to the correct type to avoid false positives.

## Common Fixes & Workarounds

1. Always initialize instance variables in the class constructor (`__init__`).
2. Use default values for instance variables when possible.
3. Review all code paths to ensure variables are set before use.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUninitializedInstanceVariable) for options to adjust or suppress this diagnostic if needed.

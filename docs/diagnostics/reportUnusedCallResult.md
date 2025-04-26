## Overview

`reportUnusedCallResult` is a Pylance and Pyright diagnostic that warns when the result of a function or method call is not used. This can help identify places where you may have forgotten to use or store a value, or where code can be simplified.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#7001](https://github.com/microsoft/pylance-release/issues/7001): Prefer 'openFilesOnly' diagnostic mode for large projects to avoid full reanalysis on every edit; use workspace analysis selectively.
-   [#1125](https://github.com/microsoft/pyright/issues/1125): Consider using explicit statements to indicate that a returned value is intentionally ignored to mitigate false positives from unused call results.
-   [#1320](https://github.com/microsoft/pyright/issues/1320): Document the interaction between `typeCheckingMode` and specific diagnostic settings to clarify their effects on each other.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#6756](https://github.com/microsoft/pyright/issues/6756): Avoid using throwaway variables `_` when the result's type is unknown, as it can trigger strict type checks that expect assigned variables to have known types.
-   [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing and ensure clear variable identification.
-   [#7193](https://github.com/microsoft/pyright/issues/7193): After an `isinstance` check with a specific type, the variable should be explicitly set to that type or a more specific type to avoid false positive errors in static analysis tools.

## Common Fixes & Workarounds

1. Assign the result of a function call to a variable if you intend to use it later.
2. If the result is intentionally unused, consider using a comment or a clearly named variable (e.g., `_unused`) to indicate this.
3. Review your code for places where a function call's result should be used or returned.
4. Adjust your Pyright or Pylance configuration if you want to change the severity or disable this diagnostic. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedCallResult) for details.

## Overview

`reportConstantRedefinition` is a Pylance and Pyright diagnostic that warns when a constant (typically an ALL_CAPS variable) is redefined in your code. Redefining constants can lead to confusion and bugs, especially in large codebases.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.
-   [#2974](https://github.com/microsoft/pyright/issues/2974): Explicitly type instance variables at the point of definition to avoid unintended type inference from multiple assignments.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#5265](https://github.com/microsoft/pyright/issues/5265): Use a single assignment to define constants in Python to avoid issues with static type checking tools like pyright.

## Common Fixes & Workarounds

1. Avoid redefining constants; assign them only once.
2. Use ALL_CAPS naming for constants and do not reassign them later in the code.
3. Explicitly type instance variables at the point of definition to prevent unintended type inference.
4. Exclude unnecessary folders (like `.venv`) from your project configuration to improve performance.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportConstantRedefinition) for details on configuring or disabling this diagnostic.

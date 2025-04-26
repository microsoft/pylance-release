## Overview

`reportFunctionMemberAccess` is a Pylance and Pyright diagnostic that warns when function or method members are accessed or modified in ways that can lead to type inference issues or runtime errors. This helps ensure your code is type-safe and maintainable.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#6403](https://github.com/microsoft/pylance-release/issues/6403): Ensure that your configuration settings do not interfere with the proper functioning of decorators and their dynamically added attributes.
-   [#990](https://github.com/microsoft/pylance-release/issues/990): Ensure all diagnostic severity rules in configuration files are accurately named to prevent misdirected diagnostics.
-   [#2524](https://github.com/microsoft/pyright/issues/2524): Ensure that bound methods have their `__self__` attribute correctly typed to the instance type, enhancing type safety and clarity.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#6510](https://github.com/microsoft/pyright/issues/6510): When working with functions or methods in Python, avoid reading or writing attributes directly on them as it can lead to incomplete type inference and potential runtime errors.
-   [#6814](https://github.com/microsoft/pyright/issues/6814): Ensure that overridden symbols in subclasses are correctly aligned with the base class definitions to avoid type violations related to incompatible variable overrides.

## Common Fixes & Workarounds

1. Avoid reading or writing attributes directly on functions or methods unless necessary.
2. Use decorators and wrapper classes to add functionality to functions in a type-safe way.
3. Ensure configuration settings are correct and do not interfere with function member behavior.
4. Review subclass overrides for compatibility with base class definitions.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportFunctionMemberAccess) for details on configuring or disabling this diagnostic.

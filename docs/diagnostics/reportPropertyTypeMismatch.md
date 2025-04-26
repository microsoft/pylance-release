## Overview

`reportPropertyTypeMismatch` is a diagnostic in Pylance and Pyright that warns you when the type of a property setter does not match the type returned by its getter. This helps ensure type consistency for properties, preventing subtle bugs and improving static analysis.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#990](https://github.com/microsoft/pylance-release/issues/990): Ensure all diagnostic severity rules in configuration files are accurately named to prevent misdirected diagnostics.
-   [#2424](https://github.com/microsoft/pyright/issues/2424): Ensure that property setters' value types are consistent with the getter return type to avoid mismatches that confuse static analysis tools.
-   [#2721](https://github.com/microsoft/pyright/issues/2721): When using `iscoroutine` or similar type guards to conditionally check and assign types, consider using `isinstance` for clearer control over the type narrowing process.
-   [#2980](https://github.com/microsoft/pyright/issues/2980): Ensure that configuration parameters default to "none" and are correctly applied in the project settings.
-   [#2981](https://github.com/microsoft/pyright/issues/2981): Ensure that configuration details for diagnostics and type checking are clearly documented, especially when different interfaces like VS Code settings or project-specific configurations might be used.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.

## Common Fixes & Workarounds

1. Ensure the type of the property setter matches the getter's return type (or is a compatible union).
2. Refactor property definitions to use consistent types for both getter and setter.
3. Use `Union` types if a property can accept multiple types.
4. Double-check type stubs and configuration for accuracy.
5. Update your configuration files to use the correct diagnostic rule names.

For more details on configuring this diagnostic, see the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportPropertyTypeMismatch).

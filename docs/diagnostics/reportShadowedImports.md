## Overview

`reportShadowedImports` is a Pylance diagnostic that warns when an import in your Python code is shadowed by another symbol with the same name. This helps prevent confusion and bugs caused by accidentally redefining or hiding imported modules or variables.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#4777](https://github.com/microsoft/pylance-release/issues/4777): When configuring `exclude` paths in a project for static analysis tools like Pylance, it's crucial to balance comprehensive exclusion with the inclusion of necessary workspace components.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#6446](https://github.com/microsoft/pylance-release/issues/6446): Always set Pylance-specific defaults in pyrightconfig.json to avoid unintended changes when enabling configuration files.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing and ensure clear variable identification.

## Common Fixes & Workarounds

1. Avoid redeclaring variables or functions with the same name as an imported module or symbol.
2. Refactor your code to use unique names for local variables and imports.
3. Review your import statements and ensure they are not being unintentionally shadowed later in the code.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportShadowedImports) to adjust the severity or disable this diagnostic if needed.


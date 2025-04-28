## Overview

`reportPrivateImportUsage` flags cases where imports from private modules or symbols are used in a way that exposes internal implementation details. This diagnostic helps enforce encapsulation and maintain a clean public API for your packages.

## Representative Issues

-   [#2943](https://github.com/microsoft/pylance-release/issues/2943): Ensure that the use of '# type: ignore' comments is respected and correctly flagged by static analysis tools.
-   [#3003](https://github.com/microsoft/pylance-release/issues/3003): Ensure Pylint plugins are installed and configured, and VSCode parses their diagnostics into editor warnings.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities by type checking mode.
-   [#7001](https://github.com/microsoft/pylance-release/issues/7001): Prefer 'openFilesOnly' diagnostic mode for large projects.
-   [#2277](https://github.com/microsoft/pyright/issues/2277): Use alias imports to indicate public interface symbols in `py.typed` libraries.
-   [#2639](https://github.com/microsoft/pyright/issues/2639): Ensure symbols are explicitly re-exported if they should be part of the public API.
-   [#8377](https://github.com/microsoft/pyright/issues/8377): Invoke Pyright with the project root directory for correct import resolution.

## Common Fixes & Workarounds

1. Avoid importing private modules or symbols unless necessary.
2. Use alias imports and explicit re-exports to clarify your package's public API.
3. Configure your project to use the correct root directory for import resolution.
4. Use strict type checking and configure directories as needed in your config files.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportPrivateImportUsage) for details on configuring or disabling this diagnostic.

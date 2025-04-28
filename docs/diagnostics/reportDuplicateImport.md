## Overview

`reportDuplicateImport` is a Pylance and Pyright diagnostic that warns when the same module or symbol is imported more than once in your code. Duplicate imports can clutter your code and may lead to confusion or subtle bugs.

## Representative Issues

-   [#1969](https://github.com/microsoft/pylance-release/issues/1969): Ensure that `python.analysis.indexing` is enabled to maintain an up-to-date index of available modules and symbols, which helps in providing accurate auto-import suggestions.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#3793](https://github.com/microsoft/pylance-release/issues/3793): Ensure that the configuration settings for Pylance/Pyright are correctly applied to suppress errors in Python library files.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.

## Common Fixes & Workarounds

1. Remove duplicate import statements for the same module or symbol.
2. Consolidate imports at the top of your file for clarity and maintainability.
3. Enable `python.analysis.indexing` to improve auto-import suggestions and avoid accidental duplicates.
4. Ensure your configuration settings are correctly applied to suppress unnecessary errors.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportDuplicateImport) for details on configuring or disabling this diagnostic.

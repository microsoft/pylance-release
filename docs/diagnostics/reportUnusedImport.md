## Overview

`reportUnusedImport` is a Pylance and Pyright diagnostic that warns when an imported module or symbol is not used anywhere in your code. Removing unused imports helps keep your code clean and can improve performance.

## Representative Issues

-   [#1969](https://github.com/microsoft/pylance-release/issues/1969): Ensure that `python.analysis.indexing` is enabled to maintain an up-to-date index of available modules and symbols, which helps in providing accurate auto-import suggestions.
-   [#2840](https://github.com/microsoft/pylance-release/issues/2840): Enhance the static analysis capabilities of Pylance to include warnings for unused function parameters, similar to how it handles other unreferenced elements in the code.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#3793](https://github.com/microsoft/pylance-release/issues/3793): Ensure that the configuration settings for Pylance/Pyright are correctly applied to suppress errors in Python library files.
-   [#3853](https://github.com/microsoft/pylance-release/issues/3853): Configure Pylance's packageIndexDepths appropriately for packages and ensure the correct Python environment is active to enable accurate auto-import suggestions.
-   [#3855](https://github.com/microsoft/pylance-release/issues/3855): Ensure Python indexing is enabled in VSCode settings to support auto-import functionality for external packages.
-   [#4012](https://github.com/microsoft/pylance-release/issues/4012): To override the diagnostic severity for import cycles in a project using pyright, configure it globally rather than per file.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#495](https://github.com/microsoft/pylance-release/issues/495): Utilize the `exclude` property in Pyright's config file to prevent analysis of unwanted folders, ensuring smoother configuration and reduced diagnostics clutter.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.

## Common Fixes & Workarounds

1. Remove unused import statements from your code.
2. Enable `python.analysis.indexing` and configure `packageIndexDepths` for better auto-import suggestions.
3. Use the `exclude` property in your config to avoid analyzing unnecessary folders.
4. Ensure your configuration settings are correctly applied to suppress unnecessary errors.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedImport) for details on configuring or disabling this diagnostic.

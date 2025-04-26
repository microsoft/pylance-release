## Overview

`reportUnusedVariable` is a Pylance and Pyright diagnostic that warns when a variable is defined but never used in your code. Removing unused variables helps keep your code clean, maintainable, and free of unnecessary clutter.

## Representative Issues

-   [#1925](https://github.com/microsoft/pylance-release/issues/1925): Provide a global setting in Pylance to disable all diagnostics, simplifying configuration and reducing noise.
-   [#1969](https://github.com/microsoft/pylance-release/issues/1969): Ensure that `python.analysis.indexing` is enabled to maintain an up-to-date index of available modules and symbols, which helps in providing accurate auto-import suggestions.
-   [#2840](https://github.com/microsoft/pylance-release/issues/2840): Enhance the static analysis capabilities of Pylance to include warnings for unused function parameters, similar to how it handles other unreferenced elements in the code.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#495](https://github.com/microsoft/pylance-release/issues/495): Utilize the `exclude` property in Pyright's config file to prevent analysis of unwanted folders, ensuring smoother configuration and reduced diagnostics clutter.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#1187](https://github.com/microsoft/pyright/issues/1187): Maintainers of py.typed packages should ensure that all public symbols are fully annotated with type information to facilitate compatibility and accurate type checking across different tools.
-   [#2046](https://github.com/microsoft/pyright/issues/2046): Consider providing type hints or using function parameters to avoid runtime errors and improve code correctness. Implementing a feature to report unused function parameters would be beneficial for users who rely on such checks.
-   [#2307](https://github.com/microsoft/pyright/issues/2307): Ensure that configuration settings for unused variables are correctly applied and respected by the language server.

## Common Fixes & Workarounds

1. Remove variables that are never used in your code.
2. Use underscores (`_`) for intentionally unused variables or parameters.
3. Enable `python.analysis.indexing` for better static analysis and auto-import suggestions.
4. Use the `exclude` property in your config to avoid analyzing unnecessary folders.
5. Add type hints to function parameters for clarity and correctness.
6. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedVariable) for details on configuring or disabling this diagnostic.

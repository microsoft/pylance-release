## Overview

`reportUnusedFunction` is a Pylance and Pyright diagnostic that warns when a function is defined but never used in your code. Removing unused functions helps keep your codebase clean and maintainable.

## Representative Issues

-   [#2840](https://github.com/microsoft/pylance-release/issues/2840): Enhance the static analysis capabilities of Pylance to include warnings for unused function parameters, similar to how it handles other unreferenced elements in the code.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#495](https://github.com/microsoft/pylance-release/issues/495): Utilize the `exclude` property in Pyright's config file to prevent analysis of unwanted folders, ensuring smoother configuration and reduced diagnostics clutter.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#1462](https://github.com/microsoft/pyright/issues/1462): Always verify that configuration settings are respected by CLI tools in applications, especially when dealing with library code for types.
-   [#2307](https://github.com/microsoft/pyright/issues/2307): Ensure that configuration settings for unused variables are correctly applied and respected by the language server.
-   [#5411](https://github.com/microsoft/pyright/issues/5411): Always use the explicit `AsyncGenerator` type annotation for async generator functions to avoid inconsistencies with inferred types.
-   [#5412](https://github.com/microsoft/pyright/issues/5412): When using `type(self)` as a constructor in a generic class, ensure to dynamically generate the correct specialized type for subclasses.
-   [#6747](https://github.com/microsoft/pyright/issues/6747): When using private functions within a module, ensure that the `reportUnusedFunction` check is disabled to avoid false positives in static analysis tools like Pyright.

## Common Fixes & Workarounds

1. Remove functions that are never called in your code.
2. Use underscores (`_`) for intentionally unused function parameters.
3. Use the `exclude` property in your config to avoid analyzing unnecessary folders.
4. Add type hints and use explicit type annotations for clarity.
5. Disable `reportUnusedFunction` for private functions if needed to avoid false positives.
6. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedFunction) for details on configuring or disabling this diagnostic.

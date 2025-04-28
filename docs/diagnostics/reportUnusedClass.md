## Overview

`reportUnusedClass` is a Pylance and Pyright diagnostic that warns when a class is defined but never used in your code. Removing unused classes helps keep your codebase clean and maintainable.

## Representative Issues

-   [#2840](https://github.com/microsoft/pylance-release/issues/2840): Enhance the static analysis capabilities of Pylance to include warnings for unused function parameters, similar to how it handles other unreferenced elements in the code.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#3793](https://github.com/microsoft/pylance-release/issues/3793): Ensure that the configuration settings for Pylance/Pyright are correctly applied to suppress errors in Python library files.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.
-   [#2307](https://github.com/microsoft/pyright/issues/2307): Ensure that configuration settings for unused variables are correctly applied and respected by the language server.
-   [#5411](https://github.com/microsoft/pyright/issues/5411): Always use the explicit `AsyncGenerator` type annotation for async generator functions to avoid inconsistencies with inferred types.
-   [#5412](https://github.com/microsoft/pyright/issues/5412): When using `type(self)` as a constructor in a generic class, ensure to dynamically generate the correct specialized type for subclasses.
-   [#9745](https://github.com/microsoft/pyright/issues/9745): Ensure that configuration files are correctly placed in the project root and properly formatted to enable effective Pyright settings within the development environment.

## Common Fixes & Workarounds

1. Remove classes that are never used in your code.
2. Use the `exclude` property in your config to avoid analyzing unnecessary folders.
3. Add type hints and use explicit type annotations for clarity.
4. Ensure configuration files are correctly placed and formatted for your project.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedClass) for details on configuring or disabling this diagnostic.

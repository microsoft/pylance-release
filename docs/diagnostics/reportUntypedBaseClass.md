## Overview

`reportUntypedBaseClass` flags cases where a class inherits from a base class that lacks type information. This diagnostic helps ensure that all base classes are properly typed, improving static analysis and code reliability.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#1759](https://github.com/microsoft/pyright/issues/1759): Ensure that libraries used in a project include type information or provide stub files.
-   [#2912](https://github.com/microsoft/pyright/issues/2912): Use type aliases to explicitly define base classes for subclasses.
-   [#3251](https://github.com/microsoft/pyright/issues/3251): Pyright should support namespace packages to align with modern Python packaging techniques.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure comments in TOML files use correct line endings and do not contain unsupported control characters.

## Common Fixes & Workarounds

1. Use base classes that include type information or provide type stubs for third-party libraries.
2. Use type aliases to explicitly define base classes for subclasses.
3. Ensure all necessary packages are installed in your environment.
4. Exclude unnecessary folders from analysis to improve performance.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUntypedBaseClass) for details on configuring or disabling this diagnostic.

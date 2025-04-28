## Overview

`reportUnknownParameterType` is a diagnostic in Pylance and Pyright that warns when a function or method parameter has an unknown type. This helps catch missing or ambiguous type annotations, improving code clarity and type safety.

## Representative Issues

-   [#4382](https://github.com/microsoft/pylance-release/issues/4382): Ensure that the correct version of static analysis tools is used and verify that all necessary dependencies, including type stubs, are correctly installed.
-   [#5202](https://github.com/microsoft/pylance-release/issues/5202): Always provide detailed type annotations in library stubs to enhance the accuracy of static analysis tools like Pylance.
-   [#1117](https://github.com/microsoft/pyright/issues/1117): Always include type hints for all class members to help static analysis tools like Pyright accurately infer types.
-   [#1759](https://github.com/microsoft/pyright/issues/1759): Ensure that libraries used in a project include type information or provide stub files to aid static analysis tools like pyright.

## Common Fixes & Workarounds

1. Add explicit type annotations to all function and method parameters.
2. Use type stubs or install third-party stubs for external libraries.
3. Review and update type hints in your codebase for completeness.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownParameterType) for options to adjust or suppress this diagnostic if needed.

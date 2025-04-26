## Overview

`reportUnknownVariableType` is a diagnostic in Pylance and Pyright that warns when a variable's type cannot be determined. This helps catch missing or ambiguous type information, improving code reliability and maintainability.

## Representative Issues

-   [#1023](https://github.com/microsoft/pylance-release/issues/1023): Avoid using literal types within tuples for collection elements to prevent incorrect type inference and concatenation issues.
-   [#3192](https://github.com/microsoft/pylance-release/issues/3192): Ensure matplotlib type stubs match the library's actual return types, especially for subscriptable objects like ndarray and subplot arrays.
-   [#4382](https://github.com/microsoft/pylance-release/issues/4382): Ensure that the correct version of static analysis tools is used and verify that all necessary dependencies, including type stubs, are correctly installed.
-   [#5648](https://github.com/microsoft/pylance-release/issues/5648): Ensure that the `py.typed` file is correctly configured and placed to be recognized by Pylance's type checking system.

## Common Fixes & Workarounds

1. Add explicit type annotations to variables where possible.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify variable types where needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownVariableType) for options to adjust or suppress this diagnostic if needed.

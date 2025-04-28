## Overview

`reportUnknownMemberType` is a diagnostic in Pylance and Pyright that warns when the type of a class or object member cannot be determined. This helps catch missing or ambiguous type information for members, improving static analysis and code safety.

## Representative Issues

-   [#1449](https://github.com/microsoft/pylance-release/issues/1449): Ensure that the configuration file specified in a project is correctly referenced and applied by the development environment.
-   [#1455](https://github.com/microsoft/pylance-release/issues/1455): Exclude third-party package directories like **pypackages** from analysis and configure paths explicitly in pyproject.toml for accurate type checking.
-   [#1997](https://github.com/microsoft/pylance-release/issues/1997): Implement more specific analysis rules or allow for different severity levels to be configured for `reportUnknownMemberType`.
-   [#2071](https://github.com/microsoft/pylance-release/issues/2071): Ensure that type stubs are correctly imported using the `X as X` form.
-   [#3084](https://github.com/microsoft/pylance-release/issues/3084): Ensure that the library you are using includes a "py.typed" file to provide accurate type information for Pylance.

## Common Fixes & Workarounds

1. Add explicit type annotations to class and object members where possible.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify member types where needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownMemberType) for options to adjust or suppress this diagnostic if needed.

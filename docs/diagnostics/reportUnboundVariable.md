## Overview

`reportUnboundVariable` flags cases where a variable is referenced before it has been assigned a value in the current scope. This diagnostic helps catch potential runtime errors and ensures variables are always initialized before use.

## Representative Issues

-   [#2438](https://github.com/microsoft/pylance-release/issues/2438): Always ensure that variables are declared and assigned a value before they are used.
-   [#3853](https://github.com/microsoft/pylance-release/issues/3853): Configure Pylance's packageIndexDepths appropriately for packages and ensure the correct Python environment is active to enable accurate auto-import suggestions.
-   [#3855](https://github.com/microsoft/pylance-release/issues/3855): Ensure Python indexing is enabled in VSCode settings to support auto-import functionality for external packages.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#4497](https://github.com/microsoft/pylance-release/issues/4497): Configure the type checking mode to 'basic' to ensure that unbound variables within functions are reported as errors.
-   [#5073](https://github.com/microsoft/pylance-release/issues/5073): Use conditional imports in conjunction with type checking directives to manage module availability and avoid unbound variable errors.
-   [#509](https://github.com/microsoft/pylance-release/issues/509): Ensure that Pylance respects the user's configuration for disabling linting, allowing users to rely solely on external tools like flake8.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#5901](https://github.com/microsoft/pylance-release/issues/5901): Ensure that static type checkers are configured to flag potential unbound variables as errors in your code.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer `typing.Dict` over `dict[t, t]` for compatibility across Python versions.

## Common Fixes & Workarounds

1. Always assign a value to variables before referencing them in any code path.
2. Use conditional logic carefully to ensure variables are initialized in all branches before use.
3. Set `python.analysis.typeCheckingMode` to 'basic' or stricter in VS Code to catch more unbound variable issues.
4. Use `# pyright: ignore[reportUnboundVariable]` to suppress this diagnostic for special cases.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnboundVariable) for more details.

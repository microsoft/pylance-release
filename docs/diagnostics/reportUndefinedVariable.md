## Overview

`reportUndefinedVariable` flags cases where a variable is used before it is defined or assigned a value. This diagnostic helps catch potential runtime errors and improves code reliability by ensuring all variables are properly declared before use.

## Representative Issues

-   [#2334](https://github.com/microsoft/pylance-release/issues/2334): Implement a configuration mechanism in Pylance to allow users to define custom lists of strings for context-specific variables, enhancing the accuracy of static analysis.
-   [#2438](https://github.com/microsoft/pylance-release/issues/2438): Always ensure that variables are declared and assigned a value before they are used.
-   [#3356](https://github.com/microsoft/pylance-release/issues/3356): Ensure that static analysis tools like Pylance are aware of any custom paths or modules added during startup to avoid unresolved import errors.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#4497](https://github.com/microsoft/pylance-release/issues/4497): Configure the type checking mode to 'basic' to ensure that unbound variables within functions are reported as errors.
-   [#509](https://github.com/microsoft/pylance-release/issues/509): Ensure that Pylance respects the user's configuration for disabling linting, allowing users to rely solely on external tools like flake8.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer `typing.Dict` over `dict[t, t]` for compatibility across Python versions.
-   [#3229](https://github.com/microsoft/pyright/issues/3229): Use `# pyright: ignore[rule-name]` to suppress specific diagnostics rather than `# type: ignore`.

## Common Fixes & Workarounds

1. Always declare and assign a value to variables before using them.
2. Check for typos in variable names that may lead to undefined variable errors.
3. Configure extra analysis paths if using custom startup scripts or modules.
4. Set `python.analysis.typeCheckingMode` to 'basic' or stricter in VS Code to catch more undefined variable issues.
5. Use `# pyright: ignore[reportUndefinedVariable]` to suppress this diagnostic for special cases.
6. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUndefinedVariable) for more details.

## Overview

`reportMissingModuleSource` is a diagnostic in Pylance and Pyright that warns you when an imported module is found, but its source code cannot be located. This often happens with compiled modules, missing files, or misconfigured environments, and can affect features like IntelliSense and type checking.

## Representative Issues

-   [#2202](https://github.com/microsoft/pylance-release/issues/2202): Ensure all necessary modules are installed in the Python environment specified for the project.
-   [#2411](https://github.com/microsoft/pylance-release/issues/2411): Ensure the correct Python environment is selected and check for any configuration issues that might be preventing the error message from appearing.
-   [#242](https://github.com/microsoft/pylance-release/issues/242): Always include type stubs ('.pyi' files) for compiled Python modules to facilitate correct intellisense functionality in tools like Pylance.
-   [#295](https://github.com/microsoft/pylance-release/issues/295): Ensure that Pylance is correctly configured to minimize unnecessary diagnostics and errors, especially those related to missing type stubs.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#4976](https://github.com/microsoft/pylance-release/issues/4976): Ensure that static analysis tools are configured correctly to recognize all necessary modules, or use runtime checks if dynamic imports are involved.
-   [#5073](https://github.com/microsoft/pylance-release/issues/5073): Use conditional imports in conjunction with type checking directives to manage module availability and avoid unbound variable errors.
-   [#509](https://github.com/microsoft/pylance-release/issues/509): Ensure that Pylance respects the user's configuration for disabling linting, allowing users to rely solely on external tools like flake8.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#1585](https://github.com/microsoft/pyright/issues/1585): Ensure that all necessary Python libraries and modules are installed in the GitHub Actions environment to avoid import errors when running static analysis tools like pyright.
-   [#3314](https://github.com/microsoft/pyright/issues/3314): When defining dictionaries with mixed key and value types, specify the exact types to enhance type inference and reduce ambiguity.
-   [#4286](https://github.com/microsoft/pyright/issues/4286): Ensure that Protocol classes are consistently imported from the `typing_extensions` module to avoid runtime issues with static type checkers.
-   [#5577](https://github.com/microsoft/pyright/issues/5577): Ensure the correct Python environment is configured and that all required libraries are properly installed to avoid import errors.
-   [#7060](https://github.com/microsoft/pyright/issues/7060): Ensure that the Python library in question is correctly installed and recognized by the development environment, possibly requiring installation of additional dependencies or configuration for type hints.
-   [#7832](https://github.com/microsoft/pyright/issues/7832): Ensure that type hints are explicitly defined for functions and methods in libraries to avoid runtime errors during type checking.
-   [#8558](https://github.com/microsoft/pyright/issues/8558): Ensure that callable objects are correctly handled and compatible with the expected types in static type checking contexts.
-   [#8902](https://github.com/microsoft/pyright/issues/8902): Ensure that static analysis tools are configured to handle inline script metadata correctly when using `pipx run` for scripts that depend on non-standard libraries.

## Common Fixes & Workarounds

1. Install the required module or package in your Python environment.
2. Add or update type stubs (`.pyi` files) for compiled or missing modules.
3. Check your Python environment and ensure the correct interpreter is selected.
4. Use conditional imports and type checking guards for platform-specific or optional modules.
5. Adjust your `pyrightconfig.json` or `pyproject.toml` to include or exclude relevant paths and directories.
6. Use runtime checks or fallback logic for dynamic imports.

For more details on configuring this diagnostic, see the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingModuleSource).


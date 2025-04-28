## Overview

`reportCallInDefaultInitializer` is a Pylance and Pyright diagnostic that warns when a function call is used as a default value for a function parameter. This can lead to unexpected behavior because the call is evaluated only once, not each time the function is called.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.
-   [#2721](https://github.com/microsoft/pyright/issues/2721): When using `iscoroutine` or similar type guards to conditionally check and assign types, consider using `isinstance` for clearer control over the type narrowing process.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
-   [#5411](https://github.com/microsoft/pyright/issues/5411): Always use the explicit `AsyncGenerator` type annotation for async generator functions to avoid inconsistencies with inferred types.
-   [#5412](https://github.com/microsoft/pyright/issues/5412): When using `type(self)` as a constructor in a generic class, ensure to dynamically generate the correct specialized type for subclasses.
-   [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing and ensure clear variable identification.
-   [#7193](https://github.com/microsoft/pyright/issues/7193): After an `isinstance` check with a specific type, the variable should be explicitly set to that type or a more specific type to avoid false positive errors in static analysis tools.

## Common Fixes & Workarounds

1. Avoid using function calls as default parameter values; use `None` and set the value inside the function if needed.
2. Use explicit type annotations for clarity and to help static analysis tools.
3. Ensure all abstract methods are implemented in subclasses.
4. Prefer `typing.Dict` over `dict[t, t]` for type compatibility.
5. Use `isinstance` for type checks and type narrowing.
6. Use explicit type annotations for async generators and other advanced types.
7. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallInDefaultInitializer) for details on configuring or disabling this diagnostic.

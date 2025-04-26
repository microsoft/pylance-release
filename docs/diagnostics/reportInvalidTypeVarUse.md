## Overview

`reportInvalidTypeVarUse` detects improper or inconsistent usage of `TypeVar` in Python code. This diagnostic helps ensure that type variables are used correctly in generic functions, type aliases, and overloads, preventing subtle type errors and improving code maintainability.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#1147](https://github.com/microsoft/pyright/issues/1147): Ensure that TypeVar is used consistently and correctly within the scope of a generic function or type alias to maintain proper runtime behavior.
-   [#1894](https://github.com/microsoft/pyright/issues/1894): Ensure that the use of TypeVar in function overloads is consistent and correctly defined according to the Pyright documentation.
-   [#2315](https://github.com/microsoft/pyright/issues/2315): Ensure that TypeVars bound types do not introduce cyclical dependencies, as this can lead to inconsistencies in static type checking.
-   [#2509](https://github.com/microsoft/pyright/issues/2509): Ensure that TypeVars defined in generic function signatures are used within the function to maintain proper type checking and avoid redundant warnings.
-   [#3288](https://github.com/microsoft/pyright/issues/3288): Ensure that TypeVars used within function overloads are properly constrained to avoid runtime issues and improve static type checking with tools like pyright.
-   [#3381](https://github.com/microsoft/pyright/issues/3381): Consider implementing specific error codes in Pyright that MyPy can understand and suppress, reducing manual intervention.

## Common Fixes & Workarounds

1. Ensure that every `TypeVar` is used consistently within the scope of a generic function, class, or type alias.
2. Avoid cyclical dependencies when binding `TypeVar` types.
3. When using function overloads, make sure `TypeVar` usage is consistent and properly constrained across all overloads.
4. Remove or adjust unused or redundant `TypeVar` definitions to avoid unnecessary warnings.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInvalidTypeVarUse) for details on configuring this diagnostic.
6. Suppress specific diagnostics with `# pyright: reportInvalidTypeVarUse=false` if needed for special cases.

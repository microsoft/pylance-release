## Overview

`reportInvalidStubStatement` flags statements in Python type stub (`.pyi`) files that are not valid according to the stub file specification. This diagnostic helps ensure that stubs are syntactically correct and compatible with static type checkers.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types to avoid runtime errors and type checking issues.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#3332](https://github.com/microsoft/pyright/issues/3332): Always specify the module path when referencing submodules within larger modules to avoid syntax and import errors.

## Common Fixes & Workarounds

1. Only use valid stub syntax in `.pyi` files (e.g., type annotations, function/class definitions, and docstrings).
2. Avoid executable statements or runtime logic in stub files.
3. Ensure all imports and references in stubs use the correct module paths.
4. Match default argument types to their annotated parameter types.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInvalidStubStatement) for details on configuring this diagnostic.
6. Suppress this diagnostic with `# pyright: reportInvalidStubStatement=false` if you have a special case.

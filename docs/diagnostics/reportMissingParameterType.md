## Overview

`reportMissingParameterType` is a diagnostic in Pylance and Pyright that warns when a function or method parameter is missing a type annotation. This helps catch missing or ambiguous type information, improving code clarity and type safety.

## Representative Issues

-   [#3078](https://github.com/microsoft/pyright/issues/3078): Always provide type hints for function parameters to avoid diagnostic errors in static analysis tools.
-   [#2735](https://github.com/microsoft/pyright/issues/2735): Provide specific configuration options for type check diagnostics to improve code maintainability.
-   [#774](https://github.com/microsoft/pyright/issues/774): When using decorators that modify the signature of a function, use TypeVars bound to Callable types to maintain the original signatures.

## Common Fixes & Workarounds

1. Add explicit type annotations to all function and method parameters.
2. Use type stubs or install third-party stubs for external libraries.
3. Review and update type hints in your codebase for completeness.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingParameterType) for options to adjust or suppress this diagnostic if needed.

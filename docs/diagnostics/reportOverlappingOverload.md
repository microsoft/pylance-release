## Overview

`reportOverlappingOverload` is a diagnostic in Pylance and Pyright that warns when function overloads overlap, meaning multiple overload signatures could match the same call. This can lead to ambiguity and unexpected behavior in type checking and code execution.

## Representative Issues

-   [#10014](https://github.com/microsoft/pyright/issues/10014): Avoid using default keyword arguments in overloads to prevent false positives for overlapping overloads.
-   [#7084](https://github.com/microsoft/pyright/issues/7084): Avoid using multiple TypeVars in function signatures without a clear reason to distinguish different overloads.
-   [#9603](https://github.com/microsoft/pyright/issues/9603): Ensure that `join` returns the appropriate type based on the elements in the list, avoiding mismatches between literal and non-literal strings.

## Common Fixes & Workarounds

1. Make overload signatures mutually exclusive so that only one matches any given call.
2. Avoid using default keyword arguments in overloads.
3. Use clear and distinct TypeVars only when necessary.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOverlappingOverload) for options to adjust or suppress this diagnostic if needed.

## Overview

`reportUnnecessaryContains` is a diagnostic in Pylance and Pyright that warns when a membership test (like `in`) is unnecessary or always evaluates to the same result due to type incompatibility or redundancy. This helps catch logic errors and keeps code clean and efficient.

## Representative Issues

-   [#5218](https://github.com/microsoft/pyright/issues/5218): Ensure that collection membership checks are performed with compatible types to avoid unnecessary diagnostics.
-   [#6087](https://github.com/microsoft/pyright/issues/6087): Adjust `reportUnnecessaryContains` to correctly handle cases where values are equal but of different types.
-   [#7354](https://github.com/microsoft/pyright/issues/7354): Direct comparisons between objects of different types will always evaluate to False unless explicitly overridden.

## Common Fixes & Workarounds

1. Ensure membership tests are performed between compatible types.
2. Refactor code to remove redundant or logically impossible membership checks.
3. Use explicit type conversions or assertions where needed for clarity and correctness.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnnecessaryContains) for options to adjust or suppress this diagnostic if needed.

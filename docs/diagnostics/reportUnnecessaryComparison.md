## Overview

`reportUnnecessaryComparison` is a diagnostic in Pylance and Pyright that warns when a comparison is unnecessary or always evaluates to the same result due to type incompatibility or redundancy. This helps catch logic errors and keeps code clean and efficient.

## Representative Issues

-   [#1744](https://github.com/microsoft/pyright/issues/1744): Always ensure that the types being compared have a clear overlap or use type checking to handle comparisons, especially in conditional statements.
-   [#4861](https://github.com/microsoft/pyright/issues/4861): Ensure that comparisons between `bool` and `Literal[0, 1]` are explicitly converted to `bool` type to avoid false positives.
-   [#5218](https://github.com/microsoft/pyright/issues/5218): Ensure that collection membership checks are performed with compatible types to avoid unnecessary diagnostics.

## Common Fixes & Workarounds

1. Compare values of compatible types to avoid unnecessary or always-false comparisons.
2. Refactor code to remove redundant or logically impossible comparisons.
3. Use explicit type conversions where needed for clarity and correctness.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnnecessaryComparison) for options to adjust or suppress this diagnostic if needed.

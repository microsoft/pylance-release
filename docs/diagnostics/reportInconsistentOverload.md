## Overview

`reportInconsistentOverload` is a diagnostic in Pylance and Pyright that warns when function overloads are inconsistent—such as when overload signatures overlap or do not match the implementation. This helps catch subtle bugs and ensures that type hints for overloaded functions are accurate and unambiguous.

## Representative Issues

-   [#9603](https://github.com/microsoft/pyright/issues/9603): Ensure that `join` returns the appropriate type based on the elements in the list, avoiding mismatches between literal and non-literal strings.

## Common Fixes & Workarounds

1. Make sure that overload signatures do not overlap and are mutually exclusive.
2. Ensure that the implementation of the function matches at least one of the overload signatures.
3. Use precise and non-overlapping type annotations for each overload.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInconsistentOverload) for options to adjust or suppress this diagnostic if needed.

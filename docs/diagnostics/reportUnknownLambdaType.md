## Overview

`reportUnknownLambdaType` is a diagnostic in Pylance and Pyright that warns when the type of a lambda function cannot be determined. This helps catch missing or ambiguous type information for lambdas, improving static analysis and code safety.

## Representative Issues

-   [#3347](https://github.com/microsoft/pyright/issues/3347): Use keyword-only arguments in lambda functions when assigning them to protocols with specific argument requirements.
-   [#7039](https://github.com/microsoft/pyright/issues/7039): Ensure that the `owner` argument in the `__set_name__` method can be used to infer the type of the descriptor.

## Common Fixes & Workarounds

1. Add explicit type annotations to lambda parameters and return types where possible.
2. Use protocols or type hints to clarify expected lambda signatures.
3. Refactor code to use named functions with explicit types if needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownLambdaType) for options to adjust or suppress this diagnostic if needed.

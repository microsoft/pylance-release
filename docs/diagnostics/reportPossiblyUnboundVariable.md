## Overview

`reportPossiblyUnboundVariable` is a diagnostic in Pylance and Pyright that warns when a variable might be used before it is assigned a value. This helps catch potential runtime errors due to uninitialized variables, especially in conditional or loop constructs.

## Representative Issues

-   [#5901](https://github.com/microsoft/pylance-release/issues/5901): Ensure that static type checkers are configured to flag potential unbound variables as errors in your code.
-   [#7822](https://github.com/microsoft/pyright/issues/7822): Always initialize variables that are assigned within a loop prior to the loop to avoid issues with static type checkers.
-   [#7879](https://github.com/microsoft/pyright/issues/7879): Ensure that the configuration setting used for detecting unbound variables in code aligns with the latest documentation and tool capabilities.
-   [#8748](https://github.com/microsoft/pyright/issues/8748): Ensure variables are initialized before they are accessed in loops to avoid potential unbound variable errors.
-   [#9299](https://github.com/microsoft/pyright/issues/9299): Ensure the `pyright` configuration uses "standard" type checking mode for comprehensive variable binding checks.
-   [#9638](https://github.com/microsoft/pyright/issues/9638): Ensure that the static analyzer reports variables as possibly unbound when they are deleted in enclosing scopes.

## Common Fixes & Workarounds

1. Always initialize variables before using them, especially in loops and conditionals.
2. Review all code paths to ensure variables are assigned before access.
3. Use default values or `None` initialization when unsure if a variable will be set.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportPossiblyUnboundVariable) for options to adjust or suppress this diagnostic if needed.

## Overview

`reportUnnecessaryIsInstance` is a diagnostic in Pylance and Pyright that warns when an `isinstance` check is unnecessary—such as when the type is already known or the check is redundant. This helps keep code clean and avoids misleading or unreachable code paths.

## Representative Issues

-   [#2080](https://github.com/microsoft/pyright/issues/2080): Warn or error on unreachable statements/expressions, providing clearer diagnostic messages.
-   [#3065](https://github.com/microsoft/pyright/issues/3065): When using `isinstance` in an exhaustive check where all possible types are covered by `Union`, suppress the warning by adding an `else` clause.

## Common Fixes & Workarounds

1. Remove unnecessary `isinstance` checks when the type is already known or guaranteed.
2. Refactor code to avoid unreachable or redundant branches.
3. Add an `else` clause when using exhaustive type checks with `Union` types.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnnecessaryIsInstance) for options to adjust or suppress this diagnostic if needed.

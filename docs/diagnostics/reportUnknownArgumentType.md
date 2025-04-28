## Overview

`reportUnknownArgumentType` is a diagnostic in Pylance and Pyright that warns when an argument passed to a function or method has an unknown type. This helps catch missing or ambiguous type information, improving code reliability and maintainability.

## Representative Issues

-   [#1759](https://github.com/microsoft/pyright/issues/1759): Ensure that libraries used in a project include type information or provide stub files to aid static analysis tools like pyright.
-   [#3066](https://github.com/microsoft/pyright/issues/3066): Enhance the diagnostic tool to differentiate between completely unknown and partially unknown variable types.
-   [#3347](https://github.com/microsoft/pyright/issues/3347): Use keyword-only arguments in lambda functions when assigning them to protocols with specific argument requirements.

## Common Fixes & Workarounds

1. Add or improve type annotations for function arguments.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify argument types where possible.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownArgumentType) for options to adjust or suppress this diagnostic if needed.

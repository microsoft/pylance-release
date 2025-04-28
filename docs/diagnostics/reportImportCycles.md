## Overview

`reportImportCycles` is a diagnostic that flags cycles in your Python import graph, which can lead to confusing bugs and maintenance issues. Cyclic imports can cause modules to be partially initialized, resulting in runtime errors or unexpected behavior.

## Representative Issues

-   [#3003](https://github.com/microsoft/pylance-release/issues/3003): Ensure Pylint plugins are installed and configured for correct diagnostics.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Default argument types in functions should match annotated parameter types.
-   [#3853](https://github.com/microsoft/pylance-release/issues/3853): Configure `packageIndexDepths` and ensure the correct Python environment for auto-imports.
-   [#3855](https://github.com/microsoft/pylance-release/issues/3855): Enable Python indexing in VSCode for auto-imports.
-   [#4012](https://github.com/microsoft/pylance-release/issues/4012): Override diagnostic severity for import cycles globally in pyright.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in type stubs between Pyright CLI and Pylance settings.
-   [#495](https://github.com/microsoft/pylance-release/issues/495): Use the `exclude` property in config files to prevent analysis of unwanted folders.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Customize diagnostic rule severities by type checking mode.
-   [#531](https://github.com/microsoft/pylance-release/issues/531): Use `# pyright: reportImportCycles=none` to suppress cyclical import warnings for a file/module.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure abstract base classes implement all abstract methods.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv for performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer `typing.Dict` over `dict[t, t]` for compatibility.

## Common Fixes & Workarounds

1. Refactor code to break import cycles, possibly by moving imports inside functions or reorganizing modules.
2. Use the `exclude` property in your `pyrightconfig.json` to avoid analyzing unnecessary folders.
3. Suppress specific import cycle warnings with `# pyright: reportImportCycles=none` in affected files.
4. Ensure your Python environment and type stubs are consistent and properly configured.
5. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportImportCycles) for details on configuring this rule.

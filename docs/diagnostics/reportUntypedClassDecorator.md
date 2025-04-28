## Overview

`reportUntypedClassDecorator` flags cases where a class decorator does not have type information, which can obscure the type of the decorated class. This diagnostic helps ensure that decorators are properly typed, improving static analysis and code reliability.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#324](https://github.com/microsoft/pyright/issues/324): Ensure the 'reportMissingImports' setting in pyright is set to true to maintain default behavior.
-   [#4173](https://github.com/microsoft/pyright/issues/4173): Implement per-module configuration settings in Pyright for more flexible type checking.
-   [#836](https://github.com/microsoft/pyright/issues/836): Manage configuration settings within the IDE to avoid conflicts with project-specific configurations.
-   [#8681](https://github.com/microsoft/pyright/issues/8681): Avoid circular dependencies where decorators depend on class fields defined later.

## Common Fixes & Workarounds

1. Add type annotations to class decorators to clarify the type of the decorated class.
2. Refactor code to avoid circular dependencies between decorators and class fields.
3. Use per-module configuration settings to adjust diagnostics as needed.
4. Exclude unnecessary folders from analysis to improve performance.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUntypedClassDecorator) for details on configuring or disabling this diagnostic.

## Overview

`reportTypeCommentUsage` flags cases where type comments (e.g., `# type: ...`) are used in ways that are deprecated or not recommended. This diagnostic helps encourage the use of modern type annotation syntax and ensures compatibility with static type checkers.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities by type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use correct line endings and do not contain unsupported control characters.

## Common Fixes & Workarounds

1. Use modern type annotation syntax instead of type comments where possible.
2. Refactor code to remove deprecated or unnecessary type comments.
3. Exclude unnecessary folders from analysis to improve performance.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportTypeCommentUsage) for details on configuring or disabling this diagnostic.

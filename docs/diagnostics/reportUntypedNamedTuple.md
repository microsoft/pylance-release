## Overview

`reportUntypedNamedTuple` flags cases where a `NamedTuple` is defined without explicit type annotations for its fields. This diagnostic helps ensure that all fields in a `NamedTuple` are properly typed, improving static analysis and code reliability.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax for compatibility across Python versions.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use correct line endings and do not contain unsupported control characters.

## Common Fixes & Workarounds

1. Add explicit type annotations to all fields in your `NamedTuple` definitions.
2. Use the `typing.NamedTuple` class with type annotations for better static analysis.
3. Exclude unnecessary folders from analysis to improve performance.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUntypedNamedTuple) for details on configuring or disabling this diagnostic.

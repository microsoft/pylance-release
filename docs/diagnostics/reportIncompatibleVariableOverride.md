## Overview

`reportIncompatibleVariableOverride` flags cases where a variable in a subclass does not match the type of the variable it overrides in the base class. This diagnostic helps ensure that subclass variables are compatible with their base class counterparts, improving code reliability and maintainability.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#4777](https://github.com/microsoft/pylance-release/issues/4777): Balance comprehensive exclusion with inclusion of necessary workspace components in `exclude` paths.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities by type checking mode.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#1804](https://github.com/microsoft/pyright/issues/1804): Report errors when generics are overridden with incompatible types.
-   [#2678](https://github.com/microsoft/pyright/issues/2678): Ensure that overridden properties are explicitly typed to match the abstract base class declaration.
-   [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use correct line endings and do not contain unsupported control characters.
-   [#6814](https://github.com/microsoft/pyright/issues/6814): Ensure that overridden symbols in subclasses are correctly aligned with the base class definitions.
-   [#8862](https://github.com/microsoft/pyright/issues/8862): Configure type checking settings to avoid false positive errors related to undefined variables.

## Common Fixes & Workarounds

1. Ensure that overridden variables in subclasses match the type of the base class variable.
2. Add explicit type annotations to overridden variables.
3. Align subclass definitions with base class definitions to avoid type violations.
4. Exclude unnecessary folders from analysis to improve performance.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportIncompatibleVariableOverride) for details on configuring or disabling this diagnostic.

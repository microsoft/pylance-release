## Overview

`reportDeprecated` is a Pylance and Pyright diagnostic that warns when your code uses deprecated functions, classes, or modules. This helps you keep your codebase up to date and avoid using features that may be removed in future versions of libraries or Python itself.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.

## Examples

```python
from typing_extensions import deprecated

@deprecated("Use new_function instead")
def old_function() -> None:
    pass

old_function()  # Warning: "old_function" is deprecated
```

**Fix — use the recommended alternative:**

```python
def new_function() -> None:
    pass

new_function()  # No warning
```

## Common Fixes & Workarounds

1. Replace deprecated functions, classes, or modules with their recommended alternatives.
2. Review library and Python release notes for deprecation warnings and migration guides.
3. Refactor code to remove or update deprecated usages.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportDeprecated) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

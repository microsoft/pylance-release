## Overview

`reportUntypedClassDecorator` flags cases where a class decorator does not have type information, which can obscure the type of the decorated class. This diagnostic helps ensure that decorators are properly typed, improving static analysis and code reliability.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
- [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
- [#324](https://github.com/microsoft/pyright/issues/324): Ensure the 'reportMissingImports' setting in pyright is set to true to maintain default behavior.
- [#4173](https://github.com/microsoft/pyright/issues/4173): Implement per-module configuration settings in Pyright for more flexible type checking.
- [#836](https://github.com/microsoft/pyright/issues/836): Manage configuration settings within the IDE to avoid conflicts with project-specific configurations.
- [#8681](https://github.com/microsoft/pyright/issues/8681): Avoid circular dependencies where decorators depend on class fields defined later.

## Examples

**Error:**

```python
from untyped_lib import register  # 'register' has no type info

@register  # Decorator return type is unknown
class MyPlugin:
    pass
```

**Fix — add type annotations to the decorator:**

```python
from typing import TypeVar

T = TypeVar("T", bound=type)

def register(cls: T) -> T:
    # registration logic
    return cls

@register
class MyPlugin:
    pass
```

Or install/provide type stubs for the library.

## Common Fixes & Workarounds

1. Add type annotations to class decorators to clarify the type of the decorated class.
2. Refactor code to avoid circular dependencies between decorators and class fields.
3. Use per-module configuration settings to adjust diagnostics as needed.
4. Exclude unnecessary folders from analysis to improve performance.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUntypedClassDecorator) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

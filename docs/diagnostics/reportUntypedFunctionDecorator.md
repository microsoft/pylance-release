## Overview

`reportUntypedFunctionDecorator` is a Pylance and Pyright diagnostic that warns when a decorator obscures the type of the function it decorates. This helps enforce type safety and improves code clarity, especially when using decorators from libraries or frameworks.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
- [#6300](https://github.com/microsoft/pylance-release/issues/6300): When configuring file exclusions in a Python project, it's crucial to accurately exclude unnecessary folders like .venv to improve performance.
- [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.
- [#1187](https://github.com/microsoft/pyright/issues/1187): Maintainers of py.typed packages should ensure that all public symbols are fully annotated with type information to facilitate compatibility and accurate type checking across different tools.
- [#1443](https://github.com/microsoft/pyright/issues/1443): Use comments to indicate strict type checking for new files and configure specific directories in the pyrightconfig.json file to gradually enable strict type-checking.
- [#324](https://github.com/microsoft/pyright/issues/324): Ensure that the 'reportMissingImports' setting in pyright is set to true to maintain default behavior for missing import diagnostics.
- [#4330](https://github.com/microsoft/pyright/issues/4330): When using `attrs` decorators like `@x.validator`, ensure that the type of the field is explicitly defined to avoid misinterpretation by static type checkers like pyright.
- [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
- [#5370](https://github.com/microsoft/pyright/issues/5370): Pyright should support a setting to emit diagnostics on untyped function signatures, similar to `reportUnknownParameterType`, to help enforce type annotations in Python code.
- [#792](https://github.com/microsoft/pyright/issues/792): Always provide type hints for function parameters and return types to help static analysis tools like Pyright accurately determine the types of variables and members.
- [#836](https://github.com/microsoft/pyright/issues/836): When using Pyright in a VS Code environment, configuration settings should be managed within the IDE's own configuration system to avoid conflicts with project-specific configurations.

## Examples

**Error:**

```python
from untyped_lib import cache  # 'cache' has no type annotations

@cache  # Decorator obscures function type
def compute(x: int) -> int:
    return x * 2
```

**Fix — use a typed decorator or add a stub:**

```python
from functools import cache  # functools.cache is fully typed

@cache
def compute(x: int) -> int:
    return x * 2
```

If writing your own decorator, annotate it properly:

```python
from typing import Callable, TypeVar
from functools import wraps

F = TypeVar("F", bound=Callable[..., object])

def my_decorator(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # type: ignore[return-value]
```

## Common Fixes & Workarounds

1. Add type annotations to decorators that obscure the types of the functions they decorate.
2. Use type hints for decorator parameters and return values to improve static analysis and code clarity.
3. Review your code for untyped decorators and add annotations or type stubs.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUntypedFunctionDecorator) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

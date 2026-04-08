## Overview

`reportUnknownArgumentType` is a diagnostic in Pylance and Pyright that warns when an argument passed to a function or method has an unknown type. This helps catch missing or ambiguous type information, improving code reliability and maintainability.

## Representative Issues

- [#1759](https://github.com/microsoft/pyright/issues/1759): Ensure that libraries used in a project include type information or provide stub files to aid static analysis tools like pyright.
- [#3066](https://github.com/microsoft/pyright/issues/3066): Enhance the diagnostic tool to differentiate between completely unknown and partially unknown variable types.
- [#3347](https://github.com/microsoft/pyright/issues/3347): Use keyword-only arguments in lambda functions when assigning them to protocols with specific argument requirements.

## Examples

**Error:**

```python
import json

data = json.loads('{"key": 1}')  # json.loads returns Any
process(data)  # Argument type is Unknown
```

**Fix — narrow the type before passing:**

```python
import json
from typing import Any, cast

raw: Any = json.loads('{"key": 1}')
data: dict[str, int] = cast(dict[str, int], raw)
process(data)  # Argument type is now known
```

Or add a type annotation:

```python
data: dict[str, int] = json.loads('{"key": 1}')
process(data)
```

## Common Fixes & Workarounds

1. Add or improve type annotations for function arguments.
2. Use or install type stubs for third-party libraries.
3. Refactor code to clarify argument types where possible.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnknownArgumentType) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

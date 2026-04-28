## Overview

`reportGeneralTypeIssues` is a diagnostic that flags a wide range of type-related issues in Python code, such as protocol mismatches, incorrect type narrowing, and improper use of generics. Some patterns that were originally reported under this umbrella (such as assignment and return type mismatches) have since been split into more specific rules like `reportAssignmentType`, `reportReturnType`, and `reportArgumentType`.

## Examples

**Error:**

```python
from typing import final

@final
class Base:
    pass

class Child(Base):  # Error: Base class "Base" is marked final and cannot be subclassed
    pass
```

**Fix — correct the annotation or the value:**

```python
class Base:
    pass

class Child(Base):  # OK — Base is not marked final
    pass
```

Another common case — incompatible return type:

```python
def greet(name: str) -> str:
    if not name:
        return None  # 'None' is not assignable to 'str'
    return f"Hello, {name}"
```

Fix:

```python
def greet(name: str) -> str | None:
    if not name:
        return None
    return f"Hello, {name}"
```

## Representative Issues

- [#1023](https://github.com/microsoft/pylance-release/issues/1023): Avoid using literal types within tuples for collection elements to prevent incorrect type inference and concatenation issues.
- [#1034](https://github.com/microsoft/pylance-release/issues/1034): Ensure type hints match actual constructor arguments.
- [#1068](https://github.com/microsoft/pylance-release/issues/1068): Use 'TypeGuard' to indicate type checks within functions.
- [#106](https://github.com/microsoft/pylance-release/issues/106): Ensure all necessary imports are included and referenced.
- [#1094](https://github.com/microsoft/pylance-release/issues/1094): Use covariant TypeVar for assignment between related types.
- [#1095](https://github.com/microsoft/pylance-release/issues/1095): Avoid unnecessary type arguments in annotations.
- [#1274](https://github.com/microsoft/pylance-release/issues/1274): Correctly type function parameters.
- [#1290](https://github.com/microsoft/pylance-release/issues/1290): Use independent TypeVar declarations for nested generic classes.
- [#1295](https://github.com/microsoft/pylance-release/issues/1295): Ensure correct order of parent class inheritance in protocols.

## Common Fixes & Workarounds

1. Review and correct type hints and annotations throughout your code.
2. Use explicit type aliases and TypeVar declarations where needed.
3. Match type annotations to actual usage and constructor arguments.
4. Refactor code to avoid ambiguous or incorrect type usage.
5. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportGeneralTypeIssues) for details on configuring this rule.

## See Also

- [How to Use Type Narrowing to Fix Type Errors](../howto/type-narrowing.md) — narrow union types with `isinstance`, `is None` checks, and type guards
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

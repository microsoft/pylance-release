## Overview

`reportAbstractUsage` is a diagnostic in Pylance and Pyright that warns when you attempt to instantiate or use an abstract class or method that has not been fully implemented. This helps catch errors where required abstract methods are missing or not properly overridden in subclasses.

## Representative Issues

- [#7328](https://github.com/microsoft/pyright/issues/7328): Avoid calling an unimplemented abstract method from the parent class when overriding it.
- [#8017](https://github.com/microsoft/pyright/issues/8017): Ensure a clean and properly installed version of pyright to avoid errors related to corrupted installations.

## Examples

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

# Error: Cannot instantiate abstract class "Animal"
a = Animal()
```

**Fix — implement all abstract methods in a subclass:**

```python
class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

d = Dog()  # OK
```

## Common Fixes & Workarounds

1. Implement all abstract methods in subclasses before instantiating the class.
2. If overriding an abstract method, ensure the implementation is complete and does not call an unimplemented abstract method from the parent class.
3. Check for typos or signature mismatches in method definitions.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAbstractUsage) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

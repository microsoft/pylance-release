## Overview

`reportAbstractUsage` is a diagnostic in Pylance and Pyright that warns when you attempt to instantiate or use an abstract class or method that has not been fully implemented. This helps catch errors where required abstract methods are missing or not properly overridden in subclasses.

## Representative Issues

-   [#7328](https://github.com/microsoft/pyright/issues/7328): Ensure that any overridden method in a subclass calls the corresponding method in the parent class, if it exists and is abstract.
-   [#8017](https://github.com/microsoft/pyright/issues/8017): Ensure a clean and properly installed version of pyright to avoid errors related to corrupted installations.

## Common Fixes & Workarounds

1. Implement all abstract methods in subclasses before instantiating the class.
2. If overriding an abstract method, ensure the implementation is complete and does not call an unimplemented abstract method from the parent class.
3. Check for typos or signature mismatches in method definitions.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAbstractUsage) for options to adjust or suppress this diagnostic if needed.

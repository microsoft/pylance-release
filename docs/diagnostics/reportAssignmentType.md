## Overview

`reportAssignmentType` is a Pylance and Pyright diagnostic that warns when a value assigned to a variable, attribute, or parameter does not match the expected type. This helps catch type mismatches early, improving code safety and maintainability.

## Representative Issues

-   [#5564](https://github.com/microsoft/pyright/issues/5564): When overriding an abstract property in a subclass, ensure the override is consistent with the parent class definition by using `@property` methods.
-   [#7484](https://github.com/microsoft/pyright/issues/7484): When introducing new rules or changing default severities, ensure that existing configurations are backward compatible to avoid disruptions.
-   [#7665](https://github.com/microsoft/pyright/issues/7665): Static type checkers should recognize idiomatic use of `_` in function signatures and avoid raising errors unrelated to variable reassignment.
-   [#7995](https://github.com/microsoft/pyright/issues/7995): Use `ClassVar` to define class variables in metaclasses, ensuring type consistency across the class and its instances.
-   [#8067](https://github.com/microsoft/pyright/issues/8067): Always use the Literal type within a type expression and not as part of a value context to avoid such compatibility issues.
-   [#8646](https://github.com/microsoft/pyright/issues/8646): Ensure that `TypedDict` definitions are strictly adhered to when converting between them, using `NotRequired` for optional keys.
-   [#9066](https://github.com/microsoft/pyright/issues/9066): When using `classmethod` with `partial`, ensure that the partial application includes all necessary parameters to avoid type errors.
-   [#9104](https://github.com/microsoft/pyright/issues/9104): Ensure that third-party library stubs are correctly defined to avoid runtime type checking errors in static analysis tools like pyright.
-   [#9614](https://github.com/microsoft/pyright/issues/9614): Avoid redeclaring properties of classes in subclasses or within Enum definitions.

## Common Fixes & Workarounds

1. Ensure assigned values match the expected type annotations.
2. Use `@property` decorators for property overrides in subclasses.
3. Use `ClassVar` for class variables in metaclasses.
4. Avoid redeclaring properties in subclasses or Enums.
5. Use `Literal` only within type expressions, not as values.
6. Double-check third-party stubs for correct type definitions.
7. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAssignmentType) for details on configuring or disabling this diagnostic.

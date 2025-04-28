## Overview

`reportImplicitOverride` is a diagnostic in Pylance and Pyright that warns when a method or attribute in a subclass implicitly overrides a member from a superclass without an explicit `@override` decorator. This helps ensure that overrides are intentional and clear, reducing the risk of accidental bugs.

## Representative Issues

-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#7192](https://github.com/microsoft/pyright/issues/7192): Avoid redeclaring variables with the same type to prevent shadowing and ensure clear variable identification.
-   [#7193](https://github.com/microsoft/pyright/issues/7193): After an `isinstance` check, set the variable to the correct type to avoid false positives.
-   [#7281](https://github.com/microsoft/pyright/issues/7281): Ensure protected members are accessed only from within the class or subclasses.
-   [#7328](https://github.com/microsoft/pyright/issues/7328): Ensure overridden methods in subclasses call the parent method if required.
-   [#7624](https://github.com/microsoft/pyright/issues/7624): Ensure type comparisons are clear and explicit.

## Common Fixes & Workarounds

1. Use the `@override` decorator when overriding methods or attributes from a superclass.
2. Double-check that overrides are intentional and not accidental name collisions.
3. Implement all required abstract methods in subclasses.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportImplicitOverride) for options to adjust or suppress this diagnostic if needed.

## Overview

`reportIncompatibleMethodOverride` flags cases where a method in a subclass does not match the signature or return type of the method it overrides in the base class. This diagnostic helps ensure that subclass methods are compatible with their base class counterparts, improving code reliability and maintainability.

## Representative Issues

-   [#1651](https://github.com/microsoft/pylance-release/issues/1651): Always provide explicit return type annotations for properties when overriding methods.
-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities by type checking mode.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): Prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax for compatibility across Python versions.
-   [#2104](https://github.com/microsoft/pyright/issues/2104): Allow the use of NoReturn as a return type when assigning functions with matching signatures but differing return types.
-   [#2235](https://github.com/microsoft/pyright/issues/2235): Ensure that the return type of overridden methods matches or is compatible with the parent class's method.
-   [#2678](https://github.com/microsoft/pyright/issues/2678): Ensure that overridden properties are explicitly typed to match the abstract base class declaration.
-   [#3473](https://github.com/microsoft/pyright/issues/3473): Flag unused parameters in function signatures as errors.

## Common Fixes & Workarounds

1. Ensure that overridden methods in subclasses match the signature and return type of the base class method.
2. Add explicit type annotations to overridden methods and properties.
3. Implement all abstract methods when inheriting from abstract base classes.
4. Use the `typing.Dict` syntax for type annotations to ensure compatibility.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportIncompatibleMethodOverride) for details on configuring or disabling this diagnostic.

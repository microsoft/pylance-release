## Overview

`reportMissingSuperCall` is a diagnostic in Pylance and Pyright that warns when a method in a subclass should call its superclass method (typically using `super()`), but does not. This is important for correct initialization and behavior in class hierarchies, especially with `__init__` and other special methods.

## Representative Issues

-   [#3793](https://github.com/microsoft/pylance-release/issues/3793): Ensure that the configuration settings for Pylance/Pyright are correctly applied to suppress errors in Python library files.
-   [#3968](https://github.com/microsoft/pyright/issues/3968): Ensure that the `__init__` method of a class does not call `super().__init__()` unless it is necessary for proper inheritance and initialization.
-   [#5887](https://github.com/microsoft/pylance-release/issues/5887): Ensure that classes inheriting from abstract base classes implement all abstract methods.
-   [#6376](https://github.com/microsoft/pyright/issues/6376): Consider adding diagnostic rules to your configuration file instead of using the "all" default.

## Common Fixes & Workarounds

1. Add a call to `super()` in subclass methods when required for correct initialization or behavior.
2. Only call `super()` if the superclass method exists and needs to be invoked.
3. Review class hierarchies to ensure proper method chaining and initialization.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingSuperCall) for options to adjust or suppress this diagnostic if needed.

## Overview

`reportAttributeAccessIssue` is a Pylance and Pyright diagnostic that warns when your code tries to access an attribute that may not exist or is not recognized by the type checker. This helps catch typos, missing initializations, or incorrect usage of attributes in Python classes and modules.

## Representative Issues

-   [#6068](https://github.com/microsoft/pylance-release/issues/6068): Always use the correct syntax when working with type variables in Python, and ensure that you import them from the `typing` module.
-   [#10013](https://github.com/microsoft/pyright/issues/10013): When using Pyright or similar type checkers, explicitly declare attribute types at the point of assignment to help the tool recognize and manage variable types correctly.
-   [#2882](https://github.com/microsoft/pyright/issues/2882): Pyright should be capable of handling namespace packages where modules share the same namespace, by searching through all entries in PYTHONPATH to resolve imports accurately.
-   [#7352](https://github.com/microsoft/pyright/issues/7352): When working with dynamic attributes in Python, especially concerning the stdlib and modules like sys and pathlib, ensure that attribute access is handled correctly according to pyright's type checking rules.
-   [#7470](https://github.com/microsoft/pyright/issues/7470): Avoid using aliases or short-hand notations that might mislead static analysis tools; instead, use the actual class names defined in the library.
-   [#7484](https://github.com/microsoft/pyright/issues/7484): When introducing new rules or changing default severities, ensure that existing configurations are backward compatible to avoid disruptions.
-   [#7494](https://github.com/microsoft/pyright/issues/7494): When using namespace packages spread across different directories on the Python path, ensure that imports from each package are performed separately to avoid import errors in static analysis tools like Pyright.
-   [#7632](https://github.com/microsoft/pyright/issues/7632): Always ensure that instance variables are properly initialized before they are accessed in methods or functions.
-   [#8504](https://github.com/microsoft/pyright/issues/8504): Ensure `Final` and `TypeAlias` are only used directly in type annotations without being combined in a way that is not supported by the Python typing system.
-   [#9022](https://github.com/microsoft/pyright/issues/9022): Enhance execution environments in pyright to support pattern-based configurations for more efficient type checking rule application.
-   [#9104](https://github.com/microsoft/pyright/issues/9104): Ensure that third-party library stubs are correctly defined to avoid runtime type checking errors in static analysis tools like pyright.

## Common Fixes & Workarounds

1. Double-check attribute names for typos and ensure they exist on the object or class.
2. Explicitly initialize all instance variables in the class constructor (`__init__`).
3. Use the correct import and syntax for type variables and other typing constructs.
4. Avoid using aliases or shorthand for class names that may confuse static analysis tools.
5. When using namespace packages, import each module separately to avoid import errors.
6. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportAttributeAccessIssue) for details on configuring or disabling this diagnostic.

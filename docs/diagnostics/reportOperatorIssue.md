## Overview

`reportOperatorIssue` is a Pylance and Pyright diagnostic that identifies problems with the use of Python operators (such as `+`, `-`, `*`, `/`, etc.) where the operands are not type-compatible or where operator overloading is misapplied. This helps catch subtle bugs and type errors in code that uses custom classes or generics with operator methods.

## Representative Issues

-   [#7548](https://github.com/microsoft/pyright/issues/7548): Always ensure that TypeVars are properly scoped and resolved within their respective contexts to avoid type resolution failures.

## Common Fixes & Workarounds

1. Check that both operands of an operator are of compatible types or implement the appropriate dunder methods (e.g., `__add__`, `__mul__`).
2. For generic classes, ensure that `TypeVar`s are correctly scoped and resolved in all contexts where operators are used.
3. If using operator overloading, verify that the method signatures match expected types and return values.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOperatorIssue) for options to adjust or suppress this diagnostic if needed.

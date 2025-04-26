## Overview

`reportCallIssue` is a Pylance and Pyright diagnostic that identifies problems with function and method calls in your Python code. This includes incorrect argument types, missing or extra arguments, and issues with callable objects. The goal is to help you catch mistakes early and ensure your code is type-safe and compatible with static analysis tools.

## Representative Issues

-   [#7106](https://github.com/microsoft/pyright/issues/7106): Use `Annotated` with valid metadata types that align with the intended static type checking requirements.
-   [#7186](https://github.com/microsoft/pyright/issues/7186): Ensure that the types are explicitly defined and correctly annotated to avoid false positives in static type checking tools like `pyright`.
-   [#7362](https://github.com/microsoft/pyright/issues/7362): When overriding methods inherited from a parent class like `MutableMapping`, ensure that the method signatures are compatible, especially concerning optional arguments.
-   [#7370](https://github.com/microsoft/pyright/issues/7370): Always use `Annotated` with specific types rather than attempting to call it directly, unless the intention is to define a new callable type.
-   [#7382](https://github.com/microsoft/pyright/issues/7382): Ensure that the data structure used for initializing dictionaries aligns with the expected types according to the type checker.
-   [#7470](https://github.com/microsoft/pyright/issues/7470): Avoid using aliases or short-hand notations that might mislead static analysis tools; instead, use the actual class names defined in the library.
-   [#8017](https://github.com/microsoft/pyright/issues/8017): Ensure a clean and properly installed version of pyright to avoid errors related to corrupted installations.
-   [#8018](https://github.com/microsoft/pyright/issues/8018): Avoid using dynamic code constructs like `try/except` in stub files; instead, use direct imports from the appropriate module.
-   [#8377](https://github.com/microsoft/pyright/issues/8377): Ensure Pyright is invoked with the project root directory to maintain correct import resolution behavior, especially when using editable installations within the same environment.
-   [#8646](https://github.com/microsoft/pyright/issues/8646): Ensure that `TypedDict` definitions are strictly adhered to when converting between them, using `NotRequired` for optional keys.
-   [#8777](https://github.com/microsoft/pyright/issues/8777): Ensure that the argument passed to `memoryview.cast` is of an expected type, using assertions or appropriate checks for code safety and correctness.
-   [#9066](https://github.com/microsoft/pyright/issues/9066): When using `classmethod` with `partial`, ensure that the partial application includes all necessary parameters to avoid type errors.
-   [#9316](https://github.com/microsoft/pyright/issues/9316): Use function overloading to clarify type bounds for complex or combined types, especially when dealing with overloaded functions like `np.mean`.
-   [#9480](https://github.com/microsoft/pyright/issues/9480): Always provide explicit type annotations for variable assignments to avoid diagnostics errors in static analysis tools like Pyright.
-   [#9539](https://github.com/microsoft/pyright/issues/9539): Ensure that the types of arguments passed to functions match those expected by the function definition or documentation.
-   [#9568](https://github.com/microsoft/pyright/issues/9568): When using `type[TypeVar]` in function signatures, ensure that type checks are performed correctly with `issubclass` to avoid runtime errors and incorrect type refinements.
-   [#9606](https://github.com/microsoft/pyright/issues/9606): Ensure to use a stable and recommended version of pyright for best type checking results.
-   [#9685](https://github.com/microsoft/pyright/issues/9685): Ensure to test new versions of libraries and tools thoroughly before upgrading in production environments.
-   [#9809](https://github.com/microsoft/pyright/issues/9809): Use specific type annotations instead of unions when calling functions to avoid syntax errors.

## Common Fixes & Workarounds

1. Double-check function and method signatures for correct argument types and counts.
2. Use explicit type annotations for variables and function parameters.
3. Avoid using dynamic constructs (like `try/except` for imports) in stub files; prefer direct imports.
4. Use the actual class names from libraries rather than aliases or shorthand notations.
5. When using `Annotated`, ensure metadata types are valid and used as intended.
6. For overloaded functions, provide clear and compatible overload signatures.
7. Use assertions or type checks to ensure arguments match expected types, especially for functions like `memoryview.cast`.
8. Keep Pyright and Pylance up to date and ensure installations are not corrupted.
9. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallIssue) for details on configuring or disabling this diagnostic.

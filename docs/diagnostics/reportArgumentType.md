## Overview

`reportArgumentType` is a Pylance and Pyright diagnostic that warns when an argument passed to a function, method, or constructor does not match the expected type. This helps catch type mismatches early and improves code safety and maintainability.

## Representative Issues

-   [#7084](https://github.com/microsoft/pyright/issues/7084): Avoid using multiple TypeVars in function signatures without a clear reason to distinguish different overloads, as this can lead to confusion and misleading error messages.
-   [#7186](https://github.com/microsoft/pyright/issues/7186): Ensure that the types are explicitly defined and correctly annotated to avoid false positives in static type checking tools like `pyright`.
-   [#7228](https://github.com/microsoft/pyright/issues/7228): When using type annotations in Python, ensure that the syntax adheres to the latest typing specifications to avoid runtime errors.
-   [#7255](https://github.com/microsoft/pyright/issues/7255): Ensure that the configuration options for diagnostics in static analysis tools like Pyright distinguish between default arguments and explicitly assigned function call arguments to avoid misinterpretation of type mismatches.
-   [#7362](https://github.com/microsoft/pyright/issues/7362): When overriding methods inherited from a parent class like `MutableMapping`, ensure that the method signatures are compatible, especially concerning optional arguments.
-   [#7382](https://github.com/microsoft/pyright/issues/7382): Ensure that the data structure used for initializing dictionaries aligns with the expected types according to the type checker.
-   [#7484](https://github.com/microsoft/pyright/issues/7484): When introducing new rules or changing default severities, ensure that existing configurations are backward compatible to avoid disruptions.
-   [#7523](https://github.com/microsoft/pyright/issues/7523): Use type guards and annotations to narrow down variable types before accessing them to avoid errors like 'reportOptionalSubscript' in static type checkers.
-   [#7543](https://github.com/microsoft/pyright/issues/7543): Pyright should include special support for dynamic dispatch mechanisms like singledispatchmethod to recognize compatibility with protocols.
-   [#7548](https://github.com/microsoft/pyright/issues/7548): Always ensure that TypeVars are properly scoped and resolved within their respective contexts to avoid type resolution failures.

## Common Fixes & Workarounds

1. Ensure that all arguments passed to functions, methods, and constructors match the expected type annotations.
2. Use type guards and assertions to narrow variable types before use.
3. Add or update type annotations to clarify expected argument types.
4. Refactor code to avoid ambiguous or mismatched argument types.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportArgumentType) for details on configuring or disabling this diagnostic.

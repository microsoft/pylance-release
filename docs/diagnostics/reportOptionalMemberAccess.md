## Overview

`reportOptionalMemberAccess` flags cases where you attempt to access an attribute or method on a value that could be `None`. This diagnostic helps prevent runtime errors by ensuring you only access members of objects that are guaranteed to be non-None.

## Representative Issues

-   [#1506](https://github.com/microsoft/pylance-release/issues/1506): Adjust diagnostic severity overrides in IDE settings to control type-checking behavior after updates.
-   [#2385](https://github.com/microsoft/pylance-release/issues/2385): Update type stubs in typeshed to indicate non-Optional attributes when parameters like PIPE guarantee their presence.
-   [#2424](https://github.com/microsoft/pylance-release/issues/2424): Avoid using `NoReturn` with complex overloads and unions, as the current implementation does not fully support this scenario.
-   [#2751](https://github.com/microsoft/pylance-release/issues/2751): Ensure that variables holding optional types are properly initialized and checked before accessing their attributes.
-   [#3358](https://github.com/microsoft/pylance-release/issues/3358): Users can revert to previous default type checking settings by adjusting configurations in their IDE.
-   [#3809](https://github.com/microsoft/pylance-release/issues/3809): Adjust the diagnostic settings in your code editor to disable specific rules causing false positives or errors.
-   [#3942](https://github.com/microsoft/pylance-release/issues/3942): Always check the type of an object before attempting to access its members, especially with multiple possible types.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#4360](https://github.com/microsoft/pylance-release/issues/4360): Always ensure that optional members are properly handled by checking for `None` before accessing them.
-   [#4690](https://github.com/microsoft/pylance-release/issues/4690): Ensure that type annotations are explicit and align with the actual behavior of functions, especially with potential `None` values.
-   [#4950](https://github.com/microsoft/pylance-release/issues/4950): Use `typing.overload` to clarify the return types of functions with different outputs based on input parameters.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#5671](https://github.com/microsoft/pylance-release/issues/5671): Prefer using an `if` statement for conditional checks instead of relying on exception handling to control flow.

## Common Fixes & Workarounds

1. Use type guards (e.g., `if obj is not None:`) before accessing attributes or methods on possibly-None values.
2. Add or refine type annotations to clarify when a value can be `None`.
3. Use assertions (e.g., `assert obj is not None`) before member access if you know the value is not `None` at that point.
4. Refactor code to avoid accessing members of values that may be `None`.
5. Use `typing.overload` to clarify function return types when needed.
6. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportOptionalMemberAccess) for details on configuring or disabling this diagnostic.

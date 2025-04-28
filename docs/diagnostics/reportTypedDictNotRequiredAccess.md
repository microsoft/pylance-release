## Overview

`reportTypedDictNotRequiredAccess` flags cases where you access a non-required (optional) field of a `TypedDict` without first checking if it is present. This diagnostic helps prevent runtime errors and ensures safe access to optional fields in typed dictionaries.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
-   [#1693](https://github.com/microsoft/pyright/issues/1693): Use type inheritance in TypedDict to clearly define required and not required fields.
-   [#4173](https://github.com/microsoft/pyright/issues/4173): Implement per-module configuration settings in Pyright for more flexible type checking.

## Common Fixes & Workarounds

1. Check for the presence of a non-required field in a `TypedDict` before accessing it (e.g., using `if "field" in my_dict:`).
2. Use type inheritance to clearly define required and not required fields in your `TypedDict` definitions.
3. Use per-module configuration settings to adjust diagnostics as needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportTypedDictNotRequiredAccess) for details on configuring or disabling this diagnostic.

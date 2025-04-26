## Overview

`reportGeneralTypeIssues` is a diagnostic that flags a wide range of type-related issues in Python code, such as incorrect type hints, improper use of generics, and mismatches between type annotations and actual usage. This helps developers catch subtle bugs and improve code quality.

## Representative Issues

-   [#1023](https://github.com/microsoft/pylance-release/issues/1023): Avoid using literal types within tuples for collection elements to prevent incorrect type inference and concatenation issues.
-   [#1034](https://github.com/microsoft/pylance-release/issues/1034): Ensure type hints match actual constructor arguments.
-   [#1068](https://github.com/microsoft/pylance-release/issues/1068): Use 'TypeGuard' to indicate type checks within functions.
-   [#106](https://github.com/microsoft/pylance-release/issues/106): Ensure all necessary imports are included and referenced.
-   [#1094](https://github.com/microsoft/pylance-release/issues/1094): Use covariant TypeVar for assignment between related types.
-   [#1095](https://github.com/microsoft/pylance-release/issues/1095): Avoid unnecessary type arguments in annotations.
-   [#1274](https://github.com/microsoft/pylance-release/issues/1274): Correctly type function parameters.
-   [#1290](https://github.com/microsoft/pylance-release/issues/1290): Use independent TypeVar declarations for nested generic classes.
-   [#1295](https://github.com/microsoft/pylance-release/issues/1295): Ensure correct order of parent class inheritance in protocols.

## Common Fixes & Workarounds

1. Review and correct type hints and annotations throughout your code.
2. Use explicit type aliases and TypeVar declarations where needed.
3. Match type annotations to actual usage and constructor arguments.
4. Refactor code to avoid ambiguous or incorrect type usage.
5. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportGeneralTypeIssues) for details on configuring this rule.

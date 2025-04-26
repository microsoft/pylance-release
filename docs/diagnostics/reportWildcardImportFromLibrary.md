## Overview

`reportWildcardImportFromLibrary` is a Pylance and Pyright diagnostic that warns when you use a wildcard import (e.g., `from module import *`) from a library. Wildcard imports can make code harder to read and maintain, and may introduce unexpected names into your namespace.

## Representative Issues

-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
-   [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.

## Common Fixes & Workarounds

1. Replace wildcard imports with explicit imports of only the names you need.
2. Refactor code to avoid relying on `import *` from libraries.
3. Use type annotations and explicit imports for better code clarity and maintainability.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportWildcardImportFromLibrary) for details on configuring or disabling this diagnostic.

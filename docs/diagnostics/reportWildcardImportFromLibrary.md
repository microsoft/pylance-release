## Overview

`reportWildcardImportFromLibrary` is a Pylance and Pyright diagnostic that warns when you use a wildcard import (e.g., `from module import *`) from a library. Wildcard imports can make code harder to read and maintain, and may introduce unexpected names into your namespace.


## Common Fixes & Workarounds

1. Replace wildcard imports with explicit imports of only the names you need.
2. Refactor code to avoid relying on `import *` from libraries.
3. Use type annotations and explicit imports for better code clarity and maintainability.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportWildcardImportFromLibrary) for details on configuring or disabling this diagnostic.

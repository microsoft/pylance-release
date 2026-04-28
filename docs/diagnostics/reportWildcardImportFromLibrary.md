## Overview

`reportWildcardImportFromLibrary` is a Pylance and Pyright diagnostic that warns when you use a wildcard import (e.g., `from module import *`) from a library. Wildcard imports can make code harder to read and maintain, and may introduce unexpected names into your namespace.

## Examples

**Error:**

```python
from os.path import *  # Wildcard import from library

result = join("/home", "user")  # Works but pollutes namespace
```

**Fix — use explicit imports:**

```python
from os.path import join, exists

result = join("/home", "user")
```

Or import the module and use qualified names:

```python
import os.path

result = os.path.join("/home", "user")
```

## Common Fixes & Workarounds

1. Replace wildcard imports with explicit imports of only the names you need.
2. Refactor code to avoid relying on `import *` from libraries.
3. Use type annotations and explicit imports for better code clarity and maintainability.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportWildcardImportFromLibrary) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

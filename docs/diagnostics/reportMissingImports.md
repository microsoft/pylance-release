## Overview

`reportMissingImports` is a diagnostic in Pylance and Pyright that warns when an import statement cannot be resolved because the module is missing or not installed. This helps catch missing dependencies and configuration issues, improving code reliability and maintainability.

## Representative Issues

- [#2202](https://github.com/microsoft/pylance-release/issues/2202): Ensure all necessary modules are installed in the Python environment specified for the project.
- [#2996](https://github.com/microsoft/pylance-release/issues/2996): Use comments to suppress specific warnings in static analysis tools when dealing with optional imports.
- [#4976](https://github.com/microsoft/pylance-release/issues/4976): Ensure that static analysis tools are configured correctly to recognize all necessary modules, or use runtime checks if dynamic imports are involved.

## Examples

```python
import my_custom_module  # Error: Import "my_custom_module" could not be resolved
from utils import helper # Error: Import "utils" could not be resolved
```

**Fix — install the package or configure extra paths:**

```bash
# If it's a third-party library, install it:
pip install my_custom_module
```

```json
// If it's your own code in a non-standard location, add to .vscode/settings.json:
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

**Fix — suppress for optional/platform-specific imports:**

```python
try:
    import optional_module  # pyright: ignore[reportMissingImports]
except ImportError:
    optional_module = None
```

## Common Fixes & Workarounds

1. Install missing modules using pip or your package manager.
2. Check that the correct [Python environment](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter) is selected in your IDE or editor.
3. Use comments like `# pyright: ignore[reportMissingImports]` to suppress warnings for optional or platform-specific imports.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingImports) for options to adjust or suppress this diagnostic if needed.

## See Also

- [Fixing unresolved imports](../howto/unresolved-imports.md) — comprehensive guide for resolving import issues
- [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) — add extra search paths for imports
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

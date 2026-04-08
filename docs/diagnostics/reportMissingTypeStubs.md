## Overview

`reportMissingTypeStubs` is a diagnostic in Pylance and Pyright that warns when a module is missing type stubs (`.pyi` files) or type annotations. This helps catch missing type information for third-party libraries, improving static analysis and type safety.

## Representative Issues

- [#9393](https://github.com/microsoft/pyright/issues/9393): Ensure that all modules within the 'google.cloud' namespace include a 'py.typed' marker and appropriate type annotations to avoid errors like 'reportMissingTypeStubs'.

## Examples

```python
import some_library  # Warning: Stub file not found for "some_library"
```

**Fix — install type stubs if available:**

```bash
pip install types-some_library
# or for common packages:
pip install types-requests types-PyYAML
```

**Fix — use `useLibraryCodeForTypes` to infer types from source:**

```json
// .vscode/settings.json
{
    "python.analysis.useLibraryCodeForTypes": true
}
```

## Common Fixes & Workarounds

1. Install or generate type stubs (`.pyi` files) for third-party libraries.
2. Use libraries that provide type annotations or a `py.typed` marker file.
3. Contribute type stubs to the typeshed repository or the library itself if missing.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingTypeStubs) for options to adjust or suppress this diagnostic if needed.

## See Also

- [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) — use library source when type stubs are missing
- [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md) — specify a custom path for type stubs
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

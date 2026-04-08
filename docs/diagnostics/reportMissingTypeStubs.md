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

### Stub-package version mismatches

Stub-only packages (like `boto3-stubs`, `types-requests`) must match the version of the library they describe. If you install `types-requests==2.28.0` but have `requests==2.31.0`, the stubs may define different APIs, causing false errors.

Fix: keep stub-package versions aligned with library versions:

```bash
pip install requests==2.31.0 types-requests==2.31.0
```

For AWS SDK stubs (`boto3-stubs`, `mypy-boto3-*`), install matching versions and the service-specific sub-packages:

```bash
pip install 'boto3-stubs[s3,ec2]'  # installs service stubs for s3 and ec2
```

**Diagnosis**: run `pip list | grep types-` (or `pip list | grep stubs`) and compare versions against the library they describe.

If a stub package produces errors itself (e.g., internal stub inconsistencies), check for newer versions or file an issue on the stub package's repository.

## See Also

- [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) — use library source when type stubs are missing
- [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md) — specify a custom path for type stubs
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

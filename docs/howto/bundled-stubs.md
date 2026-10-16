# How to Override Bundled Third-Party Stubs in Pylance

Pylance ships bundled type stubs for some popular third-party packages. These stubs improve IntelliSense and type checking when a package does not include its own type information.

Bundled stubs are a fallback. If the bundled stub for a package is incomplete or does not match the version of the package you use, you can override it in two ways: install the package's own type stubs (for example a PEP 561 `-stubs` package) into your environment, or add workspace-local stubs through [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md).

---

## When bundled stubs are used

Pylance checks these locations for imports. A later stub can take priority over an earlier source-file match:

1. [`stubPath`](../settings/python_analysis_stubPath.md), which defaults to `typings`
2. workspace source and [`extraPaths`](../settings/python_analysis_extraPaths.md)
3. standard-library typeshed stubs
4. installed packages from the selected interpreter, such as `site-packages`
5. bundled third-party stubs
6. typeshed third-party fallback stubs

This means custom stubs in `stubPath` have higher priority than bundled stubs. Installed stub packages also take priority over bundled stubs, including PEP 561 `-stubs` packages (with or without a `py.typed` marker) and partial stub packages. A bare inline `.pyi` file in a runtime package without a `py.typed` marker or installed `-stubs` package does not take priority over a bundled stub.

For the complete import-resolution order, see [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md#how-pylance-resolves-imports). To inspect the order in your workspace, enable trace logging and see [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md).

---

## Use `typings` for a workspace-local override

The default [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md) value is `typings`. If you create a `typings` folder at the workspace root, Pylance checks it before bundled stubs.

Use this when you need to patch one package for one workspace without replacing the full typeshed tree.

```text
my_project/
├── .vscode/
│   └── settings.json
├── typings/
│   └── examplelib-stubs/
│       ├── __init__.pyi
│       ├── py.typed
│       └── api.pyi
└── src/
    └── app.py
```

If you use the default `typings` folder name, no setting is required. If you prefer another folder name, configure it explicitly:

```json
{
    "python.analysis.stubPath": "custom_typings"
}
```

---

## Prefer partial stub packages for small patches

For a small package-specific correction, a PEP 561 partial stub package is usually the safest shape. The folder name should end with `-stubs`, and its `py.typed` file should contain `partial`.

Example:

```text
typings/
└── examplelib-stubs/
    ├── __init__.pyi
    ├── py.typed
    └── missing_module.pyi
```

`typings/examplelib-stubs/py.typed`:

```text
partial
```

This tells Pylance to use your stubs for the modules you provided while still allowing the installed package to supply the rest of the package surface.

Use a partial stub package when you want to fill gaps. Use a full package stub, such as `typings/examplelib/...`, only when you intend your local stubs to describe the package surface completely.

---

## Example: patch a missing Django symbol

Suppose your code imports a symbol that exists in your installed Django version, but Pylance reports it as missing because the bundled Django stub does not match your runtime package.

Create a partial local stub package:

```text
typings/
└── django-stubs/
    ├── __init__.pyi
    ├── py.typed
    └── utils/
        ├── __init__.pyi
        └── deprecation.pyi
```

`typings/django-stubs/py.typed`:

```text
partial
```

`typings/django-stubs/utils/deprecation.pyi`:

```python
class RemovedInDjango50Warning(DeprecationWarning): ...
class RemovedInDjango51Warning(PendingDeprecationWarning): ...
```

For the most accurate result, copy or adapt the declarations from a `django-stubs` package version that supports your Django version.

---

## Disable a mismatched bundled stub

To use installed package information without maintaining a replacement stub, set `python.analysis.disableBundledStubs` in `settings.json`:

```json
{
    "python.analysis.disableBundledStubs": ["django"]
}
```

Use the import name (`django`), not the stub-directory name (`django-stubs`). Set the value to `true` to disable all bundled stubs, or `false` (the default) to restore them.

If you use external Pyright diagnostics, only `true` disables the bundled stubs there; per-package lists apply to Pylance only.

---

## Check which stub Pylance used

Enable trace logging:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

Then open **Output -> Python Language Server** and search for the module name. Helpful lines include:

| Log Message | Meaning |
| ----------- | ------- |
| `Looking in stubPath '...'` | Pylance checked your workspace-local custom stubs. |
| `Looking in python search path '...'` | Pylance checked installed packages from the selected interpreter. |
| `Looking in bundled stubs path '...'` | Pylance checked bundled third-party stubs. |
| `Resolved import with file '...'` | Pylance found the import at that path. |

If the resolved path is under your workspace `typings` folder, your override is active.

---

## Should I use `stubPath` or `typeshedPaths`?

Use [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md) for package-specific fixes, including bundled third-party stub overrides.

Use [`python.analysis.typeshedPaths`](../settings/python_analysis_typeshedPaths.md) only when you need to replace the typeshed source tree that Pylance consults for standard-library or typeshed fallback stubs.

---

## Related Guides

- [Understanding `python.analysis.stubPath`](../settings/python_analysis_stubPath.md) - setting reference and directory layouts
- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) - full import-resolution order and troubleshooting checklist
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) - trace logging and log interpretation

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

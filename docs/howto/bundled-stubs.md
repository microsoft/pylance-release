# How to Override Bundled Third-Party Stubs in Pylance

Pylance ships bundled type stubs for some popular third-party packages. These stubs improve IntelliSense and type checking when a package does not include its own type information.

Bundled stubs are a fallback. If the bundled stub for a package is incomplete or does not match the version of the package you use, you can override it with workspace-local stubs through [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md).

---

## When bundled stubs are used

Pylance looks for imports in several places and stops at the first usable match. For third-party packages, the important order is:

1. [`stubPath`](../settings/python_analysis_stubPath.md), which defaults to `typings`
2. workspace source and [`extraPaths`](../settings/python_analysis_extraPaths.md)
3. standard-library typeshed stubs
4. installed packages from the selected interpreter, such as `site-packages`
5. bundled third-party stubs
6. typeshed third-party fallback stubs

This means custom stubs in `stubPath` have higher priority than bundled stubs. Installed packages that provide type information through a `py.typed` marker also take priority over bundled stubs.

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

## Check which stub Pylance used

Enable trace logging:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

Then open **Output -> Pylance** and search for the module name. Helpful lines include:

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
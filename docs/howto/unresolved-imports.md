# How to Fix Unresolved Import Errors in Pylance

Pylance uses static analysis to resolve Python imports. When it cannot find a module, it reports one of several diagnostics depending on what is missing. This guide covers the most common import errors, their causes, and how to fix them.

---

## Table of Contents

- [Import Could Not Be Resolved (`reportMissingImports`)](#import-could-not-be-resolved-reportmissingimports)
- [Import Could Not Be Resolved from Source (`reportMissingModuleSource`)](#import-could-not-be-resolved-from-source-reportmissingmodulesource)
- [Stub File Not Found (`reportMissingTypeStubs`)](#stub-file-not-found-reportmissingtypestubs)
- [Circular Import Detected (`reportImportCycles`)](#circular-import-detected-reportimportcycles)
- [Works at Runtime but Pylance Shows Errors](#works-at-runtime-but-pylance-shows-errors)
- [Bundled Third-Party Stubs](#bundled-third-party-stubs)
- [How Pylance Resolves Imports](#how-pylance-resolves-imports)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## Import Could Not Be Resolved (`reportMissingImports`)

**Symptom**: `Import "mypackage" could not be resolved` [`Pylance(reportMissingImports)`](../diagnostics/reportMissingImports.md)

### Diagnostic Steps

1. **Check the Python interpreter**: Click the Python version in the VS Code status bar. Verify it points to the correct virtual environment.

    ```bash
    # Check this terminal's interpreter against the environment selected for the file:
    which python    # Linux/macOS
    where python    # Windows
    python -c "import sys; print(sys.path)"
    ```

2. **Check if the package is installed**:

    ```bash
    pip show mypackage
    # or
    python -c "import mypackage; print(mypackage.__file__)"
    ```

3. **Check [`extraPaths`](../settings/python_analysis_extraPaths.md)**: Open Settings (JSON) and verify `python.analysis.extraPaths` includes the correct import root, not just an existing but wrong directory level.

4. **Check for editable install issues**: If using `pip install -e`:

    ```bash
    # Look for .pth files:
    find .venv/lib -name "*.pth" | xargs cat
    # Python 3.13+ can discover import hooks when enableEditableInstalls is enabled
    ```

5. **Enable verbose logging**: Add to settings.json:

    ```json
    {
        "python.analysis.logLevel": "Trace"
    }
    ```

    Then check the **Output** panel → **Python Language Server** for import resolution attempts. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) for a detailed walkthrough.

6. **Check [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: If it exists, it may override VS Code settings. Verify [`include`](../settings/python_analysis_include.md), [`exclude`](../settings/python_analysis_exclude.md), and [`extraPaths`](../settings/python_analysis_extraPaths.md). See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md#validate-path-based-settings) for config precedence and path-validation checks.

### Common Causes and Fixes

| Cause                                                                                          | Fix                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wrong interpreter selected                                                                     | Select the correct venv in VS Code status bar                                                                                                                  |
| Package not installed in the venv                                                              | `pip install mypackage` in the correct venv                                                                                                                    |
| [`extraPaths`](../settings/python_analysis_extraPaths.md) missing a directory                  | Add the package source dir to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                        |
| Configured path exists but points to the wrong directory level                                 | Change the path so it points at the intended import root. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md#validate-path-based-settings) |
| Editable install uses import hooks                                                             | Check Python 3.13+ editable-install discovery or use a path-based install. See [How to Use Editable Installs with Pylance](editable-installs.md)               |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides settings | Check and update the config file. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md)                                                      |
| [`include`](../settings/python_analysis_include.md) setting excludes the file                  | Use `include` for finding files for analysis. For unresolved imports, check the import search paths.                                                           |
| File is in [`exclude`](../settings/python_analysis_exclude.md) patterns                        | Change `exclude` to include it in workspace analysis. For unresolved imports, check the import search paths.                                                   |
| Namespace package (no `__init__.py`)                                                           | Pylance supports namespace packages, but verify structure                                                                                                      |
| Missing `__init__.py` in a regular package                                                     | Add `__init__.py` to each package directory (even if empty) unless using namespace packages                                                                    |

---

## Import Could Not Be Resolved from Source (`reportMissingModuleSource`)

**Symptom**: `Import "mypackage" could not be resolved from source` `Pylance(reportMissingModuleSource)`

**What it means**: Pylance found a type stub (`.pyi`) for the package but could not resolve its corresponding runtime implementation. This is different from `reportMissingImports` — the import _does_ resolve (via stubs), but its runtime implementation was not found.

### Common Causes and Fixes

| Cause                                                                                | Fix                                                                                                              |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| Native runtime module is not resolved in the selected environment                    | Check the selected interpreter and runtime installation; a resolved `.so` / `.pyd` does not require `.py` source |
| Stub found, but compiled runtime file is not found                                   | Pylance recognizes a `.pyc` file alongside its stub. Check the selected environment and package location.        |
| Stubs installed separately (e.g., `types-requests`) but main package not in the venv | Install the main package: `pip install requests`                                                                 |
| Stub-only package with no corresponding runtime package                              | Suppress for that specific package: `# type: ignore[reportMissingModuleSource]`                                  |

---

## Stub File Not Found (`reportMissingTypeStubs`)

**Symptom**: `Stub file not found for "mypackage"` `Pylance(reportMissingTypeStubs)`

**What it means**: The package is installed and importable, but it has no type stubs (no `.pyi` files) and is not marked as `py.typed`. This diagnostic is **off by default** and is an error in `strict` type-checking mode.

### Common Causes and Fixes

| Cause                                            | Fix                                                                                                                                                                                                                         |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Third-party package without type support         | Install stubs if available: `pip install types-mypackage`                                                                                                                                                                   |
| No stubs available for the package               | Suppress: `"reportMissingTypeStubs": "none"` in [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md), or create a stub file in [`stubPath`](../settings/python_analysis_stubPath.md) |
| Package _is_ typed but missing `py.typed` marker | Report to the package maintainer, or create a local stub                                                                                                                                                                    |

---

## Circular Import Detected (`reportImportCycles`)

**Symptom**: `Cycle detected in import chain` `Pylance(reportImportCycles)` — followed by a list of file paths forming the cycle.

**What it means**: Files form a circular dependency (A imports B, B imports C, C imports A). This diagnostic is **off by default** — you only see it when `reportImportCycles` is explicitly enabled.

### Mitigation Strategies

- **Move shared types to a separate module** that both sides can import without creating a cycle
- **Use `TYPE_CHECKING` imports** for type-only references to avoid runtime cycles. These imports still count when Pylance checks for import cycles:

    ```python
    from __future__ import annotations
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from mypackage.models import User  # only used for type hints, not at runtime
    ```

- **Restructure the dependency** so the cycle is broken at the module level
- **Suppress per-file**: `# pyright: reportImportCycles=false` at the top of files where circular imports are intentional

---

## Works at Runtime but Pylance Shows Errors

**Symptom**: `import mypackage` works in the terminal (`python -c "import mypackage"` succeeds), but Pylance shows `reportMissingImports`.

This can happen when runtime and analysis use different environments or search paths.

### Things Pylance Cannot Follow

Some of the mechanisms below can be handled when configured as described in the table.

| Runtime Mechanism                                           | Why Pylance Can't Follow It                                                                                                                  | Fix                                                                                                                                                                            |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Import-hook `.pth` files** (lines starting with `import`) | Pylance can discover editable sources on Python 3.13+                                                                                        | Check the selected environment and use a path-based install or explicit source paths if discovery fails. See [How to Use Editable Installs with Pylance](editable-installs.md) |
| **`sys.path.append()` / `sys.path.insert()`** in code       | Pylance does not execute Python code — dynamic path modifications are invisible                                                              | Add the path to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                                                                              |
| **`PYTHONPATH` environment variable**                       | Pylance can receive `PYTHONPATH` from the Python extension                                                                                   | Check `python.envFile` or add explicit [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                               |
| **`pkgutil.extend_path()` in `__init__.py`**                | Pylance does not execute this runtime path mutation; configure the contributing source roots explicitly                                      | Add all contributing directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                  |
| **`importlib` dynamic imports**                             | All programmatic imports are invisible to static analysis                                                                                    | Use regular `import` statements or `TYPE_CHECKING` import blocks for type checking                                                                                             |
| **Namespace packages across separate roots**                | Pylance can resolve namespace portions across configured roots; a missing root cannot contribute its modules                                 | Put all contributing directories in [`extraPaths`](../settings/python_analysis_extraPaths.md) so Pylance sees all sources                                                      |
| **pytest `conftest.py` path injection**                     | Runtime path changes made by test configuration are not automatically added as ordinary import roots for analysis                            | Add test root directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                         |
| **Django `INSTALLED_APPS` / app autodiscovery**             | Django dynamically discovers and imports apps via settings; Pylance can't execute `django.setup()`                                           | Add each app's parent directory to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                   |
| **Conda environment path layout**                           | Conda environments store packages in `lib/pythonX.Y/site-packages` under the conda prefix, which may differ from a venv layout               | Select the conda interpreter in VS Code status bar; verify with `python -c "import sys; print(sys.prefix)"`                                                                    |
| **`sys.modules` patching**                                  | Some libraries inject modules into `sys.modules` at runtime (e.g., aliasing `pkg` → `pkg_v2`); Pylance cannot follow runtime module aliasing | Use `TYPE_CHECKING` imports for the real module name, or add a type stub                                                                                                       |
| **`site.addsitedir()`**                                     | Adds directories to `sys.path` at runtime and processes `.pth` files; Pylance does not call `site.addsitedir()`                              | Add the directories to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                                                                       |

### Framework-Specific Examples

**pytest**: If tests import helper modules from a `tests/` directory via conftest:

```text
project/
├── src/mypackage/
├── tests/
│   ├── conftest.py      # pytest adds this dir to sys.path
│   └── helpers/
│       └── test_utils.py
```

If the test runner makes `from helpers.test_utils import ...` work at runtime but `tests/` is not a Pylance import root, configure that root:

```json
{
    "python.analysis.extraPaths": ["./tests"]
}
```

**Django**: If your project uses app discovery via `INSTALLED_APPS`:

```text
myproject/
├── myproject/
│   └── settings.py  # INSTALLED_APPS = ["users", "billing"]
├── users/
│   └── models.py
└── billing/
    └── models.py
```

With `myproject/` as the execution root, Pylance can resolve `from users.models import User` from source without running Django. If that root is not otherwise searchable, configure it explicitly:

```json
{
    "python.analysis.extraPaths": ["."]
}
```

Or add the project root to [`extraPaths`](../settings/python_analysis_extraPaths.md) in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration).

**Flask**: If your Flask project uses blueprints or app factories spanning multiple packages:

```text
myproject/
├── app/
│   ├── __init__.py       # create_app() factory
│   └── extensions.py     # db = SQLAlchemy()
├── blueprints/
│   ├── auth/
│   │   └── routes.py     # from app.extensions import db
│   └── api/
│       └── routes.py     # from app.extensions import db
└── tests/
    └── conftest.py
```

With `myproject/` as the execution root, Pylance can resolve `from app.extensions import db` without running the app factory. The following setting is only needed if that root is not otherwise searchable:

```json
{
    "python.analysis.extraPaths": ["."]
}
```

### Diagnosis Workflow

1. **Confirm the runtime path**: `python -c "import mypackage; print(mypackage.__file__)"`
2. **Check Pylance's search paths**: Enable `"python.analysis.logLevel": "Trace"` and look in **Output → Python Language Server** for the import resolution log (see [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md))
3. **Compare**: Is the directory containing `mypackage` in Pylance's search paths? If not, add it to [`extraPaths`](../settings/python_analysis_extraPaths.md)

---

## Bundled Third-Party Stubs

Pylance includes bundled stubs for some popular third-party packages. These bundled stubs are used only after Pylance checks custom stubs, workspace paths, typeshed standard-library stubs, and installed packages from the selected interpreter.

If a bundled third-party stub does not match the package version you use, add a workspace-local override through [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md). The default stub directory is `typings`, and Pylance checks it before bundled stubs.

For a package-specific patch, prefer a PEP 561 partial stub package under `typings`, such as `typings/package-stubs/py.typed` containing `partial`. See [How to Override Bundled Third-Party Stubs in Pylance](bundled-stubs.md) for examples.

---

## How Pylance Resolves Imports

Pylance checks the following locations. Stubs and namespace packages can affect which match wins:

| Priority | Search Location                                                                                                                     | Notes                                                  |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 1        | [`stubPath`](../settings/python_analysis_stubPath.md) (custom stubs)                                                                | Default: `./typings`                                   |
| 2        | Source files in the project root (or execution environment root)                                                                    | Your workspace files                                   |
| 3        | `src/` directory (if [`autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) is `true` and `src/` has no `__init__.py`) | Automatic convenience path                             |
| 4        | [`extraPaths`](../settings/python_analysis_extraPaths.md) entries                                                                   | Searched in order listed                               |
| 5        | Typeshed stdlib stubs                                                                                                               | Standard library type info                             |
| 6        | Python interpreter search paths (`site-packages`)                                                                                   | Installed packages from the selected interpreter       |
| 7        | Bundled third-party stubs (Pylance ships with stubs for some popular packages)                                                      | Used when no earlier typed package or custom stub wins |
| 8        | Typeshed third-party stubs                                                                                                          | Community-maintained fallback stubs                    |

**Key implications**:

- [`extraPaths`](../settings/python_analysis_extraPaths.md) entries are searched before interpreter paths, but a typed package or stub can take priority over an earlier untyped match.
- [`stubPath`](../settings/python_analysis_stubPath.md) has **higher priority** than bundled third-party stubs. Use it for workspace-local package-stub overrides.
- Installed packages that include type information, such as a `py.typed` marker or installed stub package, take priority over bundled third-party stubs.
- If a [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` with `[tool.pyright]` defines `extraPaths`, that list replaces VS Code's [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md). Otherwise, VS Code paths still apply. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).

---

## Diagnostic Checklist

When imports aren't resolving, run through this checklist:

- [ ] **Interpreter**: Is the correct Python interpreter selected? (status bar)
- [ ] **Interpreter path**: Does `python -c "import sys; print(sys.prefix)"` in the VS Code terminal point to the right venv?
- [ ] **Package installed**: Is the package installed in that venv? (`pip show <package>`)
- [ ] **Editable install**: Is its source found through a path-based `.pth` file or Python 3.13+ import-hook discovery? See [How to Use Editable Installs with Pylance](editable-installs.md)
- [ ] **[`extraPaths`](../settings/python_analysis_extraPaths.md)**: Do paths exist and point to the import root rather than a nested package directory?
- [ ] **Path-based settings**: If you use [`stubPath`](../settings/python_analysis_stubPath.md) or [`typeshedPaths`](../settings/python_analysis_typeshedPaths.md), do those resolved paths point to the intended root? See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md#validate-path-based-settings)
- [ ] **[`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: Does a config file exist that might override settings?
- [ ] **[`include`](../settings/python_analysis_include.md)/[`exclude`](../settings/python_analysis_exclude.md)**: Are the intended workspace files found for analysis?
- [ ] **Pylance output**: Check Output panel → Python Language Server for any errors or warnings
- [ ] **Verbose logging**: Enable `"python.analysis.logLevel": "Trace"` and check for import resolution details. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md)
- [ ] **Restart**: Run "Python: Restart Language Server" after any configuration change

---

## FAQ

### Q: My .env file with PYTHONPATH is being ignored. Why?

The Python extension can forward `PYTHONPATH` from its configured `.env` file to Pylance. Check `python.envFile` and the environment for the file being analyzed. Explicit [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) is an alternative:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

Configure runtime `PYTHONPATH` in the Python extension's `.env` file; Pylance can use those paths too.

### Q: Can I use `PYTHONPATH` environment variable instead of `extraPaths`?

Pylance uses `PYTHONPATH` forwarded by the Python extension along with the selected interpreter's search paths. You can also configure explicit [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md), for example:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"],
    "python.envFile": "${workspaceFolder}/.env"
}
```

The `python.envFile` setting selects the Python extension's environment file; its forwarded `PYTHONPATH` values can affect Pylance's import resolution.

### Q: How do I handle namespace packages (no `__init__.py`)?

Pylance supports [PEP 420](https://peps.python.org/pep-0420/) namespace packages. If your project uses them:

1. Ensure the parent directory is in [`extraPaths`](../settings/python_analysis_extraPaths.md) or is the workspace root
2. Do **not** add `__init__.py` to the namespace root
3. Each sub-package that contributes to the namespace should have its own `__init__.py`

```text
project/
├── packages/
│   ├── core/
│   │   └── mycompany/
│   │       └── core/
│   │           └── __init__.py
│   └── utils/
│       └── mycompany/
│           └── utils/
│               └── __init__.py
```

```json
{
    "python.analysis.extraPaths": ["./packages/core", "./packages/utils"]
}
```

Both `from mycompany.core import X` and `from mycompany.utils import Y` will resolve.

### Q: What's the difference between `include`, `exclude`, and `ignore`?

| Setting                                                    | Effect on File Discovery | Effect on Diagnostics              | Effect on Import Resolution          |
| ---------------------------------------------------------- | ------------------------ | ---------------------------------- | ------------------------------------ |
| Not in [`include`](../settings/python_analysis_include.md) | Not discovered           | Can report diagnostics when opened | Still available to import resolution |
| In [`exclude`](../settings/python_analysis_exclude.md)     | Not discovered           | Can report diagnostics when opened | Still available to import resolution |
| In [`ignore`](../settings/python_analysis_ignore.md)       | Discovered & analyzed    | Diagnostics suppressed             | Resolved normally                    |

### Q: How do I debug import resolution?

Enable trace logging and check the **Output → Python Language Server** panel:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

The log shows each search location Pylance tries, including `stubPath`, the project root, `extraPaths`, typeshed, `site-packages`, bundled third-party stubs, and third-party fallback stubs. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) for a detailed walkthrough.

### Q: Auto-import suggests the wrong package path. How do I fix it?

**Symptom**: Auto-import suggests `from packages.shared.src.shared.utils import X` instead of `from shared.utils import X`.

**Cause**: Pylance sees the file through the filesystem, not through the configured import path.

**Fix**: Configure [`extraPaths`](../settings/python_analysis_extraPaths.md) to point to the correct source root:

```json
{
    "python.analysis.extraPaths": ["./packages/shared/src"]
}
```

Not:

```json
{
    "python.analysis.extraPaths": ["./packages/shared"]
}
```

The [`extraPaths`](../settings/python_analysis_extraPaths.md) entry should point to the directory that _contains the top-level package directory_.

### Q: Go to Definition goes to the wrong location. How do I fix it?

**Symptom**: Go to Definition opens a file from `site-packages` instead of the source directory, or vice versa.

**Cause**: Pylance found a different copy of the package.

**Fix**:

- If you want source: Add its import root to [`extraPaths`](../settings/python_analysis_extraPaths.md) and confirm the target with Go to Definition
- If you want installed: Check for competing workspace import roots, [`extraPaths`](../settings/python_analysis_extraPaths.md), or custom stubs
- For editable installs: Verify that the selected environment exposes the intended source through paths or supported hook discovery. See [How to Use Editable Installs with Pylance](editable-installs.md)

---

## Using `TYPE_CHECKING` for Type-Only Imports

Python's `typing.TYPE_CHECKING` constant is `False` at runtime but `True` for type checkers like Pylance. This is commonly used for:

- **Avoiding circular imports**: Import a type only for annotations, not at runtime.
- **Reducing startup cost**: Skip heavy imports that are only needed for type hints.

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heavy_module import HeavyClass

def process(obj: HeavyClass) -> None:  # Pylance resolves this
    ...
```

### How Pylance handles `TYPE_CHECKING` blocks

- Pylance treats `TYPE_CHECKING` as `True` and analyzes imports inside the block.
- Names imported under `TYPE_CHECKING` are available for type annotations.
- `from __future__ import annotations` (PEP 563) makes all annotations string-based, so the imported names don't need to exist at runtime.
- On Python 3.13 and earlier, use `from __future__ import annotations` or string annotations (`"HeavyClass"`) to avoid eager evaluation of names imported only under `TYPE_CHECKING`. Python 3.14+ defers annotation evaluation by default.

### Common errors

| Error                                             | Cause                                                                                 | Fix                                                                                                                             |
| ------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `"HeavyClass" is not defined` at runtime          | Eager annotation evaluation on Python 3.13 or earlier refers to a runtime-absent name | Add `from __future__ import annotations` or use `"HeavyClass"` as a string annotation                                           |
| Pylance shows errors inside `TYPE_CHECKING` block | Invalid import or type use                                                            | Fix the reported diagnostic in that file; [`ignore`](../settings/python_analysis_ignore.md) hides diagnostics in matching files |
| Circular import persists in Pylance               | Both modules import each other under `TYPE_CHECKING`                                  | Break the static import cycle or explicitly suppress `reportImportCycles`                                                       |

---

## Related Guides

- [How to Use Glob Patterns in Extra Paths with Pylance](extra-paths-glob-resolution.md) — wildcard `extraPaths` entries with deterministic ordering
- [How to Override Bundled Third-Party Stubs in Pylance](bundled-stubs.md) — override bundled package stubs with workspace-local custom stubs
- [How to Use Editable Installs with Pylance](editable-installs.md) — build backend compatibility and `.pth` file troubleshooting
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) — trace logging, search order, and log interpretation
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — config file precedence and setting interactions
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — multi-root workspaces, execution environments, and cross-package imports

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

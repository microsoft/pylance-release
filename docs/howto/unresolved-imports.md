# How to Fix Unresolved Import Errors in Pylance

Pylance uses static analysis to resolve Python imports — it does not execute your code. When it cannot find a module, it reports one of several diagnostics depending on what is missing. This guide covers the most common import errors, their causes, and how to fix them.

---

## Table of Contents

- [Import Could Not Be Resolved (`reportMissingImports`)](#import-could-not-be-resolved-reportmissingimports)
- [Import Could Not Be Resolved from Source (`reportMissingModuleSource`)](#import-could-not-be-resolved-from-source-reportmissingmodulesource)
- [Stub File Not Found (`reportMissingTypeStubs`)](#stub-file-not-found-reportmissingtypestubs)
- [Circular Import Detected (`reportImportCycles`)](#circular-import-detected-reportimportcycles)
- [Works at Runtime but Pylance Shows Errors](#works-at-runtime-but-pylance-shows-errors)
- [How Pylance Resolves Imports](#how-pylance-resolves-imports)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## Import Could Not Be Resolved (`reportMissingImports`)

**Symptom**: `Import "mypackage" could not be resolved` [`Pylance(reportMissingImports)`](../diagnostics/reportMissingImports.md)

### Diagnostic Steps

1. **Check the Python interpreter**: Click the Python version in the VS Code status bar. Verify it points to the correct virtual environment.

    ```bash
    # In the VS Code terminal, confirm:
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

3. **Check [`extraPaths`](../settings/python_analysis_extraPaths.md)**: Open Settings (JSON) and verify `python.analysis.extraPaths` includes the correct path.

4. **Check for editable install issues**: If using `pip install -e`:

    ```bash
    # Look for .pth files:
    find .venv/lib -name "*.pth" | xargs cat
    # Any line starting with "import" will be ignored by Pylance
    ```

5. **Enable verbose logging**: Add to settings.json:

    ```json
    {
        "python.analysis.logLevel": "Trace"
    }
    ```

    Then check the **Output** panel → **Pylance** for import resolution attempts. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) for a detailed walkthrough.

6. **Check [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: If it exists, it may override VS Code settings. Verify [`include`](../settings/python_analysis_include.md), [`exclude`](../settings/python_analysis_exclude.md), and [`extraPaths`](../settings/python_analysis_extraPaths.md). See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) for details on config file precedence.

### Common Causes and Fixes

| Cause                                                                                          | Fix                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Wrong interpreter selected                                                                     | Select the correct venv in VS Code status bar                                                                                  |
| Package not installed in the venv                                                              | `pip install mypackage` in the correct venv                                                                                    |
| [`extraPaths`](../settings/python_analysis_extraPaths.md) missing a directory                  | Add the package source dir to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                        |
| Editable install uses import hooks                                                             | Reinstall with `--config-settings editable_mode=compat`. See [How to Use Editable Installs with Pylance](editable-installs.md) |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides settings | Check and update the config file. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md)                      |
| [`include`](../settings/python_analysis_include.md) setting excludes the file                  | Verify [`python.analysis.include`](../settings/python_analysis_include.md) covers your files                                   |
| File is in [`exclude`](../settings/python_analysis_exclude.md) patterns                        | Remove from [`python.analysis.exclude`](../settings/python_analysis_exclude.md)                                                |
| Namespace package (no `__init__.py`)                                                           | Pylance supports namespace packages, but verify structure                                                                      |
| Missing `__init__.py` in a regular package                                                     | Add `__init__.py` to each package directory (even if empty) unless using namespace packages                                    |

---

## Import Could Not Be Resolved from Source (`reportMissingModuleSource`)

**Symptom**: `Import "mypackage" could not be resolved from source` `Pylance(reportMissingModuleSource)`

**What it means**: Pylance found a type stub (`.pyi`) for the package but could not find the corresponding Python source (`.py`). This is different from `reportMissingImports` — the import _does_ resolve (via stubs), but the source code is missing.

### Common Causes and Fixes

| Cause                                                                                | Fix                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package is a C extension or native library (`.so` / `.pyd`)                          | Safe to ignore — native extensions don't have `.py` source. Suppress with `"reportMissingModuleSource": "none"` in [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) |
| Package installed as `.pyc`-only (compiled wheel without source)                     | Install a source distribution, or suppress the diagnostic                                                                                                                                                      |
| Stubs installed separately (e.g., `types-requests`) but main package not in the venv | Install the main package: `pip install requests`                                                                                                                                                               |
| Stub-only package with no corresponding runtime package                              | Suppress for that specific package: `# type: ignore[reportMissingModuleSource]`                                                                                                                                |

---

## Stub File Not Found (`reportMissingTypeStubs`)

**Symptom**: `Stub file not found for "mypackage"` `Pylance(reportMissingTypeStubs)`

**What it means**: The package is installed and importable, but it has no type stubs (no `.pyi` files) and is not marked as `py.typed`. This diagnostic is **off by default** and only appears in `strict` type-checking mode (where it's an error).

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
- **Use `TYPE_CHECKING` imports** for type-only references:

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

This is one of the most common complaint patterns. It happens because Pylance does **static analysis** and cannot execute dynamic Python mechanisms.

### Things Pylance Cannot Follow

| Runtime Mechanism                                           | Why Pylance Can't Follow It                                                                                                                  | Fix                                                                                                                                                                                |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Import-hook `.pth` files** (lines starting with `import`) | Pylance reads `.pth` files but only processes plain path lines — it skips `import` lines                                                     | Reinstall with `--config-settings editable_mode=compat`, or enable `enableEditableInstalls` on Python 3.13+. See [How to Use Editable Installs with Pylance](editable-installs.md) |
| **`sys.path.append()` / `sys.path.insert()`** in code       | Pylance does not execute Python code — dynamic path modifications are invisible                                                              | Add the path to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                                                                                  |
| **`PYTHONPATH` environment variable**                       | Pylance does not read environment variables                                                                                                  | Add directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                                       |
| **`pkgutil.extend_path()` in `__init__.py`**                | Pylance resolves namespace packages statically — it picks the first match rather than merging all `sys.path` entries at runtime              | Add all contributing directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                      |
| **`importlib` dynamic imports**                             | All programmatic imports are invisible to static analysis                                                                                    | Use regular `import` statements or `TYPE_CHECKING` import blocks for type checking                                                                                                 |
| **Namespace packages across separate roots**                | Python merges same-named packages from different `sys.path` entries; Pylance resolves to the first match                                     | Put all contributing directories in [`extraPaths`](../settings/python_analysis_extraPaths.md) so Pylance sees all sources                                                          |
| **pytest `conftest.py` path injection**                     | pytest adds `conftest.py` directories and `rootdir` to `sys.path` at runtime; Pylance has no awareness of pytest's path logic                | Add test root directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                             |
| **Django `INSTALLED_APPS` / app autodiscovery**             | Django dynamically discovers and imports apps via settings; Pylance can't execute `django.setup()`                                           | Add each app's parent directory to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                       |
| **Conda environment path layout**                           | Conda environments store packages in `lib/pythonX.Y/site-packages` under the conda prefix, which may differ from a venv layout               | Select the conda interpreter in VS Code status bar; verify with `python -c "import sys; print(sys.prefix)"`                                                                        |
| **`sys.modules` patching**                                  | Some libraries inject modules into `sys.modules` at runtime (e.g., aliasing `pkg` → `pkg_v2`); Pylance cannot follow runtime module aliasing | Use `TYPE_CHECKING` imports for the real module name, or add a type stub                                                                                                           |
| **`site.addsitedir()`**                                     | Adds directories to `sys.path` at runtime and processes `.pth` files; Pylance does not call `site.addsitedir()`                              | Add the directories to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                                                                           |

### Framework-Specific Examples

**pytest**: If tests import helper modules from a `tests/` directory via conftest:

```
project/
├── src/mypackage/
├── tests/
│   ├── conftest.py      # pytest adds this dir to sys.path
│   └── helpers/
│       └── test_utils.py
```

pytest makes `from helpers.test_utils import ...` work at runtime but Pylance can't see it. Fix:

```json
{
    "python.analysis.extraPaths": ["./tests"]
}
```

**Django**: If your project uses app discovery via `INSTALLED_APPS`:

```
myproject/
├── myproject/
│   └── settings.py  # INSTALLED_APPS = ["users", "billing"]
├── users/
│   └── models.py
└── billing/
    └── models.py
```

Django resolves `from users.models import User` at runtime because `django.setup()` manipulates `sys.path`. Fix:

```json
{
    "python.analysis.extraPaths": ["."]
}
```

Or add the project root to [`extraPaths`](../settings/python_analysis_extraPaths.md) in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration).

**Flask**: If your Flask project uses blueprints or app factories spanning multiple packages:

```
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

Flask's app factory pattern uses `from app.extensions import db` which works at runtime because the project root is on `sys.path`. Fix:

```json
{
    "python.analysis.extraPaths": ["."]
}
```

### Diagnosis Workflow

1. **Confirm the runtime path**: `python -c "import mypackage; print(mypackage.__file__)"`
2. **Check Pylance's search paths**: Enable `"python.analysis.logLevel": "Trace"` and look in **Output → Pylance** for the import resolution log (see [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md))
3. **Compare**: Is the directory containing `mypackage` in Pylance's search paths? If not, add it to [`extraPaths`](../settings/python_analysis_extraPaths.md)

---

## How Pylance Resolves Imports

Pylance searches for modules in a specific order, stopping at the first match:

| Priority | Search Location                                                                                                                     | Notes                                |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| 1        | [`stubPath`](../settings/python_analysis_stubPath.md) (custom stubs)                                                                | Default: `./typings`                 |
| 2        | Bundled type stubs (Pylance ships with stubs for popular packages)                                                                  | e.g., `django-stubs`, `pandas-stubs` |
| 3        | Source files in the project root (or execution environment root)                                                                    | Your workspace files                 |
| 4        | [`extraPaths`](../settings/python_analysis_extraPaths.md) entries                                                                   | Searched in order listed             |
| 5        | `src/` directory (if [`autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) is `true` and `src/` has no `__init__.py`) | Automatic convenience path           |
| 6        | Typeshed stdlib stubs                                                                                                               | Standard library type info           |
| 7        | Python interpreter search paths (`site-packages`)                                                                                   | Third-party installed packages       |
| 8        | Typeshed third-party stubs                                                                                                          | Community-maintained stubs           |

**Key implications**:

- [`extraPaths`](../settings/python_analysis_extraPaths.md) entries have **higher priority** than installed packages in `site-packages`. This means workspace source code takes precedence over the same package installed from PyPI.
- If [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` with `[tool.pyright]` exists, VS Code's [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) setting is **ignored** — use `"extraPaths"` in the config file instead. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).

---

## Diagnostic Checklist

When imports aren't resolving, run through this checklist:

- [ ] **Interpreter**: Is the correct Python interpreter selected? (status bar)
- [ ] **Interpreter path**: Does `python -c "import sys; print(sys.prefix)"` in the VS Code terminal point to the right venv?
- [ ] **Package installed**: Is the package installed in that venv? (`pip show <package>`)
- [ ] **Editable install**: If editable, is the `.pth` file path-based (not import-hook)? See [How to Use Editable Installs with Pylance](editable-installs.md)
- [ ] **[`extraPaths`](../settings/python_analysis_extraPaths.md)**: Are paths configured to the right directory level?
- [ ] **[`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: Does a config file exist that might override settings?
- [ ] **[`include`](../settings/python_analysis_include.md)/[`exclude`](../settings/python_analysis_exclude.md)**: Are the correct files included and not excluded?
- [ ] **Pylance output**: Check Output panel → Pylance for any errors or warnings
- [ ] **Verbose logging**: Enable `"python.analysis.logLevel": "Trace"` and check for import resolution details. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md)
- [ ] **Restart**: Run "Python: Restart Language Server" after any configuration change

---

## FAQ

### Q: My .env file with PYTHONPATH is being ignored. Why?

Pylance does **not** read `.env` files for `PYTHONPATH`. Use [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) instead:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

If you need `PYTHONPATH` for runtime, keep the `.env` file for the Python extension's terminal integration, and separately configure [`extraPaths`](../settings/python_analysis_extraPaths.md) for Pylance.

### Q: Can I use `PYTHONPATH` environment variable instead of `extraPaths`?

Pylance does not use `PYTHONPATH` directly. It relies on [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) and the selected Python interpreter's `sys.path`. If you need the same paths available:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"],
    "python.envFile": "${workspaceFolder}/.env"
}
```

The `python.envFile` setting gives the Python extension access to env vars for terminal use, but it does **not** affect Pylance's import resolution.

### Q: How do I handle namespace packages (no `__init__.py`)?

Pylance supports [PEP 420](https://peps.python.org/pep-0420/) namespace packages. If your project uses them:

1. Ensure the parent directory is in [`extraPaths`](../settings/python_analysis_extraPaths.md) or is the workspace root
2. Do **not** add `__init__.py` to the namespace root
3. Each sub-package that contributes to the namespace should have its own `__init__.py`

```
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

| Setting                                                    | Effect on File Discovery | Effect on Diagnostics  | Effect on Import Resolution                                                         |
| ---------------------------------------------------------- | ------------------------ | ---------------------- | ----------------------------------------------------------------------------------- |
| Not in [`include`](../settings/python_analysis_include.md) | Not discovered           | No diagnostics         | Not resolved as workspace file                                                      |
| In [`exclude`](../settings/python_analysis_exclude.md)     | Not discovered           | No diagnostics         | Not resolved as workspace file (but still resolved if imported by an included file) |
| In [`ignore`](../settings/python_analysis_ignore.md)       | Discovered & analyzed    | Diagnostics suppressed | Resolved normally                                                                   |

### Q: How do I debug import resolution?

Enable trace logging and check the **Output → Pylance** panel:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

The log shows each search location Pylance tries (stubPath → project root → extraPaths → typeshed → site-packages) and whether it resolved or failed. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) for a detailed walkthrough.

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

The [`extraPaths`](../settings/python_analysis_extraPaths.md) entry should point to the directory that _contains_ the top-level `__init__.py` (or namespace package directory).

### Q: Go to Definition goes to the wrong location. How do I fix it?

**Symptom**: Go to Definition opens a file from `site-packages` instead of the source directory, or vice versa.

**Cause**: Pylance found the module through installed packages instead of the workspace source.

**Fix**:

- If you want source: Add the source directory to [`extraPaths`](../settings/python_analysis_extraPaths.md) (it has higher priority than `site-packages`)
- If you want installed: Remove the source directory from [`extraPaths`](../settings/python_analysis_extraPaths.md)
- For editable installs: Ensure the `.pth` file points to the correct location. See [How to Use Editable Installs with Pylance](editable-installs.md)

---

## Related Guides

- [How to Use Editable Installs with Pylance](editable-installs.md) — build backend compatibility and `.pth` file troubleshooting
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) — trace logging, search order, and log interpretation
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — config file precedence and setting interactions
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — multi-root workspaces, execution environments, and cross-package imports

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

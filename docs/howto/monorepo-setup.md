# How to Set Up a Python Monorepo with Pylance

A monorepo contains multiple Python packages or projects in a single repository. Pylance supports several strategies for working in monorepos, each with different trade-offs for import resolution, performance, and feature coverage.

This guide covers all the approaches, explains when to use each, and shows how to troubleshoot common problems.

---

## Table of Contents

- [Key Concepts](#key-concepts)
    - [Multi-Root Workspaces](#multi-root-workspaces)
    - [Extra Paths](#extra-paths)
    - [Editable Installs](#editable-installs)
        - [Python 3.13+ Enhanced Editable Install Support](#python-313-enhanced-editable-install-support)
    - [Execution Environments](#execution-environments)
    - [Use Nearest Configuration](#use-nearest-configuration)
    - [How They Relate](#how-they-relate)
- [Import Resolution Order](#import-resolution-order)
- [Setup Approaches](#setup-approaches)
    - [Approach 1: Single Root + extraPaths](#approach-1-single-root--extrapaths)
    - [Approach 2: Multi-Root Workspace](#approach-2-multi-root-workspace)
    - [Approach 3: Execution Environments](#approach-3-execution-environments)
    - [Approach 4: Editable Installs](#approach-4-editable-installs)
    - [Approach 5: Use Nearest Configuration](#approach-5-use-nearest-configuration)
    - [Approach 6: Combined (Editable + Multi-Root)](#approach-6-combined-editable--multi-root)
    - [Comparison Table](#comparison-table)
- [VS Code Settings Strategies](#vs-code-settings-strategies)
    - [Workspace-Level Settings](#workspace-level-settings)
    - [Folder-Level Settings in .code-workspace](#folder-level-settings-in-code-workspace)
    - [Per-Folder .vscode/settings.json](#per-folder-vscodesettingsjson)
    - [pyrightconfig.json / pyproject.toml](#pyrightconfigjson--pyprojecttoml)
    - [Settings Precedence](#settings-precedence)
- [Performance Tuning for Monorepos](#performance-tuning-for-monorepos)
    - [Language Server Mode](#language-server-mode)
    - [Diagnostic Mode](#diagnostic-mode)
    - [Indexing Controls](#indexing-controls)
    - [Exclude Patterns](#exclude-patterns)
    - [Exclude Entire Workspace Folders](#exclude-entire-workspace-folders)
    - [Performance Settings Summary](#performance-settings-summary)
- [Feature Impact](#feature-impact)
    - [How Setup Affects Features](#how-setup-affects-features)
    - [What Each Feature Needs](#what-each-feature-needs)
- [Troubleshooting](#troubleshooting)
    - [Import Could Not Be Resolved](#import-could-not-be-resolved)
    - [Wrong Python Interpreter](#wrong-python-interpreter)
    - [Slow Startup or High Memory](#slow-startup-or-high-memory)
    - [Auto-Import Suggests Wrong Packages](#auto-import-suggests-wrong-packages)
    - [Go to Definition Goes to Wrong Location](#go-to-definition-goes-to-wrong-location)
    - [Diagnostics Missing for Some Files](#diagnostics-missing-for-some-files)
    - [Editable Install Not Recognized](#editable-install-not-recognized)
    - [Settings Not Taking Effect](#settings-not-taking-effect)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## Key Concepts

### Multi-Root Workspaces

A VS Code [multi-root workspace](https://code.visualstudio.com/docs/editor/multi-root-workspaces) opens multiple folders in a single window using a `.code-workspace` file.

```jsonc
// myproject.code-workspace
{
    "folders": [{ "path": "packages/api" }, { "path": "packages/shared" }, { "path": "packages/worker" }],
    "settings": {},
}
```

**What Pylance does**: Creates a separate analysis service (analyzer instance) for each workspace folder. Each folder gets:

- Its own Python interpreter
- Its own [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) / [`pyproject.toml`](https://microsoft.github.io/pyright/#/configuration?id=pyprojecttoml-sample) lookup
- Its own [`include`](../settings/python_analysis_include.md) / [`exclude`](../settings/python_analysis_exclude.md) / [`extraPaths`](../settings/python_analysis_extraPaths.md) settings
- Independent diagnostics and IntelliSense

**Key implication**: Settings in one folder do not affect other folders.

### Extra Paths

[`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) tells Pylance to look in additional directories when resolving imports, similar to adding entries to `sys.path`.

```json
{
    "python.analysis.extraPaths": ["./packages/shared/src", "./libs/common"]
}
```

**How it works**:

- Paths are searched **after** the workspace root, **before** third-party packages
- Relative paths resolve from the workspace root (or config file location for [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration))
- Each path is searched in the order listed

### Editable Installs

An [editable install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs) (`pip install -e .`) installs a package so that Python resolves imports to the source directory instead of copying files to `site-packages`.

**How Pylance detects editable installs**: Pylance reads `.pth` files in `site-packages`. These files contain directory paths that extend the import search path.

```
# Example .pth file content (path-based — works with Pylance):
/home/user/monorepo/packages/shared/src
```

> **Critical**: By default, Pylance only reads **path-based** `.pth` files. If a `.pth` file starts with `import` (an import-hook-based editable install), Pylance **ignores it**. This is a common cause of unresolved imports in monorepos. See [Python 3.13+ enhanced support](#python-313-enhanced-editable-install-support) below for an exception.

#### Python 3.13+ Enhanced Editable Install Support

When using **Python 3.13 or later**, Pylance can resolve import-hook-based editable installs that would otherwise be ignored. Enable this with:

```json
{
    "python.analysis.enableEditableInstalls": true
}
```

With this setting enabled, Pylance uses a sandboxed Python environment to execute dynamic `.pth` files and resolve the actual module paths. This means build backends that use import hooks (like setuptools' default mode) work **without** needing compat or strict mode.

**Requirements**:

- Python 3.13 or later selected as the workspace interpreter
- `python.analysis.enableEditableInstalls` set to `true`

**What changes**: The [Build Backend Compatibility](#build-backend-compatibility) table below assumes the default behavior (setting disabled or Python < 3.13). With this setting enabled on Python 3.13+, all build backends in the table that show "❌ No" become "✅ Yes" automatically.

#### Build Backend Compatibility

The table below shows compatibility with the **default** Pylance behavior. On Python 3.13+ with `python.analysis.enableEditableInstalls` enabled, all backends work regardless of their `.pth` file type.

| Build Backend        | Default Behavior  | Works with Pylance? | How to Fix                                                                                                                                                                                                                                                                  |
| -------------------- | ----------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **setuptools** (pip) | Import hooks      | ❌ No               | Use [compat mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#legacy-behavior) or [strict mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#strict-editable-installs), or enable `enableEditableInstalls` on Python 3.13+ |
| **setuptools** (uv)  | Import hooks      | ❌ No               | Add `[tool.uv] config-settings = { editable_mode = "compat" }`, or enable `enableEditableInstalls` on Python 3.13+                                                                                                                                                          |
| **uv_build**         | Path-based `.pth` | ✅ Yes              | No change needed                                                                                                                                                                                                                                                            |
| **Hatchling**        | Path-based `.pth` | ✅ Yes              | No change needed (unless `dev-mode-exact = true`)                                                                                                                                                                                                                           |
| **PDM**              | Path-based `.pth` | ✅ Yes              | No change needed (unless `editable-backend = "editables"`)                                                                                                                                                                                                                  |
| **Flit**             | Path-based `.pth` | ✅ Yes              | No change needed                                                                                                                                                                                                                                                            |
| **Maturin**          | Path-based `.pth` | ✅ Yes              | No change needed                                                                                                                                                                                                                                                            |
| **meson-python**     | Import hooks      | ❌ No               | Enable `enableEditableInstalls` on Python 3.13+                                                                                                                                                                                                                             |

#### Fixing setuptools Editable Installs

**Option A: compat mode** (recommended for most cases)

```toml
# pyproject.toml
[tool.setuptools]
# nothing special needed, just use the pip flag:
```

```bash
pip install -e . --config-settings editable_mode=compat
```

**Option B: compat mode with uv**

```toml
# pyproject.toml
[tool.uv]
config-settings = { editable_mode = "compat" }
```

```bash
uv pip install -e .
```

**Option C: strict mode**

```bash
pip install -e . --config-settings editable_mode=strict
```

#### Verifying Editable Install Works

Check that a path-based `.pth` file exists in your `site-packages`:

```bash
# Find .pth files for your package
find .venv/lib/python*/site-packages -name "*.pth" | xargs grep -l "your_package"

# Or on Windows:
Get-ChildItem -Recurse .venv\Lib\site-packages\*.pth | Select-String "your_package"
```

A working `.pth` file looks like:

```
/absolute/path/to/your/package/src
```

A **dynamic** `.pth` file (ignored by default, but supported on Python 3.13+ with `enableEditableInstalls`) looks like:

```
import _editable_finder; _editable_finder.install(...)
```

### Execution Environments

`executionEnvironments` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) defines separate analysis contexts for different parts of a monorepo, each with their own Python version, import paths, and diagnostic settings.

```jsonc
// pyrightconfig.json
{
    "executionEnvironments": [
        {
            "root": "packages/api",
            "pythonVersion": "3.11",
            "extraPaths": ["packages/shared/src"],
        },
        {
            "root": "packages/worker",
            "pythonVersion": "3.10",
            "extraPaths": ["packages/shared/src"],
        },
        {
            "root": "packages/shared",
        },
    ],
}
```

**How matching works**: Files are assigned to the **first** execution environment whose `root` contains the file. If no environment matches, the default (project root) is used.

**Per-environment overrides**:

- `pythonVersion` — e.g. `"3.9"`, `"3.12"`
- `pythonPlatform` — `"Windows"`, `"Darwin"`, `"Linux"`, `"All"`
- [`extraPaths`](../settings/python_analysis_extraPaths.md) — array of additional search paths (overrides the global [`extraPaths`](../settings/python_analysis_extraPaths.md) for files in this environment)
- Any [diagnostic rule](https://microsoft.github.io/pyright/#/configuration?id=type-check-diagnostics-settings) — e.g. `"reportMissingImports": "warning"`

**Important**: If file A (in environment 1) imports file B (in environment 2), imports from B use environment 2's [`extraPaths`](../settings/python_analysis_extraPaths.md), not environment 1's.

### Use Nearest Configuration

[`python.analysis.useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) makes Pylance auto-discover [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or [`pyproject.toml`](https://microsoft.github.io/pyright/#/configuration?id=pyprojecttoml-sample) (with `[tool.pyright]`) files in subdirectories, creating a virtual workspace for each.

```json
{
    "python.analysis.useNearestConfiguration": true
}
```

**Example**: With this structure:

```
monorepo/
├── packages/
│   ├── api/
│   │   ├── pyrightconfig.json   ← virtual workspace created here
│   │   └── src/
│   ├── shared/
│   │   ├── pyproject.toml       ← virtual workspace if contains [tool.pyright]
│   │   └── src/
│   └── worker/
│       ├── pyrightconfig.json   ← virtual workspace created here
│       └── src/
```

Each package gets its own analysis scope without needing a `.code-workspace` file.

**Skipped directories**: any directory starting with `.` (covers `.git`, `.vscode`, `.venv`, `.env`, `.tox`, `.nox`, `.mypy_cache`, `.pytest_cache`, `.eggs`, etc.), plus `node_modules`, `__pycache__`, `venv`, `env`, `site-packages`, `dist`, `build`, and `*.egg-info`.

### How They Relate

```
                    ┌───────────────────────────────┐
                    │  Python Interpreter Selection │
                    │  (per workspace folder)       │
                    └──────────────┬────────────────┘
                                   │ determines sys.path
                                   │ & site-packages
                                   ▼
                    ┌────────────────────────────────┐
                    │  Workspace Structure           │
                    │                                │
                    │  Single Root ──or── Multi-Root │
                    │  (one analyzer)  (N analyzers) │
                    └──────────────┬─────────────────┘
                                   │ each analyzer uses
                                   ▼
              ┌─────────────────────────────────────────────┐
              │  Import Resolution (per analyzer)           │
              │                                             │
              │  1. extraPaths        (VS Code setting)     │
              │  2. executionEnvs     (pyrightconfig)       │
              │  3. editable installs (pip install -e)      │
              │  4. autoSearchPaths   (auto src/ detection) │
              │  5. nearestConfig     (auto-discovery)      │
              │                                             │
              │  → These are alternatives, not a pipeline.  │
              │    Pick the approach that fits your layout. │
              └─────────────────────────────────────────────┘
```

**In summary**:

- **Multi-root workspace** = physical separation (separate analyzer per folder)
- **executionEnvironments** = logical separation within one workspace (same analyzer, different configs per subtree)
- **[`extraPaths`](../settings/python_analysis_extraPaths.md)** = "add these dirs to the search path" (works with both)
- **Editable installs** = let the package manager handle it (Pylance reads `.pth` files)
- **[`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)** = automatic virtual workspaces without `.code-workspace`

---

## Import Resolution Order

When you write `import mypackage`, Pylance searches in this order (see also [Pyright import resolution](https://microsoft.github.io/pyright/#/import-resolution)):

| Priority | Source                              | Configured By                                                                                                             |
| -------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1        | Custom stub path                    | [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md) or `stubPath` in config                             |
| 2        | Execution environment root          | Workspace root or `executionEnvironments[].root`                                                                          |
| 3        | Extra paths (in order)              | [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) or `executionEnvironments[].extraPaths`         |
| 4        | Auto-detected `src/` directory      | [`python.analysis.autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) (only when no execution environments) |
| 5        | Installed stub packages (`*-stubs`) | Python environment (`site-packages`)                                                                                      |
| 6        | Inline stubs (`.pyi` in packages)   | Python environment                                                                                                        |
| 7        | `py.typed` packages                 | Python environment                                                                                                        |
| 8        | Library code (`.py` files)          | Enabled by [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md)              |
| 9        | Typeshed stdlib stubs               | Bundled or [`typeshedPath`](../settings/python_analysis_typeshedPaths.md)                                                 |
| 10       | Typeshed third-party stubs          | Bundled or [`typeshedPath`](../settings/python_analysis_typeshedPaths.md)                                                 |
| 11       | Fallback (same dir + parent dirs)   | Automatic                                                                                                                 |

For **relative imports** (`from . import something`), resolution is always relative to the importing file's location.

---

## Setup Approaches

### Approach 1: Single Root + extraPaths

Open the monorepo root in VS Code and add package source directories to [`extraPaths`](../settings/python_analysis_extraPaths.md).

**Monorepo structure**:

```
monorepo/
├── .vscode/
│   └── settings.json
├── packages/
│   ├── api/
│   │   └── src/
│   │       └── api/
│   │           └── __init__.py
│   ├── shared/
│   │   └── src/
│   │       └── shared/
│   │           └── __init__.py
│   └── worker/
│       └── src/
│           └── worker/
│               └── __init__.py
└── pyproject.toml
```

**`.vscode/settings.json`**:

```json
{
    "python.analysis.extraPaths": ["./packages/api/src", "./packages/shared/src", "./packages/worker/src"]
}
```

**Pros**:

- Simple, one file to configure
- Single workspace, single interpreter
- Works for all VS Code features (search, git, etc.)

**Cons**:

- All packages share one Python interpreter
- Cross-package imports may suggest imports that don't work at runtime
- No per-package Python version or diagnostic rule overrides
- Must manually maintain the [`extraPaths`](../settings/python_analysis_extraPaths.md) list

**Best for**: Small monorepos where all packages share one Python version and the same set of dependencies.

### Approach 2: Multi-Root Workspace

Create a `.code-workspace` file with each package as a separate folder.

**`monorepo.code-workspace`**:

```jsonc
{
    "folders": [{ "path": "packages/api" }, { "path": "packages/shared" }, { "path": "packages/worker" }],
    "settings": {
        // Workspace-wide settings (shared across all folders)
        "python.analysis.diagnosticMode": "openFilesOnly",
    },
}
```

**Per-folder interpreter**: VS Code Python extension lets you select a different interpreter per folder. The status bar shows which interpreter is active.

**Per-folder settings**: Add folder-specific settings in the `.code-workspace` file:

```jsonc
{
    "folders": [
        {
            "path": "packages/api",
            "name": "API Service",
        },
        {
            "path": "packages/shared",
            "name": "Shared Library",
        },
    ],
    "settings": {
        // Global defaults
        "python.analysis.typeCheckingMode": "standard",
    },
}
```

Or use per-folder `.vscode/settings.json` files:

```
packages/
├── api/
│   ├── .vscode/
│   │   └── settings.json    ← API-specific settings
│   └── src/
├── shared/
│   ├── .vscode/
│   │   └── settings.json    ← Shared-specific settings
│   └── src/
```

**Cross-folder imports**: If `api` imports from `shared`, add `shared`'s source to `api`'s [`extraPaths`](../settings/python_analysis_extraPaths.md):

```json
// packages/api/.vscode/settings.json
{
    "python.analysis.extraPaths": ["../shared/src"]
}
```

**Pros**:

- Separate Python interpreters per package
- Separate settings (type checking, diagnostics) per package
- Clear physical isolation
- Each folder can have its own [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)

**Cons**:

- Higher memory use (separate analyzer per folder)
- Must create and maintain `.code-workspace` file
- Must manually configure cross-folder [`extraPaths`](../settings/python_analysis_extraPaths.md)
- With many folders (>10), can become slow and use significant RAM

**Best for**: Monorepos with packages that use different Python versions or different virtual environments.

### Approach 3: Execution Environments

Use a single `pyrightconfig.json` at the monorepo root to define per-subtree analysis.

**`pyrightconfig.json` (at monorepo root)**:

```jsonc
{
    "include": ["packages"],

    "executionEnvironments": [
        {
            "root": "packages/api",
            "pythonVersion": "3.11",
            "extraPaths": ["packages/shared/src"],
            "reportMissingImports": "error",
        },
        {
            "root": "packages/worker",
            "pythonVersion": "3.10",
            "extraPaths": ["packages/shared/src"],
            "reportMissingImports": "error",
        },
        {
            "root": "packages/shared",
            "pythonVersion": "3.10",
        },
        {
            "root": "packages",
            // Catch-all for anything else under packages/
        },
    ],
}
```

**Or in [`pyproject.toml`](https://microsoft.github.io/pyright/#/configuration?id=pyprojecttoml-sample)**:

```toml
[tool.pyright]
include = ["packages"]

[[tool.pyright.executionEnvironments]]
root = "packages/api"
pythonVersion = "3.11"
extraPaths = ["packages/shared/src"]

[[tool.pyright.executionEnvironments]]
root = "packages/worker"
pythonVersion = "3.10"
extraPaths = ["packages/shared/src"]

[[tool.pyright.executionEnvironments]]
root = "packages/shared"
pythonVersion = "3.10"
```

**Pros**:

- Lightweight — single workspace, single analyzer
- Per-subtree Python version and diagnostic rules
- Lower memory than multi-root
- Works with `code .`

**Cons**:

- Only one Python interpreter for installed packages (the workspace's selected interpreter)
- Must manually maintain environment list
- No VS Code UI for per-environment settings — config file only
- Environments match in order (first match wins) — ordering matters

**Best for**: Monorepos where packages need different Python versions or different diagnostic strictness but share one interpreter for installed packages.

### Approach 4: Editable Installs

Install each package as editable in a shared or per-package virtual environment.

**Step 1: Create virtual environment**:

```bash
cd monorepo
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows
```

**Step 2: Install packages as editable**:

```bash
# Using pip with setuptools (compat mode)
pip install -e ./packages/shared --config-settings editable_mode=compat
pip install -e ./packages/api --config-settings editable_mode=compat

# Using uv (with setuptools backend)
# Add to monorepo's pyproject.toml:
# [tool.uv]
# config-settings = { editable_mode = "compat" }
uv pip install -e ./packages/shared
uv pip install -e ./packages/api

# Using uv workspaces (recommended for uv-based monorepos)
# uv handles this automatically when packages are declared as workspace members
uv sync
```

**Step 3: Select the venv as interpreter** in VS Code (click the Python version in the status bar).

**Pros**:

- Matches runtime behavior exactly
- Pylance auto-discovers packages through `.pth` files
- No manual [`extraPaths`](../settings/python_analysis_extraPaths.md) needed
- Works with standard Python tooling (pytest, etc.)

**Cons**:

- Requires installing packages (not just opening the folder)
- Build backend must produce path-based `.pth` files (see [Build Backend Compatibility](#build-backend-compatibility))
- Need to re-install when adding new packages

**Best for**: Monorepos that already use `pip install -e` or uv workspaces as part of their development workflow.

### Approach 5: Use Nearest Configuration

Let Pylance auto-discover configurations in subdirectories.

**Step 1**: Enable the setting:

```json
{
    "python.analysis.useNearestConfiguration": true
}
```

**Step 2**: Add [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` with `[tool.pyright]` in each package:

```
monorepo/
├── .vscode/
│   └── settings.json          ← enable useNearestConfiguration
├── packages/
│   ├── api/
│   │   ├── pyrightconfig.json ← auto-discovered
│   │   └── src/
│   ├── shared/
│   │   ├── pyproject.toml     ← auto-discovered if has [tool.pyright]
│   │   └── src/
│   └── worker/
│       ├── pyrightconfig.json ← auto-discovered
│       └── src/
```

**Example `packages/api/pyrightconfig.json`**:

```json
{
    "include": ["src"],
    "pythonVersion": "3.11",
    "extraPaths": ["../shared/src"],
    "typeCheckingMode": "standard"
}
```

**Pros**:

- No `.code-workspace` file needed
- Works with `code .` (just open the monorepo root)
- Per-package configuration without manual workspace setup
- Each config file lives next to its package

**Cons**:

- Must add config files to each package
- Single Python interpreter for all (workspace-wide)
- Relatively new feature — may have edge cases
- Config file discovery only happens at workspace init and on file changes

**Best for**: Monorepos where each package already has (or should have) its own [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) / `pyproject.toml`, and you want zero-config workspace setup.

### Approach 6: Combined (Editable + Multi-Root)

For maximum isolation: use multi-root for separate interpreters and editable installs for cross-package imports.

**`monorepo.code-workspace`**:

```jsonc
{
    "folders": [{ "path": "packages/api" }, { "path": "packages/shared" }, { "path": "packages/worker" }],
    "settings": {
        "python.analysis.diagnosticMode": "openFilesOnly",
    },
}
```

**Per-folder setup**:

```bash
cd packages/api
python -m venv .venv
source .venv/bin/activate
pip install -e ../shared --config-settings editable_mode=compat
pip install -e . --config-settings editable_mode=compat
```

Each folder uses its own `.venv` → separate interpreter. Cross-package imports resolve through editable installs in each venv.

**Pros**:

- Full isolation (separate interpreters, separate dependencies)
- Cross-package imports work through standard Python mechanism
- Each package can have completely different dependency sets

**Cons**:

- Most complex setup
- Highest memory use
- Must install editable packages in each venv

**Best for**: Large, professional monorepos with strict dependency isolation between packages.

### Comparison Table

| Approach                                                                          | Isolation                                                      | Config                                                                                                                                           | Memory                         | Cross-Package Imports                                                          | Best For                                                  |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------- |
| [**Single Root + extraPaths**](#approach-1-single-root--extrapaths)               | Shared interpreter, shared settings                            | `.vscode/settings.json` only                                                                                                                     | Low                            | Manual [`extraPaths`](../settings/python_analysis_extraPaths.md) list          | Small monorepos, one Python version                       |
| [**Multi-Root Workspace**](#approach-2-multi-root-workspace)                      | Separate interpreter per folder                                | Per-folder `.vscode/settings.json` + per-folder `pyrightconfig.json`                                                                             | High (one analyzer per folder) | [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable installs | Different venvs per package                               |
| [**Execution Environments**](#approach-3-execution-environments)                  | Shared interpreter, per-subtree Python version and diagnostics | Single `pyrightconfig.json` with [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) | Low (single analyzer)          | [`extraPaths`](../settings/python_analysis_extraPaths.md) per environment      | Different strictness/version per subtree, RAM-constrained |
| [**Editable Installs**](#approach-4-editable-installs)                            | Shared interpreter, shared settings                            | None needed (Python tooling handles it)                                                                                                          | Low                            | Automatic via `.pth` files                                                     | Already using `pip install -e` or uv workspaces           |
| [**Use Nearest Config**](#approach-5-use-nearest-configuration)                   | Shared interpreter, per-package analysis scope                 | Auto-discovered `pyrightconfig.json` / `pyproject.toml` per package                                                                              | Low                            | [`extraPaths`](../settings/python_analysis_extraPaths.md) in each config file  | Per-package configs without `.code-workspace`             |
| [**Combined (Editable + Multi-Root)**](#approach-6-combined-editable--multi-root) | Separate interpreter per folder                                | Per-folder settings + editable installs                                                                                                          | High (one analyzer per folder) | Automatic via `.pth` files in each venv                                        | Strict dependency isolation between packages              |

---

## VS Code Settings Strategies

### Workspace-Level Settings

Settings in `.vscode/settings.json` at the workspace root apply to everything in that workspace.

```json
// monorepo/.vscode/settings.json
{
    "python.analysis.extraPaths": ["./packages/shared/src"],
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.typeCheckingMode": "standard"
}
```

### Folder-Level Settings in .code-workspace

In a `.code-workspace` file, you can set per-folder overrides:

```jsonc
{
    "folders": [
        {
            "path": "packages/api",
        },
        {
            "path": "packages/worker",
        },
    ],
    "settings": {
        // These apply to ALL folders
        "python.analysis.typeCheckingMode": "standard",
    },
}
```

> **Note**: VS Code `.code-workspace` files support a `settings` key at the top level (workspace-wide), but per-folder settings overrides in the workspace file are set through VS Code UI: open Settings, switch to the "Workspace" or specific folder tab, and edit from there. The resulting per-folder settings are stored in the folder's `.vscode/settings.json`.

### Per-Folder .vscode/settings.json

Each folder can have its own `.vscode/settings.json`:

```
monorepo/
├── packages/
│   ├── api/
│   │   ├── .vscode/
│   │   │   └── settings.json
│   │   └── src/
│   └── worker/
│       ├── .vscode/
│       │   └── settings.json
│       └── src/
```

```json
// packages/api/.vscode/settings.json
{
    "python.analysis.extraPaths": ["../shared/src"],
    "python.analysis.typeCheckingMode": "strict"
}
```

### pyrightconfig.json / pyproject.toml

[Pyright configuration files](https://microsoft.github.io/pyright/#/configuration) provide settings that VS Code `.vscode/settings.json` cannot:

- [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) — per-subtree analysis contexts
- [`include` / `exclude`](https://microsoft.github.io/pyright/#/configuration?id=main-configuration-options) — file-level control with wildcard support
- [`defineConstant`](https://microsoft.github.io/pyright/#/configuration?id=environment-options) — conditional type checking

```jsonc
// pyrightconfig.json
{
    "include": ["src", "tests"],
    "exclude": ["**/node_modules", "**/__pycache__"],
    "extraPaths": ["../shared/src"],
    "pythonVersion": "3.11",
    "typeCheckingMode": "standard",
}
```

**[`pyproject.toml`](https://microsoft.github.io/pyright/#/configuration?id=pyprojecttoml-sample) equivalent**:

```toml
[tool.pyright]
include = ["src", "tests"]
exclude = ["**/node_modules", "**/__pycache__"]
extraPaths = ["../shared/src"]
pythonVersion = "3.11"
typeCheckingMode = "standard"
```

### Settings Precedence

When multiple settings sources exist, they are applied in this order (later wins):

1. Pyright defaults
2. [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` `[tool.pyright]`
3. VS Code user settings
4. VS Code workspace settings (`.code-workspace` or `.vscode/settings.json`)
5. `python.analysis.languageServerMode` overrides (for settings at their default values)

**Important**:

- If a [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) exists, its [`include`](../settings/python_analysis_include.md)/[`exclude`](../settings/python_analysis_exclude.md) take precedence over the VS Code [`python.analysis.include`](../settings/python_analysis_include.md)/[`python.analysis.exclude`](../settings/python_analysis_exclude.md) settings.
- [`extraPaths`](../settings/python_analysis_extraPaths.md) from `pyrightconfig.json` and from VS Code settings are **not merged** — the config file's takes precedence.

### Variable Substitution

The following variables are supported in Pylance path settings (in `pyrightconfig.json` and VS Code settings). Note that only three specific environment variables are recognized — arbitrary `${env:VAR}` is not supported.

| Variable                  | Expands To                        | Example                              |
| ------------------------- | --------------------------------- | ------------------------------------ |
| `${workspaceFolder}`      | Root of the workspace folder      | `/home/user/monorepo`                |
| `${workspaceFolder:name}` | Root of a named workspace folder  | `/home/user/monorepo/packages/api`   |
| `${env:HOME}`             | Home directory (env var)          | `/home/user`                         |
| `${env:USERNAME}`         | Current username (env var)        | `user`                               |
| `${env:VIRTUAL_ENV}`      | Active virtual env path (env var) | `/home/user/monorepo/.venv`          |
| `~/path`                  | Home directory                    | `~/monorepo` → `/home/user/monorepo` |

**Example with multi-root workspace**:

```json
{
    "python.analysis.extraPaths": ["${workspaceFolder:shared}/src"]
}
```

---

## Performance Tuning for Monorepos

Large monorepos can cause high memory usage and slow IntelliSense. The following settings help manage performance.

### Language Server Mode

[`python.analysis.languageServerMode`](../settings/python_analysis_languageServerMode.md) provides preset configurations:

| Setting     | Features                          | Memory   | Best For                                          |
| ----------- | --------------------------------- | -------- | ------------------------------------------------- |
| `"default"` | Balanced features                 | Moderate | Most monorepos                                    |
| `"light"`   | Minimal features, open files only | Low      | Very large monorepos (>10 folders, 100k+ files)   |
| `"full"`    | All features, deep indexing       | High     | Small-to-medium projects wanting max IntelliSense |

**What `"light"` mode changes**:

| Setting                                                                                           | Default Value | Light Mode Value                                       |
| ------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------ |
| [`python.analysis.exclude`](../settings/python_analysis_exclude.md)                               | `[]`          | `["**"]` (exclude everything, analyze open files only) |
| [`python.analysis.indexing`](../settings/python_analysis_indexing.md)                             | `true`        | `false`                                                |
| [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)             | `"standard"`  | `"off"`                                                |
| [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) | `true`        | `false`                                                |
| `python.analysis.enablePytestSupport`                                                             | `true`        | `false`                                                |

```json
{
    "python.analysis.languageServerMode": "light"
}
```

> You can override individual settings even in light mode. For example, enable indexing in light mode:
>
> ```json
> {
>     "python.analysis.languageServerMode": "light",
>     "python.analysis.indexing": true
> }
> ```

### Diagnostic Mode

[`python.analysis.diagnosticMode`](../settings/python_analysis_diagnosticMode.md) controls which files get type-checked:

| Value                       | Behavior                                     | When to Use                    |
| --------------------------- | -------------------------------------------- | ------------------------------ |
| `"openFilesOnly"` (default) | Only analyzes files open in the editor       | Large monorepos                |
| `"workspace"`               | Analyzes all included files in the workspace | Small projects, CI-like checks |

```json
{
    "python.analysis.diagnosticMode": "openFilesOnly"
}
```

### Indexing Controls

| Setting                                                                                         | Default     | Effect                                                                                |
| ----------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------- |
| [`python.analysis.indexing`](../settings/python_analysis_indexing.md)                           | `true`      | Enable/disable the symbol indexer for auto-imports and workspace symbol search        |
| [`python.analysis.userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md) | `2000`      | Max user files to index. Set to `-1` for unlimited, `0` to disable user file indexing |
| [`python.analysis.packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md)       | (see below) | Control how deep to index third-party packages                                        |
| [`python.analysis.persistAllIndices`](../settings/python_analysis_persistAllIndices.md)         | `false`     | Persist third-party indices across VS Code sessions                                   |
| [`python.analysis.autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md) | `false`     | Show auto-import suggestions in completions                                           |

**Reducing indexing scope for large monorepos**:

```json
{
    "python.analysis.indexing": true,
    "python.analysis.userFileIndexingLimit": 500,
    "python.analysis.packageIndexDepths": [{ "name": "", "depth": 1 }]
}
```

**Disabling indexing entirely** (saves memory, loses auto-import for unopened files):

```json
{
    "python.analysis.indexing": false
}
```

### Exclude Patterns

[`python.analysis.exclude`](../settings/python_analysis_exclude.md) controls which files Pylance analyzes.

**Default excludes** (when you don't set this setting):

- `**/node_modules`
- `**/__pycache__`
- `**/.*` (hidden directories like `.git`, `.venv`)
- Virtual environment directories (detected automatically)

> **Warning**: Setting [`python.analysis.exclude`](../settings/python_analysis_exclude.md) **overrides** (not appends to) the defaults. If you customize it, include the defaults explicitly:
>
> ```json
> {
>     "python.analysis.exclude": ["**/node_modules", "**/__pycache__", "**/.*", "packages/legacy/**", "data/**"]
> }
> ```

**[`exclude`](../settings/python_analysis_exclude.md) vs [`ignore`](../settings/python_analysis_ignore.md)**:

| Setting                                                             | Behavior                                                                |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [`python.analysis.exclude`](../settings/python_analysis_exclude.md) | Files are not discovered or analyzed. Not part of the workspace.        |
| [`python.analysis.ignore`](../settings/python_analysis_ignore.md)   | Files are analyzed (imports still work) but diagnostics are suppressed. |

Use [`ignore`](../settings/python_analysis_ignore.md) when you need imports to resolve but don't want to see errors:

```json
{
    "python.analysis.ignore": ["packages/generated/**"]
}
```

### Exclude Entire Workspace Folders

In multi-root workspaces, you can exclude entire folders from analysis using a variable substitution:

```jsonc
// In .code-workspace file
{
    "settings": {
        "python.analysis.exclude": ["${workspaceFolder:legacy-service}"],
    },
}
```

This completely prevents Pylance from creating an analyzer for that folder, saving significant memory.

### Performance Settings Summary

**For very large monorepos (>100k files, >10 workspace folders)**:

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.diagnosticMode": "openFilesOnly"
}
```

**For medium monorepos (balanced)**:

```json
{
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.userFileIndexingLimit": 1000,
    "python.analysis.indexing": true
}
```

**For small monorepos (full features)**:

```json
{
    "python.analysis.languageServerMode": "full",
    "python.analysis.diagnosticMode": "workspace"
}
```

---

## Feature Impact

### How Setup Affects Features

Each feature below runs within a **single workspace folder's analyzer** unless noted otherwise. In multi-root workspaces, features only see files within that folder's program — which includes files reachable through [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable installs.

| Feature                              | Needs [`extraPaths`](../settings/python_analysis_extraPaths.md) / editable for cross-package? | Depends on [`indexing`](../settings/python_analysis_indexing.md)?                                    | Light mode behavior                                                        | Multi-root scope                                                                                          | Key settings                                                                                                                                                                                                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Import resolution**                | Yes — module must be reachable                                                                | No                                                                                                   | Works (only open files analyzed)                                           | Per-folder only; cross-folder needs [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable | [`extraPaths`](../settings/python_analysis_extraPaths.md), [`stubPath`](../settings/python_analysis_stubPath.md), [`autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md)                                                                                   |
| **Go to definition**                 | Yes — target module must be reachable                                                         | No                                                                                                   | Works                                                                      | Per-folder only; cross-folder needs [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable | [`extraPaths`](../settings/python_analysis_extraPaths.md), [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md)                                                                                                                            |
| **Auto-import completions**          | Yes — source must be discoverable                                                             | Improves coverage but not required; without indexing, only open/loaded files and stdlib are searched | Reduced coverage (indexing off by default), but still works for open files | Per-folder only                                                                                           | [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md), [`indexing`](../settings/python_analysis_indexing.md), [`packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md)                                                       |
| **Workspace symbol search** (Ctrl+T) | No — searches all user files in program                                                       | Improves coverage; without indexing, falls back to on-demand parsing                                 | Reduced scope (only open files in program), but still works                | **All folders** (aggregated across workspaces)                                                            | [`indexing`](../settings/python_analysis_indexing.md), [`includeVenvInWorkspaceSymbols`](../settings/python_analysis_includeVenvInWorkspaceSymbols.md), [`includeExtraPathSymbolsInSymbolSearch`](../settings/python_analysis_includeExtraPathSymbolsInSymbolSearch.md) |
| **Find all references**              | Yes — target files must be in the program                                                     | No                                                                                                   | Searches all files in program (in light mode, mainly open files)           | Per-folder only                                                                                           | —                                                                                                                                                                                                                                                                       |
| **Rename symbol**                    | Yes — but only **user code** files are modified                                               | No                                                                                                   | Only user code files in program (in light mode, mainly open files)         | Per-folder only                                                                                           | —                                                                                                                                                                                                                                                                       |
| **Type checking diagnostics**        | Yes — imported types must be resolvable                                                       | No                                                                                                   | Works for open files only                                                  | Per-folder                                                                                                | [`diagnosticMode`](../settings/python_analysis_diagnosticMode.md), [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md), [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md)                                   |
| **Hover information**                | Yes — symbol's type info must be reachable                                                    | No                                                                                                   | Works                                                                      | Per-folder only; cross-folder needs [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable | [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md)                                                                                                                                                                                       |

### What Each Feature Needs

**Import resolution & Go to Definition**: Require that Pylance can find the target module. Ensure the source is reachable via one of:

- [`extraPaths`](../settings/python_analysis_extraPaths.md)
- Editable install (`.pth` in `site-packages`)
- [`executionEnvironments[].extraPaths`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options)
- Installed package in the interpreter's `site-packages`

**Auto-import completions**: Work best with [`indexing`](../settings/python_analysis_indexing.md) enabled, which pre-indexes all workspace and library symbols for fast lookup. Without indexing, auto-imports still work but only for files already loaded in the program (open files, their imports, and pre-built stdlib indices). Third-party packages that haven't been opened or imported won't appear.

**Workspace symbol search (Ctrl+T)**: The only feature that searches **all workspace folders** in multi-root. With [`indexing`](../settings/python_analysis_indexing.md) enabled, searches pre-built indices for fast results. Without indexing, falls back to on-demand parsing of files in the program. By default, only **user code** is searched. To include library symbols, enable:

- [`includeVenvInWorkspaceSymbols`](../settings/python_analysis_includeVenvInWorkspaceSymbols.md) — adds symbols from the active venv's `site-packages` (default: `false`)
- [`includeExtraPathSymbolsInSymbolSearch`](../settings/python_analysis_includeExtraPathSymbolsInSymbolSearch.md) — adds symbols from [`extraPaths`](../settings/python_analysis_extraPaths.md) directories (default: `false`)

Enabling these may slow down workspace symbol search.

**Find all references**: Searches all files within the current workspace folder's program. Includes user code files, and also includes non-user files (like those in [`extraPaths`](../settings/python_analysis_extraPaths.md) or `site-packages`) if the file is **open in the editor**. In multi-root, only works within a single folder.

**Rename symbol**: Similar to Find All References, but **only modifies user code files** (files that are tracked by your workspace and are not third-party imports or typeshed stubs). Files reachable through [`extraPaths`](../settings/python_analysis_extraPaths.md) or `site-packages` that are not user code will be excluded from the rename — Pylance intentionally avoids modifying library code. In multi-root, only works within a single folder.

---

## Troubleshooting

### Import Could Not Be Resolved

**Symptom**: `Import "mypackage" could not be resolved` [`Pylance(reportMissingImports)`](../diagnostics/reportMissingImports.md)

**Diagnostic steps**:

1. **Check the Python interpreter**: Click the Python version in the VS Code status bar. Verify it's the correct virtual environment.

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

    Then check the **Output** panel → **Pylance** for import resolution attempts.

6. **Check [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: If it exists, it may override VS Code settings. Verify [`include`](../settings/python_analysis_include.md), [`exclude`](../settings/python_analysis_exclude.md), and [`extraPaths`](../settings/python_analysis_extraPaths.md).

**Common causes and fixes**:

| Cause                                                                                          | Fix                                                                                          |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Wrong interpreter selected                                                                     | Select the correct venv in VS Code status bar                                                |
| Package not installed in the venv                                                              | `pip install mypackage` in the correct venv                                                  |
| [`extraPaths`](../settings/python_analysis_extraPaths.md) missing a directory                  | Add the package source dir to [`extraPaths`](../settings/python_analysis_extraPaths.md)      |
| Editable install uses import hooks                                                             | Reinstall with `--config-settings editable_mode=compat`                                      |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides settings | Check and update the config file                                                             |
| [`include`](../settings/python_analysis_include.md) setting excludes the file                  | Verify [`python.analysis.include`](../settings/python_analysis_include.md) covers your files |
| File is in [`exclude`](../settings/python_analysis_exclude.md) patterns                        | Remove from [`python.analysis.exclude`](../settings/python_analysis_exclude.md)              |
| Namespace package (no `__init__.py`)                                                           | Pylance supports namespace packages, but verify structure                                    |

### Wrong Python Interpreter

**Symptom**: Pylance can't find packages that are installed, or finds wrong versions.

**In multi-root workspaces**: Each folder can have a different interpreter. The Python extension remembers the selection per folder.

**Steps**:

1. Click the Python version in the status bar
2. Select **"Enter interpreter path..."** or choose from the list
3. Confirm with: `python -c "import sys; print(sys.prefix)"`

**Hidden directory gotcha**: If workspace folders use hidden directories (starting with `.`), the Python extension may have trouble detecting the correct interpreter. Explicitly set the interpreter path.

### Slow Startup or High Memory

**Symptom**: Pylance uses >4GB RAM, syntax highlighting takes minutes, or "Extension host terminated unexpectedly."

**Common causes in monorepos**:

| Cause                                                                                            | Fix                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Too many workspace folders (>10)                                                                 | Use [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) instead, or exclude unused folders       |
| [`diagnosticMode`](../settings/python_analysis_diagnosticMode.md)`: "workspace"` with many files | Switch to `"openFilesOnly"`                                                                                                                                  |
| Indexing many files                                                                              | Reduce [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md) or set [`indexing`](../settings/python_analysis_indexing.md)`: false` |
| Virtual environments inside workspace                                                            | Ensure venvs are auto-excluded (check [`exclude`](../settings/python_analysis_exclude.md) settings)                                                          |
| Redundant file discovery (older Pylance)                                                         | Update to latest Pylance version                                                                                                                             |

**Quick fix for very large monorepos**:

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.indexing": false
}
```

### Auto-Import Suggests Wrong Packages

**Symptom**: Auto-import suggests `from packages.shared.src.shared.utils import X` instead of `from shared.utils import X`.

**Cause**: Pylance sees the file through the filesystem, not through the configured import path.

**Fix**: Configure [`extraPaths`](../settings/python_analysis_extraPaths.md) to point to the correct source root:

```json
{
    "python.analysis.extraPaths": [
        "./packages/shared/src" // ✅ Points to "shared" package root
    ]
}
```

Not:

```json
{
    "python.analysis.extraPaths": [
        "./packages/shared" // ❌ Points one level too high
    ]
}
```

The [`extraPaths`](../settings/python_analysis_extraPaths.md) entry should point to the directory that contains the top-level `__init__.py` (or namespace package directory).

### Go to Definition Goes to Wrong Location

**Symptom**: Go to Definition opens a file from `site-packages` instead of the source directory, or vice versa.

**Cause**: Pylance found the module through installed packages instead of the workspace source.

**Fix**:

- If you want source: Add the source directory to [`extraPaths`](../settings/python_analysis_extraPaths.md) (it has higher priority than `site-packages`)
- If you want installed: Remove the source directory from [`extraPaths`](../settings/python_analysis_extraPaths.md)
- For editable installs: Ensure the `.pth` file points to the correct location

### Diagnostics Missing for Some Files

**Symptom**: No errors, warnings, or IntelliSense for some files.

**Checks**:

1. Is [`diagnosticMode`](../settings/python_analysis_diagnosticMode.md) set to `"openFilesOnly"`? → Only open files get diagnostics
2. Is the file in [`python.analysis.exclude`](../settings/python_analysis_exclude.md)? → Remove it from exclude
3. Is [`python.analysis.include`](../settings/python_analysis_include.md) set? → Setting [`include`](../settings/python_analysis_include.md) overrides the default (all files). Make sure your file is covered.
4. Is [`languageServerMode`](../settings/python_analysis_languageServerMode.md) set to `"light"`? → In light mode, [`exclude`](../settings/python_analysis_exclude.md) defaults to `["**"]`, so only open files are analyzed

### Editable Install Not Recognized

**Symptom**: Package is installed as editable (`pip install -e`) but Pylance shows "could not be resolved."

**Steps**:

1. **Check for path-based `.pth` file**:

    ```bash
    cat .venv/lib/python*/site-packages/__editable__*.pth
    ```

    If the content starts with `import`, the build backend is using import hooks. Either:
    - Reinstall with compat mode (see [Build Backend Compatibility](#build-backend-compatibility)), or
    - On **Python 3.13+**, enable `"python.analysis.enableEditableInstalls": true` to let Pylance resolve import-hook-based installs directly (see [Python 3.13+ Enhanced Editable Install Support](#python-313-enhanced-editable-install-support))

2. **Reload Pylance**: After reinstalling or changing settings, run **"Python: Restart Language Server"** from the Command Palette.

3. **Check Python version in `.pth` filename**: The `.pth` file must be in the `site-packages` of the Python interpreter Pylance is using.

### Settings Not Taking Effect

**Symptom**: Changed a setting but Pylance behavior didn't change.

**Common causes**:

| Cause                                                                                                  | Fix                                                                |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides VS Code settings | Edit the config file instead                                       |
| Setting is in wrong scope (user vs workspace)                                                          | Move to workspace scope                                            |
| Multi-root: setting is in wrong folder                                                                 | Check which folder's settings apply                                |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md) override                     | Explicitly set the individual setting to override the mode default |
| Pylance needs restart                                                                                  | Run "Python: Restart Language Server"                              |

---

## Diagnostic Checklist

When something isn't working in your monorepo, run through this checklist:

- [ ] **Interpreter**: Is the correct Python interpreter selected? (status bar)
- [ ] **Interpreter path**: Does `python -c "import sys; print(sys.prefix)"` in the VS Code terminal point to the right venv?
- [ ] **Package installed**: Is the package installed in that venv? (`pip show <package>`)
- [ ] **Editable install**: If editable, is the `.pth` file path-based (not import-hook)?
- [ ] **[`extraPaths`](../settings/python_analysis_extraPaths.md)**: Are paths configured to the right directory level?
- [ ] **[`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)**: Does a config file exist that might override settings?
- [ ] **[`include`](../settings/python_analysis_include.md)/[`exclude`](../settings/python_analysis_exclude.md)**: Are the correct files included and not excluded?
- [ ] **Pylance output**: Check Output panel → Pylance for any errors or warnings
- [ ] **Verbose logging**: Enable `"python.analysis.logLevel": "Trace"` and check for import resolution details
- [ ] **Restart**: Run "Python: Restart Language Server" after any configuration change

---

## FAQ

### Q: Should I use multi-root workspace or execution environments?

**Multi-root** if packages need:

- Different Python interpreters (different venvs)
- Complete isolation of settings

**Execution environments** if packages:

- Share one interpreter but need different Python version analysis
- Need different diagnostic strictness per subtree
- RAM is a concern (single analyzer)

### Q: Can I use both [`extraPaths`](../settings/python_analysis_extraPaths.md) and [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options)?

Yes. [`extraPaths`](../settings/python_analysis_extraPaths.md) at the global level applies as the default for environments that don't override it. Each execution environment can have its own [`extraPaths`](../settings/python_analysis_extraPaths.md) that overrides the global one for files within that environment.

### Q: Does [`python.analysis.autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) work with execution environments?

[`autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) (default: `true`) auto-adds a `src/` directory to the search path if it exists and doesn't contain `__init__.py`. When execution environments are defined in a config file, the auto-detected `src/` path goes into the default execution environment but **does not** automatically apply to explicitly defined execution environments. Add `src` to each environment's [`extraPaths`](../settings/python_analysis_extraPaths.md) if needed.

### Q: How do I debug import resolution?

Enable verbose logging:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

Open the **Output** panel, select **Pylance**, and look for lines showing where Pylance searches for imports. You'll see each search path tried in order.

### Q: Why does Pylance crash with many workspace folders?

Each workspace folder creates a separate analyzer service. With many folders (>10–20), the combined memory usage can exceed the Node.js heap limit (default 8GB). Mitigations:

1. Use [`languageServerMode`](../settings/python_analysis_languageServerMode.md)`: "light"` to minimize per-folder memory
2. Exclude folders you're not working on: [`python.analysis.exclude`](../settings/python_analysis_exclude.md)`: ["${workspaceFolder:unused-folder}"]`
3. Switch to [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) instead (single analyzer)
4. Use [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) instead (still single workspace)

### Q: My .env file with PYTHONPATH is being ignored. Why?

Pylance does **not** read `.env` files for `PYTHONPATH`. Use [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) instead:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

If you need `PYTHONPATH` for runtime, keep the `.env` file for the Python extension's terminal integration, and separately configure [`extraPaths`](../settings/python_analysis_extraPaths.md) for Pylance.

### Q: How do I set up a uv workspace monorepo?

With [uv workspaces](https://docs.astral.sh/uv/concepts/workspaces/):

1. Define workspace members in the root `pyproject.toml`:

    ```toml
    [tool.uv.workspace]
    members = ["packages/*"]
    ```

2. Run `uv sync` to install all packages as editable.

3. Select the workspace venv as the Python interpreter in VS Code.

4. If using setuptools backend, ensure compat mode:

    ```toml
    [tool.uv]
    config-settings = { editable_mode = "compat" }
    ```

5. Verify `.pth` files exist:
    ```bash
    ls .venv/lib/python*/site-packages/__editable__*.pth
    ```

### Q: Can I use `PYTHONPATH` environment variable instead of [`extraPaths`](../settings/python_analysis_extraPaths.md)?

Pylance does not use `PYTHONPATH` directly. It relies on [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) and the selected Python interpreter's `sys.path`. If you need the same paths available:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"],
    "python.envFile": "${workspaceFolder}/.env"
}
```

The `python.envFile` setting gives the Python extension access to env vars for terminal use, but it does **not** affect Pylance's import resolution.

### Q: How do I handle namespace packages (no `__init__.py`) in a monorepo?

Pylance supports [PEP 420](https://peps.python.org/pep-0420/) namespace packages. If your monorepo uses them:

1. Ensure the parent directory is in [`extraPaths`](../settings/python_analysis_extraPaths.md) or is the workspace root
2. Do **not** add `__init__.py` to the namespace root
3. Each sub-package that contributes to the namespace should have its own `__init__.py`

```
monorepo/
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

### Q: What's the difference between [`include`](../settings/python_analysis_include.md), [`exclude`](../settings/python_analysis_exclude.md), and [`ignore`](../settings/python_analysis_ignore.md)?

| Setting                                                    | Effect on File Discovery | Effect on Diagnostics  | Effect on Import Resolution                                                         |
| ---------------------------------------------------------- | ------------------------ | ---------------------- | ----------------------------------------------------------------------------------- |
| Not in [`include`](../settings/python_analysis_include.md) | Not discovered           | No diagnostics         | Not resolved as workspace file                                                      |
| In [`exclude`](../settings/python_analysis_exclude.md)     | Not discovered           | No diagnostics         | Not resolved as workspace file (but still resolved if imported by an included file) |
| In [`ignore`](../settings/python_analysis_ignore.md)       | Discovered & analyzed    | Diagnostics suppressed | Resolved normally                                                                   |

### Q: How do I make Pylance see packages across workspace folders?

In multi-root workspaces, each folder is isolated. To import across folders:

**Option A: [`extraPaths`](../settings/python_analysis_extraPaths.md)** (simple)

```json
// In packages/api/.vscode/settings.json
{
    "python.analysis.extraPaths": ["../shared/src"]
}
```

**Option B: Editable installs** (matches runtime)

```bash
# In packages/api's venv:
pip install -e ../shared --config-settings editable_mode=compat
```

**Option C: Single root** with [`extraPaths`](../settings/python_analysis_extraPaths.md) (avoids the multi-root overhead entirely)

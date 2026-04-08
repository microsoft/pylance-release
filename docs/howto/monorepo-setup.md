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
- [Detect Your Current Setup](#detect-your-current-setup)
    - [Triage Questions](#triage-questions)
    - [Quick Diagnostic Commands](#quick-diagnostic-commands)
    - [Common Setup Conflicts](#common-setup-conflicts)
- [Setting Interaction Reference](#setting-interaction-reference)
    - [pyrightconfig.json Overrides VS Code Settings](#pyrightconfigjson-overrides-vs-code-settings)
    - [languageServerMode Default Overrides](#languageservermode-default-overrides)
    - [Common Problematic Combinations](#common-problematic-combinations)
- [Troubleshooting](#troubleshooting)
    - [Import Could Not Be Resolved](#import-could-not-be-resolved)
    - [Import Could Not Be Resolved from Source](#import-could-not-be-resolved-from-source)
    - [Stub File Not Found](#stub-file-not-found)
    - [Circular Import Detected](#circular-import-detected)
    - [Works at Runtime but Pylance Shows Errors](#works-at-runtime-but-pylance-shows-errors)
    - [Wrong Python Interpreter](#wrong-python-interpreter)
    - [Slow Startup or High Memory](#slow-startup-or-high-memory)
    - [Auto-Import Suggests Wrong Packages](#auto-import-suggests-wrong-packages)
    - [Go to Definition Goes to Wrong Location](#go-to-definition-goes-to-wrong-location)
    - [Diagnostics Missing for Some Files](#diagnostics-missing-for-some-files)
    - [Editable Install Not Recognized](#editable-install-not-recognized)
    - [Settings Not Taking Effect](#settings-not-taking-effect)
    - [Reading Pylance Import Resolution Logs](#reading-pylance-import-resolution-logs)
- [Working with Generated Code](#working-with-generated-code)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)
    - [Multi-root vs execution environments](#q-should-i-use-multi-root-workspace-or-execution-environments)
    - [extraPaths + executionEnvironments](#q-can-i-use-both-extrapaths-and-executionenvironments)
    - [autoSearchPaths + execution environments](#q-does-pythonanalysisautosearchpaths-work-with-execution-environments)
    - [Debug import resolution](#q-how-do-i-debug-import-resolution)
    - [Many workspace folders crash](#q-why-does-pylance-crash-with-many-workspace-folders)
    - [.env / PYTHONPATH ignored](#q-my-env-file-with-pythonpath-is-being-ignored-why)
    - [uv workspace setup](#q-how-do-i-set-up-a-uv-workspace-monorepo)
    - [PYTHONPATH vs extraPaths](#q-can-i-use-pythonpath-environment-variable-instead-of-extrapaths)
    - [Namespace packages](#q-how-do-i-handle-namespace-packages-no-__init__py-in-a-monorepo)
    - [include / exclude / ignore](#q-whats-the-difference-between-include-exclude-and-ignore)
    - [Cross-folder imports](#q-how-do-i-make-pylance-see-packages-across-workspace-folders)
    - [Poetry monorepo setup](#q-how-do-i-set-up-a-poetry-monorepo)
    - [Docker / Remote SSH / WSL](#q-how-do-i-use-pylance-in-docker-dev-containers-remote-ssh-or-wsl)
    - [diagnosticSeverityOverrides in monorepos](#q-how-do-i-use-diagnosticseverityoverrides-in-a-monorepo)
    - [Conda monorepo setup](#q-how-do-i-set-up-a-conda-monorepo)
    - [CI/CD with Pyright](#q-how-do-i-run-pyright-type-checking-in-cicd-for-a-monorepo)

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
| **Poetry**           | Path-based `.pth` | ✅ Yes              | Use `poetry install` with path dependencies in `pyproject.toml`                                                                                                                                                                                                             |
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

**Diagnosing per-folder memory usage**: In multi-root workspaces, identifying which folder consumes the most memory helps target optimizations:

1. Open **Help → Toggle Developer Tools → Console**.
2. Run `process.memoryUsage()` to see the extension host's total heap.
3. Narrow by temporarily removing workspace folders one at a time from `.code-workspace` and checking if memory drops.
4. For the offending folder, apply targeted fixes: switch to `"openFilesOnly"`, disable indexing, or tighten `exclude` patterns for that folder only.

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

## Detect Your Current Setup

Before troubleshooting, identify which setup approach your workspace uses. Check these indicators:

| Indicator                                                                                                                                                                                        | What It Means                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.code-workspace` file present                                                                                                                                                                   | **Multi-root workspace** (Approach 2 or 3)                                                                                                                      |
| Multiple folders listed in VS Code Explorer sidebar                                                                                                                                              | **Multi-root workspace** — check `.code-workspace` for per-folder settings                                                                                      |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) with [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) | **Execution environments** (Approach 3)                                                                                                                         |
| `pyproject.toml` with `[tool.pyright]` containing [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options)                                | **Execution environments** (Approach 3)                                                                                                                         |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` with `[tool.pyright]` at workspace root (without `executionEnvironments`)                        | **Single root with config file** — VS Code settings that the config overrides are ignored (see [Setting Interaction Reference](#setting-interaction-reference)) |
| [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) in `settings.json`                                                                                                     | **Extra paths** (Approach 1) — check if config file also exists (they conflict)                                                                                 |
| `__editable__*.pth` files in `site-packages`                                                                                                                                                     | **Editable installs** (Approach 4)                                                                                                                              |
| [`python.analysis.useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)`: true` in `settings.json`                                                                   | **Nearest configuration** (Approach 5)                                                                                                                          |
| Multiple [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) files in subdirectories                                                                                     | Likely **nearest configuration** (if enabled) or **multi-root workspace**                                                                                       |
| None of the above                                                                                                                                                                                | **Single root with defaults** — Pylance analyzes the workspace root as one project                                                                              |

### Triage Questions

When a user reports a monorepo issue, these questions quickly narrow down the cause:

1. **What error message do you see?** → Jump to the matching [Troubleshooting](#troubleshooting) section
2. **Does the import work at runtime?** (`python -c "import mypackage"`) → If yes, see [Works at Runtime but Pylance Shows Errors](#works-at-runtime-but-pylance-shows-errors)
3. **Do you have a `pyrightconfig.json` or `pyproject.toml` with `[tool.pyright]`?** → If yes, VS Code settings may be ignored (see [pyrightconfig.json Overrides](#pyrightconfigjson-overrides-vs-code-settings))
4. **How are you opening the repo?** Single folder (`code .`) vs `.code-workspace` file → Determines if multi-root isolation applies
5. **Are you using editable installs?** → Check `.pth` file contents (path-based vs import-hook)
6. **What `languageServerMode` are you using?** → `"light"` changes many defaults (see [languageServerMode Default Overrides](#languageservermode-default-overrides))

### Quick Diagnostic Commands

Run these in the VS Code integrated terminal to gather facts:

```bash
# 1. Which Python interpreter is Pylance using?
#    (click the Python version in the status bar to verify)
python -c "import sys; print(sys.prefix)"

# 2. What's in sys.path? (shows runtime search order)
python -c "import sys; print('\n'.join(sys.path))"

# 3. Any editable installs?
ls .venv/lib/python*/site-packages/__editable__*.pth 2>/dev/null   # Linux/macOS
Get-ChildItem .venv\Lib\site-packages\__editable__*.pth 2>$null    # Windows

# 4. Import-hook or path-based .pth?
cat .venv/lib/python*/site-packages/__editable__*.pth              # Linux/macOS
Get-Content .venv\Lib\site-packages\__editable__*.pth              # Windows
# Lines starting with "import" = import-hook (Pylance can't follow these)
# Plain paths = path-based (Pylance reads these)

# 5. Any pyrightconfig.json files?
find . -name "pyrightconfig.json" -not -path "*/node_modules/*"    # Linux/macOS
Get-ChildItem -Recurse -Filter pyrightconfig.json -Exclude node_modules  # Windows

# 6. Any pyproject.toml with [tool.pyright]?
grep -rl "tool.pyright" . --include="pyproject.toml"               # Linux/macOS
```

### Common Setup Conflicts

| Conflict                                                                                                                                                                           | Symptom                                                                                                                | Resolution                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `settings.json` sets [`extraPaths`](../settings/python_analysis_extraPaths.md) + [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) exists                | Yellow warning: _"python.analysis.extraPaths cannot be set when a Pyrightconfig.json or pyproject.toml is being used"_ | Move [`extraPaths`](../settings/python_analysis_extraPaths.md) into [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) |
| Multi-root workspace + relative [`extraPaths`](../settings/python_analysis_extraPaths.md)                                                                                          | Paths break when adding/removing workspace folders                                                                     | Use `${workspaceFolder}` variables or absolute paths                                                                                            |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md)`: "light"` + [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)`: true` | Virtual workspaces created but all files excluded                                                                      | Switch to `"default"` mode, or explicitly set [`exclude`](../settings/python_analysis_exclude.md) to a narrower pattern                         |
| Editable install + wrong interpreter selected                                                                                                                                      | `.pth` files exist but Pylance looks in wrong `site-packages`                                                          | Select the interpreter whose `site-packages` contains the `.pth` files                                                                          |

---

## Setting Interaction Reference

Some settings interact in non-obvious ways. This section documents the combinations that cause the most confusion.

### `pyrightconfig.json` Overrides VS Code Settings

When a [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` (with `[tool.pyright]`) exists in a workspace folder, the following VS Code settings **are ignored** — the config file takes precedence:

| Ignored VS Code Setting                                                                                     | Where to Set Instead                                                                                      |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md)                                   | `"extraPaths"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)             |
| [`python.analysis.include`](../settings/python_analysis_include.md)                                         | `"include"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                |
| [`python.analysis.exclude`](../settings/python_analysis_exclude.md)                                         | `"exclude"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                |
| [`python.analysis.ignore`](../settings/python_analysis_ignore.md)                                           | `"ignore"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                 |
| [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)                       | `"typeCheckingMode"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)       |
| [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md)                                       | `"stubPath"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)               |
| [`python.analysis.autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md)                         | `"autoSearchPaths"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)        |
| [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md)           | `"useLibraryCodeForTypes"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) |
| [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) | `"reportXxx"` rules in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)        |

Pylance shows a yellow warning squiggle in `settings.json` for any setting that a config file overrides. The warning message reads: _"python.analysis.extraPaths cannot be set when a Pyrightconfig.json or pyproject.toml is being used."_

### `languageServerMode` Default Overrides

[`languageServerMode`](../settings/python_analysis_languageServerMode.md) sets defaults for several settings. You can **override any individual setting** even when a mode is active — the mode only sets defaults, it doesn't lock them.

| Setting                                                                           | `"light"` Default | `"default"` Default | `"full"` Default |
| --------------------------------------------------------------------------------- | ----------------- | ------------------- | ---------------- |
| [`exclude`](../settings/python_analysis_exclude.md)                               | `["**"]`          | `[]`                | `[]`             |
| [`indexing`](../settings/python_analysis_indexing.md)                             | `false`           | `true`              | `true`           |
| [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)             | `"off"`           | `"standard"`        | (unchanged)      |
| [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) | `false`           | `true`              | `true`           |
| [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md)   | (unchanged)       | `false`             | `true`           |
| [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md)   | (unchanged)       | `2000`              | `-1` (unlimited) |

**Example**: Enable indexing in light mode:

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.indexing": true
}
```

### Common Problematic Combinations

| Combination                                                                                                                               | What Happens                                                                                                            | Fix                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `light` mode + `diagnosticMode: "workspace"`                                                                                              | `exclude: ["**"]` means no files are discovered, so `"workspace"` mode has nothing to analyze                           | Either switch to `"default"` mode, or explicitly set `exclude` to a narrower pattern                                                               |
| `light` mode + `indexing: true` (explicit)                                                                                                | Works — indexing is enabled because you explicitly set it. But `exclude: ["**"]` limits what gets indexed to open files | Also explicitly set `exclude` to include the directories you need                                                                                  |
| Config file exists + `extraPaths` in `settings.json`                                                                                      | VS Code setting ignored, yellow warning squiggle                                                                        | Move `extraPaths` into the config file                                                                                                             |
| `autoSearchPaths: true` + [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) | Auto-detected `src/` only applies to the **default** environment, not explicitly defined ones                           | Add `"src"` to each environment's `extraPaths`                                                                                                     |
| `useNearestConfiguration: true` + `exclude: ["**"]`                                                                                       | All virtual workspaces are excluded                                                                                     | Set `exclude` to only what you actually want excluded                                                                                              |
| Multi-root (>10 folders) + `diagnosticMode: "workspace"`                                                                                  | Each folder analyzes all its files — combined memory can exceed 8GB heap limit                                          | Use `"openFilesOnly"` or switch to [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) |
| Global `extraPaths` in config + `executionEnvironments[].extraPaths`                                                                      | Each execEnv's `extraPaths` **replaces** (not merges with) the global `extraPaths` for files in that environment        | Repeat common paths in each environment's `extraPaths`, or put shared packages in a location already on `sys.path`                                 |

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
| Missing `__init__.py` in a regular package                                                     | Add `__init__.py` to each package directory (even if empty) unless using namespace packages  |

### Import Could Not Be Resolved from Source

**Symptom**: `Import "mypackage" could not be resolved from source` `Pylance(reportMissingModuleSource)`

**What it means**: Pylance found a type stub (`.pyi`) for the package but could not find the corresponding Python source (`.py`). This is different from `reportMissingImports` — the import _does_ resolve (via stubs), but the source code is missing.

**Common causes in monorepos**:

| Cause                                                                                | Fix                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package is a C extension or native library (`.so` / `.pyd`)                          | Safe to ignore — native extensions don't have `.py` source. Suppress with `"reportMissingModuleSource": "none"` in [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) |
| Package installed as `.pyc`-only (compiled wheel without source)                     | Install a source distribution, or suppress the diagnostic                                                                                                                                                      |
| Stubs installed separately (e.g., `types-requests`) but main package not in the venv | Install the main package: `pip install requests`                                                                                                                                                               |
| Stub-only package with no corresponding runtime package                              | Suppress for that specific package: `# type: ignore[reportMissingModuleSource]`                                                                                                                                |

### Stub File Not Found

**Symptom**: `Stub file not found for "mypackage"` `Pylance(reportMissingTypeStubs)`

**What it means**: The package is installed and importable, but it has no type stubs (no `.pyi` files) and is not marked as `py.typed`. This diagnostic is **off by default** and only appears in `strict` type-checking mode (where it's an error).

**Common causes and fixes**:

| Cause                                            | Fix                                                                                                                                                                                                                         |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Third-party package without type support         | Install stubs if available: `pip install types-mypackage`                                                                                                                                                                   |
| No stubs available for the package               | Suppress: `"reportMissingTypeStubs": "none"` in [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md), or create a stub file in [`stubPath`](../settings/python_analysis_stubPath.md) |
| Package _is_ typed but missing `py.typed` marker | Report to the package maintainer, or create a local stub                                                                                                                                                                    |

### Circular Import Detected

**Symptom**: `Cycle detected in import chain` `Pylance(reportImportCycles)` — followed by a list of file paths forming the cycle.

**What it means**: Files form a circular dependency (A imports B, B imports C, C imports A). This diagnostic is **off by default** — you only see it when `reportImportCycles` is explicitly enabled.

**Mitigation strategies**:

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

### Works at Runtime but Pylance Shows Errors

**Symptom**: `import mypackage` works in the terminal (`python -c "import mypackage"` succeeds), but Pylance shows `reportMissingImports`.

This is the most common monorepo complaint pattern. It happens because Pylance does **static analysis** and cannot execute dynamic Python mechanisms.

**Things Pylance cannot follow**:

| Runtime Mechanism                                           | Why Pylance Can't Follow It                                                                                                                  | Fix                                                                                                                       |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Import-hook `.pth` files** (lines starting with `import`) | Pylance reads `.pth` files but only processes plain path lines — it skips `import` lines                                                     | Reinstall with `--config-settings editable_mode=compat`, or enable `enableEditableInstalls` on Python 3.13+               |
| **`sys.path.append()` / `sys.path.insert()`** in code       | Pylance does not execute Python code — dynamic path modifications are invisible                                                              | Add the path to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                         |
| **`PYTHONPATH` environment variable**                       | Pylance does not read environment variables                                                                                                  | Add directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                              |
| **`pkgutil.extend_path()` in `__init__.py`**                | Pylance resolves namespace packages statically — it picks the first match rather than merging all `sys.path` entries at runtime              | Add all contributing directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                             |
| **`importlib` dynamic imports**                             | All programmatic imports are invisible to static analysis                                                                                    | Use regular `import` statements or `TYPE_CHECKING` import blocks for type checking                                        |
| **Namespace packages across separate roots**                | Python merges same-named packages from different `sys.path` entries; Pylance resolves to the first match                                     | Put all contributing directories in [`extraPaths`](../settings/python_analysis_extraPaths.md) so Pylance sees all sources |
| **pytest `conftest.py` path injection**                     | pytest adds `conftest.py` directories and `rootdir` to `sys.path` at runtime; Pylance has no awareness of pytest's path logic                | Add test root directories to [`extraPaths`](../settings/python_analysis_extraPaths.md)                                    |
| **Django `INSTALLED_APPS` / app autodiscovery**             | Django dynamically discovers and imports apps via settings; Pylance can't execute `django.setup()`                                           | Add each app's parent directory to [`extraPaths`](../settings/python_analysis_extraPaths.md)                              |
| **Conda environment path layout**                           | Conda environments store packages in `lib/pythonX.Y/site-packages` under the conda prefix, which may differ from a venv layout               | Select the conda interpreter in VS Code status bar; verify with `python -c "import sys; print(sys.prefix)"`               |
| **`sys.modules` patching**                                  | Some libraries inject modules into `sys.modules` at runtime (e.g., aliasing `pkg` → `pkg_v2`); Pylance cannot follow runtime module aliasing | Use `TYPE_CHECKING` imports for the real module name, or add a type stub                                                  |
| **`site.addsitedir()`**                                     | Adds directories to `sys.path` at runtime and processes `.pth` files; Pylance does not call `site.addsitedir()`                              | Add the directories to [`extraPaths`](../settings/python_analysis_extraPaths.md) instead                                  |

**Framework-specific examples**:

**pytest**: If tests import helper modules from a `tests/` directory via conftest:

```
monorepo/
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
monorepo/
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
monorepo/
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

**pytest cross-package conftest sharing**: In a monorepo where multiple packages share test fixtures:

```
monorepo/
├── conftest.py              # shared fixtures for all packages
├── packages/
│   ├── core/
│   │   ├── src/core/
│   │   └── tests/
│   │       ├── conftest.py  # imports from root conftest
│   │       └── test_core.py
│   └── api/
│       ├── src/api/
│       └── tests/
│           ├── conftest.py
│           └── test_api.py  # uses fixtures from root + local conftest
└── tests/
    └── helpers/
        └── factories.py     # shared test factory functions
```

pytest makes the root `conftest.py` and `tests/helpers/` accessible via `sys.path` manipulation. Pylance can't see these. Fix:

```json
{
    "python.analysis.extraPaths": [".", "./tests", "./packages/core/src", "./packages/api/src"]
}
```

**Diagnosis workflow**:

1. **Confirm the runtime path**: `python -c "import mypackage; print(mypackage.__file__)"`
2. **Check Pylance's search paths**: Enable `"python.analysis.logLevel": "Trace"` and look in **Output → Pylance** for the import resolution log (see [Reading Pylance Import Resolution Logs](#reading-pylance-import-resolution-logs))
3. **Compare**: Is the directory containing `mypackage` in Pylance's search paths? If not, add it to [`extraPaths`](../settings/python_analysis_extraPaths.md)

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

> **Node.js heap limit**: Pylance's default heap limit is 8GB (`--max-old-space-size=8192`). If you hit "JavaScript heap out of memory" errors, you can:
>
> 1. **Increase the heap limit** — set [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md) to `"auto"` (downloads a standalone Node.js) and increase [`python.analysis.nodeArguments`](../settings/python_analysis_nodeArguments.md) to e.g. `["--max-old-space-size=16384"]`.
> 2. **Reduce Pylance's workload** — fewer workspace folders, `"openFilesOnly"`, disable indexing.
>
> See [Pylance memory management](https://aka.ms/AApf7ox) for more information.

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

### Reading Pylance Import Resolution Logs

When `"python.analysis.logLevel": "Trace"` is enabled, Pylance writes detailed import resolution output to the **Output** panel (select **Pylance** from the dropdown). Here's how to read it.

**Enable trace logging** (add to `settings.json`):

```json
{
    "python.analysis.logLevel": "Trace"
}
```

> **Warning**: Trace logging significantly increases output volume and may impact performance. Enable it temporarily for diagnosis, then remove it.

**Import resolution search order**: Pylance tries these locations in order, stopping at the first match:

| Priority | Search Location                                                      | Log Prefix                                                 |
| -------- | -------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1        | [`stubPath`](../settings/python_analysis_stubPath.md) (custom stubs) | `Looking in stubPath '...'`                                |
| 2        | Execution environment root (project root)                            | `Looking in root directory of execution environment '...'` |
| 3        | [`extraPaths`](../settings/python_analysis_extraPaths.md) entries    | `Looking in extraPath '...'`                               |
| 4        | Typeshed stdlib stubs                                                | `Looking for typeshed stdlib path`                         |
| 5        | Python interpreter search paths (`site-packages`)                    | `Looking in python search path '...'`                      |
| 6        | Typeshed third-party stubs                                           | `Looking for typeshed third-party path`                    |

**What to look for**:

- `Resolved import with file '...'` — Pylance found the module. The path tells you _where_ it resolved to.
- `Did not find file '...' or '...'` — exhausted options in that search location, trying the next.
- `Partially resolved import with directory '...'` — found a directory but no `__init__.py` or module file.
- `No python interpreter search path` — Pylance has no site-packages path. Check that the correct interpreter is selected.

**Example: successful import resolution**

A successful resolution looks like this — Pylance finds the module in one of its search locations and stops:

```
Looking in root directory of execution environment '/workspace'
Attempting to resolve using root path '/workspace'
Resolved import with file '/workspace/packages/shared/src/shared/utils.py'
```

This tells you the import resolved from the project root. If the path looks wrong (e.g., resolving to `site-packages` instead of your workspace source), adjust [`extraPaths`](../settings/python_analysis_extraPaths.md) so the preferred source has higher priority.

**Example: diagnosing a missing cross-package import**

If you see this sequence:

```
Looking in stubPath '/workspace/typings'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
Looking in root directory of execution environment '/workspace'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
Looking in python search path '/workspace/.venv/lib/python3.11/site-packages'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
```

This means Pylance checked `stubPath`, the workspace root, and `site-packages` but never found `mypackage`. The fix depends on how `mypackage` should be found:

- If it's a workspace package: Add its parent directory to [`extraPaths`](../settings/python_analysis_extraPaths.md)
- If it should be in `site-packages`: Check the interpreter selection or `pip install` it
- If it's an editable install: Check the `.pth` file contents (see [Editable Install Not Recognized](#editable-install-not-recognized))

**Note**: Import resolution logs are separate from `verboseOutput` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration). The `logLevel: "Trace"` setting controls Pylance's log output, while `verboseOutput` is a Pyright-level setting for additional CLI diagnostics.

---

### Working with Generated Code

Monorepos often contain generated Python files (protobuf/gRPC stubs, SQLAlchemy models, Django migrations, Pydantic datamodel-code-generator output). These files can cause noisy diagnostics or missing type information.

**Strategy 1: Add generated output to [`extraPaths`](../settings/python_analysis_extraPaths.md)**

If your build step generates Python files in an output directory:

```
monorepo/
├── proto/
│   └── service.proto
├── generated/          # protoc output: service_pb2.py, service_pb2_grpc.py
├── packages/api/
│   └── src/api/
│       └── client.py   # from generated.service_pb2 import ServiceRequest
```

```json
{
    "python.analysis.extraPaths": ["./generated"]
}
```

**Strategy 2: Use [`stubPath`](../settings/python_analysis_stubPath.md) for hand-written stubs**

If generated code is complex or has missing type info, create `.pyi` stub files:

```json
{
    "python.analysis.stubPath": "./typestubs"
}
```

```
monorepo/
├── typestubs/
│   └── generated/
│       ├── __init__.pyi
│       └── service_pb2.pyi   # hand-written or mypy-protobuf generated
```

**Strategy 3: Suppress diagnostics for generated files with [`ignore`](../settings/python_analysis_ignore.md)**

To keep Pylance from reporting errors in generated code you don't want to fix:

```json
{
    "python.analysis.ignore": ["generated/**"]
}
```

This still allows imports _from_ generated code to resolve — it only suppresses diagnostics _in_ those files.

**Strategy 4: Use [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) with a relaxed config**

Drop a `pyrightconfig.json` in the generated directory:

```json
// generated/pyrightconfig.json
{
    "typeCheckingMode": "off"
}
```

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

Enable trace logging and check the **Output → Pylance** panel:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

The log shows each search location Pylance tries (stubPath → project root → extraPaths → typeshed → site-packages) and whether it resolved or failed. See [Reading Pylance Import Resolution Logs](#reading-pylance-import-resolution-logs) for a detailed walkthrough of the log format, search order, and how to interpret the output.

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

### Q: How do I set up a Poetry monorepo?

[Poetry](https://python-poetry.org/) supports path dependencies between packages. With a layout like:

```
monorepo/
├── pyproject.toml          # root project
├── packages/
│   ├── core/
│   │   └── pyproject.toml
│   └── api/
│       └── pyproject.toml
```

1. Declare path dependencies in each package's `pyproject.toml`:

    ```toml
    # packages/api/pyproject.toml
    [tool.poetry.dependencies]
    core = { path = "../core", develop = true }
    ```

2. Run `poetry install` in each package (or from the root if using a workspace plugin like `poetry-monorepo`).

3. Verify `.pth` files are created:

    ```bash
    find .venv/lib -name "*.pth" | xargs cat
    ```

4. Select the Poetry-managed venv as the Python interpreter in VS Code.

Poetry uses path-based `.pth` files for editable installs, which Pylance reads natively. No additional `extraPaths` or config changes are needed.

### Q: How do I use Pylance in Docker Dev Containers, Remote SSH, or WSL?

When working in [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), [Remote SSH](https://code.visualstudio.com/docs/remote/ssh), or [WSL](https://code.visualstudio.com/docs/remote/wsl):

- **Use relative paths in [`extraPaths`](../settings/python_analysis_extraPaths.md)**: Absolute paths break across environments. Always use workspace-relative paths:

    ```json
    // ✅ Portable — works in any container, WSL, or remote host
    { "python.analysis.extraPaths": ["./packages/shared/src"] }

    // ❌ Breaks in containers — host path doesn't exist inside the container
    { "python.analysis.extraPaths": ["/home/user/monorepo/packages/shared/src"] }
    ```

- **Commit settings files**: Check `.vscode/settings.json` or `.code-workspace` files into the repo so every environment gets the same Pylance configuration.

- **Use editable installs** (`pip install -e`) as the most portable approach — they rely on the interpreter's `site-packages` path, which works identically in any environment.

- If using `pyrightconfig.json`, paths are already relative to the config file location, so they are naturally portable.

- **Dev Container setup** (`devcontainer.json`): Configure Pylance settings in the `customizations.vscode.settings` block so they apply automatically inside the container:

    ```jsonc
    // .devcontainer/devcontainer.json
    {
        "image": "mcr.microsoft.com/devcontainers/python:3.12",
        "postCreateCommand": "pip install -e ./packages/core -e ./packages/api",
        "customizations": {
            "vscode": {
                "extensions": ["ms-python.vscode-pylance"],
                "settings": {
                    "python.analysis.extraPaths": ["./packages/core/src", "./packages/api/src"],
                    "python.analysis.typeCheckingMode": "basic",
                },
            },
        },
    }
    ```

- **WSL note**: When opening a repo in WSL, VS Code runs Pylance on the Linux side. Ensure the Python interpreter path in the status bar points to a Linux path (e.g., `/home/user/.venv/bin/python`), not a Windows path. Windows Python interpreters are not usable from WSL.

- **Remote SSH**: Pylance runs entirely on the remote machine. Ensure Node.js and Python are available there. If you use [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md), the path must be valid on the remote host — setting it to `"auto"` is the safest approach for mixed local/remote workflows. Note that `nodeExecutable` has `"scope": "machine"`, so a global (User Settings) value set for your local machine will also be sent to the remote — override it in the remote machine's settings if needed.

- **GitHub Codespaces**: Works like Dev Containers. Add Pylance settings to `devcontainer.json` (see example above) and they apply automatically when the Codespace is created.

### Q: How do I use [`diagnosticSeverityOverrides`](https://microsoft.github.io/pyright/#/configuration?id=diagnostic-settings-defaults) in a monorepo?

[`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) lets you adjust the severity of specific diagnostics. In monorepos, common uses include:

**Suppress warnings for generated or vendored code** (via `pyrightconfig.json` per directory):

```json
// vendor/pyrightconfig.json — relaxed rules for third-party vendored code
{
    "typeCheckingMode": "off"
}
```

**Suppress `reportMissingModuleSource` for C extension packages**:

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingModuleSource": "none"
    }
}
```

**Use stricter settings for core packages and relaxed settings for scripts**:

```toml
# pyrightconfig.json at root
{
    "executionEnvironments": [
        { "root": "packages/core", "typeCheckingMode": "strict" },
        { "root": "scripts", "typeCheckingMode": "basic" }
    ]
}
```

> **Note**: `diagnosticSeverityOverrides` set in VS Code `settings.json` will be **ignored** if a `pyrightconfig.json` or `[tool.pyright]` section exists in the project. Move overrides into the config file in that case. See [pyrightconfig.json Overrides VS Code Settings](#pyrightconfigjson-overrides-vs-code-settings).

### Q: How do I set up a conda monorepo?

[Conda](https://docs.conda.io/) environments store packages in a different layout than pip venvs. In a monorepo:

1. **Create and activate the conda environment**:

    ```bash
    conda create -n monorepo python=3.12
    conda activate monorepo
    ```

2. **Install local packages as editable**:

    ```bash
    # conda does not natively support editable installs, so use pip inside conda:
    pip install -e ./packages/core --config-settings editable_mode=compat
    pip install -e ./packages/api --config-settings editable_mode=compat
    ```

3. **Select the conda interpreter in VS Code**: Click the Python version in the status bar and choose the conda environment (e.g., `~/anaconda3/envs/monorepo/bin/python`).

4. **Verify Pylance sees the packages**:

    ```bash
    python -c "import core; print(core.__file__)"
    ```

**Common pitfall**: If you install packages with `conda install` instead of `pip install -e`, Pylance will find the packages in `site-packages` (stubs or compiled) but may not have source code for Go to Definition. Use editable installs for source packages you're actively developing.

**If editable installs aren't feasible** (e.g., C extensions built with conda-build), add source directories to [`extraPaths`](../settings/python_analysis_extraPaths.md):

```json
{
    "python.analysis.extraPaths": ["./packages/core/src", "./packages/api/src"]
}
```

### Q: How do I run Pyright type checking in CI/CD for a monorepo?

[Pyright](https://github.com/microsoft/pyright) can run as a standalone CLI in CI to validate the same type checking that Pylance performs in the editor.

**Single-root monorepo with `pyrightconfig.json`**:

```yaml
# .github/workflows/typecheck.yml
name: Type Check
on: [push, pull_request]
jobs:
    pyright:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-python@v5
              with:
                  python-version: '3.12'
            - run: pip install -e ./packages/core -e ./packages/api
            - run: npx pyright
```

Pyright reads `pyrightconfig.json` (or `[tool.pyright]` in `pyproject.toml`) from the repo root and applies the same `extraPaths`, `executionEnvironments`, and diagnostic settings.

**Multi-package monorepo** (separate config per package):

```yaml
# .github/workflows/typecheck.yml
jobs:
    pyright:
        runs-on: ubuntu-latest
        strategy:
            matrix:
                package: [core, api, worker]
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-python@v5
              with:
                  python-version: '3.12'
            - run: pip install -e ./packages/${{ matrix.package }}
            - run: npx pyright --project packages/${{ matrix.package }}
```

**With [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)**: Pyright CLI does not support `useNearestConfiguration` (that is a Pylance-only VS Code setting). In CI, either use a root `pyrightconfig.json` with [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options), or run `npx pyright --project <path>` separately per package.

**Tips**:

- Pin the Pyright version: `npx pyright@1.1.390` to avoid surprise breakage.
- Use the same `typeCheckingMode` in CI as in your editor config.
- If your editor uses [`extraPaths`](../settings/python_analysis_extraPaths.md) in VS Code settings (not in a config file), replicate them in a `pyrightconfig.json` for CI, since Pyright CLI doesn't read VS Code settings.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

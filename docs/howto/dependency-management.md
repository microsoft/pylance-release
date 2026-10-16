# How to Manage Python Dependencies for Pylance

Pylance does not automatically install declared dependencies. It resolves imports using the selected interpreter and configured search paths. Most "missing dependency" complaints in the editor are really one of:

- The dependency is not installed in the active environment.
- It is installed, but in a different environment than the one Pylance is using.
- It is installed but the project's dependency declarations are inconsistent across `requirements.txt`, `pyproject.toml`, lockfiles, and PEP 723 inline metadata.

This guide explains how the common dependency declaration styles affect Pylance, how to inspect what Pylance currently sees, and how to keep declarations and the active environment in sync.

---

## Table of Contents

- [How Pylance Sees Dependencies](#how-pylance-sees-dependencies)
- [Inspect What Pylance Sees](#inspect-what-pylance-sees)
- [Generate a Dependency File](#generate-a-dependency-file)
- [Declaration Styles](#declaration-styles)
    - [requirements.txt](#requirementstxt)
    - [pyproject.toml](#pyprojecttoml)
    - [Lockfiles](#lockfiles)
    - [PEP 723 Inline Script Metadata](#pep-723-inline-script-metadata)
- [Multiple requirements files](#multiple-requirements-files)
- [Dependency Conflicts](#dependency-conflicts)
- [Missing Type Information](#missing-type-information)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## How Pylance Sees Dependencies

Pylance treats a dependency as "available" only when it can resolve an import for it. That means:

1. The package is installed under the active interpreter's `site-packages`, or somewhere on its `sys.path`.
2. Or the package source is reachable via [`extraPaths`](../settings/python_analysis_extraPaths.md), `pyrightconfig.json` `extraPaths`, or an editable install.
3. Or a stub-only package is installed (for example `types-requests`).

Pylance's dependency handling:

- Pylance reads `requirements.txt` and `pyproject.toml` to discover direct dependencies for auto-import suggestions. It does not automatically install packages declared in those files, `Pipfile`, `poetry.lock`, or `uv.lock`.
- The opt-in [Troubleshoot Missing Imports](../settings/python_analysis_enableTroubleshootMissingImports.md) Quick Fix can offer installation through Python Environments after you choose the packages.
- `PYTHONPATH` supplied by the Python environment-variable API, including `.env` values, can provide analysis search paths. Explicit `extraPaths` are placed before those paths.

Practical consequence: a project can be perfectly declared in `pyproject.toml` and still show import errors in the editor if you never installed the dependencies into the active environment.

See [How to Choose a Python Environment for Pylance](python-environments.md) for picking the environment, and [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) for unresolved-import triage.

---

## Inspect What Pylance Sees

Before changing any declaration file, confirm reality.

| Question                                  | How to answer it                                                                                                                                               |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Which interpreter is active?              | `pylancePythonEnvironments` for the workspace root.                                                                                                            |
| What packages does the environment list?  | `pylanceInstalledTopLevelModules` for the same workspace root. This lists top-level module names from the active environment.                                  |
| Which imports across the project resolve? | `pylanceImports`. Returns aggregated resolved and unresolved module-name lists across the workspace.                                                           |
| What does the runtime say?                | `pylanceRunCodeSnippet` with `import sys, importlib; print(importlib.import_module("pkg").__file__)` &mdash; tells you the actual location.                    |
| What settings does Pylance report?        | `pylanceSettings`. Watch for `extraPaths` and `useLibraryCodeForTypes`, and inspect `pyrightconfig.json` or `[tool.pyright]` separately for project overrides. |

A missing inventory entry does not prove that the runtime import will fail. Confirm with the runtime check above.

---

## Generate a Dependency File

Pylance can generate or update a dependency file from workspace imports:

1. Open the Command Palette and run **Pylance: Generate Dependency File**. Select the workspace folder if prompted.
2. Choose the dependency-file format and version-pinning style.
3. Choose **Merge only** to add missing packages while keeping existing entries, or **Sync** to also remove packages not found in the code.

The command applies edits to the dependency file; it does not install packages. Review the updated file, then use your package manager's install or sync workflow for the selected environment.

---

## Declaration Styles

Different projects declare dependencies in different ways. They do not all behave the same in the editor.

### requirements.txt

A flat list of pinned (or unpinned) packages, typically installed with `pip install -r requirements.txt`.

- **Pylance impact**: Pylance reads the root `requirements.txt` to discover direct dependencies for auto-import suggestions. The declarations do not install packages; imports still need installed packages or reachable sources.
- **Best for**: Simple deployments, CI pipelines, environments where you do not own the project metadata.
- **Common pitfalls**:
    - Multiple `requirements*.txt` files (`requirements.txt`, `requirements-dev.txt`, `requirements-test.txt`) often drift apart. The active environment may have only one of them installed, leaving editor errors for symbols defined in another.
    - `-r requirements-other.txt` chaining is followed by Pylance's direct-dependency discovery as well as by `pip`.
    - Unpinned versions can install a different release than CI uses, leading to type errors that only show up locally.

If you use `requirements.txt`, install the union of every file you need analyzed and confirm with `pylanceInstalledTopLevelModules`.

### pyproject.toml

The modern standard (PEP 518 / PEP 621). Tools like `pip`, `uv`, `poetry`, and `hatch` install from it.

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "requests>=2.31",
    "pydantic>=2",
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

- **Pylance impact**: Pylance reads `[project]` dependencies and optional dependencies for direct-dependency discovery, and `[tool.pyright]` for analysis configuration. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).
- **Best for**: Distributable libraries, tool-driven workflows.
- **Common pitfalls**:
    - Optional dependency groups (`pip install '.[dev]'`, `uv sync --all-extras`) must be installed explicitly. Forgetting `[dev]` is a frequent cause of "test framework not found" errors in the editor.
    - Workspaces (`uv` workspaces, Poetry path dependencies) need an actual install step before Pylance sees the cross-package code, unless you use editable installs or [`extraPaths`](../settings/python_analysis_extraPaths.md). See [How to Use Editable Installs with Pylance](editable-installs.md).

### Lockfiles

`uv.lock`, `poetry.lock`, `Pipfile.lock` describe the exact versions resolved by the tool. They are inputs for the installer, not for Pylance.

If the lockfile and the active environment disagree (for example you pulled a teammate's change to `uv.lock` but never ran `uv sync`), Pylance will show errors based on whatever is actually installed, not on the lockfile.

A good habit when imports start failing after a `git pull`:

1. Re-sync the environment (`uv sync`, `poetry install`, `pip install -r requirements.txt`, etc.).
2. Confirm with `pylanceInstalledTopLevelModules`.
3. Reload the window if necessary.

### PEP 723 Inline Script Metadata

[PEP 723](https://peps.python.org/pep-0723/) declares dependencies inline at the top of a single-file script:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27",
#     "rich",
# ]
# ///

import httpx
from rich import print
```

`uv run script.py` (and similar runners) creates an ephemeral environment satisfying that block, then runs the script.

Pylance impact:

- For an open local `.py` script, Pylance can use the file-specific PEP 723 interpreter selected by Python Environments.
- For an editor experience on PEP 723 scripts, point Pylance at a real environment that has those dependencies installed (for example a shared `.venv` you created with `uv pip install httpx rich`).
- For runtime, `pylanceRunCodeSnippet` runs against the workspace's active interpreter. If you actually want PEP 723 resolution at runtime, invoke `uv run` from a terminal instead.

---

## Multiple requirements files

Many projects keep separate files for different audiences:

```text
requirements.txt          # production
requirements-dev.txt      # tests, linters
requirements-docs.txt     # documentation toolchain
```

Pylance recognizes `[project.optional-dependencies]` and `[dependency-groups]` for direct-dependency discovery, but those declarations do not install the packages. To get a clean editor experience:

1. Decide which set of requirements is needed for the editor to be useful (usually production + dev).
2. Install all of them into the active venv.
3. Confirm with `pylanceInstalledTopLevelModules` that every package you need is present.

If different parts of the project genuinely need different environments (for example a `dashboard/` subproject with its own dependencies that conflict with the parent), use a multi-root workspace and give each folder its own venv. See [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) and [How to Choose a Python Environment for Pylance](python-environments.md).

For the same project structured as a single workspace folder, you can also use [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) `executionEnvironments` to point different subdirectories at different `extraPaths` and Python versions, while still installing one combined environment.

---

## Dependency Conflicts

Conflicts usually present in the editor as one of:

- A package "disappears" after a fresh install (because a transitive resolver downgraded or removed it).
- Imports resolve, but to an unexpected version (for example `pydantic` v1 features unavailable on a v2 install).
- `pylanceRunCodeSnippet` and `pylanceLSP` disagree.

Workflow:

1. Confirm versions: `pylanceRunCodeSnippet` with `import pkg; print(pkg.__version__)`.
2. Compare against the version expected by your declarations and lockfile.
3. If they disagree, the environment is out of sync. Re-run the relevant install / sync command.
4. If they agree but Pylance still complains, the issue is more likely a missing or wrong stub package &mdash; see [Missing Type Information](#missing-type-information).

When two transitive dependencies require incompatible versions of a third, no editor setting will fix that. Resolve the conflict in your declaration file (pin a compatible version, drop a dependency, or split into two environments).

---

## Missing Type Information

Pylance can sometimes resolve an import but show many `unknown` types or attribute errors for it. Common causes:

| Cause                                                                                                                                                     | Fix                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package is untyped (no `py.typed` marker, no inline annotations).                                                                                         | Install a stub package if available (`pip install types-requests`, `pip install types-PyYAML`, etc.).                                                                                                                                       |
| Package lacks stubs and needs library-source inference, but [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) is `false`. | Enable it. `light` language server mode disables it by default &mdash; see [How to Tune Pylance Performance](performance-tuning.md).                                                                                                        |
| Stubs you wrote locally are not picked up.                                                                                                                | Verify [`stubPath`](../settings/python_analysis_stubPath.md) points at the stub root (the directory containing per-package subdirectories), not at one specific package.                                                                    |
| Stub-only package installed but the runtime package is missing.                                                                                           | You will get `reportMissingModuleSource`. Install the runtime package or suppress the rule. See [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md#import-could-not-be-resolved-from-source-reportmissingmodulesource). |

For a wider tour of when to use `stubPath` vs `typeshedPaths` vs `useLibraryCodeForTypes`, see [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).

---

## Diagnostic Checklist

Use this when "missing dependency" complaints reach you:

1. `pylanceWorkspaceRoots` &mdash; capture the canonical workspace root URI.
2. `pylancePythonEnvironments` &mdash; confirm the active interpreter is the one the user expects.
3. `pylanceInstalledTopLevelModules` &mdash; inspect installed packages, then verify the import with `pylanceRunCodeSnippet`.
4. If not installed, install with the user's preferred package manager into that environment.
5. If installed but Pylance does not resolve it, run `pylanceImports` and check `pylanceSettings` for `extraPaths`, then inspect the project configuration separately for overrides.
6. If resolved but types are unknown, look for a stub package or change [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md).
7. Re-run `pylanceLSP` `textDocument/diagnostic` to confirm the error is gone.

---

## FAQ

### Q: Pylance shows errors but `python script.py` runs fine. Who is right?

Both are right about different things. The runtime ran whatever was on `sys.path` when you launched it. Pylance analyzed against its configured interpreter and search paths. If they disagree, the question is: which environment do you actually want the editor to reflect? Fix that one with [How to Choose a Python Environment for Pylance](python-environments.md).

### Q: I added a dependency to `pyproject.toml`. Why does Pylance still flag the import?

Adding the line does not install the package. Run your install/sync command (`uv sync`, `poetry install`, `pip install -e .[dev]`, etc.) and re-check `pylanceInstalledTopLevelModules`.

### Q: Can Pylance use a `requirements.txt` to know what to install?

Pylance reads `requirements.txt` for direct-dependency discovery, but does not automatically install it. Use your package manager for the full file; the opt-in missing-import Quick Fix can offer user-confirmed installation of individual missing packages.

### Q: How do I pin the editor to the same Python version as production?

The Python version comes from the selected interpreter. To pin the version independently of which interpreter the user happens to have, set `pythonVersion` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) (or under `[tool.pyright]` in `pyproject.toml`). Both Pylance and `pyright` honor it, which keeps the editor and CI in sync. See [How to Run Pyright in CI](ci-type-checking.md).

### Q: Does Pylance support PEP 723 scripts?

Pylance can use a PEP 723 interpreter selected for an open local `.py` script by Python Environments. Scripts that rely on PEP 723 work fine when run with `uv run`, but for the editor experience point Pylance at a real environment that has the dependencies installed.

### Q: How do I get Copilot to install a missing package?

Copilot can read this guide via `pylanceDocuments` and use `pylancePythonEnvironments` to identify the environment, but it should not run `pip install` against the wrong one. Tell Copilot the workspace root, ask it to confirm the active environment, and only then install. See [How to Fix Pylance Issues with Copilot](copilot-pylance-workflow.md).

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

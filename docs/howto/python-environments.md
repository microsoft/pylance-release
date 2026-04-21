# How to Choose a Python Environment for Pylance

Pylance resolves imports, infers types, and runs code analysis against a specific Python interpreter. If the wrong interpreter is selected, almost everything Pylance reports will be misleading: imports look broken, third-party types disappear, stdlib looks the wrong version, and `pip install` "does nothing".

This guide explains how Pylance picks an interpreter, how to switch it correctly, and how to handle workspaces that contain multiple environments (`venv`, `virtualenv`, `conda`, `uv`, `poetry`, `pipenv`, system Python).

---

## Table of Contents

- [How Pylance Picks an Interpreter](#how-pylance-picks-an-interpreter)
- [How to Inspect and Change the Active Interpreter](#how-to-inspect-and-change-the-active-interpreter)
- [Common Symptoms of a Wrong Interpreter](#common-symptoms-of-a-wrong-interpreter)
- [Virtual Environments](#virtual-environments)
- [Workspaces with Multiple Environments](#workspaces-with-multiple-environments)
- [uv-Managed Environments](#uv-managed-environments)
- [conda Environments](#conda-environments)
- [Poetry, Pipenv, Hatch](#poetry-pipenv-hatch)
- [Remote, WSL, and Container Environments](#remote-wsl-and-container-environments)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## How Pylance Picks an Interpreter

Pylance does not select interpreters on its own. It uses the interpreter chosen by the [Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

The Python extension picks an interpreter for each workspace folder using roughly this order, stopping at the first match:

1. The interpreter explicitly chosen for the workspace (saved in `python.defaultInterpreterPath` or in workspace state).
2. A virtual environment under the workspace folder (typical names: `.venv`, `venv`, `env`, `.env`).
3. An environment named in tooling files in the folder, such as `.python-version` (`pyenv`), `pyproject.toml` (`poetry`, `hatch`), or `Pipfile` (`pipenv`).
4. A `conda` environment recorded for the folder.
5. The first Python interpreter discovered on `PATH`.

Once selected, the interpreter:

- Determines `sys.path` and the `site-packages` Pylance searches for third-party packages.
- Determines the Python version Pylance assumes for type checking. Pylance derives the version from the interpreter itself. To pin the version independently of the interpreter, set `pythonVersion` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) (or `[tool.pyright]` in `pyproject.toml`).
- Determines what `pylanceRunCodeSnippet` and `pylancePythonDebug` execute against.

If the Python extension and Pylance disagree, Pylance loses. Always fix the Python extension's selection first.

---

## How to Inspect and Change the Active Interpreter

There are three reliable ways to inspect or switch interpreters.

### From the VS Code UI

1. Click the Python version in the status bar.
2. The interpreter quick pick lists detected environments.
3. Pick one. The selection is persisted per workspace folder.

If your environment is not listed:

- Open the folder that contains the venv as a workspace folder, or
- Run **Python: Select Interpreter** &rarr; **Enter interpreter path...** and provide the absolute path to `python` (or `python.exe`).

### From settings

Set `python.defaultInterpreterPath` in the appropriate scope. Workspace-folder scope wins:

```jsonc
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
}
```

On Windows, prefer `.venv/Scripts/python.exe`.

### From Copilot

Copilot can see and change the interpreter through Pylance's MCP tools:

- `pylancePythonEnvironments` &mdash; lists all discovered environments for a workspace root and marks which one is active.
- `pylanceUpdatePythonEnvironment` &mdash; switches the active environment.

`pylanceUpdatePythonEnvironment` accepts either a value returned by `pylancePythonEnvironments` or an absolute path to a Python executable. Pass the same `workspaceRoot` URI you got from `pylanceWorkspaceRoots`.

After switching, re-check diagnostics with `pylanceLSP` `textDocument/diagnostic` or `workspace/diagnostic`. See [How to Fix Pylance Issues with Copilot](copilot-pylance-workflow.md).

---

## Common Symptoms of a Wrong Interpreter

| Symptom                                                                  | Likely cause                                                                                                                                                 |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Every third-party `import` is unresolved.                                | Wrong interpreter, or no interpreter at all (system Python pointing at empty `site-packages`).                                                               |
| `pip install` succeeds but Pylance still flags the import.               | `pip` and the active interpreter point at different environments.                                                                                            |
| Stdlib types look wrong (for example `dict[str, int]` flagged as error). | Interpreter is older than expected, or `pythonVersion` in `pyrightconfig.json` / `[tool.pyright]` does not match the interpreter.                            |
| Some files resolve imports, others do not.                               | Multi-root workspace with one folder pointing at the wrong interpreter. See [Workspaces with Multiple Environments](#workspaces-with-multiple-environments). |
| `pylanceRunCodeSnippet` works but Pylance shows errors.                  | Common when the package is editable, uses import hooks, or relies on `.pth` files. See [How to Use Editable Installs with Pylance](editable-installs.md).    |
| Tests that run fine in the terminal show import errors in the editor.    | The terminal is using a different shell-activated environment than the editor.                                                                               |

A fast confirmation: run `pylanceRunCodeSnippet` with `import sys; print(sys.executable); print(sys.path)`. If that output does not match the interpreter you expected, the problem is interpreter selection, not Pylance.

---

## Virtual Environments

A virtual environment is a self-contained directory with its own `python` binary and `site-packages`. It is the recommended way to isolate dependencies for a single project.

Pylance treats venvs the same regardless of the tool that created them (`python -m venv`, `virtualenv`, `uv venv`, `poetry`, `hatch`, `pipenv`). The only thing Pylance cares about is the absolute path to the interpreter.

Recommended layout:

```text
my-project/
    .venv/                          # virtual environment
        bin/python                  # Linux / macOS
        Scripts/python.exe          # Windows
    src/...
    tests/...
    pyproject.toml
    .vscode/settings.json
```

Recommended workspace setting:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

On Windows replace with `${workspaceFolder}/.venv/Scripts/python.exe`.

Common pitfalls:

- Activating the venv in a terminal does not affect the editor. The editor uses the configured interpreter, not whatever happens to be on `PATH` in your shell.
- Deleting and recreating the venv leaves the editor pointing at a stale path until you reselect the interpreter.
- A venv inside the workspace is auto-discovered. A venv outside the workspace must be added by absolute path.

---

## Workspaces with Multiple Environments

A repository can contain multiple environments for legitimate reasons:

- A monorepo where each package owns its own venv.
- A project that ships a separate venv for build / automation tooling.
- Mixed runtimes (for example a service in Python 3.11 plus a script in Python 3.13).

Each VS Code workspace folder gets its own active interpreter. Pick the right strategy:

| Setup                                                               | Recommendation                                                                                                                                                                                              |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One repo, one logical project, one venv.                            | Single-folder workspace. Pin the interpreter via `python.defaultInterpreterPath` in `.vscode/settings.json`.                                                                                                |
| One repo, several packages, one shared venv.                        | Single-folder workspace plus [`extraPaths`](../settings/python_analysis_extraPaths.md) or editable installs to share code.                                                                                  |
| One repo, several packages, several venvs.                          | Multi-root workspace (`.code-workspace`). Each folder picks its own interpreter. See [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md).                                                     |
| Different Python versions for different parts.                      | Multi-root workspace, or use `executionEnvironments` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration). See [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md). |
| Separate environment for tooling that must not pollute the project. | Keep the tooling env outside the workspace, or in an explicitly excluded folder.                                                                                                                            |

When the same import appears resolved in one folder and unresolved in another, the cause is almost always per-folder interpreter selection or per-folder `extraPaths`. Inspect both sides with `pylancePythonEnvironments` and `pylanceSettings` before changing anything.

---

## uv-Managed Environments

[`uv`](https://docs.astral.sh/uv/) manages environments and dependencies in a layout Pylance handles natively, because the resulting venv is just a regular venv.

Typical setup:

```bash
uv venv .venv
uv sync                  # if a pyproject.toml exists
# or
uv pip install -r requirements.txt
```

Then point Pylance at it the same as any other venv:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

Notes specific to `uv`:

- `uv run <script>` resolves dependencies in a managed environment. Running a script with `uv run` does not change which interpreter Pylance uses in the editor &mdash; you still need to select the matching environment via the Python extension.
- `uv` supports [PEP 723 inline script metadata](dependency-management.md#pep-723-inline-script-metadata) for single-file scripts. Pylance does not currently parse PEP 723 metadata to add to its analysis search path; for an editor experience, point Pylance at a venv that has those dependencies installed.
- `uv` can create environments in arbitrary locations (`uv venv --python 3.12 path/to/env`). Add such environments by absolute interpreter path.

---

## conda Environments

`conda` and `mamba` environments are also detected by the Python extension. Pylance treats them as just another interpreter.

Things to watch for:

- A conda environment activated in a terminal does not change the editor's interpreter. Select it via **Python: Select Interpreter**.
- Mixing `conda install` and `pip install` in the same environment can produce a `site-packages` layout where Pylance sees a package but `import` fails at runtime, or vice versa. Prefer one tool per environment.
- For very large conda envs (data-science stacks), see [How to Tune Pylance Performance](performance-tuning.md).

---

## Poetry, Pipenv, Hatch

`poetry`, `pipenv`, and `hatch` create venvs in tool-specific locations. Pylance still only needs the absolute path to the resulting `python` binary.

| Tool     | Find the interpreter                                                                          |
| -------- | --------------------------------------------------------------------------------------------- |
| `poetry` | `poetry env info -p`, then append `/bin/python` (Linux/macOS) or `\Scripts\python.exe` (Win). |
| `pipenv` | `pipenv --venv`, then append `/bin/python` or `\Scripts\python.exe`.                          |
| `hatch`  | `hatch env find <env-name>`, then append `/bin/python` or `\Scripts\python.exe`.              |

Either select that path through **Python: Select Interpreter** &rarr; **Enter interpreter path...** or pin it in `python.defaultInterpreterPath`.

For `poetry`, see also [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md#q-how-do-i-set-up-a-poetry-monorepo).

---

## Remote, WSL, and Container Environments

When VS Code is connected to a remote workspace (SSH, WSL, dev container, Codespace), Pylance runs in the remote environment. Interpreter selection still happens through the Python extension, but only environments that exist on the remote side are visible.

Common gotchas:

- A venv created on the local machine is not visible in WSL or in a container.
- Mounted host paths can confuse interpreter discovery if the venv was built for a different OS.
- For containers, prefer building the venv as part of the container image, or in a path that survives container rebuilds.

See [How to Use Pylance in Remote Development](remote-development.md).

---

## Diagnostic Checklist

When the user reports "Pylance is broken", run this checklist before changing anything:

1. Get the active interpreter from `pylancePythonEnvironments`. Verify the path matches the user's expected venv.
2. From `pylanceRunCodeSnippet`, confirm `sys.executable` and `sys.version`.
3. From `pylanceInstalledTopLevelModules`, confirm the missing package is actually importable.
4. From `pylanceSettings`, look for `python.defaultInterpreterPath`, `python.analysis.extraPaths`, and any `pyrightconfig.json` / `[tool.pyright]` overrides (including `pythonVersion`).
5. Only then consider settings changes.

---

## FAQ

### Q: Why does Pylance ignore the venv I activated in the terminal?

The editor uses the interpreter selected by the Python extension. Terminal activation only affects new processes started from that terminal, not the language server. Select the interpreter through the UI or pin it in settings.

### Q: I switched interpreters and Pylance still shows the old errors.

Run **Developer: Reload Window** if diagnostics do not refresh after a switch. If you also changed `python.defaultInterpreterPath`, confirm with `pylancePythonEnvironments` that the new path is now active.

### Q: Can Pylance use multiple interpreters in a single folder?

Not directly. Each VS Code workspace folder gets one active interpreter. To analyze parts of the same folder under different Python versions or platforms, use `executionEnvironments` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration). See [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md#approach-3-execution-environments).

### Q: Should I commit `.vscode/settings.json` with `python.defaultInterpreterPath`?

Yes for relative paths under the workspace (`${workspaceFolder}/.venv/...`). Avoid committing absolute paths or user-specific locations &mdash; they will not work for other contributors.

### Q: How do I make the editor and a CI run agree?

CI typically does not use Pylance at all; it runs `pyright` (or another type checker) against a specific Python version. Match the editor's interpreter to the CI Python version, and prefer a project-level [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) with an explicit `pythonVersion` so both the editor and CI see the same configuration. See [How to Run Pyright in CI](ci-type-checking.md).

### Q: How do I tell Copilot which environment to use?

Tell Copilot the workspace root and let it run `pylancePythonEnvironments` &rarr; `pylanceUpdatePythonEnvironment`. You can also pass the absolute interpreter path directly. See [How to Fix Pylance Issues with Copilot](copilot-pylance-workflow.md).

# How to Use Editable Installs with Pylance

Editable installs (`pip install -e .`) let you develop a package and see changes reflected immediately without reinstalling. This guide explains how Pylance resolves editable installs, which build backends are compatible, and how to troubleshoot common issues.

---

## Table of Contents

- [How Editable Installs Work](#how-editable-installs-work)
- [Build Backend Compatibility](#build-backend-compatibility)
- [Python 3.13+ Enhanced Editable Install Support](#python-313-enhanced-editable-install-support)
- [Verifying Your Editable Install](#verifying-your-editable-install)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## How Editable Installs Work

When you run `pip install -e .`, pip creates a `.pth` file in the interpreter's `site-packages` directory. This file tells Python (and Pylance) where to find the package source code.

There are two kinds of `.pth` files:

| `.pth` File Type | Content                                                       | Pylance Support                                                                                      |
| ---------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Path-based**   | A plain filesystem path (e.g., `/home/user/myproject/src`)    | **Full support** — Pylance reads the path and resolves imports                                       |
| **Import-hook**  | A line starting with `import` (e.g., `import _editable_impl`) | **Not supported** (unless Python 3.13+ with `enableEditableInstalls`) — Pylance skips `import` lines |

The type depends on which build backend your project uses and how it's configured.

---

## Build Backend Compatibility

| Build Backend                     | Default `.pth` Type      | Pylance Works? | How to Get Path-Based `.pth`                                                             |
| --------------------------------- | ------------------------ | -------------- | ---------------------------------------------------------------------------------------- |
| **setuptools** (compat mode)      | Path-based               | Yes            | `pip install -e . --config-settings editable_mode=compat`                                |
| **setuptools** (strict mode)      | Import-hook              | No\*           | Switch to compat mode (see above)                                                        |
| **setuptools** (default, pre-v64) | Path-based               | Yes            | Default behavior                                                                         |
| **setuptools** (default, v64+)    | Import-hook (**strict**) | No\*           | Use `--config-settings editable_mode=compat`                                             |
| **Hatchling** / **hatch**         | Import-hook              | No\*           | No compat mode available — use [`extraPaths`](../settings/python_analysis_extraPaths.md) |
| **Flit**                          | Symlink or pth-file      | Usually yes    | Default creates symlinks or path-based `.pth`                                            |
| **PDM** (pep517)                  | Path-based               | Yes            | Default behavior                                                                         |
| **Poetry**                        | Path-based               | Yes            | Default behavior                                                                         |
| **Maturin** (Rust + Python)       | Import-hook              | No\*           | Use [`extraPaths`](../settings/python_analysis_extraPaths.md)                            |
| **Meson-python**                  | Import-hook              | No\*           | Use [`extraPaths`](../settings/python_analysis_extraPaths.md)                            |

\* Except on Python 3.13+ with `enableEditableInstalls` enabled — see below.

---

## Python 3.13+ Enhanced Editable Install Support

Starting with Python 3.13, the Python runtime provides APIs that let Pylance resolve import-hook-based editable installs directly.

To enable this:

```json
{
    "python.analysis.enableEditableInstalls": true
}
```

> **Warning**: This setting is currently **experimental** and may cause Pylance to stop working. Use it with caution and be prepared to disable it if you encounter issues.

**Requirements**:

- Python 3.13 or later selected as the interpreter
- The setting `python.analysis.enableEditableInstalls` set to `true`

When enabled, Pylance can resolve imports from any build backend's editable install, including those that use import hooks (setuptools strict, Hatchling, Maturin, etc.).

---

## Verifying Your Editable Install

### Step 1: Check that `.pth` files exist

```bash
# Linux/macOS
ls .venv/lib/python*/site-packages/__editable__*.pth

# Windows
Get-ChildItem .venv\Lib\site-packages\__editable__*.pth
```

### Step 2: Check the `.pth` file content

```bash
# Linux/macOS
cat .venv/lib/python*/site-packages/__editable__*.pth

# Windows
Get-Content .venv\Lib\site-packages\__editable__*.pth
```

- **Path-based** `.pth`: Shows a plain path like `/home/user/myproject/src` → Pylance can follow this
- **Import-hook** `.pth`: Shows `import _editable_impl` or similar → Pylance cannot follow this (unless Python 3.13+ with `enableEditableInstalls`)

### Step 3: Confirm the package resolves at runtime

```bash
python -c "import mypackage; print(mypackage.__file__)"
```

If this works but Pylance shows errors, see [How to Fix Unresolved Import Errors — Works at Runtime but Pylance Shows Errors](unresolved-imports.md#works-at-runtime-but-pylance-shows-errors).

---

## Troubleshooting

### Editable Install Not Recognized

**Symptom**: Package is installed as editable (`pip install -e`) but Pylance shows "could not be resolved."

**Steps**:

1. **Check for path-based `.pth` file** (see [Verifying Your Editable Install](#verifying-your-editable-install) above). If the content starts with `import`, the build backend is using import hooks. Either:
    - Reinstall with compat mode: `pip install -e . --config-settings editable_mode=compat`
    - On **Python 3.13+**, enable `"python.analysis.enableEditableInstalls": true`
    - Add the source to [`extraPaths`](../settings/python_analysis_extraPaths.md) as a fallback

2. **Reload Pylance**: After reinstalling or changing settings, run **"Python: Restart Language Server"** from the Command Palette.

3. **Check Python version in `.pth` filename**: The `.pth` file must be in the `site-packages` of the Python interpreter Pylance is using. If you have multiple interpreters, ensure the correct one is selected.

### Wrong Interpreter Selected

The `.pth` files are in a specific interpreter's `site-packages`. If Pylance uses a different interpreter, it won't see them.

1. Click the Python version in the VS Code status bar
2. Select the interpreter whose `site-packages` contains your `.pth` files
3. Confirm with: `python -c "import sys; print(sys.prefix)"`

### Setuptools Version Gotcha

Setuptools v64+ changed the default editable mode from path-based to strict (import-hook). If you recently upgraded setuptools and editable installs stopped working:

```bash
pip install -e . --config-settings editable_mode=compat
```

Or pin setuptools behavior in `pyproject.toml`:

```toml
[tool.setuptools]
# Forces compat mode for editable installs
```

---

## FAQ

### Q: How do I set up a uv workspace with editable installs?

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

### Q: How do I set up a Poetry monorepo with editable installs?

[Poetry](https://python-poetry.org/) supports path dependencies between packages:

1. Declare path dependencies in each package's `pyproject.toml`:

    ```toml
    # packages/api/pyproject.toml
    [tool.poetry.dependencies]
    core = { path = "../core", develop = true }
    ```

2. Run `poetry install` in each package.

3. Verify `.pth` files are created:

    ```bash
    find .venv/lib -name "*.pth" | xargs cat
    ```

4. Select the Poetry-managed venv as the Python interpreter in VS Code.

Poetry uses path-based `.pth` files for editable installs, which Pylance reads natively. No additional `extraPaths` or config changes are needed.

### Q: My build backend doesn't support compat mode. What are my options?

If your build backend only produces import-hook `.pth` files (e.g., Hatchling, Maturin, Meson-python):

1. **Python 3.13+**: Enable `"python.analysis.enableEditableInstalls": true`
2. **Older Python**: Add the source directory to [`extraPaths`](../settings/python_analysis_extraPaths.md):

    ```json
    {
        "python.analysis.extraPaths": ["./packages/mypackage/src"]
    }
    ```

3. **Alternative**: Use a regular `pip install` (non-editable) and accept that source changes require a reinstall

### Q: How do I set up a conda environment with editable installs?

[Conda](https://docs.conda.io/) does not natively support editable installs. Use pip inside conda:

1. Create and activate the conda environment:

    ```bash
    conda create -n myproject python=3.12
    conda activate myproject
    ```

2. Install local packages as editable using pip:

    ```bash
    pip install -e ./packages/core --config-settings editable_mode=compat
    pip install -e ./packages/api --config-settings editable_mode=compat
    ```

3. Select the conda interpreter in VS Code (e.g., `~/anaconda3/envs/myproject/bin/python`).

**Common pitfall**: If you install with `conda install` instead of `pip install -e`, Pylance will find the packages in `site-packages` (stubs or compiled) but may not have source code for Go to Definition.

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution and runtime vs. static analysis gaps
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) — trace logging and search order
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — monorepo-specific editable install patterns

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

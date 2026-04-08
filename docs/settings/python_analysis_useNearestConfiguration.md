# Understanding `python.analysis.useNearestConfiguration` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

Many codebases contain multiple Python sub-projects — each with different type-checking needs, Python version targets, or strictness levels. Pylance offers the `python.analysis.useNearestConfiguration` setting to automatically discover `pyrightconfig.json` and `pyproject.toml` files throughout your workspace and apply the right settings to the right files — without requiring a multi-root workspace.

This guide explains what `python.analysis.useNearestConfiguration` does, how it discovers configuration files, and how virtual workspaces work.

## What Is `python.analysis.useNearestConfiguration`?

The `python.analysis.useNearestConfiguration` setting controls whether Pylance scans your workspace for `pyrightconfig.json` and `pyproject.toml` files in subdirectories and creates **virtual workspaces** for each one. Each virtual workspace uses its own configuration, so different parts of your codebase can have independent type-checking settings.

This is an **experimental** feature and is disabled by default.

## How Does It Work?

When `python.analysis.useNearestConfiguration` is set to `true`:

1. **Discovery**: Pylance recursively scans your workspace from the root, looking for `pyrightconfig.json` and qualifying `pyproject.toml` files in subdirectories.
2. **Virtual workspace creation**: For each discovered config file, Pylance creates an internal virtual workspace rooted at that config file's parent directory.
3. **Isolation**: Each Python file is type-checked using the configuration from its enclosing virtual workspace — the nearest ancestor directory that has a config file.
4. **Dynamic updates**: File watchers detect config files being added, removed, or changed, and recompute virtual workspaces automatically.

### What Gets Discovered

- **`pyrightconfig.json`**: Any valid JSON file with this name in a subdirectory.
- **`pyproject.toml`**: Only included if it contains a `[tool.pyright]` or `[tool.pyrightconfig]` section.

### What Gets Skipped

These directories are automatically skipped during discovery:

- Any directory starting with `.` (covers `.git`, `.vscode`, `.venv`, `.env`, `.tox`, `.nox`, `.mypy_cache`, `.pytest_cache`, `.eggs`, etc.)
- `node_modules`, `__pycache__`
- `venv`, `env`, `site-packages`
- `dist`, `build`, `*.egg-info`

### Example

```
workspace/
├── pyproject.toml          # Python 3.11, strict checking
├── src/
│   └── main.py
├── scripts/
│   ├── pyrightconfig.json  # Python 3.12, relaxed checking
│   └── helper.py
└── examples/
    ├── pyrightconfig.json  # Python 3.12, medium checking
    └── demo.py
```

With `"python.analysis.useNearestConfiguration": true`:

- `src/main.py` uses the root `pyproject.toml` (Python 3.11, strict)
- `scripts/helper.py` uses `scripts/pyrightconfig.json` (Python 3.12, relaxed)
- `examples/demo.py` uses `examples/pyrightconfig.json` (Python 3.12, medium)

## The `python.analysis.useNearestConfiguration` Setting

### Accepted Values

- `true`: Enables automatic discovery of config files and creation of virtual workspaces.
- `false` (default): Pylance only uses config files at workspace roots.

### Default Value

The default value is `false`.

## How to Change the Setting

To enable `python.analysis.useNearestConfiguration`:

- Open **Settings** and search for `python.analysis.useNearestConfiguration`.
- Check the box to enable it.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type **Preferences: Open Settings (JSON)**, and select it.
- Add or update the following line:
    ```json
    "python.analysis.useNearestConfiguration": true
    ```

## Virtual Workspace Behavior

### Transparency

Virtual workspaces are transparent — they do not appear in the VS Code Explorer or change the UI in any way. The setting scope is `resource`, so it can be configured per workspace folder.

### Isolation Between Virtual Workspaces

Virtual workspaces are **isolated** by default. Files in one virtual workspace cannot import from another virtual workspace unless `extraPaths` is explicitly configured in the config file.

To allow cross-workspace imports, add [`extraPaths`](https://microsoft.github.io/pyright/#/configuration?id=main-configuration-options) in the relevant `pyrightconfig.json`:

```json
{
    "extraPaths": ["../shared"]
}
```

### Excluding Virtual Workspaces

Use [`python.analysis.exclude`](python_analysis_exclude.md) to prevent virtual workspaces from being created for certain subdirectories:

```json
{
    "python.analysis.useNearestConfiguration": true,
    "python.analysis.exclude": ["**/tests/**", "**/temp/**"]
}
```

Changes to `python.analysis.exclude` trigger an automatic recomputation of virtual workspaces.

## Comparison with Multi-Root Workspaces

| Feature                    | Multi-Root Workspaces            | `useNearestConfiguration` |
| -------------------------- | -------------------------------- | ------------------------- |
| Manual setup required      | Yes — `.code-workspace` file     | No — automatic discovery  |
| UI changes                 | Yes — multiple roots in Explorer | No — single root          |
| Works with `code .`        | No — needs a workspace file      | Yes                       |
| Config in any subdirectory | No — only explicit roots         | Yes                       |
| User awareness             | Explicit                         | Transparent               |

## Limitations

- **Experimental**: This feature is experimental and may change in future releases.
- **Extension-side only**: The config discovery and virtual workspace creation happen on the VS Code extension side. The language server receives virtual workspaces as standard workspace folders.
- **Light mode interaction**: When [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md) is set to `light`, the default [`python.analysis.exclude`](python_analysis_exclude.md) pattern is `["**"]`, which excludes all subdirectories — effectively making `useNearestConfiguration` have no effect.
- **Only `pyrightconfig.json` and qualifying `pyproject.toml`**: Other config formats are not discovered.

## Frequently Asked Questions

### Q: Do I still need a multi-root workspace if I enable this?

**A:** In most cases, no. `useNearestConfiguration` automatically discovers config files and creates virtual workspaces. Multi-root workspaces are still useful when your sub-projects are in unrelated directories or when you want explicit control over which folders are included.

### Q: Why aren't my `pyproject.toml` files being picked up?

**A:** Pylance only recognizes `pyproject.toml` files that contain a `[tool.pyright]` or `[tool.pyrightconfig]` section. Add one of these sections to your `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "standard"
```

### Q: Can files in one virtual workspace import from another?

**A:** Not by default. Virtual workspaces are isolated. Add [`extraPaths`](https://microsoft.github.io/pyright/#/configuration?id=main-configuration-options) in the relevant `pyrightconfig.json` to enable cross-workspace imports.

### Q: Why does this have no effect in light mode?

**A:** In light mode, [`python.analysis.exclude`](python_analysis_exclude.md) defaults to `["**"]`, which excludes all virtual workspace subdirectories. Switch to `default` or `full` language server mode to use `useNearestConfiguration`.

## Related Settings

- [`python.analysis.exclude`](python_analysis_exclude.md): Exclude patterns that filter out virtual workspaces.
- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md): Controls language server mode; `light` mode effectively disables `useNearestConfiguration`.

## See Also

- [How to Set Up CI Type Checking](../howto/ci-type-checking.md) — per-subtree config for CI pipelines
- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — multi-config monorepo patterns

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

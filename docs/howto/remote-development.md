# How to Use Pylance in Remote Development Environments

Pylance runs as a language server on the same machine as the code. In remote scenarios — Dev Containers, WSL, Remote SSH, and GitHub Codespaces — Pylance runs on the remote side. This guide covers the configuration patterns that keep Pylance working correctly across environments.

---

## Table of Contents

- [General Principles](#general-principles)
- [Dev Containers](#dev-containers)
- [WSL](#wsl)
- [Remote SSH](#remote-ssh)
- [GitHub Codespaces](#github-codespaces)
- [Portable Configuration Tips](#portable-configuration-tips)
- [FAQ](#faq)

---

## General Principles

These rules apply to all remote development scenarios:

1. **Use relative paths in [`extraPaths`](../settings/python_analysis_extraPaths.md)**: Absolute paths break across environments.

    ```json
    // ✅ Portable — works in any container, WSL, or remote host
    { "python.analysis.extraPaths": ["./packages/shared/src"] }

    // ❌ Breaks in containers — host path doesn't exist inside the container
    { "python.analysis.extraPaths": ["/home/user/monorepo/packages/shared/src"] }
    ```

2. **Commit settings files**: Check `.vscode/settings.json` or `.code-workspace` files into the repo so every environment gets the same Pylance configuration.

3. **Use editable installs** (`pip install -e`) as the most portable approach — they rely on the interpreter's `site-packages` path, which works identically in any environment. See [How to Use Editable Installs with Pylance](editable-installs.md).

4. **Config file paths are already portable**: If using [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration), paths are relative to the config file location, so they work naturally across environments.

---

## Dev Containers

When working in [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), configure Pylance settings in the `customizations.vscode.settings` block of `devcontainer.json` so they apply automatically inside the container:

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

**Tips**:

- Use `postCreateCommand` to install dependencies so they're available when Pylance starts
- If using editable installs with setuptools, add `--config-settings editable_mode=compat` to ensure Pylance can follow them

---

## WSL

When opening a repo in [WSL](https://code.visualstudio.com/docs/remote/wsl), VS Code runs Pylance on the Linux side.

**Key considerations**:

- Ensure the Python interpreter path in the status bar points to a **Linux path** (e.g., `/home/user/.venv/bin/python`), not a Windows path. Windows Python interpreters are not usable from WSL.
- All paths in `settings.json` should use Linux-style forward slashes
- Packages installed in the WSL environment are separate from any Windows Python installation

---

## Remote SSH

When using [Remote SSH](https://code.visualstudio.com/docs/remote/ssh), Pylance runs entirely on the remote machine.

**Key considerations**:

- Ensure Node.js and Python are available on the remote host
- If you use [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md), the path must be valid on the remote host. Setting it to `"auto"` is the safest approach for mixed local/remote workflows.
- `nodeExecutable` has `"scope": "machine"`, so a global (User Settings) value set for your local machine will also be sent to the remote — override it in the remote machine's settings if needed.
- Use per-project `.vscode/settings.json` files (committed to the repo) so settings apply correctly on the remote host

---

## GitHub Codespaces

[GitHub Codespaces](https://github.com/features/codespaces) works like Dev Containers. Add Pylance settings to `devcontainer.json` and they apply automatically when the Codespace is created.

The same `devcontainer.json` configuration shown in [Dev Containers](#dev-containers) applies directly to Codespaces.

---

## Portable Configuration Tips

### Use `pyrightconfig.json` for Path-Heavy Projects

If your project has many path dependencies, prefer [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) over VS Code settings. Config file paths are relative to the file location and don't need variable substitution — they work everywhere.

```json
// pyrightconfig.json (at project root)
{
    "extraPaths": ["packages/core/src", "packages/api/src"],
    "typeCheckingMode": "basic"
}
```

### Avoid Machine-Scoped Settings in Shared Configs

Some settings like [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md) have `"scope": "machine"`. These follow the machine, not the workspace. Keep them in per-machine settings (User Settings) or use `"auto"` values that adapt to the environment.

### Editable Installs Are the Most Portable Pattern

Editable installs (`pip install -e`) create `.pth` files in the interpreter's `site-packages`. Since the interpreter path is already environment-specific (each container/WSL/remote host has its own), editable installs "just work" across environments without any extra Pylance configuration.

---

## FAQ

### Q: My Pylance settings don't apply inside a container. Why?

Check whether settings are in the right place:

- **User Settings** (on your host): These are sent to the container, but may be overridden by workspace settings
- **Workspace settings** (`.vscode/settings.json`): Apply inside the container if the repo is mounted
- **`devcontainer.json` settings**: Apply via `customizations.vscode.settings` — this is the most reliable place for container-specific settings

### Q: Can I use different Pylance settings for local vs. remote development?

Yes. Use per-machine User Settings for machine-specific values (like `nodeExecutable`), and commit `.vscode/settings.json` with portable settings (like `extraPaths` with relative paths). Machine settings override workspace settings for machine-scoped properties.

---

## Related Guides

- [How to Use Editable Installs with Pylance](editable-installs.md) — portable editable install patterns
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — configuration precedence and conflicts
- [How to Tune Pylance Performance](performance-tuning.md) — `nodeExecutable` and heap settings for remote hosts

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

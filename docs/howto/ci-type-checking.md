# How to Run Pyright Type Checking in CI/CD

[Pyright](https://github.com/microsoft/pyright) can run as a standalone CLI in CI to validate the same type checking that Pylance performs in the editor. This guide covers how to set up Pyright in CI pipelines, common configurations, and differences from the editor experience.

---

## Table of Contents

- [Basic Setup](#basic-setup)
- [Multi-Package Projects](#multi-package-projects)
- [Differences from Pylance in the Editor](#differences-from-pylance-in-the-editor)
- [Tips](#tips)
- [Pre-commit Hook](#pre-commit-hook)
- [FAQ](#faq)

---

## Basic Setup

### Single-Root Project with `pyrightconfig.json`

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

Pyright reads [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) (or `[tool.pyright]` in `pyproject.toml`) from the repo root and applies the same `extraPaths`, `executionEnvironments`, and diagnostic settings.

### Without a Config File

If you use VS Code `settings.json` for Pylance configuration but don't have a `pyrightconfig.json`, create one for CI:

```json
// pyrightconfig.json
{
    "extraPaths": ["packages/core/src", "packages/api/src"],
    "typeCheckingMode": "basic"
}
```

Pyright CLI does **not** read VS Code `settings.json`. Any paths or settings configured only in VS Code must be replicated in a config file for CI.

---

## Multi-Package Projects

For projects where each package has its own config file, use a matrix strategy:

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

The `--project` flag tells Pyright to use the `pyrightconfig.json` in the specified directory.

---

## Differences from Pylance in the Editor

| Feature                                                                             | Pylance (VS Code)               | Pyright CLI                                                |
| ----------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------- |
| Reads VS Code `settings.json`                                                       | Yes                             | No — use `pyrightconfig.json` or `[tool.pyright]`          |
| [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) | Supported                       | **Not supported** — this is a Pylance-only VS Code setting |
| Language server mode (`light`/`default`/`full`)                                     | Supported                       | Not applicable — CLI always analyzes all specified files   |
| Bundled type stubs for popular packages                                             | Yes (Pylance ships extra stubs) | No — use `pip install types-*` or typeshed                 |
| Auto-import, completions, hover                                                     | Yes                             | Not applicable (CLI only reports diagnostics)              |

### Handling `useNearestConfiguration` in CI

If your editor uses [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) to auto-discover per-directory configs, you need a different approach in CI:

- **Option A**: Use a root `pyrightconfig.json` with [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options)
- **Option B**: Run `npx pyright --project <path>` separately per package

---

## Different Severity in CI vs Editor

A common requirement is strict errors in CI but softer warnings in the editor. Since `pyrightconfig.json` overrides VS Code settings when present, use this approach:

**Option A: CI-only config file**

Keep no `pyrightconfig.json` in the workspace (so VS Code settings apply for editing). Create a CI-specific config:

```json
// pyrightconfig.ci.json
{
    "typeCheckingMode": "standard",
    "reportUnusedImport": "error",
    "reportReturnType": "error"
}
```

In CI, run:

```bash
npx pyright --project pyrightconfig.ci.json
```

In VS Code, use `settings.json` with softer settings:

```json
{
    "python.analysis.typeCheckingMode": "standard",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedImport": "information"
    }
}
```

**Option B: Shared config + VS Code per-file overrides**

Use `pyrightconfig.json` for CI (strict). Developers add `# pyright: reportUnusedImport=information` in files they're actively editing.

---

## Tips

- **Pin the Pyright version**: `npx pyright@1.1.390` to avoid surprise breakage from upstream updates
- **Use the same `typeCheckingMode`** in CI as in your editor config for consistent behavior
- **Install dependencies first**: Pyright needs to see installed packages in `site-packages` to resolve third-party imports. Run `pip install -e .` or `pip install -r requirements.txt` before `npx pyright`
- **Editable installs**: Use `--config-settings editable_mode=compat` if using setuptools, so Pyright can follow `.pth` files. See [How to Use Editable Installs with Pylance](editable-installs.md)
- **`extraPaths` in VS Code only?** If your editor uses `extraPaths` in VS Code settings (not in a config file), replicate them in a `pyrightconfig.json` for CI, since Pyright CLI doesn't read VS Code settings

---

## Pre-commit Hook

You can run Pyright as a [pre-commit](https://pre-commit.com/) hook using the official mirror:

```yaml
# .pre-commit-config.yaml
repos:
    - repo: https://github.com/RobertCraigie/pyright-python
      rev: v1.1.400 # pin to a recent version
      hooks:
          - id: pyright
```

Alternatively, use the simpler local hook approach:

```yaml
repos:
    - repo: local
      hooks:
          - id: pyright
            name: pyright
            entry: npx pyright
            language: node
            types: [python]
            pass_filenames: false
```

**Tips for pre-commit**:

- Set `pass_filenames: false` — Pyright analyzes the whole project, not individual files
- Pin the version to avoid surprise breakage
- Ensure your virtual environment is active so Pyright can find installed packages

---

## FAQ

### Q: Do I need Pyright in CI if I already use Pylance in VS Code?

Pyright in CI ensures type checking runs on every pull request, catching errors that individual developers might miss if they haven't opened a particular file. It's especially valuable for multi-developer projects where not everyone uses VS Code or Pylance.

### Q: Can I use Pylance instead of Pyright in CI?

No. Pylance is a VS Code extension and cannot run as a standalone CLI. The Pyright CLI performs the same core type checking. Some Pylance-specific behaviors (bundled stubs, `useNearestConfiguration`) are not available in the CLI.

### Q: How do I get the same diagnostic results in CI as in the editor?

1. Use a `pyrightconfig.json` that matches your VS Code settings
2. Install the same packages in CI as in your local environment
3. Pin the Pyright version to match the Pylance version you use (Pylance bundles a specific Pyright version)
4. Use the same `typeCheckingMode` setting

---

## Related Guides

- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — `pyrightconfig.json` vs. VS Code settings precedence
- [How to Use Editable Installs with Pylance](editable-installs.md) — ensuring CI can resolve editable packages
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — multi-package CI strategies

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

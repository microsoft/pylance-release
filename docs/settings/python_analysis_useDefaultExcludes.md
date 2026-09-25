# Understanding `python.analysis.useDefaultExcludes` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.useDefaultExcludes` setting controls whether Pylance applies its built-in default exclusions in addition to the paths you list in [`python.analysis.exclude`](python_analysis_exclude.md).

## What Is `python.analysis.useDefaultExcludes`?

To keep analysis fast, Pylance excludes a set of directories that rarely need to be analyzed. When this setting is enabled (the default), those built-in exclusions are applied **in addition to** any paths you specify in [`python.analysis.exclude`](python_analysis_exclude.md).

The built-in default exclusions are:

- `**/node_modules`
- `**/__pycache__`
- `**/__editable__.*`
- Hidden directories (dotfiles), i.e. any directory whose name begins with a `.` (for example `.git`, `.venv`, `.tox`)
- Auto-detected virtual environment directories (e.g., those containing `bin/activate`, `Scripts/activate`, or `pyvenv.cfg`)

These defaults take precedence over [`python.analysis.include`](python_analysis_include.md), so a directory that Pylance auto-detects as a virtual environment stays excluded even if you name it explicitly in `include`.

**Type**: `boolean`
**Default**: `true`
**Scope**: resource (can be set per workspace folder)

## Behavior

### When enabled (`true`, the default)

The built-in default exclusions listed above are applied on top of your `python.analysis.exclude` entries. Your custom excludes are **additive** — they add to the defaults rather than replacing them — so you never need to re-list the defaults to keep them excluded.

### When disabled (`false`)

All of the built-in default exclusions are turned off, **including virtual-environment auto-detection**. Only the paths you list in [`python.analysis.exclude`](python_analysis_exclude.md) are excluded.

> **Note**: Disabling the built-in excludes can slow analysis significantly if your workspace contains large dependency or virtual-environment directories, because Pylance will then analyze them unless you exclude them yourself.

## How to Change `python.analysis.useDefaultExcludes`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.useDefaultExcludes`.
3. Check or uncheck the box.

### Using `settings.json`

```json
{
    "python.analysis.useDefaultExcludes": false
}
```

## When to Use It

- **Keep enabled** (the default) for almost all projects. The built-in excludes keep analysis fast and rarely need to change, and your own `python.analysis.exclude` entries are added on top of them.
- **Disable** when a default exclusion is skipping a directory you need analyzed — most commonly a directory that was incorrectly auto-detected as a virtual environment. Because the defaults take precedence over `include`, turning this setting off is the way to force analysis of such a directory; adding it to `include` will not.

When you disable the defaults, you'll typically want to re-add the exclusions you still care about (such as `**/node_modules` and your real virtual environment) to `python.analysis.exclude` yourself:

```json
{
    "python.analysis.useDefaultExcludes": false,
    "python.analysis.exclude": ["**/node_modules", "**/__pycache__", "venv/**"]
}
```

## Related Settings

- [`python.analysis.exclude`](python_analysis_exclude.md): Paths to exclude from analysis; combined with the built-in defaults this setting controls.
- [`python.analysis.include`](python_analysis_include.md): Paths to include in analysis. The built-in default exclusions take precedence over `include`.
- [`python.analysis.ignore`](python_analysis_ignore.md): Suppresses diagnostics for specific paths without excluding them.

## See Also

- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — per-subfolder exclusion patterns
- [How to Tune Pylance Performance](../howto/performance-tuning.md) — using excludes to reduce analysis scope

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

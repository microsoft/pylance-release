# Understanding `python.analysis.showOnlyDirectDependenciesInAutoImport` in Pylance

## What It Does

When enabled, Pylance filters auto-import completion suggestions to show only packages declared as direct dependencies in your project's `requirements.txt` or `pyproject.toml`. This reduces noise from transitive dependencies and keeps completion lists focused on packages you actually use.

This setting affects **auto-import completions only** — the symbols that appear in the completion list with an import icon. The **"Add import" code action** (light bulb / Ctrl+.) continues to show all possible imports regardless of this setting.

## Accepted Values

| Value             | Behavior                                                                             |
| ----------------- | ------------------------------------------------------------------------------------ |
| `false` (default) | Auto-import completions suggest symbols from all installed packages                  |
| `true`            | Auto-import completions suggest symbols only from direct dependencies and user files |

## How Direct Dependencies Are Detected

Pylance reads the following files in your workspace root:

- **`requirements.txt`** — including recursive `-r` includes
- **`pyproject.toml`** — both `[project.dependencies]` and `[tool.poetry.dependencies]` sections

Distribution names are automatically mapped to top-level module names (e.g., `scikit-learn` → `sklearn`, `Pillow` → `PIL`).

If neither file exists, the setting has no effect — all packages are shown as if the setting were `false`.

## Language Server Mode Defaults

| Mode      | Default value |
| --------- | ------------- |
| `default` | `false`       |
| `light`   | `false`       |
| `full`    | `true`        |

In `full` mode, this setting is enabled by default to improve the relevance of auto-import suggestions alongside the broader indexing depth.

## Example

```json
{
    "python.analysis.showOnlyDirectDependenciesInAutoImport": true
}
```

With this enabled and a `requirements.txt` containing:

```
flask
requests
```

Auto-import completions will suggest symbols from `flask`, `requests`, the standard library, and your own workspace files — but not from transitive dependencies like `werkzeug`, `urllib3`, or `certifi`.

## When to Enable

- Your project has many installed packages but you only import from a small set of direct dependencies.
- The completion list is cluttered with suggestions from packages you don't directly use.
- You are in `default` or `light` mode and want the focused suggestion behavior that `full` mode provides by default.

## When to Disable

- Your project intentionally imports from transitive dependencies (e.g., `werkzeug` utilities in a Flask project).
- You don't maintain a `requirements.txt` or `pyproject.toml` and want all installed packages available.

## Related Settings

- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md) — enable or disable auto-import completions entirely
- [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md) — control how deeply packages are indexed for auto-imports
- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md) — preset modes that adjust this and other settings

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

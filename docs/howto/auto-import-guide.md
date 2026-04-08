# How to Configure Auto-Imports in Pylance

Pylance can automatically suggest and add import statements when you use a symbol that isn't imported yet. This guide explains the settings that control auto-import behavior, how to tune them for your project, and how to troubleshoot common issues.

---

## Table of Contents

- [How Auto-Imports Work](#how-auto-imports-work)
- [Enable or Disable Auto-Import Completions](#enable-or-disable-auto-import-completions)
- [Control Import Style](#control-import-style)
- [Control Which Symbols Appear](#control-which-symbols-appear)
- [Improve Auto-Import Coverage with Indexing](#improve-auto-import-coverage-with-indexing)
- [Too Many Suggestions](#too-many-suggestions)
- [Missing Suggestions](#missing-suggestions)
- [Organize Imports on Save](#organize-imports-on-save)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## How Auto-Imports Work

When you type a symbol name, Pylance searches:

1. **Open files** and the **current project** for matching symbols.
2. **Indexed packages** (if [indexing](../settings/python_analysis_indexing.md) is enabled) for library symbols.
3. **Standard library** stubs for built-in module symbols.

Matches appear in the completion list with an import icon. Accepting one inserts the import statement at the top of the file.

Auto-imports also work through **quick fixes**: if you write code with an unresolved name, Pylance offers an "Add import" code action (light bulb).

---

## Enable or Disable Auto-Import Completions

[`python.analysis.autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md) controls whether auto-import suggestions appear in the completion list.

```json
{
    "python.analysis.autoImportCompletions": true
}
```

| Value                                  | Behavior                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| `true`                                 | Auto-import suggestions appear in completions                                               |
| `false` (default for `"default"` mode) | Auto-import suggestions are hidden from completions, but quick-fix "Add import" still works |

Even with `autoImportCompletions` disabled, you can still trigger auto-imports via the code action (light bulb / Ctrl+.).

---

## Control Import Style

[`python.analysis.importFormat`](../settings/python_analysis_importFormat.md) controls whether auto-imports use absolute or relative style:

```json
{
    "python.analysis.importFormat": "absolute"
}
```

| Value                  | Result                               |
| ---------------------- | ------------------------------------ |
| `"absolute"` (default) | `from mypackage.utils import helper` |
| `"relative"`           | `from .utils import helper`          |

Relative imports are only used when the file and the target symbol are in the same package.

---

## Control Which Symbols Appear

### Include Re-exports from User Files

[`python.analysis.includeAliasesFromUserFiles`](../settings/python_analysis_includeAliasesFromUserFiles.md) controls whether re-exported symbols from your own code appear in auto-imports:

```json
{
    "python.analysis.includeAliasesFromUserFiles": true
}
```

When `true`, if `mypackage/__init__.py` imports `helper` from `mypackage._internal`, Pylance will suggest `from mypackage import helper` in completions.

### Control Package Indexing Depth

[`python.analysis.packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md) lets you control how deeply Pylance indexes specific packages:

```json
{
    "python.analysis.packageIndexDepths": [
        { "name": "numpy", "depth": 2 },
        { "name": "pandas", "depth": 2 },
        { "name": "sklearn", "depth": 3, "includeAllSymbols": true }
    ]
}
```

| Property            | Meaning                                                            |
| ------------------- | ------------------------------------------------------------------ |
| `depth`             | How many subpackage levels to index (default: 2 for most packages) |
| `includeAllSymbols` | Include non-`__all__` symbols (default: false)                     |

Increase `depth` for packages where auto-imports miss deeply nested symbols.

---

## Improve Auto-Import Coverage with Indexing

[`python.analysis.indexing`](../settings/python_analysis_indexing.md) enables background indexing, which pre-scans installed packages for symbols:

```json
{
    "python.analysis.indexing": true
}
```

Without indexing, Pylance only knows about symbols from files it has already opened or analyzed. With indexing, it proactively discovers symbols across your installed packages.

| Scenario                                                                            | Indexing recommended?                                     |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Large project with many dependencies                                                | Yes — significantly improves auto-import quality          |
| Small script, few dependencies                                                      | Optional — auto-imports work reasonably without it        |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md) `"light"` | Indexing defaults to `false`; enable explicitly if needed |

### Related indexing settings

- [`persistAllIndices`](../settings/python_analysis_persistAllIndices.md) — cache indices to disk for faster startup
- [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md) — limit the number of user files indexed
- [`regenerateStdLibIndices`](../settings/python_analysis_regenerateStdLibIndices.md) — force re-index of standard library

---

## Too Many Suggestions

**Symptom**: Completion list is cluttered with symbols from packages you don't use.

### Fixes

1. **Reduce `packageIndexDepths`** for noisy packages:

    ```json
    {
        "python.analysis.packageIndexDepths": [{ "name": "noisy_package", "depth": 1 }]
    }
    ```

2. **Disable auto-import completions** and rely on quick fixes instead:

    ```json
    {
        "python.analysis.autoImportCompletions": false
    }
    ```

3. **Exclude directories** you don't want indexed:

    ```json
    {
        "python.analysis.exclude": ["vendor/**", "third_party/**"]
    }
    ```

---

## Missing Suggestions

**Symptom**: Typing a known symbol doesn't show an auto-import suggestion.

### Common Causes and Fixes

| Cause                                                                                  | Fix                                                                                                                         |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Indexing disabled                                                                      | Set [`indexing`](../settings/python_analysis_indexing.md) to `true`                                                         |
| `autoImportCompletions` is `false`                                                     | Set [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md) to `true`                               |
| Package not installed in selected environment                                          | Install the package in the active interpreter's environment                                                                 |
| Symbol is deeply nested                                                                | Increase `depth` in [`packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md)                               |
| Symbol is not in `__all__`                                                             | Set `includeAllSymbols: true` in [`packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md) for that package |
| Private symbol (underscore prefix)                                                     | Pylance hides private symbols by default. Import manually                                                                   |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md) is `"light"` | Switch to `"default"` or `"full"` for better indexing                                                                       |
| Symbol only available through a re-export                                              | Enable [`includeAliasesFromUserFiles`](../settings/python_analysis_includeAliasesFromUserFiles.md)                          |

---

## Organize Imports on Save

VS Code can automatically sort and remove unused imports when you save. This works alongside auto-imports.

Add to `.vscode/settings.json`:

```json
{
    "editor.codeActionsOnSave": {
        "source.organizeImports.pylance": "explicit"
    }
}
```

This runs Pylance's import organizer on save. It:

- Sorts imports alphabetically
- Groups imports by standard lib → third-party → local
- Removes unused imports

See [`python.analysis.fixAll`](../settings/python_analysis_fixAll.md) for other code actions available on save.

> **Note**: Pylance's organizer handles sorting and removing unused imports. For more advanced import formatting (custom grouping rules, blank lines between groups, line length), consider using [isort](https://pycqa.github.io/isort/) or [Ruff](https://docs.astral.sh/ruff/formatter/) as a complementary tool.

Example `settings.json` for using Ruff as the import organizer instead of Pylance:

```json
{
    "editor.codeActionsOnSave": {
        "source.organizeImports.ruff": "explicit"
    },
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

With isort, configure it in `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
known_first_party = ["mypackage"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

---

## Diagnostic Checklist

When auto-imports aren't working as expected:

- [ ] **Indexing enabled**: [`python.analysis.indexing`](../settings/python_analysis_indexing.md) is `true`
- [ ] **Auto-import completions enabled**: [`python.analysis.autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md) is `true`
- [ ] **Correct interpreter**: Package is installed in the selected Python environment
- [ ] **Indexing complete**: Check **Output → Pylance** — auto-imports improve after indexing finishes
- [ ] **Language server mode**: Not set to `"light"` (limits indexing)
- [ ] **Config file**: No `pyrightconfig.json` overriding VS Code settings unexpectedly. See [Settings Troubleshooting](settings-troubleshooting.md)

---

## FAQ

### Q: Why does auto-import suggest a long path instead of the short one?

Pylance suggests the path where the symbol is defined, not necessarily the re-export path. To prefer shorter paths:

- Enable [`includeAliasesFromUserFiles`](../settings/python_analysis_includeAliasesFromUserFiles.md) — this makes re-exported symbols available through the shorter path.
- Libraries that define `__all__` in their `__init__.py` usually provide the short path by default.

### Q: Can I auto-import from packages in `extraPaths`?

Yes. Packages found through [`extraPaths`](../settings/python_analysis_extraPaths.md) are treated like installed packages for auto-import purposes.

### Q: Does auto-import work with `pyrightconfig.json`?

Auto-import settings like `autoImportCompletions` are **not** overridden by `pyrightconfig.json`. They remain controlled by VS Code settings. However, path settings (`extraPaths`, `include`, `exclude`) in the config file do affect which symbols are available.

### Q: How do I make auto-import prefer `from X import Y` style?

This is the default behavior. Pylance generates `from module import name` style imports. There is currently no setting to switch to `import module` style for auto-imports.

---

## Related Guides

- [How to Fix Unresolved Import Errors](unresolved-imports.md) — when imports don't resolve at all
- [How to Tune Pylance Performance](performance-tuning.md) — indexing and memory management
- [Settings Troubleshooting](settings-troubleshooting.md) — config file precedence

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

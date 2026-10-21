# How to Configure Auto-Imports in Pylance

Pylance can automatically suggest and add import statements when you use a symbol that isn't imported yet. This guide explains the settings that control auto-import behavior, how to tune them for your project, and how to troubleshoot common issues.

---

## Table of Contents

- [How Auto-Imports Work](#how-auto-imports-work)
- [Suggestion ordering and history](#suggestion-ordering-and-history)
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

### Paste code with its imports

Copy code from one Python file in VS Code, then use **Paste As** in another Python file and choose **Paste with Imports**. Review the imports Pylance adds to the destination file.

---

## Suggestion ordering and history

"Add import" quick fixes, auto-import completions, and the import search picker share the ranking below:

1. **Recent choices**, with the most recently accepted symbol and source first.
2. **The same symbol from the same source** already imported in open project files.
3. **Other candidates matching imports** in open project files.
4. **Symbols defined in your project**.
5. **Symbols from `typing`**.
6. **Standard library symbols**.
7. **Third-party library symbols**.
8. **Library symbols re-exported by your project**.

Open-file preferences use a bounded scan of top-level imports in open project files, not workspace-wide usage or frequency analysis. Local aliases can affect name matching. Within a priority, symbol names and module paths affect ordering.

Without recent choices or open-file preferences, `typing.Literal` ranks before third-party `schema.Literal`, and `pathlib.Path` ranks before third-party `Path` alternatives. A same-name symbol defined in your project ranks above those library candidates. Explicitly choosing `schema.Literal` can move it ahead of `typing.Literal` next time, even ahead of open-file preferences. Check the source before accepting: identically named symbols can have different purposes.

The interfaces can still show different lists because their ranking, filtering, and presentation differ. Your environment, indexing, and [which symbols are included](#control-which-symbols-appear) determine the available candidates; ranking does not add missing candidates. Import suggestions keep their category placement within completions, and quick fixes show at most three import candidates after ranking.

**History tracks recency, not frequency.** Completions, quick fixes, and picker selections share up to 100 distinct symbol-and-source choices. Choosing the same pair again moves it to the front; the oldest distinct choices are evicted when the limit is reached. Local aliases do not create separate history entries. A choice is recorded when the import is accepted.

Import history is kept separately for each workspace folder.

Recent choices can affect subsequent ordering across all three interfaces. Restarting the language server or VS Code does not clear saved import history.

Suggestion ordering helps you choose **which symbol and source to import**. It is separate from [organizing imports](#organize-imports-on-save), which rearranges import statements already in your file.

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
| `depth`             | How many subpackage levels to index (default: 1 for most packages) |
| `includeAllSymbols` | Include non-`__all__` symbols (default: false)                     |

Increase `depth` for packages where auto-imports miss deeply nested symbols.

#### How default depths vary by language server mode

In `default` mode, most packages are indexed at depth **1** (top-level only). A few popular libraries (`sklearn`, `matplotlib`, `scipy`, `flask`, `fastapi`) default to depth **2**, `django` defaults to depth **4**, and `cuda` defaults to depth **3** with `includeAllSymbols: true`.

In `full` mode, **most** packages default to depth **4** with `includeAllSymbols: true`, providing much broader auto-import coverage at the cost of higher resource usage.

In `light` mode, indexing is disabled by default. Enable [`python.analysis.indexing`](../settings/python_analysis_indexing.md) explicitly to use package indexing in light mode.

#### Automatic depth boost for direct dependencies

Packages declared in `requirements.txt` or `pyproject.toml` are automatically indexed at depth **2**, even when the global default is 1. Named entries in `packageIndexDepths` take priority over the automatic boost. See the [`packageIndexDepths` setting page](../settings/python_analysis_packageIndexDepths.md#automatic-depth-boost-for-direct-dependencies) for details.

#### Namespace packages

[PEP 420](https://peps.python.org/pep-0420/) namespace packages (e.g., `azure`, `google`) lack an `__init__.py` at the top level. Pylance automatically looks up to 4 levels deep to find the first real subpackage, so `from azure.storage.blob import BlobClient` works even at the default depth of 1. See the [`packageIndexDepths` setting page](../settings/python_analysis_packageIndexDepths.md#namespace-package-handling) for details.

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

1. **Show only direct dependencies** — enable [`showOnlyDirectDependenciesInAutoImport`](../settings/python_analysis_showOnlyDirectDependenciesInAutoImport.md) to limit auto-import completions to packages declared in `requirements.txt` or `pyproject.toml`:

    ```json
    {
        "python.analysis.showOnlyDirectDependenciesInAutoImport": true
    }
    ```

2. **Reduce `packageIndexDepths`** for noisy packages:

    ```json
    {
        "python.analysis.packageIndexDepths": [{ "name": "noisy_package", "depth": 1 }]
    }
    ```

3. **Disable auto-import completions** and rely on quick fixes instead:

    ```json
    {
        "python.analysis.autoImportCompletions": false
    }
    ```

4. **Exclude directories** you don't want indexed:

    ```json
    {
        "python.analysis.exclude": ["vendor/**", "third_party/**"]
    }
    ```

---

## Missing Suggestions

**Symptom**: Typing a known symbol doesn't show an auto-import suggestion.

### Common Causes and Fixes

| Cause                                                                                  | Fix                                                                                                                                                                                                 |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Indexing disabled                                                                      | Set [`indexing`](../settings/python_analysis_indexing.md) to `true`                                                                                                                                 |
| `autoImportCompletions` is `false`                                                     | Set [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md) to `true`                                                                                                       |
| Package not installed in selected environment                                          | Install the package in the active interpreter's environment                                                                                                                                         |
| Symbol is deeply nested                                                                | Increase `depth` in [`packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md). Direct dependencies declared in `requirements.txt`/`pyproject.toml` are automatically indexed deeper |
| Symbol omitted from `__all__` in an untyped `.py` package                              | Set `includeAllSymbols: true` in [`packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md) for that package                                                                         |
| Private symbol (underscore prefix)                                                     | Pylance hides private symbols by default. Import manually                                                                                                                                           |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md) is `"light"` | Switch to `"default"` or `"full"` for better indexing                                                                                                                                               |
| Symbol only available through a re-export in your code                                 | Enable [`includeAliasesFromUserFiles`](../settings/python_analysis_includeAliasesFromUserFiles.md)                                                                                                  |

---

## Organize Imports on Save

VS Code can automatically remove unused imports with Pylance when you save; sorting requires a separate import organizer. This works alongside auto-imports.

Add to `.vscode/settings.json`:

```json
{
    "editor.codeActionsOnSave": {
        "source.unusedImports": "explicit"
    }
}
```

This removes unused imports on save.

See [`python.analysis.fixAll`](../settings/python_analysis_fixAll.md) for other code actions available on save.

> **Note**: To sort and format imports (custom grouping rules, blank lines between groups, line length), consider using [isort](https://pycqa.github.io/isort/) or [Ruff](https://docs.astral.sh/ruff/formatter/).

Example `settings.json` for using Ruff as the import organizer:

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
- [ ] **Indexing complete**: Check **Output → Python Language Server** — auto-imports improve after indexing finishes
- [ ] **Language server mode**: Not set to `"light"` (limits indexing)
- [ ] **Config file**: No `pyrightconfig.json` overriding VS Code settings unexpectedly. See [Settings Troubleshooting](settings-troubleshooting.md)

---

## FAQ

### Q: Why does auto-import suggest a long path instead of the short one?

Pylance suggests the path where the symbol is defined, not necessarily the re-export path. To prefer shorter paths:

- Enable [`includeAliasesFromUserFiles`](../settings/python_analysis_includeAliasesFromUserFiles.md) — this makes re-exported symbols available through the shorter path.
- Libraries that define `__all__` in their `__init__.py` usually provide the short path by default.

### Q: Can I auto-import from packages in `extraPaths`?

Yes. Pylance can offer auto-imports from packages found through [`extraPaths`](../settings/python_analysis_extraPaths.md).

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

Last content update aligned with [Pylance 2026.4.100](https://github.com/microsoft/pylance-release/blob/c7d6efcb25c68381cc542a088d218608f6d87761/CHANGELOG.md#20264100-9-october-2026-prerelease).

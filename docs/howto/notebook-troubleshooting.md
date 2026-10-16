# How to Troubleshoot Pylance in Jupyter Notebooks

Pylance provides IntelliSense, diagnostics, and type checking inside Jupyter notebooks in VS Code. However, notebooks have a different execution model from standalone `.py` files, which can cause unexpected behavior. This guide covers the most common issues.

---

## Table of Contents

- [How Pylance Analyzes Notebooks](#how-pylance-analyzes-notebooks)
- [Missing Imports or Unresolved Symbols](#missing-imports-or-unresolved-symbols)
- [Variables from Other Cells Not Recognized](#variables-from-other-cells-not-recognized)
- [No Diagnostics or IntelliSense in Notebook Cells](#no-diagnostics-or-intellisense-in-notebook-cells)
- [Performance Issues in Large Notebooks](#performance-issues-in-large-notebooks)
- [Wrong Python Environment](#wrong-python-environment)
- [Diagnostics Differ Between Notebooks and .py Files](#diagnostics-differ-between-notebooks-and-py-files)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## How Pylance Analyzes Notebooks

Pylance analyzes Python code cells in order, parsing each cell separately and making names from earlier cells available to later cells. This means:

- A variable defined in Cell 1 is visible in Cell 2 (as long as Cell 1 appears earlier in the notebook).
- Imports in an earlier cell apply to later cells.
- Pylance does **not** track runtime execution order — it uses the **document order** (top to bottom) of cells.

Markdown cells are ignored during analysis.

---

## Missing Imports or Unresolved Symbols

**Symptom**: `Import "pandas" could not be resolved` or similar errors in notebook cells.

### Causes and Fixes

| Cause                                                                                                  | Fix                                                                                                                  |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| Wrong kernel/interpreter selected                                                                      | Click the kernel selector in the top-right of the notebook and choose the environment where the package is installed |
| Package not installed in the selected environment                                                      | Run `%pip install pandas` in a notebook cell, or install in the terminal with the correct venv active                |
| [`extraPaths`](../settings/python_analysis_extraPaths.md) not set                                      | Add the source directory to [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md)                |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides VS Code settings | Check config file. See [Settings Troubleshooting](settings-troubleshooting.md)                                       |

### Quick Check

Run this in a notebook cell to confirm the environment:

```python
import sys
print(sys.executable)
print(sys.path)
```

Compare the output with what VS Code shows in the kernel selector.

---

## Variables from Other Cells Not Recognized

**Symptom**: Pylance shows `"x" is not defined` for a variable defined in another cell.

### Common Causes

1. **Cell order matters**: Pylance uses the top-to-bottom order of cells in the notebook, not the order you ran them. If you define `x` in Cell 5 and use it in Cell 3, Pylance will report it as undefined even if you ran Cell 5 first at runtime.

2. **Conditional definitions**: If a variable is defined inside an `if` block, Pylance may flag it as possibly unbound in later cells. This is correct static analysis — Pylance cannot know which branches ran.

3. **Magic commands / `%run`**: Pylance does not execute `%run`, `%load`, or other magic commands. Variables injected this way are invisible to static analysis.

### Fix

- Reorder cells so definitions come before usage in document order.
- For variables injected by magic commands, add a type stub or type annotation:

```python
# Tell Pylance about a variable injected by %run
import pandas as pd
df: pd.DataFrame  # Pylance now knows df exists and its type
```

---

## No Diagnostics or IntelliSense in Notebook Cells

**Symptom**: Completions and error squiggles don't appear in notebook cells.

### Checks

1. **Pylance is the active language server**: Open Settings and verify `"python.languageServer"` is `"Pylance"` (or `"Default"`, which uses Pylance).

2. **Workspace trust**: Installed-library analysis requires a trusted workspace.

3. **Restart**: Run **"Python: Restart Language Server"** from the Command Palette (Ctrl+Shift+P).

4. **Check [`languageServerMode`](../settings/python_analysis_languageServerMode.md)**: If set to `"light"`, diagnostics are limited. Try `"default"` or `"full"`.

5. **Check Pylance output**: Open **Output** panel → select **Python Language Server** → look for errors.

---

## Performance Issues in Large Notebooks

**Symptom**: Slow completions, delayed diagnostics, or high memory usage with large notebooks.

### Recommendations

- **Split large notebooks**: Notebooks with hundreds of cells create a large virtual document for Pylance to analyze.
- **Reduce [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)**: Use `"off"` or `"basic"` for data-science notebooks where strict typing is less important.
- **Disable unused features**: Turn off [inlay hints](../settings/python_analysis_inlayHints_variableTypes.md) if you don't need them.
- **Check [`languageServerMode`](../settings/python_analysis_languageServerMode.md)**: Use `"light"` or `"default"` for large notebooks. See [Performance Tuning](performance-tuning.md).

---

## Wrong Python Environment

**Symptom**: Pylance resolves different packages than your notebook kernel uses.

Notebook execution and analysis use these environment selections:

1. **Kernel**: The Python environment that executes cells (shown in the top-right kernel selector).
2. **Language server**: Pylance uses the interpreter information supplied for the notebook's kernel.

If a package works at runtime but Pylance cannot resolve it, check the notebook kernel's environment.

### Fix

1. Click the kernel selector in the notebook → choose your environment.
2. Confirm imports resolve in the notebook after changing the kernel.
3. Run **"Python: Restart Language Server"** to pick up the change.

---

## Diagnostics Differ Between Notebooks and .py Files

Pylance's notebook analysis has a few differences from standalone file analysis:

- **Cell boundaries are transparent**: Variables flow across cells but Pylance treats them like consecutive blocks in one file.
- **IPython magics are ignored**: Lines starting with `%` or `!` are treated as comments by Pylance. No errors, but no analysis either.
- **`display()` and IPython builtins**: Pylance normally recognizes `display()` when IPython is available. Add explicit imports for other injected globals or unresolved names:

```python
from IPython.display import display
```

---

For non-Python cell bodies, the experimental `python.analysis.cellMagicLanguages` setting maps magic names (without `%%`) to VS Code language IDs. Install an extension that provides the desired language, then add a mapping in `.vscode/settings.json`, for example:

```json
{
    "python.analysis.cellMagicLanguages": {
        "sql": "sql"
    }
}
```

Keep the notebook cell's language set to Python and put `%%sql` at the start of the cell, with SQL on the following lines. Pylance forwards completions, hover, and Go to Definition for the body to that language extension. Use Ctrl+Space to request completions manually. Available language features depend on the extension.

## Diagnostic Checklist

When Pylance isn't working correctly in a notebook:

- [ ] **Notebook environment**: Select the kernel where your packages are installed
- [ ] **Package is installed**: Run `%pip show <package>` in a cell to verify
- [ ] **Cell order**: Definitions appear above usages in document order (not just execution order)
- [ ] **Workspace trust**: Installed-library analysis requires a trusted workspace
- [ ] **Restart**: Run "Python: Restart Language Server" after changes
- [ ] **Output panel**: Check **Output → Python Language Server** for errors or warnings

---

## FAQ

### Q: Can I use `pyrightconfig.json` with notebooks?

Yes. If a `pyrightconfig.json` exists in the workspace root, it applies to notebooks the same way it applies to `.py` files. Settings like [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md), [`extraPaths`](../settings/python_analysis_extraPaths.md), and diagnostic overrides all take effect.

### Q: Why does Pylance flag `display()` as undefined?

`display()` is normally recognized when IPython is available. If it is unresolved, check the notebook's environment or try an explicit import:

```python
from IPython.display import display
```

### Q: How do I suppress diagnostics for cells that use magic commands?

For Python diagnostics, add `# type: ignore` on lines that Pylance cannot analyze, or use [`python.analysis.ignore`](../settings/python_analysis_ignore.md) to suppress diagnostics for the entire notebook file (not recommended for most cases). For errors from another cell language, use that language extension's diagnostic settings.

### Q: Can Pylance analyze `.ipynb` files outside VS Code?

Pylance runs only inside VS Code. For static type checking of notebooks outside VS Code, consider exporting to `.py` and running [Pyright CLI](ci-type-checking.md).

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution for all file types
- [How to Tune Pylance Performance](performance-tuning.md) — memory and responsiveness settings
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — config file precedence and overrides

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

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

Pylance treats each notebook as a single virtual document by concatenating all code cells in order. This means:

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

2. **Notebook is trusted**: VS Code requires you to trust a notebook before extensions can run. Click **Trust** in the notification bar if prompted.

3. **Restart**: Run **"Python: Restart Language Server"** from the Command Palette (Ctrl+Shift+P).

4. **Check [`languageServerMode`](../settings/python_analysis_languageServerMode.md)**: If set to `"light"`, diagnostics are limited. Try `"default"` or `"full"`.

5. **Check Pylance output**: Open **Output** panel → select **Pylance** → look for errors.

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

Notebooks in VS Code have **two** Python selections that must match:

1. **Kernel**: The Python environment that executes cells (shown in the top-right kernel selector).
2. **Language server**: The Python interpreter Pylance uses for analysis (shown in the VS Code status bar).

If these point to different environments, Pylance may report missing imports for packages that work at runtime.

### Fix

1. Click the kernel selector in the notebook → choose your environment.
2. Click the Python version in the VS Code status bar → choose the **same** environment.
3. Run **"Python: Restart Language Server"** to pick up the change.

---

## Diagnostics Differ Between Notebooks and .py Files

Pylance's notebook analysis has a few differences from standalone file analysis:

- **Cell boundaries are transparent**: Variables flow across cells but Pylance treats them like consecutive blocks in one file.
- **IPython magics are ignored**: Lines starting with `%` or `!` are treated as comments by Pylance. No errors, but no analysis either.
- **`display()` and IPython builtins**: Pylance may not know about `display()`, `get_ipython()`, or other IPython-injected globals. Add explicit imports if you see errors:

```python
from IPython.display import display
```

---

## Diagnostic Checklist

When Pylance isn't working correctly in a notebook:

- [ ] **Kernel matches language server**: Both point to the same Python environment
- [ ] **Package is installed**: Run `%pip show <package>` in a cell to verify
- [ ] **Cell order**: Definitions appear above usages in document order (not just execution order)
- [ ] **Notebook is trusted**: Check the trust banner at the top
- [ ] **Restart**: Run "Python: Restart Language Server" after changes
- [ ] **Output panel**: Check **Output → Pylance** for errors or warnings

---

## FAQ

### Q: Can I use `pyrightconfig.json` with notebooks?

Yes. If a `pyrightconfig.json` exists in the workspace root, it applies to notebooks the same way it applies to `.py` files. Settings like [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md), [`extraPaths`](../settings/python_analysis_extraPaths.md), and diagnostic overrides all take effect.

### Q: Why does Pylance flag `display()` as undefined?

`display()` is injected into the IPython namespace at runtime. Pylance doesn't know about it without an explicit import:

```python
from IPython.display import display
```

### Q: How do I suppress diagnostics for cells that use magic commands?

Add `# type: ignore` on lines that Pylance cannot analyze, or use [`python.analysis.ignore`](../settings/python_analysis_ignore.md) to suppress diagnostics for the entire notebook file (not recommended for most cases).

### Q: Can Pylance analyze `.ipynb` files outside VS Code?

Pylance runs only inside VS Code. For static type checking of notebooks outside VS Code, consider exporting to `.py` and running [Pyright CLI](ci-type-checking.md).

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution for all file types
- [How to Tune Pylance Performance](performance-tuning.md) — memory and responsiveness settings
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — config file precedence and overrides

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

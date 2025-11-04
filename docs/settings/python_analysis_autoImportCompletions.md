# Understanding `python.analysis.autoImportCompletions` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, code completion, code navigation, and other language features to enhance your Python development experience.

One of Pylance's powerful features is **auto-import completions**, which can significantly improve coding efficiency by automatically suggesting import statements as you type. However, this feature can affect the performance of the editor or might introduce too many suggestions, especially in large projects.

This guide explains what auto-import completions are, how the `python.analysis.autoImportCompletions` setting affects them, and how you can customize Pylance to suit your workflow.

## What Are Auto-Import Completions?

Auto-import completions are code completion suggestions provided by Pylance to automatically insert import statements for symbols (such as classes, functions, and constants) that are not currently imported into your code file.

When you start typing a symbol that is not yet imported, Pylance can suggest it along with an import statement, saving you the effort of manually adding the necessary imports at the top of your file.

### Example of Auto-Import Completions

Consider the following scenario:

```python
def calculate_area():
    circle = Circle(radius=5)
```

As you start typing `Circle`, Pylance can suggest the `Circle` class from `mathlib.shapes`, even if you haven't imported it yet.

Selecting the suggestion automatically adds the import statement at the top of your file:

```python
from mathlib.shapes import Circle

def calculate_area():
    circle = Circle(radius=5)
```

This feature streamlines the coding process by reducing the need to manually write import statements.

## The `python.analysis.autoImportCompletions` Setting

The `python.analysis.autoImportCompletions` setting in Pylance allows you to enable or disable auto-import completions. By adjusting this setting, you can control whether Pylance offers auto-import suggestions in the completions list.

### Accepted Values

- `true`: Enables auto-import completions. Pylance will suggest auto-imports for symbols as you type.
- `false` (default): Disables auto-import completions. Pylance will not suggest symbols that are not already imported.

### How to Change the Setting

To adjust this setting in Visual Studio Code:

1. **Open the Settings**:

   - Click on the gear icon in the lower-left corner and select **Settings**.

2. **Search for the Setting**:

   - In the search bar at the top, type `python.analysis.autoImportCompletions`.

3. **Modify the Setting**:

   - Check the box to set it to `true` (enable auto-import completions), or uncheck it to set it to `false` (disable auto-import completions).

Alternatively, you can edit your `settings.json` file directly:

1. **Open the Settings (JSON)**:

   - Open the Command Palette and select **Preferences: Open Settings (JSON)**.

2. **Add the Setting**:

   - Add or modify the following line in your `settings.json` file:

   ```json
   "python.analysis.autoImportCompletions": true
   ```

## Related Settings

- [`python.analysis.indexing`](python_analysis_indexing.md)
  - Used to specify whether Pylance should index installed third party libraries and user files to improve features such as auto-import, add import, workspace symbols, etc.

- [`python.analysis.includeAliasFromUserFiles`](python_analysis_includeAliasesFromUserFiles.md)
  - Include alias symbols from user files. This will make alias symbols appear in features such as `add import` and `auto import`.

- [`python.analysis.userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md)
    - Maximum number of user files to index in the workspace. 

- [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md)
    - Used to override how many levels under installed packages to index on a per package basis. 

- `python.analysis.showOnlyDirectDependenciesInAutoImport`
  - Show only direct dependencies declared in `requirements.txt` or `pyproject.toml` in `auto import` suggestions, if they exist. This only affects `auto import` for completions. The `add import` code action will continue to show all possible imports.

## Frequently Asked Questions

### Q: Why aren't auto-import completions working for some packages?

**A:** By default, Pylance indexes only the top-level modules of packages to optimize performance. If auto-import completions aren't suggesting symbols from deeper submodules, you may need to adjust the [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepapt install screenfetchths.md) setting to increase the indexing depth for those packages.

### Q: Will enabling auto-import completions affect performance?

**A:** Enabling `python.analysis.autoImportCompletions` can impact performance, especially in large projects or with packages that have many submodules. You can mitigate this by limiting the indexing depth or disabling auto-import completions if performance becomes an issue.

### Q: How can I exclude certain packages from auto-import completions?

**A:** You can adjust the [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md) setting by setting the `depth` to `0` for packages you want to exclude:

```json
"python.analysis.packageIndexDepths": [
    {
        "name": "unwanted_package",
        "depth": 0
    }
]
```

This prevents Pylance from indexing the specified package for auto-import completions.

### Q: Can I enable auto-import completions only for specific packages?

**A:** Yes, by configuring the [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md) setting, you can specify which packages to index and to what depth. Set `depth` to a positive number for packages you want to include and `0` for others.

### Q: Why do some top-level variables not appear in auto-import or add import suggestions?

**A:**
The behavior for top-level variables differs between user files and third-party libraries:

- **Third-party libraries:**
  Whether a symbol is a variable or not generally does not affect indexing, since top-level variables are rare in packages. Instead, which symbols are available for auto-import is determined by other logic, such as the [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md) setting (which controls how deeply Pylance indexes packages), the [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md), and the `python.analysis.showOnlyDirectDependenciesInAutoImport` option (see [README.md](../../README.md)). These settings affect which modules and symbols are indexed and suggested for auto-import.

- **User files (your own workspace):**
  For variables defined at the top level in user files, Pylance only includes them in auto-import/add import suggestions if:
  - The variable name is all uppercase (e.g., `MY_CONSTANT`), or
  - The variable is explicitly listed in the module’s `__all__` attribute.

  This is because user workspaces often contain many scripts with numerous temporary or local variables, and there is no reliable way for Pylance to know which variables are intended to be imported by other modules. Using `__all__` signals that a variable is meant to be exported and available for import elsewhere.

  Additional settings can also affect this behavior:
  - [`python.analysis.includeAliasesFromUserFiles`](python_analysis_includeAliasesFromUserFiles.md): Controls whether alias symbols from user files are included in auto-import suggestions.
  - [`python.analysis.userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md): Limits how many user files are indexed, which can affect which variables are available for import.

If you want a variable from your own code to appear in auto-import suggestions, either use an all-uppercase name or add it to the module’s `__all__` list.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

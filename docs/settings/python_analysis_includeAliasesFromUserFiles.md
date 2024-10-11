# Understanding `python.analysis.includeAliasesFromUserFiles` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It enhances Python development by providing IntelliSense features such as code completion, type checking, auto imports.

One of Pylance's powerful features is its ability to provide auto-import suggestions to improve coding efficiency. However, in some cases, developers may use aliases in their code, and by default, Pylance does not include alias symbols from user files in its auto-import suggestions or add import features. The `python.analysis.includeAliasesFromUserFiles` setting allows you to control this behavior.

This guide explains what alias symbols are, how the `python.analysis.includeAliasesFromUserFiles` setting affects them, and how you can configure Pylance to include or exclude alias symbols from user files in auto-import and add/search import features.

## What Are Alias Symbols in User Files?

In Python, alias symbols refer to symbols that are not defined in the current file but are imported from other files. By default, Pylance does not include these alias symbols when providing features like auto-imports and add import. This means that if you try to auto-import a symbol, Pylance will suggest importing it from its original source, not from another user file where it has been imported.

For example:

```python
# utils.py
def helper_function():
    pass

# __init__.py
from .utils import helper_function

# main.py
# Trying to use 'helper_function' might not prompt an auto-import suggestion 
# from '__init__.py' unless the "python.analysis.includeAliasesFromUserFiles" is enabled.
```

In this example, `helper_function` is imported into `__init__.py`, and Pylance may not suggest importing `helper_function` from `__init__.py` in `main.py` unless `includeAliasesFromUserFiles` is set to `true`.

## The `python.analysis.includeAliasesFromUserFiles` Setting

The `python.analysis.includeAliasesFromUserFiles` setting controls if alias symbols from user files are included in auto-import and add import suggestions.

- `true`: Includes alias symbols from user files.
- `false` (default): Only suggests symbols from their original definitions.

## How to Change the Setting

1. **Open Settings**: Click on the gear icon in the lower-left corner of Visual Studio Code and select **Settings**.
2. **Search for the Setting**: Type `python.analysis.includeAliasesFromUserFiles` in the search bar.
3. **Modify the Setting**: Set it to `true` or `false` as needed.

Alternatively, you can edit your `settings.json` file directly:

1. **Open Settings (JSON)**: Open the command palette and type `Preferences: Open Settings (JSON)`.
2. **Add or Modify the Setting**:
   ```json
   "python.analysis.includeAliasesFromUserFiles": true
   ```

## When and Why to Enable `includeAliasesFromUserFiles`

### Improved Auto-Import Suggestions

By enabling `python.analysis.includeAliasesFromUserFiles`, Pylance will include alias symbols from your user files in features like auto-import suggestions. This can be particularly useful when you have organized your codebase to expose certain symbols through a central module or when you frequently use aliases to simplify imports.

Consider the following scenario with the following project structure:

```
my_project/
├── __init__.py
├── utils.py
├── nested/
│   ├── redundant.py
│   ├── all.py
└── usage.py
```

**`utils.py`**

```python
def helper_function():
    print("This is the helper function")
```

**`__init__.py`**

```python
from .utils import helper_function
```

**`nested/redundant.py`**

```python
from ..utils import helper_function as helper_function
```

**`nested/all.py`**

```python
from my_project.utils import helper_function
__all__ = ["helper_function"]
```

**`usage.py`**

```python
from .utils import helper_function
```

When using auto-import, Pylance will choose the best alias symbol based on the following criteria, with each criterion contributing 1 point:

- The alias symbol is in an `__init__.py` file.
- The alias symbol is in a redundant form (e.g., `import helper_function as helper_function`).
- The alias symbol is listed in `__all__`.

The alias symbol with the highest score will be chosen. In case of a tie, the symbol with the shortest import module path will be selected.

For example, the alias symbol from `usage.py` has the lowest score and will be disregarded. The alias symbols from `__init__.py`, `redundant.py`, and `all.py` each have 1 point, but the one from `__init__.py` has the shortest import module path, so it will be selected. If `__init__.py` had used `from .utils import helper_function as helper_function` instead, it would have received 2 points and be selected.

Unlike auto-import suggestions in  the completion list, the add/search import for code action will display all available alias symbols, allowing you to choose one. Once you select an alias, the Most Recently Used (MRU) feature will remember your choice and continue suggesting it for future imports.

### Consistent Import Paths

Enabling this setting can help maintain consistent import paths across your codebase. If you prefer to import symbols from a specific module that re-exports them (using aliases), including aliases in auto-import suggestions ensures that Pylance assists you in keeping this consistency.

## Performance Considerations

Enabling `python.analysis.includeAliasesFromUserFiles` can impact performance, especially in large codebases. Pylance may need to index more symbols and monitor more files for changes, which can increase resource usage.

When this setting is `true`, Pylance includes alias symbols from user files in its analysis, which can cause:

- Increased memory usage.

- More CPU utilization during indexing.

- Potential delays in displaying auto-import suggestions.

If you experience performance degradation after enabling this setting, you may consider:

- Keeping the setting disabled (`false`) to improve performance.

- Optimizing your codebase to reduce the number of aliases or reorganizing imports.

## Frequently Asked Questions

### Does enabling `includeAliasesFromUserFiles` affect third-party libraries?

No, this setting only affects alias symbols defined in your user files (the code within your project). Alias symbols in third-party libraries are already included by default. As they are less likely to change frequently, there is no significant performance concern.

### Why are alias symbols from user files excluded by default?

Excluding alias symbols by default helps optimize Pylance's performance. User files change frequently, and supporting alias symbols requires re-indexing all dependent files, which can be numerous and impact performance significantly.

### Can I enable this setting for specific files or projects?

Currently, the `python.analysis.includeAliasesFromUserFiles` setting applies globally or per-workspace in Visual Studio Code settings. You can adjust the setting in your workspace's `settings.json` to enable it for a specific project.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

---

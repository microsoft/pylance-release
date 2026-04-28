# Understanding `python.analysis.includeExtraPathSymbolsInSymbolSearch` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a powerful language server for Python in Visual Studio Code, offering advanced features like IntelliSense, type checking, auto-imports, and more. One of the settings that influence Pylance's workspace symbol search behavior is `python.analysis.includeExtraPathSymbolsInSymbolSearch`.

This guide explains what the `python.analysis.includeExtraPathSymbolsInSymbolSearch` setting does, how it affects Workspace Symbol search, and how to configure it.

## What is `python.analysis.includeExtraPathSymbolsInSymbolSearch`?

The `python.analysis.includeExtraPathSymbolsInSymbolSearch` setting controls whether Pylance includes symbols from directories listed in [`python.analysis.extraPaths`](python_analysis_extraPaths.md) when you use **Workspace Symbol search** (Ctrl+T / Cmd+T).

By default, Workspace Symbol search only returns symbols from your own project files (user code). Enabling this setting expands the search to include symbols from directories you've added to `extraPaths` — for example, shared libraries or other packages in a monorepo that aren't part of the current workspace folder.

## The `python.analysis.includeExtraPathSymbolsInSymbolSearch` Setting

### Accepted Values

- `false` (default): Workspace Symbol search only includes symbols from user code.
- `true`: Workspace Symbol search also includes symbols from directories in [`python.analysis.extraPaths`](python_analysis_extraPaths.md).

### Default Value

The default value is `false`.

## How to Change the Setting

To adjust the `python.analysis.includeExtraPathSymbolsInSymbolSearch` setting:

- Open **Settings** and search for `python.analysis.includeExtraPathSymbolsInSymbolSearch`.
- Toggle the setting on or off.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:
    ```json
    "python.analysis.includeExtraPathSymbolsInSymbolSearch": true
    ```

## When to Use This Setting

This setting is particularly useful in **monorepo** setups where you use `extraPaths` to make other packages importable. Without this setting, Workspace Symbol search won't show symbols from those packages. Enabling it lets you search for functions, classes, and other symbols across your monorepo's shared libraries.

## Performance Considerations

Enabling this setting may slow down Workspace Symbol search because Pylance needs to search through additional indexed symbols from `extraPaths` directories.

## Related Settings

- [`python.analysis.extraPaths`](python_analysis_extraPaths.md): The directories whose symbols are included when this setting is enabled.
- [`python.analysis.indexing`](python_analysis_indexing.md): Must be enabled for symbol indexing. If indexing is disabled, this setting has no effect.
- [`python.analysis.includeVenvInWorkspaceSymbols`](python_analysis_includeVenvInWorkspaceSymbols.md): Similar setting for including symbols from the active venv's `site-packages`.

## See Also

- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — symbol search across `extraPaths` directories
- [How to Tune Pylance Performance](../howto/performance-tuning.md) — performance impact of searching extra paths

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

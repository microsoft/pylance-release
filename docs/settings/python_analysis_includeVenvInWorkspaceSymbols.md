# Understanding `python.analysis.includeVenvInWorkspaceSymbols` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a powerful language server for Python in Visual Studio Code, offering advanced features like IntelliSense, type checking, auto-imports, and more. One of the settings that influence Pylance's workspace symbol search behavior is `python.analysis.includeVenvInWorkspaceSymbols`.

This guide explains what the `python.analysis.includeVenvInWorkspaceSymbols` setting does, how it affects Workspace Symbol search, and how to configure it.

## What is `python.analysis.includeVenvInWorkspaceSymbols`?

The `python.analysis.includeVenvInWorkspaceSymbols` setting controls whether Pylance includes symbols from installed packages in the active virtual environment's `site-packages` directory when you use **Workspace Symbol search** (Ctrl+T / Cmd+T).

By default, Workspace Symbol search only returns symbols from your own project files (user code). Enabling this setting expands the search to include symbols from third-party packages installed in your virtual environment.

## The `python.analysis.includeVenvInWorkspaceSymbols` Setting

### Accepted Values

- `false` (default): Workspace Symbol search only includes symbols from user code.
- `true`: Workspace Symbol search also includes symbols from packages in the active venv's `site-packages` and `dist-packages` directories.

### Default Value

The default value is `false`.

## How to Change the Setting

To adjust the `python.analysis.includeVenvInWorkspaceSymbols` setting:

- Open **Settings** and search for `python.analysis.includeVenvInWorkspaceSymbols`.
- Toggle the setting on or off.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:
    ```json
    "python.analysis.includeVenvInWorkspaceSymbols": true
    ```

## Performance Considerations

Enabling this setting may slow down Workspace Symbol search because Pylance needs to search through additional indexed symbols from installed packages.

The depth of sub-packages searched is controlled by [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md). Increase the `depth` for a specific package to include symbols from deeper sub-modules.

## Related Settings

- [`python.analysis.indexing`](python_analysis_indexing.md): Must be enabled for library symbol indexing. If indexing is disabled, this setting has no effect.
- [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md): Controls how deep into each package Pylance indexes sub-modules.
- [`python.analysis.includeExtraPathSymbolsInSymbolSearch`](python_analysis_includeExtraPathSymbolsInSymbolSearch.md): Similar setting for including symbols from [`python.analysis.extraPaths`](python_analysis_extraPaths.md) directories.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

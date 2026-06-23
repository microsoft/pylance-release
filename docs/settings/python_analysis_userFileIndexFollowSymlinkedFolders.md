# Understanding `python.analysis.userFileIndexFollowSymlinkedFolders` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.userFileIndexFollowSymlinkedFolders` setting controls whether Pylance follows symbolic links when indexing the user files in your workspace.

## What is `python.analysis.userFileIndexFollowSymlinkedFolders`?

To power features such as auto-import, add-import, and workspace symbol search, Pylance builds an index of the files in your workspace. When this setting is enabled, that user-file indexing follows folders that are symbolic links and indexes the files they point to.

This exists as a performance safeguard. If a workspace contains symlinks that point into very large directory trees, following them can make indexing slow. Disabling this setting tells Pylance not to descend into symlinked folders, keeping indexing fast.

**Type**: `boolean`
**Default**: `true`
**Scope**: resource (can be set per workspace or folder)

## How to Change `python.analysis.userFileIndexFollowSymlinkedFolders`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.userFileIndexFollowSymlinkedFolders`.
3. Uncheck the box to stop following symlinked folders.

### Using `settings.json`

```json
{
    "python.analysis.userFileIndexFollowSymlinkedFolders": false
}
```

## When to Use It

- **Keep enabled** (the default) if your workspace uses symlinks to include source you actively edit and want those files indexed.
- **Disable** if your workspace contains symlinks into very large directory trees and indexing is slow, so Pylance skips them.

## Related Settings

- [`python.analysis.indexing`](python_analysis_indexing.md) — controls whether Pylance indexes installed libraries and user files.
- [`python.analysis.userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md) — limits how many user files are indexed.

## See Also

- [How to Tune Pylance Performance](../howto/performance-tuning.md) — strategies for large workspaces.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

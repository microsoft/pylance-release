# Understanding `python.analysis.userFileIndexingLimit` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

To provide features like auto-import suggestions and workspace symbol searches, Pylance indexes your project's Python files. In large workspaces, this indexing process can consume significant resources and impact performance.

The `python.analysis.userFileIndexingLimit` setting allows you to control the number of user files Pylance indexes, helping you balance functionality and performance in your development environment.

## What Is User File Indexing in Pylance?

User file indexing is the process where Pylance scans and indexes Python files in your workspace (user files). This indexing enables several powerful features:

- **Auto-Import Suggestions**: Pylance can suggest imports from your codebase when you reference symbols not yet imported.
- **Workspace Symbol Search**: Quickly navigate to symbols (classes, functions, variables) defined anywhere in your workspace.
- **Enhanced Misc Features**: Used for other miscellaneous features such as code generation, document outline, and document symbols.

While indexing enhances productivity, it can be resource-intensive in large projects with thousands of files, potentially affecting performance.

## Understanding `python.analysis.userFileIndexingLimit`

The `python.analysis.userFileIndexingLimit` setting controls the maximum number of user (workspace) files that Pylance will index. By adjusting this limit, you can manage Pylance's resource consumption and improve performance in large workspaces.

### How It Works

- **Default Value**: `2000` (`-1` in `full` language server mode)

    With a limit of `2000`, Pylance indexes up to 2,000 Python files in your workspace.

- **Custom Value**: You can set this to any positive integer or `-1`:
    - **Positive Integer**: Pylance will index up to that number of files.
    - **`-1`**: Pylance will index all Python files in your workspace, regardless of the number.

### Why It Matters

In projects with a large number of Python files, indexing all files can lead to high memory usage and CPU load, potentially slowing down your development environment or causing Pylance to crash with out-of-memory errors.

By setting `python.analysis.userFileIndexingLimit` to a lower number, you can reduce the resource impact of indexing, at the cost of reduced functionality in features that rely on indexing.

## How to Change the Setting

You can adjust the `python.analysis.userFileIndexingLimit` setting in Visual Studio Code to control Pylance's indexing behavior.

### Via Settings UI

1. **Open Settings**:
    - Click on the gear icon in the lower-left corner and select **Settings**.

2. **Find the Setting**:
    - In the search bar at the top, type `python.analysis.userFileIndexingLimit`.

3. **Modify the Setting**:
    - Enter the desired integer value in the input box. For example, enter `1000` to limit indexing to 1,000 files.

### Via `settings.json`

1. **Open Command Palette**:
    - Click on the gear icon in the lower-left corner and select **Command Palette**.

2. **Open Settings (JSON)**:
    - Type `Preferences: Open Settings (JSON)` and select it.

3. **Add or Modify the Setting**:
    - Add the following line to your `settings.json` file:

        ```json
        "python.analysis.userFileIndexingLimit": 1000
        ```

    - Replace `1000` with the desired limit, or `-1` to index all files.

## Frequently Asked Questions

### Q: What features are affected by changing `python.analysis.userFileIndexingLimit`?

**A:** Reducing the limit can reduce auto-import coverage. Workspace symbol search can still find symbols in unindexed files.

### Q: Are there other settings I should adjust for large workspaces?

**A:** Yes, consider adjusting:

- **[`python.analysis.indexing`](python_analysis_indexing.md)**: Set to `false` to disable indexing entirely.

    ```json
    "python.analysis.indexing": false
    ```

    This will disable both user file indexing and library indexing.

- **[`python.analysis.include`](python_analysis_include.md)** and **[`python.analysis.exclude`](python_analysis_exclude.md)**: Specify where Pylance looks for files to analyze.

    ```json
    "python.analysis.exclude": [
        "**/node_modules",
        "**/__pycache__",
        "*.gen.py"
    ]
    ```

- **[`python.analysis.userFileIndexFollowSymlinkedFolders`](python_analysis_userFileIndexFollowSymlinkedFolders.md)**: Disable to stop user-file indexing from following symlinked folders that point into very large directory trees.

### Q: How do I know what value to set for `python.analysis.userFileIndexingLimit`?

**A:** It depends on your project's size and your machine's capabilities. Start with the default value and adjust as needed. Monitor Pylance's performance and resource usage to find an optimal setting.

### Q: Will reducing the indexing limit affect IntelliSense features?

**A:** Reducing the indexing limit can reduce auto-import coverage. IntelliSense within open files will still function, and workspace symbol search can still find symbols in unindexed files.

### Q: What is the difference between [`packageIndexDepths`](python_analysis_packageIndexDepths.md) and `userFileIndexingLimit`?

**A:** The [`packageIndexDepths`](python_analysis_packageIndexDepths.md) setting controls the indexing of third-party library packages (e.g., files under `site-packages`), allowing you to specify how deeply Pylance should index these libraries. In contrast, the `userFileIndexingLimit` setting controls the indexing of user Python files (e.g., files within your workspace). Together, these settings enable you to customize the scope and depth of indexing for both user and third-party code.

## See Also

- [How to Tune Pylance Performance](../howto/performance-tuning.md) — adjusting indexing limits for large workspaces

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

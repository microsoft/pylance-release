# Understanding `python.analysis.persistAllIndices` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It offers advanced features like type checking, IntelliSense, auto-imports, and code navigation to enhance your Python development experience.

One of the ways Pylance provides these features is through **indexing** your project's files and installed libraries. Indexing allows Pylance to analyze the codebase and offer features like auto-import suggestions and workspace symbol search more efficiently.

The `python.analysis.persistAllIndices` setting in Pylance controls whether the indices for third-party libraries are saved to disk and reused across sessions. This guide explains what indexing is in Pylance, how the `python.analysis.persistAllIndices` setting affects it, and how you can configure it to optimize your development workflow.

## What Is Indexing in Pylance?

Indexing is the process by which Pylance scans your project's files and installed third-party libraries to build a database (indices) of symbols such as classes, functions, and variables. This enables features like:

- **Auto-import Suggestions**: Quickly import symbols from libraries without manually typing import statements.
- **Workspace Symbol Search**: Search for symbols across your project and libraries.

By default, Pylance indexes the top-level symbols of installed packages. However, indexing can be resource-intensive, especially in large projects or when using many third-party libraries.

## The `python.analysis.persistAllIndices` Setting

The `python.analysis.persistAllIndices` setting determines whether Pylance saves the indices for third-party libraries to disk. When enabled, Pylance will persist these indices between sessions, potentially improving performance by avoiding the need to re-index libraries each time you open your project.

### Accepted Values

- `true` (default): Pylance will save indices for all third-party libraries to disk and reuse them in future sessions.
- `false`: Pylance will not persist indices; it will re-index libraries upon each session.

### How to Change the Setting

To adjust this setting in Visual Studio Code:

1. **Open the Settings (JSON)**:

   - Open the Command Palette and select **Preferences: Open User Settings (JSON)** or **Preferences: Open Workspace Settings (JSON)**, depending on whether you want to apply the setting globally or per workspace.

2. **Add or Modify the Setting**:

   ```json
   "python.analysis.persistAllIndices": true
   ```

   - Setting it to `true` enables index persistence.
   - Setting it to `false` disables index persistence.

## When and Why to Enable `python.analysis.persistAllIndices`

### Benefits of Persisting Indices

- **Performance Improvement**: By persisting indices, Pylance doesn't need to re-index third-party libraries every time you open your project, leading to faster startup times.
- **Efficient Resource Utilization**: Reduces CPU and I/O usage on subsequent sessions since indexing large libraries can be resource-intensive.

### Ideal Scenarios for Enabling

- **Stable Dependencies**: If your project's dependencies don't change frequently, persisting indices ensures that Pylance always has up-to-date information without needing to re-index.
- **Large Projects**: In projects with a lot of third-party dependencies, indexing can take considerable time. Persisting indices mitigates this overhead.
- **Continuous Development**: For developers who open and close their projects frequently, persisting indices enhances productivity by reducing wait times.

### Potential Considerations

- **Disk Space Usage**: Persisted indices consume disk space. The amount depends on the size and number of third-party libraries.
- **Outdated Indices**: If you update or add new packages, the persisted indices might become outdated. In such cases, you may need to clear and regenerate the indices.
- **Corrupted Indices**: Although rare, indices can become corrupted, leading to unexpected behavior in Pylance.

### Clearing Persisted Indices

If you encounter issues due to outdated or corrupted indices, you can clear them:

1. Open the Command Palette.
2. Run the command:
   ```plaintext
   Pylance: Clear All Persisted Indices
   ```

This command deletes all persisted indices, and Pylance will re-index libraries the next time it's activated.

## Related Settings

- [`python.analysis.indexing`](python_analysis_indexing.md)
   - Determines whether Pylance should index user files and installed third-party libraries.
   - **Note**: If `indexing` is set to `false`, `persistAllIndices` has no effect because indices are not created.

- [`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md)
   - Configures the depth of indexing for specific packages.
   - **Note**: Increasing the index depth can improve auto-import suggestions but may impact indexing time and resource usage. When this setting is changed, indices need to be regenerated by clearing persisted indices. 

## Frequently Asked Questions

### Q: How about user file indices? Will `persistAllIndices` persist user file indices as well?

**A:** No, user file indices will be recalculated every time a new VS Code session starts, based on the [`userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md) setting. This setting only affects third-party package indices. Unlike third-party libraries, user files change frequently, so they need to be re-indexed often regardless of persistence, reducing the potential savings from persisting them.

### Q: What is the difference between `python.analysis.persistAllIndices` and [`python.analysis.indexing`](python_analysis_indexing.md)?

**A:** `python.analysis.indexing` controls whether Pylance performs indexing of user files and third-party libraries at all. When set to `false`, indexing is disabled, and features like auto-imports may be limited.

`python.analysis.persistAllIndices` controls whether the indices created during indexing are saved to disk and reused in future sessions. When set to `true`, Pylance saves the indices, improving performance on subsequent launches by avoiding re-indexing. If `python.analysis.indexing` is `false`, `python.analysis.persistAllIndices` has no effect because no indices are created.

### Q: How can I tell if persisted indices are causing issues?

**A:** If you notice incorrect auto-import suggestions, missing symbols, or unexpected behavior in code navigation, it might be due to outdated or corrupted persisted indices. Clearing the persisted indices can resolve these issues.

### Q: Will enabling `python.analysis.persistAllIndices` affect my project's performance?

**A:** Enabling this setting generally improves performance by reducing the time spent indexing on startup. However, the initial indexing process may take longer, and disk space usage will increase due to the saved indices.

### Q: Do I need to manually update indices after adding new packages?

**A:** Pylance should automatically detect changes in your environment. However, if you experience issues after adding or updating packages, you may need to clear and regenerate the indices using the **"Pylance: Clear All Persisted Indices"** command.

### Q: Is `python.analysis.persistAllIndices` enabled by default?

**A:** Yes, as of the latest versions, `python.analysis.persistAllIndices` is enabled by default (`true`). You need to disable it explicitly if you don't want to. Even if it is enabled, if VS Code cannot write indices to disk, they won't be persisted.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*


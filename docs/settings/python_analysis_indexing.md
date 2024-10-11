

# Understanding `python.analysis.indexing` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a powerful language server for Python in Visual Studio Code, offering advanced features like IntelliSense, type checking, auto-imports, and more. One of the key settings that influence Pylance's behavior is `python.analysis.indexing`.

This guide explains what the `python.analysis.indexing` setting is, how it affects Pylance's functionality, and how you can configure it to optimize your development experience.

## What is `python.analysis.indexing`?

The `python.analysis.indexing` setting in Pylance controls whether the language server should index your codebase and installed third-party libraries to enhance features like auto-import suggestions, `go to symbol` in the workspace, and code completion.

When indexing is enabled, Pylance scans your project's files and the libraries in your environment to build an index of available symbols. This index allows Pylance to provide more accurate and comprehensive suggestions, such as automatically importing modules or functions when you reference them in your code.

### Benefits of Indexing

- **Improved Auto-Imports**: With indexing, Pylance can suggest auto-imports for symbols that are not yet imported in your code nor opened in VS Code, saving you time and reducing errors.
- **Enhanced Code Navigation**: Indexing improves the performance of the `go to symbol` feature in the workspace, allowing it to find symbols across your entire codebase more efficiently, although the functionality will still work even if indexing is disabled.
- **Improved Code Generation**: Indexing can enhance generated code by automatically adding import statements for symbols used, streamlining the development process.

### Performance Considerations

While indexing offers significant benefits, it can also impact performance, especially in large projects or when working remotely with low system resources. Indexing involves scanning and analyzing files, which can consume CPU and memory resources.

## The `python.analysis.indexing` Setting

### Accepted Values

- `true` (default): Enables indexing of user files and installed third-party libraries.
- `false`: Disables indexing, reducing resource usage but limiting certain features.

### Default Value

- The default value is `true` when `python.analysis.languageServerMode` is set to `default`.
- In `light` language server mode, the default value is `false` to optimize for performance.

## How to Change the Setting

To adjust the `python.analysis.indexing` setting:

- Open **Settings** and search for `python.analysis.indexing`.
- Modify the setting as needed (enable or disable).

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line in your `settings.json` file:
  ```json
  "python.analysis.indexing": true
  ```

## When to Enable or Disable Indexing

### Enable Indexing

Enable indexing if you need advanced IntelliSense features, your project is small to medium-sized, or your system has enough resources. It enhances features like auto-imports, code completion, and code navigation.

### Disable Indexing

Disable indexing if you face performance issues, have limited resources, or are working on very large projects. Disabling it can improve editor responsiveness at the cost of some advanced features.

## What Does the Indexer Index?

The indexer creates two indices: one for user files (files that belong to the VS Code workspace) and one for third-party libraries.

- **User File Index**: This index includes files within the current workspace and is controlled by `python.analysis.userFileIndexingLimit`.
- **Third-Party Library Index**: This index covers third-party libraries installed in the environment and can be controlled using `python.analysis.packageIndexDepths`.

## Adjusting Indexing Behavior with Related Settings

To further customize indexing behavior in Pylance, you can use additional settings along with `python.analysis.indexing` to refine how indexing works:

- **[`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md)**: Allows you to control how deeply specific packages are indexed, providing flexibility in managing indexing performance.

- **`python.analysis.include`**: Specifies which directories or files belong to the VS Code workspace, which indirectly affects what files the indexer will process.

- **`python.analysis.exclude`**: Excludes specific directories or files from being part of the VS Code workspace, which affects what files the indexer will process.

- **`python.analysis.extraPaths`**: By default, the indexer will index packages in import roots returned by `sys.path`. If there are other packages or modules you want to include, use `extraPaths` to add them as third-party packages to the workspace, which will indirectly cause the indexer to index them.

- **`python.analysis.userFileIndexingLimit`**: Limits the number of user files to index, which can help manage performance on larger projects.

- **`python.analysis.persistAllIndices`**: Determines if third-party library indices are preserved across VS Code sessions. Note that user file indices are always re-indexed.

Using these settings together, you can tailor indexing to meet your specific development needs while balancing performance considerations.

## Frequently Asked Questions

### Q: How does indexing affect auto-import suggestions?

**A:** Indexing enables Pylance to scan your codebase and installed libraries for available symbols. With indexing enabled, Pylance can suggest auto-imports for symbols that were never opened or used in VS Code, making it easier to write and maintain code without manually adding import statements.

### Q: Will disabling indexing remove all IntelliSense features?

**A:** Disabling indexing keeps most IntelliSense features. Import suggestions for symbols in open files will still work, but auto-import for unused symbols may be limited, and workspace symbol search could be slower and use more memory.

### Q: I disabled indexing, but I'm still experiencing performance issues. What else can I do?

**A:** If performance issues persist after disabling indexing, consider taking a look at this wiki: [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code).

### Q: Can I control which files or libraries are indexed?

**A:** Yes, you can control indexing behavior using settings like `python.analysis.packageIndexDepths`, `python.analysis.include`, `python.analysis.exclude`, and `python.analysis.extraPaths`. These settings allow you to specify which directories or packages to include or exclude from indexing, and how deeply to index them.

### Q: How can I tell if indexing is causing performance issues?

**A:** If you notice high CPU usage, memory consumption, or sluggishness in the editor, indexing might be a contributing factor. Consider providing the information described here: [Collecting data for an investigation](https://github.com/microsoft/pylance-release/wiki/Collecting-data-for-an-investigation.).

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

---


# Understanding `python.analysis.languageServerMode` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

One of Pylance's configurable settings is **`python.analysis.languageServerMode`**, which allows you to optimize Pylance's performance based on your development needs.

This guide explains what `python.analysis.languageServerMode` is, how it affects Pylance's functionality, and how you can customize it to suit your preferences.

## What is `python.analysis.languageServerMode`?

The `python.analysis.languageServerMode` setting in Pylance offers predefined configurations to help users optimize Pylance's performance based on their development needs. It controls how many IntelliSense features Pylance provides, allowing you to choose between full language service functionality or a lightweight experience optimized for performance.

By adjusting this setting, you can strike a balance between the richness of features and the performance impact on your system.

### Accepted Values

- `default` (default value)
- `light`
- `full`

### Descriptions

- **`default`**: Provides a balanced experience with many useful features enabled by default. This mode ensures that Pylance delivers sufficient functionality for most users without overloading the system. Advanced features like full language analysis, indexing, and IntelliSense are enabled, allowing for a comprehensive development experience.

- **`light`**: Designed for users seeking a lightweight, memory-efficient setup. This mode disables various features to make Pylance function more like a streamlined text editor. It is ideal for those who do not require the full breadth of IntelliSense capabilities and prefer Pylance to be as resource-friendly as possible.

- **`full`**: Designed for users seeking the most extensive feature set. This mode enables most of Pylance's features, offering the richest IntelliSense experience. It is ideal for those who want access to the full range of available functionality. However, it will need a lot of resources, so it may not be suitable for very large projects or systems with limited hardware.

### Modifications to Default Settings

When you change the `python.analysis.languageServerMode` setting, Pylance automatically adjusts several other settings to match the selected mode. Below are the default values for each mode:

| Setting                                                  | `default` mode | `light` mode | `full` mode |
| -------------------------------------------------------- | -------------- | ------------ | ----------- |
| `python.analysis.exclude`                                | `[]`           | `["**"]`     | `[]`        |
| `python.analysis.useLibraryCodeForTypes`                 | `true`         | `false`      | `true`      |
| `python.analysis.enablePytestSupport`                    | `true`         | `false`      | `true`      |
| `python.analysis.indexing`                               | `true`         | `false`      | `true`      |
| `python.analysis.autoImportCompletions`                  | `false`        | `false`      | `true`      |
| `python.analysis.showOnlyDirectDependenciesInAutoImport` | `false`        | `false`      | `true`      |
| `python.analysis.userFileIndexingLimit`                  | `2000`         | `2000`       | `-1`        |
| `python.analysis.functionReturnTypes`                    | `false`        | `false`      | `true`      |
| `python.analysis.pytestParameters`                       | `false`        | `false`      | `true`      |
| `python.analysis.supportRestructuredText`                | `false`        | `false`      | `true`      |
| `python.analysis.supportDocstringTemplate`               | `false`        | `false`      | `true`      |
| `python.analysis.packageIndexDepths`                     | `default`      | `default`    | `full`      |

- **[`python.analysis.exclude`](python_analysis_exclude.md)**: Specifies paths to directories or files that Pylance should not include in the analysis. In `light` mode, it is set to `["**"]`, which means Pylance will exclude all files from the workspace, enabling IntelliSense support for open files only.

- **[`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md)**: When set to `true`, Pylance parses the source code of libraries when type stubs are not available. In `light` mode, this is set to `false`, reducing memory usage.

- **`python.analysis.enablePytestSupport`**: Enables Pytest-specific IntelliSense features. Disabled in `light` mode to reduce resource consumption.

- **[`python.analysis.indexing`](python_analysis_indexing.md)**: Indexes installed third-party libraries and user files to improve features like auto-imports and symbol searches. Disabled in `light` mode for performance optimization.

- **`python.analysis.autoImportCompletions`**: Controls the offering of auto-imports in completions. Enabled in `full` mode to provide a richer development experience.

- **`python.analysis.showOnlyDirectDependenciesInAutoImport`**: In `full` mode, only direct dependencies declared in `requirements.txt` or `pyproject.toml` are shown in auto-import suggestions, improving the relevance of suggestions.

- **`python.analysis.userFileIndexingLimit`**: Limits the number of user files indexed in the workspace. In `full` mode, there is no limit (`-1`), allowing comprehensive indexing of all files.

- **`python.analysis.functionReturnTypes`**: Enables inlay hints for function return types in `full` mode, providing additional type information during development.

- **`python.analysis.pytestParameters`**: Enables inlay hints for Pytest function parameters in `full` mode, enhancing test development support.

- **`python.analysis.supportRestructuredText`**: Enables support for reStructuredText in docstrings in `full` mode, allowing for richer documentation rendering.

- **`python.analysis.supportDocstringTemplate`**: Enables support for docstring generation in `full` mode, facilitating better code documentation.

- **[`python.analysis.packageIndexDepths`](python_analysis_packageIndexDepths.md)**: Used to override how many levels under installed packages to index on a per-package basis. By default, only top-level modules are indexed.

  - **Default value**:
    ```jsonc
    [
        { "name": "sklearn", "depth": 2 }, 
        { "name": "matplotlib", "depth": 2 }, 
        { "name": "scipy", "depth": 2 }, 
        { "name": "django", "depth": 2 }, 
        { "name": "flask", "depth": 2 }, 
        { "name": "fastapi", "depth": 2 }
    ]
    ```
    or in `full` mode
    ```jsonc
    [
        { "name": "", "depth": 4, "includeAllSymbols": true }
    ]
    ```

  In `full` mode, this ensures comprehensive indexing of submodules, improving features like auto-import and symbol searches for deeply nested packages. For more detail, please refer to the link above.

These settings can be individually customized to override the defaults for each mode.

## How to Change the Setting

1. **Open Settings**: Click on the gear icon in the lower-left corner of Visual Studio Code and select **Settings**.
2. **Search for the Setting**: Type `python.analysis.languageServerMode` in the search bar.
3. **Modify the Setting**: Choose `default`, `light`, or `full` from the dropdown menu.

Alternatively, you can edit your `settings.json` file directly:

1. **Open Settings (JSON)**: Open the command palette and type `Preferences: Open Settings (JSON)`.
2. **Add or Modify the Setting**:
   ```json
   "python.analysis.languageServerMode": "light"
   ```

## When and Why to Use Each Mode

- **`light`**

  - **Large Projects**: Improves performance by analyzing only open files, reducing resource usage.
  - **Limited Resources**: Suitable for systems with low memory or CPU power.
  - **Quick Edits**: Ideal if you don't need advanced features and just need a simple editor setup.

- **`default`**

  - **Balanced Performance**: Offers a good balance of features and performance, suitable for most users.
  - **General Development**: Ideal for regular Python development with IntelliSense and type checking features enabled by default.

- **`full`**

  - **Comprehensive Features**: Ideal for those who need access to the full range of IntelliSense and analysis features.
  - **High Resource Availability**: Suitable for systems with sufficient memory and CPU power to handle more extensive analysis.

## Frequently Asked Questions

### Q: What are the benefits and drawbacks of using `full` mode?

**A:** `Full` mode provides the most extensive set of features, including advanced IntelliSense, type checking, comprehensive indexing, and auto-imports. This mode is ideal if you need full language support, especially for complex projects. However, it requires a lot of system resources, such as memory and CPU power, which means it may not be suitable for very large projects or systems with limited hardware. If your system struggles with performance issues while using `full` mode, consider switching to `default` or `light` mode.

### Q: How does `light` mode affect existing projects and what features are disabled?

**A:** In `light` mode, Pylance does not analyze closed files, perform indexing, extract type information from library code, or provide Pytest support. This reduces resource usage but limits IntelliSense features like auto-import suggestions, workspace-wide code navigation, find all references, and multi-file rename. Editor features such as completion, hover, and go-to definition will still work, but third-party library symbols may be unavailable if stubs or type information are missing, which can also affect diagnostics.

### Q: Can I customize individual settings after switching to `light` mode?

**A:** Yes, you can individually override any of the settings adjusted by `languageServerMode`. For example, you can re-enable indexing or Pytest support by explicitly setting those configurations in your `settings.json`.

### Q: Is `light` mode suitable for all types of development?

**A:** `Light` mode is ideal for large projects, systems with limited resources, or when you require a lightweight editing experience. If you need comprehensive IntelliSense and code analysis across your entire workspace, `default` mode is recommended.

### Q: How do I know if I should switch to `light` mode?

**A:** If you experience performance issues, such as high memory or CPU usage, slow editor responses, or lag in IntelliSense features, trying `light` mode may help. You can monitor system performance and adjust settings as needed.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*
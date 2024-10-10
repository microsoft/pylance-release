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

### Descriptions

- **`default`**: Provides a balanced experience with many useful features enabled by default. This mode ensures that Pylance delivers sufficient functionality for most users without overloading the system. Advanced features like full language analysis, indexing, and IntelliSense are enabled, allowing for a comprehensive development experience.

- **`light`**: Designed for users seeking a lightweight, memory-efficient setup. This mode disables various features to make Pylance function more like a streamlined text editor. It is ideal for those who do not require the full breadth of IntelliSense capabilities and prefer Pylance to be as resource-friendly as possible.

### Modifications to Default Settings

When you change the `python.analysis.languageServerMode` setting, Pylance automatically adjusts several other settings to match the selected mode. Below are the default values for each mode:

| Setting                                  | `default` mode | `light` mode |
| ---------------------------------------- | -------------- | ------------ |
| `python.analysis.exclude`                | `[]`           | `["**"]`     |
| `python.analysis.useLibraryCodeForTypes` | `true`         | `false`      |
| `python.analysis.enablePytestSupport`    | `true`         | `false`      |
| `python.analysis.indexing`               | `true`         | `false`      |

- **`python.analysis.exclude`**: Specifies paths to directories or files that Pylance should not include in the analysis. In `light` mode, it is set to `["**"]`, which means Pylance will exclude all files from workspace, enabling IntelliSense support for open files only.

- **`python.analysis.useLibraryCodeForTypes`**: When set to `true`, Pylance parses the source code of libraries when type stubs are not available. In `light` mode, this is set to `false`, reducing memory usage.

- **`python.analysis.enablePytestSupport`**: Enables Pytest-specific IntelliSense features. Disabled in `light` mode to reduce resource consumption.

- **`python.analysis.indexing`**: Indexes installed third-party libraries and user files to improve features like auto-imports and symbol searches. Disabled in `light` mode for performance optimization.

These settings can be individually customized to override the defaults for each mode.

## How to Change the Setting

To adjust the `python.analysis.languageServerMode` setting in Visual Studio Code:

1. **Open the Settings**:

   - Click on the gear icon in the lower-left corner and select **Settings**.

2. **Search for the Setting**:

   - In the search bar at the top, type `python.analysis.languageServerMode`.

3. **Modify the Setting**:

   - Select your preferred mode (`default` or `light`) from the dropdown menu.

Alternatively, you can edit your `settings.json` file directly:

1. **Open Settings (JSON)**:

   - Open the command palette and type `Preferences: Open Settings (JSON)`.

2. **Add or Modify the Setting**:

   ```json
   "python.analysis.languageServerMode": "light"
   ```

## When and Why to Use `light` Mode

### Large Projects

Working with large codebases can strain system resources due to the extensive analysis required. Switching to `light` mode can improve performance by limiting Pylance's analysis to open files only.

### Limited System Resources

On systems with limited memory or CPU capabilities, such as older machines or those running many applications simultaneously, `light` mode can provide a smoother editing experience.

### Lightweight Editing

If you primarily use Visual Studio Code as a text editor for quick edits and do not require advanced IntelliSense features, `light` mode can simplify your setup.

### Performance Optimization

In scenarios where Pylance's resource consumption affects the responsiveness of the editor, adjusting to `light` mode can alleviate these issues.

## Practical Examples

### Example 1: Switching to `light` Mode for a Large Workspace

Suppose you're working on a sizable project with thousands of files, and you notice that Visual Studio Code becomes sluggish. You can switch to `light` mode to improve performance:

1. Open your `settings.json` file.

2. Add the following line:

   ```json
   "python.analysis.languageServerMode": "light"
   ```

3. Restart Visual Studio Code to apply the changes.

In `light` mode, Pylance will focus on providing IntelliSense and diagnostics for open files, reducing the load on your system.

### Example 2: Customizing Settings After Switching Modes

After switching to `light` mode, you might want to re-enable a specific feature that was disabled by default. For instance, if you still want Pylance to index your user files:

1. In your `settings.json`, add:
   ```json
   "python.analysis.languageServerMode": "light",
   "python.analysis.indexing": true
   ```

This overrides the default value for `python.analysis.indexing` in `light` mode, re-enabling indexing while keeping other optimizations.

## Frequently Asked Questions

### Q: What features are disabled when using `light` mode?

**A:** In `light` mode, Pylance disables workspace-wide analysis, indexing, type information extraction from library code, and Pytest support. This reduces resource usage but limits some IntelliSense features such as auto-import suggestions and code navigation across the workspace.

### Q: Can I customize individual settings after switching to `light` mode?

**A:** Yes, you can individually override any of the settings adjusted by `languageServerMode`. For example, you can re-enable indexing or Pytest support by explicitly setting those configurations in your `settings.json`.

### Q: Will switching to `light` mode affect my existing projects?

**A:** Switching to `light` mode will change how Pylance analyzes your code in all projects where the setting is applied. IntelliSense features may be limited, and some diagnostics may not appear.

### Q: Is `light` mode suitable for all types of development?

**A:** `Light` mode is ideal for large projects, systems with limited resources, or when you require a lightweight editing experience. If you need comprehensive IntelliSense and code analysis across your entire workspace, `default` mode is recommended.

### Q: How do I know if I should switch to `light` mode?

**A:** If you experience performance issues, such as high memory or CPU usage, slow editor responses, or lag in IntelliSense features, trying `light` mode may help. You can monitor system performance and adjust settings as needed.

---

*For more information on Pylance settings and customization, refer to the ****[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)**** documentation.*

---

*"This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness."*


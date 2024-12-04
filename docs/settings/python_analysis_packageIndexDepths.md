# Understanding `python.analysis.packageIndexDepths` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It offers advanced IntelliSense features, including type checking, auto-completions, and code navigation, enhancing your Python development experience.

One of Pylance's configuration settings is `python.analysis.packageIndexDepths`, which allows you to control how Pylance indexes third-party packages for features such as auto-imports and code completion.

This guide explains what `python.analysis.packageIndexDepths` does, how to use it effectively, and considerations when adjusting this setting.

## What Is `python.analysis.packageIndexDepths`?

By default, Pylance indexes only the top-level modules of installed third-party packages (depth = 1). This indexing behavior is a performance optimization, ensuring that Pylance operates efficiently, especially in large projects.

The `python.analysis.packageIndexDepths` setting allows you to override this default behavior by specifying the depth to which Pylance should index specific packages. Increasing the index depth enables Pylance to recognize deeper modules and symbols within a package, improving IntelliSense features like auto-import suggestions for those modules.

### Why Adjust Indexing Depth?

In some cases, you may notice that Pylance does not provide auto-import suggestions for certain submodules or symbols within a third-party package. This behavior occurs because those submodules are not included in the default index.

By adjusting the indexing depth for a package, you can include additional submodules and symbols, enhancing Pylance's ability to provide relevant suggestions.

## How to Use `python.analysis.packageIndexDepths`

The `python.analysis.packageIndexDepths` setting accepts a list of configurations, each specifying a package, the depth to which it should be indexed, and whether to include all symbols.

### Accepted Values and Structure

Each configuration in the list should be an object with the following properties:

- `"name"`: The name of the package (string).
- `"depth"`: The depth to which Pylance should index the package (integer).
- `"includeAllSymbols"` (optional): Whether to include all symbols in the indexing (boolean). If set to `false`, only symbols specified in a module's `__all__` attribute are included. Default is `false` if not specified.

**Note**: When you manually set the `python.analysis.packageIndexDepths` setting, the default indexing behavior is removed. This means you need to explicitly add any additional packages that you want indexed to this setting, even if you still want them indexed at the default depth.

#### Example Structure:

```json
{
  "name": "package_name",
  "depth": depth_to_scan,
  "includeAllSymbols": true_or_false
}
```

### How to Configure the Setting

To adjust the `packageIndexDepths` setting in Visual Studio Code:

1. **Open the Settings JSON**:

   - Open the Command Palette and select **Preferences: Open Settings (JSON)**.

2. **Add or Modify the Setting**:

   - Include the `python.analysis.packageIndexDepths` setting in your `settings.json` file:
     ```json
     "python.analysis.packageIndexDepths": [
       {
         "name": "package_name",
         "depth": depth_to_scan,
         "includeAllSymbols": true_or_false
       }
     ],
     ```

3. **Save and Reload**:

   - Save the `settings.json` file.
   - Reload Visual Studio Code for the changes to take effect.

**Note**: Adjusting the indexing depth may impact performance. It's recommended to specify only the packages you need and to set the minimum depth required.

### Understanding Index Depth

- **Depth**: The number of modules in the module path that Pylance should index.
  - **Depth 1**: Only the package's top-level modules are indexed (e.g., `django`).
  - **Depth 2**: Includes modules one level deeper (e.g., `django.core`).
  - **Depth 3**: Includes modules two levels deeper (e.g., `django.core.api`).&#x20;

    Note that the depth does not directly correspond to the directory structure. For example, `django.core` could be located in `django/core.py` or `django/core/__init__.py`.

### `includeAllSymbols`

- **`includeAllSymbols: false`** (default):

  - Pylance includes only symbols that are specified in a module's `__all__` attribute.
  - This helps reduce the number of irrelevant or private symbols in the index.

- **`includeAllSymbols: true`**:

  - Pylance includes all top-level symbols declared in the files, regardless of the `__all__` attribute.
  - Use this option if necessary symbols are not included due to missing `__all__` declarations.

## Performance Considerations

Adjusting the `python.analysis.packageIndexDepths` setting causes Pylance to allocate more resources for indexing third-party libraries. Indexing deeper levels or including all symbols increases the amount of data Pylance processes, which can lead to:

- **Increased Memory Usage**: More symbols and modules are loaded into memory.
- **Longer Indexing Times**: Initial indexing when starting VS Code may take more time.
- **Potential Impact on Responsiveness**: Large projects or extensive indexing may affect editor performance.

To mitigate performance impacts:

- Only specify packages where deeper indexing is necessary.
- Set the smallest `depth` value that includes the required modules.
- Avoid setting `includeAllSymbols` to `true` unless needed.

## Examples

### Example 1: Indexing a Package to a Specific Depth

Suppose you're working with the `django` package and need auto-import suggestions for modules within `django.core`.

```json
"python.analysis.packageIndexDepths": [
  {
    "name": "django",
    "depth": 3
  }
],
```

- **Explanation**: This setting tells Pylance to index `django` to a depth of 3, including `django` (depth 1), `django.core` (depth 2), and submodules within `django.core` (depth 3).

### Example 2: Including All Symbols in Indexing

If the package does not correctly export symbols via `__all__`, and you need all symbols indexed, you can set `includeAllSymbols` to `true`.

```json
"python.analysis.packageIndexDepths": [
  {
    "name": "rest_framework",
    "depth": 3,
    "includeAllSymbols": true
  }
],
```

- **Explanation**: This setting tells Pylance to index the `rest_framework` package to a depth of 3 and include all symbols. This can be useful if you're not getting auto-import suggestions for certain classes or functions within the package.

### Example 3: Setting Index Depth for Multiple Packages

You can specify multiple packages in the `packageIndexDepths` list.

```json
"python.analysis.packageIndexDepths": [
  {
    "name": "matplotlib",
    "depth": 2
  },
  {
    "name": "numpy",
    "depth": 2
  },
  {
    "name": "pandas",
    "depth": 2
  }
],
```

- **Explanation**: This configuration adjusts the indexing depth for `matplotlib`, `numpy`, and `pandas` to 2, enabling better auto-imports and auto-import suggestions for submodules within these packages.

### Example 4: Overriding Default Indexing for All Packages

If you want to change the indexing depth for all packages, you can set the `name` to an empty string `""`.

```json
"python.analysis.packageIndexDepths": [
  {
    "name": "",
    "depth": 3
  }
],
```

- **Explanation**: This setting adjusts the default indexing depth for all packages to 3. Use this cautiously, as it may significantly impact performance.

## Default Values for Each Language Server Mode

- Default value for `light` and `default` mode:
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
  or in `full` mode:
  ```jsonc
  [
      { "name": "", "depth": 4,  "includeAllSymbols": true }
  ]
  ```

## Frequently Asked Questions

### Q: How do I know what depth to set for a package?

**A:** The depth depends on how deep the modules or symbols you need are within the package's directory structure. Start with a depth of 2 or 3 and increase if necessary. Be mindful of performance impacts when setting higher depths.

### Q: What happens to the default `packageIndexDepth` when I manually set the depth?

**A:** When you manually set the `python.analysis.packageIndexDepths` setting, the default indexing behavior is overridden. Therefore, you need to explicitly add any packages that you want indexed to this setting, even if you still want them indexed at the default depth. Make sure to include all required packages in the configuration to avoid losing indexing capabilities for important packages.

### Q: Can I enable this setting for specific files or projects?

**A:** Currently, the `python.analysis.packageIndexDepths` setting applies globally or per-workspace in VS Code settings. You can adjust the setting in your workspace's `settings.json` to enable it for a specific project.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*"This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness."*

---

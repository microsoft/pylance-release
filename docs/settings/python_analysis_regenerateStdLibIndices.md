# Understanding `python.analysis.regenerateStdLibIndices` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

To deliver fast and accurate code completions, Pylance pre-builds an index of the standard library (stdlib) for quick reference. However, discrepancies can occur if the prebuilt indices do not match the specific Python version or platform you are using.

The `python.analysis.regenerateStdLibIndices` setting addresses this issue by allowing Pylance to regenerate the standard library indices specific to your workspace, ensuring that code suggestions and completions align with your Python version and platform.

This guide explains the purpose of `python.analysis.regenerateStdLibIndices`, how to use it, and how it can improve your development experience with Pylance.

## What Are Standard Library Indices in Pylance?

Pylance uses indices to provide fast and accurate code completions, auto-import suggestions, and symbol searches. For the Python standard library, Pylance ships with prebuilt indices, which enables it to offer these features without the overhead of indexing the standard library every time you open a workspace.

### The Challenge with Prebuilt Indices

While prebuilt indices improve performance, they are built assuming the latest Python version and may not account for differences in older Python versions or platform-specific modules. This can lead to situations where Pylance suggests imports or code completions for modules or functions that are not available in your configured Python version.

### Example Scenario

Consider the following code using the `override` decorator introduced in Python 3.12:

```python
class A:
    def method(self):
        pass

class B(A):
    @override
    def method(self):
        pass
```

If your project targets Python 3.11, Pylance might still suggest importing `override` from `typing` (which is only available in Python 3.12+) because the prebuilt indices assume the latest Python version.

## The `python.analysis.regenerateStdLibIndices` Setting

The `python.analysis.regenerateStdLibIndices` setting allows Pylance to regenerate the standard library indices specific to your workspace's Python version and platform. By enabling this setting, Pylance creates indices that accurately reflect the modules and functions available in your configured Python environment.

### How to Enable `python.analysis.regenerateStdLibIndices`

To enable this setting in Visual Studio Code:

1. **Open the Settings**:

   - Click on the gear icon in the lower-left corner and select **Settings**.

2. **Search for the Setting**:

   - In the search bar at the top, type `python.analysis.regenerateStdLibIndices`.

3. **Modify the Setting**:

   - Check the box to set it to `true`, enabling the regeneration of standard library indices.

Alternatively, you can edit your `settings.json` file directly:

1. **Open Settings (JSON)**:

   - Click on the gear icon in the lower-left corner and select **Settings**.
   - Click on the **Open Settings (JSON)** icon in the upper-right corner.

2. **Add the Setting**:

   - Add or modify the following line in your `settings.json` file:
     ```json
     "python.analysis.indexOptions": {
         "regenerateStdLibIndices": true
     }
     ```

### Note on Performance

Regenerating the standard library indices can take a few seconds when you open a workspace, depending on your machine's performance. The indices are generated per workspace and are not shared across projects. However, this ensures that Pylance provides accurate code completions and suggestions for your specific Python version and platform.

## Benefits of Regenerating Standard Library Indices

- **Accurate Code Completions**: Ensures that Pylance only suggests modules and functions available in your Python version.
- **Correct Auto-Imports**: Prevents Pylance from suggesting imports that may not exist in your environment, reducing runtime errors.
- **Platform-Specific Modules**: Accounts for differences between platforms (e.g., Windows, Linux) where certain standard library modules may vary.

## Limitations and Considerations

- **Workspace-Specific**: The indices are regenerated per workspace. If you work with multiple projects, you need to ensure the setting is enabled in each workspace.
- **Initial Delay**: There may be a delay when opening a workspace as Pylance regenerates the indices.
- **Persistence of Indices**: With [`persistAllIndices`](python_analysis_persistAllIndices.md) settings, this can be persisted to disk and happen only once. Otherwise, it will happen every time for a new session.

## Related Settings

- [`python.analysis.indexing`](python_analysis_indexing.md) 
   - Used to specify whether Pylance should index installed third party libraries and user files to improve features such as auto-import, add import, workspace symbols, etc.
- [`python.analysis.persistAllIndices`](python_analysis_persistAllIndices.md)
   - Determines if third-party library indices are preserved across VS Code sessions.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

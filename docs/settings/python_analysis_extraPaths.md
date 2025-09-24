# Understanding `python.analysis.extraPaths` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It enhances your Python development experience with advanced features like type checking, auto-completions, and code navigation.

One common challenge developers encounter is unresolved import warnings or missing IntelliSense for custom modules stored in non-standard locations. The `python.analysis.extraPaths` setting in Pylance addresses this by allowing you to specify additional directories for Pylance to include when resolving imports. This ensures your custom modules are recognized and eliminates related warnings.

## Understanding Import Resolution in Python and Pylance

### Python's Import Mechanism

When importing a module in Python, the interpreter searches for the module in directories listed in `sys.path`. By default, these include:

- The directory containing the script used to invoke the interpreter.
- The Python standard library and `site-packages` directories.

```python
import sys
print(sys.path)
```

Custom directories are not included in `sys.path` unless explicitly added via runtime modifications or the `PYTHONPATH` environment variable.

### Pylance's Import Resolution

Pylance mimics Python's import mechanism for static code analysis, enabling IntelliSense features. However, it relies on Visual Studio Code settings and may not recognize modules in non-standard locations without additional configuration. Consequently, you might see warnings like:

```
Import "my_module" could not be resolved Pylance(reportMissingImports)
```

This impacts IntelliSense features like autocompletion, "go to definition," and error checking, even if the code runs correctly.

## What is `python.analysis.extraPaths`?

The `python.analysis.extraPaths` setting informs Pylance of additional directories to consider when resolving imports. Adding paths to this setting eliminates unresolved import warnings and ensures full IntelliSense support for custom modules.

### Key Features

- **Purpose**: Adds directories to Pylance's module search paths, mirroring the effect of modifying `sys.path` in Python.
- **Use Cases**: Resolving imports for modules stored outside standard directories or in complex project structures.

### How to Configure `python.analysis.extraPaths`

#### Using the Settings Editor

1. Open **File > Preferences > Settings**.
2. Search for `python.analysis.extraPaths`.
3. Add the paths to your custom module directories.

#### Editing `settings.json` Directly

1. Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
2. Add the following to `settings.json`:

    ```json
    {
        "python.analysis.extraPaths": ["./src", "./lib"]
    }
    ```

### Path Specifications

- **Relative Paths**: Interpreted relative to the workspace root.
- **Absolute Paths**: Supported but less portable.

Example:

```json
{
    "python.analysis.extraPaths": ["./libs/", "${workspaceFolder}/common/"]
}
```

## Examples

### Example 1: Adding a Local Module Directory

**Project Structure**:

```
project/
├── .vscode/
│   └── settings.json
├── main.py
└── modules/
    ├── __init__.py
    └── my_module.py
```

**Issue**:

Importing `my_module` in `main.py` results in an unresolved import warning:

```python
from my_module import my_function  # Unresolved import
```

**Solution**:

Add `modules` to `python.analysis.extraPaths`: This will make `modules` a top-level import root, allowing `my_module` to be imported directly instead of requiring `import modules.my_module`.

```json
{
    "python.analysis.extraPaths": ["./modules"]
}
```

### Example 2: Working with a `src` Directory

**Project Structure**:

```
project/
├── .vscode/
│   └── settings.json
├── src/
│   ├── package/
│   │   ├── __init__.py
│   │   └── utils.py
│   └── main.py
```

**Issue**:

Pylance cannot resolve imports from `src/package` in `main.py`:

```python
from package.utils import helper_function  # Unresolved import
```

**Solution**:

Add `src` to `python.analysis.extraPaths`:

```json
{
    "python.analysis.extraPaths": ["./src"]
}
```

## Best Practices

### When to Use `python.analysis.extraPaths`

- For custom project structures, such as monorepos.
- When modules are stored outside standard directories.
- For editable installations (`pip install -e`) not recognized by Pylance.

### Avoiding Common Issues

- **Use Relative Paths**: Maintain portability across environments.
- **Document Configurations**: Ensure consistency across team members.

### Benefits

- Eliminates import warnings.
- Enhances IntelliSense features, improving productivity.
- Reduces confusion from unresolved imports.

## FAQs

### Can I use environment variables like `${workspaceFolder}`?

It is supported and it can be used in multi root workspace in vscode so one workspace root can see other roots and import them.

### Can I use wildcards or globs like `./src/**/foo/*`?

No wildcards or globs are not supported. For two reasons:

- Extra paths make every lookup of every import take longer. Wildcard imports would have a high impact on this lookup that are not easy for the user to understand why they're taking so long.
- Wildcards make the lookup order non-deterministic. Lookup needs to be deterministic for finding a python file otherwise what works on one machine may not match another. 

### How does this differ from modifying `sys.path`?

`python.analysis.extraPaths` only affects Pylance's static analysis. It does not alter `sys.path` or runtime behavior. If your code modifies `sys.path` at runtime, static analysis tools like Pylance cannot detect these changes beforehand. This is a scenario where `extraPaths` becomes useful, as it informs Pylance about such dynamic behaviors explicitly.

### Does this setting affect virtual environments?

`extraPaths` supplements the selected interpreter's `sys.path`, ensuring static analysis recognizes additional directories.

## Related Documentation

For additional guidance on managing large workspaces, refer to the [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code#manually-configure-your-workspace) guide.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference#_python-languag-server-settings)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*


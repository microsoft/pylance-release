# Understanding `python.analysis.extraPaths` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker. It enhances your Python development experience with advanced features like type checking, auto-completions, and code navigation.

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

### Glob Patterns

Entries may contain glob wildcards, which are expanded to the matching directories:

- `*` — any characters within a single path segment (`packages/*/src`)
- `**` — any number of path segments (`external/**/site-packages`)
- `?` — a single character

Matches are added in a deterministic, sorted order, so the expanded list is identical on every machine. Only directories are matched; a glob never adds a file. For the full behavior, precedence rules, worked examples, and performance guidance, see [How to Use Glob Patterns in Extra Paths with Pylance](../howto/extra-paths-glob-resolution.md).

Example:

```json
{
    "python.analysis.extraPaths": ["./packages/*/src", "external/rules_python~~pip~pip_310_*/site-packages"]
}
```

For `extraPaths`, path validity means more than "the directory exists".

- Each entry should point to an import root that belongs on `sys.path`.
- Relative paths in VS Code settings resolve from the workspace root.
- If you set `extraPaths` in `pyrightconfig.json`, those paths resolve from the config file location instead.

An existing but wrong directory can still leave imports unresolved. A common mistake is pointing to the package directory itself when the import needs the package's parent directory.

For example, if your code imports `package.utils`, `extraPaths` should usually include the directory that contains `package/`, not `package/` itself.

For a broader checklist that also covers `stubPath`, `typeshedPaths`, `include`, `exclude`, and `ignore`, see [How to Troubleshoot Pylance Settings](../howto/settings-troubleshooting.md#validate-path-based-settings).

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
- **Use the Correct Import Root**: Add the directory that should be on `sys.path`, not just a nested folder with a similar name.
- **Document Configurations**: Ensure consistency across team members.

### Benefits

- Eliminates import warnings.
- Enhances IntelliSense features, improving productivity.
- Reduces confusion from unresolved imports.

## FAQs

### Can I use environment variables like `${workspaceFolder}`?

It is supported and it can be used in multi root workspace in vscode so one workspace root can see other roots and import them.

### Can I use wildcards or globs like `./src/**/foo/*`?

Yes. Glob patterns (`*`, `**`, `?`) in `extraPaths` are expanded to the matching directories. This was historically unsupported for two reasons — lookup cost and non-deterministic order — and both are now addressed:

- **Deterministic order**: matched directories are sorted with a case-sensitive, platform-independent comparison, and precedence is fixed (an explicit entry beats a glob-discovered duplicate; an earlier glob beats a later one). The expanded list is identical on every machine.
- **Performance**: expansion happens once when configuration loads, not on every import. The lookup cost still grows with how many directories a glob matches, so keep globs specific.

For the full behavior, worked examples, and performance guidance, see [How to Use Glob Patterns in Extra Paths with Pylance](../howto/extra-paths-glob-resolution.md).

### How does this differ from modifying `sys.path`?

`python.analysis.extraPaths` only affects Pylance's static analysis. It does not alter `sys.path` or runtime behavior. If your code modifies `sys.path` at runtime, static analysis tools like Pylance cannot detect these changes beforehand. This is a scenario where `extraPaths` becomes useful, as it informs Pylance about such dynamic behaviors explicitly.

### Does this setting affect virtual environments?

`extraPaths` supplements the selected interpreter's `sys.path`, ensuring static analysis recognizes additional directories.

## Related Settings

- [`python.analysis.autoSearchPaths`](python_analysis_autoSearchPaths.md): Automatically adds common source directories like `src/` to the search path.
- [`python.analysis.include`](python_analysis_include.md): Controls which files are included in analysis.
- [`python.analysis.stubPath`](python_analysis_stubPath.md): Directory for custom type stubs.

## See Also

- [How to Use Glob Patterns in Extra Paths with Pylance](../howto/extra-paths-glob-resolution.md) — wildcard syntax, deterministic ordering, and performance
- [How to Fix Unresolved Import Errors](../howto/unresolved-imports.md) — troubleshooting import resolution
- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — using `extraPaths` in multi-package projects
- [How to Work with Editable Installs](../howto/editable-installs.md) — `extraPaths` as a fallback for editable installs
- [How to Troubleshoot Settings](../howto/settings-troubleshooting.md) — precedence rules when `pyrightconfig.json` overrides `extraPaths`

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference#_python-languag-server-settings)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

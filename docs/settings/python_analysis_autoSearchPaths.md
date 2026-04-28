# Understanding `python.analysis.autoSearchPaths` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

Managing import paths in Python projects can sometimes be challenging, especially in larger projects with complex directory structures. Pylance offers the `python.analysis.autoSearchPaths` setting to help streamline this process by automatically adding certain directories to the import search path.

This guide explains what `python.analysis.autoSearchPaths` does, how it affects your project, and how you can configure it to suit your needs.

## What Is `python.analysis.autoSearchPaths`?

The `python.analysis.autoSearchPaths` setting controls whether Pylance automatically adds a `src` directory to the import search paths used for module resolution. When enabled, Pylance checks for a `src` directory at the root of your workspace and, if it meets certain conditions, includes it as an extra search path — without requiring you to configure [`python.analysis.extraPaths`](python_analysis_extraPaths.md) manually.

## How Does It Work?

When `python.analysis.autoSearchPaths` is set to `true`, Pylance checks for a directory named `src` at the root of your workspace. If it finds one and the following conditions are met, it adds this directory to the module search paths:

- **Directory name**: Must be `src`, located at the workspace root.
- **No `__init__.py`**: The `src` directory must **not** contain an `__init__.py` file at its root. If `__init__.py` is present, `src` is treated as a Python package rather than a search path root.

### Effect on Imports

With `autoSearchPaths` enabled and a qualifying `src/` directory present, you can write imports relative to `src/` without additional configuration.

**Example project structure**:

```
my_project/
├── src/
│   ├── module_a.py
│   └── package/
│       └── module_b.py
└── main.py
```

In `main.py`, you can import directly:

```python
from module_a import some_function
from package.module_b import helper
```

Without `autoSearchPaths`, Pylance would flag these as unresolved imports because it wouldn't know to look inside `src/`.

## The `python.analysis.autoSearchPaths` Setting

### Accepted Values

- `true` (default): Enables automatic addition of the `src` directory to search paths.
- `false`: Disables automatic search paths. You manage all import paths manually through [`extraPaths`](python_analysis_extraPaths.md) or config files.

### Default Value

The default value is `true`.

## How to Change the Setting

To adjust `python.analysis.autoSearchPaths`:

- Open **Settings** and search for `python.analysis.autoSearchPaths`.
- Toggle the setting on or off.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)\*\*, and select it.
- Add or update the following line:
    ```json
    "python.analysis.autoSearchPaths": false
    ```

## Interaction with Other Settings

### Combined with `extraPaths`

The auto-detected `src/` path and any manually specified [`extraPaths`](python_analysis_extraPaths.md) are **additive** — they are combined, not mutually exclusive. Setting `extraPaths` does not override the auto-detected `src/` directory.

### Execution Environments

When execution environments are defined in a `pyrightconfig.json` file, the auto-detected `src/` path applies only to the **default** execution environment. It does **not** automatically apply to explicitly defined execution environments. Add `src` to each environment's `extraPaths` if needed:

```json
{
    "executionEnvironments": [
        {
            "root": "packages/api",
            "extraPaths": ["../../src"]
        }
    ]
}
```

## Limitations

- **Only `src/`**: Only a directory named `src` at the workspace root is auto-detected. Other directory names (e.g., `lib`, `source`, `app`) require manual configuration via [`extraPaths`](python_analysis_extraPaths.md).
- **No nested directories**: Nested `src/` directories (e.g., `packages/core/src/`) are not auto-detected.
- **`__init__.py` changes behavior**: If `src/` contains `__init__.py`, it is treated as a package rather than a search path root. Imports would then require `from src.module_a import ...`.

## Frequently Asked Questions

### Q: Why isn't my `src` directory being automatically included?

**A:** Ensure that:

- `python.analysis.autoSearchPaths` is set to `true`
- The `src` directory is at the workspace root
- There is no `__init__.py` file in the `src` directory

### Q: Can I auto-detect directories other than `src`?

**A:** No. `autoSearchPaths` only detects `src/`. For other directories, use [`python.analysis.extraPaths`](python_analysis_extraPaths.md).

### Q: Does this setting affect runtime behavior?

**A:** No. `autoSearchPaths` only affects Pylance's analysis within VS Code. It does not modify `sys.path` at runtime. To ensure your code runs correctly, you may need to adjust `PYTHONPATH` or configure your build tool.

## Related Settings

- [`python.analysis.extraPaths`](python_analysis_extraPaths.md): Manually add directories to the import search path. Additive with `autoSearchPaths`.
- [`python.analysis.stubPath`](python_analysis_stubPath.md): Directory containing custom type stubs.

## See Also

- [How to Fix Unresolved Import Errors](../howto/unresolved-imports.md) — how `autoSearchPaths` fits into import resolution
- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — `autoSearchPaths` behavior with `src/` layouts
- [How to Troubleshoot Settings](../howto/settings-troubleshooting.md) — `autoSearchPaths` with execution environments

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

# Pylance Frequently Asked Questions

## General Questions

### What is the relationship between Pylance, Pyright and the Python extension?
Pylance is a language server, which provides features like IntelliSense, logical linting (e.g., errors and warnings), code actions, code navigation, semantic colorization, etc. Pyright is the open-source type checker which Pylance uses under the hood to provide its functionality. Pylance provides a superset of Pyright's functionality. To use Pylance, you must have the core Python extension installed in Visual Studio Code as it builds upon that experience.

### What features are in Pylance but not in Pyright? What is the difference exactly?
Pylance has a handful of valuable features that are not available in Pyright, including semantic highlighting, refactoring code actions (extract variable/extract method), docstrings for built-in/standard library modules, and IntelliCode compatibility. Pylance also ships with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking.

### How do I enable automatic docstring template generation?
Pylance includes built-in support for automatic docstring template generation. To enable this feature:
1. Open Settings (File > Preferences > Settings)
2. Search for `python.analysis.supportDocstringTemplate`
3. Enable the setting

Once enabled, typing `"""` inside a function, class, or method will automatically generate a docstring template with parameters, return types, and other sections. Pylance supports multiple popular formats including Google style, NumPy style, and Sphinx style.

For more details, see the [supportDocstringTemplate documentation](docs/settings/python_analysis_supportDocstringTemplate.md).

**Note:** This feature is enabled by default in `full` language server mode. You can also use the autoDocstring extension for additional customization options.

### Are there any plans to open-source Pylance in the future?
Because we have plans to include Pylance in Microsoft products outside of VS Code that do not have the same license, business models and/or are closed-source (for example, fully managed products and services), we do not currently have plans to open-source Pylance.

However, a substantial portion of Pylance's source code is open source via the [Pyright type checker](https://github.com/microsoft/pyright). We welcome contributions via that repository, and feedback on Pylance via our [pylance-release repo](https://github.com/microsoft/pylance-release).

### Can I load Pylance in Code – OSS?
Pylance is licensed for use in Microsoft products and services only, so can only be used on official Microsoft builds of Visual Studio Code and GitHub Codespaces.

### What telemetry and user data do you collect? Can I opt out?
You can read about how we collect and use telemetry, including how to disable it, [here](https://code.visualstudio.com/docs/getstarted/telemetry).

## Installation and Setup

### How do I install Pylance?
Pylance comes bundled as an optional dependency with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Simply install the Python extension from the VS Code marketplace, and Pylance will be installed automatically. Open any Python (.py) file to activate it.

### What is the minimum VS Code version required for Pylance?
Pylance requires VS Code version 1.57 or above.

### How do I switch to Pylance from another language server?
If you've previously set a different language server, update your `settings.json` file with: `"python.languageServer": "Pylance"` or `"python.languageServer": "Default"`. You can also use the Settings Editor UI to make this change.

## Configuration and Performance

### What are the different language server modes (light/default/full)?
Pylance offers three predefined modes via the `python.analysis.languageServerMode` setting:

- **`default`**: Balanced experience with many useful features enabled. Suitable for most users.
- **`light`**: Lightweight, memory-efficient setup with fewer features. Ideal for resource-constrained environments or when you prefer minimal IntelliSense.
- **`full`**: Most extensive feature set with all capabilities enabled. Provides the richest IntelliSense experience but uses more resources.

You can override individual settings regardless of which mode you choose.

### Why is Pylance using so much memory?
Large projects can cause Pylance to use significant memory. To reduce memory usage:

1. **Use `light` mode**: Set `"python.analysis.languageServerMode": "light"` in settings.json
2. **Exclude unnecessary files**: Add `"python.analysis.exclude": ["**/testFiles/*.py", "**/node_modules/**"]` to exclude files you don't need analyzed
3. **Use `openFilesOnly` diagnostic mode**: Set `"python.analysis.diagnosticMode": "openFilesOnly"` to only analyze open files
4. **Provide a custom Node.js executable**: Set `"python.analysis.nodeExecutable": "auto"` to use a version without memory limits (see [TROUBLESHOOTING.md](TROUBLESHOOTING.md#pylance-is-crashing) for details)

### What's the difference between `diagnosticMode` settings?
- **`openFilesOnly`** (default): Only analyzes files you have open in the editor. Faster and uses less memory.
- **`workspace`**: Analyzes all Python files in your workspace. Finds more issues but uses more resources.

### What type checking modes are available?
Pylance offers four type checking modes via `python.analysis.typeCheckingMode`:

- **`off`** (default): No type checking analysis; only shows unresolved imports/variables
- **`basic`**: Basic type checking rules
- **`standard`**: Standard type checking rules (more strict)
- **`strict`**: Strictest type checking with all rules enforced

Note: This can be overridden by `pyrightconfig.json` or `pyproject.toml` configuration files.

## Import and Module Resolution

### Why do I get "Import X could not be resolved" warnings?
This usually happens for one of these reasons:

1. **Package not installed**: Install the package using `pip install package-name`
2. **Wrong Python environment**: Ensure VS Code is using the correct Python interpreter (check the bottom-left status bar)
3. **Custom project structure**: If you have a `sources` or custom directory structure, add it to `python.analysis.extraPaths`:
   ```json
   {
       "python.analysis.extraPaths": ["./sources", "./my_custom_dir"]
   }
   ```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#unresolved-import-warnings) for more details.

### How do I configure Pylance to find my own modules?
Create a `.vscode/settings.json` file in your workspace and add the directories containing your modules to `python.analysis.extraPaths`:

```json
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

Relative paths are relative to the workspace root. The `src` directory is automatically detected, so no configuration is needed for standard `src` layouts.

### Why can't Pylance find my editable install modules?
Pylance requires editable installs to use `.pth` files rather than import hooks. Configure your package manager to use path-based editable installs:

- **pip/setuptools**: Use compat mode or strict mode (see setuptools documentation)
- **uv**: Add `config-settings = { editable_mode = "compat" }` to `[tool.uv]` in pyproject.toml
- **Hatchling**: Uses path-based `.pth` files by default
- **PDM**: Uses path-based `.pth` files by default

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#editable-install-modules-not-found) for detailed instructions.

## Virtual Environments and Interpreters

### How do I select the correct Python interpreter?
Click on the Python version in the bottom-left status bar of VS Code, or use the command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and search for "Python: Select Interpreter". Choose the interpreter from your virtual environment.

### Does Pylance work with conda environments?
Yes, Pylance works with conda environments. Make sure to select the conda environment's Python interpreter using the Python extension's interpreter selector.

### Does Pylance work with Poetry, pipenv, or other virtual environment managers?
Yes, Pylance works with all virtual environment managers. Just ensure you've selected the correct Python interpreter from your virtual environment in VS Code.

## Framework and Tool Integration

### Does Pylance work with Jupyter Notebooks?
Yes, Pylance has native Jupyter Notebooks compatibility. Open any `.ipynb` file in VS Code and Pylance will provide IntelliSense and type checking within notebook cells.

### Does Pylance support pytest?
Yes, Pylance has pytest support enabled by default in `default` and `full` modes. You can explicitly enable it with `"python.analysis.enablePytestSupport": true`.

### How do I configure Pylance for Django projects?
For Django projects, you may need to add your Django app directories to `python.analysis.extraPaths` if you encounter import resolution issues. Also consider creating type stubs for Django-specific features that might not be fully typed.

## Troubleshooting

### Pylance is not starting or shows an error on startup
Ensure you're running an official build of VS Code (not VS Codium or other variants). Pylance only works with official VS Code builds and GitHub Codespaces. If the problem persists, check the Output panel (View > Output > Python Language Server) for error messages.

### Why are packages not resolving when using WSL?
When using Pylance with WSL (Windows Subsystem for Linux), make sure your workspace is located under a WSL folder (`/home/...`) and not on a Windows-shared path (`/mnt/...`). See [issue #1443](https://github.com/microsoft/pylance-release/issues/1443#issuecomment-867863124) for more details.

### How do I disable specific diagnostic rules?
You can disable specific diagnostics in your `settings.json` or `pyrightconfig.json`. For example:

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedVariable": "none",
        "reportGeneralTypeIssues": "warning"
    }
}
```

See the [diagnostics documentation](docs/diagnostics/) for a full list of available diagnostic rules.

### How do I report issues or get help?
Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first for common issues. If your problem isn't covered, file an issue on the [pylance-release repository](https://github.com/microsoft/pylance-release/issues) with logs (enable with `"python.analysis.logLevel": "Trace"`) and a code example to reproduce the issue.

## Advanced Configuration

### Can I use a custom type stub directory?
Yes, you can specify custom type stub directories using `python.analysis.stubPath` in your settings.json. By default, Pylance looks for stubs in a `typings` directory in your workspace root.

### How do I configure Pylance with pyrightconfig.json or pyproject.toml?
Pylance respects configuration in `pyrightconfig.json` or the `[tool.pyright]` section of `pyproject.toml`. These files allow you to configure type checking behavior, include/exclude paths, and more. See the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md) for details.

### Can I use Pylance in a multi-root workspace?
Yes, Pylance has native multi-root workspace support. Place `.vscode/settings.json` in the root directory of each workspace for workspace-specific configuration.

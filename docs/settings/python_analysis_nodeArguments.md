# Understanding `python.analysis.nodeArguments` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.nodeArguments` setting lets you pass extra command-line arguments to the Node.js process that runs Pylance. This is useful for tuning memory limits or enabling Node.js diagnostics.

## What is `python.analysis.nodeArguments`?

When [`python.analysis.nodeExecutable`](python_analysis_nodeExecutable.md) is set (to `"auto"` or a custom path), Pylance launches a separate Node.js process for the language server. `nodeArguments` controls the arguments passed to that process.

**Default value**: `["--max-old-space-size=8192"]` (8 GB heap limit)

## Configuring `python.analysis.nodeArguments`

### Increase the heap limit for very large projects

If 8 GB is not enough (e.g., large monorepos with many workspace folders):

```json
{
    "python.analysis.nodeExecutable": "auto",
    "python.analysis.nodeArguments": ["--max-old-space-size=16384"]
}
```

This sets the V8 heap limit to 16 GB.

### Use the default heap limit

To restore the default:

```json
{
    "python.analysis.nodeArguments": ["--max-old-space-size=8192"]
}
```

Or remove the setting entirely.

## Important Considerations

- **Requires `nodeExecutable`**: `nodeArguments` only takes effect when `python.analysis.nodeExecutable` is set to `"auto"` or a custom Node.js path. When Pylance uses VS Code's bundled Node.js, this setting is ignored.

- **Scope**: This is a **machine-scoped** setting. It cannot be set in workspace or folder settings (`.vscode/settings.json`) for security reasons.

- **Restart required**: Changing this setting requires restarting VS Code (or reloading the window).

- **Memory vs. system RAM**: Don't set `--max-old-space-size` higher than your available physical RAM. Exceeding physical RAM causes swapping, which degrades performance.

## When to Use `python.analysis.nodeArguments`

| Scenario                                             | Recommended Value                |
| ---------------------------------------------------- | -------------------------------- |
| Default (most projects)                              | `["--max-old-space-size=8192"]`  |
| Large monorepo (>10 packages, workspace diagnostics) | `["--max-old-space-size=16384"]` |
| Memory-constrained machine (<8 GB RAM)               | `["--max-old-space-size=4096"]`  |

## Related Settings

- [`python.analysis.nodeExecutable`](python_analysis_nodeExecutable.md) — specifies the Node.js executable for Pylance
- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md) — reduces memory usage by limiting features
- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md) — `"openFilesOnly"` reduces memory by analyzing fewer files

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

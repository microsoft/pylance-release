# Understanding `python.analysis.logLevel` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.logLevel` setting controls how much detail Pylance writes to its Output panel.

## What is `python.analysis.logLevel`?

Pylance logs information about its activity — startup, environment detection, indexing, and analysis — to the **Output** panel. `logLevel` sets the verbosity of that log.

**Type**: `string`
**Default**: `"Information"`
**Scope**: window (applies to the whole VS Code window)

### Accepted values

| Value           | Description                                                                                        |
| --------------- | -------------------------------------------------------------------------------------------------- |
| `"Error"`       | Logs only errors.                                                                                  |
| `"Warning"`     | Logs warnings and errors.                                                                          |
| `"Information"` | Logs general informational messages, warnings, and errors. This is the default.                    |
| `"Trace"`       | Logs highly detailed diagnostic output, including the messages above. Useful when troubleshooting. |

This setting exists so you can increase verbosity when diagnosing a problem (for example, why a library is not resolving) and reduce it again for normal use.

## How to Change `python.analysis.logLevel`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.logLevel`.
3. Choose a value from the dropdown.

### Using `settings.json`

```json
{
    "python.analysis.logLevel": "Trace"
}
```

To view the log, open the **Output** panel (**View > Output**) and select **Python Language Server** from the dropdown.

## When to Use It

- **Use `"Trace"`** when troubleshooting an issue or preparing a bug report, to capture detailed diagnostic information.
- **Use `"Information"`** (the default) for everyday work.
- **Use `"Warning"` or `"Error"`** to keep the log quiet once everything is working.

## Related Settings

- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md) — controls how much of your project Pylance analyzes.

## See Also

- [Reading Pylance Logs](../howto/reading-pylance-logs.md) — how to find, read, and use Pylance's logs.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

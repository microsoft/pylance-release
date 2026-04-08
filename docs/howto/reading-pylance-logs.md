# How to Read Pylance Import Resolution Logs

When Pylance can't resolve an import, trace logging shows exactly where it looked and what it found. This guide explains how to enable trace logging, interpret the output, and use it to diagnose import problems.

---

## Table of Contents

- [Enabling Trace Logging](#enabling-trace-logging)
- [Import Resolution Search Order](#import-resolution-search-order)
- [Reading the Log Output](#reading-the-log-output)
- [Example: Successful Import Resolution](#example-successful-import-resolution)
- [Example: Diagnosing a Missing Import](#example-diagnosing-a-missing-import)
- [FAQ](#faq)

---

## Enabling Trace Logging

Add to `settings.json`:

```json
{
    "python.analysis.logLevel": "Trace"
}
```

Then open the **Output** panel in VS Code (View → Output) and select **Pylance** from the dropdown.

> **Warning**: Trace logging significantly increases output volume and may impact performance. Enable it temporarily for diagnosis, then remove it.

---

## Import Resolution Search Order

Pylance tries these locations in order, stopping at the first match:

| Priority | Search Location                                                      | Log Prefix                                                 |
| -------- | -------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1        | [`stubPath`](../settings/python_analysis_stubPath.md) (custom stubs) | `Looking in stubPath '...'`                                |
| 2        | Execution environment root (project root)                            | `Looking in root directory of execution environment '...'` |
| 3        | [`extraPaths`](../settings/python_analysis_extraPaths.md) entries    | `Looking in extraPath '...'`                               |
| 4        | Typeshed stdlib stubs                                                | `Looking for typeshed stdlib path`                         |
| 5        | Python interpreter search paths (`site-packages`)                    | `Looking in python search path '...'`                      |
| 6        | Typeshed third-party stubs                                           | `Looking for typeshed third-party path`                    |

---

## Reading the Log Output

### Key Log Patterns

| Log Message                                      | Meaning                                                                            |
| ------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `Resolved import with file '...'`                | Pylance found the module. The path tells you _where_ it resolved to.               |
| `Did not find file '...' or '...'`               | Exhausted options in that search location, trying the next.                        |
| `Partially resolved import with directory '...'` | Found a directory but no `__init__.py` or module file.                             |
| `No python interpreter search path`              | Pylance has no site-packages path. Check that the correct interpreter is selected. |

### What to Look For

1. **Where did Pylance look?** The log shows every search location in order.
2. **Where did it resolve (or fail)?** A successful `Resolved import with file` line tells you the exact file path.
3. **Is the resolution correct?** If it resolved to `site-packages` instead of your workspace source, adjust [`extraPaths`](../settings/python_analysis_extraPaths.md) so the preferred source has higher priority.

---

## Example: Successful Import Resolution

A successful resolution looks like this — Pylance finds the module in one of its search locations and stops:

```text
Looking in root directory of execution environment '/workspace'
Attempting to resolve using root path '/workspace'
Resolved import with file '/workspace/packages/shared/src/shared/utils.py'
```

This tells you the import resolved from the project root. If the path looks wrong (e.g., resolving to `site-packages` instead of your workspace source), adjust [`extraPaths`](../settings/python_analysis_extraPaths.md) so the preferred source has higher priority.

---

## Example: Diagnosing a Missing Import

If you see this sequence:

```text
Looking in stubPath '/workspace/typings'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
Looking in root directory of execution environment '/workspace'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
Looking in python search path '/workspace/.venv/lib/python3.11/site-packages'
Did not find file '.../mypackage.pyi' or '.../mypackage.py'
```

This means Pylance checked `stubPath`, the workspace root, and `site-packages` but never found `mypackage`. The fix depends on how `mypackage` should be found:

| How `mypackage` Should Be Found | Fix                                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| It's a workspace package        | Add its parent directory to [`extraPaths`](../settings/python_analysis_extraPaths.md)                  |
| It should be in `site-packages` | Check the interpreter selection or run `pip install mypackage`                                         |
| It's an editable install        | Check the `.pth` file contents — see [How to Use Editable Installs with Pylance](editable-installs.md) |

---

## FAQ

### Q: What's the difference between `logLevel: "Trace"` and `verboseOutput` in pyrightconfig.json?

Import resolution logs are controlled by `"python.analysis.logLevel": "Trace"` in VS Code settings. The `verboseOutput` option in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) is a Pyright-level setting for additional CLI diagnostics — it does not affect the Output panel logs.

### Q: The log says "No python interpreter search path." What does that mean?

Pylance couldn't find a `site-packages` directory for the selected interpreter. This usually means:

- No interpreter is selected (check the Python version in the status bar)
- The selected interpreter's environment is broken or incomplete
- The interpreter path points to a non-existent location

### Q: How do I find logs for a specific import?

Search the Output panel (Ctrl+F) for the module name. The log lines include the module being resolved (e.g., `Looking for ... 'mypackage'`).

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — common import errors and their fixes
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — settings precedence and config file interactions
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — cross-package import resolution in monorepos

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._
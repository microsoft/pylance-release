# How to Gradually Adopt Strict Type Checking in Pylance

Moving a Python project from no type checking to strict mode is easier when done incrementally. This guide covers practical strategies for adopting stricter type checking without overwhelming your team with thousands of new errors.

---

## Table of Contents

- [Strategy Overview](#strategy-overview)
- [Step 1: Start with Basic Mode](#step-1-start-with-basic-mode)
- [Step 2: Enable Individual Rules](#step-2-enable-individual-rules)
- [Step 3: Move to Standard Mode](#step-3-move-to-standard-mode)
- [Step 4: Per-File Strict Mode](#step-4-per-file-strict-mode)
- [Step 5: Project-Wide Strict Mode](#step-5-project-wide-strict-mode)
- [Suppress Rules That Don't Fit](#suppress-rules-that-dont-fit)
- [Use CI to Prevent Regressions](#use-ci-to-prevent-regressions)
- [FAQ](#faq)

---

## Strategy Overview

| Phase | Mode                                      | Goal                                                         |
| ----- | ----------------------------------------- | ------------------------------------------------------------ |
| 1     | `basic`                                   | Catch common mistakes (undefined variables, missing imports) |
| 2     | `basic` + selective overrides             | Add specific rules one at a time                             |
| 3     | `standard`                                | Broader type checking with manageable noise                  |
| 4     | `standard` + per-file `# pyright: strict` | Strict mode for fully-typed files                            |
| 5     | `strict`                                  | Full strictness across the project                           |

---

## Step 1: Start with Basic Mode

Set the baseline in `.vscode/settings.json`:

```json
{
    "python.analysis.typeCheckingMode": "basic"
}
```

Or in `pyrightconfig.json`:

```json
{
    "typeCheckingMode": "basic"
}
```

`basic` enables rules that catch real bugs with low false-positive rates:

- [`reportMissingImports`](../diagnostics/reportMissingImports.md) — unresolved imports
- [`reportUndefinedVariable`](../diagnostics/reportUndefinedVariable.md) — undefined names
- [`reportDuplicateImport`](../diagnostics/reportDuplicateImport.md) — duplicate imports
- [`reportInvalidStringEscapeSequence`](../diagnostics/reportInvalidStringEscapeSequence.md) — bad escape sequences

Fix these first. They are almost always real bugs.

---

## Step 2: Enable Individual Rules

Once `basic` is clean, enable additional rules one at a time using [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md):

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportReturnType": "warning",
        "reportArgumentType": "warning"
    }
}
```

Good rules to enable early (high value, low noise):

| Rule                                                                         | What it catches                          |
| ---------------------------------------------------------------------------- | ---------------------------------------- |
| [`reportReturnType`](../diagnostics/reportReturnType.md)                     | Return value doesn't match declared type |
| [`reportArgumentType`](../diagnostics/reportArgumentType.md)                 | Wrong argument type passed to function   |
| [`reportAssignmentType`](../diagnostics/reportAssignmentType.md)             | Assigning wrong type to a variable       |
| [`reportOptionalMemberAccess`](../diagnostics/reportOptionalMemberAccess.md) | Accessing attribute on possibly `None`   |
| [`reportAttributeAccessIssue`](../diagnostics/reportAttributeAccessIssue.md) | Accessing undefined attribute            |

Use `"warning"` severity first so errors don't block development. Promote to `"error"` after cleanup.

---

## Step 3: Move to Standard Mode

When most `basic` + custom overrides are clean:

```json
{
    "python.analysis.typeCheckingMode": "standard"
}
```

`standard` enables many additional rules. Suppress any that are too noisy initially:

```json
{
    "python.analysis.typeCheckingMode": "standard",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedImport": "information",
        "reportCallIssue": "warning"
    }
}
```

---

## Step 4: Per-File Strict Mode

For files that are already fully annotated, enable strict mode on a per-file basis using a file-level comment:

```python
# pyright: strict

from typing import Optional

def process(name: str, count: int) -> Optional[str]:
    if count <= 0:
        return None
    return name * count
```

This applies `strict` rules only to that file, independent of the project-wide setting.

### Useful per-file comments

| Comment                                        | Effect                                                     |
| ---------------------------------------------- | ---------------------------------------------------------- |
| `# pyright: strict`                            | Enable strict mode for this file                           |
| `# pyright: basic`                             | Use basic mode for this file (override a stricter default) |
| `# pyright: reportMissingImports=false`        | Disable one rule for this file                             |
| `# pyright: reportUnknownVariableType=warning` | Change rule severity for this file                         |

Per-file comments override both VS Code settings and `pyrightconfig.json` for that file.

---

## Step 5: Project-Wide Strict Mode

When most files pass `strict`:

```json
{
    "python.analysis.typeCheckingMode": "strict"
}
```

Then use per-file `# pyright: basic` comments on legacy files that are not yet ready:

```python
# pyright: basic
# TODO: Add type annotations to this module

def legacy_function(data):
    return process(data)
```

This "strict by default, basic for exceptions" approach ensures new code starts strict.

---

## Suppress Rules That Don't Fit

Some rules may never fit your project. Use [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) to permanently suppress them:

```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedCallResult": "none",
        "reportMissingSuperCall": "none"
    }
}
```

Common suppressions in strict mode:

| Rule                                                                                         | Why projects suppress it                                 |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [`reportUnusedCallResult`](../diagnostics/reportUnusedCallResult.md)                         | Many calls legitimately ignore return values             |
| [`reportUnnecessaryTypeIgnoreComment`](../diagnostics/reportUnnecessaryTypeIgnoreComment.md) | Keeping `# type: ignore` for cross-version compatibility |
| [`reportUnknownMemberType`](../diagnostics/reportUnknownMemberType.md)                       | Noisy with untyped dependencies                          |
| [`reportMissingSuperCall`](../diagnostics/reportMissingSuperCall.md)                         | Not all `__init__` methods need `super().__init__()`     |

---

## Use CI to Prevent Regressions

Lock in progress by running Pyright in CI. See [How to Use Pyright in CI](ci-type-checking.md) for setup.

Key CI configuration: use the same `pyrightconfig.json` or `pyproject.toml` that your IDE uses so CI and IDE agree.

```json
// pyrightconfig.json
{
    "typeCheckingMode": "standard",
    "reportReturnType": "error",
    "reportArgumentType": "error"
}
```

This ensures no new violations slip in while you gradually tighten rules.

---

## FAQ

### Q: Which rules does each mode enable?

See the [Pyright diagnostic rule defaults](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults) table for the exact rules in `off`, `basic`, `standard`, and `strict`.

### Q: Can I use different modes for different directories?

Yes. Use the top-level `strict` array in `pyrightconfig.json` to apply strict mode to specific directories:

```json
{
    "typeCheckingMode": "basic",
    "strict": ["src/core"]
}
```

This applies `strict` checking to all files under `src/core/` while the rest of the project uses `basic`. You can also use per-file `# pyright: strict` comments for more granular control.

### Q: How do I count how many errors I have at each mode?

Run Pyright CLI:

```bash
npx pyright --outputjson | python -c "import json,sys; d=json.load(sys.stdin); print(len(d['generalDiagnostics']))"
```

### Q: Does `diagnosticSeverityOverrides` work with `pyrightconfig.json`?

If a config file exists, VS Code's `diagnosticSeverityOverrides` is **ignored**. Set rule severities directly in the config file instead:

```json
// pyrightconfig.json
{
    "typeCheckingMode": "standard",
    "reportReturnType": "error"
}
```

See [Settings Troubleshooting](settings-troubleshooting.md) for the full precedence rules.

---

## Related Guides

- [Type Narrowing](type-narrowing.md) — fix type errors using `isinstance`, `is None`, and type guards
- [Settings Troubleshooting](settings-troubleshooting.md) — config file precedence and override rules
- [CI Type Checking](ci-type-checking.md) — enforce type checking in your build pipeline
- [Performance Tuning](performance-tuning.md) — manage resource usage as you add more checking
- [`typeCheckingMode` setting](../settings/python_analysis_typeCheckingMode.md) — detailed setting reference
- [`diagnosticSeverityOverrides` setting](../settings/python_analysis_diagnosticSeverityOverrides.md) — per-rule overrides

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

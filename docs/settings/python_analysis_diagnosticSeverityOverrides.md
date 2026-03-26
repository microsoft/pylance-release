# Understanding `python.analysis.diagnosticSeverityOverrides` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides rich language features and a large set of configurable diagnostics.

The `python.analysis.diagnosticSeverityOverrides` setting lets you change the severity of individual diagnostic rules without changing your whole type-checking mode.

## What `python.analysis.diagnosticSeverityOverrides` does

`python.analysis.diagnosticSeverityOverrides` is an object whose keys are diagnostic rule names and whose values are severity levels.

Use this setting when the default severity for one specific rule does not fit your project, but you do not want to broadly weaken or strengthen every rule.

Example:

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "warning",
        "reportGeneralTypeIssues": "error"
    }
}
```

## Accepted values

Each rule can be set to one of these values:

- `error`
    - Show the diagnostic as an error.
- `warning`
    - Show the diagnostic as a warning.
- `information`
    - Show the diagnostic as an information message.
- `none`
    - Disable that diagnostic rule.
- `true`
    - Alias for `error`.
- `false`
    - Alias for `none`.

The string forms are usually clearer than the boolean aliases, especially when you revisit the setting later.

## How this relates to `python.analysis.typeCheckingMode`

[`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) chooses a broad default rule set for the workspace.

`python.analysis.diagnosticSeverityOverrides` then lets you adjust individual rules on top of that baseline.

This means you can keep a mode like `standard` or `strict` and still soften or disable a small number of rules that do not fit your codebase.

The default values shown for individual rules correspond to the defaults when `python.analysis.typeCheckingMode` is `off`. Effective defaults vary by type-checking mode. For the current default table, see the Pyright documentation on [diagnostic rule defaults](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults).

## When to use this setting

Use `python.analysis.diagnosticSeverityOverrides` when:

- one or two specific rules are too noisy for your project
- you want to gradually adopt stricter analysis without switching all rules at once
- you want a rule to remain visible but at a lower severity

Common examples include:

- lowering `reportMissingImports` while migrating an environment or dependency layout
- disabling one rule temporarily during a cleanup effort
- making a rule stricter in CI-oriented or highly typed projects

## When another solution is better

Severity overrides are useful, but they are not always the best long-term fix.

### Use `ignore` for path-wide suppression

If you want to suppress all diagnostics for specific generated, vendored, or legacy paths, [`python.analysis.ignore`](python_analysis_ignore.md) is usually the better tool.

Use `diagnosticSeverityOverrides` when the issue is rule-specific. Use `ignore` when the issue is location-specific.

### Use stubs when Pylance is missing real type information

If a rule is noisy because Pylance does not know about injected globals, custom runtime symbols, or missing package typing, adding stubs can be a better fix than silencing the rule.

One common case is `reportUndefinedVariable` for symbols that are genuinely injected into your runtime environment. In that situation, you can teach Pylance about those names with a stub instead of disabling the rule.

For example, create a `__builtins__.pyi` file under your stub directory:

```text
typings/
└── __builtins__.pyi
```

```python
# typings/__builtins__.pyi

magic_variable_1: int
magic_variable_2: str
```

Then either rely on the default stub directory name `typings` or point Pylance at a custom stub root with [`python.analysis.stubPath`](python_analysis_stubPath.md):

```json
{
    "python.analysis.stubPath": "typings"
}
```

This keeps the diagnostic rule active for real mistakes while telling Pylance about the symbols that actually exist at runtime.

The same idea applies to third-party packages with missing typing. If `reportMissingImports`, `reportUnknownMemberType`, or related rules are noisy because a library has incomplete typing information, adding focused package stubs is usually better than globally muting the rule.

### Use `TYPE_CHECKING` patterns for runtime import fallbacks

If your code intentionally uses runtime fallback imports for different environments or package versions, a severity override can hide the warning, but it may also hide real problems.

In many of those cases, a clearer static-analysis pattern is to use `typing.TYPE_CHECKING` to tell the type checker which import branch to assume.

For example, this runtime-only fallback can trigger import-related noise:

```python
try:
    from PySide6.QtCore import QTimer
except ImportError:
    from PySide2.QtCore import QTimer
```

Instead, separate the static-analysis branch from the runtime branch:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import QTimer
else:
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer
```

That approach lets Pylance analyze one intentional branch while preserving your runtime compatibility logic.

### Fix the environment or import configuration when the import should really resolve

Sometimes a noisy rule is reporting a real configuration problem rather than something you should suppress.

For example, if `reportMissingImports` appears because:

- the selected Python environment does not actually contain the package
- the import root is missing from your project configuration
- the package lives in a source directory that should be added through workspace or Pyright configuration

then a severity override hides the symptom but does not fix the root cause. In those cases, fixing the environment, search paths, or project layout is usually the better move.

## Example configurations

### Lower one rule and disable another

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "warning",
        "reportUnusedImport": "none"
    }
}
```

### Keep a strict workspace but soften one high-noise rule

```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "information"
    }
}
```

### Use boolean aliases

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": false,
        "reportGeneralTypeIssues": true
    }
}
```

That works, but the string forms are usually easier to read:

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "none",
        "reportGeneralTypeIssues": "error"
    }
}
```

## Finding rule names

Rule names use the Pyright diagnostic rule names, such as `reportMissingImports`, `reportUnusedImport`, or `reportGeneralTypeIssues`.

For the current rule list and default severities by type-checking mode, see the Pyright documentation on [diagnostic settings defaults](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults).

## Frequently asked questions

### Does this replace `python.analysis.typeCheckingMode`?

No. [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md) still determines the overall default analysis posture. `diagnosticSeverityOverrides` is a per-rule customization layer on top.

### Should I use `none` or `false`?

Both disable the rule. `false` is just an alias for `none`. Using `none` is usually clearer.

### Can I use this to suppress diagnostics only in one folder?

Not directly. This setting changes a rule globally for the workspace. If you want path-based suppression, use [`python.analysis.ignore`](python_analysis_ignore.md).

### Why not just disable a noisy rule permanently?

Sometimes that is appropriate, but often the better fix is to improve Pylance's understanding of the code by restructuring imports, adding stubs, or adjusting workspace configuration.

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.

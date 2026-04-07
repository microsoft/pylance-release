# Understanding `python.analysis.typeEvaluation.analyzeUnannotatedFunctions` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.analyzeUnannotatedFunctions` setting controls whether Pylance analyzes and reports errors for functions and methods that have no type annotations for input parameters or return types.

## What `python.analysis.typeEvaluation.analyzeUnannotatedFunctions` does

When enabled, Pylance performs type analysis inside functions that lack type annotations and reports errors it finds. When disabled, Pylance skips error reporting for unannotated function bodies, which can reduce noise in untyped codebases.

The default value is `true`.

```json
"python.analysis.typeEvaluation.analyzeUnannotatedFunctions": true
```

### Example

```python
def add(a, b):
    return a + b

result = add(1, "2")
```

With the setting set to `true`, Pylance may report a type error for the call `add(1, "2")` because it infers types within the function and detects the mismatch.

With the setting set to `false`, Pylance skips analysis of the unannotated `add` function and does not report errors within it.

## Accepted values

- `true` (default): Analyze and report errors for unannotated functions.
- `false`: Skip error reporting for functions without type annotations.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.analyzeUnannotatedFunctions`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.analyzeUnannotatedFunctions": false
    ```

## When to change this setting

### Keep `true` (default) for better error detection

The default is a good choice when you want Pylance to catch errors in all functions, even those without annotations. This helps identify bugs early, especially in codebases that are gradually adopting type hints.

### Set to `false` for legacy or untyped codebases

If your codebase has many unannotated functions and the resulting diagnostics are too noisy, setting this to `false` can reduce the number of reported errors while you incrementally add type annotations.

## Related settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules. Higher modes enable more diagnostics overall.
- [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md)
    - Fine-grained control over individual diagnostic rule severities.

## Frequently asked questions

### Q: Will disabling this setting turn off all type checking?

**A:** No. It only affects functions that have no type annotations for parameters or return types. Annotated functions continue to be fully checked.

### Q: Does this setting affect third-party library code?

**A:** No. This setting applies to your own source files. Third-party library analysis is controlled by other settings such as [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md).

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

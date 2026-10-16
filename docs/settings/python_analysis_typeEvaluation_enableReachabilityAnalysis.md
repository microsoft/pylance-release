# Understanding `python.analysis.typeEvaluation.enableReachabilityAnalysis` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language server extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.enableReachabilityAnalysis` setting controls whether Pylance reports code that is determined to be unreachable based on type analysis.

## What `python.analysis.typeEvaluation.enableReachabilityAnalysis` does

When enabled, Pylance uses type information to identify code blocks that can never execute and grays them out in the editor using a tagged hint. For example, if a type guard narrows a variable's type so that a branch condition can never be true, Pylance marks that branch as unreachable.

The default value is `false`.

```json
"python.analysis.typeEvaluation.enableReachabilityAnalysis": false
```

**Important**: This setting only affects code that is unreachable _because of type analysis_. Code that is unreachable regardless of types (e.g., code after an unconditional `return`) is always reported as unreachable, regardless of this setting.

### Example

```python
def process(value: int) -> None:
    if not isinstance(value, int):
        print("string")   # grayed out when setting is true
    else:
        print("integer")
```

Since `value` is annotated as `int`, the negated `isinstance(value, int)` check can never be true according to static analysis. With the setting enabled, Pylance grays out the `if` branch.

## Accepted values

- `true`: Enable type-based reachability analysis. Unreachable code is grayed out.
- `false` (default): Disable type-based reachability hints. Structurally unreachable code (e.g., after `return`) and statically false branches are still reported.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.enableReachabilityAnalysis`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.enableReachabilityAnalysis": true
    ```

You can also set this in `pyrightconfig.json`:

```json
{
    "enableReachabilityAnalysis": true
}
```

## When to enable this setting

### Finding dead code

Enable this setting to identify code branches that type analysis proves can never execute. This helps you clean up unnecessary code paths.

### When to keep the default

If your code includes defensive runtime type checks (e.g., `isinstance` guards for types not covered by annotations), enabling this setting may gray out code that is intentionally reachable at runtime. In that case, keeping the default (`false`) avoids visual noise.

### Dynamic typing and untyped libraries

In codebases that interface with dynamic or untyped code, static type analysis may not accurately predict runtime types. Disabling reachability analysis prevents Pylance from incorrectly marking defensively written code as dead.

## Frequently asked questions

### Q: Will disabling this setting affect other Pylance features?

**A:** No. Disabling reachability analysis only affects the graying out of type-unreachable code. Completions, diagnostics, navigation, and other features continue to work normally.

### Q: Does this setting affect the command-line version of Pyright?

**A:** No. The command-line version of Pyright does not emit tagged hints for unreachable code, so this setting has no effect there.

### Q: Can I disable reachability analysis for specific files?

**A:** There is no per-file comment override. Configure this setting for the applicable workspace or project.

## Related Diagnostics

Reachability analysis interacts with these diagnostic rules:

- [`reportUnnecessaryComparison`](../diagnostics/reportUnnecessaryComparison.md) — comparison always has the same result
- [`reportUnnecessaryIsInstance`](../diagnostics/reportUnnecessaryIsInstance.md) — `isinstance()` check always true or false
- [`reportUnnecessaryContains`](../diagnostics/reportUnnecessaryContains.md) — `in` check always has the same result

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

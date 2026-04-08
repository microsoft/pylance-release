# Understanding `python.analysis.typeCheckingMode` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides diagnostics, completions, navigation, and type analysis that can range from lightweight to highly strict.

The `python.analysis.typeCheckingMode` setting controls the baseline strictness of Pylance's type-checking rules.

## What `python.analysis.typeCheckingMode` does

`python.analysis.typeCheckingMode` selects a preset level of type-checking strictness.

The default value is `off`.

```json
"python.analysis.typeCheckingMode": "off"
```

Each stricter mode builds on the previous one:

- `off`
    - No broad type-checking pass. Pylance still reports core problems such as unresolved imports and undefined variables.
- `basic`
    - Adds a smaller set of type-checking rules intended to catch common mistakes.
- `standard`
    - Adds more type-checking rules on top of `basic`.
- `strict`
    - Enables the strictest default rule set.

For the current rule-by-rule defaults, see the Pyright documentation on [diagnostic rule defaults](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults).

## Accepted values

- `off`
- `basic`
- `standard`
- `strict`

## How to choose a mode

### Use `off` when you want the lightest type-checking posture

`off` is the default because it keeps Pylance focused on essential diagnostics without running a broader type-checking rule set.

Use it when:

- you want minimal type-checking noise while editing
- you are working in a loosely typed or dynamic codebase
- performance is more important than deep type analysis

### Use `basic` when you want a gradual step up

`basic` is a good starting point when you want more help than `off` provides but are not ready for the broader rule coverage of `standard` or `strict`.

This is often a practical choice for teams that are introducing type checking incrementally.

### Use `standard` when you want stronger defaults without going fully strict

`standard` adds more checking than `basic` and is often a better fit for teams that want meaningful type analysis but do not want the full noise floor of `strict`.

### Use `strict` when the project is intentionally heavily typed

`strict` is the best fit when:

- the codebase already has strong typing discipline
- the team wants type checking to catch as many issues as possible
- you are willing to spend effort on annotations and cleanup

## Precedence: config files can override the VS Code setting

The VS Code setting is not always the final source of truth.

If your workspace contains a `pyrightconfig.json` file or a `pyproject.toml` file with a `[tool.pyright]` section, that project configuration can override the `python.analysis.typeCheckingMode` value you set in `settings.json`.

That matters when the editor seems to show a different behavior than the VS Code setting suggests.

For example, this workspace setting:

```json
{
    "python.analysis.typeCheckingMode": "off"
}
```

can still be effectively overridden by a project config like:

```json
{
    "typeCheckingMode": "strict"
}
```

If you are debugging unexpected rule behavior, check both:

- your VS Code `settings.json`
- any `pyrightconfig.json`
- any `pyproject.toml` with `[tool.pyright]`

## How this relates to `diagnosticSeverityOverrides`

`python.analysis.typeCheckingMode` sets the baseline.

[`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md) lets you adjust individual rules on top of that baseline.

That combination is useful when you want a generally stricter mode without accepting every default rule severity unchanged.

For example, you can keep `standard` mode but soften a single high-noise rule:

```json
{
    "python.analysis.typeCheckingMode": "standard",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "warning"
    }
}
```

## Performance considerations

Higher type-checking modes can increase the amount of analysis Pylance performs.

If you are tuning for performance, `typeCheckingMode` is only one lever. Related settings that often matter more for large workspaces include:

- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md)
    - Broad preset that changes multiple performance-sensitive settings at once.
- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md)
    - Controls whether diagnostics are produced for open files only or for the whole workspace.
- [`python.analysis.exclude`](python_analysis_exclude.md)
    - Removes files or folders from the workspace view used by Pylance.
- [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md)
    - Controls whether Pylance parses third-party library source when stubs are missing.
- [`python.analysis.indexing`](python_analysis_indexing.md)
    - Controls indexing for auto-import, symbol search, and related features.
- [`python.analysis.userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md)
    - Limits how many workspace files are indexed.

If your main goal is to reduce CPU or memory pressure in a very large workspace, changing `typeCheckingMode` alone may not be enough. Narrowing workspace scope or indexing behavior is often more effective.

## Example configurations

### Keep the default lightweight baseline

```json
{
    "python.analysis.typeCheckingMode": "off"
}
```

### Adopt a moderate baseline

```json
{
    "python.analysis.typeCheckingMode": "basic"
}
```

### Use a stricter baseline with one rule override

```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingTypeStubs": "none"
    }
}
```

## Frequently asked questions

### Why does the editor not seem to follow my `python.analysis.typeCheckingMode` setting?

Check for `pyrightconfig.json` or `pyproject.toml` project settings. Those can override the VS Code value.

### Does `off` mean Pylance stops reporting every problem?

No. `off` disables the broader type-checking rule set, but Pylance still reports core problems such as unresolved imports and undefined variables.

### Should I jump directly to `strict`?

Usually only if the codebase is already well annotated or the team is prepared for the cleanup work. Many projects adopt `basic` or `standard` first and then use [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md) to smooth the path toward stricter checking.

## See Also

- [How to Set Up CI Type Checking](../howto/ci-type-checking.md) — using `typeCheckingMode` in CI pipelines
- [How to Troubleshoot Settings](../howto/settings-troubleshooting.md) — what happens when `pyrightconfig.json` overrides the VS Code setting

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.

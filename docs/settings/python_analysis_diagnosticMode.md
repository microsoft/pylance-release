# Understanding `python.analysis.diagnosticMode` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics that help you spot problems while you work.

The `python.analysis.diagnosticMode` setting controls how broadly Pylance analyzes your workspace when producing diagnostics.

## What `python.analysis.diagnosticMode` does

`python.analysis.diagnosticMode` tells Pylance whether diagnostics should be produced only for files you currently have open or for all files in the workspace.

The default value is `openFilesOnly`.

```json
"python.analysis.diagnosticMode": "openFilesOnly"
```

## Accepted values

- `openFilesOnly`
    - Analyze and report diagnostics for open files only.
    - This is the default.
- `workspace`
    - Analyze and report diagnostics for all files in the workspace.

## When to use each value

### Use `openFilesOnly` when you want a lighter default workflow

`openFilesOnly` is usually the right choice when:

- you work in a large repository and want to reduce ongoing diagnostic work
- you care primarily about diagnostics in the files you are actively editing
- workspace-wide diagnostics would be noisy or expensive

This mode is commonly the better fit for very large workspaces, monorepos, or course/exercise folders where you do not need every file checked all the time.

### Use `workspace` when you want full-project diagnostics

`workspace` is useful when:

- you want errors surfaced in unopened files
- you treat the editor as a project-wide diagnostic pass, not just an active-file tool
- you are working in a smaller or more tightly managed workspace

## What this setting does not do

`python.analysis.diagnosticMode` controls diagnostic scope. It does not redefine the workspace itself.

That distinction matters in large workspaces. Even with `openFilesOnly`, Pylance may still perform workspace-related setup or feature work that is separate from reporting diagnostics for every file.

If your goal is to reduce how much content belongs to the workspace in the first place, use these settings alongside `diagnosticMode`:

- [`python.analysis.include`](python_analysis_include.md)
    - Explicitly choose which files or folders belong in the workspace.
- [`python.analysis.exclude`](python_analysis_exclude.md)
    - Remove files or folders from the workspace view used by Pylance.
- [`python.analysis.ignore`](python_analysis_ignore.md)
    - Keep files available for language features, but suppress diagnostics for matching paths.

In other words:

- use `diagnosticMode` to decide how broadly diagnostics are reported
- use `include` and `exclude` to shape the workspace contents
- use `ignore` when you still want files processed but do not want diagnostics from them

## Performance considerations

Switching from `workspace` to `openFilesOnly` can reduce diagnostic workload in large repositories.

However, if performance problems come from the size or shape of the workspace itself, `diagnosticMode` may not be the only setting you need to adjust. In that case, narrowing [`python.analysis.include`](python_analysis_include.md) or broadening [`python.analysis.exclude`](python_analysis_exclude.md) is often more effective.

For example, if you want Pylance to avoid most workspace files entirely, excluding large generated folders, vendored code, or exercise archives may help more than changing diagnostic scope alone.

If you are tuning Pylance for overall performance, these are the other settings worth checking alongside `diagnosticMode`:

- [`python.analysis.languageServerMode`](python_analysis_languageServerMode.md)
    - Broad preset that changes several performance-sensitive defaults at once. `light` is usually the fastest starting point when you want a low-resource setup.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Higher type-checking modes add more analysis work. Lowering this can reduce diagnostic and type-analysis overhead.
- [`python.analysis.exclude`](python_analysis_exclude.md)
    - One of the most direct ways to reduce work in very large workspaces.
- [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md)
    - Turning this off avoids parsing third-party library source when stubs are missing.
- [`python.analysis.indexing`](python_analysis_indexing.md)
    - Disabling indexing reduces work for auto-import, workspace symbols, and related features.
- [`python.analysis.userFileIndexingLimit`](python_analysis_userFileIndexingLimit.md)
    - Lets you cap how many workspace files are indexed.

Those settings do different jobs, but together they form the main performance-sensitive surface area for large workspaces.

## Example configurations

### Open files only

```json
{
    "python.analysis.diagnosticMode": "openFilesOnly"
}
```

### Full workspace diagnostics

```json
{
    "python.analysis.diagnosticMode": "workspace"
}
```

### Open-file diagnostics with an aggressively narrowed workspace

```json
{
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.exclude": ["**/build/**", "**/generated/**", "**/.venv/**"]
}
```

## Frequently asked questions

### Why does Pylance still seem busy when `diagnosticMode` is `openFilesOnly`?

Because `openFilesOnly` limits diagnostic reporting scope, not every kind of workspace-related work. If the workspace is very large, consider adjusting [`python.analysis.include`](python_analysis_include.md) or [`python.analysis.exclude`](python_analysis_exclude.md) as well.

### Does `openFilesOnly` mean unopened files are never considered for anything?

No. It means diagnostics are reported only for open files. Other language-service behavior can still depend on workspace structure and project configuration.

### Should I use `ignore` instead of `diagnosticMode`?

Not usually. Use `diagnosticMode` when you want to control analysis scope globally. Use [`python.analysis.ignore`](python_analysis_ignore.md) when you want to suppress diagnostics only for specific paths.

## See Also

- [How to Tune Pylance Performance](../howto/performance-tuning.md) — using `diagnosticMode` to reduce resource usage
- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — `diagnosticMode` in multi-root workspaces

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.

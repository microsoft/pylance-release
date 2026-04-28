# How to Tune Pylance Performance

Pylance runs as a language server inside VS Code and can consume significant CPU and memory on large projects. This guide covers the key settings for controlling resource usage and the trade-offs each option involves.

---

## Table of Contents

- [Language Server Mode](#language-server-mode)
- [Diagnostic Mode](#diagnostic-mode)
- [Indexing Controls](#indexing-controls)
- [Exclude Patterns](#exclude-patterns)
- [Node.js Heap Limit](#nodejs-heap-limit)
- [Per-Folder Memory in Multi-Root Workspaces](#per-folder-memory-in-multi-root-workspaces)
- [Performance Presets](#performance-presets)
- [FAQ](#faq)

---

## Language Server Mode

[`python.analysis.languageServerMode`](../settings/python_analysis_languageServerMode.md) is the single most impactful performance setting. It sets defaults for several other settings at once:

| Setting                                                                           | `"light"` Default | `"default"` Default | `"full"` Default |
| --------------------------------------------------------------------------------- | ----------------- | ------------------- | ---------------- |
| [`exclude`](../settings/python_analysis_exclude.md)                               | `["**"]`          | `[]`                | `[]`             |
| [`indexing`](../settings/python_analysis_indexing.md)                             | `false`           | `true`              | `true`           |
| [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)             | `"off"`           | `"off"`             | (unchanged)      |
| [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) | `false`           | `true`              | `true`           |
| [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md)   | (unchanged)       | `false`             | `true`           |
| [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md)   | (unchanged)       | `2000`              | `-1` (unlimited) |

You can **override any individual setting** even when a mode is active — the mode only sets defaults, it doesn't lock them.

**Example**: Enable indexing in light mode:

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.indexing": true
}
```

---

## Diagnostic Mode

[`python.analysis.diagnosticMode`](../settings/python_analysis_diagnosticMode.md) controls which files Pylance actively analyzes for errors:

- **`"openFilesOnly"`** (default): Only files open in the editor are analyzed. The most memory-efficient option.
- **`"workspace"`**: All Python files in the workspace are analyzed. Provides project-wide diagnostics but uses more memory and CPU.

For large projects, `"openFilesOnly"` is strongly recommended. Switch to `"workspace"` only if you need to see all errors across the project without opening each file.

---

## Indexing Controls

Indexing pre-parses workspace files and library packages to enable fast auto-imports, workspace symbol search (Ctrl+T), and completions. The trade-off is upfront CPU and memory usage.

### Key Settings

| Setting                                                                                                                         | Effect                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [`python.analysis.indexing`](../settings/python_analysis_indexing.md)                                                           | `true` (default) enables background indexing; `false` disables it                                                       |
| [`python.analysis.userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md)                                 | Maximum number of user files to index (default: `2000`; `-1` for unlimited)                                             |
| [`python.analysis.packageIndexDepths`](../settings/python_analysis_packageIndexDepths.md)                                       | Controls how deep Pylance indexes specific third-party packages                                                         |
| [`python.analysis.includeVenvInWorkspaceSymbols`](../settings/python_analysis_includeVenvInWorkspaceSymbols.md)                 | Include venv `site-packages` symbols in workspace symbol search (default: `false`)                                      |
| [`python.analysis.includeExtraPathSymbolsInSymbolSearch`](../settings/python_analysis_includeExtraPathSymbolsInSymbolSearch.md) | Include [`extraPaths`](../settings/python_analysis_extraPaths.md) symbols in workspace symbol search (default: `false`) |

### When to Disable Indexing

Disable indexing (`"python.analysis.indexing": false`) if:

- Startup is too slow and you can tolerate reduced auto-import coverage
- You mainly work in open files and don't rely on workspace symbol search
- Memory usage is a concern on constrained machines

Without indexing, auto-imports still work for open files, their transitive imports, and stdlib — but won't find symbols in files that haven't been loaded.

---

## Exclude Patterns

[`python.analysis.exclude`](../settings/python_analysis_exclude.md) removes directories from Pylance's file discovery. This is one of the most effective ways to reduce memory and indexing time.

**Common patterns to exclude**:

```json
{
    "python.analysis.exclude": ["**/node_modules", "**/.git", "**/build", "**/dist", "**/data", "**/__pycache__"]
}
```

In multi-root workspaces, you can also **exclude entire workspace folders** you're not actively working on:

```json
{
    "python.analysis.exclude": ["${workspaceFolder:unused-folder}"]
}
```

> **Note**: Virtual environments (`.venv`, `venv`, etc.) are auto-excluded by default. You don't need to add them to `exclude` manually.

> **Note**: If [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` with `[tool.pyright]` exists, the VS Code `exclude` setting is **ignored** — set `exclude` in the config file instead. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).

---

## Node.js Heap Limit

By default, Pylance runs inside VS Code's built-in Node.js runtime, which uses [pointer compression](https://v8.dev/blog/pointer-compression). This limits the effective heap to approximately **4 GB**, regardless of system RAM.

When `languageServerMode` is `"full"` (or `python.analysis.nodeExecutable` is set), Pylance launches in a separate Node.js process where the `--max-old-space-size=8192` argument takes effect, raising the limit to **8 GB**.

If you hit "JavaScript heap out of memory" errors or "Extension host terminated unexpectedly," switch to an external Node.js runtime and optionally increase the heap:

1. Set [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md) to `"auto"` (downloads a standalone Node.js) or set `languageServerMode` to `"full"` (which does this automatically):

    ```json
    {
        "python.analysis.nodeExecutable": "auto"
    }
    ```

2. Optionally increase [`python.analysis.nodeArguments`](../settings/python_analysis_nodeArguments.md) beyond the 8 GB default:

    ```json
    {
        "python.analysis.nodeArguments": ["--max-old-space-size=16384"]
    }
    ```

3. **Restart VS Code** (both settings require a full restart).

### Recommended Heap Sizes

These apply only when running with an external Node.js (`nodeExecutable` or `languageServerMode: "full"`):

| Project Size                 | Recommended `--max-old-space-size` |
| ---------------------------- | ---------------------------------- |
| Small–Medium (< 5,000 files) | 8192 (default with external Node)  |
| Large (5,000–20,000 files)   | 12288–16384                        |
| Very large (> 20,000 files)  | 16384–32768                        |

> **Tip**: Increasing heap doesn't fix the root cause — it gives Pylance more room to work. Prefer reducing Pylance's workload first (fewer workspace folders, `"openFilesOnly"`, proper `exclude` patterns, disable indexing).

See the [`python.analysis.nodeExecutable`](../settings/python_analysis_nodeExecutable.md) and [`python.analysis.nodeArguments`](../settings/python_analysis_nodeArguments.md) setting pages for details and scope considerations.

---

## Per-Folder Memory in Multi-Root Workspaces

In multi-root workspaces, each workspace folder creates a separate analyzer service. With many folders (>10–20), the combined memory usage can exceed the Node.js heap limit.

### Diagnosis

1. Open **Output → Pylance** and look for per-folder startup/analysis messages
2. Check how many workspace folders are configured in your `.code-workspace` file
3. Look for "JavaScript heap out of memory" or "Extension host terminated unexpectedly" in the Output panel

### Mitigations

| Strategy                                                                                                                  | Effect                                                                         |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Switch to [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) | Single analyzer instead of per-folder — dramatically reduces memory            |
| Use [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)                                   | Single workspace with auto-discovered configs — lower overhead than multi-root |
| Set [`languageServerMode`](../settings/python_analysis_languageServerMode.md) to `"light"`                                | Minimizes per-folder memory footprint                                          |
| Use `"openFilesOnly"` diagnostic mode                                                                                     | Avoids analyzing all files in every folder                                     |
| Exclude unused folders                                                                                                    | `"python.analysis.exclude": ["${workspaceFolder:unused-folder}"]`              |
| Increase the heap limit                                                                                                   | See [Node.js Heap Limit](#nodejs-heap-limit) above                             |

---

## Performance Presets

### Large Projects (minimal resource usage)

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.indexing": false
}
```

### Medium Projects (balanced)

```json
{
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.userFileIndexingLimit": 1000,
    "python.analysis.indexing": true
}
```

### Small Projects (full features)

```json
{
    "python.analysis.languageServerMode": "full",
    "python.analysis.diagnosticMode": "workspace"
}
```

---

## FAQ

### Q: Why does Pylance crash with many workspace folders?

Each workspace folder creates a separate analyzer service. With many folders (>10–20), the combined memory usage can exceed the Node.js heap limit. Mitigations:

1. Use [`languageServerMode`](../settings/python_analysis_languageServerMode.md)`: "light"` to minimize per-folder memory
2. Exclude folders you're not working on
3. Switch to [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) instead (single analyzer)
4. Use [`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) instead (single workspace)

### Q: Does `diagnosticMode: "workspace"` affect auto-imports?

No. Auto-import completions are driven by the indexer, not by diagnostic mode. You can use `"openFilesOnly"` and still get full auto-import coverage if indexing is enabled.

### Q: Can I enable indexing in light mode?

Yes. Override the default:

```json
{
    "python.analysis.languageServerMode": "light",
    "python.analysis.indexing": true
}
```

But also set `exclude` to a narrower pattern — light mode defaults `exclude` to `["**"]`, which limits indexing to open files.

### Q: How do I know if Pylance is running out of memory?

Look for these signs in the **Output → Pylance** panel or VS Code notifications:

- "Extension host terminated unexpectedly"
- "JavaScript heap out of memory"
- Pylance stops responding (no hovers, completions, or diagnostics)
- Very slow startup or analysis

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution and common missing-import fixes
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — config file precedence and setting interactions
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — multi-root workspaces and execution environments

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

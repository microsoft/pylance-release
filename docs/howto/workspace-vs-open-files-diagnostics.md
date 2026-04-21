# How to Get Whole-Workspace Diagnostics from Pylance

By default Pylance only reports errors for files you have open. That keeps the editor responsive on large projects, but it surprises users who expect to see every error in the project at once. This guide explains the trade-off, when to widen scope, and how to get whole-workspace diagnostics on demand without permanently changing settings.

---

## Table of Contents

- [Why You Only See Errors for Open Files](#why-you-only-see-errors-for-open-files)
- [Pick the Right Approach](#pick-the-right-approach)
- [Get Workspace Diagnostics On-Demand via LSP](#get-workspace-diagnostics-on-demand-via-lsp)
- [Switch diagnosticMode to "workspace"](#switch-diagnosticmode-to-workspace)
- [Run Pyright in CI](#run-pyright-in-ci)
- [Confirm What Pylance Is Analyzing](#confirm-what-pylance-is-analyzing)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## Why You Only See Errors for Open Files

[`python.analysis.diagnosticMode`](../settings/python_analysis_diagnosticMode.md) controls which files Pylance actively reports diagnostics for in the editor.

| Value                       | Behavior                                                                                                                                                                     |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"openFilesOnly"` (default) | Only files open in the editor produce diagnostics in the Problems panel and inline squiggles.                                                                                |
| `"workspace"`               | All Python files in the workspace produce diagnostics, subject to [`include`](../settings/python_analysis_include.md) / [`exclude`](../settings/python_analysis_exclude.md). |

Pylance still parses and indexes other files for completions, hovers, and import resolution. The setting only controls whether diagnostics are _published_ for them.

The default is `"openFilesOnly"` because:

- Whole-workspace diagnostics on large monorepos can use significant CPU and memory.
- Most editing flows only care about the file you are touching.
- CI is the right place to enforce errors across the whole project.

See [How to Tune Pylance Performance](performance-tuning.md) for the full picture.

---

## Pick the Right Approach

You have three ways to see errors outside the file you are editing. Pick by need:

| You want to...                                                   | Use this                                                                                                    |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Quickly check the whole project once, without changing settings. | [Get Workspace Diagnostics On-Demand via LSP](#get-workspace-diagnostics-on-demand-via-lsp).                |
| Continuously see all errors while editing.                       | [Switch diagnosticMode to "workspace"](#switch-diagnosticmode-to-workspace).                                |
| Enforce errors as a build gate, independent of any editor state. | [Run Pyright in CI](#run-pyright-in-ci) (canonical guide: [How to Run Pyright in CI](ci-type-checking.md)). |

The on-demand LSP path is the most common answer for "I want to know everything that is wrong right now without slowing down my editor".

---

## Get Workspace Diagnostics On-Demand via LSP

The LSP `workspace/diagnostic` request asks the language server for diagnostics across all known files. It works regardless of `diagnosticMode`, because the request is explicit.

### From Copilot or any MCP client

Use the `pylanceLSP` MCP tool:

```jsonc
// pylanceLSP
{
    "method": "workspace/diagnostic",
    "params": {},
}
```

For a single file:

```jsonc
// pylanceLSP
{
    "method": "textDocument/diagnostic",
    "params": { "textDocument": { "uri": "file:///path/to/file.py" } },
}
```

These return the same diagnostics the editor would show, including type-check errors, unused imports, and other rules controlled by [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md).

A common workflow when investigating a Pylance-related complaint:

1. `pylanceWorkspaceRoots` to capture the canonical root URI.
2. `pylanceWorkspaceUserFiles` to confirm which files Pylance considers part of the workspace.
3. `pylanceLSP` `workspace/diagnostic` to get every diagnostic at once.
4. Group results by file and rule, then act.

See [How to Fix Pylance Issues with Copilot](copilot-pylance-workflow.md) for the full diagnosis loop.

### From the VS Code UI

VS Code has no built-in command for "give me all workspace diagnostics" without changing settings. To force a one-shot full analysis you can either:

- Open a representative set of files and let `openFilesOnly` produce diagnostics for them, or
- Switch [`python.analysis.diagnosticMode`](../settings/python_analysis_diagnosticMode.md) to `"workspace"` temporarily, or
- Run `pyright` from a terminal as a one-shot check.

---

## Switch diagnosticMode to "workspace"

If you genuinely want full-project errors live in the editor, set:

```json
{
    "python.analysis.diagnosticMode": "workspace"
}
```

Things to know before flipping this on:

- Initial analysis can be CPU- and memory-heavy on large workspaces. See [How to Tune Pylance Performance](performance-tuning.md).
- The setting is honored per workspace folder. In a multi-root workspace you can enable it only where it matters.
- Pair it with sensible [`include`](../settings/python_analysis_include.md) / [`exclude`](../settings/python_analysis_exclude.md) so test fixtures, vendored code, and generated outputs do not flood the Problems panel. See [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) and [How to Handle Generated Code](generated-code.md).
- For very large repos, prefer the on-demand LSP path or CI; do not leave `"workspace"` on permanently if it makes the editor sluggish.

---

## Run Pyright in CI

Pylance is the editor; [`pyright`](https://github.com/microsoft/pyright) is the type checker that powers it. For build-gate enforcement, run `pyright` in CI rather than relying on a contributor's editor configuration.

This is the right tool when you want:

- A blocking check that everyone sees the same errors regardless of their VS Code settings.
- A pinned Python version and pinned tool version.
- Output that integrates with PR checks.

Canonical guide: [How to Run Pyright in CI](ci-type-checking.md). For project-wide settings that both Pylance and `pyright` honor, prefer [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) over VS Code settings.

---

## Confirm What Pylance Is Analyzing

If `workspace/diagnostic` returns fewer results than you expect, the issue is usually file scope, not the diagnostic mode.

| Question                                                | How to answer it                                                                                                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Which files does Pylance treat as user files?           | `pylanceWorkspaceUserFiles` for the workspace root.                                                                 |
| Are the missing files excluded by include / exclude?    | `pylanceSettings`. Look at `include`, `exclude`, `ignore`.                                                          |
| Is a `pyrightconfig.json` overriding VS Code scope?     | See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).                                            |
| Is the file even reachable from the active interpreter? | `pylanceImports` for the file in question; [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md). |

Common gotchas:

- Large auto-generated trees ignored by `exclude` will not produce diagnostics anywhere, regardless of `diagnosticMode`.
- `include` defaults to the workspace root; if you set it explicitly to a subfolder, files outside that subfolder become invisible to diagnostics.
- Files filtered out by [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md) are still analyzed for diagnostics; the limit only affects indexing for auto-imports and symbol search. See [How to Tune Pylance Performance](performance-tuning.md).

---

## Diagnostic Checklist

Use this when "Pylance is missing errors" is the complaint:

1. Confirm `python.analysis.diagnosticMode` with `pylanceSettings`.
2. Confirm the file is in `pylanceWorkspaceUserFiles`.
3. Run `pylanceLSP` `workspace/diagnostic` (or `textDocument/diagnostic` for a single file) and inspect the result.
4. If the expected errors are still missing, check `pylanceSettings` for `include` / `exclude`, [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md), and any `pyrightconfig.json` overrides.
5. If you only need a one-time sweep, prefer the LSP request over flipping the setting.

---

## FAQ

### Q: Why do my errors disappear when I close the file?

`openFilesOnly` only publishes diagnostics for currently open files. Closing the file removes its diagnostics from the Problems panel. The errors will reappear when you reopen the file. To see them continuously, switch to `"workspace"` or use `pylanceLSP` `workspace/diagnostic` on demand.

### Q: Is `workspace/diagnostic` slower than the editor?

It usually is on first call, because Pylance has to type-check files it had not analyzed yet. Subsequent calls are typically faster &mdash; the in-memory program retains analysis state for files that have not changed, so unchanged files do not need to be re-checked &mdash; but Pylance does not maintain a separate persisted cache of closed-file diagnostics, and any file change invalidates dependent results. For very large workspaces, prefer running [`pyright`](https://github.com/microsoft/pyright) in CI for build gating instead of repeatedly issuing `workspace/diagnostic`.

### Q: Can I limit `workspace/diagnostic` to a folder?

Not via the LSP request itself &mdash; it always covers the language server's view of the workspace. Limit scope by changing `include` / `exclude`, by opening a smaller folder as the workspace, or by running `pyright path/to/folder` from a terminal.

### Q: I switched to `"workspace"` and the editor became unresponsive. What now?

Switch back to `"openFilesOnly"` and either run `pylanceLSP` `workspace/diagnostic` on demand, or run `pyright` in a terminal. Tighten [`exclude`](../settings/python_analysis_exclude.md) to drop folders that should not be analyzed (vendored code, generated outputs, large test fixtures), and consider [`languageServerMode`](../settings/python_analysis_languageServerMode.md) `"light"` for very large workspaces. See [How to Tune Pylance Performance](performance-tuning.md). Note: [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md) only affects indexing for auto-imports and symbol search, so it does not change the cost of `"workspace"` diagnostic mode.

### Q: Should Copilot just flip `diagnosticMode` to `"workspace"` to see everything?

No. The non-destructive answer is `pylanceLSP` `workspace/diagnostic`. Changing the user's settings should be an explicit ask, not a side effect of running a diagnosis. See [How to Fix Pylance Issues with Copilot](copilot-pylance-workflow.md).

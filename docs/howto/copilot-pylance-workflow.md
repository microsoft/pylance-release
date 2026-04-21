# How to Fix Pylance Issues with Copilot

Pylance ships a set of MCP tools that let GitHub Copilot (and any other MCP client) inspect your Python project the same way Pylance does in the editor: it can resolve interpreters, list user files, ask the language server for diagnostics, apply refactorings, and run code against the active environment.

This guide is the canonical entry point for Copilot when fixing Pylance + VS Code problems. It maps common symptoms to the right tool, explains the order to call them in, and links out to topic-specific guides.

The workflows here also work for humans driving Copilot Chat: ask Copilot to use a named tool, or ask it to "diagnose Pylance issues in this workspace" and let it pick.

---

## Table of Contents

- [When to Use This Guide](#when-to-use-this-guide)
- [Pylance MCP Tools at a Glance](#pylance-mcp-tools-at-a-glance)
- [Standard Diagnosis Loop](#standard-diagnosis-loop)
- [Symptom &rarr; Tool Map](#symptom--tool-map)
- [Workflow Recipes](#workflow-recipes)
    - [Verify the Active Environment and Workspace](#verify-the-active-environment-and-workspace)
    - [Get Diagnostics for One File or the Whole Workspace](#get-diagnostics-for-one-file-or-the-whole-workspace)
    - [Fix Unresolved Imports](#fix-unresolved-imports)
    - [Remove Unused Imports and Run Fix-All](#remove-unused-imports-and-run-fix-all)
    - [Resolve Type Errors](#resolve-type-errors)
    - [Confirm a Hypothesis at Runtime](#confirm-a-hypothesis-at-runtime)
- [Tool Call Conventions](#tool-call-conventions)
- [What Copilot Should Not Do](#what-copilot-should-not-do)
- [Related Guides](#related-guides)

---

## When to Use This Guide

Use this workflow when any of the following is true:

- Pylance shows unexpected errors, missing errors, or wrong import resolution.
- Completions, hovers, or auto-imports are missing or wrong.
- The wrong Python interpreter is selected, or multiple environments are involved.
- You want Copilot to clean up imports, fix simple type errors, or apply other refactorings.
- You want to confirm a static-analysis result against real runtime behavior.

If the user only describes a symptom, Copilot should run [Standard Diagnosis Loop](#standard-diagnosis-loop) before suggesting fixes.

---

## Pylance MCP Tools at a Glance

| Tool                                 | Use it to                                                                                                                        |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `pylanceDocuments`                   | Search and fetch Pylance how-to / settings / diagnostic docs (this guide and others).                                            |
| `pylanceWorkspaceRoots`              | List workspace roots, or find the root that owns a given file.                                                                   |
| `pylanceWorkspaceUserFiles`          | List the user Python files Pylance considers part of the workspace (after include/exclude).                                      |
| `pylancePythonEnvironments`          | List discovered Python interpreters and which one is active per workspace root.                                                  |
| `pylanceUpdatePythonEnvironment`     | Switch the active interpreter for a workspace root.                                                                              |
| `pylanceSettings`                    | Inspect effective `python.analysis.*` settings for a workspace.                                                                  |
| `pylanceFileSyntaxErrors`            | Quickly check parse errors in a single workspace file.                                                                           |
| `pylanceSyntaxErrors`                | Parse-check an arbitrary code snippet without saving a file.                                                                     |
| `pylanceLSP`                         | Issue read-only LSP requests: hover, completion, diagnostics (file or workspace), references, symbols, call/type hierarchy, etc. |
| `pylanceImports`                     | List resolved and unresolved imports across the workspace.                                                                       |
| `pylanceInstalledTopLevelModules`    | List top-level modules importable from the active environment.                                                                   |
| `pylanceInvokeRefactoring`           | Apply automated refactorings (unused imports, fix-all, convert imports, add type annotations, etc.).                             |
| `pylanceCheckSignatureCompatibility` | Verify that all callers of a function still match its current signature.                                                         |
| `pylanceSemanticContext`             | Get rich semantic context (types, related snippets, dependencies) at a cursor position.                                          |
| `pylanceRunCodeSnippet`              | Execute Python code against the workspace's active interpreter.                                                                  |
| `pylancePythonDebug`                 | Launch the debugger to inspect runtime values, breakpoints, and stack frames.                                                    |

These tools all operate against the same in-memory analysis Pylance is using in the editor, so their answers reflect the user's actual VS Code state, not a separate copy.

---

## Standard Diagnosis Loop

When the user reports a Pylance problem, run this loop before guessing.

1. **Ground the workspace.** Call `pylanceWorkspaceRoots` and `pylanceWorkspaceUserFiles` for the affected root. Confirm the workspace root URI and that the file Pylance is complaining about is actually a user file.
2. **Confirm the interpreter.** Call `pylancePythonEnvironments` for the same root. Verify the active interpreter is the one the user expects (right venv, right Python version, right interpreter type).
3. **Inspect settings.** Call `pylanceSettings`. Note any `python.analysis.*` settings that diverge from defaults, especially `extraPaths`, `include`, `exclude`, `diagnosticMode`, `typeCheckingMode`, `languageServerMode`, and `useLibraryCodeForTypes`.
4. **Get diagnostics.** Call `pylanceLSP` with `textDocument/diagnostic` for the file in question, or `workspace/diagnostic` for the whole workspace. See [How to Get Whole-Workspace Diagnostics from Pylance](workspace-vs-open-files-diagnostics.md).
5. **Confirm imports resolve.** If the issue smells like an import problem, call `pylanceImports` and `pylanceInstalledTopLevelModules`. See [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md).
6. **Form a hypothesis, then act.** Apply the smallest fix (refactoring, settings change, environment switch). Re-run step 4 to confirm.

Stop only when diagnostics either disappear or are explicitly accepted by the user.

---

## Symptom &rarr; Tool Map

| Symptom                                                | Start with                                                                                                                                                                                 |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Import "X" could not be resolved`                     | `pylanceWorkspaceRoots` &rarr; `pylancePythonEnvironments` &rarr; `pylanceInstalledTopLevelModules` &rarr; `pylanceImports`. See [Unresolved Imports](unresolved-imports.md).              |
| Wrong interpreter / wrong venv                         | `pylancePythonEnvironments` &rarr; `pylanceUpdatePythonEnvironment`. See [How to Choose a Python Environment for Pylance](python-environments.md).                                         |
| "I only see errors for files I have open"              | `pylanceSettings` (check `diagnosticMode`) &rarr; `pylanceLSP` `workspace/diagnostic`. See [How to Get Whole-Workspace Diagnostics from Pylance](workspace-vs-open-files-diagnostics.md).  |
| Unused imports / formatting cleanup                    | `pylanceInvokeRefactoring` (`source.unusedImports`, `source.fixAll.pylance`).                                                                                                              |
| Wildcard import I want to expand                       | `pylanceInvokeRefactoring` (`source.convertImportStar`).                                                                                                                                   |
| Need types added                                       | `pylanceInvokeRefactoring` (`source.addTypeAnnotation`).                                                                                                                                   |
| Type error I do not understand                         | `pylanceLSP` (`textDocument/hover`, `textDocument/diagnostic`) &rarr; `pylanceSemanticContext` &rarr; optional `pylancePythonDebug` to confirm at runtime.                                 |
| Missing dependency                                     | `pylanceInstalledTopLevelModules` &rarr; install via the user's package manager. See [How to Manage Python Dependencies for Pylance](dependency-management.md).                            |
| Conflicting environments / multiple `requirements.txt` | `pylancePythonEnvironments` &rarr; [How to Choose a Python Environment for Pylance](python-environments.md) and [How to Manage Python Dependencies for Pylance](dependency-management.md). |
| "Pylance does not seem to know about file X"           | `pylanceWorkspaceUserFiles` &rarr; `pylanceSettings` (check `include` / `exclude` / `pyrightconfig.json`).                                                                                 |
| Editor settings change had no effect                   | `pylanceSettings`. See [How to Troubleshoot Pylance Settings](settings-troubleshooting.md).                                                                                                |

---

## Workflow Recipes

### Verify the Active Environment and Workspace

Always start here for any Pylance issue.

1. `pylanceWorkspaceRoots` &mdash; with no arguments to list all roots, or with `fileUri` to find the root that owns a specific file.
2. `pylancePythonEnvironments` for the relevant `workspaceRoot`.
3. If the active interpreter is wrong, call `pylanceUpdatePythonEnvironment` with either an environment value returned by `pylancePythonEnvironments`, or the absolute path to a Python executable.
4. Re-check diagnostics after switching &mdash; many Pylance "errors" are simply the wrong interpreter selected.

See [How to Choose a Python Environment for Pylance](python-environments.md).

### Get Diagnostics for One File or the Whole Workspace

For a single file, prefer the LSP path because it returns the same diagnostics the editor shows:

```jsonc
// pylanceLSP
{
    "method": "textDocument/diagnostic",
    "params": { "textDocument": { "uri": "file:///path/to/file.py" } },
}
```

For the whole workspace, ask LSP directly. This works even when `python.analysis.diagnosticMode` is `"openFilesOnly"` because the LSP request targets all known files:

```jsonc
// pylanceLSP
{
    "method": "workspace/diagnostic",
    "params": {},
}
```

`pylanceFileSyntaxErrors` is a fast sanity check for parse errors in a single file (no type checking). `pylanceSyntaxErrors` does the same for an unsaved code snippet.

See [How to Get Whole-Workspace Diagnostics from Pylance](workspace-vs-open-files-diagnostics.md).

### Fix Unresolved Imports

1. Confirm the interpreter with `pylancePythonEnvironments`.
2. Call `pylanceInstalledTopLevelModules` for that environment to see whether the module is actually importable.
3. Call `pylanceImports` to see what Pylance currently treats as resolved vs unresolved across the workspace.
4. If the package is installed but Pylance does not see it, the issue is almost always one of:
    - Wrong interpreter (fix with `pylanceUpdatePythonEnvironment`).
    - Missing or wrong `extraPaths` / `include` (inspect with `pylanceSettings`).
    - A `pyrightconfig.json` or `pyproject.toml` overriding VS Code settings.
5. If the package is not installed, install it in the active environment using the user's package manager.

See [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md), [How to Troubleshoot Pylance Settings](settings-troubleshooting.md), and [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md).

### Remove Unused Imports and Run Fix-All

`pylanceInvokeRefactoring` exposes the same source actions VS Code does, plus a few extras:

- `source.unusedImports` &mdash; remove every unused `import` from a file.
- `source.fixAll.pylance` &mdash; run every action listed in the `python.analysis.fixAll` array setting (a subset of `source.unusedImports`, `source.convertImportFormat`, `source.convertImportStar`, `source.addTypeAnnotation`). This is the same code action VS Code's `editor.codeActionsOnSave` invokes when the user opts into fix-on-save, but the two are configured independently &mdash; calling `source.fixAll.pylance` runs whatever is in `python.analysis.fixAll` regardless of any save-time configuration.
- `source.convertImportFormat` &mdash; flip absolute &harr; relative imports per `python.analysis.importFormat`.
- `source.convertImportStar` &mdash; expand `from x import *` into explicit names.
- `source.convertImportToModule` &mdash; turn `from x import a, b` into `import x` plus qualified references.
- `source.renameShadowedStdlibImports` &mdash; rename local modules that shadow stdlib names.
- `source.addTypeAnnotation` &mdash; add inferred annotations to variables and functions.

Each refactoring takes a single `fileUri` and an optional `mode`:

- `mode: "edits"` returns a `WorkspaceEdit` without touching the editor. Useful for previewing or for "does this file actually need cleanup?" checks.
- `mode: "string"` returns the rewritten file as text.
- `mode: "update"` (default) applies a `WorkspaceEdit` to the editor. **It does not write to disk.** The change appears as an unsaved edit in the active editor. Copilot must explicitly save the file (for example by calling the host's save-file action) for the change to land on disk. Skipping the save step is a frequent source of "the refactoring did nothing" confusion.

For multi-file cleanup, iterate `pylanceWorkspaceUserFiles`, call `pylanceInvokeRefactoring` per file, save each file, and then re-run `pylanceLSP` `workspace/diagnostic` to confirm.

### Resolve Type Errors

1. Get the exact diagnostic with `pylanceLSP` `textDocument/diagnostic`. Note the rule name (for example `reportArgumentType`).
2. Read the rule page through `pylanceDocuments`: `path: "diagnostics/<reportName>.md"`. The rule page explains what triggers it and the canonical fixes.
3. Use `pylanceLSP` `textDocument/hover` at the failing position to get the inferred types.
4. Use `pylanceSemanticContext` for the position when you need surrounding code, base types, override sites, and project traits.
5. Decide between, in order of preference:
    1. **Fixing the code** so the types line up.
    2. **Narrowing the type** with `isinstance`, `is None`, `assert`, or a type guard. See [How to Use Type Narrowing](type-narrowing.md).
    3. **Adjusting annotations** (more precise input types, `TypeGuard`, `cast`, `assert_type`).
    4. **Suppressing in source** for a single line that is genuinely correct but not provable. Two forms:
        - `# type: ignore[ruleName]` &mdash; the standard typing-PEP comment, honored by Pylance and other type checkers.
        - `# pyright: ignore[ruleName]` &mdash; Pyright/Pylance-specific. Prefer this when you only want to silence Pylance/Pyright and keep the diagnostic visible to other tools.
          Always pin the rule name in brackets so the suppression does not also hide unrelated future errors. Add a brief comment explaining why the suppression is safe.
    5. **Project-wide rule changes** via [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) or [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md). Reserve this for rules that are genuinely wrong for the project, not for one-off failures.
6. After editing, re-run `textDocument/diagnostic` for the same file.

For changes to a function's signature, run `pylanceCheckSignatureCompatibility` at the function's name position to verify that all existing callers still match the new shape.

### Confirm a Hypothesis at Runtime

Static analysis is necessary but not sufficient. When a type error or unresolved import looks wrong, confirm with the actual interpreter:

- `pylanceRunCodeSnippet` &mdash; run a short script against the active environment. Useful to check what is importable, what an object's type really is, or what an attribute resolves to.
- `pylancePythonDebug` &mdash; launch the debugger, set breakpoints, and inspect values mid-execution. Use this when the bug only reproduces with real input.

A common pattern: `pylanceLSP` says a value is `Optional[int]` and you do not believe it. Run a `pylanceRunCodeSnippet` that imports the module and prints `type(...)` to confirm. If runtime disagrees with static, the fix is usually a missing annotation, a missing stub, or a shadowing import &mdash; not a Pylance bug.

---

## Tool Call Conventions

These conventions apply to every tool call:

- `workspaceRoot` is a directory URI. On Windows the canonical form is `file:///c:/path/to/workspace` (lowercase drive letter, forward slashes).
- `fileUri` is a file URI, for example `file:///c:/path/to/workspace/pkg/module.py`. Files outside any workspace root are typically rejected.
- LSP `position` and `range` use 0-based `line` and `character`.
- Pylance only reports user files; library and dependency files are excluded from diagnostics and from `pylanceWorkspaceUserFiles`.
- Always pass an explicit `workspaceRoot` when the tool accepts one. Do not assume the current working directory.

When in doubt, run `pylanceWorkspaceRoots` first to capture the canonical root URI, then reuse that string in subsequent calls.

---

## What Copilot Should Not Do

- Do not infer the active interpreter from `which python` / `where python`. Use `pylancePythonEnvironments`.
- Do not run `pip install` to "fix" an unresolved import without first confirming the active environment with `pylancePythonEnvironments`. Installing into the wrong environment will not change Pylance's behavior.
- Do not blanket-suppress diagnostics with bare `# type: ignore` (no rule name) or [`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) before understanding the rule. Read the rule page via `pylanceDocuments` first, and prefer rule-pinned suppressions like `# type: ignore[reportArgumentType]` or `# pyright: ignore[reportArgumentType]` when suppression is justified.
- Do not assume `pylanceInvokeRefactoring` `mode: "update"` persists changes &mdash; it leaves the file dirty in the editor. Always save explicitly after editing, then re-check diagnostics.
- Do not edit `pyrightconfig.json` or `pyproject.toml` to override VS Code settings unless the user asked for project-level configuration. Many `python.analysis.*` settings are silently ignored when a config file exists (see [How to Troubleshoot Pylance Settings](settings-troubleshooting.md)).
- Do not assume `pylanceRunCodeSnippet` succeeded means the import will resolve in Pylance. The two paths can disagree when the runtime uses import hooks or `.pth` tricks. See [How to Use Editable Installs with Pylance](editable-installs.md).

---

## Related Guides

- [How to Choose a Python Environment for Pylance](python-environments.md)
- [How to Manage Python Dependencies for Pylance](dependency-management.md)
- [How to Get Whole-Workspace Diagnostics from Pylance](workspace-vs-open-files-diagnostics.md)
- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md)
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md)
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md)
- [How to Tune Pylance Performance](performance-tuning.md)
- [How to Use Type Narrowing](type-narrowing.md)
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md)

# How to Troubleshoot Pylance Settings

Pylance reads configuration from multiple sources with specific precedence rules. When settings don't take effect, it's often because a higher-priority source is overriding them. This guide explains the precedence rules, common conflicts, and how to diagnose them.

---

## Table of Contents

- [Configuration Sources and Precedence](#configuration-sources-and-precedence)
- [pyrightconfig.json Overrides VS Code Settings](#pyrightconfigjson-overrides-vs-code-settings)
- [languageServerMode Default Overrides](#languageservermode-default-overrides)
- [VS Code Settings Scopes](#vs-code-settings-scopes)
- [Variable Substitution](#variable-substitution)
- [Common Problematic Combinations](#common-problematic-combinations)
- [Settings Not Taking Effect](#settings-not-taking-effect)
- [Diagnostics Missing for Some Files](#diagnostics-missing-for-some-files)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)

---

## Configuration Sources and Precedence

Pylance reads settings from these sources, listed from **highest** to **lowest** priority:

| Priority | Source                                                                                                           | Scope                                                                |
| -------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1        | [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` `[tool.pyright]` | Per-project (many VS Code settings are **ignored** when this exists) |
| 2        | `.vscode/settings.json` (workspace folder)                                                                       | Per-folder in multi-root workspaces                                  |
| 3        | `.code-workspace` file settings                                                                                  | Per-workspace                                                        |
| 4        | User settings (`settings.json`)                                                                                  | Global                                                               |
| 5        | [`languageServerMode`](../settings/python_analysis_languageServerMode.md) defaults                               | Implicit defaults set by the selected mode                           |

---

## pyrightconfig.json Overrides VS Code Settings

When a [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) or `pyproject.toml` (with `[tool.pyright]`) exists in a workspace folder, the following VS Code settings **are ignored** — the config file takes precedence:

| Ignored VS Code Setting                                                                                     | Where to Set Instead                                                                                      |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md)                                   | `"extraPaths"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)             |
| [`python.analysis.include`](../settings/python_analysis_include.md)                                         | `"include"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                |
| [`python.analysis.exclude`](../settings/python_analysis_exclude.md)                                         | `"exclude"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                |
| [`python.analysis.ignore`](../settings/python_analysis_ignore.md)                                           | `"ignore"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)                 |
| [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)                       | `"typeCheckingMode"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)       |
| [`python.analysis.stubPath`](../settings/python_analysis_stubPath.md)                                       | `"stubPath"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)               |
| [`python.analysis.useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md)           | `"useLibraryCodeForTypes"` in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) |
| [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) | `"reportXxx"` rules in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration)        |

Pylance shows a **yellow warning squiggle** in `settings.json` for any setting that a config file overrides. The warning message reads: _"python.analysis.extraPaths cannot be set when a Pyrightconfig.json or pyproject.toml is being used."_

---

## languageServerMode Default Overrides

[`languageServerMode`](../settings/python_analysis_languageServerMode.md) sets defaults for several settings. You can **override any individual setting** even when a mode is active — the mode only sets defaults, it doesn't lock them.

| Setting                                                                           | `"light"` Default | `"default"` Default | `"full"` Default |
| --------------------------------------------------------------------------------- | ----------------- | ------------------- | ---------------- |
| [`exclude`](../settings/python_analysis_exclude.md)                               | `["**"]`          | `[]`                | `[]`             |
| [`indexing`](../settings/python_analysis_indexing.md)                             | `false`           | `true`              | `true`           |
| [`typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md)             | `"off"`           | `"off"`             | (unchanged)      |
| [`useLibraryCodeForTypes`](../settings/python_analysis_useLibraryCodeForTypes.md) | `false`           | `true`              | `true`           |
| [`autoImportCompletions`](../settings/python_analysis_autoImportCompletions.md)   | (unchanged)       | `false`             | `true`           |
| [`userFileIndexingLimit`](../settings/python_analysis_userFileIndexingLimit.md)   | (unchanged)       | `2000`              | `-1` (unlimited) |

See [How to Tune Pylance Performance](performance-tuning.md) for guidance on choosing a mode.

---

## VS Code Settings Scopes

VS Code settings can be set at different scopes, each overriding the previous:

| Scope         | Location                                                                                     | When to Use                                         |
| ------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **User**      | `~/.config/Code/User/settings.json` (Linux) or `%APPDATA%\Code\User\settings.json` (Windows) | Personal defaults                                   |
| **Workspace** | `.code-workspace` file → `"settings"` block                                                  | Shared across all folders in a multi-root workspace |
| **Folder**    | `.vscode/settings.json` in a workspace folder                                                | Per-project settings                                |

In multi-root workspaces, folder-level settings override workspace-level settings, which override user-level settings.

### Variable Substitution

VS Code settings support these variables:

| Variable                                               | Resolves To                           | Notes                                                          |
| ------------------------------------------------------ | ------------------------------------- | -------------------------------------------------------------- |
| `${workspaceFolder}`                                   | Root of the current workspace folder  | In multi-root, refers to the folder the setting is in          |
| `${workspaceFolder:folderName}`                        | Root of the named workspace folder    | Useful for cross-folder references in `.code-workspace` files  |
| `${env:HOME}`, `${env:USERNAME}`, `${env:VIRTUAL_ENV}` | Value of these specific env vars only | Only these three are supported — arbitrary `${env:VAR}` is not |

> **Note**: [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) does **not** support VS Code variable substitution. Paths in config files are relative to the config file location.

---

## Common Problematic Combinations

| Combination                                                                                                                               | What Happens                                                                                                            | Fix                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `light` mode + `diagnosticMode: "workspace"`                                                                                              | `exclude: ["**"]` means no files are discovered, so `"workspace"` mode has nothing to analyze                           | Either switch to `"default"` mode, or explicitly set `exclude` to a narrower pattern                                                               |
| `light` mode + `indexing: true` (explicit)                                                                                                | Works — indexing is enabled because you explicitly set it. But `exclude: ["**"]` limits what gets indexed to open files | Also explicitly set `exclude` to include the directories you need                                                                                  |
| Config file exists + `extraPaths` in `settings.json`                                                                                      | VS Code setting ignored, yellow warning squiggle                                                                        | Move `extraPaths` into the config file                                                                                                             |
| `autoSearchPaths: true` + [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) | Auto-detected `src/` only applies to the **default** environment, not explicitly defined ones                           | Add `"src"` to each environment's `extraPaths`                                                                                                     |
| `useNearestConfiguration: true` + `exclude: ["**"]`                                                                                       | All virtual workspaces are excluded                                                                                     | Set `exclude` to only what you actually want excluded                                                                                              |
| Multi-root (>10 folders) + `diagnosticMode: "workspace"`                                                                                  | Each folder analyzes all its files — combined memory can exceed 8 GB heap limit                                         | Use `"openFilesOnly"` or switch to [`executionEnvironments`](https://microsoft.github.io/pyright/#/configuration?id=execution-environment-options) |
| Global `extraPaths` in config + `executionEnvironments[].extraPaths`                                                                      | Each execEnv's `extraPaths` **replaces** (not merges with) the global `extraPaths` for files in that environment        | Repeat common paths in each environment's `extraPaths`                                                                                             |

---

## Settings Not Taking Effect

**Symptom**: Changed a setting but Pylance behavior didn't change.

### Common Causes

| Cause                                                                                                  | Fix                                                                                             |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) overrides VS Code settings | Edit the config file instead (see [table above](#pyrightconfigjson-overrides-vs-code-settings)) |
| Setting is in wrong scope (user vs workspace)                                                          | Move to workspace or folder scope                                                               |
| Multi-root: setting is in wrong folder                                                                 | Check which folder's settings apply                                                             |
| [`languageServerMode`](../settings/python_analysis_languageServerMode.md) override                     | Explicitly set the individual setting to override the mode default                              |
| Pylance needs restart                                                                                  | Run **"Python: Restart Language Server"** from the Command Palette                              |

---

## Diagnostics Missing for Some Files

**Symptom**: No errors, warnings, or IntelliSense for some files.

### Checks

1. Is [`diagnosticMode`](../settings/python_analysis_diagnosticMode.md) set to `"openFilesOnly"`? → Only open files get diagnostics
2. Is the file in [`python.analysis.exclude`](../settings/python_analysis_exclude.md)? → Remove it from exclude
3. Is [`python.analysis.include`](../settings/python_analysis_include.md) set? → Setting [`include`](../settings/python_analysis_include.md) overrides the default (all files). Make sure your file is covered.
4. Is [`languageServerMode`](../settings/python_analysis_languageServerMode.md) set to `"light"`? → In light mode, [`exclude`](../settings/python_analysis_exclude.md) defaults to `["**"]`, so only open files are analyzed

---

## Diagnostic Checklist

When settings aren't working as expected:

- [ ] **Config file check**: Does a `pyrightconfig.json` or `pyproject.toml` with `[tool.pyright]` exist? (If so, many VS Code settings are ignored)
- [ ] **Yellow squiggles**: Look for warning squiggles in your `settings.json` — they indicate overridden settings
- [ ] **Setting scope**: Is the setting at the right level (user / workspace / folder)?
- [ ] **Language server mode**: Is a mode active that changes defaults?
- [ ] **Restart**: Run "Python: Restart Language Server" after any configuration change
- [ ] **Pylance output**: Check **Output → Pylance** for errors or config warnings
- [ ] **Trace logging**: Enable `"python.analysis.logLevel": "Trace"` and look for which settings are in effect. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md)

---

## FAQ

### Q: How do I use `diagnosticSeverityOverrides` when a config file exists?

[`diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) set in VS Code `settings.json` are **ignored** if a `pyrightconfig.json` or `[tool.pyright]` section exists. Move overrides into the config file:

```json
// pyrightconfig.json
{
    "reportMissingModuleSource": "none",
    "reportMissingTypeStubs": "warning"
}
```

### Q: What's the difference between `include`, `exclude`, and `ignore`?

| Setting                                                    | Effect on File Discovery | Effect on Diagnostics  | Effect on Import Resolution                                                         |
| ---------------------------------------------------------- | ------------------------ | ---------------------- | ----------------------------------------------------------------------------------- |
| Not in [`include`](../settings/python_analysis_include.md) | Not discovered           | No diagnostics         | Not resolved as workspace file                                                      |
| In [`exclude`](../settings/python_analysis_exclude.md)     | Not discovered           | No diagnostics         | Not resolved as workspace file (but still resolved if imported by an included file) |
| In [`ignore`](../settings/python_analysis_ignore.md)       | Discovered & analyzed    | Diagnostics suppressed | Resolved normally                                                                   |

### Q: Does `autoSearchPaths` work with execution environments?

[`autoSearchPaths`](../settings/python_analysis_autoSearchPaths.md) (default: `true`) auto-adds a `src/` directory to the search path if it exists and doesn't contain `__init__.py`. When execution environments are defined in a config file, the auto-detected `src/` path goes into the default execution environment but **does not** automatically apply to explicitly defined execution environments. Add `src` to each environment's [`extraPaths`](../settings/python_analysis_extraPaths.md) if needed.

---

## Related Guides

- [How to Tune Pylance Performance](performance-tuning.md) — language server mode, indexing, and heap settings
- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution order and diagnostic fixes
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) — trace logging for diagnosing setting effects
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — multi-root and execution environment setup

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

---
name: pylance-type-checking-setup
description: Configure Pylance/Pyright type-checking strictness and scope in VS Code. Use when setting typeCheckingMode (off/basic/standard/strict), per-rule diagnosticSeverityOverrides, languageServerMode, pyrightVersion pinning, or reconciling settings.json vs pyrightconfig.json vs pyproject.toml [tool.pyright]. Triggers on "configure pylance", "enable strict type checking", "typeCheckingMode", "diagnosticSeverityOverrides", "pyright config", "settings precedence".
---

# Pylance type-checking setup & configuration

This skill configures *how strict* Pylance/Pyright is and *how settings are resolved*. For what each diagnostic rule means, see the `pylance-diagnostics-triage` skill. For moving a codebase to strict gradually, see `pylance-strict-migration`.

## The four type-checking modes

`python.analysis.typeCheckingMode` is the baseline strictness preset (default `off`). Each level adds rules on top of the previous:

- **`off`** — No broad type-checking pass; still reports unresolved imports and undefined variables.
- **`basic`** — Catches common mistakes (argument/assignment/return mismatches, Optional-member access).
- **`standard`** — Adds more rules on top of `basic`.
- **`strict`** — The strictest default rule set.

**Read the authoritative mode→rule table** to know exactly which rules each level enables: [../../docs/settings/python_analysis_typeCheckingMode.md](../../docs/settings/python_analysis_typeCheckingMode.md).

## Overriding individual rules without changing mode

Use `python.analysis.diagnosticSeverityOverrides` to raise/lower one rule without shifting the whole mode. Values: `error`, `warning`, `information`, `none`, `true` (= `error`), `false` (= `none`).

```jsonc
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "error",
    "reportGeneralTypeIssues": "warning",
    "reportUnknownVariableType": "none"   // keep basic mode but silence one strict-family rule
  }
}
```

Full accepted-values and pyrightconfig interaction: [../../docs/settings/python_analysis_diagnosticSeverityOverrides.md](../../docs/settings/python_analysis_diagnosticSeverityOverrides.md).

## Language server mode

`languageServerMode` (`light`/`default`/`full`) trades features for performance — separate from type-checking strictness. Detail: [../../docs/settings/python_analysis_languageServerMode.md](../../docs/settings/python_analysis_languageServerMode.md).

## Pinning a Pyright version

`python.analysis.pyrightVersion` pins the Pyright version that produces diagnostics, useful for matching CI. `useNearestConfiguration` changes which config file applies per directory. See [../../docs/settings/python_analysis_pyrightVersion.md](../../docs/settings/python_analysis_pyrightVersion.md) and [../../docs/settings/python_analysis_useNearestConfiguration.md](../../docs/settings/python_analysis_useNearestConfiguration.md).

## Config-file precedence & conflicts

Three sources can define settings; precedence and override quirks (why an override seems ignored) are the most common config bug:

- `.vscode/settings.json` — `python.analysis.*`
- `pyrightconfig.json` — Pyright-native keys (e.g. `typeCheckingMode`, rule names directly)
- `pyproject.toml` — `[tool.pyright]`

Diagnose precedence and conflicts: [../../docs/howto/settings-troubleshooting.md](../../docs/howto/settings-troubleshooting.md).

## Pylance vs standalone Pyright

Defaults differ between the Pylance extension and a standalone Pyright install (e.g. `typeCheckingMode` `off` vs `standard`, `autoSearchPaths`, `extraPaths`/`PYTHONPATH` handling). When matching editor diagnostics to CLI/CI, reconcile: [../../USING_WITH_PYRIGHT.md](../../USING_WITH_PYRIGHT.md).

## A real example config

[../../testing/single/pyrightconfig.json](../../testing/single/pyrightconfig.json) shows `executionEnvironments` with per-env `extraPaths`, rule severities, and `typeCheckingMode: basic`. The matching VS Code settings: [../../testing/single/.vscode/settings.json](../../testing/single/.vscode/settings.json).

## Related skills

- **pylance-diagnostics-triage** — what each `report*` rule means and how to suppress it.
- **pylance-strict-migration** — phased path from `off` to `strict`.
- **pylance-import-resolution** — path/interpreter settings that imports depend on.

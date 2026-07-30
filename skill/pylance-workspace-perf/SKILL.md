---
name: pylance-workspace-perf
description: Control which files Pylance checks and keep it fast. Use for diagnosticMode (openFilesOnly vs workspace), include/exclude/ignore, monorepo/multi-root setup, reducing CPU/memory, reading logs, and notebook/remote (SSH/WSL/container) type checking. Triggers on "whole workspace diagnostics", "diagnosticMode", "pylance slow", "memory", "exclude", "monorepo", "notebook", "SSH", "WSL".
---

# Pylance workspace scope & performance

Control *which files* Pylance analyzes and *keep it fast*. For import-path config, see `pylance-import-resolution`; for strictness, see `pylance-type-checking-setup`.

## openFilesOnly vs workspace

`diagnosticMode` (default `openFilesOnly`) controls scope. `openFilesOnly` only checks files you open — fast, but you won't see errors elsewhere. `workspace` checks everything — complete, but heavier. Trade-off and how to get whole-workspace diagnostics on demand: [../../docs/howto/workspace-vs-open-files-diagnostics.md](../../docs/howto/workspace-vs-open-files-diagnostics.md). Setting page: [../../docs/settings/python_analysis_diagnosticMode.md](../../docs/settings/python_analysis_diagnosticMode.md).

## File scope settings

- [include](../../docs/settings/python_analysis_include.md) — which paths to analyze.
- [exclude](../../docs/settings/python_analysis_exclude.md) — paths to skip.
- [ignore](../../docs/settings/python_analysis_ignore.md) — suppress diagnostics on a path without excluding it.
- [useDefaultExcludes](../../docs/settings/python_analysis_useDefaultExcludes.md) — the built-in default excludes (`.git`, `venv`, etc.; additive).
- [excludeLibraryDiagnostics](../../docs/settings/python_analysis_excludeLibraryDiagnostics.md) — hide third-party diagnostics.

## Monorepo / multi-root

Configure execution environments with per-root `extraPaths` and cross-project resolution: [../../docs/howto/monorepo-setup.md](../../docs/howto/monorepo-setup.md). Example config: [../../testing/single/pyrightconfig.json](../../testing/single/pyrightconfig.json).

## Performance

Reduce CPU/memory: indexing limits, excludes, `languageServerMode`, `nodeExecutable`. Guide: [../../docs/howto/performance-tuning.md](../../docs/howto/performance-tuning.md). Key settings:

- [indexing](../../docs/settings/python_analysis_indexing.md), [packageIndexDepths](../../docs/settings/python_analysis_packageIndexDepths.md), [userFileIndexingLimit](../../docs/settings/python_analysis_userFileIndexingLimit.md)
- [nodeExecutable](../../docs/settings/python_analysis_nodeExecutable.md), [languageServerMode](../../docs/settings/python_analysis_languageServerMode.md)

FAQ on memory tuning: [../../FAQ.md](../../FAQ.md).

## Debugging with logs

Trace logging to diagnose import resolution and settings issues: [../../docs/howto/reading-pylance-logs.md](../../docs/howto/reading-pylance-logs.md).

## Notebooks & remote

- Jupyter notebooks: [../../docs/howto/notebook-troubleshooting.md](../../docs/howto/notebook-troubleshooting.md)
- SSH/WSL/containers/Codespaces: [../../docs/howto/remote-development.md](../../docs/howto/remote-development.md)
- Auto-import (indexing-driven): [../../docs/howto/auto-import-guide.md](../../docs/howto/auto-import-guide.md)

## Related skills

- **pylance-import-resolution** — `extraPaths`/interpreter config that imports depend on.
- **pylance-type-checking-setup** — `languageServerMode` and config precedence.
- **pylance-diagnostics-triage** — silencing noise via `exclude`/`ignore` vs per-rule severity.

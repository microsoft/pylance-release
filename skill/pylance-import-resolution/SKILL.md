---
name: pylance-import-resolution
description: Fix unresolved-import and missing-stub errors in Pylance/Pyright. Use for "Import ... could not be resolved", reportMissingImports, reportMissingModuleSource, reportMissingTypeStubs, and configuring extraPaths, autoSearchPaths, stubPath, typeshedPaths, useLibraryCodeForTypes, editable installs, or interpreter selection. Triggers on "unresolved import", "extraPaths", "stub", "py.typed", "editable install", "interpreter", "venv".
---

# Pylance import resolution

Fixes for `Import "..." could not be resolved` and related import/stub errors. **The single most common Pylance pain point.** For the specific diagnostic rules involved, see `pylance-diagnostics-triage`. For monorepo cross-project paths, see `pylance-workspace-perf`.

## How Pylance resolves imports

Pylance mimics Python's import mechanism for static analysis: it searches a constructed `sys.path` (interpreter site-packages + stdlib + configured paths). If a module isn't on that path, you get `reportMissingImports`. Background: [../../docs/howto/unresolved-imports.md](../../docs/howto/unresolved-imports.md) and the deep-dive in [../../docs/settings/python_analysis_extraPaths.md](../../docs/settings/python_analysis_extraPaths.md).

## Decision tree

1. **Wrong interpreter?** The #1 cause. A selected venv/conda/uv/poetry environment must actually contain the package. Pick/switch interpreters per [../../docs/howto/python-environments.md](../../docs/howto/python-environments.md). Reconcile declared deps: [../../docs/howto/dependency-management.md](../../docs/howto/dependency-management.md).
2. **Your own code in a non-standard layout (e.g. `src/` layout)?** Add it to `extraPaths`. Glob patterns and ordering: [../../docs/howto/extra-paths-glob-resolution.md](../../docs/howto/extra-paths-glob-resolution.md).
3. **Third-party lib missing type info?** Install stubs (`pip install types-requests`) or put custom `.pyi` in `stubPath`, or let Pylance infer from source via `useLibraryCodeForTypes`. Override bundled stubs: [../../docs/howto/bundled-stubs.md](../../docs/howto/bundled-stubs.md).
4. **`pip install -e` not resolvable?** Editable installs (PEP 660): [../../docs/howto/editable-installs.md](../../docs/howto/editable-installs.md).
5. **Still stuck?** Trace logs: [../../docs/howto/reading-pylance-logs.md](../../docs/howto/reading-pylance-logs.md); root troubleshooting: [../../TROUBLESHOOTING.md](../../TROUBLESHOOTING.md).

## Path & stub settings (one page each)

- [extraPaths](../../docs/settings/python_analysis_extraPaths.md) — additional import-resolution directories
- [autoSearchPaths](../../docs/settings/python_analysis_autoSearchPaths.md) — auto-detect `src/`
- [stubPath](../../docs/settings/python_analysis_stubPath.md) — custom `.pyi` location
- [typeshedPaths](../../docs/settings/python_analysis_typeshedPaths.md) — custom typeshed
- [useLibraryCodeForTypes](../../docs/settings/python_analysis_useLibraryCodeForTypes.md) — infer types from library source when stubs missing (the type-inference lever)
- [enableEditableInstalls](../../docs/settings/python_analysis_enableEditableInstalls.md) — resolve PEP 660 on Python 3.13+
- [importFormat](../../docs/settings/python_analysis_importFormat.md) — absolute vs relative in auto-imports

## Quick fixes users often apply

```jsonc
// .vscode/settings.json
{
  "python.analysis.extraPaths": ["./src", "./lib"]
}
```

```python
# Optional / platform-specific import — suppress the diagnostic
try:
    import optional_module  # pyright: ignore[reportMissingImports]
except ImportError:
    optional_module = None
```

## Related skills

- **pylance-diagnostics-triage** — details on `reportMissingImports`, `reportMissingModuleSource`, `reportMissingTypeStubs`, `reportIncompleteStub`, `reportPrivateImportUsage`, `reportImportCycles`.
- **pylance-workspace-perf** — monorepo/multi-root `extraPaths` and execution environments.
- **pylance-type-checking-setup** — config-file precedence (why `extraPaths` might be ignored).

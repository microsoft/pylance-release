---
name: pylance-strict-migration
description: Move a Python codebase from off/basic to strict type checking incrementally with Pylance/Pyright. Use for per-file "# pyright: strict" comments, per-directory strict arrays in pyrightconfig.json, CI enforcement, and quieting the reportUnknown* rule family. Triggers on "move to strict", "gradual strict adoption", "enable strict mode", "reportUnknownVariableType", "reportUnknownParameterType", "typeEvaluation strict".
---

# Migrating to strict type checking

A phased path from `off`/`basic` to `strict`. For what individual rules mean, see `pylance-diagnostics-triage`. For the modes themselves, see `pylance-type-checking-setup`.

## The 5-phase strategy

Authoritative walkthrough: [../../docs/howto/gradual-strict-adoption.md](../../docs/howto/gradual-strict-adoption.md). In summary:

1. Start at `basic` workspace-wide; fix the common mistakes (argument/assignment/return, Optional-member access).
2. Opt individual files into `strict` via the `# pyright: strict` comment at the top of a file.
3. Promote directories: add them to the `strict` array in `pyrightconfig.json` so whole subtrees are strict.
4. Quiet the `reportUnknown*` family by adding annotations (not by silencing).
5. Flip the workspace default to `strict` once most code is clean.

## Per-file / per-directory strict

```python
# pyright: strict
```

```jsonc
// pyrightconfig.json
{
  "typeCheckingMode": "basic",
  "strict": ["src/core", "src/api"],
  "strictListInference": true,
  "strictDictionaryInference": true
}
```

Per-file/per-directory commentary and common rule suppressions: [../../docs/howto/gradual-strict-adoption.md](../../docs/howto/gradual-strict-adoption.md).

## The reportUnknown* family

Strict mode leans heavily on these. Address them by adding type annotations rather than disabling:

- [reportUnknownVariableType](../../docs/diagnostics/reportUnknownVariableType.md)
- [reportUnknownArgumentType](../../docs/diagnostics/reportUnknownArgumentType.md)
- [reportUnknownParameterType](../../docs/diagnostics/reportUnknownParameterType.md)
- [reportUnknownMemberType](../../docs/diagnostics/reportUnknownMemberType.md)
- [reportUnknownLambdaType](../../docs/diagnostics/reportUnknownLambdaType.md)

Common culprit: unannotated function returns/params. The `analyzeUnannotatedFunctions` setting controls whether unannotated functions are analyzed at all.

## Strict inference settings (typeEvaluation.*)

These sharpen Pylance's inference and are the levers behind strict-mode noise:

- [strictDictionaryInference](../../docs/settings/python_analysis_typeEvaluation_strictDictionaryInference.md)
- [strictListInference](../../docs/settings/python_analysis_typeEvaluation_strictListInference.md)
- [strictSetInference](../../docs/settings/python_analysis_typeEvaluation_strictSetInference.md)
- [strictParameterNoneValue](../../docs/settings/python_analysis_typeEvaluation_strictParameterNoneValue.md)
- [analyzeUnannotatedFunctions](../../docs/settings/python_analysis_typeEvaluation_analyzeUnannotatedFunctions.md)

Mode table: [../../docs/settings/python_analysis_typeCheckingMode.md](../../docs/settings/python_analysis_typeCheckingMode.md).

## CI parity

CI must match editor diagnostics or the migration feels broken. Run the Pyright CLI in CI with JSON output / pre-commit / GitHub Action: [../../docs/howto/ci-type-checking.md](../../docs/howto/ci-type-checking.md). Pin `pyrightVersion` to match — [../../docs/settings/python_analysis_pyrightVersion.md](../../docs/settings/python_analysis_pyrightVersion.md).

## Related skills

- **pylance-diagnostics-triage** — per-rule meaning and suppression.
- **pylance-type-checking-setup** — `typeCheckingMode`, `diagnosticSeverityOverrides`, config precedence.
- **pylance-type-system-patterns** — annotation patterns that clear unknown-type errors.

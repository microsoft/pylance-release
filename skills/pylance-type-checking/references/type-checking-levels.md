# Type-Checking Levels: What Code Each Catches

Pylance/Pyright have four strictness levels: `off` → `basic` → `standard` → `strict`. Each stricter level is a **superset** — it enables everything below it plus more rules. This reference tells you what each level flags so you can **write code that passes it**, and how to tighten or relax a single file with inline comments.

> This is about the Python code you write, not editor configuration. To set the project's level or change a rule's severity, configure `pyrightconfig.json` or `[tool.pyright]` in `pyproject.toml` — see the [settings docs](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md).

## The Four Levels

| Level | What it catches |
| ----- | ----------------- |
| `off` | Only core problems: unresolved imports, undefined variables, invalid type forms. No broad type-checking pass. |
| `basic` | Common mistakes: argument/return/assignment mismatches, `None` misuse, general type incompatibilities, invalid TypeVar/generic use. Low false-positive rate. |
| `standard` | Adds override compatibility, possibly-unbound variables, overlapping overloads, function-member access. |
| `strict` | Full set: unknown types (from untyped sources), missing annotations/stubs, unnecessary casts & checks, unused symbols, untyped decorators/bases. |

### Representative rules each level turns on

Headline rules per level — see the [full defaults table](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults) for every rule and its exact severity.

- **`off`** — `reportMissingImports`, `reportMissingModuleSource`, `reportInvalidTypeForm`, `reportUndefinedVariable` (all warnings).
- **`basic`** — `reportReturnType`, `reportArgumentType`, `reportAssignmentType`, `reportGeneralTypeIssues`, `reportCallIssue`, `reportIndexIssue`, `reportOperatorIssue`, the `reportOptional*` family (`reportOptionalMemberAccess`, `reportOptionalCall`, `reportOptionalSubscript`, `reportOptionalIterable`, `reportOptionalContextManager`, `reportOptionalOperand`), `reportAttributeAccessIssue`, `reportInvalidTypeVarUse`, `reportInvalidTypeArguments`, `reportAssertAlwaysTrue`, `reportInvalidStringEscapeSequence`, `reportUnboundVariable`, `reportRedeclaration`, `reportUnusedCoroutine`, `reportPrivateImportUsage`.
- **`standard`** — adds `reportFunctionMemberAccess`, `reportIncompatibleMethodOverride`, `reportIncompatibleVariableOverride`, `reportOverlappingOverload`, `reportPossiblyUnboundVariable`.
- **`strict`** — adds the `reportUnknown*` family (`reportUnknownVariableType`, `reportUnknownArgumentType`, `reportUnknownMemberType`, `reportUnknownParameterType`, `reportUnknownLambdaType`), `reportMissingParameterType`, `reportMissingTypeArgument`, `reportMissingTypeStubs`, `reportUntyped*` (`reportUntypedBaseClass`, `reportUntypedFunctionDecorator`, `reportUntypedClassDecorator`, `reportUntypedNamedTuple`), `reportDeprecated`, `reportDuplicateImport`, `reportConstantRedefinition`, `reportMatchNotExhaustive`, `reportPrivateUsage`, `reportUnnecessary*` (`reportUnnecessaryCast`, `reportUnnecessaryComparison`, `reportUnnecessaryIsInstance`), `reportUnused*` (`reportUnusedImport`, `reportUnusedVariable`, `reportUnusedFunction`, `reportUnusedClass`), `reportTypeCommentUsage`.
- **Never enabled by any level (opt-in only)** — `reportCallInDefaultInitializer`, `reportImplicitOverride`, `reportImplicitStringConcatenation`, `reportImportCycles`, `reportMissingSuperCall`, `reportPropertyTypeMismatch`, `reportUninitializedInstanceVariable`, `reportUnnecessaryTypeIgnoreComment`, `reportUnusedCallResult`.

## Writing Toward Each Level

### `off` — minimal
Just write valid Python that imports resolve and doesn't reference undefined names. No annotations required, but adding them costs nothing and helps the next levels.

### `basic` — the practical baseline
- Annotate function parameters and return types (avoids the downstream `reportArgumentType`/`reportReturnType` chain).
- Narrow `X | None` before using it (`reportOptional*` family). See [type-narrowing.md](type-narrowing.md).
- Initialize all instance attributes in `__init__` (`reportAttributeAccessIssue`).
- Don't misuse `TypeVar` or supply wrong generic arguments.

### `standard` — stronger defaults
- Make subclass overrides signature-compatible with the parent (`reportIncompatibleMethodOverride`/`reportIncompatibleVariableOverride`). Add `@override`.
- Avoid overlapping overload signatures (`reportOverlappingOverload`).
- Make sure names are bound on all code paths (`reportPossiblyUnboundVariable`).

### `strict` — heavily typed
- **Annotate every parameter and return** (`reportMissingParameterType`, `reportUnknownParameterType`).
- **Supply all generic arguments** — `list[int]`, `dict[str, int]`, never bare `list`/`dict` (`reportMissingTypeArgument`).
- **Avoid `Any` and `Unknown`** — they trigger `reportUnknownVariableType`/`reportUnknownArgumentType`/`reportUnknownMemberType`. Source unknowns usually come from untyped libraries; install `types-*` stubs. See [typed-imports-and-stubs.md](typed-imports-and-stubs.md).
- **Inherit from typed bases** (`reportUntypedBaseClass`) and use typed decorators (`reportUntypedFunctionDecorator`/`reportUntypedClassDecorator`).
- **Remove dead code** — unused imports/vars/functions/classes, redundant `cast()` and `isinstance` (`reportUnused*`, `reportUnnecessary*`).
- **Don't use legacy `# type:` comments** — use real annotations (`reportTypeCommentUsage`).
- **Cover all `match` cases** (`reportMatchNotExhaustive`).

## Tightening or Relaxing a Single File (inline comments)

You can override the project level for one file with a comment at the top of the file — no config change needed:

| Comment | Effect |
| ------- | ------ |
| `# pyright: strict` | Apply strict to this file only (good for fully-typed files) |
| `# pyright: basic` | Use basic for this file (relax a stricter project default) |
| `# pyright: reportMissingImports=false` | Disable one rule for this file |
| `# pyright: reportUnknownVariableType=warning` | Change one rule's severity for this file |

```python
# pyright: strict

from typing import Optional

def process(name: str, count: int) -> Optional[str]:
    if count <= 0:
        return None
    return name * count
```

This is the incremental path to strictness: keep the project at `basic`/`standard` and opt individual files into `# pyright: strict` as they're fully annotated, then eventually raise the project default. New code in a strict-by-default project can be marked `# pyright: basic` temporarily while it's being brought up to standard.

> Per-file comments override both `pyrightconfig.json` and editor settings for that file. To change a rule's severity project-wide, set it in `pyrightconfig.json`/`[tool.pyright]` — see the [settings docs](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_diagnosticSeverityOverrides.md).

## See Also

- [Fixing type errors](fixing-type-errors.md) — what to change in the code when a `report*` rule fires
- [Type narrowing](type-narrowing.md) — the fix for `reportOptional*` and many `reportArgumentType`/`reportReturnType` errors
- [Typed imports & stubs](typed-imports-and-stubs.md) — fixing `reportMissingTypeStubs` and `reportUnknown*` from untyped libraries
- [Diagnostics reference](diagnostics-reference.md) — full lookup table
- Full `typeCheckingMode` doc: https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md

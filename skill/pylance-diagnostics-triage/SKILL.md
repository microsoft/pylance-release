---
name: pylance-diagnostics-triage
description: Look up and fix individual Pylance/Pyright diagnostic rules (the report* family). Use when decoding a specific squiggle, suppressing a rule with "# pyright: ignore[...]" or "# type: ignore", or changing one rule's severity. Triggers on any "report..." rule name (reportArgumentType, reportMissingTypeStubs, reportOptionalMemberAccess, reportUnknownVariableType, reportIncompatibleMethodOverride, etc.) and on "pyright ignore", "type ignore", "what does this Pylance error mean".
---

# Pylance diagnostics triage

Each Pyright/Pylance diagnostic rule has its own page under [../../docs/diagnostics/](../../docs/diagnostics/) with overview, representative issues, examples, and fixes. Use this grouped index to find the right page fast.

## Suppression

- File/line suppression: `# pyright: ignore[<ruleName>]` (or `# type: ignore`).
- Disable a rule project-wide: set it to `"none"` in `diagnosticSeverityOverrides` — [../../docs/settings/python_analysis_diagnosticSeverityOverrides.md](../../docs/settings/python_analysis_diagnosticSeverityOverrides.md).
- Mark unreachable-ignore analysis via `reportUnnecessaryTypeIgnoreComment`.

## Which mode enables a rule

A rule only fires if the active `typeCheckingMode` enables it **and** its severity isn't `none`. See the mode→rule table: [../../docs/settings/python_analysis_typeCheckingMode.md](../../docs/settings/python_analysis_typeCheckingMode.md).

## Rule index (grouped)

### Import / stub
- [reportMissingImports](../../docs/diagnostics/reportMissingImports.md) — import cannot be resolved.
- [reportMissingModuleSource](../../docs/diagnostics/reportMissingModuleSource.md) — module found but source/stub not available.
- [reportMissingTypeStubs](../../docs/diagnostics/reportMissingTypeStubs.md) — no `.pyi`/`py.typed` for a module.
- [reportIncompleteStub](../../docs/diagnostics/reportIncompleteStub.md) — stub present but incomplete.
- [reportPrivateImportUsage](../../docs/diagnostics/reportPrivateImportUsage.md) — importing a name not in a module's public API.
- [reportImportCycles](../../docs/diagnostics/reportImportCycles.md) — circular imports.
- [reportDuplicateImport](../../docs/diagnostics/reportDuplicateImport.md) — same import twice.
- [reportUnusedImport](../../docs/diagnostics/reportUnusedImport.md) — imported but never used.
- [reportWildcardImportFromLibrary](../../docs/diagnostics/reportWildcardImportFromLibrary.md) — `from lib import *`.

### Core type errors
- [reportArgumentType](../../docs/diagnostics/reportArgumentType.md) — argument doesn't match parameter type.
- [reportAssignmentType](../../docs/diagnostics/reportAssignmentType.md) — RHS type not assignable to LHS.
- [reportReturnType](../../docs/diagnostics/reportReturnType.md) — return value type mismatch.
- [reportAttributeAccessIssue](../../docs/diagnostics/reportAttributeAccessIssue.md) — attribute access invalid for the type.
- [reportCallIssue](../../docs/diagnostics/reportCallIssue.md) — calling something that can't be called that way.
- [reportIndexIssue](../../docs/diagnostics/reportIndexIssue.md) — invalid indexing/subscripting.
- [reportOperatorIssue](../../docs/diagnostics/reportOperatorIssue.md) — operator not valid for the operand type(s).
- [reportGeneralTypeIssues](../../docs/diagnostics/reportGeneralTypeIssues.md) — broad type-compatibility errors (older catch-all).

### None-safety (Optional family)
- [reportOptionalMemberAccess](../../docs/diagnostics/reportOptionalMemberAccess.md)
- [reportOptionalCall](../../docs/diagnostics/reportOptionalCall.md)
- [reportOptionalSubscript](../../docs/diagnostics/reportOptionalSubscript.md)
- [reportOptionalIterable](../../docs/diagnostics/reportOptionalIterable.md)
- [reportOptionalOperand](../../docs/diagnostics/reportOptionalOperand.md)
- [reportOptionalContextManager](../../docs/diagnostics/reportOptionalContextManager.md)

> Fix pattern: narrow with `is None` / `isinstance` before use — see `pylance-type-system-patterns`.

### Unknown-type (strict-mode family)
- [reportUnknownVariableType](../../docs/diagnostics/reportUnknownVariableType.md)
- [reportUnknownArgumentType](../../docs/diagnostics/reportUnknownArgumentType.md)
- [reportUnknownParameterType](../../docs/diagnostics/reportUnknownParameterType.md)
- [reportUnknownMemberType](../../docs/diagnostics/reportUnknownMemberType.md)
- [reportUnknownLambdaType](../../docs/diagnostics/reportUnknownLambdaType.md)

> These dominate strict mode — address by adding annotations, not by silencing. See `pylance-strict-migration`.

### Generics / TypeVar / overloads
- [reportInvalidTypeArguments](../../docs/diagnostics/reportInvalidTypeArguments.md)
- [reportMissingTypeArgument](../../docs/diagnostics/reportMissingTypeArgument.md)
- [reportInvalidTypeVarUse](../../docs/diagnostics/reportInvalidTypeVarUse.md)
- [reportInconsistentOverload](../../docs/diagnostics/reportInconsistentOverload.md)
- [reportOverlappingOverload](../../docs/diagnostics/reportOverlappingOverload.md)

> Fix by authoring generics correctly — see `pylance-type-system-patterns`.

### OOP / overrides
- [reportIncompatibleMethodOverride](../../docs/diagnostics/reportIncompatibleMethodOverride.md)
- [reportIncompatibleVariableOverride](../../docs/diagnostics/reportIncompatibleVariableOverride.md)
- [reportImplicitOverride](../../docs/diagnostics/reportImplicitOverride.md)
- [reportAbstractUsage](../../docs/diagnostics/reportAbstractUsage.md)
- [reportMissingSuperCall](../../docs/diagnostics/reportMissingSuperCall.md)
- [reportPropertyTypeMismatch](../../docs/diagnostics/reportPropertyTypeMismatch.md)
- [reportFunctionMemberAccess](../../docs/diagnostics/reportFunctionMemberAccess.md)
- [reportPrivateUsage](../../docs/diagnostics/reportPrivateUsage.md)
- [reportUnsupportedDunderAll](../../docs/diagnostics/reportUnsupportedDunderAll.md)

### TypedDict / type forms
- [reportTypedDictNotRequiredAccess](../../docs/diagnostics/reportTypedDictNotRequiredAccess.md)
- [reportInvalidTypeForm](../../docs/diagnostics/reportInvalidTypeForm.md)
- [reportTypeCommentUsage](../../docs/diagnostics/reportTypeCommentUsage.md)

### Unnecessary / redundant
- [reportUnnecessaryIsInstance](../../docs/diagnostics/reportUnnecessaryIsInstance.md)
- [reportUnnecessaryComparison](../../docs/diagnostics/reportUnnecessaryComparison.md)
- [reportUnnecessaryContains](../../docs/diagnostics/reportUnnecessaryContains.md)
- [reportUnnecessaryCast](../../docs/diagnostics/reportUnnecessaryCast.md)
- [reportUnnecessaryTypeIgnoreComment](../../docs/diagnostics/reportUnnecessaryTypeIgnoreComment.md)

### Untyped code
- [reportUntypedBaseClass](../../docs/diagnostics/reportUntypedBaseClass.md)
- [reportUntypedClassDecorator](../../docs/diagnostics/reportUntypedClassDecorator.md)
- [reportUntypedFunctionDecorator](../../docs/diagnostics/reportUntypedFunctionDecorator.md)
- [reportUntypedNamedTuple](../../docs/diagnostics/reportUntypedNamedTuple.md)
- [reportMissingParameterType](../../docs/diagnostics/reportMissingParameterType.md)

### Variables / binding
- [reportUndefinedVariable](../../docs/diagnostics/reportUndefinedVariable.md)
- [reportUnboundVariable](../../docs/diagnostics/reportUnboundVariable.md)
- [reportPossiblyUnboundVariable](../../docs/diagnostics/reportPossiblyUnboundVariable.md)
- [reportUninitializedInstanceVariable](../../docs/diagnostics/reportUninitializedInstanceVariable.md)
- [reportRedeclaration](../../docs/diagnostics/reportRedeclaration.md)
- [reportConstantRedefinition](../../docs/diagnostics/reportConstantRedefinition.md)
- [reportUnhashable](../../docs/diagnostics/reportUnhashable.md)

### Misc
- [reportAbstractUsage](../../docs/diagnostics/reportAbstractUsage.md) — abstract base usage.
- [reportAssertAlwaysTrue](../../docs/diagnostics/reportAssertAlwaysTrue.md) — assert on a constant truthy.
- [reportAssertTypeFailure](../../docs/diagnostics/reportAssertTypeFailure.md) — `assert_type` mismatch.
- [reportMatchNotExhaustive](../../docs/diagnostics/reportMatchNotExhaustive.md) — non-exhaustive `match`.
- [reportDeprecated](../../docs/diagnostics/reportDeprecated.md) — use of `@deprecated`.
- [reportUnusedVariable](../../docs/diagnostics/reportUnusedVariable.md), [reportUnusedFunction](../../docs/diagnostics/reportUnusedFunction.md), [reportUnusedClass](../../docs/diagnostics/reportUnusedClass.md), [reportUnusedExpression](../../docs/diagnostics/reportUnusedExpression.md), [reportUnusedCallResult](../../docs/diagnostics/reportUnusedCallResult.md), [reportUnusedCoroutine](../../docs/diagnostics/reportUnusedCoroutine.md)
- [reportImplicitStringConcatenation](../../docs/diagnostics/reportImplicitStringConcatenation.md)
- [reportInvalidStringEscapeSequence](../../docs/diagnostics/reportInvalidStringEscapeSequence.md)
- [reportInvalidStubStatement](../../docs/diagnostics/reportInvalidStubStatement.md)
- [reportCallInDefaultInitializer](../../docs/diagnostics/reportCallInDefaultInitializer.md)
- [reportWildcardImportFromLibrary](../../docs/diagnostics/reportWildcardImportFromLibrary.md) — listed under Import/stub too.

## Note on the deprecated rule list

[../../DIAGNOSTIC_SEVERITY_RULES.md](../../DIAGNOSTIC_SEVERITY_RULES.md) is a **deprecated stub**. Do **not** use it as the rule source — the authoritative live set is this `docs/diagnostics/` directory plus the mode table above.

## Related skills

- **pylance-strict-migration** — addressing the `reportUnknown*` family and raising strictness.
- **pylance-type-system-patterns** — typing fixes for generics/overload/override rules.
- **pylance-import-resolution** — fixes for the import/stub rules.
- **pylance-type-checking-setup** — changing a rule's severity or mode.

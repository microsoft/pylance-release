# Diagnostics Reference

A compact lookup of all `report*` diagnostic rules: first-active mode, one-line description, and link to the full per-rule doc. Grouped by category. Rules are supersets across modes (`off` ⊂ `basic` ⊂ `standard` ⊂ `strict`); opt-in rules are enabled only when you set them explicitly.

See [type-checking-levels.md](type-checking-levels.md) for level details and [fixing-type-errors.md](fixing-type-errors.md) for fixes to common rules. For the exact per-level severity table, see [Pyright diagnostic defaults](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults).

> Each rule links to the full Pylance per-rule doc for triggers, examples, and fixes.

## General type compatibility

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportGeneralTypeIssues](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportGeneralTypeIssues.md) | basic | Umbrella: protocol mismatches, `@final` subclassing, covariant TypeVar misuse |
| [reportArgumentType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportArgumentType.md) | basic | Wrong argument type passed to a function |
| [reportReturnType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportReturnType.md) | basic | Return value doesn't match declared return type |
| [reportAssignmentType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportAssignmentType.md) | basic | Assigning wrong type to a variable |
| [reportCallIssue](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportCallIssue.md) | basic | Generic call/argument problems not covered by more specific rules |
| [reportIndexIssue](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportIndexIssue.md) | basic | Subscript/index type issues |
| [reportOperatorIssue](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOperatorIssue.md) | basic | Operator operand type issues |
| [reportAttributeAccessIssue](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportAttributeAccessIssue.md) | basic | Undefined/typo'd attribute, or uninitialized instance attribute |
| [reportRedeclaration](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportRedeclaration.md) | basic | Variable redeclared with an incompatible type |
| [reportUnhashable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnhashable.md) | basic | Using an unhashable value where hashable is required |
| [reportAssertTypeFailure](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportAssertTypeFailure.md) | basic | `assert_type` actual type doesn't match asserted type |
| [reportTypedDictNotRequiredAccess](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportTypedDictNotRequiredAccess.md) | basic | Unsafe access to a `NotRequired` TypedDict key |

## Optional / `None` handling (the `reportOptional*` family)

All fire when a possibly-`None` value is used where non-`None` is required. Fix by narrowing — see [type-narrowing.md](type-narrowing.md).

| Rule | First active | Fires when you |
| ---- | ------------ | -------------- |
| [reportOptionalMemberAccess](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalMemberAccess.md) | basic | access an attribute (`x.foo`) |
| [reportOptionalCall](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalCall.md) | basic | call it (`x()`) |
| [reportOptionalSubscript](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalSubscript.md) | basic | subscript it (`x[0]`) |
| [reportOptionalIterable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalIterable.md) | basic | iterate it (`for i in x`) |
| [reportOptionalContextManager](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalContextManager.md) | basic | use as `with x:` |
| [reportOptionalOperand](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOptionalOperand.md) | basic | use as an operand (`x + 1`) |

## Unknown / untyped symbols (strict)

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportUnknownVariableType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownVariableType.md) | strict | Variable has `Unknown` type (often untyped library) |
| [reportUnknownArgumentType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownArgumentType.md) | strict | Argument passed has unknown type |
| [reportUnknownMemberType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownMemberType.md) | strict | Attribute access returns unknown type |
| [reportUnknownParameterType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownParameterType.md) | strict | Function parameter has unknown type |
| [reportUnknownLambdaType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnknownLambdaType.md) | strict | Lambda parameter/return has unknown type |

## Missing annotations / stubs / imports

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportMissingImports](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingImports.md) | off (warning) | Import can't be resolved |
| [reportMissingModuleSource](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingModuleSource.md) | off (warning) | Module resolves but source not found |
| [reportInvalidTypeForm](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInvalidTypeForm.md) | off (warning) | Invalid type expression in annotation |
| [reportUndefinedVariable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUndefinedVariable.md) | off (warning) | Reference to an undefined name |
| [reportUnboundVariable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnboundVariable.md) | basic | Name used before assignment in its scope |
| [reportPossiblyUnboundVariable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportPossiblyUnboundVariable.md) | standard | Name possibly unbound on some path |
| [reportMissingParameterType](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingParameterType.md) | strict | Function parameter missing annotation |
| [reportMissingTypeArgument](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingTypeArgument.md) | strict | Generic used without type arguments |
| [reportMissingTypeStubs](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingTypeStubs.md) | strict | Imported library has no stubs / `py.typed` |
| [reportInvalidTypeArguments](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInvalidTypeArguments.md) | basic | Wrong/missing generic arguments |
| [reportInvalidTypeVarUse](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInvalidTypeVarUse.md) | basic | Inconsistent `TypeVar` use |
| [reportIncompleteStub](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportIncompleteStub.md) | strict | Stub file is incomplete |
| [reportInvalidStubStatement](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInvalidStubStatement.md) | strict | Invalid statement in a stub file |

## Inheritance / overrides

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportIncompatibleMethodOverride](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportIncompatibleMethodOverride.md) | standard | Subclass method signature incompatible with parent |
| [reportIncompatibleVariableOverride](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportIncompatibleVariableOverride.md) | standard | Subclass variable override incompatible with parent |
| [reportOverlappingOverload](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportOverlappingOverload.md) | standard | Overload signatures overlap |
| [reportInconsistentOverload](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInconsistentOverload.md) | basic | Overload signature inconsistent with implementation |
| [reportFunctionMemberAccess](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportFunctionMemberAccess.md) | standard | Accessing member on a function object |
| [reportUntypedBaseClass](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUntypedBaseClass.md) | strict | Base class has no type info |
| [reportAbstractUsage](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportAbstractUsage.md) | basic | Instantiating an abstract class |

## Decorators / classes / typing discipline

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportUntypedFunctionDecorator](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUntypedFunctionDecorator.md) | strict | Function decorator has no type info |
| [reportUntypedClassDecorator](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUntypedClassDecorator.md) | strict | Class decorator has no type info |
| [reportUntypedNamedTuple](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUntypedNamedTuple.md) | strict | `NamedTuple` subclass without annotations |
| [reportTypeCommentUsage](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportTypeCommentUsage.md) | strict | Legacy `# type:` comment used instead of annotations |
| [reportPrivateUsage](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportPrivateUsage.md) | strict | Using a private (`_`-prefixed) symbol from outside |
| [reportMatchNotExhaustive](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMatchNotExhaustive.md) | strict | `match` statement doesn't handle all cases |
| [reportConstantRedefinition](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportConstantRedefinition.md) | strict | `Final`/constant variable reassigned |
| [reportDeprecated](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportDeprecated.md) | strict | Using a `@deprecated` symbol |

## Unused / dead code (mostly strict)

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportUnusedImport](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedImport.md) | strict | Imported but never used |
| [reportUnusedVariable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedVariable.md) | strict | Declared but never used |
| [reportUnusedFunction](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedFunction.md) | strict | Function defined but never used |
| [reportUnusedClass](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedClass.md) | strict | Class defined but never used |
| [reportUnusedExpression](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedExpression.md) | basic | Expression statement with no effect |
| [reportUnusedCoroutine](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedCoroutine.md) | basic | Coroutine not awaited |
| [reportUnnecessaryCast](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryCast.md) | strict | Redundant `cast()` — type already correct |
| [reportUnnecessaryComparison](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryComparison.md) | strict | Redundant comparison — type already narrowed |
| [reportUnnecessaryContains](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryContains.md) | strict | Redundant `in` check |
| [reportUnnecessaryIsInstance](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryIsInstance.md) | strict | Redundant `isinstance` — type already narrowed |
| [reportDuplicateImport](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportDuplicateImport.md) | strict | Same name imported more than once |

## Imports / modules

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportPrivateImportUsage](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportPrivateImportUsage.md) | basic | Using a symbol not in a package's `__all__` / private re-export |
| [reportWildcardImportFromLibrary](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportWildcardImportFromLibrary.md) | basic | `from lib import *` |
| [reportUnsupportedDunderAll](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnsupportedDunderAll.md) | basic | `__all__` with unsupported types |

## Strings

| Rule | First active | What it catches |
| ---- | ------------ | ---------------- |
| [reportInvalidStringEscapeSequence](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportInvalidStringEscapeSequence.md) | basic | Invalid escape sequence in a string |
| [reportImplicitStringConcatenation](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportImplicitStringConcatenation.md) | opt-in | Adjacent string literals implicitly concatenated |
| [reportAssertAlwaysTrue](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportAssertAlwaysTrue.md) | basic | `assert` with a constant-truthy tuple |

## Opt-in only (never enabled by any mode)

Enable these explicitly via `diagnosticSeverityOverrides` or `pyrightconfig.json` if you want them.

| Rule | What it catches |
| ---- | --------------- |
| [reportCallInDefaultInitializer](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportCallInDefaultInitializer.md) | Function call in a default argument (evaluated at def time) |
| [reportImplicitOverride](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportImplicitOverride.md) | Override without `@override` |
| [reportImportCycles](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportImportCycles.md) | Circular imports |
| [reportMissingSuperCall](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportMissingSuperCall.md) | Override missing `super().__init__()` (or parent method) |
| [reportPropertyTypeMismatch](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportPropertyTypeMismatch.md) | Property getter/setter/deleter type mismatch |
| [reportUninitializedInstanceVariable](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUninitializedInstanceVariable.md) | Instance variable not assigned in `__init__` |
| [reportUnnecessaryTypeIgnoreComment](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnnecessaryTypeIgnoreComment.md) | `# type: ignore` / `# pyright: ignore` that suppresses nothing |
| [reportUnusedCallResult](https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/reportUnusedCallResult.md) | Ignoring the result of a call |

## See Also

- [type-checking-levels.md](type-checking-levels.md) — which levels enable which rules, and per-file overrides
- [fixing-type-errors.md](fixing-type-errors.md) — concrete fixes for the most common rules
- Pylance diagnostics directory: https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/
- Pyright diagnostic defaults table: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults

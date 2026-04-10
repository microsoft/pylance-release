# Pylance Documentation Index

This is the complete index of Pylance documentation. Use it to find guides, settings references, and diagnostic rule explanations.

---

## How-To Guides

Step-by-step guides for common Pylance workflows and troubleshooting.

| Guide                                                         | Description                                                                        |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [Auto-Import Guide](howto/auto-import-guide.md)               | Control auto-import suggestions: settings, indexing, and common issues             |
| [CI Type Checking](howto/ci-type-checking.md)                 | Run Pyright in CI to enforce type checking                                         |
| [Editable Installs](howto/editable-installs.md)               | Make `pip install -e` work with Pylance                                            |
| [Generated Code](howto/generated-code.md)                     | Handle generated or dynamic code that Pylance cannot analyze statically            |
| [Gradual Strict Adoption](howto/gradual-strict-adoption.md)   | Move from `off` to `strict` type checking incrementally                            |
| [Monorepo Setup](howto/monorepo-setup.md)                     | Configure Pylance for monorepos, multi-root workspaces, and execution environments |
| [Notebook Troubleshooting](howto/notebook-troubleshooting.md) | Fix common Pylance issues in Jupyter notebooks                                     |
| [Performance Tuning](howto/performance-tuning.md)             | Reduce memory use and improve responsiveness                                       |
| [Reading Pylance Logs](howto/reading-pylance-logs.md)         | Use trace logging to diagnose import resolution and settings                       |
| [Remote Development](howto/remote-development.md)             | Use Pylance with SSH, WSL, containers, and Codespaces                              |
| [Settings Troubleshooting](howto/settings-troubleshooting.md) | Diagnose settings precedence, config file overrides, and common conflicts          |
| [Type Narrowing](howto/type-narrowing.md)                     | Use `isinstance`, `is None`, and type guards to fix type errors                    |
| [Unresolved Imports](howto/unresolved-imports.md)             | Fix `reportMissingImports` and related import errors                               |

---

## Settings Reference

Each page explains one `python.analysis.*` setting: what it does, accepted values, and when to use it.

### Core Settings

| Setting                                                                                | Description                                                      |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [typeCheckingMode](settings/python_analysis_typeCheckingMode.md)                       | Baseline strictness level (`off`, `basic`, `standard`, `strict`) |
| [diagnosticMode](settings/python_analysis_diagnosticMode.md)                           | Check open files only or the whole workspace                     |
| [diagnosticSeverityOverrides](settings/python_analysis_diagnosticSeverityOverrides.md) | Override severity of individual diagnostic rules                 |
| [languageServerMode](settings/python_analysis_languageServerMode.md)                   | Trade features for performance (`light`, `default`, `full`)      |

### Import and Path Settings

| Setting                                                                    | Description                                              |
| -------------------------------------------------------------------------- | -------------------------------------------------------- |
| [autoImportCompletions](settings/python_analysis_autoImportCompletions.md) | Enable or disable auto-import suggestions in completions |
| [autoSearchPaths](settings/python_analysis_autoSearchPaths.md)             | Auto-detect `src/` directories                           |
| [extraPaths](settings/python_analysis_extraPaths.md)                       | Additional directories for import resolution             |
| [importFormat](settings/python_analysis_importFormat.md)                   | Prefer absolute or relative imports in auto-imports      |
| [stubPath](settings/python_analysis_stubPath.md)                           | Directory for custom `.pyi` stub files                   |
| [typeshedPaths](settings/python_analysis_typeshedPaths.md)                 | Custom typeshed location                                 |

### File Scope Settings

| Setting                                        | Description                                   |
| ---------------------------------------------- | --------------------------------------------- |
| [include](settings/python_analysis_include.md) | Files and directories to analyze              |
| [exclude](settings/python_analysis_exclude.md) | Files and directories to skip                 |
| [ignore](settings/python_analysis_ignore.md)   | Files to analyze but suppress diagnostics for |

### Indexing and Completions

| Setting                                                                                                      | Description                                                       |
| ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| [indexing](settings/python_analysis_indexing.md)                                                             | Enable background indexing for auto-imports and workspace symbols |
| [packageIndexDepths](settings/python_analysis_packageIndexDepths.md)                                         | Control indexing depth for specific packages                      |
| [showOnlyDirectDependenciesInAutoImport](settings/python_analysis_showOnlyDirectDependenciesInAutoImport.md) | Limit auto-import completions to direct dependencies              |
| [persistAllIndices](settings/python_analysis_persistAllIndices.md)                                           | Cache all indices to disk                                         |
| [regenerateStdLibIndices](settings/python_analysis_regenerateStdLibIndices.md)                               | Force re-index of standard library                                |
| [userFileIndexingLimit](settings/python_analysis_userFileIndexingLimit.md)                                   | Maximum number of user files to index                             |
| [includeAliasesFromUserFiles](settings/python_analysis_includeAliasesFromUserFiles.md)                       | Include re-exported aliases in completions                        |
| [includeExtraPathSymbolsInSymbolSearch](settings/python_analysis_includeExtraPathSymbolsInSymbolSearch.md)   | Include extraPaths symbols in workspace search                    |
| [includeVenvInWorkspaceSymbols](settings/python_analysis_includeVenvInWorkspaceSymbols.md)                   | Include virtual environment symbols in workspace search           |

### Code Actions and Hints

| Setting                                                                                      | Description                             |
| -------------------------------------------------------------------------------------------- | --------------------------------------- |
| [fixAll](settings/python_analysis_fixAll.md)                                                 | Code actions applied on save or fix-all |
| [inlayHints.callArgumentNames](settings/python_analysis_inlayHints_callArgumentNames.md)     | Show parameter names at call sites      |
| [inlayHints.functionReturnTypes](settings/python_analysis_inlayHints_functionReturnTypes.md) | Show inferred return types              |
| [inlayHints.pytestParameters](settings/python_analysis_inlayHints_pytestParameters.md)       | Show pytest fixture parameter types     |
| [inlayHints.variableTypes](settings/python_analysis_inlayHints_variableTypes.md)             | Show inferred variable types            |
| [enablePytestSupport](settings/python_analysis_enablePytestSupport.md)                       | Enable pytest-aware analysis            |

### Type Evaluation Settings

| Setting                                                                                                              | Description                                                |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [typeEvaluation.analyzeUnannotatedFunctions](settings/python_analysis_typeEvaluation_analyzeUnannotatedFunctions.md) | Analyze functions without type annotations                 |
| [typeEvaluation.deprecateTypingAliases](settings/python_analysis_typeEvaluation_deprecateTypingAliases.md)           | Flag deprecated `typing` aliases (e.g., `typing.List`)     |
| [typeEvaluation.disableBytesTypePromotions](settings/python_analysis_typeEvaluation_disableBytesTypePromotions.md)   | Disable implicit `bytes` promotions                        |
| [typeEvaluation.enableExperimentalFeatures](settings/python_analysis_typeEvaluation_enableExperimentalFeatures.md)   | Enable experimental type-checking features                 |
| [typeEvaluation.enableReachabilityAnalysis](settings/python_analysis_typeEvaluation_enableReachabilityAnalysis.md)   | Detect unreachable code                                    |
| [typeEvaluation.enableTypeIgnoreComments](settings/python_analysis_typeEvaluation_enableTypeIgnoreComments.md)       | Control `# type: ignore` comments                          |
| [typeEvaluation.strictDictionaryInference](settings/python_analysis_typeEvaluation_strictDictionaryInference.md)     | Infer literal dict key/value types                         |
| [typeEvaluation.strictListInference](settings/python_analysis_typeEvaluation_strictListInference.md)                 | Infer literal list element types                           |
| [typeEvaluation.strictParameterNoneValue](settings/python_analysis_typeEvaluation_strictParameterNoneValue.md)       | Require explicit `None` type for `None` default parameters |
| [typeEvaluation.strictSetInference](settings/python_analysis_typeEvaluation_strictSetInference.md)                   | Infer literal set element types                            |

### Advanced Settings

| Setting                                                                        | Description                                            |
| ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| [useLibraryCodeForTypes](settings/python_analysis_useLibraryCodeForTypes.md)   | Infer types from library source when stubs are missing |
| [useNearestConfiguration](settings/python_analysis_useNearestConfiguration.md) | Use nearest `pyrightconfig.json` for each file         |
| [nodeArguments](settings/python_analysis_nodeArguments.md)                     | Extra Node.js arguments for the language server        |
| [nodeExecutable](settings/python_analysis_nodeExecutable.md)                   | Custom Node.js executable path                         |

---

## Diagnostic Rules

Each page explains one Pyright diagnostic rule: what triggers it, code examples, and how to fix or suppress it.

All rules can be configured via [`diagnosticSeverityOverrides`](settings/python_analysis_diagnosticSeverityOverrides.md) or in [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration).

| Rule                                                                                      | Description                                                       |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [reportAbstractUsage](diagnostics/reportAbstractUsage.md)                                 | Instantiating abstract classes or using abstract methods directly |
| [reportArgumentType](diagnostics/reportArgumentType.md)                                   | Argument type incompatible with parameter type                    |
| [reportAssertAlwaysTrue](diagnostics/reportAssertAlwaysTrue.md)                           | Assert statement condition is always true                         |
| [reportAssertTypeFailure](diagnostics/reportAssertTypeFailure.md)                         | `assert_type()` type mismatch                                     |
| [reportAssignmentType](diagnostics/reportAssignmentType.md)                               | Assignment type incompatible with target                          |
| [reportAttributeAccessIssue](diagnostics/reportAttributeAccessIssue.md)                   | Accessing undefined attributes                                    |
| [reportCallInDefaultInitializer](diagnostics/reportCallInDefaultInitializer.md)           | Function calls in default parameter values                        |
| [reportCallIssue](diagnostics/reportCallIssue.md)                                         | Problems with function or method calls                            |
| [reportConstantRedefinition](diagnostics/reportConstantRedefinition.md)                   | Redefining a `Final` constant                                     |
| [reportDeprecated](diagnostics/reportDeprecated.md)                                       | Using deprecated functions, classes, or parameters                |
| [reportDuplicateImport](diagnostics/reportDuplicateImport.md)                             | Same module imported more than once                               |
| [reportFunctionMemberAccess](diagnostics/reportFunctionMemberAccess.md)                   | Accessing non-standard attributes on functions                    |
| [reportGeneralTypeIssues](diagnostics/reportGeneralTypeIssues.md)                         | General type incompatibility issues                               |
| [reportImplicitOverride](diagnostics/reportImplicitOverride.md)                           | Method overrides without `@override` decorator                    |
| [reportImplicitStringConcatenation](diagnostics/reportImplicitStringConcatenation.md)     | Implicit string literal concatenation                             |
| [reportImportCycles](diagnostics/reportImportCycles.md)                                   | Circular import chains                                            |
| [reportIncompatibleMethodOverride](diagnostics/reportIncompatibleMethodOverride.md)       | Method override incompatible with base class                      |
| [reportIncompatibleVariableOverride](diagnostics/reportIncompatibleVariableOverride.md)   | Variable override incompatible with base class                    |
| [reportIncompleteStub](diagnostics/reportIncompleteStub.md)                               | Stub file has `__getattr__` fallback                              |
| [reportInconsistentOverload](diagnostics/reportInconsistentOverload.md)                   | Overloaded function inconsistencies                               |
| [reportIndexIssue](diagnostics/reportIndexIssue.md)                                       | Invalid subscript or index operations                             |
| [reportInvalidStringEscapeSequence](diagnostics/reportInvalidStringEscapeSequence.md)     | Unrecognized escape sequence in string                            |
| [reportInvalidStubStatement](diagnostics/reportInvalidStubStatement.md)                   | Invalid statements in `.pyi` stub files                           |
| [reportInvalidTypeArguments](diagnostics/reportInvalidTypeArguments.md)                   | Invalid generic type arguments                                    |
| [reportInvalidTypeForm](diagnostics/reportInvalidTypeForm.md)                             | Invalid type expression syntax                                    |
| [reportInvalidTypeVarUse](diagnostics/reportInvalidTypeVarUse.md)                         | Incorrect TypeVar usage                                           |
| [reportMatchNotExhaustive](diagnostics/reportMatchNotExhaustive.md)                       | `match` statement missing cases                                   |
| [reportMissingImports](diagnostics/reportMissingImports.md)                               | Import could not be resolved                                      |
| [reportMissingModuleSource](diagnostics/reportMissingModuleSource.md)                     | Module found as stub only, no source                              |
| [reportMissingParameterType](diagnostics/reportMissingParameterType.md)                   | Function parameter missing type annotation                        |
| [reportMissingSuperCall](diagnostics/reportMissingSuperCall.md)                           | `__init__` missing `super().__init__()` call                      |
| [reportMissingTypeArgument](diagnostics/reportMissingTypeArgument.md)                     | Generic type used without type arguments                          |
| [reportMissingTypeStubs](diagnostics/reportMissingTypeStubs.md)                           | No type stubs found for a library                                 |
| [reportOperatorIssue](diagnostics/reportOperatorIssue.md)                                 | Invalid operator usage for given types                            |
| [reportOptionalCall](diagnostics/reportOptionalCall.md)                                   | Calling a possibly `None` value                                   |
| [reportOptionalContextManager](diagnostics/reportOptionalContextManager.md)               | Using possibly `None` as context manager                          |
| [reportOptionalIterable](diagnostics/reportOptionalIterable.md)                           | Iterating over possibly `None` value                              |
| [reportOptionalMemberAccess](diagnostics/reportOptionalMemberAccess.md)                   | Accessing attribute on possibly `None` value                      |
| [reportOptionalOperand](diagnostics/reportOptionalOperand.md)                             | Using possibly `None` in an operation                             |
| [reportOptionalSubscript](diagnostics/reportOptionalSubscript.md)                         | Indexing a possibly `None` value                                  |
| [reportOverlappingOverload](diagnostics/reportOverlappingOverload.md)                     | Overloads with ambiguous overlap                                  |
| [reportPossiblyUnboundVariable](diagnostics/reportPossiblyUnboundVariable.md)             | Variable may not be bound in all code paths                       |
| [reportPrivateImportUsage](diagnostics/reportPrivateImportUsage.md)                       | Importing a private symbol from a typed library                   |
| [reportPrivateUsage](diagnostics/reportPrivateUsage.md)                                   | Accessing private members (underscore-prefixed)                   |
| [reportPropertyTypeMismatch](diagnostics/reportPropertyTypeMismatch.md)                   | Property getter/setter type mismatch                              |
| [reportRedeclaration](diagnostics/reportRedeclaration.md)                                 | Variable declared with incompatible types                         |
| [reportReturnType](diagnostics/reportReturnType.md)                                       | Return value incompatible with declared return type               |
| [reportTypeCommentUsage](diagnostics/reportTypeCommentUsage.md)                           | Using `# type:` comments instead of annotations                   |
| [reportTypedDictNotRequiredAccess](diagnostics/reportTypedDictNotRequiredAccess.md)       | Accessing optional TypedDict keys without check                   |
| [reportUnboundVariable](diagnostics/reportUnboundVariable.md)                             | Using an unbound variable                                         |
| [reportUndefinedVariable](diagnostics/reportUndefinedVariable.md)                         | Using an undefined variable                                       |
| [reportUnhashable](diagnostics/reportUnhashable.md)                                       | Using unhashable type as dict key or set member                   |
| [reportUninitializedInstanceVariable](diagnostics/reportUninitializedInstanceVariable.md) | Instance variable not initialized in `__init__`                   |
| [reportUnknownArgumentType](diagnostics/reportUnknownArgumentType.md)                     | Argument has unknown type (strict mode)                           |
| [reportUnknownLambdaType](diagnostics/reportUnknownLambdaType.md)                         | Lambda has unknown parameter or return type                       |
| [reportUnknownMemberType](diagnostics/reportUnknownMemberType.md)                         | Attribute access returns unknown type                             |
| [reportUnknownParameterType](diagnostics/reportUnknownParameterType.md)                   | Function parameter has unknown type                               |
| [reportUnknownVariableType](diagnostics/reportUnknownVariableType.md)                     | Variable has unknown type (strict mode)                           |
| [reportUnnecessaryCast](diagnostics/reportUnnecessaryCast.md)                             | `cast()` call that has no effect                                  |
| [reportUnnecessaryComparison](diagnostics/reportUnnecessaryComparison.md)                 | Comparison that always has the same result                        |
| [reportUnnecessaryContains](diagnostics/reportUnnecessaryContains.md)                     | `in` check that always has the same result                        |
| [reportUnnecessaryIsInstance](diagnostics/reportUnnecessaryIsInstance.md)                 | `isinstance()` check that is always true or false                 |
| [reportUnnecessaryTypeIgnoreComment](diagnostics/reportUnnecessaryTypeIgnoreComment.md)   | `# type: ignore` on a line with no error                          |
| [reportUnsupportedDunderAll](diagnostics/reportUnsupportedDunderAll.md)                   | Unsupported operations on `__all__`                               |
| [reportUntypedBaseClass](diagnostics/reportUntypedBaseClass.md)                           | Inheriting from a class with no type information                  |
| [reportUntypedClassDecorator](diagnostics/reportUntypedClassDecorator.md)                 | Class decorator with no type information                          |
| [reportUntypedFunctionDecorator](diagnostics/reportUntypedFunctionDecorator.md)           | Function decorator with no type information                       |
| [reportUntypedNamedTuple](diagnostics/reportUntypedNamedTuple.md)                         | Using untyped `namedtuple()` instead of `NamedTuple`              |
| [reportUnusedCallResult](diagnostics/reportUnusedCallResult.md)                           | Ignoring return value of a function call                          |
| [reportUnusedClass](diagnostics/reportUnusedClass.md)                                     | Class defined but never used                                      |
| [reportUnusedCoroutine](diagnostics/reportUnusedCoroutine.md)                             | Coroutine created but never awaited                               |
| [reportUnusedExpression](diagnostics/reportUnusedExpression.md)                           | Expression result is unused                                       |
| [reportUnusedFunction](diagnostics/reportUnusedFunction.md)                               | Function defined but never called                                 |
| [reportUnusedImport](diagnostics/reportUnusedImport.md)                                   | Import not used in the file                                       |
| [reportUnusedVariable](diagnostics/reportUnusedVariable.md)                               | Variable assigned but never used                                  |
| [reportWildcardImportFromLibrary](diagnostics/reportWildcardImportFromLibrary.md)         | Using `from lib import *` with a library                          |

---

## Type Server Protocol (TSP)

| Document         | Description                        |
| ---------------- | ---------------------------------- |
| [TSP docs](tsp/) | Type Server Protocol documentation |

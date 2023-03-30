# Pyright and Pylance Together

[Pyright](https://github.com/Microsoft/pyright) is an open source version of a Python type checker that forms the basis for Pylance. Both Pyright and Pylance can be used inside of an IDE to provide a [language server](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide#why-language-server) for Python code.

Pyright can also be used on the [command line](https://github.com/microsoft/pyright/blob/main/docs/command-line.md) to produce json or text output. This can be used in a variety of situations, like a pre-commit hook, or a [github action](https://github.com/jakebailey/pyright-action).

However, Pylance and Pyright don't always produce the same results. The reason for this is a difference in configuration. 

## Settings differences

Both Pylance and Pyright have [settings](https://github.com/microsoft/pylance-release#settings-and-customization) to control behavior. For the most part, they use the same values, but the few differences do have an impact on the analysis.

| Setting | Pylance default | Pyright default | Description | Potential Impact |
|----|----|----|----|----|
| python.analysis.autoSearchPaths | true | false|  Adds 'src' to the list of search paths | This may change what files are found when analyzing. So if you're getting missing imports for things in your 'src' tree, this might be why |
| python.analysis.indexing | true | false | All files in the current virtual environment are parsed to a certain depth. This gives Pylance more information for auto import completions and other things. | This can have an impact on completions and hover information, but shouldn't impact errors returned.
| python.analysis.useLibraryCodeForTypes | true | false | When true, this means 3rd party libraries are analyzed to produce type information. Without it, all 3 party libraries are just assumed to be of type Any unless they provided type information explicitly | This setting changes the types found by Pylance/Pyright. It can definitely cause differences in errors reported, so make this the same for both if you want consistent results |
| python.analysis.typeCheckingMode | off | basic | Determines what diagnostics are shown. | Pylance defaults to off, but there is a possibility that VS code will force this to 'basic' for pylance users. If you want to guarantee this is the same as Pyright, force it to 'basic' (or whatever you want to enforce) by specifying it in your settings.json|
| python.analysis.diagnosticMode | openFilesOnly | openFilesOnly | Determines which files are analyzed. `openFilesOnly` means only those files that are open in an IDE | You'll likely set this to 'workspace' for the CI version of Pyright. This means Pylance would likely not give you all of the same errors since it's only looking at open files. |
| python.analysis.diagnosticSeverityOverrides | - | - | Allows a user to override the severity levels for individual diagnostic rules. | See below |

## Diagnostic severity overrides

Both Pylance and Pyright specify a custom [`python.analysis.diagnosticSeverityOverrides`](https://microsoft.github.io/pyright/#/configuration?id=diagnostic-rule-defaults) setting. Differences in this setting have a direct impact on the diagnostics returned. If you were attempting to get the same error output for both, making sure this setting is consistent is probably the first thing to do.


### Diagnostic Severity Overrides to match Pyright defaults

| Diagnostic Rule                           | Off        | Basic      | Strict     |
| :---------------------------------------- | :--------- | :--------- | :--------- |
| strictListInference                       | false      | false      | true       |
| strictDictionaryInference                 | false      | false      | true       |
| strictSetInference                        | false      | false      | true       |
| analyzeUnannotatedFunctions               | true       | true       | true       |
| strictParameterNoneValue                  | true       | true       | true       |
| enableTypeIgnoreComments                  | true       | true       | true       |
| reportMissingModuleSource                 | "warning"  | "warning"  | "warning"  |
| reportMissingImports                      | "warning"  | "error"    | "error"    |
| reportUndefinedVariable                   | "warning"  | "error"    | "error"    |
| reportAssertAlwaysTrue                    | "none"     | "warning"  | "error"    |
| reportInvalidStringEscapeSequence         | "none"     | "warning"  | "error"    |
| reportInvalidTypeVarUse                   | "none"     | "warning"  | "error"    |
| reportMissingTypeStubs                    | "none"     | "warning"  | "error"    |
| reportSelfClsParameterName                | "none"     | "warning"  | "error"    |
| reportUnsupportedDunderAll                | "none"     | "warning"  | "error"    |
| reportUnusedExpression                    | "none"     | "warning"  | "error"    |
| reportWildcardImportFromLibrary           | "none"     | "warning"  | "error"    |
| reportGeneralTypeIssues                   | "none"     | "error"    | "error"    |
| reportOptionalSubscript                   | "none"     | "error"    | "error"    |
| reportOptionalMemberAccess                | "none"     | "error"    | "error"    |
| reportOptionalCall                        | "none"     | "error"    | "error"    |
| reportOptionalIterable                    | "none"     | "error"    | "error"    |
| reportOptionalContextManager              | "none"     | "error"    | "error"    |
| reportOptionalOperand                     | "none"     | "error"    | "error"    |
| reportTypedDictNotRequiredAccess          | "none"     | "error"    | "error"    |
| reportPrivateImportUsage                  | "none"     | "error"    | "error"    |
| reportUnboundVariable                     | "none"     | "error"    | "error"    |
| reportUnusedCoroutine                     | "none"     | "error"    | "error"    |
| reportConstantRedefinition                | "none"     | "none"     | "error"    |
| reportDeprecated                          | "none"     | "none"     | "error"    |
| reportDuplicateImport                     | "none"     | "none"     | "error"    |
| reportFunctionMemberAccess                | "none"     | "none"     | "error"    |
| reportImportCycles                        | "none"     | "none"     | "error"    |
| reportIncompatibleMethodOverride          | "none"     | "none"     | "error"    |
| reportIncompatibleVariableOverride        | "none"     | "none"     | "error"    |
| reportIncompleteStub                      | "none"     | "none"     | "error"    |
| reportInconsistentConstructor             | "none"     | "none"     | "error"    |
| reportInvalidStubStatement                | "none"     | "none"     | "error"    |
| reportMatchNotExhaustive                  | "none"     | "none"     | "error"    |
| reportMissingParameterType                | "none"     | "none"     | "error"    |
| reportMissingTypeArgument                 | "none"     | "none"     | "error"    |
| reportOverlappingOverload                 | "none"     | "none"     | "error"    |
| reportPrivateUsage                        | "none"     | "none"     | "error"    |
| reportTypeCommentUsage                    | "none"     | "none"     | "error"    |
| reportUnknownArgumentType                 | "none"     | "none"     | "error"    |
| reportUnknownLambdaType                   | "none"     | "none"     | "error"    |
| reportUnknownMemberType                   | "none"     | "none"     | "error"    |
| reportUnknownParameterType                | "none"     | "none"     | "error"    |
| reportUnknownVariableType                 | "none"     | "none"     | "error"    |
| reportUnnecessaryCast                     | "none"     | "none"     | "error"    |
| reportUnnecessaryComparison               | "none"     | "none"     | "error"    |
| reportUnnecessaryContains                 | "none"     | "none"     | "error"    |
| reportUnnecessaryIsInstance               | "none"     | "none"     | "error"    |
| reportUnusedClass                         | "none"     | "none"     | "error"    |
| reportUnusedImport                        | "none"     | "none"     | "error"    |
| reportUnusedFunction                      | "none"     | "none"     | "error"    |
| reportUnusedVariable                      | "none"     | "none"     | "error"    |
| reportUntypedBaseClass                    | "none"     | "none"     | "error"    |
| reportUntypedClassDecorator               | "none"     | "none"     | "error"    |
| reportUntypedFunctionDecorator            | "none"     | "none"     | "error"    |
| reportUntypedNamedTuple                   | "none"     | "none"     | "error"    |
| reportCallInDefaultInitializer            | "none"     | "none"     | "none"     |
| reportImplicitOverride                    | "none"     | "none"     | "none"     |
| reportImplicitStringConcatenation         | "none"     | "none"     | "none"     |
| reportMissingSuperCall                    | "none"     | "none"     | "none"     |
| reportPropertyTypeMismatch                | "none"     | "none"     | "none"     |
| reportShadowedImports                     | "none"     | "none"     | "none"     |
| reportUninitializedInstanceVariable       | "none"     | "none"     | "none"     |
| reportUnnecessaryTypeIgnoreComment        | "none"     | "none"     | "none"     |
| reportUnusedCallResult                    | "none"     | "none"     | "none"     |

If you wanted a consistent set of settings for diagnostic severity overrides, the Pyright basic settings would like this:

```json
"python.anaylsis.diagnosticSeverityOverrides": {
    "reportAssertAlwaysTrue ": "warning",
    "reportCallInDefaultInitializer ": "none",
    "reportConstantRedefinition ": "none",
    "reportDuplicateImport ": "none",
    "reportImplicitStringConcatenation ": "none",
    "reportImportCycles ": "none",
    "reportIncompatibleMethodOverride ": "none",
    "reportIncompatibleVariableOverride ": "none",
    "reportInvalidStubStatement ": "none",
    "reportMissingImports ": "error",
    "reportMissingTypeStubs ": "none",
    "reportOptionalCall ": "error",
    "reportOptionalContextManager ": "error",
    "reportOptionalIterable ": "error",
    "reportOptionalMemberAccess ": "error",
    "reportOptionalOperand ": "error",
    "reportOptionalSubscript ": "error",
    "reportPrivateUsage ": "none",
    "reportPropertyTypeMismatch ": "none",
    "reportSelfClsParameterName ": "warning",
    "reportShadowedImports ": "none",
    "reportUndefinedVariable ": "error",
    "reportUnboundVariable ": "error",
    "reportUnnecessaryCast ": "none",
    "reportUnnecessaryInstance ": "none",
    "reportUnknownArgumentType ": "none",
    "reportUnknownLambdaType ": "none",
    "reportUnknownMemberType ": "none",
    "reportUnknownParmeterType ": "none",
    "reportUnknownVariableType ": "none",
    "reportUntypedBaseClass ": "none",
    "reportUntypedClassDecorator ": "none",
    "reportUntypedFunctionDecorator ": "none",
    "reportUntypedNamedTuple ": "none",
    "reportUnusedClass ": "none",
    "reportUnusedFunction ": "none",
    "reportUnusedImport ": "none",
    "reportUnusedVariable ": "none",
}
```

You would add these settings to your settings.json when running inside of VS Code.




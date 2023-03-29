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

Differences for typeCheckingMode `basic`:


| Diagnostic Override | Pylance | Pyright |
|----|----|----|
| reportAssertAlwaysTrue | "information" | "warning" |
| reportCallInDefaultInitializer | "information" | "none" |
| reportConstantRedefinition | "warning" | "none" |
| reportDuplicateImport | "warning" | "none" |
| reportImplicitStringConcatenation | "warning" | "none" |
| reportImportCycles | "warning" | "none" |
| reportIncompatibleMethodOverride | "warning" | "none" |
| reportIncompatibleVariableOverride | "warning" | "none" |
| reportInvalidStubStatement | "warning" | "none" |
| reportMissingImports | "warning" | "error" |
| reportMissingTypeStubs | "warning" | "none" |
| reportOptionalCall | "warning" | "error" |
| reportOptionalContextManager | "warning" | "error" |
| reportOptionalIterable | "warning" | "error" |
| reportOptionalMemberAccess | "warning" | "error" |
| reportOptionalOperand | "warning" | "error" |
| reportOptionalSubscript | "warning" | "error" |
| reportPrivateUsage | "warning" | "none" |
| reportPropertyTypeMismatch | "error" | "none" |
| reportSelfClsParameterName | "information" | "warning" |
| reportShadowedImports | "warning" | "none" |
| reportUndefinedVariable | "warning" | "error" |
| reportUnboundVariable | "information" | "error" |
| reportUnnecessaryCast | "information" | "none" |
| reportUnnecessaryInstance | "information" | "none" |
| reportUnknownArgumentType | "warning" | "none" |
| reportUnknownLambdaType | "warning" | "none" |
| reportUnknownMemberType | "warning" | "none" |
| reportUnknownParmeterType | "warning" | "none" |
| reportUnknownVariableType | "warning" | "none" |
| reportUntypedBaseClass | "warning" | "none" |
| reportUntypedClassDecorator | "warning" | "none" |
| reportUntypedFunctionDecorator | "warning" | "none" |
| reportUntypedNamedTuple | "warning" | "none" |
| reportUnusedClass | "information" | "none" |
| reportUnusedFunction | "information" | "none" |
| reportUnusedImport | "information" | "none" |
| reportUnusedVariable | "information" | "none" |

## Diagnostic Severity Overrides to match Pyright defaults

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




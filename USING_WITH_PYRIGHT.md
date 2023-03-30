# Pyright and Pylance Together

[Pyright](https://github.com/Microsoft/pyright) is an open source version of a Python type checker that forms the basis for Pylance. Both Pyright and Pylance can be used inside of an IDE to provide a [language server](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide#why-language-server) for Python code.

Pyright can also be used on the [command line](https://github.com/microsoft/pyright/blob/main/docs/command-line.md) to produce json or text output. This can be used in a variety of situations, like a [pre-commit hook](https://github.com/microsoft/pyright/blob/main/docs/ci-integration.md#running-pyright-as-a-pre-commit-hook), or a [github action](https://github.com/jakebailey/pyright-action).


However, Pylance and Pyright don't always produce the same results. The reason for this is a difference in configuration. 

## Stub differences

Pylance comes bundled with a bunch of stubs, usually found here in the installation:

```
<pylance-extension-install>/dist/bundled
<pylance-extension-install>/dist/native-stubs
```

In order for Pyright to produce the same errors as Pylance it need to use the same stub files. 

This might be done by copying the contents of each of those folders to a new folder. 

You'd then reference that new folder in your [pyrightconfig.json](https://microsoft.github.io/pyright/#/configuration)

```json
{
    "stubPath": "./pylanceStubs"
}
```

Where `pylanceStubs` contains the contents of the `bundled` and `native-stubs` folders.

We have plans to make this easier in the [future](https://github.com/microsoft/pylance-release/discussions/3638).

## Settings differences

Both Pylance and Pyright have [settings](https://github.com/microsoft/pylance-release#settings-and-customization) to control behavior. For the most part, they use the same values, but the few differences, described below, do have an impact on the analysis.


| Setting | Pylance default | Pyright default | Description | Potential Impact |
|----|----|----|----|----|
| python.analysis.autoSearchPaths | true | false|  Adds 'src' to the list of search paths. | This may change what files are found when analyzing. So if you're getting missing imports for modules in your 'src' tree, this might be why. |

| python.analysis.indexing | true | false | All files in the current virtual environment are parsed to a certain depth. This gives Pylance more information for features such as auto import. | This can have an impact on completions and hover information, but shouldn't impact errors returned.

| python.analysis.useLibraryCodeForTypes | true | false | When true, 3rd party libraries are analyzed to produce type information. Without it, all 3rd party library types are assumed to be of type `Any` unless they provided type information explicitly. | This setting changes the types found by Pylance/Pyright and therefore can cause differences in errors reported, so make this the same for both if you want consistent results. A lot of the time this is the sole cause of differences. |

| python.analysis.typeCheckingMode | off | basic | Determines what diagnostics are shown. | Pylance defaults to off, but there is a possibility that VS code will force this to 'basic' for pylance users. If you want to guarantee this is the same as Pyright, force it to 'basic' (or whatever you want to enforce) by specifying it in your settings.json|
| python.analysis.diagnosticMode | openFilesOnly | openFilesOnly | Determines which files are analyzed. `openFilesOnly` means only those files that are open in an IDE | You'll likely set this to 'workspace' for the CI version of Pyright. This means Pylance would likely not give you all of the same errors since it's only looking at open files. |
| python.analysis.diagnosticSeverityOverrides | - | - | Allows a user to override the severity levels for individual diagnostic rules. | See below |

## Diagnostic severity overrides

Both Pylance and Pyright support a [`python.analysis.diagnosticSeverityOverrides`](https://microsoft.github.io/pyright/#/configuration?id=diagnostic-rule-defaults) setting. Differences in this setting have a direct impact on the diagnostics returned. If you were attempting to get the same error output from both Pylance and Pyright, ensure that they are using the same value for this setting.



### Diagnostic Severity Overrides to match Pyright defaults

Here are the settings you would provide to Pylance based on which `typeCheckingMode` you are using in Pyright:


<details>
  <summary>Pyright `typeCheckingMode` = `off`</summary>


```json
{
    "python.anaylsis.diagnosticSeverityOverrides": {
        "strictListInference": false,
        "strictDictionaryInference": false,
        "strictSetInference": false,
        "analyzeUnannotatedFunctions": true,
        "strictParameterNoneValue": true,
        "enableTypeIgnoreComments": true,
        "reportMissingModuleSource": "warning",
        "reportMissingImports": "warning",
        "reportUndefinedVariable": "warning",
        "reportAssertAlwaysTrue": "none",
        "reportInvalidStringEscapeSequence": "none",
        "reportInvalidTypeVarUse": "none",
        "reportMissingTypeStubs": "none",
        "reportSelfClsParameterName": "none",
        "reportUnsupportedDunderAll": "none",
        "reportUnusedExpression": "none",
        "reportWildcardImportFromLibrary": "none",
        "reportGeneralTypeIssues": "none",
        "reportOptionalSubscript": "none",
        "reportOptionalMemberAccess": "none",
        "reportOptionalCall": "none",
        "reportOptionalIterable": "none",
        "reportOptionalContextManager": "none",
        "reportOptionalOperand": "none",
        "reportTypedDictNotRequiredAccess": "none",
        "reportPrivateImportUsage": "none",
        "reportUnboundVariable": "none",
        "reportUnusedCoroutine": "none",
        "reportConstantRedefinition": "none",
        "reportDeprecated": "none",
        "reportDuplicateImport": "none",
        "reportFunctionMemberAccess": "none",
        "reportImportCycles": "none",
        "reportIncompatibleMethodOverride": "none",
        "reportIncompatibleVariableOverride": "none",
        "reportIncompleteStub": "none",
        "reportInconsistentConstructor": "none",
        "reportInvalidStubStatement": "none",
        "reportMatchNotExhaustive": "none",
        "reportMissingParameterType": "none",
        "reportMissingTypeArgument": "none",
        "reportOverlappingOverload": "none",
        "reportPrivateUsage": "none",
        "reportTypeCommentUsage": "none",
        "reportUnknownArgumentType": "none",
        "reportUnknownLambdaType": "none",
        "reportUnknownMemberType": "none",
        "reportUnknownParameterType": "none",
        "reportUnknownVariableType": "none",
        "reportUnnecessaryCast": "none",
        "reportUnnecessaryComparison": "none",
        "reportUnnecessaryContains": "none",
        "reportUnnecessaryIsInstance": "none",
        "reportUnusedClass": "none",
        "reportUnusedImport": "none",
        "reportUnusedFunction": "none",
        "reportUnusedVariable": "none",
        "reportUntypedBaseClass": "none",
        "reportUntypedClassDecorator": "none",
        "reportUntypedFunctionDecorator": "none",
        "reportUntypedNamedTuple": "none",
        "reportCallInDefaultInitializer": "none",
        "reportImplicitOverride": "none",
        "reportImplicitStringConcatenation": "none",
        "reportMissingSuperCall": "none",
        "reportPropertyTypeMismatch": "none",
        "reportShadowedImports": "none",
        "reportUninitializedInstanceVariable": "none",
        "reportUnnecessaryTypeIgnoreComment": "none",
        "reportUnusedCallResult": "none",
    }
}
```

</details>
</br>
<details>
    <summary>Pyright 'basic' mode</summary>

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "strictListInference": false,
        "strictDictionaryInference": false,
        "strictSetInference": false,
        "analyzeUnannotatedFunctions": true,
        "strictParameterNoneValue": true,
        "enableTypeIgnoreComments": true,
        "reportMissingModuleSource": "warning",
        "reportMissingImports": "error",
        "reportUndefinedVariable": "error",
        "reportAssertAlwaysTrue": "warning",
        "reportInvalidStringEscapeSequence": "warning",
        "reportInvalidTypeVarUse": "warning",
        "reportMissingTypeStubs": "warning",
        "reportSelfClsParameterName": "warning",
        "reportUnsupportedDunderAll": "warning",
        "reportUnusedExpression": "warning",
        "reportWildcardImportFromLibrary": "warning",
        "reportGeneralTypeIssues": "error",
        "reportOptionalSubscript": "error",
        "reportOptionalMemberAccess": "error",
        "reportOptionalCall": "error",
        "reportOptionalIterable": "error",
        "reportOptionalContextManager": "error",
        "reportOptionalOperand": "error",
        "reportTypedDictNotRequiredAccess": "error",
        "reportPrivateImportUsage": "error",
        "reportUnboundVariable": "error",
        "reportUnusedCoroutine": "error",
        "reportConstantRedefinition": "none",
        "reportDeprecated": "none",
        "reportDuplicateImport": "none",
        "reportFunctionMemberAccess": "none",
        "reportImportCycles": "none",
        "reportIncompatibleMethodOverride": "none",
        "reportIncompatibleVariableOverride": "none",
        "reportIncompleteStub": "none",
        "reportInconsistentConstructor": "none",
        "reportInvalidStubStatement": "none",
        "reportMatchNotExhaustive": "none",
        "reportMissingParameterType": "none",
        "reportMissingTypeArgument": "none",
        "reportOverlappingOverload": "none",
        "reportPrivateUsage": "none",
        "reportTypeCommentUsage": "none",
        "reportUnknownArgumentType": "none",
        "reportUnknownLambdaType": "none",
        "reportUnknownMemberType": "none",
        "reportUnknownParameterType": "none",
        "reportUnknownVariableType": "none",
        "reportUnnecessaryCast": "none",
        "reportUnnecessaryComparison": "none",
        "reportUnnecessaryContains": "none",
        "reportUnnecessaryIsInstance": "none",
        "reportUnusedClass": "none",
        "reportUnusedImport": "none",
        "reportUnusedFunction": "none",
        "reportUnusedVariable": "none",
        "reportUntypedBaseClass": "none",
        "reportUntypedClassDecorator": "none",
        "reportUntypedFunctionDecorator": "none",
        "reportUntypedNamedTuple": "none",
        "reportCallInDefaultInitializer": "none",
        "reportImplicitOverride": "none",
        "reportImplicitStringConcatenation": "none",
        "reportMissingSuperCall": "none",
        "reportPropertyTypeMismatch": "none",
        "reportShadowedImports": "none",
        "reportUninitializedInstanceVariable": "none",
        "reportUnnecessaryTypeIgnoreComment": "none",
        "reportUnusedCallResult": "none",
}
```

</details>
</br>
<details>
  <summary>Pyright 'strict' mode</summary>

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "strictListInference": true,
        "strictDictionaryInference": true,
        "strictSetInference": true,
        "analyzeUnannotatedFunctions": true,
        "strictParameterNoneValue": true,
        "enableTypeIgnoreComments": true,
        "reportMissingModuleSource": "warning",
        "reportMissingImports": "error",
        "reportUndefinedVariable": "error",
        "reportAssertAlwaysTrue": "error",
        "reportInvalidStringEscapeSequence": "error",
        "reportInvalidTypeVarUse": "error",
        "reportMissingTypeStubs": "error",
        "reportSelfClsParameterName": "error",
        "reportUnsupportedDunderAll": "error",
        "reportUnusedExpression": "error",
        "reportWildcardImportFromLibrary": "error",
        "reportGeneralTypeIssues": "error",
        "reportOptionalSubscript": "error",
        "reportOptionalMemberAccess": "error",
        "reportOptionalCall": "error",
        "reportOptionalIterable": "error",
        "reportOptionalContextManager": "error",
        "reportOptionalOperand": "error",
        "reportTypedDictNotRequiredAccess": "error",
        "reportPrivateImportUsage": "error",
        "reportUnboundVariable": "error",
        "reportUnusedCoroutine": "error",
        "reportConstantRedefinition": "error",
        "reportDeprecated": "error",
        "reportDuplicateImport": "error",
        "reportFunctionMemberAccess": "error",
        "reportImportCycles": "error",
        "reportIncompatibleMethodOverride": "error",
        "reportIncompatibleVariableOverride": "error",
        "reportIncompleteStub": "error",
        "reportInconsistentConstructor": "error",
        "reportInvalidStubStatement": "error",
        "reportMatchNotExhaustive": "error",
        "reportMissingParameterType": "error",
        "reportMissingTypeArgument": "error",
        "reportOverlappingOverload": "error",
        "reportPrivateUsage": "error",
        "reportTypeCommentUsage": "error",
        "reportUnknownArgumentType": "error",
        "reportUnknownLambdaType": "error",
        "reportUnknownMemberType": "error",
        "reportUnknownParameterType": "error",
        "reportUnknownVariableType": "error",
        "reportUnnecessaryCast": "error",
        "reportUnnecessaryComparison": "error",
        "reportUnnecessaryContains": "error",
        "reportUnnecessaryIsInstance": "error",
        "reportUnusedClass": "error",
        "reportUnusedImport": "error",
        "reportUnusedFunction": "error",
        "reportUnusedVariable": "error",
        "reportUntypedBaseClass": "error",
        "reportUntypedClassDecorator": "error",
        "reportUntypedFunctionDecorator": "error",
        "reportUntypedNamedTuple": "error",
        "reportCallInDefaultInitializer": "none",
        "reportImplicitOverride": "none",
        "reportImplicitStringConcatenation": "none",
        "reportMissingSuperCall": "none",
        "reportPropertyTypeMismatch": "none",
        "reportShadowedImports": "none",
        "reportUninitializedInstanceVariable": "none",
        "reportUnnecessaryTypeIgnoreComment": "none",
        "reportUnusedCallResult": "none",
    }
}
```

</details>
</br>

You would add these settings to your settings.json when running inside of VS Code.




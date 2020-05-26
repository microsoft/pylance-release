A new, more performant Microsoft Language Server for Python that leverages PyRight, Microsoft's static type checking tool. 

Feel free to [file issues](https://github.com/microsoft/python-language-server-v2/issues/new/choose) or ask questions on our issue tracker. Code contributions are welcomed via the [PyRight repo](https://github.com/microsoft/pyright). 


# Available Features 

- Docstrings 
- Signature help 
- Autocompletions 
- Go to definition 
- Find references  
- Parameter suggestions during function invocation (with type information) 
- Native multi-root workspace support 
- Support for extra paths to allow users to specify paths for import resolution 
- A new type checking mode (with ‘off’, ‘basic’ and ‘strict’ available) 
- Diagnostic severity overrides (with ‘error’, ‘warning’, ‘information’ or ‘none’ as values for each rule) 
- Jupyter Notebooks support 
- IntelliCode Completions Support 
- Add and remove import code actions 
- Auto-imports 


# Settings


## Type Checking Mode ("python.analysis.typeCheckingMode") 

Used to specify the level of type checking the user wants analysis to perform on their code.

Default: "off"

Available values: 

| Value  | Description                                                                                                               |
|--------|---------------------------------------------------------------------------------------------------------------------------|
| off    | Will show you no type checking-rule produced diagnostics but will still show diagnostics on unresolved imports/variables. |
| basic  | Non-type checking-related rules + basic type checking rules.                                                              |
| strict | All type checking rules at the highest severity (flagged as errors).                                                      |


## Extra Paths ("python.analysis.extraPaths") 

Used to specify extra search paths for import resolution.

Default: empty array 

Accepts an array of strings 

  
## Diagnostic Mode ("python.analysis.diagnosticMode") 

Used to allow a user to specify what files they want the language server to analyze to get problems flagged in their code.

Values: 

- "workspace" 
- "openFilesOnly" (default) 


## Stub Path ("python.analysis.stubPath") 

Used to allow a user to specify a path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory.

Default: "./typings" 


## Auto Search Paths ("python.analysis.autoSearchPaths") 

Used to automatically add search paths based on some predefined names (like "src").

Default: True  

Accepts a Boolean value


## Diagnostic Severity Overrides ("python.analysis.diagnosticSeverityOverrides") 

Used to allow a user to override the severity levels for individual diagnostics should they desire.

Accepted severity values:

- "error" (red squiggle)
- "warning" (yellow squiggle)
- "information" (blue squiggle)
- "none" (this disables the rule)

Available Rules:

- reportGeneralTypeIssues 
- reportTypeshedErrors 
- reportMissingImports 
- reportMissingModuleSource 
- reportMissingTypeStubs 
- reportImportCycles 
- reportUnusedImport 
- reportUnusedClass 
- reportUnusedFunction 
- reportUnusedVariable 
- reportDuplicateImport 
- reportOptionalSubscript 
- reportOptionalMemberAccess 
- reportOptionalCall 
- reportOptionalIterable 
- reportOptionalContextManager 
- reportOptionalOperand 
- reportUntypedFunctionDecorator 
- reportUntypedClassDecorator 
- reportUntypedBaseClass 
- reportUntypedNamedTuple 
- reportPrivateUsage 
- reportConstantRedefinition 
- reportIncompatibleMethodOverride 
- reportInvalidStringEscapeSequence 
- reportUnknownParameterType 
- reportUnknownArgumentType 
- reportUnknownLambdaType 
- reportUnknownVariableType 
- reportUnknownMemberType 
- reportCallInDefaultInitializer 
- reportUnnecessaryIsInstance 
- reportUnnecessaryCast 
- reportAssertAlwaysTrue 
- reportSelfClsParameterName 
- reportImplicitStringConcatenation 
- reportUndefinedVariable 
- reportUnboundVariable 
  

Example: 
```
{ 
    "python.analysis.diagnosticSeverityOverrides:" { 
        "some-diagnostic" : "warning", 
        "some-other-diagnostic" : "error" 
    } 
} 
```


## IntelliCode Enabled ("python.analysis.intelliCodeEnabled") 

Used to allow the user to turn off IntelliCode suggestions as part of the completions list.

Default: True 

Accepts a Boolean value 


## Use Library Code for Types ("python.analysis.useLibraryCodeForTypes") 

Used to parse the source code for a package when a typestub is not found.

Default: True 

Accepts a Boolean value 








TODO: old generated readme below



# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.

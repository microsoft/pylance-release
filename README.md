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

| Value  | Description |
|--------|-------------|
| error | Red squiggle. |
| warning | Yellow squiggle. |
| information | Blue squiggle. |
| none | Disables the rule. |

Available Rules:

| Value  | Description                                                                                                               |
|--------|---------------------------------------------------------------------------------------------------------------------------|
| reportGeneralTypeIssues | Diagnostics for general type inconsistencies, unsupported operations, argument/parameter mismatches, etc. This covers all of the basic type-checking rules not covered by other rules. It does not include syntax errors. |
| reportMissingImports | Diagnostics for imports that have no corresponding imported python file or type stub file. |
| reportMissingModuleSource | Diagnostics for imports that have no corresponding source file. This happens when a type stub is found, but the module source file was not found, indicating that the code may fail at runtime when using this execution environment. Type checking will be done using the type stub. |
| reportMissingTypeStubs | Diagnostics for imports that have no corresponding type stub file (either a typeshed file or a custom type stub). The type checker requires type stubs to do its best job at analysis. |
| reportImportCycles | Diagnostics for cyclical import chains. These are not errors in Python, but they do slow down type analysis and often hint at architectural layering issues. Generally, they should be avoided. |
| reportUnusedImport | Diagnostics for an imported symbol that is not referenced within that file. |
| reportUnusedClass | Diagnostics for a class with a private name (starting with an underscore) that is not accessed. |
| reportUnusedFunction | Diagnostics for a function or method with a private name (starting with an underscore) that is not accessed. |
| reportUnusedVariable | Diagnostics for a variable that is not accessed. |
| reportDuplicateImport | Diagnostics for an imported symbol or module that is imported more than once. |
| reportOptionalSubscript | Diagnostics for an attempt to subscript (index) a variable with an Optional type. |
| reportOptionalMemberAccess | Diagnostics for an attempt to access a member of a variable with an Optional type. |
| reportOptionalCall | Diagnostics for an attempt to call a variable with an Optional type. |
| reportOptionalIterable | Diagnostics for an attempt to use an Optional type as an iterable value (e.g. within a for statement). |
| reportOptionalContextManager | Diagnostics for an attempt to use an Optional type as a context manager (as a parameter to a with statement). |
| reportOptionalOperand | Diagnostics for an attempt to use an Optional type as an operand to a binary or unary operator (like '+', '==', 'or', 'not'). |
| reportUntypedFunctionDecorator | Diagnostics for function decorators that have no type annotations. These obscure the function type, defeating many type analysis features.  |
| reportUntypedClassDecorator | Diagnostics for class decorators that have no type annotations. These obscure the class type, defeating many type analysis features. |
| reportUntypedBaseClass | Diagnostics for base classes whose type cannot be determined statically. These obscure the class type, defeating many type analysis features. |
| reportUntypedNamedTuple | Diagnostics when “namedtuple” is used rather than “NamedTuple”. The former contains no type information, whereas the latter does. |
| reportPrivateUsage | Diagnostics for incorrect usage of private or protected variables or functions. Protected class members begin with a single underscore `_` and can be accessed only by subclasses. Private class members begin with a double underscore but do not end in a double underscore and can be accessed only within the declaring class. Variables and functions declared outside of a class are considered private if their names start with either a single or double underscore, and they cannot be accessed outside of the declaring module. |
| reportConstantRedefinition | Diagnostics for attempts to redefine variables whose names are all-caps with underscores and numerals. |
| reportIncompatibleMethodOverride | Diagnostics for methods that override a method of the same name in a base class in an incompatible manner (different number of parameters, different parameter types, or a different return type).  |
| reportInvalidStringEscapeSequence | Diagnostics for invalid escape sequences used within string literals. The Python specification indicates that such sequences will generate a syntax error in future versions. |
| reportUnknownParameterType | Diagnostics for input or return parameters for functions or methods that have an unknown type. |
| reportUnknownArgumentType | Diagnostics for call arguments for functions or methods that have an unknown type. |
| reportUnknownLambdaType | Diagnostics for input or return parameters for lambdas that have an unknown type. |
| reportUnknownVariableType | Diagnostics for variables that have an unknown type.  |
| reportUnknownMemberType | Diagnostics for class or instance variables that have an unknown type. |
| reportCallInDefaultInitializer | Diagnostics for function calls within a default value initialization expression. Such calls can mask expensive operations that are performed at module initialization time. |
| reportUnnecessaryIsInstance | Diagnostics for 'isinstance' or 'issubclass' calls where the result is statically determined to be always true or always false. Such calls are often indicative of a programming error. |
| reportUnnecessaryCast | Diagnostics for 'cast' calls that are statically determined to be unnecessary. Such calls are sometimes indicative of a programming error. |
| reportAssertAlwaysTrue | Diagnostics for 'assert' statement that will provably always assert. This can be indicative of a programming error.  |
| reportSelfClsParameterName | Diagnostics for a missing or misnamed “self” parameter in instance methods and “cls” parameter in class methods. Instance methods in metaclasses (classes that derive from “type”) are allowed to use “cls” for instance methods. |
| reportImplicitStringConcatenation | Diagnostics for two or more string literals that follow each other, indicating an implicit concatenation. This is considered a bad practice and often masks bugs such as missing commas.  |
| reportUndefinedVariable | Diagnostics for undefined variables. |
| reportUnboundVariable | Diagnostics for unbound and possibly unbound variables. |

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

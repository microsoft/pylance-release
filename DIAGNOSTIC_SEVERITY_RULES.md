Diagnostic Severity Rules
=====================
This doc details all available rules that can be customized using the `python.analysis.diagnosticSeverityOverrides` setting. If you are looking for details on other available settings, please refer back to the main [README](README.md).

| Value  | Description                                                                                                               |
|--------|---------------------------------------------------------------------------------------------------------------------------|
| reportGeneralTypeIssues | Diagnostics for general type inconsistencies, unsupported operations, argument/parameter mismatches, etc. This covers all of the basic type-checking rules not covered by other rules. It does not include syntax errors. |
| reportPropertyTypeMismatch | Diagnostics for properties where the type of the value passed to the setter is not assignable to the value returned by the getter. Such mismatches violate the intended use of properties, which are meant to act like variables. |
| reportFunctionMemberAccess | Diagnostics for member accesses on functions. |
| reportMissingImports | Diagnostics for imports that have no corresponding imported python file or type stub file. |
| reportMissingModuleSource | Diagnostics for imports that have no corresponding source file. This happens when a type stub is found, but the module source file was not found, indicating that the code may fail at runtime when using this execution environment. Type checking will be done using the type stub. |
| reportMissingTypeStubs | Diagnostics for imports that have no corresponding type stub file (either a typeshed file or a custom type stub). The type checker requires type stubs to do its best job at analysis. |
| reportImportCycles | Diagnostics for cyclical import chains. These are not errors in Python, but they do slow down type analysis and often hint at architectural layering issues. Generally, they should be avoided. |
| reportUnusedImport | Diagnostics for an imported symbol that is not referenced within that file. |
| reportUnusedClass | Diagnostics for a class with a private name (starting with an underscore) that is not accessed. |
| reportUnusedFunction | Diagnostics for a function or method with a private name (starting with an underscore) that is not accessed. |
| reportUnusedVariable | Diagnostics for a variable that is not accessed. |
| reportDuplicateImport | Diagnostics for an imported symbol or module that is imported more than once. |
| reportWildcardImportFromLibrary | Diagnostics for an wildcard import from an external library. |
| reportOptionalSubscript | Diagnostics for an attempt to subscript (index) a variable with an Optional type. |
| reportOptionalMemberAccess | Diagnostics for an attempt to access a member of a variable with an Optional type. |
| reportOptionalCall | Diagnostics for an attempt to call a variable with an Optional type. |
| reportOptionalIterable | Diagnostics for an attempt to use an Optional type as an iterable value (e.g. within a for statement). |
| reportOptionalContextManager | Diagnostics for an attempt to use an Optional type as a context manager (as a parameter to a with statement). |
| reportOptionalOperand | Diagnostics for an attempt to use an Optional type as an operand to a binary or unary operator (like '+', '==', 'or', 'not'). |
| reportTypedDictNotRequiredAccess | Diagnostics for an attempt to access a non-required key within a TypedDict without a check for its presence. |
| reportUntypedFunctionDecorator | Diagnostics for function decorators that have no type annotations. These obscure the function type, defeating many type analysis features.  |
| reportUntypedClassDecorator | Diagnostics for class decorators that have no type annotations. These obscure the class type, defeating many type analysis features. |
| reportUntypedBaseClass | Diagnostics for base classes whose type cannot be determined statically. These obscure the class type, defeating many type analysis features. |
| reportUntypedNamedTuple | Diagnostics when “namedtuple” is used rather than “NamedTuple”. The former contains no type information, whereas the latter does. |
| reportPrivateUsage | Diagnostics for incorrect usage of private or protected variables or functions. Protected class members begin with a single underscore `_` and can be accessed only by subclasses. Private class members begin with a double underscore but do not end in a double underscore and can be accessed only within the declaring class. Variables and functions declared outside of a class are considered private if their names start with either a single or double underscore, and they cannot be accessed outside of the declaring module. |
| reportPrivateImportUsage | Diagnostics for incorrect usage of symbol imported from a "py.typed" module that is [not re-exported](https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md#library-interface) from that module. |
| reportConstantRedefinition | Diagnostics for attempts to redefine variables whose names are all-caps with underscores and numerals. |
| reportIncompatibleMethodOverride | Diagnostics for methods that override a method of the same name in a base class in an incompatible manner (wrong number of parameters, incompatible parameter types, or incompatible return type). |
| reportIncompatibleVariableOverride | Diagnostics for class variable declarations that override a symbol of the same name in a base class with a type that is incompatible with the base class symbol type. |
| reportInconsistentConstructor | Diagnostics when an `__init__` method signature is inconsistent with a `__new__` signature. The default value for this setting is 'none'. |
| reportOverlappingOverload | Diagnostics for function overloads that overlap in signature and obscure each other or have incompatible return types. |
| reportInvalidStringEscapeSequence | Diagnostics for invalid escape sequences used within string literals. The Python specification indicates that such sequences will generate a syntax error in future versions. |
| reportUnknownParameterType | Diagnostics for input or return parameters for functions or methods that have an unknown type. |
| reportUnknownArgumentType | Diagnostics for call arguments for functions or methods that have an unknown type. |
| reportUnknownLambdaType | Diagnostics for input or return parameters for lambdas that have an unknown type. |
| reportUnknownVariableType | Diagnostics for variables that have an unknown type.  |
| reportUnknownMemberType | Diagnostics for class or instance variables that have an unknown type. |
| reportMissingParameterType | Diagnostics for parameters that are missing a type annotation. |
| reportMissingTypeArgument | Diagnostics for when a generic class is used without providing explicit or implicit type arguments. |
| reportInvalidTypeVarUse | Diagnostics for improper use of type variables in a function signature. |
| reportCallInDefaultInitializer | Diagnostics for function calls within a default value initialization expression. Such calls can mask expensive operations that are performed at module initialization time. |
| reportUnnecessaryIsInstance | Diagnostics for 'isinstance' or 'issubclass' calls where the result is statically determined to be always true or always false. Such calls are often indicative of a programming error. |
| reportUnnecessaryCast | Diagnostics for 'cast' calls that are statically determined to be unnecessary. Such calls are sometimes indicative of a programming error. |
| reportUnnecessaryComparison | Diagnostics for '==' and '!=' comparisons that are statically determined to be unnecessary. Such calls are sometimes indicative of a programming error. |
| reportAssertAlwaysTrue | Diagnostics for 'assert' statement that will provably always assert. This can be indicative of a programming error.  |
| reportSelfClsParameterName | Diagnostics for a missing or misnamed “self” parameter in instance methods and “cls” parameter in class methods. Instance methods in metaclasses (classes that derive from “type”) are allowed to use “cls” for instance methods. |
| reportImplicitStringConcatenation | Diagnostics for two or more string literals that follow each other, indicating an implicit concatenation. This is considered a bad practice and often masks bugs such as missing commas.  |
| reportUndefinedVariable | Diagnostics for undefined variables. |
| reportUnboundVariable | Diagnostics for unbound and possibly unbound variables. |
| reportInvalidStubStatement | Diagnostics for statements that should not appear within a stub file. |
| reportIncompleteStub | Diagnostics for the use of a module-level `__getattr__` function, indicating that the stub is incomplete. | 
| reportUnusedCallResult | Diagnostics for call expressions whose results are not consumed and are not None. |
| reportUnsupportedDunderAll | Diagnostics for unsupported operations performed on `__all__`. |
| reportUnusedCoroutine | Diagnostics for call expressions that return a Coroutine and whose results are not consumed. |
| reportUnnecessaryTypeIgnoreComment | Diagnostics for a '# type: ignore' comment that would have no effect if removed. |

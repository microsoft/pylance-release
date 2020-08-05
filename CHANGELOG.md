# Changelog

## 2020.8.0 (5 August 2020)

-   Added `python.analysis.autoImportCompletions` setting (`true` by default), which allows auto-import completions to be disabled.
    ([pylance-release#64](https://github.com/microsoft/pylance-release/issues/64))
-   Fixed the "make Pylance your default language server" prompt when language server setting was previously set outside of the user settings.

In addition, Pylance's copy of Pyright has been updated from 1.1.58 to 1.1.60, including the following changes:

-   [1.1.60](https://github.com/microsoft/pyright/releases/tag/1.1.60)
    -   Bug Fix: Fixed a bug "aliased import with leading underscore produces private usage error".
    -   Bug Fix: Fixed a bug that caused the wrong diagnostic message string to be used when "Generic" is used with no type arguments.
    -   Enhancement: Added new diagnostic message for when "Generic" is used in contexts outside of a class definition statement.
    -   Bug Fix (from Pylance): Use `sys.version_info` to query interpreter version.
    -   Enhancement: Added heuristics to type var solver so it picks the "least complex" solution when considering the elements within a union.
    -   Enhancement: Updated typeshed stubs to the latest versions.
    -   Bug Fix: Fixed a bug that caused an error to be reported when a newline token was used within an f-string expression.
        ([pylance-release#200](https://github.com/microsoft/pylance-release/issues/200))
    -   Enhancement: Added new diagnostic rule "reportInvalidStubStatement" (on by default in strict mode, off otherwise) that reports diagnostics for statements that should not appear within a type stub file.
    -   Enhancement: Added diagnostic for a module-level `__getattr__` function defined in a type stub file when in strict mode.
    -   Bug Fix: Fixed bug that caused imports (and other symbols) to be reported as unaccessed if they were accessed from within code that was deemed to be unreachable (e.g. due to the current platform configuration).
    -   Behavior Change: Changed logic for reportUnusedClass and reportUnusedFunction diagnostic rules so they don't report private-named functions and classes within stub files.
    -   Bug Fix: The token "..." should mean an ellipsis object, not the ellipsis class, when used in a normal expression within a non-stub file.
    -   Enhancement (from Pylance): Add python.analysis.autoImportCompletions to control auto-import completions.
-   [1.1.59](https://github.com/microsoft/pyright/releases/tag/1.1.59)
    -   Bug Fix: Changed the inferred type of an async function to use `Coroutine` rather than `Awaitable` type. `Coroutine` is a subclass of `Awaitable` and is arguably more correct in this case.
        ([pylance-release#184](https://github.com/microsoft/pylance-release/issues/184))
    -   Bug Fix: Fixed a bug in the handling of position-only parameters with default values followed by named parameters or \*\*kwargs.
    -   Bug Fix: Fixed a bug where "yield from" argument was assumed to be an "Iterator", but it should really be an "Iterable".
    -   Bug Fix: Fixed bug where "from .A import A" statement caused symbol "A" to have an inferred type that was a union of a module and other type, even though the other type immediately overwrites the module.
        ([pylance-release#188](https://github.com/microsoft/pylance-release/issues/188))
    -   Behavior Change: Changed type stub generator to never generate parameter type annotations based purely on default value types since those can be incorrect or incomplete. Changed type stub generator to automatically add method return types for common magic methods whose return type is always the same.
    -   Behavior Change: Changed type stub generator to avoid emitting functions and methods that begin with an underscore.
    -   Enhancement: Changed type checker to flag unaccessed symbols within type stubs in some cases. It doesn't mark function parameters or variables as unaccessed, and it doesn't mark imports of the form "from x import y as z" or "import a as b" as unaccessed since those are intended to be re-exports.
    -   Enhancement: Changed type checker to treat "..." as an "Unknown" type when used as the RHS of an assignment statement such as "a = ...". This idiom appears sometimes within type stubs, and it should be treated as a missing (unknown) type so stub authors know that they need to fill in a type annotation.
    -   Enhancement: Improved the diagnostic message used to report parameter type mismatches when a parameter name isn't known.
    -   Bug Fix: Fixed a bug whereby a TypeVar in a source type could be conflated with a same-named TypeVar in a dest type when performing TypeVar matching.
    -   Bug Fix: On the Windows platform, avoid calling 'python3' to determine the import paths for the current interpreter. This command can sometimes display a dialog indicating that python isn't installed and can be downloaded from the store.

## 2020.7.4 (29 July 2020)

-   Fixed case where analysis progress spinner would not disappear after analysis was complete.
-   Improved active parameter bolding in signature help for functions with multiple overrides.

In addition, Pylance's copy of Pyright has been updated from 1.1.54 to 1.1.58, including the following changes:

-   [1.1.58](https://github.com/microsoft/pyright/releases/tag/1.1.58)
    -   Enhancement: Rework signature help to use new VS Code / LSP APIs. Function overrides and active parameters are handled much, much better.
    -   Enhancement: Added strict-mode check for declared return types in type stubs, which don't allow for return type inference.
    -   Bug Fix: Fixed bug in type checker that resulted in a crash when a function declaration referred to itself within its return type annotation.
        ([pylance-release#181](https://github.com/microsoft/pylance-release/issues/181))
    -   Bug Fix: Fixed bug that caused duplicate diagnostics to be reported for quoted type annotations in some cases.
    -   Bug Fix: Fixed bug that caused "find all references" and "replace symbol" to sometimes miss references to a symbol if they were within quoted type annotations or type comments.
    -   Bug Fix: Fixed bugs in a few of the "find all references" tests, which were not properly quoting a forward-declared symbol.
    -   Bug Fix: Fixed a bug that caused infinite recursion and a crash when printing the type of a function that refers to itself within its own return type annotation.
        ([pylance-release#181](https://github.com/microsoft/pylance-release/issues/181))
    -   Bug Fix: Fixed bug where an f-string expression generated an error if it ended in an equal sign followed by whitespace. The Python 3.8 spec doesn't indicate whether whitespace is allowed here, but clearly the interpreter accepts it.
        ([pylance-release#182](https://github.com/microsoft/pylance-release/issues/182))
    -   Bug Fix: Fixed bug in logic that handles chained comparisons (e.g. `a < b < c`). The code was not properly handling the case where the left expression was parenthesized (e.g. `(a < b) < c`).
    -   Enhancement: Improved bidirectional type inference in the case where the type and the expected type are generic but the expected type is a base class that has been specialized. For example, if the expected type is `Mapping[str, int]` and the type is a `dict`.
-   [1.1.57](https://github.com/microsoft/pyright/releases/tag/1.1.57)
    -   Bug Fix: Fixed bug that caused partial type stub creation (for subpackages of a top-level package) to be generated in the wrong directory.
    -   Change in Behavior: Changed logic within type evaluator to track differences between None and NoneType. Previously, they were treated interchangeably. This worked in most cases, but there are some edge cases where the difference is important.
    -   Change in Behavior: Changed logic that converts a type to text so it properly distinguishes between "None" and "NoneType". It previously always output "None".
    -   Enhancement: Added support for NoneType matching a type expression `Type[T]` during TypeVar matching.
    -   Bug Fix: Fixed the handling of class or instance variable declarations that redefine a same-named symbol in an outer scope but do not use a variable declaration statement within the class.
        ([pylance-release#175](https://github.com/microsoft/pylance-release/issues/175))
    -   Bug Fix: Updated type checker's logic for dealing with symbols that are declared in an inner scope and an outer scope but used within the inner scope prior to being redefined.
    -   Bug Fix: Fixed bug a homogeneous tuple of indeterminate length was indexed with a constant expression.
    -   Enhancement: Made the reportIncompatibleMethodOverride rule smarter. It now properly handles position-only parameters and allows a subclass to extend the signature of a method it is overriding as long as the parameters are \*varg, \*\*kwarg, or have default values.
        ([pylance-release#157](https://github.com/microsoft/pylance-release/issues/157))
    -   Enhancement: Augmented the reportIncompatibleMethodOverride diagnostic rule to check for cases where a non-function symbol within a subclass redefines a function symbol in a base class.
    -   New Feature: Added new diagnostic rule "reportIncompatibleVariableOverride" which is similar to "reportIncompatibleMethodOverride" except that it reports incompatible overrides of variables (non-methods).
-   [1.1.56](https://github.com/microsoft/pyright/releases/tag/1.1.56)
    -   Bug Fix: Fixed bug that caused the default python platform not to be specified if there was no config file and no python interpreter selected.
    -   Bug Fix: Fixed crash in type checker that occurs when removing NoReturn from a union and having no remaining types.
    -   Bug Fix: Fixed bug that caused `__name__` not to be flagged as an invalid attribute on a class instance.
        ([pylance-release#154](https://github.com/microsoft/pylance-release/issues/154))
    -   Bug Fix: Fixed bug that caused quoted type annotation (i.e. a forward reference) that contains type arguments to report an "unbound symbol".
    -   Enhancement: Improved CompletionItemKind for intrinsic class symbols like `__name__`, etc.
        ([pylance-release#154](https://github.com/microsoft/pylance-release/issues/154))
    -   Bug Fix: Fixed bug in parsing of unicode named character encodings within string literals when the encoding included capital letters.
        ([pylance-release#161](https://github.com/microsoft/pylance-release/issues/161))
    -   Bug Fix: Fixed bug whereby a non-function definition (such as an instance variable) within a subclass was not considered as having overridden an abstract method or property within a base class.
    -   Change in Behavior: Changed Never internal type to be assignable to any type. Previously, it was assignable to no type.
    -   Bug Fix: Fixed bug that caused a spurious error during TypeVar matching when the TypeVar is constrained and is initially matched against an Any or Unknown type but is later matched against a known type.
    -   Bug Fix: Fixed bug in dataclass logic that reported spurious error when initializing attribute with `field(init=False)`.
        ([pylance-release#162](https://github.com/microsoft/pylance-release/issues/162))
    -   Change in Behavior: Renamed ParameterSpecification to ParamSpec to reflect latest PEP 612 changes.
    -   Enhancement: Updated typeshed fallback stubs to latest version.
    -   Change in Behavior: Updated PEP 612 and 614 features to be dependent on 3.10 rather than 3.9.
    -   Bug Fix: Fixed bug that caused diagnostics to persist in files that are not part of the workspace even after they are closed.
    -   Bug Fix: Fixed bug that generated incorrect type checking error when type alias used a `Type[x]` type annotation.
-   [1.1.55](https://github.com/microsoft/pyright/releases/tag/1.1.55)
    -   Bug Fix: Changed logic for reportMissingModuleSource diagnostic rule so it isn't reported for stub files.
    -   Enhancement: Added support for typing.OrderedDict, which is a generic alias for collections.OrderedDict.
        ([pylance-release#151](https://github.com/microsoft/pylance-release/issues/151))
    -   Enhancement: Added support for new Python extension callback so Pyright extension is notified when pythonPath is modified.
    -   Bug Fix: Fixed bug in docstring trimming code that resulted in some docstrings (those consisting of two lines where the second line was empty) not appearing when hovering over functions.
    -   Bug Fix: Fixed bug in type checker that resulted in incorrect error when creating a generic type alias with a compatible TypeVar as one of the type arguments.
    -   Bug Fix: Fixed bug that caused value expressions for default parameter values in lambdas to be evaluated within the wrong scope resulting in errors if the lambda scope had a same-named symbol.
    -   Bug Fix: Fixed bugs in handling of wildcard imports. First, it was not properly handling the implicit introduction of symbol A in the statement `from .A import *`. Second, it was implicitly including submodules as part of the wildcard, and it shouldn't.
    -   Bug Fix: Fixed bug that resulted in incorrect error when using an unpack operator in an argument expression that corresponds to a \*varg parameter in the callee.
    -   Bug Fix: Fixed recent regression that caused `isinstance` check to emit a bad error when `self.__class__` was passed as a second argument.

## 2020.7.3 (21 July 2020)

-   Fixed typo in marketplace entry's readme.

In addition, Pylance's copy of Pyright has been updated from 1.1.53 to 1.1.54, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Enhancement: Changed logic for reportMissingModuleSource diagnostic rule so it isn't reported for stub files.
    -   Enhancement: Added support for typing.OrderedDict, which is a generic alias for collections.OrderedDict.
        ([pylance-release#151](https://github.com/microsoft/pylance-release/issues/151))
    -   Bug Fix: Fixed bug in docstring trimming code that resulted in some docstrings (those consisting of two lines where the second line was empty) not appearing when hovering over functions.
    -   Bug Fix: Fixed bug in type checker that resulted in incorrect error when creating a generic type alias with a compatible TypeVar as one of the type arguments.
    -   Bug Fix: Fixed bug that caused value expressions for default parameter values in lambdas to be evaluated within the wrong scope resulting in errors if the lambda scope had a same-named symbol.
-   [1.1.54](https://github.com/microsoft/pyright/releases/tag/1.1.54)
    -   Enhancement: Added json schema for mspythonconfig.json (in addition to pyrightconfig.json).
    -   Enhancement: Updated config file watcher logic so it can detect when a new config file is added to a workspace.
    -   Bug Fix: "Find all references" should not return references to a symbol within library code unless that library source file is currently open in the editor.
    -   Bug Fix: Fixed bug in type checker that caused a crash when analyzing an abstract class with a constructor that contained two or more parameters, all of which are unannotated.
        ([pylance-release#118](https://github.com/microsoft/pylance-release/issues/118))
    -   Bug Fix: Fixed pyrightconfig.json JSON schema to accept "information" as a valid diagnostic severity setting.
    -   Enhancement: Updated log levels for messages logged by the Pyright service. Some log levels were "info" but should have been "warning" or "error".
        ([pylance-release#120](https://github.com/microsoft/pylance-release/issues/120))
    -   Bug Fix: Fixed bug that caused incorrect type evaluation for \*args or \*\*kwargs parameters if no type annotation was present. This bug also affected completion suggestions for these parameters.
        ([pylance-release#119](https://github.com/microsoft/pylance-release/issues/119))
    -   Bug Fix: Fixed a bug that resulted in Pyright attempting to parse and analyze binaries (native libraries) like ".pyd" and ".so" files.
        ([pylance-release#124](https://github.com/microsoft/pylance-release/issues/124))
    -   Bug Fix: Fixed bug in argument/parameter matching when an unpack operator is used in the argument and the parameter is a \*varg type.
    -   Enhancement: Renamed setting "pyright.useLibraryCodeForTypes" to "python.analysis.useLibraryCodeForTypes" for compatibility with Pylance. The older setting name is still supported but will be removed in the future.
    -   Enhancement: Added code to handle the case where a class is assigned to a type described by a callable protocol object. In this case, the class constructor's signature should be compared against the `__call__` signature defined in the protocol.
    -   Bug Fix: Fixed bug in import resolver that caused imports that referred to local namespace packages not to resolve.
    -   Bug Fix: Fixed bug that caused enum names that were not uppercase to be handled incorrectly.
    -   Bug Fix: Fixed bug that caused incorrect type analysis when a package `__init__.py` imported and re-exported a symbol that matched the submodule it was being imported from, e.g. `from .foo import foo`.
    -   Bug Fix: Fixed bug in type analyzer where default value expressions for lambda parameters were not being evaluated. This meant that errors related to these expressions were not reported, and symbols referenced within them were marked as unreferenced.

## 2020.7.2 (15 July 2020)

-   Allow find all references to search libraries if invoked from non-user files.

In addition, Pylance's copy of Pyright has been updated from 1.1.51 to 1.1.53, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Updated config file watcher logic so it can detect when a new config file is added to a workspace.
-   [1.1.53](https://github.com/microsoft/pyright/releases/tag/1.1.53)
    -   Bug Fix: Fixed bug in parser where it was emitting a spurious error about function return type annotations being a tuple when it was simply enclosed in parentheses.
    -   Bug Fix: Fixed a bug that caused completion suggestions not to work for the LHS of a member access expression (e.g. the "a" in "a.b").
    -   Bug Fix: Fixed diagnostic message for "partially unknown" types (used in strict mode). It was incorrectly using the "unknown" message rather than "partially unknown", which could lead to confusion.
    -   Enhancement: Changed type printing logic to emit "Unknown" annotations when in strict mode to make it clearer to the user which part of the type is unknown.
    -   Bug Fix: Fixed bug that caused extension to report empty diagnostics for all tracked files when unnecessary (in particular, when the diagnostic mode is set to openFilesOnly and the file is not open).
    -   Enhancement: Added partial support for mypy-supported variant of "# type: ignore" comment where specific error codes in square brackets after the "ignore". Pyright doesn't honor the specific error codes but now treats it as a normal # type: ignore" comment.
        ([pylance-release#108](https://github.com/microsoft/pylance-release/issues/108))
    -   Bug Fix: Fixed bug that caused the arguments of a call to remain unanalyzed if the LHS of the call was not callable. This resulted in omitted errors and spurious unreferenced symbols.
    -   Bug Fix: Changed diagnostic for second argument to "Enum" call to be dependent on the reportGenalTypeIssues diagnostic rule rather than unconditional.
    -   Bug Fix: Fixed recent regression relating to "isinstance" type narrowing when the type of the target is a constrained TypeVar.
    -   Bug Fix: Fixed bug in the handling of the NewType function introduced in PEP 484. The previous code was not synthesizing a constructor (`__init__` method) as specified in the PEP.
    -   Enhancement: Changed fallback mechanism for detecting the configured python interpreter to use the shell command "python3" first and then "python" if that fails. This is preferable on Linux and MacOS because "python" typically points to a Python 2.7 interpreter.
    -   Enhancement: Added parser error for relative imports of the form "import .abc". This is treated as a syntax error by the Python interpreter and should be flagged as such.
    -   Bug Fix: Fixed bug with "from . import a" form of import. Diagnostic was not logged when "a" could not be resolved.
-   [1.1.52](https://github.com/microsoft/pyright/releases/tag/1.1.52)
    -   Bug Fix: Fixed escaping of literal strings when printing Literal string types.
    -   Enhancement: Improved completion suggestions related to member access expressions (e.g. obj.method) by binding the method to the object when appropriate.
    -   Enhancement: When hovering over class name that is used in a constructor call, display the `__init__` method signature rather than the class.
    -   Bug Fix: Fixed recent regression in unreachable code reporting at the module level.
        ([pylance-release#107](https://github.com/microsoft/pylance-release/issues/107))
    -   Bug Fix: Removed error message for unexpected dynamic argument types to `type` initializer.
        ([pylance-release#114](https://github.com/microsoft/pylance-release/issues/114))
    -   Bug Fix: Fixed a bug in the code that validates an exception type in an "except" clause. It was not properly handling the case where the type of the exception was specified as a `Type[X]` object.
    -   Bug Fix: Reverted part of a previous change where constrained type vars were specialized as a union of the constrained types. Changed logic to use first constrained type only.
    -   Bug Fix: Fixed bug in logic that detects assignment compatibility for function types. It wasn't properly handling generic parameters, including synthesized TypeVar types used for "self" parameters.
    -   Bug Fix: Added diagnostic for TypeVar or generic class with type args being used as a second argument for isinstance or issubclass. These will raise a TypeError exception at runtime.
    -   Enhancement: Changed Pyright import resolution order to match that described in PEP 561. In particular, stubs in stubPath are now searched prior to user code, and third-party typeshed stubs are searched only after installed packages are searched for stub packages and inline stubs. There is one place where Pyright's import resolution still differs from a strict interpretation of PEP 561: it searches stdlib typeshed stubs first (unless typeshedPath is defined, in which case it searches there). This is more consistent with the way the Python interpreter resolves stdlib types.
    -   Bug Fix: Fixed bug in handling of constructor that uses a specialized class (e.g. `MyClass[int]()`). The previous code was inappropriate overriding the provided type arguments as part of bidirectional inference logic.
    -   Bug Fix: Fixed bug that caused spurious errors when assigning a specialized object/class to a variable whose type is a specialized base class of the specialized object/class.

## 2020.7.1 (10 July 2020)

-   Fixed background analysis thread, which prevented diagnostics (syntax checks, import warnings, etc) from working.
    ([pylance-release#86](https://github.com/microsoft/pylance-release/issues/86))
-   Fixed setting and survey banners blocking startup.

## 2020.7.0 (9 July 2020)

-   Hovers for class invocations will now show the `__init__` method's docstring.
-   Import organization has been disabled to prevent conflicts with the Python extension's import sorting.
    ([pylance-release#23](https://github.com/microsoft/pylance-release/issues/23))
-   Docstrings for bound methods will no longer show `self` in the signature.
-   Fixed multi-line string literals in tooltips.
-   IntelliCode now operates in environments without OpenMP.
-   The `pandas` stubs have been improved.
    ([pylance-release#13](https://github.com/microsoft/pylance-release/issues/13), [pylance-release#71](https://github.com/microsoft/pylance-release/issues/73), [pylance-release#73](https://github.com/microsoft/pylance-release/issues/71))
-   `pyplot.subplots`'s signature has been fixed.
    ([pylance-release#43](https://github.com/microsoft/pylance-release/issues/43))
-   The bundled copy of typeshed has been updated.
-   The overall startup time and responsiveness has been improved.

In addition, Pylance's copy of Pyright has been updated from 1.1.46 to 1.1.51, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed recent regression in unreachable code reporting at the module level.
    -   Enhancement: Removed error message for unexpected dynamic argument types to `type` initializer.
-   [1.1.51](https://github.com/microsoft/pyright/releases/tag/1.1.51)
    -   New Feature: Added document highlight provider. When you click on a symbol in the editor, all other symbols within the same file that have the same name and have the same semantic meaning are also highlighted.
        ([pylance-release#42](https://github.com/microsoft/pylance-release/issues/42))
    -   Enhancement: If reportGeneralTypeIssues rule is disabled, don't replace assigned type with declared type because it will lead to additional errors that will confuse users.
        Enhancement: Added type narrowing support for "in" operator when RHS is a specialized list, set, frozenset, or deque.
    -   Enhancement: Added logic to validate that RHS operand used with "in" and "not in" operators support the `__contains__` magic method.
    -   Bug Fix: Fixed bug where "field" initialization of dataclass member didn't take into account "default" or "default_factory" parameters when determining whether the field had a default value.
    -   Bug Fix: Added code to deal with the special case where a method declared with a "def" statement is later overwritten with a callable instance variable.
    -   Bug Fix: Fixed bug whereby a TypeVar type was not treated the same when it was alone versus within a union leading to some subtle differences in error reporting. Also changed specialization of constrained TypeVars to be a union of constrained types rather than Unknown if the TypeVar is not used as a type argument.
    -   Bug Fix: Fixed bug in diagnostic message for constrained TypeVar type mismatch. The wrong type was being printed leading to confusing errors.
    -   Bug Fix: Fixed a bug that caused incorrect linearization of classes during MRO calculation.
    -   Bug Fix: Fixed bug in synthesized version of `get` method for `TypedDict` class. It should provide an overload that allows for any str key and return an "Unknown" type.
-   [1.1.50](https://github.com/microsoft/pyright/releases/tag/1.1.50)
    -   Bug Fix: Fixed regression in completion provider when retrieving suggestions for "self.". Added test to cover this case.
        ([pylance-release#53](https://github.com/microsoft/pylance-release/issues/53))
    -   Enhancement: Changed "x is not iterable" diagnostic to be part of the "reportGeneralTypeIssues" rule so it doesn't get reported if typeCheckingMode is "off".
        ([pylance-release#59](https://github.com/microsoft/pylance-release/issues/59))
    -   Bug Fix: Fixed bug that caused incorrect behavior when a symbol was imported multiple times in the same file.
    -   Bug Fix: Fixed bug that caused Callable instance variables to be treated as though they needed to be "bound" to the object at the time they were accessed. This resulted in spurious errors about parameter count because an implicit "self" parameter was assumed.
    -   Enhancement: Improved type analysis performance by 5-10% on typical code and by significantly more on certain code sequences that involve many if statements within a loop. This optimization uses code flow caching to determine when incomplete types (those that haven't been fully resolved) are potentially stale.
        ([pylance-release#57](https://github.com/microsoft/pylance-release/issues/57))
    -   Bug Fix: Fixed recent regression related to imports of the form "from .x import y" within an `__init__.py(i)` file.
    -   Enhancement: Changed type analyzer to use module-level `__getattr__` for types only if the file is a stub.
    -   Enhancement: Added code to prevent "variable possibly unbound" error from propagating to other variables. It should be reported only once.
    -   Enhancement: Switched "pyright.typeCheckingMode" to "python.analysis.typeCheckingMode" for compatibility with Pylance.
    -   Enhancement: Moved a few parameter-related diagnostics to the "reportGeneralTypeIssues" diagnostic rule rather than being unconditional errors.
        ([pylance-release#15](https://github.com/microsoft/pylance-release/issues/15), [pylance-release#39](https://github.com/microsoft/pylance-release/issues/39), [pylance-release#54](https://github.com/microsoft/pylance-release/issues/54))
    -   Bug Fix: Fixed bug that resulted in incorrect type inference for a member variable that is not assigned within a class but is assigned within an ancestor class.
    -   Enhancement: Added type narrowing support for "is" and "is not" operator where RHS is an enum literal value.
-   [1.1.49](https://github.com/microsoft/pyright/releases/tag/1.1.49)
    -   Bug Fix: Fixed bug that caused incorrect type to be determined for \*args and \*\*kwargs parameters in some contexts.
        ([pylance-release#20](https://github.com/microsoft/pylance-release/issues/20))
    -   Enhancement: Updated typeshed stubs to the latest versions from the typeshed repo.
    -   Bug Fix: Fixed bug in tokenizer where it was generating an error if escaped unicode characters (using the \N{name} escape) contained a space in the name.
        ([pylance-release#25](https://github.com/microsoft/pylance-release/issues/25))
    -   Enhancement: Improved parse recovery for statements that are supposed to end in a colon followed by a suite of other indented statements. Previously, a missing colon or expression error resulted in a cascade of additional errors.
        ([pylance-release#22](https://github.com/microsoft/pylance-release/issues/22))
    -   Enhancement: Improved error message for overloaded calls where no overload matches the provided arguments.
    -   Bug Fix: Fixed bug in unreachable code detection and reporting. The logic was previously split between the binder (which used proper code flow analysis) and the checker (which didn't use code flow analysis but had access to NoReturn - call information). The new code combines everything into the checker and uses both code flow analysis and NoReturn call info.
        ([pylance-release#31](https://github.com/microsoft/pylance-release/issues/31))
    -   Bug Fix: Added code to include a symbol in a module if the source file is an `__init__.py(i)` and a relative import of the form "from .x.y.z import X" is used. In this case, the symbol "x" should appear within the module's namespace.
    -   Bug Fix: Fixed bug in pyrightconfig schema. The defaults for several settings were using strings "true" and "false" rather than booleans true and false.
    -   Bug Fix: Fixed bug in parser that generated a spurious error when an unparenthesized assignment expression (walrus operator) was used as an argument. PEP 572 indicates that this should be allowed in cases where the argument is not named.
    -   Enhancement: Changed constructor type analysis logic to always specialize the instantiated instance.
    -   Bug Fix: Fixed bug in reportAssertAlwaysTrue diagnostic. It wasn't properly handling tuples of indeterminate length.
    -   Bug Fix: Fixed bug in import resolution that resulted in an unresolved import when a local folder was present with the same name as the imported third-party library.
    -   Bug Fix: Fixed bug that caused diagnostics for unopened files to remain in "problems" panel after switching diagnostic mode from "workspace" to "open files only".
    -   Bug Fix: Fixed bug in parsing of f-string expressions that contain nested braces.
        ([pylance-release#45](https://github.com/microsoft/pylance-release/issues/45))
    -   Bug Fix: Fixed bug in import resolver where it was not preferring regular package imports over namespace packages.
        ([pylance-release#52](https://github.com/microsoft/pylance-release/issues/52))
-   [1.1.48](https://github.com/microsoft/pyright/releases/tag/1.1.48)
    -   Enhancement: Added support for accessing metaclass members from class. This allows, for example, access to the `__members__` attribute of an Enum class.
    -   Enhancement: Added type completion support for class attributes provided by a metaclass.
    -   Bug Fix: Fixed bug that caused unbound variables to go unreported if they had type annotations.
    -   Bug Fix: Fixed bug in type narrowing logic for isinstance call. It wasn't properly handling bound TypeVar types. This includes synthesized bound TypeVars like those used for unannotated "self" and "cls" parameters.
    -   Bug Fix: Fixed bug that caused stand-alone expression statements (those that are not included in other statements) to go unchecked, resulting in symbols potentially unreferenced and type errors unreported.
    -   Bug Fix: Fixed bug where the use of unpack operator within a tuple not surrounded by parens within a return/yield statement incorrectly reported an error when used with Python <3.8.
    -   Bug Fix: Changed signature help provider to use the `__init__` method signature (if available) for class construction expressions. It previously used the `__new__` method signature by default.
    -   Enhancement: Unaccessed function parameters are now displayed as "grayed out" in VS Code. There was previously code in place to do this, but it contained a bug that went unnoticed.
-   [1.1.47](https://github.com/microsoft/pyright/releases/tag/1.1.47)
    -   Enhancement: Improved support for type aliases, especially those with generic parameters. Type alias names are now tracked and used within printed type names.
    -   Bug Fix: Fixed recent regression in CLI that resulted in unintended verbose logging output.
    -   Bug Fix: Added minimum node version to package.json to prevent installation of pyright CLI on incompatible versions of node.
    -   Enhancement: Added code to better handle the obsolete "<>" operator from Python 2 - including a better error message and better parse recovery.
    -   Enhancement: Added special-case handling of 'NoReturn' type to allow Never type to be assigned to it. This can be used to verify exhaustive type narrowing.
    -   Bug Fix: Added code to differentiate between Protocol symbol in typing.pyi versus typing_extensions.pyi. The latter can be used on older versions of Python.
    -   Enhancement: Changed activation events to remove glob path for pyrightconfig.json, which speeds up extension activation on large projects. Added support for mspythonconfig.json

## 2020.6.1 (30 June 2020)

Initial release!

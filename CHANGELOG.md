# Changelog

## 2020.7.2 (15 July 2020)

-   Allow find all references to search libraries if invoked from non-user files.

In addition, Pylance's copy of Pyright has been updated from 1.1.51 to 1.1.53, including the following changes:

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

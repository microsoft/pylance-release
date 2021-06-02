# Changelog

## 2021.6.0 (2 June 2021)

Notable changes:

-   Libraries installed via egg/zip files are now supported (including `transformers` installed via `conda`).
    ([pylance-release#1260](https://github.com/microsoft/pylance-release/issues/1260))
-   Unannotated decorators are now treated as no-ops, rather than using type inference and potentially obscuring the signature of the function they decorate.
-   Files that were referenced but unopened will no longer be mistakenly reanalyzed when opened.
-   Tables in docstrings are now better spaced.
-   The bundled stubs for django have been updated.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.144 to 1.1.146, including the following changes:

-   [1.1.146](https://github.com/microsoft/pyright/releases/tag/1.1.146)
    -   Enhancement: Updated to the latest version of typeshed stubs.
    -   Behavior Change: Updated `reportIncompatibleVariableOverride` to avoid reporting an error when a class variable is reassigned a value in a base class without declaring its type.
    -   Bug Fix: Fixed false positive error indicating that a type alias is a variable. This results when a type alias refers to a union and that union is reformed when losing the original type alias.
    -   Enhancement: Added optimization for union creation where all subtypes are the same. This optimization commonly reduces the need to create new types during code flow operations. It also retains type alias info more faithfully.
    -   Enhancement: Added support for `__qualname__` and `__module__` attributes within a class body.
        ([pylance-release#1376](https://github.com/microsoft/pylance-release/issues/1376))
    -   Behavior Change: Changed call expression evaluation logic to not skip return type inference when there are errors detected during argument expression evaluation. This was previously added as an optimization, but it was leading to confusing results in some cases.
    -   Enhancement: Enhanced logic to detect unannotated decorator functions and treat them as no-ops rather than using return type inference, which often leads to incorrect and confusing results for decorators.
    -   Bug Fix: Fixed bug in pattern matching logic for class patterns where the class uses properties or descriptors for the targeted attributes.
    -   Enhancement (from pylance): Added support for libraries packages as zip/egg containers.
-   [1.1.145](https://github.com/microsoft/pyright/releases/tag/1.1.145)
    -   Bug Fix: Fixed bug that resulted in the incorrect type when bidirectional type inference (an "expected type") was used in conjunction with the `tuple()` constructor.
        ([pylance-release#1359](https://github.com/microsoft/pylance-release/issues/1359))
    -   Behavior Change: Changed logic to avoid reanalyzing a file when it is opened in the editor if we have already analyzed it and the file contents are the same as before.
    -   Bug Fix: Improved handling of call expressions where the call is a union and some of the subtypes return NoReturn and others do not.
    -   Behavior Change: Changed the logic that validates the assignment to instance variables that are marked `Final`. Previously, only one such assignment was allowed even if it was within an `__init__` method. It now allows an arbitrary number of assignments (conditional or otherwise) as long as they occur within an `__init__` method.
    -   Enhancement: Enhanced "reportIncompatibleVariableOverride" diagnostic check to detect the case where a base class declares a class variable and a child class tries to override it with an instance variable or vice versa.
    -   Bug Fix: Added logic to handle the case where a dataclass subclass overrides a member of its parent class with a ClassVar and another dataclass then subclasses from the child.
    -   Enhancement: Enhanced type stub generator so it doesn't emit "object" as base class, since that's implied in Python 3.x.
    -   Enhancement: Enhanced type stub generator to emit inferred function and method return types as comments.
    -   Behavior Change: Removed false positive error reported for a "bare" `raise` statement outside of an `except` clause.
        ([pylance-release#1365](https://github.com/microsoft/pylance-release/issues/1365))
    -   Bug Fix: Changed type variable constraint solver to preserve literal types when matching type arguments from other class types. In other cases, it typically "strips" the literal, widening the type to a str, int, etc. This change allows proper type evaluation in certain cases where a literal type is specified in a type annotation, such as with `Set[Literal["foo"]]`.
    -   Bug Fix: Fixed bug in code flow engine where it was sometimes evaluating the wrong type when cycles occurred in type dependencies.
        ([pylance-release#1356](https://github.com/microsoft/pylance-release/issues/1356))
    -   Bug Fix: Fixed bug that can result in a crash when indexing a file that includes a nested function or lambda that is used for type inference.
    -   Enhancement: Improved detection and reporting of illegal type alias recursion cases — e.g. when a possible type alias refers to a function that uses the type alias in parameter or return type annotations.
    -   Enhancement: Changed type printer to include a "\*" after a type if it is conditionally associated with a TypeVar constraint.
    -   Bug Fix: Augmented type checking logic for generator expressions to allow `await` keyword even though enclosing function isn't async. Also allowed generator expression to be evaluated as `AsyncGenerator` rather normal `Generator`.
        ([pylance-release#1348](https://github.com/microsoft/pylance-release/issues/1348))
    -   Enhancement: Changed the way conditional constraints are tracked in the type evaluator. This is a significant change that simplifies the logic and handles some cases that the old approach did not.

## 2021.5.4 (26 May 2021)

Notable changes:

-   Auto-import quick fixes now more closely match auto-import completions.
    ([pylance-release#1250](https://github.com/microsoft/pylance-release/issues/1250))
-   TypedDict support has been improved, supporting `**kwargs` unpacking checks and tagged union narrowing.
    ([pylance-release#374](https://github.com/microsoft/pylance-release/issues/374), [pylance-release#1328](https://github.com/microsoft/pylance-release/issues/1328), [pylance-release#1240](https://github.com/microsoft/pylance-release/issues/1240))
-   A bug that led to infinite recursion has been fixed.
    ([pylance-release#1315](https://github.com/microsoft/pylance-release/issues/1315))
-   Memory usage when indexing is enabled has been improved.
-   The bundled stubs for pandas have been updated.
-   The bundled stubs now include partial stubs for `gym`.

In addition, Pylance's copy of Pyright has been updated from 1.1.141 to 1.1.144, including the following changes:

-   [1.1.144](https://github.com/microsoft/pyright/releases/tag/1.1.144)
    -   Bug Fix: Changed CLI to not use process.exit() but instead return normally. The previous code sometimes resulted in truncated output.
    -   Enhancement: Added error for keyword-only parameter separator or position-only parameter separator appearing in a function signature after an "\*args" parameter. This will result in a runtime error.
        ([pylance-release#1341](https://github.com/microsoft/pylance-release/issues/1341))
    -   Enhancement: Improved error message for missing \*\*kwargs parameter when assigning one function to another.
    -   Bug Fix: Fixed bug in logic that converts a type into a text representation. It wasn't properly adding the scope for a ParamSpec in certain circumstances, so instead of outputting `P@scope`, it was outputting `P`.
    -   Bug Fix: Fixed bug in specialization of generic class that contains only one type variable that is a ParamSpec.
    -   Bug Fix: Fixed bugs that prevented ParamSpec annotations `P.args` and `P.kwargs` from working properly when the annotation was in quotes.
    -   Bug Fix: Fixed false positive error in check for inappropriate use of contravariant type var in return type annotation. It should not generate an error when the contravariant type var is part of a union.
    -   Enhancement: Improved error message consistency for for "cannot assign to None" condition.
-   [1.1.143](https://github.com/microsoft/pyright/releases/tag/1.1.143)
    -   Bug Fix: Added missing recursion check that resulted in stack overflow in type evaluator.
        ([pylance-release#1315](https://github.com/microsoft/pylance-release/issues/1315))
    -   Enhancement: Added support for unpacked dictionary argument in function calls when the unpacked expression is a TypedDict.
        ([pylance-release#374](https://github.com/microsoft/pylance-release/issues/374), [pylance-release#1328](https://github.com/microsoft/pylance-release/issues/1328))
    -   Enhancement: Improved error message for the case where positional-only parameters are used in a function and a caller does not provide enough arguments.
    -   Bug Fix: Improved logic for argument matching for call expressions where the call includes keyword-only parameters and the call expression includes an unpacked list argument.
        ([pylance-release#1319](https://github.com/microsoft/pylance-release/issues/1319))
    -   Bug Fix: Fixed bug in type evaluation of list comprehensions when literal types were involved. The literal types were being widened to their associated non-literal types.
    -   Enhancement: Improved `isinstance` type narrowing logic to accommodate the case where the first argument to `isinstance` is a module and the second argument is a runtime-checkable protocol class.
    -   Bug Fix: Fixed regression that caused false positive in the case where a `Callable` type was used that defined its own TypeVar scope and was later matched against a `self` parameter in an instance method.
    -   Enhancement: Enhanced "reportIncompatibleVariableOverride" diagnostic check so it applies to instance variables defined within a method (e.g. `self.var: str = ""`) in addition to class variables.
    -   Enhancement: Added type narrowing support for index expressions where the index value is a string literal.
    -   Enhancement: Added support for "tagged union" type narrowing when the conditional expression is of the form `x[K] == V` or `x[K] != V` where `x` is a union of TypedDict objects and `K` is a literal str key value that refers to a field with a literal type and `V` is a literal value.
        ([pylance-release#1240](https://github.com/microsoft/pylance-release/issues/1240))
-   [1.1.142](https://github.com/microsoft/pyright/releases/tag/1.1.142)
    -   Bug Fix: Fixed false negative (missing error) due to bug in dictionary expression bidirectional type inference logic when the expected type included a union.
    -   Enhancement: Added support for subscript expressions that contain slices when applied to tuples with known lengths.
    -   Bug Fix: Fixed false negative condition where a protocol class was treated as a callback protocol even though it included members other than `__call__`.
    -   Bug Fix: Fixed false positive error when a builtin symbol was used in a file but later redeclared within the module scope.
        ([pylance-release#1320](https://github.com/microsoft/pylance-release/issues/1320))
    -   Bug Fix: Fixed bug in "expression printer" which is used in some error messages. It was not properly preserving parentheses for binary operation expressions.
    -   Bug FIx: Fixed false positive error for "missing type arguments" that was surfaced when changes were made within typeshed's types.pyi stub.

## 2021.5.3 (19 May 2021)

Notable changes:

-   A number of CPU and memory improvements have been made, improving parsing, indexing, and overall performance.
-   Libraries which indicate that they are `py.typed` will now be correctly preferred over typeshed, following PEP 561. This allows the use of the types in well-typed libraries such as the newly-released Flask 2.0, PyJWT, and tornado, improving completions, hover, navigation, and the type checking experience.
    ([pylance-release#1197](https://github.com/microsoft/pylance-release/issues/1197))
-   Auto-imports now require the first character to match before fuzzy matching is applied, which reduces the number of unwanted completions and greatly improves performance when indexing is enabled.
-   Extract method now supports extracting comments.
    ([pylance-release#1262](https://github.com/microsoft/pylance-release/issues/1262))
-   Variable names using supplementary characters are now supported.
    ([pylance-release#1286](https://github.com/microsoft/pylance-release/issues/1286))
-   Tables in docstrings are now supported.
-   Incompatible type diagnostics will now fully qualify type names if the incompatible types have the same short name.
    ([pylance-release#1306](https://github.com/microsoft/pylance-release/issues/1306))
-   A bug which caused some imports from `pywin32` to not be resolved has been fixed.
    ([pylance-release#1423](https://github.com/microsoft/pylance-release/issues/1423))
-   Added stubs for pywin32, openpyxl.
    ([pylance-release#947](https://github.com/microsoft/pylance-release/issues/947), [pylance-release#1423](https://github.com/microsoft/pylance-release/issues/1423))
-   The bundled stubs for django and pandas have been updated.
-   File watcher events from `.git` directories will no longer trigger reanalysis.
    ([pylance-release#1282](https://github.com/microsoft/pylance-release/issues/1282))
-   The import resolver now supports typeshed's VERSIONS file, which indicates which versions of Python each standard library module is available.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.137 to 1.1.141, including the following changes:

-   [1.1.141](https://github.com/microsoft/pyright/releases/tag/1.1.141)
    -   Enhancement: Improved "is None" and "is not None" type narrowing logic for constrained TypeVars that include `None` as one of the constraints.
    -   Enhancement: Improved error message for illegal character in token and surrogate character codes combinations that are not allowed in identifiers.
    -   Enhancement: Added support for more surrogate character ranges that I didn't realize existed when I added the initial support.
    -   Behavior change: Don't prefer py.typed libraries when the execution environment is typeshed.
    -   Bug Fix: Fixed bug in signature help provider where it was not properly handling a call with a type `Type[T]`.
    -   Bug Fix: Fixed bug in code that handles "super" call when a `cls` variable is passed as the first argument.
    -   Bug Fix: Changed the way the current parameter index is specified in signature help to better conform to LSP standard.
    -   Enhancement: Improved the "X is incompatible with Y" error message in the case where types X and Y have the same short name. In this case, the fully-qualified names will be used to provide clarity.
    -   Bug Fix: Fixed bug that resulted in false positive when generic type was used for iterable within a list comprehension.
    -   Bug Fix: Fixed bug that resulted in incorrect errors when using a TypeVar imported from another file and referenced using a member access expression (e.g. `typing.AnyStr`).
    -   Enhancement: Added support for `defaults` argument in `namedtuple` constructor, which marks the rightmost input parameters to the resulting named tuple as having default values.
    -   Behavior change (from pylance): Filter auto-imports more strictly to reduce the number of completions returned. Matches require at least the first character to match before fuzzy matching is applied.
    -   Enhancement (from pylance): Add support for tables in docstrings.
-   [1.1.140](https://github.com/microsoft/pyright/releases/tag/1.1.140)
    -   Bug Fix: Fixed bug that caused parameters in overloaded functions not to be marked as accessed, as was intended.
    -   Bug Fix: Fixed false negative when the same name was defined in both an outer and inner function and referenced in the inner function prior to being assigned.
    -   Enhancement: Added support for identifiers that contain Unicode characters that require two UTF16 character codes (surrogates). This allows identifiers to use characters in the Unicode blocks for Egyptian Hieroglyphs, Linear B Ideograms, Cuneiform, Phoenician, etc.
    -   Enhancement: Added new diagnostic rule "reportIncompleteStub", which reports a diagnostic for a module-level `__getattr__` function in a type stub, indicating that it's incomplete. This check was previously part of the "reportUnknownMemberType" diagnostic rule.
    -   Behavior Change: Disabled support for keyword arguments in subscript expressions because PEP 637 was rejected.
    -   Bug Fix: Fixed bug in the type specialization for ParamSpec when the return type contains no generics.
    -   Bug Fix: Changed TypeGuard behavior to evaluate the return type of a call expression that invokes a type guard function to be 'bool' rather than 'TypeGuard[T]'.
    -   Behavior Change: Changed TypeGuard behavior to allow a type guard function to be passed as a callback that expects the return type to be bool.
    -   Bug Fix: Removed explicit check for Python 3.10 when using ParamSpec. It's possible to use it with older versions of Python if importing from `typing_extensions`.
    -   Bug Fix: Fixed bug that caused a false positive error when applying a subscript operation on a TypeVar.
    -   Bug Fix: Fixed bug that resulted in a false positive error when the second argument to `isinstance` or `issubclass` was a union that included both a single type and a tuple of types.
        ([pylance-release#1294](https://github.com/microsoft/pylance-release/issues/1294))
    -   Enhancement: Updated typeshed stubs to the latest version.
    -   Enhancement: Added support in typeshed VERSIONS file for submodules.
-   [1.1.139](https://github.com/microsoft/pyright/releases/tag/1.1.139)
    -   Enhancement: Updated typeshed to the latest.
    -   Enhancement: Added support for typeshed VERSION file, which indicates which stdlib modules are available in each version of Python.
    -   Bug Fix: Fixed bug that resulted in symbols being inappropriately marked "unaccessed" when they were accessed within a keyword argument used within a class declaration.
        ([pylance-release#1272](https://github.com/microsoft/pylance-release/issues/1272))
    -   Bug Fix: Fixed false positive error when a dataclass declares an instance variable but a subclass redeclares a class variable of the same name.
    -   Bug Fix: Fixed type narrowing bug with 'isinstance' checks that involve protocol classes. The bug resulted in false positive errors with the reportUnnecessaryIsInstance check.
    -   Enhancement: Added support for callback protocols that use overloaded `__call__` methods.
        ([pylance-release#1276](https://github.com/microsoft/pylance-release/issues/1276))
    -   Enhancement (from pylance): Improved performance of tokenizer's handling of string literals.
    -   Bug Fix (from pylance): Ignore updates to ".git" file so they don't trigger reanalysis.
    -   Bug Fix: Fixed false positive error in check for overload implementation consistency when one of the overloaded methods in a generic class provides an explicit type annotation for "self" or "cls" but the implementation does not.
    -   Enhancement: Improved "is None" and "is not None" type narrowing logic to handle constrained TypeVar that includes None as one of the constraints.
    -   Bug Fix: Fixed false positive error when a `__getattr__` method is present. The previous logic was assuming that `__getattr__` could provide a magic method value (e.g. for `__add__`).
        ([pylance-release#1252](https://github.com/microsoft/pylance-release/issues/1252))
    -   Bug Fix: Prefer py.typed libraries over typeshed for consistency with PEP 561.
    -   Bug Fix: Improved validation for function calls where the function signature includes keyword arguments without default values that are not directly matched by keyword arguments but are matched by a **kwargs argument. In this situation, the type of the **kwargs values should be verified to be compatible with the type of the keyword parameters.
    -   Bug Fix: Fixed bug in lambda type evaluation for lambdas that use an \*args parameter. The parameter type was not being transformed into a tuple, as it should have been.
        ([pylance-release#1284](https://github.com/microsoft/pylance-release/issues/1284))
    -   Enhancement: Improved diagnostic message for constant redefinition to make it clear that the symbol is assumed to be constant because its name is uppercase.
-   [1.1.138](https://github.com/microsoft/pyright/releases/tag/1.1.138)
    -   Bug Fix: Fixed bug in handling special-case types in typing.pyi or typing_extensions.pyi. The RHS of the assignment was not being evaluated, so symbols referenced in the RHS were not be marked as accessed.
    -   Bug Fix: Changed special-case handling of "overload" definition in typying.pyi stub. New versions of this stub have changed the definition from an object to a function.
    -   Bug Fix: Fixed recent regression in handling of f-strings that are also raw.

## 2021.5.2 (13 May 2021)

Pylance has reached stable and is officially out of public preview! (https://aka.ms/announcing-pylance-stable)

## 2021.5.1 (6 May 2021)

This is a hotfix release, fixing raw format strings ([pylance-release#1241](https://github.com/microsoft/pylance-release/issues/1241)) and handling language server settings changes available in the next Python extension release.

## 2021.5.0 (5 May 2021)

Notable changes:

-   A number of CPU and memory improvements have been made, improving indexing, docstring conversion, and peak memory usage.
-   Pylance insiders will now be automatically enabled when Python insiders is enabled. This can be overridden by explicitly setting `pylance.insidersChannel`.
-   Docstring support for compiled standard library modules (such as `math`, `sys`, and `time`) now handles module docstrings.
-   The bundled stubs for pandas and PIL have been updated.
    ([pylance-release#556](https://github.com/microsoft/pylance-release/issues/556), [pylance-release#660](https://github.com/microsoft/pylance-release/issues/660), [pylance-release#769](https://github.com/microsoft/pylance-release/issues/769), [pylance-release#779](https://github.com/microsoft/pylance-release/issues/779))
-   The "report issue" command can now be run in any file, including Jupyter notebooks.
    ([pylance-release#1207](https://github.com/microsoft/pylance-release/issues/1207))
-   A number of crashes have been fixed.
    ([pylance-release#1211](https://github.com/microsoft/pylance-release/issues/1211), [pylance-release#1218](https://github.com/microsoft/pylance-release/issues/1218), [pylance-release#1219](https://github.com/microsoft/pylance-release/issues/1219))
-   Python 3.10's new `match` and `case` keywords will now be highligted as keywords when semantic tokenization is enabled.
    ([pylance-release#1215](https://github.com/microsoft/pylance-release/issues/1215))
-   Assignment expressions in the class scope are no longer incorrectly disallowed.
    ([pylance-release#1213](https://github.com/microsoft/pylance-release/issues/1213))
-   Completions are no longer incorrectly provided in the string portion of f-strings.
    ([pylance-release#1226](https://github.com/microsoft/pylance-release/issues/1226))
-   Pylance's copy of typeshed has been updated.
    ([pylance-release#1216](https://github.com/microsoft/pylance-release/issues/1216))

In addition, Pylance's copy of Pyright has been updated from 1.1.136 to 1.1.137, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug in handling special-case types in typing.pyi or typing_extensions.pyi. The RHS of the assignment was not being evaluated, so symbols referenced in the RHS were not be marked as accessed.
-   [1.1.137](https://github.com/microsoft/pyright/releases/tag/1.1.137)
    -   Bug Fix: Fixed bug in type inference of dictionary, list and set expressions when they contain classes or class instances that are apparently the same type but internally appear different because they are "pseudo-generic". Pseudo-generic classes are those that have no type annotations in the `__init__` method and are treated internally as generics to improve type inference.
    -   Bug Fix: Fixed bug that caused false positive error when assigning `Type[Any]` to `type`.
    -   Bug Fix: Fixed false positive error when assignment expression (i.e. walrus operator) is used within a class scope.
    -   Enhancement: Updated typeshed stubs to the latest.
    -   Behavior Change: When in "outputjson" mode, the CLI now output log information to stderr.
    -   Enhancement: Add match and case keywords to completion provider.
    -   Bug Fix: Fixed regression that caused runtime assertion (and crash) in some rare circumstances.
    -   Performance: Eliminated O(n\*m) behavior when testing type compatibility of a union with n subtypes and a union of m subtypes when those subtypes contain mostly literals.
    -   Performance: Moved checks for string literal errors (unsupported escape characters, etc.) from binder to checker for performance reasons.
    -   Performance: Improved performance of string token value unescape logic by handling the common cases (no format string and no escape characters) using a fast path.
    -   Bug Fix (from Pylance): Fixed bug in file watching logic for config files.
    -   Performance (from Pylance): Reduced work done during parsing and binding related to doc string handling.
    -   Enhancement (from Pylance): Improved document symbol provider symbol type information.
    -   Behavior Change: Removed PEP 563 (deferred type annotation) behavior as default for Python 3.10, since the PEP was deferred.
    -   Bug Fix: Fixed bug in completion provider that caused completions to be provided when pressing "." within the string literal portion of an f-string.
    -   Performance (from Pylance): Provided special-case code paths in parser and binder to speed up symbol indexing operations.

## 2021.4.3 (29 April 2021)

Notable changes:

-   The bundled native module stubs for sklearn, numpy, and pandas have been updated.
-   Markdown-style links in docstrings will now be passed through as-is to tooltips.
-   Docstrings for all compiled standard library modules (such as `math`, `sys`, and `time`) are now supported.
    ([pylance-release#465](https://github.com/microsoft/pylance-release/issues/465))
-   Docstrings in signature help tooltips will now show the same docstrings as completion and hover tooltips.
-   Overload matching has been changed to more closely match matching in other type checkers.
    ([pylance-release#549](https://github.com/microsoft/pylance-release/issues/549), [pylance-release#1111](https://github.com/microsoft/pylance-release/issues/1111))
-   A number of bugs that could cause potentially nondeterministic behavior when semantic highlighting is enabled have been fixed.
    ([pylance-release#1180](https://github.com/microsoft/pylance-release/issues/1180), [pylance-release#1181](https://github.com/microsoft/pylance-release/issues/1181))

In addition, Pylance's copy of Pyright has been updated from 1.1.133 to 1.1.136, including the following changes:

-   [1.1.136](https://github.com/microsoft/pyright/releases/tag/1.1.136)
    -   Bug Fix: Fixed bug in diagnostic check for contravariant type variables used in a return type annotation that resulted in a false negative.
        ([pylance-release#1190](https://github.com/microsoft/pylance-release/issues/1190))
    -   Enhancement: Added minimal support for `*` and `**` parameter annotations within function annotation comments.
        ([pylance-release#1191](https://github.com/microsoft/pylance-release/issues/1191))
    -   Behavior Change: Modified algorithm for invariant union type assignments to avoid n^2 behavior.
    -   Bug Fix: Fixed a false positive error that occurs when a class uses itself as a type argument for one of its base classes and that base class uses a bound type variable.
    -   Enhancement: Added logic to skip the normal `__new__` constructor evaluation if the class is created by a metaclass with a custom `__call__` method.
    -   Bug Fix: Fixed bug in TypedDict type narrowing (for containment of non-required fields) that resulted in a false positive error when a narrowed type was later used.
    -   Bug Fix: Fixed bug in type variable constraint solver that resulted in a confusing false positive error in circumstances involving contravariant type variables (e.g. when dealing with callback protocols) and a combination of `Type[T]` and `T` within the callback signature.
    -   Enhancement (from pylance): Improved formatting of doc strings in tool tips.
-   [1.1.135](https://github.com/microsoft/pyright/releases/tag/1.1.135)
    -   Behavior Change: Changed behavior of function overload evaluation to more closely match the behavior of other type checkers. Notably, if one or more argument have union types, they are expanded, and each combination of argument union subtypes can use different overloads.
    -   Bug Fix: Fixed bug that caused false positive error when assigning a function with no position-only marker to a function with a position-only marker.
        ([pylance-release#1187](https://github.com/microsoft/pylance-release/issues/1187))
    -   Enhancement: Added support for call arguments whose types are constrained type variables and must be constrained to a particular subtype during call evaluation because the LHS of the call imposes such constraints.
        ([pylance-release#1182](https://github.com/microsoft/pylance-release/issues/1182))
    -   Enhancement: Added support for special cases of class pattern matching as described in PEP 634.
    -   Enhancement: Added support for auto generation of `__match_args__` class variable for dataclass and named tuples.
    -   Enhancement: Added support for type narrowing of the subject expression within a "match" statement based on the matched pattern.
    -   Bug Fix: Fixed bug in type analyzer that resulted in a false positive error when a return type annotation included a generic class but omitted the type arguments.
-   [1.1.134](https://github.com/microsoft/pyright/releases/tag/1.1.134)
    -   Enhancement: Implemented first cut at generalized support for dataclass transforms.
    -   Behavior Change: Allow NoReturn return type annotation for `__init__` method.
    -   Bug Fix: Fixed bug in completion provider that resulted in no valid completion suggestions at the end of a "from x import a, " statement.
        ([pylance-release#673](https://github.com/microsoft/pylance-release/issues/673))
    -   Bug Fix: Fixed bug in type checker that led to a false positive when assigning a function to a callable type and the source contained unannotated parameters.
    -   Bug Fix: Fixed numerous bugs that result in occasional type evaluation errors, some of which appear to be somewhat non-deterministic.
        ([pylance-release#1180](https://github.com/microsoft/pylance-release/issues/1180), [pylance-release#1181](https://github.com/microsoft/pylance-release/issues/1181))
    -   Bug Fix: Fixed bug in type evaluator that caused incorrect type evaluation for annotated parameter types in some cases.
    -   Bug Fix: Fixed a bug in the type checker that resulted in a false positive error when using "|" (union) operator in parameter type annotations in some cases.
    -   Bug Fix: Changed binder logic for "from .a import x" statements in `__init__.py`. Implicit import of ".a" is performed only in cases where there is a single dot. For example, "from .a.b import x" does not implicitly import ".a.b".
        ([pylance-release#234](https://github.com/microsoft/pylance-release/issues/234))

## 2021.4.2 (21 April 2021)

Notable changes:

-   A number of CPU and memory improvements have been made, which should lead to faster initial startup, faster analysis, and lower peak memory usage.
-   A partial stub for scikit-learn has been included, which should fix many classes (such as `MinMaxScalar`).
    ([pylance-release#1139](https://github.com/microsoft/pylance-release/issues/1139))
-   A number of crashes have been fixed.
    ([pylance-release#1072](https://github.com/microsoft/pylance-release/issues/1072))
-   `self`/`cls`, parameters in abstract methods, parameters in `Protocol` definitions, and parameters in function overloads will no longer be marked as "not accessed" and grayed out.
    ([pylance-release#194](https://github.com/microsoft/pylance-release/issues/194))
-   The bundled matplotlib stubs have been updated.
-   Pylance's copy of typeshed has been updated. Stubs that are marked as Python 2 only are no longer included.
-   Interpreter paths are now correctly queried when the selected interpreter is PyPy.
-   Indexing has been re-enabled in the insiders build.

In addition, Pylance's copy of Pyright has been updated from 1.1.130 to 1.1.133, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Enhancement: Implemented first cut at generalized support for dataclass transforms.
-   [1.1.133](https://github.com/microsoft/pyright/releases/tag/1.1.133)
    -   Bug Fix: Fixed bug that resulted in a false positive error within type checker when a constrained TypeVar was used in a lambda callback.
    -   Bug Fix: Fixed bug in type variable constraint solver that resulted in false positive error in certain cases involving bidirectional type inference with unknown (or missing) type arguments.
        ([pylance-release#1168](https://github.com/microsoft/pylance-release/issues/1168))
    -   Enhancement: Reduced memory consumption of tokenizer for string literal tokens.
    -   Enhancement: Improved performance of type analyzer in cases where certain type checking diagnostic rules are disabled.
    -   Enhancement: Improved startup time of pyright by eliminating redundant calls to Python interpreter to retrieve import resolution paths.
    -   Behavior Change: Automatically mark parameters as accessed (so they don't appear as "grayed out") in the following circumstances: 1) it is a self parameter in an instance method, 2) it is a cls parameter in a class method, 3) it is a parameter in a method marked abstract, 4) it is a parameter in a method that is part of a protocol class, 5) it is a parameter in an overload signature.
        ([pylance-release#194](https://github.com/microsoft/pylance-release/issues/194))
    -   Bug Fix: Fixed incompatibility with pypy when retrieving import resolution paths from the configured Python interpreter.
    -   Enhancement: Added diagnostic for `__init__` method that does not have a return type of `None`.
    -   Enhancement: Configuration settings can now be stored in a pyproject.toml file. If both pyproject.toml and pyrightconfig.json are both present, the latter takes precedent.
-   [1.1.132](https://github.com/microsoft/pyright/releases/tag/1.1.132)
    -   Bug Fix: Fixed regression that caused incorrect reporting of "parameter name mismatch" errors for overrides of dundered methods.
-   [1.1.131](https://github.com/microsoft/pyright/releases/tag/1.1.131)
    -   Bug Fix: Changed logic that detects generator functions to accommodate yield statements that are provably unreachable in the code flow.
    -   Behavior Change: Changed dataclass logic to not enforce ordering of fields with defaults vs those without if `init=False` is specified.
    -   Enhancement: Extended method override check to include dundered methods (other than constructors).
    -   Bug Fix (from pylance): Removed duplicate "yield" suggestion in completion list.
    -   Enhancement (from pylance): Improved logic that maps type stubs to corresponding source files.
    -   Enhancement: Added support for implicit `__annotations__` symbol at the module level.
        ([pylance-release#1161](https://github.com/microsoft/pylance-release/issues/1161))
    -   Enhancement: Updated to the latest typeshed stubs. Removed third-party stubs for that were marked as Python 2 only (enum34, fb303, futures, ipaddress, kazoo, openssl-python, pathlib2, pymssql, Routes, scribe, tornado).
    -   Enhancement: Added support for `type(None)` within isinstance type narrowing.
    -   Bug Fix: When providing a completion suggestion for an async method override, an "await" operator is now added in the generated return expression.
    -   Bug Fix: Fixed false positive error in argument/parameter matching logic for function calls that occurs when a keyword argument targets a parameter that can be either positional or keyword and a spread operator is used in an earlier argument.
    -   Bug Fix: Fixed bug that resulted in false positive error when a constrained TypeVar type was passed through the "isinstance" type narrowing logic and then used as an operand in a binary operation.
        ([pylance-release#1165](https://github.com/microsoft/pylance-release/issues/1165))
    -   Bug Fix: Fixed several bugs that caused type checker crash in certain cases.

## 2021.4.1 (14 April 2021)

Notable changes:

-   Source mapping has been greatly improved. Notably, in more recent versions of numpy (1.20+), docstrings and navigation should work for many more symbols.
    ([pylance-release#855](https://github.com/microsoft/pylance-release/issues/855))
-   The `yield` keyword will no longer be duplicated in completions.
    ([pylance-release#1137](https://github.com/microsoft/pylance-release/issues/1137))

In addition, Pylance's copy of Pyright has been updated from 1.1.129 to 1.1.130, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Changed logic that detects generator functions to accommodate yield statements that are provably unreachable in the code flow.
    -   Behavior Change: Changed dataclass logic to not enforce ordering of fields with defaults vs those without if `init=False` is specified.
    -   Enhancement: Extended method override check to include dundered methods (other than constructors).
-   [1.1.130](https://github.com/microsoft/pyright/releases/tag/1.1.130)
    -   Bug Fix: Fixed bug in type narrowing logic when the narrowed expression contained an assignment expression (walrus operator). It was not properly narrowing the target of the assignment expression.
    -   Bug Fix: Fixed bug in "isinstance" type narrowing support when the first argument is a type (e.g. a class or `Type[T]`) and the second argument is `type` (or a tuple that contains `type`).
    -   Bug Fix: Fixed bug in "isinstance" type narrowing logic where it didn't properly handle protocol classes that support runtime checking.
    -   Enhancement (from Pylance): Improved docstring formatting in hover text.
    -   Behavior Change: Suppressed "access to non-required key" diagnostic if the access is performed within a try block.
        ([pylance-release#1145](https://github.com/microsoft/pylance-release/issues/1145))
    -   Bug Fix: Fixed bug in 'callable' type narrowing logic. It wasn't properly handling type variables.
    -   Enhancement: Implemented new diagnostic rule "reportUnnecessaryComparison". It checks for "==" and "!=" comparisons where the LHS and RHS types have no overlap and the LHS has no `__eq__` overload. This new diagnostic rule is off by default in normal type checking mode but is on in strict mode.
    -   Bug Fix: Fixed false positive error that occurred when file started with "from typing import Collection". This was due to mishandling of a cyclical dependency in the typeshed classes.
    -   Enhancement: Improved bidirectional type inference for expressions that involve the pattern `[<list elements>] * <expression>`.
    -   Bug Fix: Fixed false positive error relating to the use of parentheses in "with" statement when using Python 3.9.
        ([pylance-release#999](https://github.com/microsoft/pylance-release/issues/999))
    -   Bug Fix: Fixed bug in type evaluation of async functions that are not generators but have a declared return type of AsyncGenerator. The actual return type needs to be wrapped in a Coroutine in this case.
        ([pylance-release#1140](https://github.com/microsoft/pylance-release/issues/1140))
    -   Bug Fix: Suppressed diagnostic check for `Subscript for class "X" will generate runtime exception` when it's used in a PEP 526-style variable type annotation. Apparently the exception occurs only when used in other contexts like parameter and return type annotations.

## 2021.4.0 (7 April 2021)

Notable changes:

-   `lxml.etree` (and other compiled modules) should no longer be mistakenly marked as unresolved in some cases.
    ([pylance-release#392](https://github.com/microsoft/pylance-release/issues/392))
-   A bug in a performance optimization for `__all__` involving `py.typed` libraries has been fixed. This issue manifested as auto-imports using an unwanted path (e.g. `fastapi.param_functions.Query` instead of `fastapi.Query`).
    ([pylance-release#774](https://github.com/microsoft/pylance-release/issues/774))
-   Signature help in broken code will now more correctly signatures and parameters.
    ([pylance-release#1128](https://github.com/microsoft/pylance-release/issues/1128))
-   A regression in namespace package handling has been fixed.
    ([pylance-release#1132](https://github.com/microsoft/pylance-release/issues/1132))
-   The default setting for indexing in the insiders build has been temporarily changed to `false` as we continue to analyze and improve its performance. It can still be manually enabled with `"python.analysis.indexing": true`.
-   The bundled matplotlib stubs have been updated.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.127 to 1.1.129, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug in type narrowing logic when the narrowed expression contained an assignment expression (walrus operator). It was not properly narrowing the target of the assignment expression.
    -   Bug Fix: Fixed bug in "isinstance" type narrowing support when the first argument is a type (e.g. a class or `Type[T]`) and the second argument is `type` (or a tuple that contains `type`).
    -   Bug Fix: Fixed bug in "isinstance" type narrowing logic where it didn't properly handle protocol classes that support runtime checking.
-   [1.1.129](https://github.com/microsoft/pyright/releases/tag/1.1.129)
    -   Enhancement: Added configuration option "strictSetInference" which is analogous to "strictListInference" and "strictDictionaryInference" but specifically for set expressions.
    -   Enhancement: Tweaked heuristic in constraint solver to prefer types that have no "unknown" element to those that do.
    -   Enhancement: Improved the handling of TypeVar matching when the source and dest types are both unions, the types are being compared with invariant constraints, and the dest contains a TypeVar.
    -   Enhancement: Fixed misleading error message for "unsupported `__all__` operations".
    -   Enhancement: Improved error message for dataclass fields.
    -   Bug Fix: Fixed bug that caused inconsistent type evaluation for type annotations based on order of evaluation. It was triggered in some cases by the semantic highlighting feature.
        ([pylance-release#1121](https://github.com/microsoft/pylance-release/issues/1121))
    -   Bug Fix: Fixed bug in the function type compatibility logic. If the source has a `*args` or `**kwargs` parameter but the dest does not, the function should still be assignable.
    -   Behavior Change: Changed the logic that searches for a config file. It currently searches from the current working directory all the way up the folder hierarchy. This makes sense only for a command-line tool, not for a language server. The latter already knows the project root, and we should look only in that directory for a config file.
    -   Bug Fix: Fixed bug in signature help provider where its heuristics were causing it to return a bad response when the insertion point was immediately after a comma and a call expression preceded the comma.
        ([pylance-release#1128](https://github.com/microsoft/pylance-release/issues/1128))
    -   Bug Fix: Added support for an import edge case where a module's `__init__.py` file is apparently importing from itself but intends instead to import from one of its submodules.
    -   Bug Fix: Fixed bug in namespace import resolution. When there are multiple import search matches, the import resolver needs to take into account the individual symbols specified in the import statement.
        ([pylance-release#1132](https://github.com/microsoft/pylance-release/issues/1132))
    -   Bug Fix: Fixed a bug whereby call expressions within a type annotation were flagged as errors but not evaluated, which meant that symbols referenced within them were not marked as accessed.
    -   Enhancement: Updated typeshed stubs to the latest.
-   [1.1.128](https://github.com/microsoft/pyright/releases/tag/1.1.128)
    -   Bug Fix: Fixed bug in argument-matching code that produced false positive errors when a keyword argument corresponded to a positional-only argument name but should have been matched to a \*\*kwargs parameter instead.
        ([pylance-release#1109](https://github.com/microsoft/pylance-release/issues/1109))
    -   Bug Fix: Fixed bug in bidirectional type inference logic for list and dict expressions when expected type included a type varaible.
    -   Bug Fix: Disabled the "self" annotation checks for overloaded methods because the self annotation can be used as a legitimate filter for overloads.
    -   Enhancement: Improved bidirectional type inference for set expressions so it better handles unions in expected type.
    -   Bug Fix: Improved TypeVar constraint solver so it provides a better solution when a TypeVar is constrained first by a contravariant wide bound in a first argument and then a subsequent argument relies on bidirectional type inference with a covariant or invariant use of the same TypeVar.
    -   Bug Fix: Fixed bug that caused a crash in the type checker when a protocol class inherited from a generic non-protocol class.
    -   Enhancement: Added check for a class that inherits from Generic to ensure that all type variables are included in the Generic subscript list.
    -   Bug Fix: Fixed regression in handling expressions of the form `[x] * y`. Some previously-added special-case code to handle the `[None] * n` case was too general.
    -   Enhancement: Changed printed types to fully expand type aliases in error messages where that additional detail is needed — namely, for "partially unknown" messages. This makes for verbose types, but without the expansion, it can be very difficult to determine which part of the type is unknown.
    -   Bug Fix: Fixed false positive error in type compatibility check where the destination type is `Type[Any]` and the source type is `Type[x]` where x is anything (including `Any`).
    -   Enhancement: Added exemption to the overlapping overload check for the `__get__` method. Other type checkers (namely mypy) exempt this method also.

## 2021.3.4 (31 March 2021)

Notable changes:

-   Broken symlinks in the workspace should no longer cause crashes.
    ([pylance-release#1102](https://github.com/microsoft/pylance-release/issues/1102))
-   Completion performance when IntelliCode is enabled has been improved.
-   The bundled matplotlib stubs have been updated.
-   Method override completions while editing a stub will no longer include `super()` calls, and instead add the correct `...` body.
-   Auto-import completions and quick fixes will now more correctly handle import blocks that have been split onto multiple lines.
    ([pylance-release#1097](https://github.com/microsoft/pylance-release/issues/1097))

In addition, Pylance's copy of Pyright has been updated from 1.1.125 to 1.1.127, including the following changes:

-   [1.1.127](https://github.com/microsoft/pyright/releases/tag/1.1.127)
    -   Bug Fix: Fixed bug in type evaluator that resulted in suppressed errors and evaluations when the evaluation of a lambda expression resulted in some form of recursion (e.g. it references a symbol that depends on the return result of the lambda).
        ([pylance-release#1096](https://github.com/microsoft/pylance-release/issues/1096))
    -   Enhancement: Added "reportTypedDictNotRequiredAccess" diagnostic rule and split out diagnostics that pertain specifically to unguarded accesses to non-required TypedDict keys.
    -   Bug Fix: Changed type of `__path__` variable in module from `List[str]` to `Iterable[str]`.
        ([pylance-release#1098](https://github.com/microsoft/pylance-release/issues/1098))
    -   Bug Fix: Fixed bug that resulted in a runtime crash within the type checker when a protocol class inherits from another protocol class that is not generic (like "Sized").
        ([pylance-release#1101](https://github.com/microsoft/pylance-release/issues/1101))
    -   Enhancement: Added better heuristics to auto-complete insertion logic so it honors single-symbol-per-line and multi-symbol-per-line formats of "from x import a" statements.
        ([pylance-release#1097](https://github.com/microsoft/pylance-release/issues/1097))
    -   Enhancement: Implemented a new check to validate that annotated types for "self" and "cls" parameters are supertypes of their containing classes.
    -   Bug Fix (from pylance): Fixed bug that resulted in crashes when a broken symlink was encountered.
        ([pylance-release#1102](https://github.com/microsoft/pylance-release/issues/1102))
    -   Bug Fix: Fixed recent regression that resulted in false positives when checking the type of a "self" parameter within a metaclass when the type annotation was of the form `Type[T]`.
    -   Enhancement: Added minimal support for "@no_type_check" decorator. It does not suppress errors, but it doesn't generate an error itself.
    -   Enhancement: Added support for PEP 612 ParamSpecs to be used as type parameters for generic classes and generic type aliases. Previously, they were allowed only in the specialization of `Callable`.
    -   Enhancement: Added out-of-bounds access check for index operations where the indexed type is a tuple object with known length and the index value is a negative integer literal value.
    -   Bug Fix: Fixed bugs in the handling of PEP 487 `__init_subclass__`. The logic was using the `__init_subclass__` defined in the class itself rather than its base classes.
    -   Enhancement: Added special-case handling for generic functions that return a `Callable` with generic parameters. The change allows for callers to pass type variables to the function and then have the resulting `Callable` provide a TypeVar scope for those variables.
    -   Bug Fix (from pylance): Fixed bugs relating to partial type stub packages.
-   [1.1.126](https://github.com/microsoft/pyright/releases/tag/1.1.126)
    -   Bug Fix: Fixed bug that affected the use of the `tuple` constructor. It was not properly updating the variadic type arguments. This resulted in false negatives for the resulting type.
        ([pylance-release#1085](https://github.com/microsoft/pylance-release/issues/1085))
    -   Bug Fix: Fixed bug that resulted in false negatives because diagnostics generated while analyzing a constructor call were suppressed.
        ([pylance-release#1087](https://github.com/microsoft/pylance-release/issues/1087), [pylance-release#1088](https://github.com/microsoft/pylance-release/issues/1088), [pylance-release#1104](https://github.com/microsoft/pylance-release/issues/1104))
    -   Enhancement: Improved stub generator to print "x = ..." rather than include the RHS expression if `x` is not a type alias.
    -   Enhancement: Added special-case handling for assignments of the form `x: List[A] = [a] * y` (the multiply operator on a list). This specific idiom is commonly used to initialize a list with None values.
    -   Performance: Added perf improvements that help when dealing with unions that contain many tuples. Improved TypeVar constraint solver to better handle the case where a type is widened to include hundreds of subtypes, thus grinding performance to a halt. This occurs in one of the modules in pytorch.
    -   Enhancement: Rewrote package type verifier based on feedback from users. Its error messages are now much clearer, it distinguishes between "exported symbols" and "other referenced symbols", it properly handles properties, and it omits warnings about missing docstrings by default (can be overridden with "--verbose" setting).
    -   Bug Fix: Fixed bug that resulted in incorrect type evaluation for a constructor call when the class's `__new__` method returns an instance of a different class.
        ([pylance-release#1092](https://github.com/microsoft/pylance-release/issues/1092))

## 2021.3.3 (24 March 2021)

Notable changes:

-   Recursive symlinks in the workspace should no longer cause a hang.
    ([pylance-release#1070](https://github.com/microsoft/pylance-release/issues/1070), [pylance-release#1078](https://github.com/microsoft/pylance-release/issues/1078))
-   An error about a missing "typings" folder will no longer appear at the default log level.
    ([pylance-release#1075](https://github.com/microsoft/pylance-release/issues/1075))
-   pygame stubs are no longer bundled. pygame 2.0 (released October 2020) and above include high-quality types.
    ([pylance-release#758](https://github.com/microsoft/pylance-release/issues/758))

In addition, Pylance's copy of Pyright has been updated from 1.1.122 to 1.1.125, including the following changes:

-   [1.1.125](https://github.com/microsoft/pyright/releases/tag/1.1.125)
    -   Bug Fix: Disabled the "always False comparison" check for expressions like "sys.platform == 'win32'" because they can vary depending on environment.
    -   Enhancement: Added error check for a class that attempts to derive from NamedTuple and other base classes. This is not supported and will generate runtime exceptions.
    -   Enhancement: Improved type checking for generators. Fixed several false negatives and false positives relating to "yield from" expressions.
    -   Enhancement: Changed special-case logic for `self` annotations used with `__init__` methods to accommodate new usages in typeshed stubs.
    -   Enhancement: Updated typeshed stubs to latest.
    -   Bug Fix: Fixed bug in TypeVar constraint solver that resulted in a false positive when using the built-in "filter" method with the "os.path.exists" callback.
    -   Bug Fix: Fixed bug where "comparison chaining" was not being appropriately applied to expressions that contained "is", "is not", "in" and "not in" operators in a chain (e.g. "1" in "1" == "1").
    -   Enhancement: Added smarter handling of empty lists (`[]`) and dicts (`{}`). Previously, these were inferred to have types `list[Unknown]` and `dict[Unknown, Unknown]`, respectively. They are now provided with a known type if the variable is assigned a known list or dict type along another code path.
    -   Bug Fix (from pylance): Made hover text, signature help, and completion suggestions show function docstring using same code.
    -   Bug Fix (from pylance): Fixed issue with partial stub files in cases where a stub file is found but no corresponding source (.py) file is found.
-   [1.1.124](https://github.com/microsoft/pyright/releases/tag/1.1.124)
    -   Bug Fix: Fixed bug where a keyword parameter with a generic type (a TypeVar) and a default value of "..." caused the TypeVar to be assigned a value of "Any".
    -   Bug Fix: Fixed recent regression that caused certain diagnostics to be suppressed when calling a constructor with an expected type.
    -   Enhancement: Added missing check indicated in PEP 589 for TypedDict fields that override a parent class field by the same name with a different type.
    -   Bug Fix: Added support for TypeVar where the bound or constrained types are literals.
    -   Enhancement: Updated typeshed stubs.
    -   Bug Fix: Fixed bug that resulted in false negatives when a generic class was used within a subscript (e.g. within the type argument of another type) and no type arguments were specified for the generic class. This also resulted in such types not properly getting default values. For example, in the expression `Union[int, Callable]`, the `Callable` was not being interpreted as `Callable[..., Unknown]`.
    -   Enhancement: Improved error message for partially-unknown lambda type.
    -   Bug Fix: Fixed a bug in the logic for inferring the type of list expressions when the expected type is "object".
    -   Bug Fix: Improved handling of bidirectional inference for call expressions when the expected type contains a union of literals and the function returns a generic type.
    -   Enhancement: Added new check for a common source of bugs where an equals operator within an if statement compares two values whose literal types do not overlap and will therefore never evaluate to True.
-   [1.1.123](https://github.com/microsoft/pyright/releases/tag/1.1.123)
    -   Bug Fix: Fixed bug in handling of "Final" type annotation with no specified type argument (e.g. "x: Final = 4").
    -   Enhancement: Added support for inferring type of subscripted tuple when subscript is a negative integer literal.
    -   Bug Fix: Fixed recent regression where `super(A, self).x` did not return an unknown type if class `A` had a class in its MRO that had an unknown type.
    -   Bug Fix: Fixed false positive error due to constraint solver's handling of a TypeVar used within a Callable parameter that is matched to a function parameter annotated with another TypeVar.
    -   Enhancement: Improved handling of literals within constraint solver when used with bidirectional type inference.
    -   Bug Fix: Fixed bug that caused false positive error when a generic call expression was used for an argument to an overloaded function and TypeVar matching errors were reported.
        ([pylance-release#1063](https://github.com/microsoft/pylance-release/issues/1063))
    -   Enhancement: Deferred resolution of metaclass during class type resolution to improve compatibility with code generated by mypy-protobuf, which contains cyclical dependencies.
    -   Bug Fix: Fixed bug in declaration provider that caused declaration of class variables to not be resolved correctly when accessed via a `cls` parameter in a class method.
        ([pylance-release#1064](https://github.com/microsoft/pylance-release/issues/1064))
    -   Bug Fix: Fixed bug in symbol resolution when a local class mirrors the name of a class in typing (e.g. `List`) but is not imported from typing and is used in a context where it is forward declared without quotes.
    -   Bug Fix (from pylance): Avoid recursing infinitely when searching for source files when there is a cyclical symlink present.
    -   Bug Fix: Fixed type inference for "yield" expressions. The previous code was using the same logic for "yield" and "yield from".
    -   Enhancement: Added check to determine if type variables in generic protocols use the appropriate variance.
    -   Performance Improvement: Limited "implied else type narrowing" to expressions that have declared types. It's too expensive to infer types.

## 2021.3.2 (17 March 2021)

Notable changes:

-   Completions for class property overrides are now supported.
    ([pylance-release#1054](https://github.com/microsoft/pylance-release/issues/1054))
-   Editable installs are now supported.
    ([pylance-release#78](https://github.com/microsoft/pylance-release/issues/78))
-   Module members appearing in `__all__` are now always suggested in auto-imports, regardless of their name.
    ([pylance-release#703](https://github.com/microsoft/pylance-release/issues/703))
-   Completions offered within stub files will now correctly show symbols available in the current file, rather than only the stub's "externally visible" symbols.
    ([pylance-release#685](https://github.com/microsoft/pylance-release/issues/685))
-   A bug in symlink support (introduced in the previous release) has been fixed. Some code paths were not correctly handling symlinked directories.
    ([pylance-release#1031](https://github.com/microsoft/pylance-release/issues/1031))
-   Imports of the form `from . import X` now work correctly in non-`__init__.py` files.
    ([pylance-release#1050](https://github.com/microsoft/pylance-release/issues/1050))
-   Analysis performance has been improved some code patterns with many inferred variables and deeply nested loops.
    ([pylance-release#1049](https://github.com/microsoft/pylance-release/issues/1049))
-   Python 3.10 `match` support has been updated to support unparenthesized pattern subject lists.
    ([pylance-release#1044](https://github.com/microsoft/pylance-release/issues/1044))
-   Type aliases can now be defined within the class scope.
    ([pylance-release#1043](https://github.com/microsoft/pylance-release/issues/1043))
-   The bundled Django, matplotlib, and pandas stubs have been updated to fix several bugs and missing members.
    ([pylance-release#780](https://github.com/microsoft/pylance-release/issues/780), [pylance-release#792](https://github.com/microsoft/pylance-release/issues/792), [pylance-release#850](https://github.com/microsoft/pylance-release/issues/850), [pylance-release#1037](https://github.com/microsoft/pylance-release/issues/1037))
-   When indexing is enabled (`"python.analysis.indexing": true`), auto-import quick fixes will now include results from user code. This was disabled in the previous release; completions from indexed user code are still not offered.
    ([pylance-release#1055](https://github.com/microsoft/pylance-release/issues/1055))
-   Pylance no longer needs to copy files at startup for cross-platform support, which should improve startup time.
-   The hover tooltip now separates the type from the docstring with a horizontal line, matching the completion tooltip.
-   Stubs for `scipy`'s compiled modules are now included, which should improve performance and completion quality.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.120 to 1.1.122, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug in handling of "Final" type annotation with no specified type argument (e.g. "x: Final = 4").
    -   Enhancement: Added support for inferring type of subscripted tuple when subscript is a negative integer literal.
    -   Bug Fix: Fixed recent regression where `super(A, self).x` did not return an unknown type if class `A` had a class in its MRO that had an unknown type.
    -   Bug Fix: Allow lowercase `tuple` type to be subscripted in versions of Python prior to 3.9 if it is within a quoted annotation.
        ([pylance-release#1056](https://github.com/microsoft/pylance-release/issues/1056))
-   [1.1.122](https://github.com/microsoft/pyright/releases/tag/1.1.122)
    -   Bug Fix: Fixed false positive error in constructor method with an input parameter annotated with a class-scoped TypeVar and with a default value.
    -   Enhancement: Improved performance of type analysis for certain code patterns that involve inferred types of variables that are used in deeply nested loops and chains of updates. In one such example, this change reduced the analysis time from ~17000ms to ~200ms.
    -   Bug Fix: Fixed bug in the handling of the `owner` parameter for the `__get__` method in a descriptor class. The type evaluator was using an `Any` type rather than the proper class type in this case.
    -   Bug Fix: Updated TypeVar constraint solver so it tracks a "narrow bound" and "wide bound" for each TypeVar as they are being solved. This fixes several subtle bugs.
    -   Enhancement: Updated typeshed stubs to the latest.
    -   Behavior Change: Added new top-level "extraPaths" config option for pythonconfig.json that specifies the default extraPaths to use when no execution environments apply to a file. Changed settings logic to use the new default extraPaths mechanism for the "python.analysis.extraPaths" setting.
        ([pylance-release#1053](https://github.com/microsoft/pylance-release/issues/1053))
    -   Bug Fix: Fixed bug related to the handling of `from . import X` statement located in a file other than `__init__.py`. When used outside of an `__init__.py` file, this import looks for the `__init__.py` and imports the requested symbol `X` from it rather than looking for a submodule `X`.
        ([pylance-release#1050](https://github.com/microsoft/pylance-release/issues/1050))
    -   Enhancement: Improved completion provider's handling of method overrides so it properly handles properties.
        ([pylance-release#1054](https://github.com/microsoft/pylance-release/issues/1054))
    -   Enhancement (from pylance): Add lowercased items from `__all__` in auto-imports.
    -   Bug Fix: Fixed bug in constraint solver that occurs when a constrained TypeVar is used in conjunction with a protocol that has a contravariant TypeVar.
-   [1.1.121](https://github.com/microsoft/pyright/releases/tag/1.1.121)
    -   Bug Fix: Fixed a bug that generated a false positive error when a function (or other callable) was assigned to a Hashable protocol.
    -   Enhancement (from pylance): Made auto-imports lazy for better completion suggestion performance.
    -   Enhancement (from pylance): Improved readability of hover text for functions and methods with overloaded signatures.
    -   Bug Fix: Fixed false positive error when using an instance or class variable defined within a Protocol class within a method in that same class. The previous logic was based on a misinterpretation of a sentence in PEP 544.
    -   Bug Fix: Fixed false positive error in type checker when dealing with two types that are both unions and both contain constrained type variables.
    -   Bug Fix: Fixed improper handling of symlinks used in editable installs. This affected auto-import functionality.
    -   Bug Fix: Fixed recent regression that caused crash in hover provider.
    -   Bug Fix (from pylance): Fixed issue that caused editable installs to require a restart of the language server before their effects were visible.
    -   Bug Fix: Fixed false positive error during TypeVar constraint solving in the case where the same TypeVar is used in both the form T and `Type[T]` in the same signature.
    -   Enhancement: Improved support for enums. The Python spec indicates that attributes that start and end with an underscore are not treated as enum members, nor are attributes that are assigned a descriptor object.
    -   Enhancement: Added support for inferring the "value" and "name" fields of an enum.
    -   Bug Fix: Added support for unparenthesized pattern subject lists in match statement.
        ([pylance-release#1044](https://github.com/microsoft/pylance-release/issues/1044))
    -   Bug Fix: Fixed false positive error related to a type alias declared within a class.
        ([pylance-release#1043](https://github.com/microsoft/pylance-release/issues/1043))

## 2021.3.1 (10 March 2021)

Notable changes:

-   Import resolution performance has been improved, which significantly reduces overall analysis times (30% in some projects).
-   Hover tooltips for overloaded functions will now place each overload on its own line. This matches the existing completion tooltip. Additionally, signatures which may appear too wide in a tooltip are now separated by extra newlines to visually distinguish them.
    ([pylance-release#612](https://github.com/microsoft/pylance-release/issues/612))
-   `if`/`elif` chains without `else` clauses can now completely narrow variables. For example, it's possible to verify that an enum value has been exhaustively checked against all possible values without a "default" case. This feature is only active in annotated functions.
-   Symlinks are now generally supported.
    ([pylance-release#131](https://github.com/microsoft/pylance-release/issues/131))
-   Angle brackets in docstring inline code blocks are no longer incorrectly escaped.
    ([pylance-release#816](https://github.com/microsoft/pylance-release/issues/816))
-   PEP 464 support (variadic generics) has been updated to match the current state of the PEP. This PEP is not yet accepted, but is targeting Python 3.10.
-   TypedDict support has been updated to allow for narrowing dict members. For example, checking `if "a" in d` will now recognize `d["a"]` as a safe operation.
-   When indexing is enabled (`"python.analysis.indexing": true`), auto-import completions will no longer include indexer results from user code (as this negatively impacted performance); only auto-imports in code referenced from currently open files will be offered. We are looking for feedback about the indexing feature; please file an issue if you have enabled indexing and this affects your workflow.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.117 to 1.1.120, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed a bug that generated a false positive error when a function (or other callable) was assigned to a Hashable protocol.
        ([pylance-release#1027](https://github.com/microsoft/pylance-release/issues/1027))
-   [1.1.120](https://github.com/microsoft/pyright/releases/tag/1.1.120)
    -   Bug Fix: Fixed type evaluation bug that resulted in the incorrect inference of an exception type within an "except X as Y" clause when the expression X was a bound TypeVar.
    -   Enhancement: Improved detection and error reporting for class definitions that depend on themselves (illegal cyclical dependency). Previously, pyright failed in ways that were difficult to diagnose.
    -   Enhancement: Added support for symbolic links in import resolver both for resolution of ".pth" files and for imports themselves.
    -   Behavior Change: Removed support for "venv" entry in execution environments since this never really worked. Clarified in documentation that import resolution within an execution environment is not transitive.
    -   Bug Fix: Fixed bug in completion provider that caused class variables not be included as suggestions as members for the "cls" parameter in a class method.
        ([pylance-release#1026](https://github.com/microsoft/pylance-release/issues/1026))
    -   Enhancement: Added error check for access to non-required fields in a TypedDict using a subscript with a literal string field name. Added support for "narrowing" of a TypedDict class based on guard expression of the form "S in D" where S is a string literal name of a non-required field. Improved the synthesized "get" method on a TypedDict for non-required fields; it now returns an `Optional[T]` (where T is the defined type for that field) rather than just T.
    -   Enhancement: Updated to the latest typeshed stubs.
    -   Enhancement: Added error check for a "yield" or "yield from" statement used within a list comprehension. This generates a runtime syntax error.
-   [1.1.119](https://github.com/microsoft/pyright/releases/tag/1.1.119)
    -   Bug Fix: Fixed bug in type evaluator that caused some diagnostics to be suppressed unintentionally and in a non-deterministic manner (based on the order in which types were evaluated).
    -   Enhancement: Added a heuristic to disable the "implied else" analysis if the code is within a function that has no input parameter annotations. This mitigates the performance overhead of "implied else narrowing".
    -   Enhancement: When a function decorator is applied and the decorator returns a function that has no docstring, copy the docstring from the decorated function.
    -   Enhancement: Changed inference logic for constructors to allow synthesized type for `cls` to retain its generic form when instantiated, so the expression `cls()` will remain generic.
    -   Bug Fix: Fixed false positive "metaclass conflict" error that occurs when the metaclass has an unknown class type in its class hierarchy.
    -   Bug Fix: Fixed bug in type evaluator when dealing with a bound TypeVar. The constraint solver wasn't properly handling the `Type[T]` statement in all cases.
    -   Bug Fix: Fixed recent regression in CLI where partial stub packages were not applied correctly.
    -   Enhancement: Eliminate duplicate python search paths, eliminating the need to search the same path more than once on every import resolution.
    -   Bug Fix: Fixed crash in logic that handles partial type stub merging. The crash occurs when a search path points to a file (e.g. a zip file) rather than a directory.
        ([pylance-release#1021](https://github.com/microsoft/pylance-release/issues/1021))
    -   Enhancement: Added support in PEP 646 when the unpacked TypeVarTuple is not at the end of the type parameter list. This allows for suffixing when matching type arguments against type parameters and when matching TypeVarTuple parameters in a Callable.
    -   Enhancement: Added better error reporting for reveal_type and reveal_locals calls.
    -   Enhancement: Added file system caching to import resolver for performance reasons.
    -   Bug Fix: Fixed bug in type-printing logic for tuples. When typeCheckingMode is "off", type arguments are supposed to be displayed if they are not all "Any" or "Unknown", but they were omitted always.
    -   Bug Fix: Fixed bug that caused type evaluation behavior that depends on (including, possibly, false positive errors) when evaluating subexpressions within a case statement.
    -   Enhancement (from Pylance): Fix HTML escaping in code blocks.
        ([pylance-release#816](https://github.com/microsoft/pylance-release/issues/816))
    -   Behavior Change: Exempt ParamSpec from "single use of TypeVar within function signature" check.
    -   Enhancement: Improved error reporting for ParamSpec misuse.
-   [1.1.118](https://github.com/microsoft/pyright/releases/tag/1.1.118)
    -   Bug Fix: Fixed bug in logic that verifies exception type in "raise" statement. It was not properly handling generic types that were bound to BaseException.
    -   New Feature: Add --ignoreexternal CLI flag for use with --verifytypes feature. (Contribution by Vlad Emelianov)
    -   Enhancement: The --verifytypes output now includes file paths in the report. (Contribution by Vlad Emelianov)
    -   Bug FIx: Fixed crash that occurred when a function was declared within a local scope but when the function's symbol was previous declared "global" or "nonlocal" within that scope.
    -   Enhancement (from Pylance): Method and class docstrings now inherit from parent classes if docstrings are missing in child class.
    -   Enhancement (from Pylance): Improved support for partial stubs (where py.typed file includes "partial" as per PEP 561).
    -   Bug Fix: Fixed bug that caused incorrect type evaluation for member access expressions when the member was a descriptor object and the base type was a variable containing a reference to the class.
    -   Bug Fix: Fixed bug in document symbol provider that caused incorrect range to be returned for classes and functions.
        ([pylance-release#1010](https://github.com/microsoft/pylance-release/issues/1010))
    -   Enhancement: Improved tracking of incomplete types (those that have not yet been fully established because of recursive type dependencies within the code flow graph).
    -   New Feature: Added logic for if/elif chains that contain no else clause but completely narrow one or more variables.
    -   Behavior Change: Changed behavior of TypeVar constraint solver to eliminate literal types (widening them to their associated type) when solving for TypeVars, unless a literal type was explicitly provided (e.g. using explicit specialization like `List[Literal[1, 2, 3]]`).
    -   Behavior Change: Changed reportOverlappingOverload to be an error in strict mode.
    -   Bug Fix: Fixed bug in logic that determines whether one callable type can be assigned to another. It wasn't taking into account the positional-only parameter separator (`/`).
        ([pylance-release#1017](https://github.com/microsoft/pylance-release/issues/1017))
    -   Bug Fix: Fixed a bug in conditional type narrowing that narrows based on descriminated member variable types. It was being over aggressive in narrowing in the negative ("else") case when the type of the member was a union of literal types.
    -   Bug Fix: Fixed false positive error that occurred when setting or deleting the member of an object where that member's type is defined by a parent class and is generic but is specialized by a child class.

## 2021.3.0 (3 March 2021)

Notable changes:

-   Method docstrings are now inherited from parent classes.
    ([pylance-release#550](https://github.com/microsoft/pylance-release/issues/550), [pylance-release#877](https://github.com/microsoft/pylance-release/issues/877))
-   The matplotlib and PIL stubs have been updated to be more complete and correct.
    ([pylance-release#73](https://github.com/microsoft/pylance-release/issues/73), [pylance-release#420](https://github.com/microsoft/pylance-release/issues/420), [pylance-release#462](https://github.com/microsoft/pylance-release/issues/462), [pylance-release#716](https://github.com/microsoft/pylance-release/issues/716), [pylance-release#994](https://github.com/microsoft/pylance-release/issues/994))
-   Parentheses in `with` statements will no longer be flagged as invalid.
    ([pylance-release#999](https://github.com/microsoft/pylance-release/issues/999))
-   A case where the same auto-import may be suggested more than once has been fixed.
-   Files ending in `.git` will now be ignored in file watcher events. These files are created by some tools and cause reanalysis on change.
-   Partial stub packages (defined in PEP 561) are now supported.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.114 to 1.1.117, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed crash that occurred when a function was declared within a local scope but when the function's symbol was previous declared "global" or "nonlocal" within that scope.
    -   Bug Fix: Fixed bug in logic that verifies exception type in "raise" statement. It was not properly handling generic types that were bound to BaseException.
        ([pylance-release#1003](https://github.com/microsoft/pylance-release/issues/1003))
-   [1.1.117](https://github.com/microsoft/pyright/releases/tag/1.1.117)
    -   Enhancement: Extended check that detects redeclared functions and methods to also report redeclared properties within a class.
    -   Bug Fix: Fixed crash in parser that occurs when malformed index expression is parsed.
    -   Enhancement: Improved error message for certain type incompatibilities.
    -   Bug Fix: Fixed bug in logic that determines whether a function type is assignable to another function type. It was not properly handling the case where the destination had a \*\*kwargs parameter and the source had an unmatched keyword parameter.
    -   Enhancement: Added new check to ensure that the type signature of a function with overloads is the superset of all of its overload signatures.
    -   Enhancement: Improved consistency of error messages by standardizing on "incompatible" rather than "not compatible".
    -   Bug Fix: Fixed bug in handling of `type(x)` call that resulted in false positive errors.
    -   Behavior Change: Changed the logic that determines whether a variable assignment is an implicit type alias definition. If there is an explicit type annotation (other than the use of the PEP 612 TypeAlias), it is no longer considered a type alias. This is consistent with the rules mypy uses.
    -   Bug Fix: Fixed a bug in the logic for inferring "cls" parameter that resulted in incorrect type evaluations.
    -   Enhancement: Added check to detect inappropriate use of variables (that are not type aliases) within type annotations.
    -   Bug Fix: Fixed bug in type compatibility logic that permitted a type of `Type[Any]` to be assigned to type `None`.
    -   New Feature: Implemented support for PEP 655: Marking individual TypedDict items as required or potentially-missing. This PEP is still under development, so the spec could change.
-   [1.1.116](https://github.com/microsoft/pyright/releases/tag/1.1.116)
    -   Enhancement: Improved type inference logic for tuple expressions that contain unpacked tuples.
        ([pylance-release#991](https://github.com/microsoft/pylance-release/issues/991))
    -   Bug Fix: Fixed bug that resulted in unknown types within stubs when a forward reference was made within a type alias definition.
    -   Bug Fix: Fixed bug in bidirectional type inference logic for unpack operator.
    -   Bug Fix: Fixed bug in assignment type narrowing for index expressions. The narrowed type was always evaluated as "None" rather than the assigned type.
        ([pylance-release#992](https://github.com/microsoft/pylance-release/issues/992))
    -   Bug Fix: Fixed bug in assignment type narrowing that was triggered when the RHS and LHS were both union types and the RHS contained an `Any`.
        ([pylance-release#993](https://github.com/microsoft/pylance-release/issues/993))
    -   Enhancement: Added diagnostic check for a call expression that appears within a type annotation. This was previously not flagged as an error.
    -   Bug Fix: Fixed false negative bug in the "reportOverlappingOverload" diagnostic check. It was not correctly detecting overlapping overloads when one of the parameters in the earlier overload was annotated with at TypeVar.
    -   Bug Fix: Fixed bug in logic that compares the type compatibility of two functions. In particular, if the source function contains a keyword argument and the dest function does not contain a keyword argument of the same name bug contains a \*\*kwargs, the types must match.
    -   Enhancement: Added support for overloaded `__init__` method that annotates the `self` parameter with a generic version of the class being constructed.
    -   Behavior Change: Added a few exemptions for the reportInvalidTypeVarUse check. In particular, constrained TypeVars, bound TypeVars used as type arguments, and any TypeVar used as a type argument to a generic type alias are exempt from this check. There are legitimate uses for all of these cases.
    -   Bug Fix: Fixed recent regression in type assignment check logic that broke certain cases where the destination and source were both unions that contained type variables.
    -   Behavior Change: Changed behavior when evaluating type of symbol within type stubs. Previously forward references were allowed only for class types. Now, forward references are allowed (and no code flow analysis is employed) for all symbols. The new behavior is consistent with mypy's.
    -   Enhancement: Added new diagnostic check for an overloaded function without an implementation within a source (.py) file. Fixed a bug in the diagnostic check for a single overload when an implementation is present.
    -   Bug Fix: Fixed bug in the parsing of "with" statements where the "with item" starts with an open parenthesis.
    -   Enhancement: Added "collections.defaultdict" to the list of classes that does not support runtime subscripting in versions of Python prior to 3.9.
        ([pylance-release#1001](https://github.com/microsoft/pylance-release/issues/1001))
    -   Behavior Change: Changed behavior of type inference for empty list (`[]`) and empty dict (`{}`) expressions. They were previously inferred to be `List[Any]` and `Dict[Any, Any]`, but they are now inferred as `List[Unknown]` and `Dict[Unknown, Unknown]`. This affects strict mode type checking, where partially-unknown types are reported as errors. This change may require some explicit type annotations within strictly-typed code.
-   [1.1.115](https://github.com/microsoft/pyright/releases/tag/1.1.115)
    -   Bug Fix: Fixed false positive bug where "class not runtime subscriptable" error was reported even if in a type stub.
    -   New Feature: Implemented command-line switches for pythonplatform and pythonversion. These are overridden by pyrightconfig.json settings.
    -   New Feature: Added support for comments and trailing comments within pyrightconfig.json.
    -   Enhancement: Updated to latest typeshed stubs.
    -   Enhancement (from Pylance): Improve auto-import performance.
    -   Enhancement (from Pylance): Added extra perf tracking.
    -   Bug Fix: Fixed false positive error that incorrectly complained about the use of `Annotated` as a class with no type arguments.
    -   Bug Fix: Fixed false positive error when using bidirectional inference of dictionary expression where the expected type key and/or value types contain literals.
    -   Bug Fix: Fixed bug that resulted in wildcard imports (i.e. imports the form `from x import *`) to import symbols from the target that were not meant to be externally visible. This bug occurred only when the imported module had no `__all__` symbol defined.
    -   Bug Fix: Fixed bug in validation of constrained types in TypeVars. Subtypes of constrained types should be allowed.

## 2021.2.4 (24 February 2021)

Notable changes:

-   The mapping of stub files to source files has been greatly improved. Go-to-definition and doc strings should now work for a much wider range of code.
    ([pylance-release#809](https://github.com/microsoft/pylance-release/issues/809), [pylance-release#949](https://github.com/microsoft/pylance-release/issues/949))
-   Index expression type narrowing is now supported. For example, a check like `if some_tuple[1] is not None` will cause future uses of `some_tuple[1]` to not be `None`, without needing to narrow a temporary variable.
-   Auto-import completion performance has been improved.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.112 to 1.1.114, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed false positive bug where "class not runtime subscriptable" error was reported even if in a type stub.
    -   Enhancement: Implemented command-line switches for pythonplatform and pythonversion. These are overridden by pyrightconfig.json settings.
    -   Enhancement: Added support for comments and trailing comments within pyrightconfig.
    -   Enhancement: Updated to latest typeshed stubs.
    -   Bug Fix: Fixed false positive error that incorrectly complained about the use of `Annotated` as a class with no type arguments.
    -   Bug Fix: Fixed false positive error when using bidirectional inference of dictionary expression where the expected type key and/or value types contain literals.
-   [1.1.114](https://github.com/microsoft/pyright/releases/tag/1.1.114)
    -   Enhancement: Improve source mapper (the code that maps symbols found in stub files to the corresponding code in ".py" files) to handle more cases.
    -   Enhancement: Added diagnostic error for try statement that has no except or finally statement.
    -   New Feature: Added "reportOverlappingOverload" diagnostic rule, splitting out a few checks that were previously in the "reportGeneralTypeIssue" rule. This allows for finer-grained control over these overload checks.
    -   Behavior Change: Added a few additional names that can be used for "cls" parameter without triggering diagnostic. These variants are reasonable and are used within some typeshed stubs.
    -   Enhancement: Added TypeVarTuple definition to typings.pyi stub.
    -   Enhancement: Updated TypeVarTuple logic to detect and report an error when a tuple of unknown length is bound to an unpacked TypeVarTuple. This is illegal according to the latest version of PEP 646.
    -   Enhancement: Special-cased the `__init_subclass__` method in the completion provider so it is offered as a suggestion even though there is no @classmethod decorator present. This symbol is unfortunately inconsistent from all other class methods in that it doesn't require a @classmethod decorator for some reason.
        ([pylance-release#972](https://github.com/microsoft/pylance-release/issues/972))
    -   Behavior Change: Changed logic for attributes marked `ClassVar` to allow writes from an instance of the class as long as the type of the attribute is a descriptor object.
    -   Bug Fix: Fixed a hole in type comparison logic for TypeVars that could have theoretically resulted in incorrect aliasing of types.
    -   Bug Fix: Fixed bug that caused false positive when import statement targeted a symbol that had a nonlocal or global name binding.
        ([pylance-release#977](https://github.com/microsoft/pylance-release/issues/977))
    -   Behavior Change: Enhanced method override compatibility logic to allow instance and class methods to pass generic bound types for `self` and `cls`.
    -   New Feature: Added support for ".pth" files (often used for editable installs) when using the "venv" configuration option in pythonconfig.json.
    -   Bug Fix: Fixed bug whereby import symbol “A” in the statement “from . import A” was not considered a public symbol in a py.typed source file, but it should be.
    -   Enhancement: Improved handling of enum classes. If such a class is defined in a ".py" file, variables defined in the class with type annotations but no assignment are now considered instance variables within each enum instance, whereas variables assigned within the enum class are assumed to be members of the enumeration. This is consistent with the way the EnumMeta metaclass works. In stub files, type annotations without assignments are still assumed to be members of the enumeration, since that's the convention used in typeshed and other stubs.
    -   Enhancement: Added check for parameter names when comparing functions. Parameter names that do not begin with an underscore must match in name. This also affects method override checks and protocol matching checks.
    -   Bug Fix: Fix potential infinite recursion in source mapping, crash in doc strings
-   [1.1.113](https://github.com/microsoft/pyright/releases/tag/1.1.113)
    -   Bug Fixes: Improved support for PEP 634 (Structured Pattern Matching):
        -   Improved negative-case type narrowing for capture patterns. Because capture patterns capture anything, the remaining type is "Never".
        -   Improved type narrowing for mapping patterns used in structural pattern matching when the subject expression type contains a typed dictionary.
        -   Added code to detect and report cases where irrefutable patterns are used within an "or" pattern and are not the last entry.
        -   Added logic to verify that all "or" subpatterns target the same names as specified in PEP 634.
        -   Added code to detect the case where a case statement without a guard expression uses an irrefutable pattern but is not the final case statement. This is disallowed according to PEP 634.
        -   Fixed bug in parser that resulted in incorrect text ranges for parenthetical patterns.
    -   Bug Fix: Improved performance for completion suggestions, especially when large numbers of suggestions are returned.
    -   Enhancement: Updated typeshed stubs to the latest.
    -   Enhancement: Enabled postponed type annotation evaluation by default for Python 3.10.
    -   Bug Fix: Fixed bug that caused a false positive when a bound TypeVar was used to access a class method that was annotated with a bound TypeVar for the "cls" parameter.
    -   Bug Fix: Fixed bug that caused index expressions to be printed incorrectly when they appeared in error messages.
    -   Enhancement: Added type narrowing support for index expressions that use a numeric (integral) literal subscript value.
    -   Enhancement: Improved the logic that determines whether a call expression within the code flow graph is a "NoReturn" call. It now provides better handling of unions when evaluating the call type.
        ([pylance-release#967](https://github.com/microsoft/pylance-release/issues/967))
    -   Enhancement: Added support for parenthesized list of context managers in "with" statement for Python 3.10.
    -   Bug Fix: Fixed bug that prevented the use of a generic type alias defined using a PEP 593-style "Annotated" with a bare TypeVar.

## 2021.2.3 (17 February 2021)

Notable changes:

-   PEP 634 ("match") is now supported, including parser and type checking support. This feature will be available in Python 3.10.
-   Completion performance has been improved when the completion list contains a large number of items, which is common when indexing is enabled (`"python.analysis.indexing": true`) and many auto-imports are suggested.
-   Indexing has been re-enabled in the insiders build.
-   The bundled Django stubs have been updated to their latest version.

In addition, Pylance's copy of Pyright has been updated from 1.1.109 to 1.1.112, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Enhancement: Improved type narrowing for mapping patterns used in structural pattern matching when the subject expression type contains a typed dictionary.
    -   Enhancement: Improved negative-case type narrowing for capture patterns. Because capture patterns capture anything, the remaining type is "Never"
-   [1.1.112](https://github.com/microsoft/pyright/releases/tag/1.1.112)
    -   Bug Fix: Fixed false negative when PEP 585 type is used in a type alias or other cases where postponed evaluation is not possible.
        ([pylance-release#953](https://github.com/microsoft/pylance-release/issues/953))
    -   Bug Fix: Fixed regression that resulted in error when "match" is used in expressions but is mistaken for a pattern-matching statement.
    -   Bug Fix: Fixed schema for "python.analysis.logLevel" setting. The default value was specified incorrectly. Thanks to Rafał Chłodnicki for this fix.
    -   Bug Fix: Fixed a bug that caused a false positive when a TypeVar is bound to a generic protocol class.
    -   Bug Fix: Fixed a bug that caused a false positive when a boolean operator was applied to a type variable and the corresponding magic method used an explicit type annotation for the "self" parameter.
    -   Enhancement: Added a new diagnostic check for out-of-range indexes for tuples that have known lengths.
    -   Enhancement: Added limited support for negative type narrowing in pattern matching. For example, if the type of the subject expression is bool and the matching pattern is `False | x`, the type of `x` will be inferred to be `True`.
    -   Bug Fix: Fixed bug that affected generic type aliases that contained Callable types that are parameterized by a type variable.
    -   Enhancement: Extended abstract method checks to Protocol classes even though they don't explicitly derive from ABCMeta.
    -   Bug Fix: Fixed bug in type narrowing for class patterns in "case" statements.
-   [1.1.111](https://github.com/microsoft/pyright/releases/tag/1.1.111)
    -   New Feature: Implemented PEP 634 support for structural pattern matching. This new PEP was just accepted, and the functionality will appear in the next alpha release of Python 3.10.
    -   Bug Fix: Fixed bug that caused a false positive error when declaring a class within a local scope when the symbol is nonlocal or global.
        ([pylance-release#950](https://github.com/microsoft/pylance-release/issues/950))
    -   Enhancement: Improved handling of unpacked arguments when the type is a union of known-length tuples.
-   [1.1.110](https://github.com/microsoft/pyright/releases/tag/1.1.110)
    -   Bug Fix: Fixed a bug in isinstance type narrowing logic where the type of the second argument to isinstance is type `Type[T]` and the first argument is a union of types that includes type `T`.
    -   Enhancement: Expanded reportUnusedCallResult diagnostic check to also check for expressions of the form `await <call expression>`.
    -   Bug Fix (from Pylance): Changed language server to set the working directory before attempting to execute script to retrieve sys.paths.
    -   Behavior Change (from Pylance): Separated behavior of "go to definition" and "got to declaration". The former tries to take you to the source, whereas the latter takes you to the stub file.
    -   Bug Fix: Changed binding logic to not assume that an assignment to a simple name can generate an exception. This fixes a reported false positive error in a type narrowing case.
    -   Enhancement: Added proper error check for the use of an unpack operator (\*) when used outside of a tuple.
    -   Bug Fix: Avoid generating a diagnostic for reporUnknownMemberType if the member access expression is used as a call argument and is a generic class that is missing type arguments. This case was already special-cased for reportUnknownArgumentType to handle common cases like `isinstance(x, list)`, but it was resulting in errors for `isinstance(x, re.Pattern)`.
    -   Bug Fix: Fixed a hole in the detection of unspecified type arguments for the Tuple and tuple classes.
    -   Enhancement: Added support for generic classes that are parameterized by ParamSpecs, as allowed in PEP 612.

## 2021.2.2 (11 February 2021)

This is a hotfix release, reverting a change in 2021.2.1 which was intended to fix file watching for non-workspace folders, but instead led to "too many files open" messages on macOS.
([pylance-release#936](https://github.com/microsoft/pylance-release/issues/936))

## 2021.2.1 (10 February 2021)

Notable changes:

-   Go-to-definition now brings you to source files (e.g. `.py` files), and a new "go-to-declaration" option brings you to stub files (`.pyi`). If either would otherwise return no result, Pylance will bring you to whichever files are available.
    ([pylance-release#65](https://github.com/microsoft/pylance-release/issues/65))
-   Pylance now correctly handles file change events outside of the workspace, triggering reanalysis on actions such as `pip install`. Environments stored in the workspace were not affected by this bug.
    ([pylance-release#923](https://github.com/microsoft/pylance-release/issues/923))
-   Some potentially nondeterministic behavior in `NoReturn` inference has been fixed, which could potentially lead to code being greyed out as unreachable.
    ([pylance-release#248](https://github.com/microsoft/pylance-release/issues/248))
-   A bug that could lead to execution of `json.py` in the workspace root and invalid entries in `sys.path` has been fixed. Thanks to [David Dworken](https://daviddworken.com) for reporting this issue.
-   The bundled Django and SQLAlchemy stubs have been updated to their latest versions.

In addition, Pylance's copy of Pyright has been updated from 1.1.108 to 1.1.109, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Behavior Change: Expanded reportUnusedCallResult diagnostic check to also check for expressions of the form `await <call expression>`.
    -   Bug Fix: Fixed a bug in isinstance type narrowing logic where the type of the second argument to isinstance is type `Type[T]` and the first argument is a union of types that includes type `T`.
-   [1.1.109](https://github.com/microsoft/pyright/releases/tag/1.1.109)
    -   Enhancement: Added some performance optimizations to handle cases where there are many overloads for a function (>100). Previous code hit n^2 analysis times where n is number of overloads.
    -   Enhancement: Added perf optimization that avoids reallocation of special form classes (like Protocol and Literal) every time they're used. Since instance of the type is now cached and reused.
    -   Enhancement (from Pylance): Improved formatting of docstrings in hover text, completion suggestions, and signature help.
    -   Enhancement (from Pylance): Added better performance metrics.
    -   Bug Fix (from Pylance): Improved logic to ignore temp files created by code formatters like black.
    -   Bug Fix: Fixed "possibly unbound" false positive error in try/except/else/finally statement in the special case where a "bare except" clause is used.
        ([pylance-release#913](https://github.com/microsoft/pylance-release/issues/913))
    -   Bug Fix: Replaced logic that detects whether a function's inferred type is "NoReturn" — and specifically whether its implementation is a "raise NotImplementedError". The old logic depended results that varied depending on the order in which types were evaluated and was therefore nondeterministic.
        ([pylance-release#248](https://github.com/microsoft/pylance-release/issues/248))
    -   Bug Fix: Fixed false negative where type expressions used as arguments to TypedDict or NamedTuple constructors are not correctly checked for incompatibility with older versions of Python when they contain `|` or use PEP 585 types.
        ([pylance-release#918](https://github.com/microsoft/pylance-release/issues/918))
    -   Behavior Change: Changed PEP 585 violations (e.g. using `list[int]` rather than `List[int]`) to be unconditional errors rather than diagnostics controlled by reportGeneralTypeIssues diagnostic rule. That way, they appear even when type checking is disabled.
        ([pylance-release#916](https://github.com/microsoft/pylance-release/issues/916), [pylance-release#917](https://github.com/microsoft/pylance-release/issues/917))
    -   Bug Fix: Reverted recent change in for/else statement logic because it introduced a regression.
    -   Behavior Change: Changed the `reportUnboundVariable` default severity from "warning" to "none" when typeCheckingMode is "off". There were too many complaints of false positives from users who have no interest in type checking.
        ([pylance-release#919](https://github.com/microsoft/pylance-release/issues/919))
    -   Enhancement: When a redundant form of a from .. import statement is used (e.g. `from x import foo as foo`), always mark the imported symbol as accessed because it is assumed that it is being re-exported.
    -   Bug Fix: Fixed bug that caused incorrect type evaluation when a return type in a generic function used a Callable with Concatenate and a ParamSpec.
    -   Bug Fix: Fixed bug in code that prints types (e.g. in error messages and hover text) that resulted in duplicate types in a union when typeCheckingMode was "off".
        ([pylance-release#920](https://github.com/microsoft/pylance-release/issues/920))
    -   Enhancement: Updated code that prints function types (e.g. for error messages and hover text) to include unioned return types in parentheses to distinguish between `() -> (int | str)` and `() -> int | str`.
    -   Bug Fix: Fixed formatting of usage text in CLI. Fix contributed by @fannheyward.
    -   Bug Fix: Fixed bug that caused problems when the type `ellipsis` was used in a type stub instead of `...`.
        ([pylance-release#925](https://github.com/microsoft/pylance-release/issues/925))
    -   Bug Fix: Fixed recent regression in handling of isinstance second parameter.

## 2021.2.0 (3 February 2021)

Notable changes:

-   Docstring formatting has been greatly improved, and now better supports indented regions (such as parameter blocks in numpy/pandas docs), nested lists (such as those in argparse), and epydoc (used in OpenCV).
    ([pylance-release#41](https://github.com/microsoft/pylance-release/issues/41), [pylance-release#48](https://github.com/microsoft/pylance-release/issues/48), [pylance-release#83](https://github.com/microsoft/pylance-release/issues/83), [pylance-release#601](https://github.com/microsoft/pylance-release/issues/601), [pylance-release#696](https://github.com/microsoft/pylance-release/issues/696))
-   The creation and deletion of temporary files should no longer trigger reanalysis.
    ([pylance-release#905](https://github.com/microsoft/pylance-release/issues/905))
-   A regression that affected pkgutil-style namespace packages has been fixed.
    ([pylance-release#892](https://github.com/microsoft/pylance-release/issues/892))
-   Pylance now supports PEP 637 (indexing with keyword arguments) and PEP 646 (variadic generics). These PEPs are still in the draft phase (targeting Python 3.10) and may change before being finalized.
-   Pylance's copy of typeshed has been updated, including support for its new directory layout.

In addition, Pylance's copy of Pyright has been updated from 1.1.106 to 1.1.108, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Enhancement: Added perf optimization that avoids reallocation of special form classes (like Protocol and Literal) every time they're used. Since instance of the type is now cached and reused.
    -   Enhancement: Added some performance optimizations to handle cases where there are many overloads for a function (>100). Previous code hit n^2 analysis times where n is number of overloads.
-   [1.1.108](https://github.com/microsoft/pyright/releases/tag/1.1.108)
    -   Behavior change: Changed type inference logic for binary expressions of the form `x or []` so `[]` uses the type of `x` to inform its type.
    -   Bug Fix: Fixed bug in the way a specialized variadic type alias is printed (for error messages, hover text, etc.).
    -   Enhancement: Added support for subscript index lists that contain a trailing comma (e.g. `a[0,]`). The subscript in this case is a tuple and is not valid for most objects, so it should generate an error.
    -   Enhancement: Improved parse error recovery for empty subscripts (e.g. `a[]`). Started to add support for PEP 637.
    -   Enhancement: Improved consistency of error messages.
    -   New Feature: Added support for PEP 637 (keyword and unpacked arguments in subscripts). This PEP is still in the draft phase and may change before being finalized.
    -   New Feature: Added a way for the "verifytypes" feature to ignore partially-unknown types imported from external packages. To use this feature, append a "!" to the end of the package name provided after the "--verifytypes" option.
-   [1.1.107](https://github.com/microsoft/pyright/releases/tag/1.1.107)
    -   Bug Fix: Fixed cyclical type resolution with TypeVar.
    -   Behavior Change: Updated typeshed stubs to new directory layout.
    -   Bug Fix: Fixed false positive error in try/except/finally statement. Call expressions are now assumed to possibly result in raised exceptions, and finally clauses are assumed to be exception targets.
    -   Bug Fix: Fixed regression in import resolution where the first portion of the import path matches multiple namespace packages.
        ([pylance-release#892](https://github.com/microsoft/pylance-release/issues/892))
    -   New Feature: Added initial support for PEP 646 (variadic type variables). This PEP is still in the draft stage and is likely to change before it is ratified.
    -   Enhancement: Added check for duplicate keyword arguments that map to \*\*kwargs parameter.
    -   Enhancement: Added support for class properties, which are now supported in Python 3.9.
    -   Behavior: Eliminated false positive errors for unbound variables that are targets of a for loop iterator and used after the for loop. This change can result in some false negatives.
        ([pylance-release#496](https://github.com/microsoft/pylance-release/issues/496))

## 2021.1.3 (27 January 2021)

Notable changes:

-   Deleting an entire folder in the workspace will now correctly retrigger analysis.
-   Analysis performance has been improved in the case of deeply nested expressions with calls to overloaded functions.
-   Import resolution should now pick the correct module when both a namespace module and a traditional module have the same name in the search paths.
    ([pylance-release#859](https://github.com/microsoft/pylance-release/issues/859))
-   The variable override compatibility check will now correclty ignore private class members.
    ([pylance-release#863](https://github.com/microsoft/pylance-release/issues/863))
-   A number of crashes and analysis bugs have been fixed.
-   The default setting for indexing in the insiders build has been temporarily changed to `false` to pin down potential performance regressions in the feature. It can still be manually enabled with `"python.analysis.indexing": true`.

In addition, Pylance's copy of Pyright has been updated from 1.1.103 to 1.1.106, including the following changes:

-   [1.1.106](https://github.com/microsoft/pyright/releases/tag/1.1.106)
    -   Bug Fix: Added missing check for empty f-string expression.
    -   Bug Fix: Fixed a bug that resulted in incorrect bidirectional type inference when the source was a call to a constructor and the destination (expected) type was a recursive type alias that includes a union with only some subtypes that match the constructed type.
        ([pylance-release#721](https://github.com/microsoft/pylance-release/issues/721))
    -   Bug Fix: Fixed two issues in the import resolution logic. First, it was returning a namespace module if it found one in the workspace path or extraPaths even if a traditional (non-namespace) module satisfied the import from the sys.path. The interpreter searches all paths and always prefers a traditional module if it can find it. Second, it was resolving a namespace module if a traditional module only partially resolved the import path. The real interpreter always prefers a traditional module even if it partially resolves the path (in which case the full import fails).
        ([pylance-release#859](https://github.com/microsoft/pylance-release/issues/859))
    -   Behavior Change: When too few type arguments are provided for a generic class specialization, this diagnostic is now handled via reportGeneralTypeIssues rather than reportMissingTypeArgument. The latter is reserved for cases where type arguments are omitted completely.
    -   Enhancement: Improved type narrowing logic for isinstance and issubclass so they better handle the case where the class passed in the second argument is a type variable.
-   [1.1.105](https://github.com/microsoft/pyright/releases/tag/1.1.105)
    -   Enhancement: Added missing check for \*\* used in argument expressions. The expression after the \*\* must be a mapping with str keys.
    -   Enhancement: Added missing check for a name-only parameter appearing in a signature after a "\*args: P.args" ParamSpec parameter.
    -   Enhancement: Improved error message for non-keyword parameter that follows a "\*" parameter.
    -   Enhancement: Added missing check for positional argument count when a simple positional argument appears after a \*args argument.
    -   Enhancement: Added missing checks for illegal usage of positional parameters when calling a function defined with ParamSpec and Concatenate.
    -   Enhancement: Added missing check for use of keyword arguments in a call to an inner function that uses P.args and P.kwargs defined by a ParamSpec.
    -   Bug Fix: Fixed false positive warning relating to single use of a type variable within a signature when that type variable is a ParamSpec, and it is also referenced in "P.args" or "P.kwargs" annotations.
    -   Enhancement: Added missing PEP 612 support for functions that take a parameter with a callable type that includes a ParamSpec as well as \*args: P.args and \*\*kwargs: P.kwargs parameters.
    -   Bug Fix: Fixed false positive error related to use of "ClassVar" when it is used in a member access expression like "typing.ClassVar".
        ([pylance-release#876](https://github.com/microsoft/pylance-release/issues/876))
    -   Enhancement: Improved performance for deeply nested expressions that involve calls to overloaded functions.
    -   Bug Fix: Fixed crash when "()" is used as a type argument for a class that doesn't accept variadic type parameters.
-   [1.1.104](https://github.com/microsoft/pyright/releases/tag/1.1.104)
    -   Bug Fix: Fixed bug in import resolver where a namespace package was chosen over a traditional package if the former had a shorter name.
    -   Enhancement: Added support for `__call__` method overloads when assigning a callable object to a callable type.
    -   Enhancement: Added error for a subscripted type annotation that involves a quoted expression in the LHS of the subscript. This generates runtime errors.
    -   Enhancement: Enhanced reportIncompatibleMethodOverride diagnostic check to support overrides that have `*args` and `**kwargs` parameters.
    -   Enhancement: Improved completion suggestions to better handle super calls in base class methods.
    -   Bug Fix: Fixed bug that affected the case where a class variable has a declared type in a base class, and a subclass assigns a value to that class variable but doesn't (re)declare its type. In this case, the type of the expression assigned within the base class should use the expected type declared in the base class for type inference.
        ([pylance-release#861](https://github.com/microsoft/pylance-release/issues/861))
    -   Enhancement: Added missing error logic to handle the case where a type variable is used in the LHS of a member access expression. This isn't supported currently in the Python type system.
    -   Enhancement: Improved error checking and reporting for NewType (for unions, literals, callables, protocol classes, and type variables).
    -   Enhancement: Added error check for an attempt to instantiate a literal (`Literal[1]()`).
    -   Bug Fix: Fixed bug in TypeVar constraint solving logic. If an "Any" or "Unknown" type is being assigned to a constrained TypeVar, it should result in "Any" or "Unknown" rather than the first constrained type.
    -   Enhancement: Added check for multiple functions declared within the same scope that have the same name, with the final one overwriting the earlier ones. This check is suppressed for overloaded functions and property setters/deleters.
        ([pylance-release#865](https://github.com/microsoft/pylance-release/issues/865))
    -   Enhancement: Improved the reportIncompatibleVariableOverride diagnostic check so it ignores symbols with private names (i.e. start with double underscores).
        ([pylance-release#863](https://github.com/microsoft/pylance-release/issues/863))
    -   Bug Fix: Changed hover text to use the last declaration of a symbol rather than the first declaration to determine which type category text (e.g. "(module)" or "(class)") in the hover text.
        ([pylance-release#867](https://github.com/microsoft/pylance-release/issues/867))
    -   Bug Fix: Fixed bug that caused error when invoking the definition provider on an unresolved module import.
    -   Bug Fix: Fixed bug in logic that infers symbol types that resulted in "unbound" types to be reported incorrectly in certain rare circumstances.
        ([pylance-release#864](https://github.com/microsoft/pylance-release/issues/864))
    -   Bug Fix: Fixed a crash in the "--verifytypes" feature of the CLI.
    -   Bug Fix: Fixed bug in file watching logic so it properly handles cases where an entire folder is deleted.

## 2021.1.2 (20 January 2021)

Notable changes:

-   Completions for method overrides in classes without a parent class will no longer generate unnecessary `super()` calls.
-   Signature help tooltips will now work when the closing parenthesis is missing.
-   Code in `context.surpress` blocks should no longer be unintentionally grayed out in some cases.
    ([pylance-release#494](https://github.com/microsoft/pylance-release/issues/494))
-   Methods prefixed with a single underscore are now correctly checked for incompatible overrides.
    ([pylance-release#843](https://github.com/microsoft/pylance-release/issues/843))
-   An internal error related to NewType when used with Protocols has been fixed.
    ([pylance-release#825](https://github.com/microsoft/pylance-release/issues/825))
-   `@final` and `Final` checks will now ignore private class members and no longer ignore members prefixed with a single underscore when checking for redeclarations.
    ([pylance-release#725](https://github.com/microsoft/pylance-release/issues/725))

In addition, Pylance's copy of Pyright has been updated from 1.1.101 to 1.1.103, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug in import resolver where a namespace package was chosen over a traditional package if the former had a shorter name.
        ([pylance-release#853](https://github.com/microsoft/pylance-release/issues/853))
    -   Enhancement: Added support for `__call__` method overloads when assigning a callable object to a callable type.
    -   Enhancement: Added error for a subscripted type annotation that involves a quoted expression in the LHS of the subscript. This generates runtime errors.
    -   Enhancement: Enhanced reportIncompatibleMethodOverride diagnostic check to support overrides that have `*args` and `**kwargs` parameters.
    -   Behavior Change: Changed error message about quoted type annotations with non-quoted subscripts to be conditional based on stubs and Python version. This will be supported at runtime in Python 3.10.
-   [1.1.103](https://github.com/microsoft/pyright/releases/tag/1.1.103)
    -   Bug Fix: Suppressed "symbol is unbound" error when used in a `del` statement, since this is legal.
    -   Enhancement: Enhanced --verifytypes command so it can now accept a module path within a package. Type analysis is limited to the specified module and its submodules.
    -   Bug Fix: Fixed bug that caused "--verifytypes" feature to report missing return type annotations for all property getters within a class if only one of them was missing a return type annotation.
    -   Enhancement: Added missing error logic to handle the case where a type variable is subscripted in a type expression. This isn't supported currently in the Python type system.
    -   Enhancement: Improved signature help in case where right parenthesis is missing.
    -   Enhancement: Added error for incorrect use of list expression for type arguments.
-   [1.1.102](https://github.com/microsoft/pyright/releases/tag/1.1.102)
    -   Enhancement: Added error for Callable that is missing a return type.
    -   Behavior Change: Changed type analysis behavior when reportGeneralTypeIssues diagnostic rule is disabled and an incompatible type is assigned to a variable. Previously, the assigned type was retained in this case, but now the declared type is assumed (as it is when reportGeneralTypeIssues is enabled).
    -   Enhancement: Added support for completion suggestions within subscript for typed dict attribute names.
    -   Behavior Change: Change string literals to use "constant" type when displayed in completion suggestion lists.
    -   Behavior Change: Changed logic for detecting overrides of Final member variables by subclasses. Symbols with double underscores are now exempt from this check, since they are considered private and are name-mangled.
        ([pylance-release#725](https://github.com/microsoft/pylance-release/issues/725))
    -   Bug Fix: Fixed bug in logic that detects overrides of @final methods. The logic was not handling the case where a private (single underscore) method was marked final.
        ([pylance-release#725](https://github.com/microsoft/pylance-release/issues/725))
    -   Enhancement: Updated typeshed stubs to latest.
    -   Bug Fix: Fixed regression in code that handles context managers that suppress exceptions.
        ([pylance-release#494](https://github.com/microsoft/pylance-release/issues/494))
    -   Bug Fix: Fixed bug that resulted in infinite recursion (and an internal error) when NewType was used with a protocol class.
        ([pylance-release#825](https://github.com/microsoft/pylance-release/issues/825))
    -   Bug Fix: Fixed reportIncompatibleMethodOverride diagnostic check so it doesn't ignore incompatible protected methods (those whose names start with a single underscore).
        ([pylance-release#843](https://github.com/microsoft/pylance-release/issues/843))
    -   Enhancement: Added support for "reveal_locals()" call to reveal all of the symbols within the current scope.
    -   Bug Fix: Fixed internal error resulting from an assignment expression located within a list comprehension scope which is contained within a class scope.
    -   Enhancement: Augmented type completeness JSON output to include alternate public names of exported symbols. For example, if a symbol "foo" is declared in module "a.b.c" and is also re-exported from "a", then the main name of the symbol is "a.b.c.foo", but it has an alternate name of "a.foo".
    -   Enhancement: Improved "partially unknown type" error messages within type completeness report.

## 2021.1.1 (13 January 2021)

Notable changes:

-   The new "report issue" VS Code command can automatically fill out a new GitHub issue template for simpler bug reporting.
    ([pylance-release#762](https://github.com/microsoft/pylance-release/issues/762))
-   The PYTHONPATH environment variable is now supported. This requires a recent insiders build of the Python extension (or the yet-to-be-released January version).
    ([pylance-release#275](https://github.com/microsoft/pylance-release/issues/275))
-   Variables that are annotated but assigned a value of the wrong type will now use the annotated type rather than using the incorrect type (while in the "off" type checking mode, Pylance's default).
    ([pylance-release#822](https://github.com/microsoft/pylance-release/issues/822))
-   A number of crashes and performance issues have been fixed.
    ([pylance-release#825](https://github.com/microsoft/pylance-release/issues/825))
-   `TypedDict` keys are now suggested in index expression completions.
    ([pylance-release#827](https://github.com/microsoft/pylance-release/issues/827))
-   The semantic token types for class members and methods have been changed to `property` and `method` respectively, for consistency with the LSP spec and other languages in VS Code.
-   Type stubs for SQLAlchemy are now bundled, improving completions, type checking, and other features.
-   The bundled Django stubs have been updated to the latest version.

In addition, Pylance's copy of Pyright has been updated from 1.1.99 to 1.1.101, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Enhancement: Added error for Callable that is missing a return type.
    -   Behavior Change: Changed type analysis behavior when reportGeneralTypeIssues diagnostic rule is disabled and an incompatible type is assigned to a variable. Previously, the assigned type was retained in this case, but now the declared type is assumed (as it is when reportGeneralTypeIssues is enabled).
        ([pylance-release#822](https://github.com/microsoft/pylance-release/issues/822))
    -   Enhancement: Added support for completion suggestions within subscript for typed dict attribute names.
-   [1.1.101](https://github.com/microsoft/pyright/releases/tag/1.1.101)
    -   Bug Fix: Fixed false negative for "reportUnknownParameterType" diagnostic rule when all function parameters were unannotated.
    -   Bug Fix: Fixed a couple of issues with TypeGuard. Previously, `TypeGuard` was implemented as an alias to `bool` which meant that `bool` was assignable to `TypeGuard` in all circumstances. Now it is special-cased to be assignable only in return statements.
    -   Bug Fix: Fixed bug that caused definition provider to not fully resolve a submodule symbol in certain cases.
    -   Enhancement: Added support for aliases of imported module "sys" when evaluating "sys.platform" and "sys.version".
    -   Behavior Change: Suppressed "Covariant type variable cannot be used in parameter type" diagnostic in the case of an `__init__` method to match mypy behavior.
    -   Bug Fix: Fixed regression that broke type inference for packages with no "py.typed" file and no stubs when "useLibraryCodeForTypes" was enabled.
-   [1.1.100](https://github.com/microsoft/pyright/releases/tag/1.1.100)
    -   Bug Fix: Fixed bug that caused "Type" with no type argument not to be flagged as an error.
    -   Enhancement: Changed pythonPlatform to accept a value of "All" in which case no particular platform will be used over the others.
    -   Bug Fix: Fixed bug that caused improper error when using "self" in a "raise ... from self" statement.
    -   Bug Fix: Fixed bug that caused false negative when using a generic type alias with no type arguments.
    -   Bug Fix: Added cache for logic that determines whether a context manager swallows exceptions (and hence acts like a try/except statement). This cache not only improves performance of code flow walks but also prevents infinite recursion in rare cases.
    -   Behavior Change: Improved handling of unannotated decorator functions. If the decorator returns a function that accepts only \*args and \*\*kwargs (which is common), the type checker now assumes that the decorated function or method's signature is unmodified by the decorator. This preserves the original signature and docstring.
        ([pylance-release#125](https://github.com/microsoft/pylance-release/issues/125))
    -   Bug Fix: Fixed bug that caused types within a "finally" clause to be evaluated incorrectly in situations where the "try" and all "except" and "else" clauses returned, raised, or broke.
    -   Enhancement: Changed error messages that refer to "named" parameters and arguments to "keyword", which is more standard for Python.
    -   Bug Fix: Fixed bug in declaration provider where the declaration of a member wasn't properly resolved when the LHS of the member access was a call to a function that returns a `Type[X]`.
        ([pylance-release#821](https://github.com/microsoft/pylance-release/issues/821))
    -   Bug Fix: Fixed bug that manifest as a problem with enums but was actually a problem in handling the circular dependency between "type" and "object" classes (since "type" is an object and "object" is a type).
    -   Bug Fix: Fixed bug that caused incorrect type evaluation when a class was assigned to a generic protocol that was satisfied by the class's metaclass if the class also derived from a base class that also satisfied the same protocol.
    -   Enhancement: Added code to test for missing annotation in `Annotated`.
    -   Bug Fix: Fixed false negative where a union type was assigned to a constrained type variable. An error should be generated in this situation.
    -   Enhancement: Added additional validation for TypeVar scoping. If an outer class defines the scope for a type var, functions and variables within an inner class cannot use a TypeVar of the same name.
    -   Bug Fix: Improved handling of "py.typed" for namespace packages and packages with submodules.
    -   Enhancement: Added support for `__index__` magic method when used with `__getitem__` or `__setitem__` magic methods.
    -   Enhancement: Added support for matching modules against protocols as specified by PEP 544.
    -   Bug Fix: Fix for missing docs in completion list due to only checking the setter for docs because its definition comes after the getter.

## 2021.1.0 (6 January 2021)

Notable changes:

-   Python files which do not have a `.py` or `.pyi` file extension are now supported.
    ([pylance-release#739](https://github.com/microsoft/pylance-release/issues/739), [pylance-release#803](https://github.com/microsoft/pylance-release/issues/803), [pylance-release#810](https://github.com/microsoft/pylance-release/issues/810))
-   Analysis performance has been improved in cases of deeply nested expressions.
    ([pylance-release#590](https://github.com/microsoft/pylance-release/issues/590), [pylance-release#767](https://github.com/microsoft/pylance-release/issues/767))
-   Numerous type checking error messages have been improved, including for `TypedDict`, type variable scoping, yields, and `ParamSpec` with overloads.
-   Two diagnostics have been added, `reportInvalidTypeVarUse` and `reportUnusedCoroutine`.
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.94 to 1.1.99, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug that caused "Type" with no type argument not to be flagged as an error.
    -   Enhancement: Changed pythonPlatform to accept a value of "All" in which case no particular platform will be used over the others.
        ([pylance-release#794](https://github.com/microsoft/pylance-release/issues/794))
    -   Bug Fix: Fixed bug that caused improper error when using "self" in a "raise ... from self" statement.
        ([pylance-release#806](https://github.com/microsoft/pylance-release/issues/806))
    -   Bug Fix: Fixed bug that caused false negative when using a generic type alias with no type arguments.
-   [1.1.99](https://github.com/microsoft/pyright/releases/tag/1.1.99)
    -   Enhancement: Improved error messages for expected TypeDicts. (Contribution from Sam Abey.)
    -   Bug Fix: Fixed bug where an \*args or \*\*kwargs parameter could be specified by name in a function call.
    -   Behavior Change: Changed behavior of kwargs parameter that has a generic (TypeVar) type annotation. Literals are now stripped in this case before assigning to the TypeVar.
    -   Enhancement: Improved mechanism for overloaded `__init__` method that uses `self` parameter annotation to specify the result of a constructor. The new mechanism supports generic type arguments within the `self` annotation.
    -   Bug Fix: Fixed bug that caused sporadic errors when modifying the builtins.pyi stub file.
    -   Bug Fix: Fixed bug with overlapping overload detection. It was reporting an incorrect overlap when a different TypeVar (bound vs unbound) was used in two overloads.
    -   Bug Fix: Fixed another false positive error related to overlapping overload methods with a TypeVar in a parameter annotation.
    -   Bug Fix: Fixed bug that caused internal stack overflow when attempting to assign a class to a protocol that refers to itself.
    -   Enhancement: Improved support for protocol matching for protocols that include properties. Getter, setter and deleter methods are now individually checked for presence and type compatibility, and generics are now supported.
    -   Enhancement: Updated to latest typeshed stubs.
-   [1.1.98](https://github.com/microsoft/pyright/releases/tag/1.1.98)
    -   New Feature: Added new diagnostic rule "reportUnusedCoroutine" that reports an error if the result returned by an async function is not consumed (awaited, assigned to a variable, etc.). This detects and reports a common error when using async coroutines.
    -   Enhancement: Improved error messages for invalid type annotation syntax usage.
    -   Enhancement: Updated to the latest typeshed stubs.
    -   Bug Fix: Fixed recent regression in error message for bound TypeVars that resulted in a confusing message.
    -   Bug Fix: Fixed bug in error messages for parameter type incompatibility; reported parameter number off by one leading to confusing message.
    -   Bug Fix: Fixed bug in type compatibility logic when the destination was a metaclass instance and the dest was a class that derived from that metaclass.
    -   Bug Fix: Fixed bug that caused failure in protocol type matching when the protocol contained a method with an annotated "self" parameter.
    -   Behavior Change: If a class derives from a protocol class explicitly, individual members are no longer type-checked. This improves performance of type evaluation in some cases.
    -   Bug Fix: Fixed bug whereby the presence of a `__getattr__` method on a class with no `__init__` method generated an incorrect error when instantiating the class.
    -   Enhancement: Implemented complete support for module-level `__getattr__` functions as described in PEP 562.
    -   Behavior Change: Eliminated restriction that prevented the analysis of text files that don't end in ".py" or ".pyi".
        ([pylance-release#739](https://github.com/microsoft/pylance-release/issues/739), [pylance-release#803](https://github.com/microsoft/pylance-release/issues/803), [pylance-release#810](https://github.com/microsoft/pylance-release/issues/810))
-   [1.1.97](https://github.com/microsoft/pyright/releases/tag/1.1.97)
    -   Enhancement: Improved type analysis performance in cases where an expression contains deeply-nested expressions that involve calls to overloaded functions or bidirectional type inference.
    -   Bug Fix: Fixed bug in ParamSpec logic that affected the case where a generic function with specialized parameters was matched to the ParamSpec.
    -   Bug Fix: Fixed bug where a union with a NoReturn subtype could have been generated when evaluating a union of iterable types.
    -   Enhancement: Improved type narrowing logic for "a is b" narrowing in the case where b is a union that contains both literal and non-literal subtypes.
    -   Enhancement: Added error condition for the situation where an overloaded function is used in conjunction with a ParamSpec.
    -   Bug Fix: Fixed bug that resulted in a false negative error when performing type assignment checks for functions that contain unspecialized type variables.
    -   Enhancement: Improved error messages that include type variables. The scope that defines the type variable is now included. This avoids confusing and seemingly-contradictory error messages like "type \_T cannot be assigned to type \_T".
    -   Bug Fix: Fixed bug that caused type evaluator to generate different results if someone hovered over the name of a type variable within an index expression before the entire source file was analyzed.
-   [1.1.96](https://github.com/microsoft/pyright/releases/tag/1.1.96)
    -   Enhancement: Updated typeshed stubs to the latest.
    -   Behavior Change: Switched to LSP-native progress reporting rather than using custom progress reporting messages.
    -   New Feature: Added a new diagnostic rule called "reportInvalidTypeVarUse" that flags errors when TypeVars are used incorrectly. In particular, it flags the use of a single instance of a TypeVar within a generic function signature.
    -   Bug Fix: Fixed assertion (and associated crash) that results when an LS client asks the language server to open a non-Python file (i.e. one whose file name doesn't have a ".py" or ".pyi" extension). The server now ignores such requests rather than crashing.
    -   Enhancement: Enhanced ParamSpec mechanism to support parameters that have default values.
    -   Bug Fix: Fixed issue with variable expansion for environment variables used within settings.
    -   Enhancement: Improved error message for yield type mismatch.
    -   Performance Improvement: Added a heuristic to skip call-site return type inference if the number of arguments is above a threshold (6). This avoids long analysis times for complex unannotated functions.
        ([pylance-release#729](https://github.com/microsoft/pylance-release/issues/729))
    -   Bug Fix: Fixed bug in error message for tuple size mismatches in the case where the source tuple has indeterminate length and the dest has a specified length.
    -   Bug Fix: Fixed incorrect assertion (which manifests as a runtime crash) when assigning to a type that is a generic class with no specified type arguments.
    -   Enhancement: Added new error for a protocol class that derives from a non-protocol base class.
    -   Behavior Change: Changed the logic for `Type` vs `type` such that `Type` (the capitalized form) is always used in cases where there is a type argument (such as `Type[int]` or `type[str]` and `type` is used in cases where the non-generic class `type` is intended. This allows `type` to be used in `isinstance` type narrowing.
    -   Bug Fix: Fixed bug in function assignment logic in the case where the destination function has name-only parameters and the source has positional parameters that match those name-only parameters.
    -   Behavior Change: Changed heuristic for when a decorator should be ignored for purposes of type checking. It was previously ignored if the application of the decorator resulted in an "Unknown" type. The new heuristic also ignores the application of the decorator if the resulting type is a union that includes an Unknown subtype. This situation occurs frequently with unannotated decorators where part of the result can be inferred but part cannot.
        ([pylance-release#728](https://github.com/microsoft/pylance-release/issues/728))
    -   Bug Fix: Fixed bug that caused incorrect type evaluation when a relative import referenced a submodule with the same name as a symbol that was imported from that submodule if that submodule was later imported again within the same file (e.g. `from .foo import foo, from .foo import bar`).
        ([pylance-release#750](https://github.com/microsoft/pylance-release/issues/750))
    -   Enhancement: Added support for protocol callable types when performing bidirectional type inference for lambda expressions.
        ([pylance-release#754](https://github.com/microsoft/pylance-release/issues/754))
    -   Enhancement: Improved "isinstance" narrowing to better handle the case where the narrowed expression is a constrained TypeVar. It now preserves the constraint so the value can be assigned back to the TypeVar type.
    -   Bug Fix: Fixed bug in "is None" and "is not None" type narrowing logic when dealing with recursive type aliases.
-   [1.1.95](https://github.com/microsoft/pyright/releases/tag/1.1.95)
    -   Behavior Change: Changed encoding of diagnostics reported through the LSP interface. The diagnostic rule (if applicable) is now reported in the "code" field, and a URL points to general documentation for diagnostic rules.
    -   Enhancement: Added support for type arg lists specified in a tuple expression (like `Dict[(str, str)]`) which is a legal way of writing type annotations.
    -   Bug Fix: Fixed infinite recursion due to a `__call__` method that returns an instance of the class that is being called.
    -   Bug Fix: Fixed bug that caused completion suggestions not to work for member accesses when the LHS of the expression was a type specified in the form `Type[X]`.
    -   Bug Fix: Fixed bug that resulted in an attempt to parse and bind a native library (binary file) resulting in long latencies and out-of-memory errors.
    -   Enhancement: Improved error message for unknown named parameters for TypeVar constructor.
    -   Bug Fix: Fixed recent regression that causes a crash in certain circumstances when binding a method to an object or class in cases where that method doesn't have a "self" parameter but instead just has `*args` and `**kwargs` parameters.
    -   Bug Fix: Fixed bug that resulted in incorrect reporting of unreported variables or parameters when they are accessed within argument expressions in cases where an error is detected when analyzing a call expression.
    -   Enhancement: Expand ${env:HOME} in settings. Thanks to @ashb for the contribution.
    -   Bug Fix: Fixed bug that generated incorrect errors when a callable type included another callable type as an input parameter and the second callable type had generic parameter types.
    -   Bug Fix: Fixed bug that caused a false negative when a default parameter value was assigned to a parameter with a generic type annotation.
    -   Bug Fix: Fixed bug that caused incorrect error to be reported when applying logical operators ("|", "&" or not) to enum.Flag literals.
        ([pylance-release#726](https://github.com/microsoft/pylance-release/issues/726))

## 2020.12.2 (11 December 2020)

Notable changes:

-   Extract method and variable refactorings are now enabled for all users.
-   Binary files will no longer be mistakenly loaded as source code.
    ([pylance-release#706](https://github.com/microsoft/pylance-release/issues/706))
-   Various crashes and stack overflows have been fixed.
    ([pylance-release#709](https://github.com/microsoft/pylance-release/issues/709), [pylance-release#717](https://github.com/microsoft/pylance-release/issues/717))

In addition, Pylance's copy of Pyright has been updated, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Behavior Change: Changed encoding of diagnostics reported through the LSP interface.
    -   Enhancement: Added support for type arg lists specified in a tuple expression (like `Dict[(str, str)]`) which is a legal way of writing type annotations.
    -   Bug Fix: Fixed infinite recursion due to a `__call__` method that returns an instance of the class that is being called.
        ([pylance-release#709](https://github.com/microsoft/pylance-release/issues/709))
    -   Bug Fix: Fixed bug that caused completion suggestions not to work for member accesses when the LHS of the expression was a type specified in the form `Type[X]`.
        ([pylance-release#714](https://github.com/microsoft/pylance-release/issues/714))
    -   Bug Fix: Fixed bug that resulted in an attempt to parse and bind a native library (binary file) resulting in long latencies and out-of-memory errors.
        ([pylance-release#706](https://github.com/microsoft/pylance-release/issues/706))
    -   Bug Fix: Fixed recent regression that causes a crash in certain circumstances when binding a method to an object or class in cases where that method doesn't have a "self" parameter but instead just has `*args` and `**kwargs` parameters.
        ([pylance-release#717](https://github.com/microsoft/pylance-release/issues/717))
    -   Bug Fix: Fixed bug that resulted in incorrect reporting of unreported variables or parameters when they are accessed within argument expressions in cases where an error is detected when analyzing a call expression.
        ([pylance-release#719](https://github.com/microsoft/pylance-release/issues/719))

## 2020.12.1 (9 December 2020)

Notable changes:

-   Context managers that may suppress exceptions (such as `contextlib.suppress`) will no longer mark code after the `with` block as unreachable.
    ([pylance-release#494](https://github.com/microsoft/pylance-release/issues/494))
-   Various stack overflows have been fixed.
    ([pylance-release#701](https://github.com/microsoft/pylance-release/issues/701))
-   Stack traces in error messages should now provide more detailed information, aiding in issue reporting for internal errors and crashes.

In addition, Pylance's copy of Pyright has been updated from 1.1.91 to 1.1.94, including the following changes:

-   [1.1.94](https://github.com/microsoft/pyright/releases/tag/1.1.94)
    -   Bug Fix: Fixed potential source of infinite recursion in type evaluator.
    -   Behavior Change: Changed behavior of tuples to strip literals when converting the variadic list of type arguments into a single "effective" type argument. This means the expression `list((1,))` will now be evaluated as type `list[int]` rather than `list[Literal[1]]`.
        ([pylance-release#697](https://github.com/microsoft/pylance-release/issues/697))
    -   Bug Fix: Fixed bug in parser that generated an inappropriate syntax error when an annotated variable assignment included a star test list on the RHS with an unpack operator.
        ([pylance-release#700](https://github.com/microsoft/pylance-release/issues/700))
    -   Enhancement: Added support for context managers that are designed to suppress exceptions.
    -   Bug Fix: Fix infinite recursion in logic that maps pyi files to py files.
    -   Enhancement: Improved source maps for better stack traces, useful for bug reports.
-   [1.1.93](https://github.com/microsoft/pyright/releases/tag/1.1.93)
    -   Enhancement: Added support for TypeVar objects that are used outside of type annotations.
    -   Bug Fix: Fixed bug that caused incorrect error when performing binary operations (arithmetics, comparisons, etc.) on classes that define corresponding magic methods that are instance methods. When performing the operation on the class, the magic methods in the metaclass should be used instead.
        ([pylance-release#705](https://github.com/microsoft/pylance-release/issues/705))
    -   Enhancement: Added support for frozen dataclasses. Errors are now reported if a frozen dataclass inherits from a non-frozen dataclass and if an attempt is made to set the member of a frozen dataclass.
    -   Bug Fix: Added support for "bytes" type promotions for bytearray and memoryview.
        ([pylance-release#692](https://github.com/microsoft/pylance-release/issues/692))
    -   Bug Fix: Added support for static methods and class methods that are invoked on non-specialized generic classes where the arguments to the method provide sufficient context to fill in the missing class-level type arguments.
    -   Behavior Change: Changed reportWildcardImportFromLibrary diagnostic rule so it doesn't apply to type stub files.
    -   Bug Fix: Fixed bug that resulted in incorrect error when attempting to assign a constrained TypeVar to a union type that satisfied all of the constrained types.
    -   Bug Fix: Added support for binary operator magic methods that operate on constrained TypeVars.
    -   Bug Fix: Fixed the logic that determines whether a type can be assigned to another type when invariance rules are in effect - in particular when the destination is a union. Previously, the unions needed to match exactly. The new logic takes into account whether the destination union contains subtypes that are subclasses of each other.
    -   Bug Fix: Fixed bug where None and Callable types could be assigned to "object" even when invariant rules were in effect. This allowed `List[None]` to be assigned to `List[object]`.
-   [1.1.92](https://github.com/microsoft/pyright/releases/tag/1.1.92)
    -   Bug Fix: Fixed bug in parser that resulted in the opening parenthesis ("(") in a parenthesized expression or tuple not being included in the parse node range.
    -   Bug Fix: Fixed bug that could result in "unaccessed variable" error for variables that were referenced in argument expressions if there were other errors related to the call expression.
    -   Bug Fix: Fixed bug in logic dealing with comment-style function annotations that resulted in spurious errors if "self" was used within an instance method that was so annotated.
    -   Bug Fix: Fixed bug that caused errors when a hierarchy of dataclass classes used generic types for one or more dataclass members.
    -   Bug Fix: Fixed bug in type checker where it allowed invariant type parameters to violate invariance if the destination was an "object" instance.
    -   Bug Fix: Fixed off-by-one error in fstring parsing with debug variables that resulted in errors if the "=" was not preceded by a space.
        ([pylance-release#686](https://github.com/microsoft/pylance-release/issues/686))
    -   Bug Fix: Fixed bug in logic that validates the assignment of a callable type to a generic callable when one of the parameters is another callable.
    -   Bug Fix: Fixed bug that affected generic type aliases that included callable types.
    -   Bug Fix: Fixed bug in bidirectional type inference logic when RHS includes call that returns a generic type. The old logic was prepopulating the type associated with that TypeVar but prevented the type from being further narrowed. This resulted in incorrect errors with argument expressions in some cases.
    -   Enhancement: Added PEP 604 support for unions passed as the second argument to isinstance and issubclass.
    -   Enhancement: Improved error messages for binary operations that involve a TypeVar for one of the operands.
    -   Enhancement: Updated the reportMissingTypeArgument diagnostic check to apply to bound types in TypeVar declarations.

## 2020.12.0 (2 December 2020)

Notable changes:

-   Extract method and extract variable code actions are available for preview in Pylance insiders (`"pylance.insidersChannel": "daily"`).
-   Completion suggestions are now matched more fuzzily. For example, typing `lx` will match a completion for `logical_xor`, even though it does not contain the substring `lx`.
    ([pylance-release#608](https://github.com/microsoft/pylance-release/issues/608))
-   Auto-imports (both completions and quick fixes) will now make use of existing imports when possible. For example, an auto-import completion for `array` when `import numpy as np` is present will now complete to `np.array`, rather than adding `from numpy import array`.
-   Auto-imports will now correctly insert a new import rather than reusing an import statement from a submodule.
    ([pylance-release#646](https://github.com/microsoft/pylance-release/issues/646))
-   Method override completions will now generate a `super()` call.
    ([pylance-release#668](https://github.com/microsoft/pylance-release/issues/668))
-   Completions for overridden methods will now show the correct signature.
-   VS Code's "word based suggestions" (`editor.wordBasedSuggestion`) are now disabled by default in Python files to mitigate poor completions when Pylance specifies no completions are available.
    ([pylance-release#604](https://github.com/microsoft/pylance-release/issues/604))
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.86 to 1.1.91, including the following changes:

-   [1.1.91](https://github.com/microsoft/pyright/releases/tag/1.1.91)
    -   Enhancement: Updated to the latest typeshed stubs.
    -   Bug Fix: Fixed bug in fstring parser that generated "unexpected token at end of string" errors if fstring debug (introduced in Python 3.8) was used in conjunction with string-formatting syntax and there was no space between the "=" and the ":".
    -   Bug Fix: Fixed bug that caused a spurious error when defining a property setter when the property getter had no declared return type.
    -   Bug Fix: Fixed bug in isinstance narrowing logic where it didn't properly preserve a TypeVar in the negative ("else") case.
    -   Bug Fix: Fixed bug in type narrowing logic for member access expressions like "a.b.c". A narrowed type needs to be abandoned if any part of the expression is reassigned (e.g. `a.b = <expression>`).
    -   Bug Fix: Fixed bug that resulted a "Never" type appearing as a type argument in an inferred function return type. "Never" should never be used as a type argument. It is now replaced by "Unknown" if it ever does appear.
    -   Bug Fix: (from pylance): Fixed completion case where the completion item said one method, but hover said another once inserted.
    -   Bug Fix: (from pylance): Reuse existing imports for auto-imports (e.g. if `import os.path` is present, `join` will use `os.path.join`).
-   [1.1.90](https://github.com/microsoft/pyright/releases/tag/1.1.90)
    -   Enhancement: Added support for type() call when argument contains a generic class instance.
    -   Enhancement: Improved reportIncompatibleMethodOverride diagnostic check for property overrides. It now checks for missing fget, fset, fdel methods and the overridden method types for each of these.
    -   Enhancement: Added special-case handling of overloaded `__init__` methods where the `self` parameter contains an annotation with a specialized version of the class. This is used in some typeshed stubs to influence the constructed object type when no additional information is available.
    -   Bug Fix: Fixed bug in parser that resulted in incorrect errors when an unpack operator was used within an f-string expression.
    -   Bug Fix: Fixed bug that resulted in incorrect errors when matching synthesized "cls" parameter type. This bug generally affected all TypeVars that were bound to a Type.
    -   Enhancement: Improved type checking support for constrained TypeVars within function and class bodies. This was a significant change, so there's some risk of regressions or new false-positive errors. Please report any bugs you see.
-   [1.1.89](https://github.com/microsoft/pyright/releases/tag/1.1.89)
    -   New Feature: Added support for new reportUnsupportedDunderAll diagnostic rule. It checks for unsupported manipulations of `__all__`.
    -   New Feature: Implemented new diagnostic rule reportUnusedCallResult that checks whether a call expression's results are consumed. If the results are None or Any, no diagnostic is produced.
    -   Enhancement: Added support for isinstance and issubclass type narrowing when "cls" or "self" parameters are used in the second argument
    -   Bug Fix: Fixed recent regression with TypeGuard type that caused spurious error when a bool value was return from a user-defined type guard function.
    -   Bug Fix: Fixed bug in reportIncompatibleMethodOverride diagnostic check where it incorrectly reported an error if a derived class used overload functions on an overridden method.
    -   Bug Fix: Fixed bug that caused incorrect binding when invoking a class method through an instance.
    -   Bug Fix: Fixed handling of recursive type annotations for variables (e.g. "int: int"). In some specific situations this is allowed if the annotation refers to a symbol in an outer scope.
    -   Bug Fix: Fixed several bugs related to constructor type inference when the expected type contained generic types with type arguments that contained type variables defined in a context outside of the constructor's call site.
-   [1.1.88](https://github.com/microsoft/pyright/releases/tag/1.1.88)
    -   Enhancement: This release includes a major update to TypeVar code. The type checker is now much more strict about how TypeVars are treated when analyzing the bodies of generic functions or methods within generic classes.
    -   Bug Fix: Fixed bug in synthesis of comparison operators in dataclass. By default, these methods should not be synthesized unless `order=True` is passed to the `@dataclass` decorator.
    -   Bug Fix: Fixed bug that caused incorrect specialization of a TypeVar when used in a descriptor class with a `__set__` method.
    -   Bug Fix: Fixed incorrectly handling of generic type alias that is defined in terms of other generic type aliases.
        ([pylance-release#636](https://github.com/microsoft/pylance-release/issues/636))
    -   Bug Fix: Fixed bug that caused incorrect overload to be selected in cases where a named argument was used.
    -   Enhancement: Improved signature help for calls to namedtuple constructor.
        ([pylance-release#630](https://github.com/microsoft/pylance-release/issues/630))
    -   Bug Fix: Added support for a generic method whose "self" parameter is annotated with a bound TypeVar and is then invoked using another bound TypeVar.
    -   Bug Fix: Improved error reporting for assignments to protocols.
    -   Enhancement: Added support for the instantiation of a class via a constructor when the type of the class is specified as a TypeVar.
    -   Bug Fix: Fixed inappropriate error in strict mode when a named argument for a call expression begins with an underscore.
    -   Bug Fix: Fixed bug that results in an incorrect type when a call to a function returns a generic type and the result is assigned to a variable with a declared type that includes a union.
-   [1.1.87](https://github.com/microsoft/pyright/releases/tag/1.1.87)
    -   Bug Fix: Fixed bug with type annotations that use a TypeVar with the new union syntax.
    -   Behavior Change: Removed special-case code that eliminates a NoReturn from an async function.
    -   Behavior Change: Changed behavior of NoReturn when it appears within unions. Previously, it was always filtered out of unions. It is now filtered out only in the inferred return type of a function. This allows NoReturn to be used in unions in other legitimate cases.
    -   Bug Fix: Fixed bug that resulted in a false negative when a callable type with a kwargs parameter was assigned to a callable type without a kwargs or with a kwargs of a different type.
    -   Enhancement (from Pylance): Changed fuzzy text matching algorithm for completion suggestions.
    -   Bug Fix: Fixed bug whereby an assignment was not flagged as an error if the target type contains a type var and the source is concrete. This change generally makes the core type checker more strict about the use of type variables.
    -   Enhancement: Added support for "eq" and "order" parameters in dataclass decorator as defined in PEP 557.
    -   New Feature: Added new diagnostic rule "reportFunctionMemberAccess" that reports an attempt to access, set or delete non-standard attributes of function objects.

## 2020.11.2 (18 November 2020)

Notable changes:

-   Pylance now includes generated stubs for select compiled modules in `numpy`, `cv2`, and `lxml`. This should greatly improve usability when working with these libraries.
    ([pylance-release#138](https://github.com/microsoft/pylance-release/issues/138), [pylance-release#150](https://github.com/microsoft/pylance-release/issues/150), [pylance-release#392](https://github.com/microsoft/pylance-release/issues/392))
-   Pylance now offers an insiders program, which provides access to prerelease builds and features. Setting `"pylance.insidersChannel": "daily"` will check daily for updates.
-   `__future__` is now properly suggested as an import.
    ([pylance-release#539](https://github.com/microsoft/pylance-release/issues/539))
-   Type aliases are now properly expanded in completion tooltips.
    ([pylance-release#562](https://github.com/microsoft/pylance-release/issues/562))

In addition, Pylance's copy of Pyright has been updated from 1.1.85 to 1.1.86, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug with type annotations that use a TypeVar with the new union syntax.
    -   Behavior Change: Removed special-case code that eliminates a NoReturn from an async function.
    -   Behavior Change: Changed behavior of NoReturn when it appears within unions. Previously, it was always filtered out of unions. It is now filtered out only in the inferred return type of a function. This allows NoReturn to be used in unions in other legitimate cases.
    -   Bug Fix: Fixed bug that resulted in a false negative when a callable type with a kwargs parameter was assigned to a callable type without a kwargs or with a kwargs of a different type.
-   [1.1.86](https://github.com/microsoft/pyright/releases/tag/1.1.86)
    -   Enhancement (from Pylance): Improvements to completion provider and signature help provider.
    -   Bug Fix: Allow `TypeAlias` to be used prior to Python 3.10 if imported from typing_extensions.
    -   Enhancement: Added special-case handling for magic method `__class_getitem__`, which is implicitly a classmethod.
    -   Enhancement: Added support for classes that include the `__class_getitem__` magic method to provide custom behaviors for subscripting.
    -   Enhancement: Support detecting multiple site-packages directories in venvs. [Contribution by Truls Asheim]
    -   Bug Fix: Fixed bug that caused incorrect type errors when dealing with magic methods on the tuple class.
    -   Bug Fix: Fixed a confusing diagnostic message relating to incorrect method override.
    -   Enhancement: Enforced that TypeVars being solved for in a TypeVar map match the expected scope.
    -   Bug Fix: Fixed bug in synthesized `setdefault` method on TypedDict for required entries, which never use the default value.
    -   Bug Fix: Fixed bug that resulted in an inappropriate error when a kwarg parameter was typed with a class-defined TypeVar (e.g. `**kwargs: _VT`).
    -   Bug Fix: Made the check less strict for the use of covariant type vars within a function input parameter annotation. In particular, unions that contain covariant type vars are now permitted.
    -   Enhancement: Add `__future__` module as import suggestion. [Contribution by cdce8p]
        ([pylance-release#539](https://github.com/microsoft/pylance-release/issues/539))
    -   Bug Fix: Fixed bug that caused the issubtype type narrowing logic to fail when used with a bound TypeVar T in combination with `Type[T]`.
    -   Bug Fix: Don't add suggestions for 'with Y as [ ]'. [Contribution by cdce8p]
    -   Enhancement: Type aliases are now expanded in completion provider text in the same way as the hover text. [Contribution by cdce8p]
        ([pylance-release#562](https://github.com/microsoft/pylance-release/issues/562))
    -   Enhancement: Improve handling of type aliases for auto-import. [Contribution by cdce8p]
        ([pylance-release#606](https://github.com/microsoft/pylance-release/issues/606))

## 2020.11.1 (11 November 2020)

Notable changes:

-   Completions will no longer be offered in contexts where a new name is being typed, including class names, function names, parameter names, and import alias names. This also has the effect of hiding undesirable auto-import completions for test fixtures.
    ([pylance-release#163](https://github.com/microsoft/pylance-release/issues/163))
-   Completions will no longer incorrectly be offered inside of string literals.
    ([pylance-release#383](https://github.com/microsoft/pylance-release/issues/383))
-   Docstring formatting in signature help tooltips will now match hover and completion tooltips.
    ([pylance-release#566](https://github.com/microsoft/pylance-release/issues/566))
-   Tokens that come from the builtins now have a "builtin" semantic modifier for theming.
    ([pylance-release#561](https://github.com/microsoft/pylance-release/issues/561))
-   The "make Pylance your default language server" prompt will now hide permanently if "no" is selected.
    ([pylance-release#568](https://github.com/microsoft/pylance-release/issues/568))
-   The pandas stubs have been updated.
    ([pylance-release#576](https://github.com/microsoft/pylance-release/issues/576))
-   Pylance's copy of typeshed has been updated.

In addition, Pylance's copy of Pyright has been updated from 1.1.83 to 1.1.85, including the following changes:

-   [1.1.85](https://github.com/microsoft/pyright/releases/tag/1.1.85)
    -   Behavior Change: Changed diagnostic about first argument to `super` call to be part of the reportGeneralTypeIssues diagnostic rule so it is suppressed when type checking mode is set to "off".
        ([pylance-release#589](https://github.com/microsoft/pylance-release/issues/589))
    -   Bug Fix: Fixed bug that caused code within finally clause to be marked as unreachable if there was no except clause and the code within the try block always raised an exception.
        ([pylance-release#592](https://github.com/microsoft/pylance-release/issues/592))
    -   Bug Fix: Fixed bugs in ParamSpec logic. It was not properly handling the case where the target callable type contained keyword-only or positional-only parameter separators.
    -   Bug Fix: Added support for `tuple` and `type` subscripts when `__future__` annotations is defined.
    -   Bug Fix: Fixed bug that caused improper errors when using new-style union syntax with `from __future__ import annotations`.
    -   Bug Fix: Worked around a reported bug in node 14+ on Linux where calls to fs.watch throw an exception when creating a recursive file watcher. The workaround is to catch the exception and proceed without a file watcher in place.
    -   Enhancement: Updated typeshed stubs to the latest.
-   [1.1.84](https://github.com/microsoft/pyright/releases/tag/1.1.84)
    -   Bug Fix: Fixed parser crash when an f-string contained an empty expression.
    -   Bug Fix: Fixed bug that caused diagnostics with "information" severity to be reported as "warnings" in the CLI version of pyright.
    -   Bug Fix: Fixed recent regression in handling type evaluations for "and" and "or" operators. Short-circuiting evaluation was not handled correctly in some cases.
    -   Bug Fix: Fixed bug in parser that caused expressions within f-strings to be handled incorrectly if they contained syntax errors.
    -   Bug Fix: Fixed bug in parsing of annotated variable assignments. It was not allowing yield expressions on the right-hand side.
    -   Enhancement: Added special-case logic to handle `isinstance` call when the first argument is a TypedDict and the second argument is a `dict` class. A TypedDict does not derive from `dict` from the perspective of type checking, but at runtime, `isinstance` returns True. This affects both type narrowing logic and checks for unnecessary `isinstance` calls.
    -   Bug Fix: Fixed bug in type narrowing logic for expressions of the form "type(x) is y" or "type(x) is not y". The logic was incorrectly narrowing the type in the negative ("else") case. And in the positive case, it was not properly handling cases where x was a subclass of y.
        ([pylance-release#572](https://github.com/microsoft/pylance-release/issues/572))
    -   Bug Fix: Fixed bug that caused completion suggestions to be presented when typing a period within a comment on the first line of the file.
    -   Enhancement: Improved signature help for data classes where default values are specified.
        ([pylance-release#585](https://github.com/microsoft/pylance-release/issues/585))
    -   Bug Fix: Fixed bug in NamedTuple logic that caused spurious errors when attempting to assign a NamedTuple to a Tuple with a compatible set of type arguments.

## 2020.11.0 (4 November 2020)

Notable changes:

-   Common module aliases (such as `np`, `pd`, `plt`) are now available as completions, in addition to being suggested in quick fixes.
-   Completions on lines containing the character `#` will now work correctly.
    ([pylance-release#461](https://github.com/microsoft/pylance-release/issues/461))
-   Completions for functions in import statements will no longer incorrectly add parentheses when `completeFunctionParens` is enabled.
    ([pylance-release#320](https://github.com/microsoft/pylance-release/issues/320))
-   The bundled Django stubs have been updated to the latest version.
    ([pylance-release#212](https://github.com/microsoft/pylance-release/issues/212))
-   Empty f-string expressions are now parsed correctly.

In addition, Pylance's copy of Pyright has been updated from 1.1.82 to 1.1.83, including the following changes:

-   [1.1.83](https://github.com/microsoft/pyright/releases/tag/1.1.83)
    -   Bug Fix: Fixed bug in perf optimization for set, list, and dictionary type inference. The old code was failing to evaluate expressions associated with entries beyond 64, which meant that tokens were not classified correctly and type errors in these expressions were not reported.
    -   Bug Fix: Do not report errors for union alternative syntax (PEP 604) if evaluation of type annotation is postponed (either in a quote or via PEP 563).
    -   Bug Fix: Fixed bug that caused spurious errors when evaluating type annotations within certain circumstances.
        ([pylance-release#513](https://github.com/microsoft/pylance-release/issues/513))
    -   Bug Fix: Fixed bug that sporadically caused incorrect and confusing type errors such as "list is incompatible with List".
        ([pylance-release#521](https://github.com/microsoft/pylance-release/issues/521))
    -   Bug Fix: PEP 585 says that it should be possible to use `type` in place of `Type` within type annotations. Previously, this generated an error.
    -   Behavior Change: Changed re-export logic for type stub and py.typed modules to honor the clarification that was recently added to PEP 484. Previously, any import that used an "as" clause was considered to be re-exported. Now, symbols are re-exported only if the "as" clause is redundant (i.e. it is of the form `import A as A` or `from A import X as X`).
    -   Bug Fix: Fixed inconsistency in handling of imported symbols that have multiple untyped declarations within the target module. The inconsistency was between the two cases `import x, x.y` and `from x import y`. In the latter case the type resolution logic considered only the last symbol declaration in the target module, but in the former case it was considering all declarations and returning the union of all types.
        ([pylance-release#545](https://github.com/microsoft/pylance-release/issues/545))
    -   Bug Fix: Fixed bug in f-string parsing. It was generating an error for comma-separate list of expressions, which is legal.
        ([pylance-release#551](https://github.com/microsoft/pylance-release/issues/551))
    -   Bug Fix: Fixed inconsistency in type narrowing for `isinstance` and `issubclass` calls. Previously, the narrowing logic used the target class(es) if the source expression was of type Any but did not do the same when the source expression was a union type that included Any but all other subtypes were eliminated.
        ([pylance-release#557](https://github.com/microsoft/pylance-release/issues/557))
    -   Bug Fix: Added logic for `or` and `and` operators to handle the case where the left-hand operand is always falsy (in the case of `or`) or always truthy (in the case of `and`).

## 2020.10.3 (28 October 2020)

Notable changes:

-   Performance while in the "off" type checking mode has been improved (the default for Pylance).
-   A performance regression related to the experimental `TypeGuard` type has been fixed, which should further improve overall performance.
-   The bundled Django stubs have been updated to the latest version.
    ([pylance-release#536](https://github.com/microsoft/pylance-release/issues/536))

In addition, Pylance's copy of Pyright has been updated from 1.1.81 to 1.1.82, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Do not report errors for union alternative syntax (PEP 604) if evaluation of type annotation is postponed (either in a quote or via PEP 563).
        ([pylance-release#513](https://github.com/microsoft/pylance-release/issues/513))
    -   Bug Fix: Fixed bug in perf optimization for set, list, and dictionary type inference. The old code was failing to evaluate expressions associated with entries beyond 64, which meant that tokens were not classified correctly and type errors in these expressions were not reported.
        ([pylance-release#518](https://github.com/microsoft/pylance-release/issues/518))
-   [1.1.82](https://github.com/microsoft/pyright/releases/tag/1.1.82)
    -   Bug Fix: Fixed internal error that occurs when the type evaluator encounters a circular dependency between a class decorator and the class that it decorates.
    -   Bug Fix: Fixed bug in protocol matching logic that results in incorrect errors indicating a function type mismatch.
    -   Perf Improvement: Conditionalized the logic for the reportPropertyTypeMismatch diagnostic check. It's somewhat expensive, so don't bother executing it if it's disabled.
    -   Perf Improvement: Fixed performance regression introduced along with user-defined type guards.
    -   Enhancement: Added support for reverse logical operators (`__ror__`, `__rand__`, etc.).
    -   Bug Fix: Added code to handle the case where a class has a custom metaclass that handles logical or (the `__or__` method). Previous to this change, use of an `|` operator with classes was assumed to be a misuse of PEP 614 in Python versions prior to 3.10.
        ([pylance-release#513](https://github.com/microsoft/pylance-release/issues/513))
    -   Bug Fix: Fixed bug that resulted in an incorrect error when a list comprehension expression was used within a lambda and the expression referenced one or more of the lambda parameters.
        ([pylance-release#520](https://github.com/microsoft/pylance-release/issues/520))
    -   Bug Fix: Fixed bug that caused incorrect error to be reported for names referenced in global and nonlocal statements when those names were not declared in the outer scope.
        ([pylance-release#526](https://github.com/microsoft/pylance-release/issues/526))
        Bug Fix: Fixed bug that resulted in incorrect error when second argument of isinstance was a "type" or "Type" object.

## 2020.10.2 (21 October 2020)

Notable changes:

-   Incremental text changes are now supported, which should improve performance when editing large files.
-   Invalid diagnostics should no longer appear when semantic highlighting is enabled.
    ([pylance-release#491](https://github.com/microsoft/pylance-release/issues/491))

In addition, Pylance's copy of Pyright has been updated from 1.1.79 to 1.1.81, including the following changes:

-   [1.1.81](https://github.com/microsoft/pyright/releases/tag/1.1.81)
    -   Bug Fix: Fixed bug in parser that caused incorrect errors in chains of comparison or "in"/"not in" operators. The expression "a == b == c" should be parsed as "a == (b == c)", but the code was previously parsing it as "(a == b) == c". This didn't matter in most cases, but it does when the types of a, b and c differ.
        ([pylance-release#506](https://github.com/microsoft/pylance-release/issues/506))
    -   Bug Fix: Fixed bug that resulted in incorrect errors when an instance variable with no type declaration was assigned an enum value. It was assumed to be of that literal enum value type rather than the wider enum type.
    -   Bug Fix: Fixed bug that resulted in false positive error when a class derived from another class that was instantiated from a custom metaclass.
        ([pylance-release#507](https://github.com/microsoft/pylance-release/issues/507))
    -   Bug Fix: Fixed bug that caused type errors when internal type cache was cleared. The code previously used parse node IDs to distinguish between types that are not created via class declarations (NamedTuple, type, NewType, etc.). Since node IDs change when a file is reparsed (due to a change), these IDs cannot be relied upon for type comparisons.
    -   Enhancement: Added support for "typing" module aliases when checking for TYPE_CHECKING symbol in static boolean expressions.
-   [1.1.80](https://github.com/microsoft/pyright/releases/tag/1.1.80)
    -   Bug Fix: Fixed bug that caused an incorrect error when `self.__class__` was used as the second argument to an `isinstance` call.
    -   Bug Fix: Changed logic for function return type inference so "unbound" type is never propagated to callers. This eliminates incorrect and confusing errors.
    -   Bug Fix: Fixed bug in type stub generator. It was not properly handling annotated variables (either those with PEP 593 annotations or older-style type comment annotations).
        ([pylance-release#490](https://github.com/microsoft/pylance-release/issues/490))
    -   Bug Fix: Fixed bug in completion provider that caused submodules within a namespace module not to be suggested within a "from x import y" statement.
        ([pylance-release#359](https://github.com/microsoft/pylance-release/issues/359))
    -   Bug Fix: Fixed misleading error message within "from x import y" statement where x was a namespace package and y was not found. The error was being reported as an "unresolved import x" rather than "unknown symbol y".
    -   Bug Fix: Fixed bug in type evaluator that caused spurious errors related to variables used within "for" and "if" statements within a comprehension.
    -   Bug Fix: Fixed bug that caused incorrect error to be reported when a recursive type alias was used in certain circumstances.
    -   Enhancement: Improved type inference for tuples in circumstances where literals are used within a tuple expression and when tuple expressions are assigned to an expected type that is not a tuple but is a compatible type (such as Iterable).
        ([pylance-release#487](https://github.com/microsoft/pylance-release/issues/487))
    -   Bug Fix: Fixed bug that resulted in incorrect error about TypeVar being used incorrectly. The specific condition was when it was referenced within a method within a generic class and one of the method's parameters also referenced the same TypeVar.
    -   Bug Fix: Fixed bug where declared variable with literal types in type arguments were being stripped of those literals when the variable was exported from a module.
    -   Bug Fix: Fixed bug that caused duplicate error messages involving certain TypeVar assignments.
    -   Enhancement: Added diagnostic check for dictionary unpack operator (\*\*) if the operand is not a mapping object.
    -   Enhancement (from Pylance): Added support for increment text changes in language server interface. This will theoretically improve performance for edits in large source files.

## 2020.10.1 (14 October 2020)

Notable changes:

-   The `pandas` stubs have been further improved.
    ([pylance-release#457](https://github.com/microsoft/pylance-release/issues/457))
-   Semantic tokens will now be refreshed on settings change.
-   Completions for function parameters will no longer incorrectly appear outside call parenthesis.

In addition, Pylance's copy of Pyright has been updated from 1.1.78 to 1.1.79, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug that caused an incorrect error when `self.__class__` was used as the second argument to an `isinstance` call.
    -   Bug Fix: Changed logic for function return type inference so "unbound" type is never propagated to callers. This eliminates incorrect and confusing errors.
        ([pylance-release#488](https://github.com/microsoft/pylance-release/issues/488))
-   [1.1.79](https://github.com/microsoft/pyright/releases/tag/1.1.79)
    -   Bug Fix: Fixed the handling of backslashes within an f-string that is also raw.
    -   Enhancement: Added streaming support for "find all references" so updates appear incrementally.
    -   Enhancement: Improved some internal type transforms to preserve type alias information where possible. This helps types be more readable in hover text and error messages.
    -   Bug Fix: Fixed bug that caused identifiers with non-ASCII characters to sometimes be handled incorrectly.
        ([pylance-release#466](https://github.com/microsoft/pylance-release/issues/466))
    -   Bug Fix: Fixed bug that resulted in an incorrect "unbound variable" error when the variable was used in an assignment expression within an if/else conditional expression.
        ([pylance-release#468](https://github.com/microsoft/pylance-release/issues/468))
    -   Bug Fix: Fixed bug where implementation of an overloaded function was included in the list of overloads leading to incorrect signature suggestions and false positives for various overload diagnostic checks.
    -   Enhancement: Updated typeshed to latest.
    -   Bug Fix: Added missing descriptor for "python.analysis.extraPaths" in Pyright VS Code extension. This caused VS Code to indicate that this setting wasn't known.
    -   Bug Fix: Fixed bugs in import resolver when a project contains multiple namespace packages with the same name.
        ([pylance-release#471](https://github.com/microsoft/pylance-release/issues/471))
    -   Bug Fix: Fixed bug that resulted in "unknown" parameter type when assigning a lambda to a variable with a declared Callable type.
    -   Bug Fix: Fixed issue with call signature arguments.
    -   Enhancement: Added support for plain text doc strings.
    -   Bug Fix: Fixed bug that caused a type variable to be "unknown" in some cases where a generic class type was used without providing explicit type arguments.
    -   Bug Fix: Fixed handling of "Annotated" type introduced in PEP 593. Wasn't properly handling string literals in type arguments.
        ([pylance-release#479](https://github.com/microsoft/pylance-release/issues/479))

## 2020.10.0 (7 October 2020)

Notable changes:

-   Indexing performance has been improved. The indexer is still disabled by default, but we'd appreciate feedback about its behavior. Indexing can be enabled by setting `"python.analysis.indexing": true`.
-   The `pandas` stubs have been further improved.
    ([pylance-release#426](https://github.com/microsoft/pylance-release/issues/426), [pylance-release#427](https://github.com/microsoft/pylance-release/issues/427), [pylance-release#428](https://github.com/microsoft/pylance-release/issues/428), [pylance-release#436](https://github.com/microsoft/pylance-release/issues/436), [pylance-release#444](https://github.com/microsoft/pylance-release/issues/444), [pylance-release#448](https://github.com/microsoft/pylance-release/issues/448), [pylance-release#449](https://github.com/microsoft/pylance-release/issues/449), [pylance-release#457](https://github.com/microsoft/pylance-release/issues/457))
-   Semantic token scopes for some type hints have been fixed.
    ([pylance-release#459](https://github.com/microsoft/pylance-release/issues/459))
-   Type aliases should now be more consistently used in tooltips.
    ([pylance-release#301](https://github.com/microsoft/pylance-release/issues/301))
-   Python 3.9's more permissive decorator syntax is now supported.
-   Recursive type aliases are now supported.
-   Experimental support for a new proposed `typing` extension "TypeGuard" has been added. This extension allows for the creation of user-defined type guards.

In addition, Pylance's copy of Pyright has been updated from 1.1.75 to 1.1.78, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed the handling of backslashes within an f-string that is also raw.
    -   Enhancement: Improved some internal type transforms to preserve type alias information where possible. This helps types be more readable in hover text and error messages.
        ([pylance-release#301](https://github.com/microsoft/pylance-release/issues/301))
-   [1.1.78](https://github.com/microsoft/pyright/releases/tag/1.1.78)
    -   Bug Fix: Fixed regression were diagnostics reported for constructor argument expressions were being suppressed.
    -   Bug Fix: Fixed bug that was causing "self is unknown type" errors in strict mode for "self" parameters used within a protocol class.
        ([pylance-release#458](https://github.com/microsoft/pylance-release/issues/458))
    -   Enhancement: Added support for arbitrary expressions in decorators for Python 3.9 and newer as specified in PEP 614.
    -   Enhancement: Implemented provisional "TypeGuard" functionality that allows for user-defined type guard functions. This must still go through a spec'ing and ratification process before it is finalized. Until then, details could change.
    -   Enhancement: Added diagnostic messages for incorrect use of contravariant type variable as a method return type or a covariant type variable as a method parameter.
    -   Bug Fix: Added missing comparison operator methods (`__eq__`, `__lt__`, etc.) for dataclass.
-   [1.1.77](https://github.com/microsoft/pyright/releases/tag/1.1.77)
    -   Bug Fix: Fixed bug where float and complex values were being inferred as Literal types when PEP 586 clearly states that complex and float values are not supported for Literal.
    -   Bug Fix: Fixed spurious "variable is unbound" error when symbol was used in a compound conditional expression where the first part of the expression was statically determined to short-circuit the evaluation (e.g. `if False and name:`).
        ([pylance-release#452](https://github.com/microsoft/pylance-release/issues/452))
    -   Bug Fix: Fixed regression relating to bidirectional type inference used for constructor calls.
    -   Bug Fix: Fixed bug that caused an internal error (stack overflow) when analyzing types of symbols that mutually depend upon each other and are potentially (but turn out not to be) type aliases.
    -   Bug Fix: Improved handling of constrained type variables where one of the constraints is a narrower version of another.
        ([pylance-release#453](https://github.com/microsoft/pylance-release/issues/453))
    -   Bug Fix: Eliminated spurious "cannot instantiate abstract class" error when the value being instantiated is typed as `Type[X]`. Even though `X` is abstract, this shouldn't generate an error because `Type[X]` means "any subclass of `X`".
    -   Bug Fix: Fixed handling of bidirectional type inference when source is an expression involving an "and" or "or" binary operator.
    -   Enhancement: Changed type printing logic to include the name of a module for module types for clarity. Rather than 'Module', it now prints 'Module("&lt;name&gt;")'. This string is used in hover text and diagnostic messages.
    -   Bug Fix: Fixed bug in hover provider where it incorrectly labeled variables as "type alias" if they are instantiated from a type alias.
    -   Bug Fix: Fixed bug that caused type narrowing for assignments not to be applied when the source of the assignment was a call to a constructor.
    -   Enhancement: Improved type narrowing for assignments when destination is declared with one or more "Any" type arguments.
    -   Enhancement: Improved bidirectional type inference for list and dict types when destination type is a union that contains one or more specialized list or dict types.
    -   Enhancement: Improved support for generic recursive type aliases. Improved bidirectional type inference for list and dict types when destination type is a wider protocol type (like Iterable, Mapping, Sequence, etc.).
    -   Bug Fix: Added escapes in docstring markdown converter for "<" and ">" characters so they are not interpreted as an HTML tag by the markdown renderer.
-   [1.1.76](https://github.com/microsoft/pyright/releases/tag/1.1.76)
    -   Bug Fix: Fixed spurious error when "Literal" was used with a dynamic type argument in a place where a type annotation wasn't expected.
    -   Enhancement: Improved type verification report for readability.
    -   Bug Fix: Fixed bug where Enum constructor was not handling some variations of parameter types.
    -   Bug Fix: Fix handling of pythonPath setting when it is unset.
    -   Enhancement: Improved logging for import search paths.
    -   Enhancement: Improved experience for auto-import completions by including "Auto-import" in details.
    -   Enhancement: Added optimizations in type validator to avoid checking built-in classes.
    -   Enhancement: Added checks in type validator for metaclasses.
    -   Bug Fix: Improved handling of bidirectional type inference when RHS of assignment is a constructor.
    -   Bug Fix: Added support for `__all__` assignments that include a type annotation. Added support for the `__all__ += <module>.__all__` idiom for mutating the `__all__` value. This idiom is used by numpy.
    -   Bug Fix: Fixed bug that caused symbols referenced by `__all__` not to be marked as accessed in some cases.
        ([pylance-release#446](https://github.com/microsoft/pylance-release/issues/446))
    -   Enhancement: Added diagnostic check for static and class methods used for property getters, setters and deleters.

## 2020.9.8 (2 October 2020)

This is a hotfix release, fixing a regression in 2020.9.7 that caused some `numpy` members (such as `numpy.nan`) to be missing.

## 2020.9.7 (30 September 2020)

Notable changes:

-   The `pandas` stubs have been further improved.
    ([pylance-release#386](https://github.com/microsoft/pylance-release/issues/386), [pylance-release#399](https://github.com/microsoft/pylance-release/issues/399), [pylance-release#405](https://github.com/microsoft/pylance-release/issues/405), [pylance-release#411](https://github.com/microsoft/pylance-release/issues/411), [pylance-release#412](https://github.com/microsoft/pylance-release/issues/412))
-   Imports of the form `from X import Y as Z` and dead code blocks will no longer have spurious errors with semantic highlighting enabled.
    ([pylance-release#376](https://github.com/microsoft/pylance-release/issues/376), [pylance-release#401](https://github.com/microsoft/pylance-release/issues/406))
-   Decorators and declarations now have additional semantic token modifiers for further customization.
    ([pylance-release#401](https://github.com/microsoft/pylance-release/issues/401))
-   Temporary folder creation on multi-user shared systems has been fixed.
    ([pylance-release#421](https://github.com/microsoft/pylance-release/issues/421))
-   Auto-import completions will now show "Auto-import" in the completion list when the tooltip hasn't been expanded.
-   Fixed a regression in the configuration of some paths, which may have prevented the correct python interpreter from being selected.

In addition, Pylance's copy of Pyright has been updated from 1.1.74 to 1.1.75, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug where Enum constructor was not handling some variations of parameter types.
    -   Bug Fix: Fixed spurious error when "Literal" was used with a dynamic type argument in a place where a type annotation wasn't expected.
-   [1.1.75](https://github.com/microsoft/pyright/releases/tag/1.1.75)
    -   Bug Fix: Fixed bug that caused some source files that were part of a "py.typed" package to not be identified as such. This meant that the special rules for "py.typed" exports were not being applied in those cases.
    -   Enhancement: Updated typeshed stubs to the latest.
    -   Behavior Change: Added special-case handling of values within enum classes in a py.typed package. They should be treated as constants and not require type annotations.
    -   Behavior Change: Improved detection of implicit type aliases.
    -   Bug Fix: Fixed bug that caused incorrect error in case where bidirectional type inference was used with a list expression and the expected type was an empty protocol.
        ([pylance-release#409](https://github.com/microsoft/pylance-release/issues/409))
    -   Bug Fix: Fixed a bug where spurious errors were generated when using an unannotated "self" as an argument to a constructor in a generic class.
        ([pylance-release#423](https://github.com/microsoft/pylance-release/issues/423))
    -   Enhancement: Added type narrowing for expressions of the form `<string> in X` and `<string> not in X` where X is a union of TypedDict instances.
    -   Bug Fix: Fixed several bugs related to recursive type aliases. The hover text was sometimes incorrect, type narrowing for "isinstance" was broken in some cases, and the reportUnnecessaryIsInstance rule was reporting incorrect errors.
    -   Bug Fix: Fixed bug in code that prints function types that contain a "named-parameter separator" (`_`). It was emitting an extra slash (`_/`).
    -   Enhancement: Added check for position-only argument separator ("/") appearing as the first parameter in a parameter list. This is a syntax error.
    -   Bug Fix: Fixed incorrect handling of global name bindings when a same-named nonlocal name was present.
        ([pylance-release#429](https://github.com/microsoft/pylance-release/issues/429))
    -   Enhancement: Expanded support for idioms used in libraries to define `__all__`. Tuples are now supported, as are calls to `expand`, `append` and `remove`.
    -   Bug Fix: Fixed bug with synthesized `__set__` and `__del__` property methods. The wrong parameter types were being specified for the 'self' and 'obj' parameters.
    -   Bug Fix: Fixed bug in diagnostics reporting logic that caused stack overflow in some rare cases.
    -   Bug Fix: Fixed bug in `callable` type narrowing logic where the union of the type includes `None`.
    -   Bug Fix: Improved handling of bidirectional type inference for constructor calls on generic types. In particular, the new logic better handles the case where the expected type is a union.
    -   Bug Fix: Fixed bug in type inference for generator types. It was not properly adding the three type arguments for Generator in the inferred return type.
        ([pylance-release#431](https://github.com/microsoft/pylance-release/issues/431))
    -   Behavior Change: Implemented new rules for reexports within a py.typed module. ".py" files now follow PEP 484 rules with an override based on `__all__`.
    -   New Feature: Implemented new "verifytypes" command-line option that analyzes a py.typed package and reports missing or partially-unknown types.
    -   Enhancement: Added limiter for list type inference to clip the number of unique subtypes and avoid poor performance in some cases.

## 2020.9.6 (23 September 2020)

Notable changes:

-   Docstrings for the builtins are now supported. You should now see docstrings in tooltips for functions like `print`, `range`, `open`, `str.split`, types like `int`, `float`, `str`, `Exception`, and more.
    ([pylance-release#49](https://github.com/microsoft/pylance-release/issues/49))
-   Semantic highlighting has been expanded to provide more token types and modifiers. Special tokens such as `self` and `cls`, constants, dunder methods, and type hints in comment will be styled similarly to VS Code's built-in regex-based highlighting.
    ([pylance-release#323](https://github.com/microsoft/pylance-release/issues/323), [pylance-release#335](https://github.com/microsoft/pylance-release/issues/335))
-   String literals are no longer highlighted when hovered or containing a cursor.
    ([pylance-release#172](https://github.com/microsoft/pylance-release/issues/172))
-   Relative paths provided settings like `extraPaths` and `stubPath` will now correctly be resolved relative to the workspace.
    ([pylance-release#326](https://github.com/microsoft/pylance-release/issues/326))
-   When hovering on a class invocation and the `__init__` method does not have a docstring, the class's docstring will be displayed instead.
    ([pylance-release#316](https://github.com/microsoft/pylance-release/issues/316))
-   The `pandas` stubs have been further improved.
    ([pylance-release#385](https://github.com/microsoft/pylance-release/issues/385), [pylance-release#387](https://github.com/microsoft/pylance-release/issues/387), [pylance-release#389](https://github.com/microsoft/pylance-release/issues/389), [pylance-release#390](https://github.com/microsoft/pylance-release/issues/390), [pylance-release#391](https://github.com/microsoft/pylance-release/issues/391), [pylance-release#393](https://github.com/microsoft/pylance-release/issues/393))

In addition, Pylance's copy of Pyright has been updated from 1.1.72 to 1.1.74, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Fixed bug that caused some source files that were part of a "py.typed" package to not be identified as such. This meant that the special rules for "py.typed" exports were not being applied in those cases.
-   [1.1.74](https://github.com/microsoft/pyright/releases/tag/1.1.74)
    -   Bug Fix: Fixed bug that caused some type aliases defined in ".py" files within a py.typed package to be treated as unknown.
    -   Bug Fix: Fixed bug relating to member access expressions used in the LHS of an assignment where the inferred type of the member is an object that does not provide a `__set__` method. This should generate an error, and it was not.
    -   Bug Fix: Fixed bug in completion provider that sometimes resulted in detailed completion information not to be displayed. The provider was making use of an internal "symbol ID" to resolve symbol information lazily when the item was selected from the completion menu, but the symbol ID was not guaranteed to be the same from one call to the next.
        ([pylance-release#382](https://github.com/microsoft/pylance-release/issues/382))
    -   Bug Fix: Fixed a bug where an overloaded function could not be assigned to the type 'object' without generating an error. This should be allowed.
    -   Bug Fix: Fixed bug with the invocation of the `__get__` method. It was not being bound to the correct object when called, resulting in incorrect type variable resolution if the "self" parameter was annotated with a TypeVar.
    -   Behavior Change: Eliminated string literal highlighting within document highlight provider. We received significant user feedback that this was not desirable.
        ([pylance-release#172](https://github.com/microsoft/pylance-release/issues/172))
    -   Bug Fix: Fixed bug in handling the two-argument form of "super". The type evaluator was not properly honoring the second argument, which specifies the class or object that should be use for binding.
        ([pylance-release#395](https://github.com/microsoft/pylance-release/issues/395))
    -   Performance Improvement: Changed the logic that infers the type of a list, set, or dict to look at only the first 64 entries. There were cases where thousands of entries were provided in list and dict statements, and this resulted in very poor performance. In practice, looking at the first 64 entries as part of the inference heuristic is sufficient.
    -   Bug Fix: Fixed bug that caused a enums to be incorrectly reported as "not iterable" in cases where a generic `Type[Enum]` was used.
    -   Bug Fix: Fixed bug where type aliases that referred to literals would have those literal values stripped if the type alias was declared within a class.
    -   Bug Fix: Made the printing of literal types more consistent within error messages and hover text. If the type is an literal type (as opposed to a literal instance), it is now consistently printed as `Type[Literal[...]]`.
    -   Bug Fix: Fixed bug in the handling of overloaded magic methods associated with arithmetic operators. If no overload was found in the primary method (e.g. `__add__`), it was not properly falling back on the reverse method (e.g. `__radd__`).
    -   Bug Fix: Fixed bug that caused the type checker to indicate that None was not compatible with the Hashable protocol.
    -   Enhancement: Improved support for constrained TypeVars. The list of constrained types is now honored when providing completion suggestions and when narrowing types for isinstance/issubclass calls.
    -   Enhancement: Improved type checking for binary operations. Previously, if the right-hand operand was a union and at least one subtype was supported, no error was reported. The new implementation verifies that all subtypes are supported and emits an error if not.
    -   Bug Fix: Fixed bug that reported incorrect error when attempting to index a symbol whose type was annotated with `Type[enum]`.
    -   Enhancement: Improved reporting of errors for call expressions, especially in the case where the call type is a union and one or more subtypes are not callable.
    -   Bug Fix: Fixed a bug in the handling of wildcard imports when a dunder all symbol is present in the target and the dunder all array refers to an implicitly-imported submodule.
        ([pylance-release#402](https://github.com/microsoft/pylance-release/issues/402))
-   [1.1.73](https://github.com/microsoft/pyright/releases/tag/1.1.73)
    -   Behavior Change: Changed reveal_type to return a string literal that represents the printed version of the type.
    -   Behavior Change: Changed reveal_type to use an information diagnostic severity rather than warning. Added support in CLI for information diagnostic severity. These were previously dropped.
    -   Bug Fix: Tweaked the logic for py.typed type inference. Assignments that are type aliases should never be ignored in a py.typed package if they are defined in a pyi file.
    -   Bug Fix: Fixed bug in the parser relating to assignment expressions. It was not allowing for ternary expressions in the RHS.
        ([pylance-release#381](https://github.com/microsoft/pylance-release/issues/381))
    -   Bug Fix: Fixed a bug that caused an incorrect error to be reported when a callable type was assigned to an 'object'. This should be allowed.
    -   Bug Fix: Fixed bug in the completion provider where it was not properly handling object references through "self".
    -   Bug Fix: Fixed bug in the type checker with respect to member accesses where the LHS is a class and the RHS is a property. This should evaluate to a property object.

## 2020.9.5 (16 September 2020)

Notable changes:

-   The `pandas` stubs have been further improved.
    ([pylance-release#302](https://github.com/microsoft/pylance-release/issues/302), [pylance-release#303](https://github.com/microsoft/pylance-release/issues/303), [pylance-release#337](https://github.com/microsoft/pylance-release/issues/337))

In addition, Pylance's copy of Pyright has been updated from 1.1.70 to 1.1.72, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Tweaked the logic for py.typed type inference. Assignments that are type aliases should never be ignored in a py.typed package if they are defined in a pyi file.
    -   Behavior Change: Changed reveal_type to use an information diagnostic severity rather than warning. Added support in CLI for information diagnostic severity. These were previously dropped.
    -   Behavior Change: Changed reveal_type to return a string literal that represents the printed version of the type.
-   [1.1.72](https://github.com/microsoft/pyright/releases/tag/1.1.72)
    -   Bug Fix: Changed the type of `__path__` attribute for a module from `Iterable[str]` to `List[str]`.
    -   Bug Fix: Fixed a bug that caused a crash in the type checker in some rare cases when a function or class declaration was located within a block of code is unaccessible.
        ([pylance-release#369](https://github.com/microsoft/pylance-release/issues/369))
    -   Behavior Change: Changed python.analysis.logLevel to use "Information" rather than "Info" for consistency with Python extension.
    -   Bug Fix: Changed comment-style type annotations for functions to always allow forward declarations.
    -   Behavior Change: Added special-case logic for the `tuple` constructor. Rather than returning a type of `tuple[_T_co]`, it now returns a type of `tuple[_T_co, ...]`.
    -   Behavior Change: Changed behavior of type evaluator for modules within a "py.typed" package when "typeCheckingMode" is not "off". If it encounters an unannotated symbol, the type evaluator no longer attempts to infer its type. Instead, it returns an unknown type. When "typeCheckingMode" is "off" (the default value for Pylance), inference is still used.
    -   Enhancement: Improved reportMissingTypeArgument diagnostic rule to report cases where some type arguments are provided but some are missing. Previously, it detected only those cases where no type arguments were provided.
    -   Bug Fix: Fixed bug that caused incorrect error to be generated when a yield was used within a lambda.
        ([pylance-release#373](https://github.com/microsoft/pylance-release/issues/373))
-   [1.1.71](https://github.com/microsoft/pyright/releases/tag/1.1.71)
    -   Behavior Change: Added code to disable the Pyright extension when the Pylance extension is installed. The two extensions are not intended to work together.
    -   Bug Fix: Fixed bug in handling of specialized "tuple" class as defined in PEP 585.
    -   Behavior Change: Changed the behavior of the command-line version of pyright when file specs are passed on the command line. Previously, file specs couldn't be used in conjunction with a config file. Now a config file is used, but the specified file specs override the "include" section of the config file.
    -   Enhancement: Added validation of arguments passed to `__init_subclass__` method described in PEP 487.
    -   Enhancement: Added detection of duplicate base classes in a class declaration.
    -   Bug Fix: Fixed bug that generated incorrect "could not create consistent mro" error if one of the base classes was "Generic". The Python interpreter appears to special-case this class.
        ([pylance-release#361](https://github.com/microsoft/pylance-release/issues/361))
    -   New Feature: Added support for new "reportWildcardImportFromLibrary" diagnostic rule that checks for the use of wildcard imports from non-local modules. By default, it is reported as a warning, but in strict mode it is an error.
    -   Enhancement: Added code to synthesize custom overloaded "pop", "setdefault", and "\_\_delitem\_\_" methods for TypedDict classes.
    -   Enhancement: Added support for the direct instantiation of a metaclass rather than using the normal metaclass hook.
        ([pylance-release#360](https://github.com/microsoft/pylance-release/issues/360))

## 2020.9.4 (10 September 2020)

Notable changes:

-   Bug Fix: Addressing memory and cpu issues a number of users had by no longer indexing libraries and unopened files at startup. This will revert auto-import completions and workspace symbols performance to previous levels.
    ([pylance-release#321](https://github.com/microsoft/pylance-release/issues/321))

In addition, Pylance's copy of Pyright has been updated from 1.1.66 to 1.1.70, including the following changes:

-   [1.1.70](https://github.com/microsoft/pyright/releases/tag/1.1.70)
    -   Enhancement: Added support for PEP 585. Standard collection types defined in builtins can now be used like their typing counterparts. This includes "tuple", which needs special-case handling because its class definition in builtins.pyi indicates that it has a single type parameter, but it actually supports variadic parameters.
    -   Bug Fix: Added code to prevent heap overrun errors during parsing/binding, most notably during indexing operations.
    -   Bug Fix: Fixed bug that caused runtime crash if typeshed stubs couldn't be found or didn't define 'tuple'.
    -   Bug Fix: Improved interaction between recursive type aliases and bidirectional type inference for lists and dicts.
    -   Bug Fix: Improved type narrowing for assignments in cases where the destination of the assignment is declared as a union and the assigned type is a narrower form of one of the union elements. Previously, the narrowing logic didn't choose the narrowest type possible in this case.
    -   Enhancement: Added perf optimization for unions that contain hundreds or thousands of int literal values. This is similar to another recent optimization for str literal unions.
    -   From Pylance: Ensure that auto-import doesn't place import statement below usage.
-   [1.1.69](https://github.com/microsoft/pyright/releases/tag/1.1.69)
    -   Enhancement: Improved type analysis perf by about 5% and reduced memory usage slightly by not formatting and logging diagnostic messages in cases where they are suppressed (e.g. argument type mismatches when doing overload matching).
    -   Bug Fix: Fixed bug that affected dependency tracking of source files on platforms with case-insensitive file systems. In some cases, the case of paths differed, and the logic was treating these as separate files.
    -   Enhancement: Added diagnostics for type variables that are used improperly as defined in PEP 484: 1) conflicting type variables that are used in nested generic class declarations, and 2) type variables that are used within annotations outside of a context in which they have meaning.
    -   New Feature: Added support for "higher-order" type variables. You can now pass a generic function as an argument to another generic function, and the type var solver can solve the type variables for both at the same time.
    -   New Feature: Added support for recursive type aliases.
    -   Behavior Change: Updated the default Python version from 3.8 to 3.9. This is used only if it is not otherwise configured and there is no Python environment from which to determine the version.
    -   Enhancement: Added checks for usage of certain built-in types that are defined as generic in the typeshed stubs but generate runtime exceptions if subscripted on older versions of Python (prior to 3.9). Such types need to be enclosed in quotes when used in annotations.
-   [1.1.67](https://github.com/microsoft/pyright/releases/tag/1.1.67)
    -   Bug Fix: Fixed bug that caused the recently-added "discriminated field type narrowing" to be used in cases where it should not. This resulted in types being narrowed inappropriately when a field was typed as a union of literals.
    -   Behavior Change: Changed command-line version to not print any non-JSON output when "--outputjson" option is used.
    -   Behavior Change: Changed behavior when "useLibraryCodeForTypes" is set to "false". Previously, all ".py" library code was ignored in this case. Now, ".py" types are used for types if the package has an associated "py.typed" file as specified in PEP 561. Packages with no "py.typed" file will still be ignored if "useLibraryCodeForTypes" is "false".
    -   Bug Fix: Fixed a couple of bugs that resulted in the hover text incorrectly identifying a symbol as a "type alias".
    -   Behavior Change: Changed type inference logic to use "List", "Set", and "Dict" rather than "list", "set" and "dict" when inferring the type of a list, set or dict expression. These are aliases for the same underlying class, but the upper-case versions are more consistent with type annotations used within the code.
    -   Bug Fix: Fixed "NoReturn" inference logic for async functions. This logic was previously flagging the code after a call to such a function as unreachable.
    -   Enhancement: Improved parser to detect syntax errors involving unpack operator within a comprehension.
    -   Enhancement: Changed import resolution logic to allow binaries (e.g. ".so" files) to satisfy local imports (within the package), not just third-party imports (within site-packages).
    -   Enhancement: Extended bidirectional type inference (expected types) to list comprehensions.
    -   New Feature: Added new diagnostic rule "reportPropertyTypeMismatch" that verifies that the type of the input parameter to a property's setter is assignable to the return type of the getter.
    -   Bug Fix: Fixed bug that caused a crash in the type checker in cases where type arguments were not provided to a few special-case built-in classes.
    -   Bug Fix: Fixed a bug in the handling of generics that involve constrained TypeVars. The TypeVar matching logic was sometimes inappropriately specializing the type using the first constrained type.
    -   Bug Fix: Added special-case handling in type checker for callers who request the type of an expression that happens to be a name used in a call expression to designate a named parameter. This isn't really an expression, so the code wasn't handling it correctly, but callers (such as the hover provider and the new semantic token provider) were assuming that it was safe. This resulted in incorrect "X is not defined" diagnostics being logged.

## 2020.9.0 (3 September 2020)

Notable changes:

-   Pylance now supports semantic highlighting. In order to enable this feature, you must be using at least version 2020.8.106424 of the Python extension, as well as a VS Code theme which includes semantic colorization support (e.g., Dark+, Light+, One Dark Pro, others).
    ([pylance-release#220](https://github.com/microsoft/pylance-release/issues/220))
-   Pylance will now index libraries and unopened files at startup to provide auto-import completions even for variables that have not been fully analyzed. This index is also used to improve the performance of the workspace symbols search.
-   The auto-import completions offered should now more accurately reflect the "intended" import, rather than suggesting importing deeper modules. This helps improve the behavior in libraries that re-export symbols through other modules.
    ([pylance-release#222](https://github.com/microsoft/pylance-release/issues/222), [pylance-release#139](https://github.com/microsoft/pylance-release/issues/139), [pylance-release#28](https://github.com/microsoft/pylance-release/issues/28), [pylance-release#97](https://github.com/microsoft/pylance-release/issues/97))
-   The auto-import completion tooltip now more clearly states what will be added to your import block. For example, a completion for "join" will explicitly say `from os.path import join`, rather than just "Auto-import from os.path".
-   When the `completeFunctionParens` feature is enabled, the signature help will now open automatically, matching the behavior when the parentheses are user-written.
    ([pylance-release#273](https://github.com/microsoft/pylance-release/issues/273))
-   Pylance now includes schemas for `pyrightconfig.json`/`mspythonconfig.json`, which enables code completion and validation for these config files.
    ([pylance-release#40](https://github.com/microsoft/pylance-release/issues/40))
-   Methods which only raise `NotImplementedError` will now be treated as abstract and not be marked as not returning, preventing some child class functions from being spuriously marked as dead code. Explicitly declaring classes and methods as abstract is still strongly preferred as it allows the type checker to more accurately check child classes for correctness.
    ([pylance-release#248](https://github.com/microsoft/pylance-release/issues/248))
-   The default `stubPath` now correctly shows in the VS Code settings UI with its default "typings".
    ([pylance-release#285](https://github.com/microsoft/pylance-release/issues/285))

In addition, Pylance's copy of Pyright has been updated from 1.1.65 to 1.1.66, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug that caused the recently-added "discriminated field type narrowing" to be used in cases where it should not. This resulted in types being narrowed inappropriately when a field was typed as a union of literals.
-   [1.1.66](https://github.com/microsoft/pyright/releases/tag/1.1.66)
    -   Enhancement: Improved completion suggestion behavior when the insertion point is between an identifier and an empty index (e.g. "f[]") or in the presence of a missing right square bracket (e.g. "f.[").
    -   Behavior Change: Changed diagnostic related to type argument count to be controlled by the "reportGeneralTypeIssues" diagnostic rule. It was previously always emitted as an error.
    -   From Pylance: Fix progress reporter type, auto-import/symbol changes, worker thread updates, improve auto-import tooltips (#977)
    -   Enhancement: Updated typeshed stubs to the latest version.
        ([pylance-release#293](https://github.com/microsoft/pylance-release/issues/293))
    -   Bug Fix: Eliminated incorrect error when "super()" was used in a class where one or more parent classes were of an unknown type.
    -   Bug Fix: Changed the handling of old-style comment method annotations to accept an optional annotation for "self" and "cls" parameters.
    -   Bug Fix: Changed handling of dataclass classes that derive from a class whose type is unknown. The synthesized constructor now allows any parameter list in this case.
    -   Enhancement: Improved completion provider to distinguish properties from other methods.
        ([pylance-release#299](https://github.com/microsoft/pylance-release/issues/299))
    -   Behavior Change: Changed heuristics for function return type inference so methods that raise a NotImplementedError and have no other return path have an inferred return type of Unknown rather than NoReturn. Such methods should be marked as abstract, but frequently they are not.
    -   Behavior Change: Changed the behavior of the import resolution logic to fail an import resolution of a multi-part name (e.g. "a.b.c") if it can't be fully resolved. This could produce false positives in cases where third-party libraries are using dynamic tricks to manipulate their package namespace, but it will eliminate false negatives.
    -   Bug Fix: Suppress the use of "Unnecessary" diagnostic hints (used to display variables and code blocks in gray) if the LSP client claims not to support this tag.
    -   Enhancement: Added new "reportMissingTypeArgument" diagnostic rule and enabled it by default in "strict" mode. It generates a diagnostic when a generic class or generic type alias is used in an annotation with no type arguments provided.
    -   Bug Fix: Fixed handling of scopes for nested classes. The previous logic allowed an inner class to access variables defined in an outer class, which is not permitted.
    -   Enhancement: Added check for raise statements that take an exception class but the class constructor requires one or more arguments.
    -   Bug Fix: Fixed bug in tokenizer that cause line numbers to be off when an invalid token occurred at the end of a line.
    -   Bug Fix: Fixed a bug in the Pyright parser. It was not correctly following the Python grammar spec when parsing type annotations, so it generated syntax errors in some cases where that was inappropriate.
    -   Enhancement: Added a check and a general type diagnostic for metaclass conflicts.

## 2020.8.3 (28 August 2020)

Notable changes:

-   Overall memory usage has been improved; in many use cases, peak memory usage has been reduced by 10%.
-   Performance with large unions of `Literal` strings has been greatly improved.
-   Type aliases now show more consistently in tooltips.
-   The upcoming Python 3.10 `typing.TypeAlias` (PEP 613) is now supported.

In addition, Pylance's copy of Pyright has been updated from 1.1.64 to 1.1.65, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Improved completion suggestion behavior when the insertion point is between an identifier and an empty index (e.g. "f[]") or in the presence of a missing right square bracket (e.g. "f.[")
        ([pylance-release#286](https://github.com/microsoft/pylance-release/issues/286))
    -   Behavior Change: Changed diagnostic related to type argument count to be controlled by the "reportGeneralTypeIssues" diagnostic rule. It was previously always emitted as an error.
        ([pylance-release#290](https://github.com/microsoft/pylance-release/issues/290))
-   [1.1.65](https://github.com/microsoft/pyright/releases/tag/1.1.65)
    -   Bug Fix: Fixed bug in command-line version that caused an error to be reported when "useLibraryCodeForTypes" or "verboseOutput" was specified in the pyrightconfig.json file.
    -   Enhancement: Added support for protocol matching where the protocol includes an overloaded method.
    -   Enhancement: Improved diagnostic messages for function type mismatches.
    -   Enhancement: Improved diagnostic messages for tuple matching and union assignments.
    -   Enhancement: Changed nested diagnostic messages to use non-breaking spaces so indentations are visible within the VS Code "Problems" panel.
    -   Bug Fix: Fixed bug in reportIncompatibleMethodOverride diagnostic check. The logic was checking for wider parameter types when it should have been checking for narrower.
    -   Bug Fix: Fixed bug in method override validation code. It wasn't applying partial specialization of the base class, resulting in inappropriate errors in some cases.
    -   Bug Fix: Fixed bug in the type evaluation of expressions with + or - operators and integer literal operands. These expressions should evaluate to a literal type, not an int.
        ([pylance-release#260](https://github.com/microsoft/pylance-release/issues/260))
    -   Bug Fix: Fixed bug in parsing of f-strings that contain \N escape and a Unicode character name that includes a hyphen.
        ([pylance-release#263](https://github.com/microsoft/pylance-release/issues/263))
    -   Bug Fix: Fixed bug in type evaluator that caused an incorrect error when a class decorator was used for a generic class.
    -   Bug Fix: (From Pylance) Fixed performance problem related to file change events triggered by reads from site-packages.
    -   Enhancement: Enabled support for PEP 613 (TypeAlias).
    -   Bug Fix: Fixed bug that caused type aliases to get expanded in some contexts when they shouldn't.
        ([pylance-release#265](https://github.com/microsoft/pylance-release/issues/265))
    -   Bug Fix: Fixed bug that caused "from .A import \*" to work incorrectly when the wildcard included symbol A.
        ([pylance-release#269](https://github.com/microsoft/pylance-release/issues/269))
    -   Enhancement: Added logic in completion provider to return class variables in base classes when the insertion point is in the context of a subclass body.
    -   Bug Fix: Fixed TypeAlias code to check for Python 3.10 rather than 3.9 since PEP 613 has been moved out to 3.10.
    -   Enhancement: Added performance optimization for TypedDict classes. Entries are now computed once and cached in the class type. This provides a big speed-up for TypeDict classes that have a large number of fields.
    -   Enhancement: Added performance optimization for union types that contain large numbers of string literals. The code for inserting new items into a union is O(n^2); this optimization makes it O(n) for string literal types.
    -   Bug Fix: Fixed bug that caused custom import aliases of "Final", "Literal" and "TypeAlias" to not work correctly.
    -   Bug Fix: Fixed bug that resulted in spurious errors when hovering over module names in import statements.
    -   Bug Fix: Fixed several bugs relating to symbols introduced into a class by its metaclass.
        ([pylance-release#154](https://github.com/microsoft/pylance-release/issues/154))
    -   Bug Fix: Fixed bug that caused type analyzer to crash when a nonlocal binding referred to a symbol that was not present in an outer scope and then was assigned to.

## 2020.8.2 (20 August 2020)

Notable changes:

-   The new `python.analysis.completeFunctionParens` option adds parenthesis to function and method completions. This option is disabled by default.
    ([pylance-release#37](https://github.com/microsoft/pylance-release/issues/37))
-   Workspace symbol searching will no longer search or return results from libraries or bundled type stubs, which greatly improves its performance.
    ([pylance-release#34](https://github.com/microsoft/pylance-release/issues/34), [pylance-release#228](https://github.com/microsoft/pylance-release/issues/228))
-   File watching support has been improved, leading to improved performance and lower peak memory consumption.
-   Settings from MPLS (for example `python.autoComplete.extraPaths` and `python.autoComplete.addBrackets`) will now be automatically ported to their updated names if present and Pylance is enabled.

In addition, Pylance's copy of Pyright has been updated from 1.1.62 to 1.1.64, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug in type evaluator that caused an incorrect error when a class decorator was used for a generic class.
    -   Bug Fix: Fixed bug in parsing of f-strings that contain \N escape and a Unicode character name that includes a hyphen.
        ([pylance-release#263](https://github.com/microsoft/pylance-release/issues/263))
    -   Behavior Change: Changed capitalization of the python.analysis.logLevel setting so it matches Pylance. The settings code in Pyright is case insensitive, but the JSON editor emits a warning if the case doesn't match.
    -   Bug Fix: Fixed bug in the type evaluation of expressions with + or - operators and integer literal operands. These expressions should evaluate to a literal type, not an int.
        ([pylance-release#260](https://github.com/microsoft/pylance-release/issues/260))
    -   Bug Fix: Fixed bug in method override validation code. It wasn't applying partial specialization of the base class, resulting in inappropriate errors in some cases.
    -   Bug Fix: Fixed bug in reportIncompatibleMethodOverride diagnostic check. The logic was checking for wider parameter types when it should have been checking for narrower.
    -   Enhancement: Changed nested diagnostic messages to use non-breaking spaces so indentations are visible within the VS Code "Problems" panel.
    -   Enhancement: Improved diagnostic messages for tuple matching and union assignments.
    -   Enhancement: Added support for protocol matching where the protocol includes an overloaded method.
    -   Bug Fix: Fixed bug in command-line version that caused an error to be reported when "useLibraryCodeForTypes" or "verboseOutput" was specified in the pyrightconfig.json file.
-   [1.1.64](https://github.com/microsoft/pyright/releases/tag/1.1.64)
    -   Bug Fix: Fixed regression that caused "isinstance(x, Callable)" to be flagged as an error when PEP 484 says that it's legal.
        ([pylance-release#247](https://github.com/microsoft/pylance-release/issues/247))
    -   Enhancement: Changed error messages related to "partially unknown" types to expand type aliases, which can obscure the unknown part of the type.
    -   Enhancement: Added support for narrowing types based on the pattern `A.B == <literal>` and `A.B != <literal>` when A has a union type and all members of the union have a field "B" with a declared literal type that discriminates one sub-type from another.
    -   Enhancement: Added bidirectional type inference for ternary expressions.
    -   Bug Fix: Fixed incorrect handling of member accesses when the accessed field had a type that was a union between two or more classes, some with special accessor methods (e.g. `__get__`) and some without.
    -   Enhancement: Improved type checking for assignments of callable types. Previously, certain edge cases were ignored.
    -   Enhancement: Added code to check for overlapping (obscured) overload functions.
    -   Bug Fix: Fixed bug that caused incorrect evaluation of type alias that refers to Literal types. The literal values were being stripped in some cases.
    -   Bug Fix: Fixed recent regression that caused type aliases that described literal types to be printed incorrectly in hover text and error messages.
    -   Enhancement: Added code to report overloads that overlap in an "unsafe" way — i.e. they can potentially accept the same arguments but return different (incompatible) types.
    -   Enhancement: Updated typeshed stubs to latest version.
    -   Bug Fix: Fixed bug in assignment checks between homogeneous multi-length tuples and fixed-size tuples.
-   [1.1.63](https://github.com/microsoft/pyright/releases/tag/1.1.63)
    -   Enhancement: Diagnostic rule severity overrides are now editable in the VS Code settings UI.
    -   Bug Fix: Fixed out-of-memory error that occurred during a workspace "find symbols" operation. We were not properly checking for the heap high watermark during this operation.
        ([pylance-release#254](https://github.com/microsoft/pylance-release/issues/254))
    -   Enhancement: Added support for special type "Counter" exported by typing module, which is an alias for collections.Counter.
    -   Bug Fix: Fixed bug in bidirectional type inference for dictionary statements. The logic was not allowing for dict subclass Mapping.
    -   Enhancement: Improved type checker's handling of "in" operator. It previously flagged an error if the right operand didn't support a `__contains__` method. It now properly checks for iterable types as well.
    -   Bug Fix: Fixed bug that caused incorrect evaluation of symbol types within a chain of assignments (e.g. "a = b = c = 4") in some cases.
    -   Enhancement: Enabled file watcher for libraries to detect changes in installed packages. This behavior is already standard for Pylance, but it was disabled for Pyright.
    -   Enhancement: Improved handling of Tuple type. The type checker now does a better job retaining the types of the individual elements within a Tuple or a class that derives from a Tuple.
    -   Enhancement: Improved support for NamedTuple classes and classed derived from NamedTuple. The type checker now retains types of individual elements when used with unpacking and indexing operators.
        ([pylance-release#251](https://github.com/microsoft/pylance-release/issues/251))
    -   Behavior Change: Changed "find workspace symbols" to return only symbols from within user code or opened files, not library files that are closed.
        ([pylance-release#34](https://github.com/microsoft/pylance-release/issues/34), [pylance-release#228](https://github.com/microsoft/pylance-release/issues/228))
    -   Bug Fix: Fixed recent regression that caused incorrect errors to be generated in sub files for certain call expressions.
        ([pylance-release#243](https://github.com/microsoft/pylance-release/issues/243))
    -   New Feature: Added support for Concatenate as described in latest version of PEP 612. Added ParamSpec and Concatenate to typing.pyi.

## 2020.8.1 (13 August 2020)

Notable changes:

-   The `pandas` stubs have been further improved.
    ([pylance-release#27](https://github.com/microsoft/pylance-release/issues/27), [pylance-release#90](https://github.com/microsoft/pylance-release/issues/90), [pylance-release#144](https://github.com/microsoft/pylance-release/issues/144), [pylance-release#148](https://github.com/microsoft/pylance-release/issues/148), [pylance-release#202](https://github.com/microsoft/pylance-release/issues/202))
-   The VS Code settings editor (both UI and JSON) now provides hints for `python.analysis.diagnosticSeverityOverrides`, listing all valid options, their values, and descriptions.
-   Old-style `# type` comments for function signature type annotations are now supported. This syntax is underspecified and not preferred, but is commonly used to provide compatibility with (the now end-of-life) Python 2, and may improve the usability of some libraries.

In addition, Pylance's copy of Pyright has been updated from 1.1.60 to 1.1.62, including the following changes:

-   Unreleased in Pyright, but included in Pylance:
    -   Bug Fix: Fixed bug that caused incorrect evaluation of symbol types within a chain of assignments (e.g. "a = b = c = 4") in some cases.
    -   Enhancement: Improved type checker's handling of "in" operator. It previously flagged an error if the right operand didn't support a `__contains__` method. It now properly checks for iterable types as well.
    -   Bug Fix: Fixed bug in bidirectional type inference for dictionary statements. The logic was not allowing for dict subclass Mapping.
    -   Enhancement: Added support for special type "Counter" exported by typing module, which is an alias for collections.Counter.
        ([pylance-release#229](https://github.com/microsoft/pylance-release/issues/229))
    -   Bug Fix: Fixed out-of-memory error that occurred during a workspace "find symbols" operation. We were not properly checking for the heap high watermark during this operation.
        ([pylance-release#228](https://github.com/microsoft/pylance-release/issues/228))
-   [1.1.62](https://github.com/microsoft/pyright/releases/tag/1.1.62)
    -   Bug Fix: Fixed bug in the handling of unrecognized escape sequences within string literals.
        ([pylance-release#219](https://github.com/microsoft/pylance-release/issues/219))
    -   Bug Fix: Fixed bug related to a subtle interaction between bidirectional type inference of list expressions that contain literal values and TypeVar matching. The previous logic was incorrectly matching T in `List[T]` and the list contained a literal type. It should have stripped the literal if possible.
    -   Enhancement: Added diagnostic message for TypeVar with a single constraint type for consistency with mypy.
    -   Enhancement: Added support for member access completion suggestions when the LHS is a function or a None type.
        ([pylance-release#214](https://github.com/microsoft/pylance-release/issues/214))
    -   Behavior Change: Behavior change for type stub generator: don't emit `__all__` assignments or assignments to self.xxx in function bodies. These violate PEP 484 guidelines for type stubs.
    -   Enhancement: Added diagnostic check to reportInvalidStubStatement that flags parameter default value expressions that are not "..." in stub files.
    -   Bug Fix: Fixed bug that caused annotated types of vargs and kwargs parameters not to be printed in hover text.
    -   Enhancement: Implemented support for older-style function annotation type comments. I previously resisted adding this additional complexity, but we're seeing many libraries that still contain these annotations for backward compatibility with Python 2.
    -   Bug Fix: Fixed bug that caused a crash in the type analyzer when a protocol class referred to itself.
        ([pylance-release#225](https://github.com/microsoft/pylance-release/issues/225))
    -   Enhancement: Added support for "useLibraryCodeForTypes" option in config file. It overrides the client setting of the same name or the "--lib" command-line option.
    -   Bug Fix: Fixed several bugs in logging for config errors.
    -   Enhancement: Added logic to type checker to validate that the "self" or "cls" parameter with a specified type annotation is assignable when binding the method to an object or class.
    -   Enhancement: Improved type assignment diagnostic message. Added "(property)" designator to the end of a property type to differentiate it from a normal attribute.
    -   Enhancement: Added code to validate that method overloads are all abstract or not.
    -   Enhancement: Updated typeshed stubs to the latest.
-   [1.1.61](https://github.com/microsoft/pyright/releases/tag/1.1.61)
    -   Bug Fix: Fixed bug that caused symbols to be marked unaccessed if they were accessed by code that is not accessible (e.g. due to conditional execution based on the platform).
    -   Bug Fix: Updated PEP 604 and PEP 612 error message to refer to Python 3.10 instead of 3.9.
    -   Behavior Change: Changed logic that validates "self" or "cls" parameter names to ignore the check if the provided parameter name begins with an underscore, as is seen in several typeshed stub files.
    -   Bug Fix: Fixed bug in nested f-string parsing when f-string contains triple quotes that include single quotes.
        ([pylance-release#203](https://github.com/microsoft/pylance-release/issues/206))
    -   Bug Fix: Fixed handling of a class that is subclassed from both Enum and another class (like str).
    -   Enhancement: Added support for generic classes that refer to themselves as type arguments within their base class.
    -   Bug Fix: Improved error message for partially-unknown types that have a type alias.
    -   Bug Fix: Allow use of forward-declared classes as subclass in class declarations within type stub files.
    -   Bug Fix: Add special-case handling of `__class_getitem__` method, which acts as a class method even though it is not decorated as such.
    -   Bug Fix: Added missing validation of arguments to `type` call.
    -   Enhancement: Added `=` character to end of named parameter for completion suggestions within a call signature.
        ([pylance-release#209](https://github.com/microsoft/pylance-release/issues/209))
    -   Bug Fix: Added client capability check for signature information "labelOffsetSupport" for compatibility with clients that don't support this capability.
    -   Bug Fix: When adding completion suggestions to the list for expression completion, avoid adding duplicately-named symbols that appear in nested scopes.
        ([pylance-release#215](https://github.com/microsoft/pylance-release/issues/215))
    -   Bug Fix: Fixed bug related to calls of methods on a metaclass via classes that are constructed by that metaclass.
    -   Enhancement: Added check for single @overload function with no additional overloads.

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

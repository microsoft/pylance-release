/**
 * Copyright (c) Microsoft Corporation.
 * All rights reserved.
 *
 * typeServerProtocol.ts
 *
 * Defines the interfaces and types for the type server protocol. A Type Server is a module that provides type information
 * for code, such as type definitions, member information, and diagnostics.
 *
 * It's Python specific at the moment, but may be made generic in the future.
 *
 * This protocol is used to communicate between the type server and the client (e.g., a language server or an IDE).
 *
 * All the types in this file should be JSON serializable, as they are sent over the wire.
 * The protocol is designed to be extensible, allowing for future additions of new requests and notifications.
 */
import {
    MessageDirection,
    ProtocolNotificationType,
    ProtocolRequestType,
    ProtocolRequestType0,
    Range,
} from 'vscode-languageserver-protocol';

export namespace TypeServerProtocol {
    export const ReturnSymbolName = '__return__'; // Special name for the return value of a function or method.
    export const InvalidHandle = -1; // Special value for an invalid handle. This is used to indicate that a type or declaration is not valid.

    /**
     * Represents a location in source code (a node in the AST).
     * Used to point to specific declarations, expressions, or statements in Python source files.
     *
     * Used for:
     * - Pointing to where a type is declared
     * - Identifying the location of expressions for type inference
     * - Error reporting and diagnostics
     * - Linking types back to their source definitions
     *
     * Examples:
     * - For `def foo():`, the node points to the function declaration
     * - For a variable `x = 42`, the node points to the assignment
     * - For default parameter values in functions
     */
    export interface Node {
        // URI of the source file containing this node.
        uri: string;
        // The range of the node in the source file.
        // This is a zero-based range, meaning the start and end positions are both zero-based
        // The range uses character offsets the same way the LSP does.
        range: Range;
    }

    /**
     * Version of the type server protocol.
     * Used for protocol negotiation between client and server to ensure compatibility.
     *
     * The version follows semantic versioning (semver):
     * - Major version changes indicate breaking changes to the protocol
     * - Minor version changes add new features while maintaining backward compatibility
     * - Patch version changes fix bugs without changing the protocol
     *
     * Clients should check the server's supported version before making requests.
     */
    export enum TypeServerVersion {
        v0_1_0 = '0.1.0', // Initial protocol version
        v0_2_0 = '0.2.0', // Added new request types and fields
        current = '0.3.0', // The current version of the type server protocol.
    }
    // Flags that describe the characteristics of a type.
    // These flags can be combined using bitwise operations.
    export const enum TypeFlags {
        None = 0,
        Instantiable = 1 << 0, // Indicates if the type can be instantiated.
        Instance = 1 << 1, // Indicates if the type represents an instance (as opposed to a class or type itself).
        Callable = 1 << 2, // Indicates if an instance of the type can be called like a function. (It has a `__call__` method).
        Literal = 1 << 3, // Indicates if the instance is a literal (like `42`, `"hello"`, etc.).
        Interface = 1 << 4, // Indicates if the type is an interface (a type that defines a set of methods and properties). In Python this would be a Protocol.
        Generic = 1 << 5, // Indicates if the type is a generic type (a type that can be parameterized with other types).
        FromAlias = 1 << 6, // Indicates if the type came from an alias (a type that refers to another type).
        Unpacked = 1 << 7, // Indicates if the type is unpacked (used with TypeVarTuple).
        Optional = 1 << 8, // Indicates if the type is optional (used with Tuple type arguments).
        Unbound = 1 << 9, // Indicates if the type is unbound (used with *args in tuple type arguments).
    }
    // Flags that describe the characteristics of a type variable.
    // These flags can be combined using bitwise operations.
    export const enum TypeVarFlags {
        None = 0,
        IsParamSpec = 1 << 0, // Indicates if the type variable is a ParamSpec (as defined in PEP 612).
        IsTypeVarTuple = 1 << 1, // Indicates if the type variable is a TypeVarTuple (as defined in PEP 646).
    }

    /**
     * Represents a Python module name, handling both absolute and relative imports.
     *
     * Used for:
     * - Import statement resolution
     * - Tracking module dependencies
     * - Resolving relative imports (from . import, from .. import)
     *
     * Examples:
     * - `import os.path`: leadingDots=0, nameParts=['os', 'path']
     * - `from . import utils`: leadingDots=1, nameParts=['utils']
     * - `from ...parent import module`: leadingDots=3, nameParts=['parent', 'module']
     * - `import mymodule`: leadingDots=0, nameParts=['mymodule']
     */
    export interface ModuleName {
        // The leading dots in the module name. This is used to determine the relative import level.
        leadingDots: number;
        // The parts of the module name, split by dots. For example, for `my_module.sub_module`, this would be `['my_module', 'sub_module']`.
        nameParts: string[];
    }
    // Represents the category of a declaration in the type system.
    // This is used to classify declarations such as variables, functions, classes, etc.
    export const enum DeclarationCategory {
        Intrinsic, // An intrinsic refers to a symbol that has no actual declaration in the source code, such as built-in types or functions. One such example is a '__class__' declaration.
        Variable, // A variable is a named storage location that can hold a value.
        Param, // A parameter is a variable that is passed to a function or method.
        TypeParam, // This is for PEP 695 type parameters.
        TypeAlias, // This is for PEP 695 type aliases.
        Function, // A function is any construct that begins with the `def` keyword and has a body, which can be called with arguments.
        Class, // A class is any construct that begins with the `class` keyword and has a body, which can be instantiated.
        Import, // An import declaration, which is a reference to another module.
    }

    /**
     * Options for customizing import resolution behavior.
     * Controls how the type server resolves import statements and accesses imported symbols.
     *
     * Used for:
     * - Fine-tuning import resolution during type checking
     * - Controlling access to private/hidden module members
     * - Optimizing resolution by skipping file checks
     *
     * TODO: See if we can remove this as these are pretty specific to Pyright at the moment.
     *
     * Examples:
     * ```python
     * # resolveLocalNames affects whether local assignments are resolved:
     * from module import name
     * name = something_else  # Does 'name' refer to import or local assignment?
     *
     * # allowExternallyHiddenAccess affects access to _private names:
     * from module import _internal_function  # Normally hidden from external access
     * ```
     */
    export interface ResolveImportOptions {
        // Whether to resolve local names in the import declaration.
        // When true, considers local variable assignments that shadow imports.
        resolveLocalNames?: boolean;

        // Whether to allow access to members that are hidden by external modules.
        // When true, permits access to symbols marked as private (e.g., _private or not in __all__).
        allowExternallyHiddenAccess?: boolean;

        // Whether to skip checking if the file is needed for the import resolution.
        // When true, optimizes by not verifying file existence/validity.
        skipFileNeededCheck?: boolean;
    }

    /**
     * Parameters for the ResolveImportRequest.
     * Provides the context needed to resolve a Python import statement to its file location.
     *
     * Used when:
     * - Resolving `import` or `from...import` statements
     * - Finding the file that contains an imported module
     * - Navigating to imported symbols
     *
     * Examples:
     * ```python
     * # In file.py:
     * from os.path import join  # sourceUri = file.py, moduleDescriptor = os.path
     * import mymodule          # sourceUri = file.py, moduleDescriptor = mymodule
     * from . import utils      # sourceUri = file.py, moduleDescriptor = .utils (relative)
     * ```
     */
    export interface ResolveImportParams {
        // The URI of the source file where the import is referenced.
        // Used to resolve relative imports and determine the import context.
        sourceUri: string;

        // The descriptor of the imported module.
        // Contains the module name parts and leading dots for relative imports.
        moduleDescriptor: ModuleName;

        // Snapshot version of the type server.
        // Type server should throw a ServerCanceled exception if this snapshot is no longer current.
        snapshot: number;
    }

    /**
     * Parameters for the GetPythonSearchPathsRequest.
     * Requests the list of directories that Python searches for modules and packages.
     *
     * The search paths include:
     * - Standard library directories
     * - Site-packages directories (third-party packages)
     * - Virtual environment paths (if active)
     * - Project-specific paths (PYTHONPATH, src directories)
     *
     * Used for:
     * - Resolving import statements to find module files
     * - Auto-import suggestions
     * - Determining which packages are available
     *
     * Example search paths:
     * ```
     * [
     *   "/usr/lib/python3.11",              # Standard library
     *   "/venv/lib/python3.11/site-packages",  # Virtual env packages
     *   "/project/src"                       # Project source
     * ]
     * ```
     */
    export interface GetPythonSearchPathsParams {
        // Root folder to get search paths from.
        // Determines the Python environment and project context for path resolution.
        fromUri: string;

        // Snapshot version of the type server.
        // Type server should throw a ServerCanceled exception if this snapshot is no longer current.
        snapshot: number;
    }

    // Flags that describe the characteristics of a symbol in a type handle.
    export const enum TypeHandleSymbolFlags {
        None = 0,

        // Indicates that the symbol is not visible from other files.
        // Used for module-level symbols.
        ExternallyHidden = 1 << 1,

        // Indicates that the symbol is a class member of a class.
        ClassMember = 1 << 2,

        // Indicates that the symbol is an instance member of a class.
        InstanceMember = 1 << 3,

        // Indicates that the symbol is specified in the __slots__
        // declaration of a class. Such symbols act like instance members
        // in some respects but are actually implemented as class members
        // using descriptor objects.
        SlotsMember = 1 << 4,

        // Indicates that the symbol is considered "private" to the
        // class or module and should not be accessed outside or overridden.
        PrivateMember = 1 << 5,

        // Indicates that the symbol is a ClassVar, so it cannot be
        // set when accessed through a class instance.
        ClassVar = 1 << 7,

        // Indicates that the symbol is in __all__.
        InDunderAll = 1 << 8,

        // Indicates that the symbol is a private import in a py.typed module.
        PrivatePyTypedImport = 1 << 9,

        // Indicates that the symbol is an InitVar as specified in PEP 557.
        InitVar = 1 << 10,

        // Indicates that the symbol is a field in a NamedTuple class, which
        // is modeled as an instance member but in some respects acts as a
        // class member.
        NamedTupleMember = 1 << 11,

        // Indicates that the symbol is marked Final and is assigned a value
        // in the class body. The typing spec indicates that these should be
        // considered ClassVars unless they are found in a dataclass.
        FinalVarInClassBody = 1 << 13,
    }

    /**
     * Represents a symbol (variable, function, class, etc.) and its type information.
     * Used in symbol tables to track class/module members.
     *
     * Contains:
     * - Flags describing the symbol's characteristics (visibility, mutability, etc.)
     * - Declarations where the symbol is defined
     * - Synthesized type information for implicit symbols
     * - Aliases for typing imports (e.g., List as an alias for list)
     *
     * Used for:
     * - Class member lookup (methods, properties, fields)
     * - Module member resolution
     * - Tracking symbol visibility and access control
     * - Handling typing module aliases
     *
     * Examples:
     * - In `class Foo: x: int`, 'x' is a TypeHandleSymbol with InstanceMember flag
     * - In `class Bar: _private: str`, '_private' has PrivateMember flag
     * - In `from typing import List`, 'List' has typingSymbolAlias='list'
     */
    export interface TypeHandleSymbol {
        // Bitfield of TypeHandleSymbolFlags describing symbol characteristics.
        // Example: ClassMember | PrivateMember for a private class variable.
        flags: TypeHandleSymbolFlags;

        // Array of declarations where this symbol is defined (can have multiple for overloads).
        // Example: A function with multiple @overload decorators has multiple declarations.
        declarations?: TypeHandleDeclaration[];

        // Type information for synthesized symbols that don't have source declarations.
        // Contains the type and optional AST node for context.
        // Example: __class__ attribute has synthesized type info.
        synthesizedTypeInfo?: {
            type: TypeHandle;
            node?: Node;
        };

        // Name of the actual typing module symbol this aliases.
        // Example: 'List' from typing aliases to 'list', 'Dict' aliases to 'dict'.
        typingSymbolAlias?: string;
    }

    export const enum ClassTypeFlags {
        None = 0,

        // Class is defined in the "builtins" or "typing" file.
        BuiltIn = 1 << 0,

        // Class requires special-case handling because it
        // exhibits non-standard behavior or is not defined
        // formally as a class. Examples include 'Optional'
        // and 'Union'.
        SpecialBuiltIn = 1 << 1,

        // Introduced in PEP 589, TypedDict classes provide a way
        // to specify type hints for dictionaries with different
        // value types and a limited set of static keys.
        TypedDictClass = 1 << 2,

        // Used in conjunction with TypedDictClass, indicates that
        // the TypedDict class is marked "closed".
        TypedDictMarkedClosed = 1 << 3,

        // Used in conjunction with TypedDictClass, indicates that
        // the TypedDict class is marked "closed" or one or more of
        // its superclasses is marked "closed".
        TypedDictEffectivelyClosed = 1 << 4,

        // Used in conjunction with TypedDictClass, indicates that
        // the dictionary values can be omitted.
        CanOmitDictValues = 1 << 5,

        // The class derives from a class that has the ABCMeta
        // metaclass. Such classes are allowed to contain
        // @abstractmethod decorators.
        SupportsAbstractMethods = 1 << 6,

        // Derives from property class and has the semantics of
        // a property (with optional setter, deleter).
        PropertyClass = 1 << 7,

        // The class is decorated with a "@final" decorator
        // indicating that it cannot be subclassed.
        Final = 1 << 8,

        // The class derives directly from "Protocol".
        ProtocolClass = 1 << 9,

        // A class whose constructor (__init__ method) does not have
        // annotated types and is treated as though each parameter
        // is a generic type for purposes of type inference.
        PseudoGenericClass = 1 << 10,

        // A protocol class that is "runtime checkable" can be used
        // in an isinstance call.
        RuntimeCheckable = 1 << 11,

        // The type is defined in the typing_extensions.pyi file.
        TypingExtensionClass = 1 << 12,

        // The class or one of its ancestors defines a __class_getitem__
        // method that is used for subscripting. This is not set if the
        // class is generic, and therefore supports standard subscripting
        // semantics.
        HasCustomClassGetItem = 1 << 14,

        // The tuple class requires special-case handling for its type arguments.
        TupleClass = 1 << 15,

        // The class has a metaclass of EnumMeta or derives from
        // a class that has this metaclass.
        EnumClass = 1 << 16,

        // Properties that are defined using the @classmethod decorator.
        ClassProperty = 1 << 17,

        // Class is declared within a type stub file.
        DefinedInStub = 1 << 18,

        // Decorated with @type_check_only.
        TypeCheckOnly = 1 << 20,

        // Created with the NewType call.
        NewTypeClass = 1 << 21,

        // Class is allowed to be used as an implicit type alias even
        // though it is not defined using a `class` statement.
        ValidTypeAliasClass = 1 << 22,

        // A special form is not compatible with type[T] and cannot
        // be directly instantiated.
        SpecialFormClass = 1 << 23,

        // This class is rejected when used as the second argument to
        // an isinstance or issubclass call.
        IllegalIsinstanceClass = 1 << 24,
    }

    /**
     * Represents a single field in a TypedDict.
     * Contains the type and metadata for one key-value pair in a TypedDict definition.
     *
     * Fields:
     * - valueType: The type of the value for this key
     * - isRequired: Whether this key must be present (vs. optional using NotRequired[])
     * - isReadOnly: Whether this key cannot be modified (using ReadOnly[])
     * - isProvided: Whether this key has been provided in a partial TypedDict construction
     *
     * Examples:
     * ```python
     * class Movie(TypedDict):
     *     name: str              # isRequired=true, isReadOnly=false
     *     year: int              # isRequired=true, isReadOnly=false
     *     rating: NotRequired[float]  # isRequired=false
     *     id: ReadOnly[int]      # isRequired=true, isReadOnly=true
     * ```
     */
    export interface TypedDictEntry {
        // The type of values for this TypedDict key.
        // Example: For `name: str`, valueType is the str type.
        valueType: TypeHandle;

        // True if this key must be present in the dictionary.
        // False for NotRequired[] fields.
        // Example: `year: NotRequired[int]` has isRequired=false.
        isRequired: boolean;

        // True if this key cannot be modified after creation.
        // Set by ReadOnly[] annotation.
        // Example: `id: ReadOnly[int]` has isReadOnly=true.
        isReadOnly: boolean;

        // True if this key has been provided during partial TypedDict construction.
        // Used for tracking incremental TypedDict building.
        isProvided: boolean;
    }

    /**
     * Represents all fields in a TypedDict class.
     * Contains both explicitly declared fields and optional extra items.
     *
     * Fields:
     * - knownItems: Dictionary mapping field names to their TypedDictEntry definitions
     * - extraItems: Optional type for additional keys (when using extra_items parameter)
     *
     * Examples:
     * ```python
     * # Standard TypedDict
     * class Movie(TypedDict):
     *     name: str
     *     year: int
     * # knownItems = {"name": TypedDictEntry(...), "year": TypedDictEntry(...)}
     * # extraItems = undefined
     *
     * # TypedDict with extra_items (closed TypedDict)
     * class Config(TypedDict, extra_items=str):
     *     host: str
     *     port: int
     * # knownItems = {"host": ..., "port": ...}
     * # extraItems = TypedDictEntry for str type
     * ```
     */
    export interface TypedDictEntries {
        // Map of explicitly declared field names to their TypedDictEntry definitions.
        // Contains all keys defined in the TypedDict class body.
        // Example: {"name": TypedDictEntry(...), "year": TypedDictEntry(...)}
        knownItems: Record<string, TypedDictEntry>;

        // Optional type for additional keys not in knownItems.
        // Set when using the extra_items parameter in closed TypedDicts.
        // Example: `class Config(TypedDict, extra_items=str)` allows any str-valued extra keys.
        extraItems?: TypedDictEntry | undefined;
    }

    /**
     * Represents a single type argument in a tuple type.
     * Used for tuple[...] generic type arguments, handling both fixed and variadic elements.
     *
     * Fields:
     * - type: The type of this tuple element
     * - isUnbounded: True for *args-style variadic elements (zero or more of this type)
     * - isOptional: True if this element can be omitted (has a default)
     *
     * Examples:
     * ```python
     * # Fixed tuple
     * x: tuple[int, str, bool]
     * # Three TupleTypeArg: [int, str, bool], all with isUnbounded=false
     *
     * # Unbounded tuple
     * y: tuple[int, ...]
     * # One TupleTypeArg: int with isUnbounded=true
     *
     * # Callable with optional params
     * def foo(a: int, b: str = "") -> None: ...
     * # Captured as tuple[int, str] where str has isOptional=true
     * ```
     */
    export interface TupleTypeArg {
        // The type of this tuple element.
        // Example: In `tuple[int, str, bool]`, each position has a different type.
        type: TypeHandle;

        // Does the type argument represent a single value or
        // an "unbounded" (zero or more) arguments?
        // True for `tuple[int, ...]` (variadic), false for `tuple[int, str]` (fixed).
        isUnbounded: boolean;

        // For tuples captured from a callable, this indicates
        // the corresponding positional parameter has a default
        // argument and can therefore be omitted.
        // Example: For `def foo(a: int, b: str = "")`, b's type has isOptional=true.
        isOptional?: boolean;
    }

    /**
     * Represents information about a property method (getter, setter, or deleter).
     * Used to track the implementation of @property decorated methods.
     *
     * Fields:
     * - methodType: The type of the decorated function (fget, fset, or fdel)
     * - classType: The class that declared this method
     *
     * Examples:
     * ```python
     * class Person:
     *     @property
     *     def name(self) -> str:  # fgetInfo contains this method's type
     *         return self._name
     *
     *     @name.setter
     *     def name(self, value: str) -> None:  # fsetInfo contains this method's type
     *         self._name = value
     *
     *     @name.deleter
     *     def name(self) -> None:  # fdelInfo contains this method's type
     *         del self._name
     * ```
     */
    export interface PropertyMethodInfo {
        // The type of the decorated function (fget, fset, or fdel).
        // Contains the function signature including parameters and return type.
        // Example: For `@property def name(self) -> str`, this is the function type.
        methodType: TypeHandle;

        // The class that declared this property method.
        // Used to track which class in the inheritance hierarchy defined the method.
        // Example: If a property is inherited, classType points to the declaring class.
        classType?: TypeHandle;
    }

    /**
     * Categorizes function parameters by their type in the function signature.
     * Determines how the parameter accepts arguments at call time.
     *
     * Used for:
     * - Regular named parameters
     * - Variadic positional parameters (*args)
     * - Variadic keyword parameters (**kwargs)
     *
     * Examples:
     * ```python
     * def example(
     *     x: int,           # Simple - regular parameter
     *     y: str,           # Simple - regular parameter
     *     *args: float,     # ArgsList - variadic positional
     *     **kwargs: bool    # KwargsDict - variadic keyword
     * ) -> None:
     *     pass
     * ```
     */
    export const enum ParamCategory {
        Simple, // Regular parameter: def foo(x: int)
        ArgsList, // Variadic positional: def foo(*args: int)
        KwargsDict, // Variadic keyword: def foo(**kwargs: str)
    }

    export enum FunctionParamFlags {
        None = 0,

        // Is the name of the parameter synthesize internally?
        NameSynthesized = 1 << 0,

        // Does the parameter have an explicitly-declared type?
        TypeDeclared = 1 << 1,
    }

    export const enum FunctionTypeFlags {
        None = 0,

        // Function is a __new__ method; first parameter is "cls"
        ConstructorMethod = 1 << 0,

        // Function is decorated with @classmethod; first parameter is "cls";
        // can be bound to associated class
        ClassMethod = 1 << 1,

        // Function is decorated with @staticmethod; cannot be bound to class
        StaticMethod = 1 << 2,

        // Function is decorated with @abstractmethod
        AbstractMethod = 1 << 3,

        // Function contains "yield" or "yield from" statements
        Generator = 1 << 4,

        // Method has no declaration in user code, it's synthesized; used
        // for implied methods such as those used in namedtuple, dataclass, etc.
        SynthesizedMethod = 1 << 6,

        // Decorated with @type_check_only.
        TypeCheckOnly = 1 << 7,

        // Function is decorated with @overload
        Overloaded = 1 << 8,

        // Function is declared with async keyword
        Async = 1 << 9,

        // Function is declared within a type stub fille
        StubDefinition = 1 << 11,

        // Function is declared within a module that claims to be fully typed
        // (i.e. a "py.typed" file is present).
        PyTypedDefinition = 1 << 12,

        // Function is decorated with @final
        Final = 1 << 13,

        // Function has one or more parameters that are missing type annotations
        UnannotatedParams = 1 << 14,

        // The *args and **kwargs parameters do not need to be present for this
        // function to be compatible. This is used for Callable[..., x] and
        // ... type arguments to ParamSpec and Concatenate.
        GradualCallableForm = 1 << 15,

        // This function represents the value bound to a ParamSpec, so its return
        // type is not meaningful.
        ParamSpecValue = 1 << 16,

        // Decorated with @override as defined in PEP 698.
        Overridden = 1 << 18,

        // Decorated with @no_type_check.
        NoTypeCheck = 1 << 19,

        // Function defined in one of the core stdlib modules.
        BuiltIn = 1 << 20,
    }

    /**
     * Represents a single parameter in a function signature.
     * Contains all information about a parameter including its type, default value, and category.
     *
     * Fields:
     * - category: Whether it's a simple param, *args, or **kwargs
     * - flags: Metadata flags (e.g., whether name is synthesized, type is declared)
     * - name: Parameter name (or undefined for positional-only)
     * - type: Type annotation for the parameter
     * - defaultType: Type of the default value (if present)
     * - defaultExpr: AST node for the default value expression
     *
     * Examples:
     * ```python
     * def example(
     *     x: int,              # Simple, name="x", type=int, no default
     *     y: str = "hello",    # Simple, name="y", type=str, defaultType=str
     *     *args: int,          # ArgsList, name="args", type=int
     *     **kwargs: str        # KwargsDict, name="kwargs", type=str
     * ) -> None:
     *     pass
     * ```
     */
    export interface FunctionParam {
        // Category of parameter: Simple (regular), ArgsList (*args), or KwargsDict (**kwargs).
        // Example: In `def foo(x, *args, **kwargs)`, x is Simple, args is ArgsList, kwargs is KwargsDict.
        category: ParamCategory;

        // Bitfield of FunctionParamFlags (e.g., NameSynthesized, TypeDeclared).
        // Example: TypeDeclared is set for `x: int` but not for `x`.
        flags: FunctionParamFlags;

        // Name of the parameter, or undefined for positional-only parameters.
        // Example: "self" for instance methods, "cls" for class methods.
        name: string | undefined;

        // Type annotation for this parameter.
        // Example: For `x: int`, type is the int type.
        type: TypeHandle;

        // Type of the default value, if the parameter has one.
        // Example: For `y: str = "hello"`, defaultType is str (inferred from "hello").
        defaultType: TypeHandle | undefined;

        // AST node pointing to the default value expression.
        // Used for analysis and error reporting on default values.
        // Example: Points to the "hello" literal in `y: str = "hello"`.
        defaultExpr: Node | undefined;
    }

    /**
     * Represents specialized (concrete) types for a generic function's parameters and return type.
     * Used when generic type parameters are substituted with actual types.
     *
     * Fields:
     * - parameterTypes: Concrete types for each parameter after type variable substitution
     * - parameterDefaultTypes: Specialized types for default values (if different from declared)
     * - returnType: Specialized return type after type variable substitution
     *
     * Examples:
     * ```python
     * # Generic function
     * def identity[T](x: T) -> T:
     *     return x
     *
     * # When called as identity[int](42):
     * # - parameterTypes = [int] (T substituted with int)
     * # - returnType = int (T substituted with int)
     *
     * # For list.append bound to list[str]:
     * # - parameterTypes = [str] (specialized from generic T)
     * ```
     */
    export interface SpecializedFunctionTypes {
        // Specialized types for each of the parameters in the "parameters" array.
        // Array matches the parameters array, with type variables replaced by concrete types.
        // Example: For `def foo[T](x: T)` specialized to `T=int`, parameterTypes=[int].
        parameterTypes: TypeHandle[];

        // Specialized types of default arguments for each parameter in
        // the "parameters" array. If an entry is undefined or the entire array
        // is missing, there is no specialized type, and the original "defaultType"
        // should be used.
        // Example: For a generic default value that depends on T, this contains the specialized version.
        parameterDefaultTypes: (TypeHandle | undefined)[] | undefined;

        // Specialized type of the declared return type. Undefined if there is
        // no declared return type.
        // Example: For `def foo[T](x: T) -> T` specialized to `T=int`, returnType=int.
        returnType: TypeHandle | undefined;
    }

    /**
     * Represents a literal value from an Enum.
     * Used to track specific enum members as literal types.
     *
     * Fields:
     * - className: Name of the enum class
     * - itemName: Name of the specific enum member
     * - itemType: Type of the enum member's value
     *
     * Examples:
     * ```python
     * from enum import Enum
     *
     * class Color(Enum):
     *     RED = 1
     *     GREEN = 2
     *     BLUE = 3
     *
     * # Color.RED is an EnumLiteral:
     * # className="Color", itemName="RED", itemType=int (for value 1)
     *
     * def process(color: Literal[Color.RED]) -> None:
     *     pass  # EnumLiteral tracks that it's specifically Color.RED
     * ```
     */
    export interface EnumLiteral {
        // Name of the enum class.
        // Example: "Color" for the Color enum.
        className: string;

        // Name of the specific enum member.
        // Example: "RED" for Color.RED.
        itemName: string;

        // Type of the enum member's value.
        // Example: int type if the enum values are integers.
        itemType: TypeHandle;
    }

    /**
     * Represents a sentinel value (a unique object used as a marker).
     * Used for special singleton values that act as sentinels in APIs.
     *
     * Fields:
     * - classNode: AST node where the sentinel class is defined
     * - moduleName: Module containing the sentinel
     * - className: Name of the sentinel class
     *
     * Examples:
     * ```python
     * # Common sentinel pattern
     * class _Sentinel:
     *     pass
     * MISSING = _Sentinel()
     *
     * def get_value(key: str, default: int | _Sentinel = MISSING) -> int:
     *     ...
     *
     * # MISSING is a SentinelLiteral pointing to the _Sentinel class instance
     *
     * # Used in standard library (e.g., dataclasses.MISSING)
     * from dataclasses import field, MISSING
     * # MISSING is tracked as a SentinelLiteral
     * ```
     */
    export interface SentinelLiteral {
        // AST node pointing to the sentinel class definition.
        // Used to locate the class in source code.
        classNode: Node;

        // Fully qualified module name where the sentinel is defined.
        // Example: "dataclasses" for dataclasses.MISSING.
        moduleName: string;

        // Name of the sentinel class.
        // Example: "_MISSING_TYPE" for the class of dataclasses.MISSING.
        className: string;
    }

    /**
     * Represents the value of a literal type in Python.
     * A literal type has a specific, known value at type-checking time.
     *
     * Literal types include:
     * - Primitive literals: numbers, booleans, strings
     * - Enum members: specific values from an Enum class
     * - Sentinel values: unique marker objects (e.g., dataclasses.MISSING)
     *
     * Used for:
     * - Type narrowing with specific values
     * - Overload resolution based on literal arguments
     * - TypedDict key validation
     * - Literal types in function signatures
     *
     * Examples:
     * ```python
     * # Primitive literals
     * x: Literal[42] = 42                    # number literal
     * y: Literal["hello"] = "hello"          # string literal
     * z: Literal[True] = True                # boolean literal
     * big: Literal[999999999999999] = 999999999999999  # bigint literal
     *
     * # Enum literal
     * class Color(Enum):
     *     RED = 1
     * color: Literal[Color.RED] = Color.RED  # EnumLiteral
     *
     * # Sentinel literal
     * from dataclasses import MISSING
     * def field(default=MISSING): ...        # SentinelLiteral
     * ```
     */
    export type LiteralValue = number | bigint | boolean | string | EnumLiteral | SentinelLiteral;

    /**
     * Discriminator for the TypeHandle union type.
     * Identifies which variant of TypeHandle is being used.
     *
     * Used for type narrowing when processing TypeHandle objects:
     * ```typescript
     * if (handle.kind === TypeHandleKind.Function) {
     *     // TypeScript knows this is FunctionTypeHandle
     *     const returnType = handle.returnType;
     * }
     * ```
     *
     * Categories:
     * - BuiltIn: Special types (unknown, any, never, etc.)
     * - Regular: Types from source declarations (base for Function/Class)
     * - Union: Multiple types combined (T1 | T2 | ...)
     * - Module: Python module types
     * - TypeVar: Generic type parameters (T, P, Ts)
     * - SynthesizedOverloaded: Functions with @overload decorators
     * - SynthesizedFunction: Built-in or generated functions
     * - SynthesizedClass: Built-in or generated classes
     * - TypeReference: Reference to another type by ID
     */
    export const enum TypeHandleKind {
        BuiltIn, // unknown, any, never, etc.
        Regular, // Base for source-declared types
        Union, // int | str | None
        Module, // import os -> os is ModuleType
        TypeVar, // T, P, Ts in generics
        SynthesizedOverloaded, // Functions with multiple @overload signatures
        SynthesizedFunction, // Built-in functions or synthesized methods
        SynthesizedClass, // Built-in classes or synthesized types
        TypeReference, // Reference by ID for deduplication
    }

    /**
     * Discriminator for the TypeHandleDeclaration union type.
     * Distinguishes between declarations that exist in source code versus those created by the type checker.
     *
     * Used to determine whether a declaration:
     * - Has an actual AST node in the parse tree (Regular)
     * - Was created implicitly by the type system (Synthesized)
     *
     * Examples:
     * - Regular: `def my_function():` - has source code node
     * - Synthesized: `__init__` method generated by @dataclass - no source node
     * - Regular: `class MyClass:` - has source code node
     * - Synthesized: Built-in `len` function - no user source code
     */
    export const enum TypeHandleDeclarationKind {
        Regular, // Declaration exists in source code with AST node
        Synthesized, // Declaration created by type checker (no source node)
    }

    /**
     * Base interface for all declaration types.
     * Provides the discriminator field for the TypeHandleDeclaration union.
     *
     * This is a generic interface that is extended by:
     * - TypeHandleRegularDeclaration (kind = Regular)
     * - TypeHandleSynthesizedDeclaration (kind = Synthesized)
     *
     * The type parameter T ensures that the kind field matches the implementing interface.
     *
     * Used for type-safe discrimination:
     * ```typescript
     * if (declaration.kind === TypeHandleDeclarationKind.Regular) {
     *     // TypeScript knows this is TypeHandleRegularDeclaration
     *     const node = declaration.node;
     * }
     * ```
     */
    export interface TypeHandleDeclarationBase<T extends TypeHandleDeclarationKind> {
        // Discriminator field that determines which declaration variant this is.
        // Regular: Has source code and AST node
        // Synthesized: Created by type checker, no source node
        kind: T;
    }

    /**
     * Represents a declaration that exists in source code.
     * Points to the actual AST node where a symbol is declared.
     *
     * Fields:
     * - category: Type of declaration (Variable, Function, Class, etc.)
     * - node: AST node pointing to the declaration location
     * - name: Name of the declared symbol (undefined for anonymous/implicit declarations)
     *
     * Examples:
     * ```python
     * def my_function(x: int) -> str:  # Function declaration
     *     return str(x)
     *
     * class MyClass:  # Class declaration
     *     x: int      # Variable declaration
     *
     * T = TypeVar('T')  # TypeParam declaration
     * ```
     */
    export interface TypeHandleRegularDeclaration extends TypeHandleDeclarationBase<TypeHandleDeclarationKind.Regular> {
        // Category of the declaration (Variable, Function, Class, etc.).
        // Determines how the declaration should be interpreted.
        // Example: DeclarationCategory.Function for `def foo():`.
        category: DeclarationCategory;

        // AST node pointing to the declaration location in source code.
        // Contains file URI and range information.
        // Example: Points to the `def` keyword and function name for function declarations.
        node: Node;

        // Name of the declared symbol, or undefined for anonymous declarations.
        // Example: "foo" for `def foo():`, undefined for lambda functions.
        name: string | undefined;
    }

    /**
     * Represents a synthesized declaration (not in source code).
     * Used for implicitly created symbols like built-in types or decorator-generated members.
     *
     * Fields:
     * - uri: The file URI where this is conceptually declared (often the module using it)
     *
     * Examples:
     * ```python
     * # Built-in functions have synthesized declarations
     * len([1, 2, 3])  # len is synthesized, not from source
     *
     * # @dataclass generates __init__, __eq__, etc. - synthesized declarations
     * @dataclass
     * class Point:
     *     x: int
     *     y: int
     * # Point.__init__ is synthesized
     * ```
     */
    export interface TypeHandleSynthesizedDeclaration
        extends TypeHandleDeclarationBase<TypeHandleDeclarationKind.Synthesized> {
        // URI of the file where this symbol is conceptually declared.
        // For built-ins, this might be a special URI; for decorator-generated code,
        // it's the file containing the decorator.
        // Example: File URI of a @dataclass-decorated class for synthesized __init__.
        uri: string;
    }

    /**
     * Union type representing any kind of declaration.
     * A declaration describes where and how a symbol (variable, function, class, etc.) is defined.
     *
     * Contains either:
     * - TypeHandleRegularDeclaration: For declarations in source code with AST nodes
     * - TypeHandleSynthesizedDeclaration: For declarations created by the type checker
     *
     * Used for:
     * - Tracking where symbols are defined
     * - Navigating to declaration locations (Go to Definition)
     * - Distinguishing user code from generated/built-in code
     * - Providing context for type information
     *
     * Examples:
     * ```python
     * # Regular declaration
     * def my_function(x: int) -> str:  # TypeHandleRegularDeclaration
     *     return str(x)
     *
     * # Synthesized declaration
     * @dataclass
     * class Point:
     *     x: int
     *     y: int
     * # Point.__init__ has TypeHandleSynthesizedDeclaration (generated by @dataclass)
     *
     * # Built-in function
     * len([1, 2, 3])  # len has TypeHandleSynthesizedDeclaration
     * ```
     */
    export type TypeHandleDeclaration = TypeHandleRegularDeclaration | TypeHandleSynthesizedDeclaration;

    /**
     * Describes the variance of a type parameter in a generic type.
     * Variance controls how subtyping relationships work with generic types.
     *
     * Variance rules:
     * - Covariant: If A is a subtype of B, then Generic[A] is a subtype of Generic[B]
     *   - Used when the type parameter appears only in output positions (return types)
     *   - Example: Tuple[T] is covariant in T
     *
     * - Contravariant: If A is a subtype of B, then Generic[B] is a subtype of Generic[A]
     *   - Used when the type parameter appears only in input positions (parameters)
     *   - Example: Callable[[T], None] is contravariant in T
     *
     * - Invariant: No subtyping relationship exists regardless of T
     *   - Used when the type parameter appears in both input and output positions
     *   - Example: List[T] is invariant in T
     *
     * Examples:
     * ```python
     * from typing import TypeVar, Generic
     *
     * T_co = TypeVar('T_co', covariant=True)      # Covariant
     * T_contra = TypeVar('T_contra', contravariant=True)  # Contravariant
     * T = TypeVar('T')  # Invariant by default
     *
     * class Container(Generic[T_co]):  # Covariant
     *     def get(self) -> T_co: ...   # T_co in output position only
     *
     * class Consumer(Generic[T_contra]):  # Contravariant
     *     def accept(self, value: T_contra) -> None: ...  # T_contra in input only
     * ```
     */
    export const enum Variance {
        Auto, // Variance not yet determined, will be inferred
        Unknown, // Variance cannot be determined
        Invariant, // No subtyping relationship (default for mutable types)
        Covariant, // Preserves subtyping: Generic[Child] <: Generic[Parent]
        Contravariant, // Reverses subtyping: Generic[Parent] <: Generic[Child]
    }

    /**
     * Contains metadata about a type alias.
     * Used when a type is created through a type alias statement (PEP 613) or traditional assignment.
     *
     * Fields:
     * - name: Short name of the alias
     * - fullName: Fully qualified name including module path
     * - moduleName: Module where the alias is defined
     * - fileUri: File location of the alias definition
     * - scopeId: Scope identifier for the alias (for scoped type variables)
     * - isTypeAliasType: True if this uses the `type` keyword (PEP 695)
     * - typeParams: Generic type parameters declared by the alias
     * - typeArgs: Concrete type arguments when the alias is specialized
     * - computedVariance: Inferred variance for type parameters
     *
     * Examples:
     * ```python
     * # PEP 695 style (isTypeAliasType=true)
     * type IntList = list[int]
     *
     * # Traditional style (isTypeAliasType=false)
     * IntList = list[int]
     *
     * # Generic alias with type parameters
     * type Pair[T] = tuple[T, T]
     * # typeParams=[T], can be specialized to Pair[int]
     *
     * # Using typing.TypeAlias
     * from typing import TypeAlias
     * UserId: TypeAlias = int
     * ```
     */
    export interface TypeHandleTypeAliasInfo {
        // Short name of the type alias.
        // Example: "IntList" for `type IntList = list[int]`.
        readonly name: string;

        // Fully qualified name including module path.
        // Example: "mymodule.IntList".
        readonly fullName: string;

        // Module where the type alias is defined.
        // Example: "mymodule" for a type defined in mymodule.py.
        readonly moduleName: string;

        // URI of the file containing the type alias definition.
        // Example: "file:///path/to/mymodule.py".
        readonly fileUri: string;

        // Scope identifier for type variables used in this alias.
        // Ensures type variables are scoped to this alias definition.
        // Example: Different aliases can use the same type variable name 'T' without conflict.
        readonly scopeId: string;

        // True if this alias uses the `type` keyword (PEP 695), false for traditional assignment.
        // Example: true for `type X = int`, false for `X = int`.
        readonly isTypeAliasType: boolean;

        // Generic type parameters declared by this alias.
        // Example: [T] for `type Pair[T] = tuple[T, T]`.
        readonly typeParams?: TypeHandle[];

        // Concrete type arguments when this alias is specialized.
        // Example: [int] when `Pair[int]` is used (specializing Pair[T]).
        readonly typeArgs?: TypeHandle[];

        // Computed variance for each type parameter.
        // Inferred based on how type parameters are used in the alias definition.
        // Example: [Covariant] if the type parameter only appears in return positions.
        readonly computedVariance?: Variance[];
    }

    /**
     * Base interface for all TypeHandle variants.
     * Provides common fields shared by all type representations in the protocol.
     *
     * This is the foundation interface extended by all TypeHandle types:
     * - BuiltInTypeHandle
     * - RegularTypeHandle (and its subclasses FunctionTypeHandle, ClassTypeHandle)
     * - UnionTypeHandle
     * - ModuleTypeHandle
     * - TypeVarTypeHandle
     * - SynthesizedOverloadedTypeHandle
     * - SynthesizedFunctionTypeHandle
     * - SynthesizedClassTypeHandle
     * - TypeReferenceTypeHandle
     *
     * The type parameter T constrains the `kind` field to match the implementing type.
     *
     * Common fields:
     * - id: Unique identifier for cycle detection and caching
     * - kind: Discriminator for the TypeHandle union
     * - flags: Characteristics of the type (Instantiable, Instance, Callable, etc.)
     * - typeAliasInfo: Optional alias information if type comes from a type alias
     *
     * Used throughout the protocol to represent Python types in a serializable format.
     */
    export interface TypeHandleBase<T extends TypeHandleKind> {
        // Unique identifier for this type instance. Used to detect cycles and cache type lookups.
        // Example: During recursive type resolution, the id is checked to avoid infinite loops.
        readonly id: number;

        // Discriminator field that determines which TypeHandle variant this is.
        // Used for type narrowing when processing TypeHandle unions.
        // Example: `if (typeHandle.kind === TypeHandleKind.BuiltIn) { ... }`
        readonly kind: T;

        // Bitfield of TypeFlags that describe characteristics of the type.
        // Common flags: Instantiable (can create instances), Instance (is an instance),
        // Callable (has __call__), Literal (is a literal value), Generic (has type parameters).
        // Example: Check if type is callable: `(flags & TypeFlags.Callable) !== 0`
        readonly flags: TypeFlags;

        // Information about type aliases. Present when this type was created from a type alias.
        // Contains the alias name, module, file location, type parameters, and type arguments.
        // Example: `type MyList = list[int]` - typeAliasInfo contains name="MyList", typeArgs=[int]
        readonly typeAliasInfo?: TypeHandleTypeAliasInfo;
    }

    /**
     * Represents special built-in types that are fundamental to Python's type system.
     * These are not regular classes but represent special semantic meanings.
     *
     * Used for:
     * - Type inference failures (unknown)
     * - Gradual typing (any)
     * - Uninitialized variables (unbound)
     * - Special literals (ellipsis for ...)
     * - Non-returning functions (never/noreturn)
     *
     * Examples:
     * - `unknown`: `x` in `def foo(x):` with no type hints and no usage to infer from
     * - `any`: Explicit `Any` annotation or from untyped imports
     * - `unbound`: Variable declared but not yet assigned: `x: int` (before assignment)
     * - `ellipsis`: The `...` in `def foo(...): ...` or `Tuple[int, ...]`
     * - `never`: `def raise_error() -> Never:` or function with only raise statements
     */
    export interface BuiltInTypeHandle extends TypeHandleBase<TypeHandleKind.BuiltIn> {
        // Optional declaration information for built-in types (usually undefined for true built-ins).
        // Example: Some built-ins like __class__ have synthesized declarations.
        readonly declaration?: TypeHandleDeclaration;

        // The name of the built-in type. Limited to specific known built-in types.
        // 'unknown': Type cannot be determined
        // 'any': Accepts any value (gradual typing)
        // 'unbound': Variable not yet bound to a value
        // 'ellipsis': The ... literal
        // 'never': Type that never occurs (e.g., function that always raises)
        // 'noreturn': Function that doesn't return (alias for never)
        readonly name: 'unknown' | 'any' | 'unbound' | 'ellipsis' | 'never' | 'noreturn';

        // For 'unknown' types, this may contain a possible type based on context.
        // Used when type inference has partial information but can't fully determine the type.
        // Example: In `if isinstance(x, int): ...` the possibleType of unknown x might be int
        readonly possibleType?: TypeHandle;
    }

    /**
     * Base type for symbols that have a declaration in source code.
     * This is the common parent for FunctionTypeHandle and ClassTypeHandle when the type
     * comes from an actual declaration node in the parse tree.
     *
     * Used for:
     * - Functions and methods with actual `def` statements
     * - Classes with actual `class` statements
     * - Variables with declarations in source
     *
     * Not used for:
     * - Synthesized types (use SynthesizedFunctionTypeHandle or SynthesizedClassTypeHandle)
     * - Built-in types (use BuiltInTypeHandle)
     *
     * Example:
     * ```python
     * def my_function(x: int) -> str:  # Regular function declaration
     *     return str(x)
     * ```
     */
    export interface RegularTypeHandle extends TypeHandleBase<TypeHandleKind.Regular> {
        // Declaration node information (source location, category, name).
        // Points to where this type was declared in the source code.
        // Example: For a function, this contains the node pointing to the 'def' keyword and function name.
        readonly declaration: TypeHandleDeclaration;
    }

    /**
     * Represents a function or method that has a declaration in the source code.
     * Used for functions parsed from actual `def` statements.
     *
     * Used for:
     * - User-defined functions with `def` statements
     * - Methods declared in source classes
     * - Lambda functions (though simple ones)
     *
     * Not used for:
     * - Built-in functions like `len`, `print` (use SynthesizedFunctionTypeHandle)
     * - Synthesized methods from decorators like @dataclass (use SynthesizedFunctionTypeHandle)
     *
     * Example:
     * ```python
     * def calculate(x: int, y: int) -> int:
     *     return x + y
     *
     * class MyClass:
     *     def method(self, value: str) -> None:
     *         pass
     * ```
     */
    export interface FunctionTypeHandle extends RegularTypeHandle {
        // The return type annotation of the function.
        // Example: In `def foo() -> int:`, returnType is the int type.
        readonly returnType?: TypeHandle;

        // Specialized versions of parameter types and return type when the function has type parameters.
        // Contains concrete types substituted for generic type variables.
        // Example: When calling `list[int].append(1)`, the self parameter is specialized to list[int].
        readonly specializedTypes?: SpecializedFunctionTypes;

        // Type of the first parameter that was removed when binding a method to an instance.
        // Example: When accessing `obj.method`, the `self` parameter is stripped and stored here.
        readonly strippedFirstParamType?: TypeHandle;

        // The class or object instance that this method is bound to.
        // Example: In `obj.method`, boundToType is the type of `obj`.
        readonly boundToType?: TypeHandle;
    }

    /**
     * Represents a class or class instance that has a declaration in the source code.
     * Used for classes parsed from actual `class` statements.
     *
     * Used for:
     * - User-defined classes with `class` statements
     * - Class instances (instances of user-defined classes)
     * - Specialized generic classes (e.g., `MyClass[int]`)
     * - Literal instances (e.g., the number `42` is an instance of `int`)
     *
     * Not used for:
     * - Built-in classes like `int`, `str`, `list` (use SynthesizedClassTypeHandle)
     * - Classes synthesized by decorators (use SynthesizedClassTypeHandle)
     *
     * Example:
     * ```python
     * class Point:
     *     x: int
     *     y: int
     *
     * class Container[T]:
     *     value: T
     *
     * # point has ClassTypeHandle (instance of Point)
     * point = Point()
     * # container has ClassTypeHandle with typeArgs=[int]
     * container: Container[int] = Container()
     * ```
     */
    export interface ClassTypeHandle extends RegularTypeHandle {
        // The literal value if this class represents a literal (e.g., int literal 42, str literal "hello").
        // Can be a primitive value, enum member, or sentinel object.
        // Example: For the literal `42`, literalValue = 42.
        readonly literalValue?: LiteralValue;

        // Type arguments when this class is a specialized generic type.
        // Example: For `list[int]`, typeArgs = [int].
        readonly typeArgs?: TypeHandle[];

        // True if this is a partial TypedDict (not all required keys are present).
        // Used during TypedDict construction and type checking.
        // Example: When constructing a TypedDict incrementally, intermediate states are partial.
        readonly isTypedDictPartial?: boolean;
    }

    /**
     * Represents a union of multiple types (Type1 | Type2 | ...).
     * Used when a value can be one of several different types.
     *
     * Used for:
     * - Explicit union type annotations using `|` or `Union[...]`
     * - Optional types (which are unions with None)
     * - Type narrowing results (e.g., after isinstance checks)
     * - Inferred types from multiple branches
     *
     * Examples:
     * ```python
     * # Explicit union annotation
     * def process(value: int | str) -> None:
     *     pass
     *
     * # Optional (union with None)
     * def find(key: str) -> str | None:
     *     return None
     *
     * # Inferred union from branches
     * if condition:
     *     x = 42        # int
     * else:
     *     x = "hello"  # str
     * # x has type int | str
     * ```
     */
    export interface UnionTypeHandle extends TypeHandleBase<TypeHandleKind.Union> {
        // Array of types that make up this union.
        // Example: For `int | str | None`, subTypes = [int, str, None].
        readonly subTypes: TypeHandle[];
    }

    /**
     * Represents a Python module as a type.
     * Used when a module object itself is referenced (not its contents).
     *
     * Used for:
     * - Module imports: `import os` makes `os` a ModuleType
     * - Module attributes accessed via __file__, __name__, etc.
     * - Submodule references: `os.path` is also a ModuleType
     *
     * The loaderFields contain all the symbols exported by the module that would
     * be accessible via attribute access (module.symbol_name).
     *
     * Examples:
     * ```python
     * import os
     * import os.path as path
     * from typing import Protocol
     *
     * # `os` has ModuleTypeHandle with loaderFields containing {"path": ..., "getcwd": ..., etc.}
     * # `path` has ModuleTypeHandle for the os.path module
     * # In type stubs, Protocol is a module symbol that gets loaded
     * ```
     */
    export interface ModuleTypeHandle extends TypeHandleBase<TypeHandleKind.Module> {
        // Fully qualified name of the module.
        // Example: "os.path" for the os.path module.
        readonly moduleName: string;

        // URI of the module's source file.
        // Example: "file:///path/to/module.py" or "<builtin>" for built-in modules.
        readonly uri: string;

        // Symbol table containing module-level symbols (functions, classes, variables).
        // Maps symbol names to their types as they would be accessed via module.name.
        // Example: For `import os`, loaderFields contains {"path": type of os.path, "getcwd": type of os.getcwd, ...}
        readonly loaderFields: Record<string, TypeHandle>;
    }

    /**
     * Represents a type variable (generic type parameter).
     * Used for generic programming where types are parameterized.
     *
     * Used for:
     * - Explicit TypeVar declarations: `T = TypeVar('T')`
     * - PEP 695 type parameters: `def func[T](x: T) -> T`
     * - ParamSpec for callable signatures: `P = ParamSpec('P')`
     * - TypeVarTuple for variadic generics: `Ts = TypeVarTuple('Ts')`
     * - Constrained type variables: `T = TypeVar('T', int, str)`
     * - Bounded type variables: `T = TypeVar('T', bound=Number)`
     *
     * Examples:
     * ```python
     * # Classic TypeVar
     * T = TypeVar('T')
     * def identity[T](x: T) -> T:
     *     return x
     *
     * # Bounded TypeVar
     * T_num = TypeVar('T_num', bound=int)
     * def double[T_num](x: T_num) -> T_num:
     *     return x * 2
     *
     * # Constrained TypeVar
     * T_str_or_bytes = TypeVar('T_str_or_bytes', str, bytes)
     *
     * # ParamSpec
     * P = ParamSpec('P')
     * def decorator(func: Callable[P, R]) -> Callable[P, R]:
     *     ...
     * ```
     */
    export interface TypeVarTypeHandle extends TypeHandleBase<TypeHandleKind.TypeVar> {
        // Name of the type variable.
        // Example: "T" in `def foo[T](x: T) -> T:`
        readonly name: string;

        // Flags indicating if this is a ParamSpec or TypeVarTuple.
        // ParamSpec (PEP 612): Represents parameter specifications for generic callables.
        // TypeVarTuple (PEP 646): Represents variable-length tuple of types.
        // Example: `P = ParamSpec('P')` has IsParamSpec flag set.
        readonly typeVarFlags: TypeVarFlags;

        // Upper bound constraint on the type variable.
        // Example: `T = TypeVar('T', bound=int)` restricts T to int and its subtypes.
        readonly boundType?: TypeHandle;

        // List of allowed types (constraints) for this type variable.
        // Example: `T = TypeVar('T', int, str)` constrains T to be either int or str.
        readonly constraintTypes?: TypeHandle[];

        // Unique identifier scoping this TypeVar to a specific function or class.
        // Necessary to differentiate TypeVars with the same name in different scopes.
        // Example: Two functions `def f[T]()` and `def g[T]()` have different scopeIds.
        readonly scopeId?: string;

        // Human-readable name of the scope (usually function or class name).
        // Used for display purposes in error messages and type representations.
        // Example: "MyClass" or "my_function"
        readonly scopeName?: string;

        // True if this TypeVar was created by the type checker (not in source code).
        // Example: Self parameter types are often synthesized.
        readonly isSynthesized?: boolean;

        // Variance declared for this type parameter (Auto, Invariant, Covariant, Contravariant).
        // Determines how subtyping works with this type parameter.
        // Example: `class Box[T_co]` declares T_co as covariant.
        readonly declaredVariance: Variance;

        // Computed variance (may differ from declared if Auto).
        // The type checker infers variance based on usage.
        // Example: If a TypeVar is used only in return positions, it's covariant.
        readonly computedVariance?: Variance;
    }

    /**
     * Represents an overloaded function with multiple signatures.
     * Used when a function has multiple `@overload` decorators defining different call signatures.
     *
     * Used for:
     * - Functions with @overload decorators
     * - Built-in functions with multiple signatures (e.g., `range(stop)` vs `range(start, stop, step)`)
     * - Methods with different signatures for different argument types
     *
     * The `overloads` array contains all the @overload signatures, and `implementation`
     * contains the actual implementation (if present).
     *
     * Examples:
     * ```python
     * from typing import overload
     *
     * @overload
     * def process(value: int) -> str: ...
     * @overload
     * def process(value: str) -> int: ...
     * def process(value: int | str) -> int | str:
     *     if isinstance(value, int):
     *         return str(value)
     *     return len(value)
     *
     * # The type of `process` is SynthesizedOverloadedTypeHandle with:
     * # - overloads = [signature for (int)->str, signature for (str)->int]
     * # - implementation = signature for (int|str)->(int|str)
     * ```
     */
    export interface SynthesizedOverloadedTypeHandle extends TypeHandleBase<TypeHandleKind.SynthesizedOverloaded> {
        // List of overload signatures for this overloaded function.
        // Each overload represents a different way the function can be called.
        // Example: For a function with @overload decorators, each overload is in this array.
        overloads: TypeHandle[];

        // The implementation signature (if present).
        // This is the actual function body, as opposed to the @overload declarations.
        // Example: The non-decorated function definition after all @overload decorators.
        implementation?: TypeHandle;
    }

    /**
     * Represents a function type that was synthesized (created by the type checker)
     * rather than parsed from a source declaration.
     *
     * Used for:
     * - Built-in functions (len, print, range, etc.)
     * - Methods synthesized by decorators (@dataclass, @property, etc.)
     * - Magic methods created implicitly (e.g., NamedTuple methods)
     * - Bound methods (when a function is accessed as an attribute)
     * - Specialized generic functions (when type parameters are substituted)
     *
     * This is more flexible than FunctionTypeHandle because it doesn't require
     * a source declaration and can represent functions created dynamically.
     *
     * Examples:
     * ```python
     * # Built-in function (synthesized)
     * result = len([1, 2, 3])  # len is a SynthesizedFunctionTypeHandle
     *
     * # Dataclass synthesized __init__
     * @dataclass
     * class Point:
     *     x: int
     *     y: int
     * # Point.__init__ is synthesized by @dataclass decorator
     *
     * # Bound method
     * my_list = [1, 2, 3]
     * append_func = my_list.append  # bound method, synthesized from list.append
     *
     * # Specialized generic
     * def identity[T](x: T) -> T: return x
     * int_identity = identity[int]  # specialized version
     * ```
     */
    export interface SynthesizedFunctionTypeHandle extends TypeHandleBase<TypeHandleKind.SynthesizedFunction> {
        // Short name of the function (not fully qualified).
        // Example: "append" for the list.append method.
        readonly name: string;

        // Fully qualified name including module and class (if method).
        // Example: "builtins.list.append" for list.append.
        readonly fullName: string;

        // Name of the module containing this function.
        // Example: "builtins" for built-in functions, "mymodule" for user code.
        readonly moduleName: string;

        // Bitfield of FunctionTypeFlags describing function characteristics.
        // Flags include: ConstructorMethod, ClassMethod, StaticMethod, AbstractMethod,
        // Generator, Async, Overloaded, Final, etc.
        // Example: Check if async: `(functionFlags & FunctionTypeFlags.Async) !== 0`
        readonly functionFlags: FunctionTypeFlags;

        // Type parameters (generic type variables) declared by this function.
        // Example: For `def foo[T](x: T) -> T:`, typeParams = [T].
        readonly typeParams: TypeHandle[];

        // List of function parameters (positional, keyword, *args, **kwargs).
        // Each FunctionParam contains name, type, default value, and category.
        // Example: For `def foo(x: int, y: str = "")`, parameters = [{name: "x", type: int, ...}, {name: "y", type: str, defaultType: str, ...}]
        readonly parameters: FunctionParam[];

        // Declared return type annotation (if present).
        // Example: In `def foo() -> int:`, declaredReturnType = int.
        readonly declaredReturnType?: TypeHandle;

        // Inferred return type based on function body analysis.
        // Used when no return type annotation is present.
        // Example: For `def foo(): return 42`, inferredReturnType = int.
        readonly inferredReturnType?: TypeHandle;

        // Documentation string (docstring) for the function.
        // Example: The string in `"""This function does X"""`
        readonly docString?: string;

        // Deprecation warning message if function is marked deprecated.
        // Example: From `@deprecated("Use new_func instead")` decorator.
        readonly deprecatedMessage?: string;

        // The class containing this method (if this is a method).
        // Example: For `list.append`, methodClass = list type.
        readonly methodClass?: TypeHandle;

        // Specialized versions of parameter types and return type (for generic functions).
        // Contains concrete types substituted for type parameters.
        // Example: When calling `list[int].append(1)`, specializedTypes contains int for the value parameter.
        readonly specializedTypes?: SpecializedFunctionTypes;

        // Type of the first parameter that was removed when binding to instance/class.
        // Example: When accessing `obj.method`, the `self` parameter type is stored here.
        readonly strippedFirstParamType?: TypeHandle;

        // The class or instance this function is bound to.
        // Example: In `obj.method`, boundToType = type of obj.
        readonly boundToType?: TypeHandle;

        // Reference to the overloaded function type if this is an overload signature.
        // Points back to the SynthesizedOverloadedTypeHandle containing this overload.
        // Example: Links an @overload signature to its parent overloaded function.
        readonly overloaded?: TypeHandle;

        // Nesting depth for type[type[...]] constructs.
        // Used to track nested instantiable class references.
        // Example: type[type[int]] has depth 2. Default is 0 if undefined.
        readonly instantiableDepth?: number;
    }

    /**
     * Represents a class type that was synthesized (created by the type checker)
     * rather than parsed from a source declaration.
     *
     * Used for:
     * - Built-in classes (int, str, list, dict, etc.)
     * - Classes from type stubs that define the Python standard library
     * - TypedDict classes created with class syntax
     * - NamedTuple classes
     * - Classes created by decorators or metaclasses
     * - Special type constructs (Protocol, Generic, etc.)
     * - Specialized generic class instances (list[int], dict[str, int])
     *
     * This is the most common class type handle and contains extensive metadata
     * about the class structure, including MRO, fields, type parameters, etc.
     *
     * Examples:
     * ```python
     * # Built-in class (synthesized)
     * x: list[int] = []  # list is SynthesizedClassTypeHandle
     *
     * # TypedDict (synthesized from class syntax)
     * class Movie(TypedDict):
     *     name: str
     *     year: int
     * # Movie is SynthesizedClassTypeHandle with typedDictEntries
     *
     * # NamedTuple (synthesized)
     * Point = NamedTuple('Point', [('x', int), ('y', int)])
     * # Point is SynthesizedClassTypeHandle with namedTupleEntries
     *
     * # Protocol (synthesized)
     * class Drawable(Protocol):
     *     def draw(self) -> None: ...
     * # Drawable is SynthesizedClassTypeHandle with ProtocolClass flag
     *
     * # Standard library class from stub
     * import os
     * stat_result = os.stat('.')  # os.stat_result is synthesized from stub
     * ```
     */
    export interface SynthesizedClassTypeHandle extends TypeHandleBase<TypeHandleKind.SynthesizedClass> {
        // Short name of the class (not fully qualified).
        // Example: "list" for the list class.
        readonly name: string;

        // Fully qualified name including module path.
        // Example: "builtins.list" for the built-in list class.
        readonly fullName: string;

        // Name of the module containing this class.
        // Example: "builtins" for built-in classes, "mymodule" for user code.
        readonly moduleName: string;

        // URI of the file where this class is defined.
        // Example: "file:///path/to/module.py" or "<builtin>" for built-in classes.
        readonly fileUri: string;

        // Bitfield of ClassTypeFlags describing class characteristics.
        // Flags include: BuiltIn, TypedDictClass, ProtocolClass, Final, EnumClass,
        // PropertyClass, RuntimeCheckable, etc.
        // Example: Check if TypedDict: `(classFlags & ClassTypeFlags.TypedDictClass) !== 0`
        readonly classFlags: ClassTypeFlags;

        // Unique identifier for the class definition source.
        // Used to distinguish between different class definitions with the same name.
        // Example: Two classes named "Point" in different modules have different typeSourceIds.
        readonly typeSourceId: number;

        // Explicitly declared metaclass (if specified with metaclass=...).
        // Example: `class MyClass(metaclass=ABCMeta):` has ABCMeta as declaredMetaclass.
        readonly declaredMetaclass?: TypeHandle;

        // Effective metaclass after inheritance and defaults.
        // Determined by walking the MRO and applying metaclass conflict resolution.
        // Example: Usually `type` for normal classes, `ABCMeta` for abstract classes.
        readonly effectiveMetaclass?: TypeHandle;

        // Documentation string (docstring) for the class.
        // Example: The string in `"""This class represents X"""`
        readonly docString?: string;

        // Direct base classes in the order they were declared.
        // Example: For `class C(A, B):`, baseClasses = [A, B].
        readonly baseClasses: TypeHandle[];

        // Method Resolution Order - linearized list of ancestor classes.
        // Used for attribute lookup and method resolution.
        // Example: For `class C(A, B):`, mro might be [C, A, B, object].
        readonly mro: TypeHandle[];

        // Symbol table mapping field/method names to their symbols.
        // Contains class members, class variables, methods, nested classes, etc.
        // Example: For `class Foo: x: int`, fields = {"x": TypeHandleSymbol for x}.
        readonly fields: Record<string, TypeHandleSymbol>;

        // Type parameters (generic type variables) declared by this class.
        // Example: For `class Box[T]:`, typeParams = [T].
        readonly typeParams: TypeHandle[];

        // Type arguments when this class is a specialized generic.
        // Example: For `list[int]`, typeArgs = [int].
        readonly typeArgs?: TypeHandle[];

        // Deprecation warning for the class itself (when used as a type).
        // Example: From `@deprecated("Use NewClass instead")` on the class.
        readonly deprecatedMessage?: string;

        // Deprecation warning when creating instances of the class.
        // Example: Warns when calling the constructor.
        readonly deprecatedInstanceMessage?: string;

        // Set of field names that are NamedTuple entries.
        // Used for classes created with typing.NamedTuple.
        // Example: For `Point = NamedTuple('Point', [('x', int), ('y', int)])`, contains {"x", "y"}.
        readonly namedTupleEntries?: Set<string>;

        // TypedDict field definitions with value types and required/readonly flags.
        // Contains both known keys and optional extra_items type.
        // Example: For `class Movie(TypedDict): name: str; year: int`, contains entries for name and year.
        readonly typedDictEntries?: TypedDictEntries;

        // Expression node for the extra_items type in a closed TypedDict.
        // Used for TypedDicts with extra_items parameter.
        // Example: In `class MyDict(TypedDict, extra_items=str):`, points to the `str` expression.
        readonly typedDictExtraItemsExpr?: Node;

        // True if this represents an empty container literal ([], {}, set()).
        // Used for type narrowing of empty collections.
        // Example: `x = []` creates a list with isEmptyContainer=true.
        readonly isEmptyContainer?: boolean;

        // True if this type represents an unpacked value (*args, **kwargs in type context).
        // Used with PEP 646 TypeVarTuple unpacking.
        // Example: In `*tuple[int, str]`, the tuple type has isUnpacked=true.
        readonly isUnpacked?: boolean;

        // True if type arguments were explicitly provided (vs inferred).
        // Affects type checking strictness.
        // Example: `list[int]` has explicit args, `list()` does not.
        readonly isTypeArgExplicit?: boolean;

        // True if type should include promoted types from type narrowing.
        // Used for tracking type guards and narrowing in conditionals.
        // Example: After `if isinstance(x, int):`, x's type includes promotions.
        readonly includePromotions?: boolean;

        // Literal value if this class instance represents a literal.
        // Can be a primitive value, enum member, or sentinel object.
        // Example: For the literal `42`, literalValue = 42.
        readonly literalValue?: LiteralValue;

        // Alternative name for special built-in types that have aliases.
        // Example: `List` (from typing) is an alias for `list`.
        readonly aliasName?: string;

        // True if this is a partial TypedDict (not all required keys are present).
        // Used during TypedDict construction and merging.
        // Example: When building a TypedDict incrementally.
        readonly isTypedDictPartial?: boolean;

        // True if this is a descriptor with asymmetric get/set types.
        // Used for properties where getter and setter have different types.
        // Example: A property that returns int but accepts int | str.
        readonly isAsymmetricDescriptor?: boolean;

        // True if this class uses __get__/__set__ for attribute access with different types.
        // Similar to isAsymmetricDescriptor but for classes implementing descriptor protocol.
        // Example: A descriptor class with different __get__ and __set__ signatures.
        readonly isAsymmetricAttributeAccessor?: boolean;

        // Information about the property's getter method (fget).
        // Contains the method type and the class declaring it.
        // Example: For `@property def x(self) -> int:`, contains info about the getter.
        readonly fgetInfo?: PropertyMethodInfo;

        // Information about the property's setter method (fset).
        // Contains the method type and the class declaring it.
        // Example: For `@x.setter def x(self, value: int):`, contains info about the setter.
        readonly fsetInfo?: PropertyMethodInfo;

        // Information about the property's deleter method (fdel).
        // Contains the method type and the class declaring it.
        // Example: For `@x.deleter def x(self):`, contains info about the deleter.
        readonly fdelInfo?: PropertyMethodInfo;

        // Type of functools.partial when this represents a partial function application.
        // Used for tracking partial function types.
        // Example: `partial(func, arg1)` has the partial call type stored here.
        readonly partialCallType?: TypeHandle;
    }

    /**
     * Represents a reference to another type by its ID.
     * Used to avoid duplicating large type structures and to handle forward references.
     *
     * Used for:
     * - Deduplication: When the same type appears multiple times, subsequent occurrences
     *   can reference the first occurrence instead of duplicating all fields
     * - Cyclic references: Breaking cycles in recursive type definitions
     * - Large types: Reducing payload size for complex types used repeatedly
     *
     * This is an optimization mechanism in the protocol to keep type handles compact
     * when transmitting over the wire.
     *
     * Examples:
     * ```python
     * # Recursive type definition
     * class Node:
     *     value: int
     *     next: Node | None  # 'Node' references back to itself
     *
     * # When serializing the type of 'next', the second occurrence of Node
     * # uses TypeReferenceTypeHandle pointing to the first Node's ID
     *
     * # Repeated complex type
     * def process_lists(
     *     list1: list[dict[str, int]],
     *     list2: list[dict[str, int]],  # Can reference the type from list1
     *     list3: list[dict[str, int]]   # Can reference the type from list1
     * ) -> None:
     *     pass
     * ```
     */
    export interface TypeReferenceTypeHandle extends TypeHandleBase<TypeHandleKind.TypeReference> {
        // Identifier that references another TypeHandle by its id.
        // Used to avoid duplicating large type structures and handle forward references.
        // Example: When a type appears multiple times, later occurrences use TypeReference
        // pointing to the first occurrence's id.
        readonly typeReferenceId: number;
    }

    export type TypeHandle =
        | BuiltInTypeHandle
        | RegularTypeHandle
        | FunctionTypeHandle
        | ClassTypeHandle
        | UnionTypeHandle
        | ModuleTypeHandle
        | TypeVarTypeHandle
        | SynthesizedOverloadedTypeHandle
        | SynthesizedFunctionTypeHandle
        | SynthesizedClassTypeHandle
        | TypeReferenceTypeHandle;

    // Requests and notifications for the type server protocol.

    // Request for the computed type of a declaration or node. Computed type is the type that is inferred based on the code flow.
    //
    // Example:
    // def foo(a: int | str):
    //     if instanceof(a, int):
    //        b = a + 1  # Computed type of 'b' is 'int'
    export namespace GetComputedTypeHandleRequest {
        export const method = 'typeServer/getComputedTypeHandle' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            { arg: TypeHandleDeclaration | Node; snapshot: number },
            TypeHandle | undefined,
            never,
            void,
            void
        >(method);
    }

    // Request for the declared type of a declaration or node. Declared type is the type that is explicitly declared in the source code.
    //
    // Example:
    // def foo(a: int | str): # Declared type of parameter 'a' is 'int | str'
    //     pass
    export namespace GetDeclaredTypeHandleRequest {
        export const method = 'typeServer/getDeclaredTypeHandle' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            { arg: TypeHandleDeclaration | Node; snapshot: number },
            TypeHandle | undefined,
            never,
            void,
            void
        >(method);
    }

    // Request for the expected type of a declaration or node. Expected type is the type that the context expects.
    //
    // Example:
    // def foo(a: int | str):
    //     pass
    // foo(4)  # Expected type of argument 'a' is 'int | str'
    export namespace GetExpectedTypeHandleRequest {
        export const method = 'typeServer/getExpectedTypeHandle' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            { arg: TypeHandleDeclaration | Node; snapshot: number },
            TypeHandle | undefined,
            never,
            void,
            void
        >(method);
    }

    /**
     * Request to get the search paths that the type server uses for Python modules.
     */
    export namespace GetPythonSearchPathsRequest {
        export const method = 'typeServer/getPythonSearchPaths' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            GetPythonSearchPathsParams,
            string[] | undefined,
            never,
            void,
            void
        >(method);
    }

    /**
     * Request from client to get the current snapshot of the type server.
     * A snapshot is a point-in-time representation of the type server's state, including all loaded files and their types.
     * A type server should change its snapshot whenever any type it might have returned is no longer valid. Meaning types are
     * only usable for the snapshot they were returned with.
     *
     * Snapshots are not meant to survive any changes that would make the type server throw away its internal cache. They are merely an
     * identifier to indicate to the client that the type server will accept requests for types from that snapshot.
     */
    export namespace GetSnapshotRequest {
        export const method = 'typeServer/getSnapshot' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType0<number, never, void, void>(method);
    }

    /**
     * Request to get the version of the protocol the type server supports.
     *
     * Returns a string representation of the protocol version (should be semver format)
     */
    export namespace GetSupportedProtocolVersionRequest {
        export const method = 'typeServer/getSupportedProtocolVersion' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType0<string, never, void, void>(method);
    }

    /**
     * Request to resolve an import. This is used to resolve the import name to its location in the file system.
     */
    export namespace ResolveImportRequest {
        export const method = 'typeServer/resolveImport' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<ResolveImportParams, string | undefined, never, void, void>(method);
    }

    /**
     * Notification sent by the server to indicate any outstanding snapshots are invalid.
     */
    export namespace SnapshotChangedNotification {
        export const method = 'typeServer/snapshotChanged' as const;
        export const messageDirection = MessageDirection.serverToClient;
        export const type = new ProtocolNotificationType<{ old: number; new: number }, void>(method);
    }
}

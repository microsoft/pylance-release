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

    // Represents a node in an AST (Abstract Syntax Tree) or similar structure.
    export interface Node {
        // URI of the source file containing this node.
        uri: string;
        // The range of the node in the source file.
        // This is a zero-based range, meaning the start and end positions are both zero-based
        // The range uses character offsets the same way the LSP does.
        range: Range;
    }

    export enum TypeServerVersion {
        v0_1_0 = '0.1.0',
        current = '0.2.0', // The current version of the type server protocol.
    }

    // Represents a category of a type, such as class, function, variable, etc.
    export const enum TypeCategory {
        // Type can be anything
        Any,
        // Callable type
        Function,
        // Functions defined with @overload decorator
        Overloaded,
        // Class definition
        Class,
        // Module instance
        Module,
        // Union of two or more other types
        Union,
        // Type variable
        TypeVar,
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
    }

    // Flags that describe the characteristics of a function or method.
    // These flags can be combined using bitwise operations.
    export const enum FunctionFlags {
        None = 0,
        Async = 1 << 0, // Indicates if the function is asynchronous.
        Generator = 1 << 1, // Indicates if the function is a generator (can yield values).
        Abstract = 1 << 2, // Indicates if the function is abstract (must be implemented in a subclass).
        Static = 1 << 3, // Indicates if the function has a @staticmethod decorator.
        // The *args and **kwargs parameters do not need to be present for this
        // function to be compatible. This is used for Callable[..., x] and
        // ... type arguments to ParamSpec and Concatenate.
        GradualCallableForm = 1 << 4,
    }

    // Flags that describe the characteristics of a class.
    // These flags can be combined using bitwise operations.
    export const enum ClassFlags {
        None = 0,
        Enum = 1 << 0, // Indicates if the class is an enum (a special kind of class that defines a set of named values).
        TypedDict = 1 << 1, // Indicates if the class is a TypedDict or derived from a TypedDict (a special kind of class that defines a dictionary with specific keys and types).
    }

    // Flags that describe the characteristics of a type variable.
    // These flags can be combined using bitwise operations.
    export const enum TypeVarFlags {
        None = 0,
        IsParamSpec = 1 << 0, // Indicates if the type variable is a ParamSpec (as defined in PEP 612).
        IsTypeVarTuple = 1 << 1, // Indicates if the type variable is a TypeVarTuple (as defined in PEP 646).
    }

    export interface ModuleName {
        // The leading dots in the module name. This is used to determine the relative import level.
        leadingDots: number;
        // The parts of the module name, split by dots. For example, for `my_module.sub_module`, this would be `['my_module', 'sub_module']`.
        nameParts: string[];
    }

    // Flags that describe how/what properties are fetched from a type.
    export const enum FetchPropertiesFlags {
        None = 0,
        All = 0xffffffff, // Indicates all flags are set.
    }

    // Backing flags type used by request params to specify which properties to fetch.
    // Alias provided to satisfy consumer request for singular name while retaining existing enum.
    export type FetchPropertyFlags = FetchPropertiesFlags;

    export interface Properties {
        fetchedPropertiesFlags: FetchPropertiesFlags;
    }

    export interface AnyProperties extends Properties {
        // Add type `Any` specific properties here.
    }

    export interface FunctionProperties extends Properties {
        // Add function specific properties here.
    }

    export interface OverloadedProperties extends Properties {
        // Add overloaded function specific properties here.
    }

    export interface ClassProperties extends Properties {
        // Add class specific properties here.
    }

    export interface ModuleProperties extends Properties {
        // Add module specific properties here.
    }

    export interface UnionProperties extends Properties {
        // Add union specific properties here.
    }

    export interface TypeVarProperties extends Properties {
        // Add type variable specific properties here.
    }

    export interface Type {
        // Unique identifier for the type definition within the snapshot. A handle doesn't need to exist beyond
        // the lifetime of the snapshot.
        //
        // It can be used by the Type Server to reference internal information about a type when the
        // type is returned in a subsequent request.
        //
        // When the internal snapshot is changed, all outstanding handles should be invalid and no longer usable.
        handle: string | number;

        // Essential classification of the Type.
        category: TypeCategory;

        // Flags describing the type.
        flags: TypeFlags;

        // Name of the module the type comes from
        moduleName: ModuleName | undefined;

        // Simple name of the type. For example, for a class `MyClass` in module `my_module`, this would be `MyClass`.
        name: string;

        // The typing module defines aliases for builtin types
        // (e.g. Tuple, List, Dict). This field holds the alias
        // name.
        aliasName?: string | undefined;

        // Flags specific to the category. For example, for a class type, this would be ClassFlags.
        // For a function type, this would be FunctionFlags.
        categoryFlags: number;

        // Properties specific to the category, such as function parameters.
        // These properties will be returned optionally if requested with `fetchPropertiesFlags`.
        categoryProperties?: Properties;

        // Declaration of the type, if available.
        decl: Declaration | undefined;
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

    export const enum DeclarationFlags {
        None = 0,
        ClassMember = 1 << 0, // Indicates if the declaration is a method (a function defined within a class).
        Constant = 1 << 1, // Indicates if the declaration is a constant (a variable that cannot be changed).
        Final = 1 << 2, // Indicates if the declaration is final variable (a class that cannot be subclassed).
        IsDefinedBySlots = 1 << 3, // Indicates if the declaration is defined by slots (a class that uses __slots__).
        UsesLocalName = 1 << 4, // Indicates if the import declaration uses 'as' with a different name (ex: import foo as f).
        UnresolvedImport = 1 << 5, // Indicates if the import declaration is unresolved (the module or symbol could not be found).
        SimpleParam = 1 << 6, // Indicates if the declaration is a simple parameter (e.g., a function parameter).
        ArgsListParam = 1 << 7, // Indicates if a declaration is an argument list (e.g., `*args`).
        KwargsDictParam = 1 << 8, // Indicates if the declaration is a keyword argument dictionary (e.g., `**kwargs`).
        PositionalParam = 1 << 9, // Indicates if the declaration is a positional parameter.
        StandardParam = 1 << 10, // Indicates if the declaration is a standard parameter.
        KeywordParam = 1 << 11, // Indicates if the declaration is a keyword parameter.
        ExpandedArgsParam = 1 << 12, // Indicates if the declaration is an expanded *args parameter.
        ReturnType = 1 << 13, // Indicates if the declaration is a return type (e.g., the return value of a function).
        EnumMember = 1 << 14, // Indicates if the declaration is a member of an enum type.
        TypeDeclared = 1 << 15, // Indicates if the declaration has an explicitly declared type.
        SpecializedType = 1 << 16, // Indicates if the declaration is a specialization of a generic type.
    }

    // Represents a symbol declaration in the type system.
    // A declaration is a specific instance of a symbol in the source code, such as a variable, function, or class.
    export interface Declaration {
        // Unique identifier for the declaration within the session.
        handle: string | number;

        // Category of this symbol (function, variable, etc.).
        category: DeclarationCategory;

        // Extra information about the declaration.
        flags: DeclarationFlags;

        // Parse node associated with the declaration
        node?: Node;

        // The dot-separated import name for the file that
        // contains the declaration (may not be definitive
        // because a source file can be accessed via different
        // import names in some cases).
        moduleName: ModuleName;

        // The symbol name for the declaration (as the user sees it)
        name: string;

        // The file that contains the declaration.
        // Unless this is an import declaration, then the uri refers to the file
        // the import is referring to.
        uri: string;
    }

    // Flags that are used for searching for symbols.
    export const enum SymbolSearchFlags {
        None = 0,
        SkipInstanceAttributes = 1 << 0, // Skip instance attributes when searching for attributes of a type.
        SkipTypeBaseClass = 1 << 1, // Skip members from the base class of a type when searching for members of a type.
        SkipAttributeAccessOverrides = 1 << 2, // Skip attribute access overrides when searching for members of a type.
        GetBoundAttributes = 1 << 3, // Look for bound attributes when searching for attributes of a type. That is methods bound specifically to an instance.
        SkipUnreachableCode = 1 << 4, // When searching for a name, skip symbols that are in unreachable code.
    }

    export const enum SymbolFlags {
        None = 0,
        SynthesizedName = 1 << 0, // Indicates if the symbol name was synthesized by the type server and not present in the source code.
    }

    // Symbol information for a node
    export interface Symbol {
        // The name of the symbol found.
        name: string;
        // The type of the symbol found.
        type: TypeServerProtocol.Type;
        // The declarations for the symbol.
        // This can include multiple declarations for the same symbol, such as when a symbol is defined in multiple files.
        decls: Declaration[];
        // Flags giving more information about the symbol.
        flags: SymbolFlags;
        // The type that is the semantic parent of this symbol. For example if the symbol is for a parameter,
        // the parent would be the function or method that contains the parameter.
        // If the symbol is for a class member, the parent would be the class that contains the member.
        parent?: Type;
    }

    // Options for resolving an import declaration.
    // TODO: See if we can remove this as these are pretty specific to Pyright at the moment.
    export interface ResolveImportOptions {
        resolveLocalNames?: boolean; // Whether to resolve local names in the import declaration.
        allowExternallyHiddenAccess?: boolean; // Whether to allow access to members that are hidden by external modules.
        skipFileNeededCheck?: boolean; // Whether to skip checking if the file is needed for the import  resolution.
    }

    // Parameters for resolving an import
    export interface ResolveImportParams {
        // The URI of the source file where the import is referenced.
        sourceUri: string;
        // The descriptor of the imported module.
        moduleDescriptor: ModuleName;
        snapshot: number;
    }

    // Flags that control how type representations are formatted.
    export const enum TypeReprFlags {
        None = 0,
        // Turn type aliases into their original type.
        ExpandTypeAliases = 1 << 0,
        // Print the variance of a type parameter.
        PrintTypeVarVariance = 1 << 1,
        // Convert the type into an instance type before printing it.
        ConvertToInstanceType = 1 << 2,
        // Limit output to legal Python syntax.
        PythonSyntax = 1 << 3,
    }

    export interface GetSymbolsForTypeParams {
        // The type for which the symbols are being requested. If this is a class, the symbols are based on the members of the class. If this is
        // a function, the symbols are the parameters and the return value.
        type: Type;
        // The location where the symbols are being requested. This can help search for symbols.
        node: Node | undefined;
        // The name to search for. If undefined, returns all the symbols for the type or node.
        name: string | undefined;
        // Flags used to do the search
        flags: SymbolSearchFlags;
        // The snapshot version of the type server state.
        snapshot: number;
        // Flags indicating which properties to fetch for the type (if any).
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetSymbolsForNodeParams {
        // The location to search for symbols from. This node is essentially used to scope the symbol search. It can be a Module node
        // in order to search for top level symbols.
        node: Node;
        // The name to search for. If undefined, returns all the symbols for the type or node.
        name: string | undefined;
        // Flags used to do the search
        flags: SymbolSearchFlags;
        // The snapshot version of the type server state.
        snapshot: number;
        // Flags indicating which properties to fetch for the type (if any).
        fetchPropertiesFlags?: FetchPropertyFlags;
    }
    export interface GetBuiltinTypeParams {
        // The node that is used to scope the builtin type. Every module may have a different set of builtins based on
        // where the module is located.
        scopingNode: Node;
        // The name of the builtin type being requested.
        name: string;
        // The snapshot version of the type server state.
        snapshot: number;
        // Flags indicating which properties to fetch for the type (if any).
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface TypeAliasInfo {
        // The original name of the alias.
        name: string;
        // The arguments for the type alias, if any.
        typeArgs: Type[] | undefined;
    }

    // Parameter interfaces for requests
    export interface CombineTypesParams {
        types: Type[];
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface CreateInstanceTypeParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface FetchTypePropertiesParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags: FetchPropertyFlags;
    }

    export interface GetDocStringParams {
        type: Type | undefined;
        decl: Declaration;
        boundObjectOrClass: Type | undefined;
        snapshot: number;
    }

    export interface GetMatchingOverloadsParams {
        callNode: Node;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetMetaclassParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetOverloadsParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetPythonSearchPathsParams {
        fromUri: string;
        snapshot: number;
    }

    export interface GetReprParams {
        type: Type;
        flags: TypeReprFlags;
        snapshot: number;
    }

    export interface GetTypeAliasInfoParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetTypeArgsParams {
        type: Type;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetTypeOfDeclarationParams {
        decl: Declaration;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface GetTypeParams {
        node: Node;
        snapshot: number;
        fetchPropertiesFlags?: FetchPropertyFlags;
    }

    export interface ResolveImportDeclarationParams {
        decl: Declaration;
        options: ResolveImportOptions;
        snapshot: number;
    }

    // Requests and notifications for the type server protocol.

    /**
     * Request to combine types. This is used to combine multiple types into a single type.
     * Example:
     * `if (someCondition) { x = 1 } else { x = "hello" }`. The combined type of `x` would be `int | str`.
     */
    export namespace CombineTypesRequest {
        export const method = 'typeServer/combineTypes' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<CombineTypesParams, Type | undefined, never, void, void>(method);
    }

    /**
     * Request to generate an instance type representation for the provided type.
     * Example:
     * Given a class type 'type[MyClass]', the resulting instance type is represented as 'MyClass'.
     */
    export namespace CreateInstanceTypeRequest {
        export const method = 'typeServer/createInstanceType' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<CreateInstanceTypeParams, Type | undefined, never, void, void>(
            method
        );
    }

    /**
     * Request to fetch category properties for the given type.
     */
    export namespace FetchTypePropertiesRequest {
        export const method = 'typeServer/fetchTypeProperties' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<FetchTypePropertiesParams, Type, never, void, void>(method);
    }

    /**
     * Request to get the type information for a specific builtin type.
     */
    export namespace GetBuiltinTypeRequest {
        export const method = 'typeServer/getBuiltinType' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetBuiltinTypeParams, Type | undefined, never, void, void>(method);
    }

    /**
     * Request to get the docstring for a specific declaration.
     */
    export namespace GetDocStringRequest {
        export const method = 'typeServer/getDocString' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetDocStringParams, string | undefined, never, void, void>(method);
    }

    /**
     * Request to get the overloads that a call node matches.
     */
    export namespace GetMatchingOverloadsRequest {
        export const method = 'typeServer/getMatchingOverloads' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetMatchingOverloadsParams, Type[] | undefined, never, void, void>(
            method
        );
    }

    /**
     * Request to get the meta class of a type.
     */
    export namespace GetMetaclassRequest {
        export const method = 'typeServer/getMetaclass' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetMetaclassParams, Type | undefined, never, void, void>(method);
    }

    /**
     * Request to get all overloads of a function or method. The returned value doesn't include the implementation signature.
     */
    export namespace GetOverloadsRequest {
        export const method = 'typeServer/getOverloads' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetOverloadsParams, Type[] | undefined, never, void, void>(method);
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
     * Request to get the string representation of a type in a human-readable format. This may or may not be the same as the type's "name".
     */
    export namespace GetReprRequest {
        export const method = 'typeServer/getRepr' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetReprParams, string | undefined, never, void, void>(method);
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
     * Request to find symbols from a node.
     */
    export namespace GetSymbolsForNodeRequest {
        export const method = 'typeServer/getSymbolsForNode' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetSymbolsForNodeParams, Symbol[] | undefined, never, void, void>(
            method
        );
    }

    /**
     * Request to find symbols from a type.
     */
    export namespace GetSymbolsForTypeRequest {
        export const method = 'typeServer/getSymbolsForType' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetSymbolsForTypeParams, Symbol[] | undefined, never, void, void>(
            method
        );
    }

    /**
     * Get information about a type alias.
     * Example: `MyType = List[int]` is a type alias. In this case the List[int] is the type passed to this function but it has the Alias TypeFlag set.
     * The type alias info will return the name 'MyType' and the args [int]
     */
    export namespace GetTypeAliasInfoRequest {
        export const method = 'typeServer/getTypeAliasInfo' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            GetTypeAliasInfoParams,
            TypeAliasInfo | undefined,
            never,
            void,
            void
        >(method);
    }

    /**
     * Request to get the collection of subtypes that make up a union type or the types that makes up a generic type.
     */
    export namespace GetTypeArgsRequest {
        export const method = 'typeServer/getTypeArgs' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetTypeArgsParams, Type[] | undefined, never, void, void>(method);
    }

    /**
     * Request to get the type of a declaration.
     */
    export namespace GetTypeOfDeclarationRequest {
        export const method = 'typeServer/getTypeOfDeclaration' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetTypeOfDeclarationParams, Type | undefined, never, void, void>(
            method
        );
    }

    /**
     * Request to get the type information for a specific node.
     */
    export namespace GetTypeRequest {
        export const method = 'typeServer/getType' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<GetTypeParams, Type | undefined, never, void, void>(method);
    }

    /**
     * Request to resolve an import declaration. Example: `from module import something`. The `something` is the import declaration. Resolving it
     * means finding the actual declaration of `something` in the module.
     */
    export namespace ResolveImportDeclarationRequest {
        export const method = 'typeServer/resolveImportDeclaration' as const;
        export const messageDirection = MessageDirection.clientToServer;
        export const type = new ProtocolRequestType<
            ResolveImportDeclarationParams,
            Declaration | undefined,
            never,
            void,
            void
        >(method);
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

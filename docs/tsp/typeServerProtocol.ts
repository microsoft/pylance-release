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
    CancellationToken,
    Diagnostic,
    Disposable,
    FileEvent,
    NotificationHandler,
    RequestHandler,
    WorkspaceFolder,
} from 'vscode-languageserver';

export interface RequestSender {
    sendRequest<R>(method: string, params: any, token?: CancellationToken): Promise<R>;
}

export interface NotificationSender {
    sendNotification: (method: string, params?: any) => void;
}

export interface RequestReceiver {
    onRequest<P, R, E>(method: string, handler: RequestHandler<P, R, E>): Disposable;
}

export interface NotificationReceiver {
    onNotification<P>(method: string, handler: NotificationHandler<P>): Disposable;
}

export namespace TypeServerProtocol {
    export const ReturnAttributeName = '__return__'; // Special name for the return value of a function or method.
    export const InvalidHandle = -1; // Special value for an invalid handle. This is used to indicate that a type or declaration is not valid.

    // Represents a node in an AST (Abstract Syntax Tree) or similar structure.
    export interface Node {
        // URI of the source file containing this node.
        uri: string;
        // The start byte position (zero-based) of the node in the source file.
        // Note this is per byte and not per character.
        start: number;
        // The length of the node (in number of bytes) in the source file.
        length: number;
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
    }

    // Flags that describe the characteristics of a function or method.
    // These flags can be combined using bitwise operations.
    export const enum FunctionFlags {
        None = 0,
        Async = 1 << 0, // Indicates if the function is asynchronous.
        Generator = 1 << 1, // Indicates if the function is a generator (can yield values).
        Abstract = 1 << 2, // Indicates if the function is abstract (must be implemented in a subclass).
        Static = 1 << 3, // Indicates if the function has a @staticmethod decorator.
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
    }

    export interface ModuleName {
        // The leading dots in the module name. This is used to determine the relative import level.
        leadingDots: number;
        // The parts of the module name, split by dots. For example, for `my_module.sub_module`, this would be `['my_module', 'sub_module']`.
        nameParts: string[];
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

        // Flags specific to the category. For example, for a class type, this would be ClassFlags.
        // For a function type, this would be FunctionFlags.
        categoryFlags: number;
        // Declaration of the type, if available.
        decl: Declaration | undefined;
    }

    export const enum AttributeFlags {
        None = 0,
        IsArgsList = 1 << 0, // Indicates if a parameter is an argument list (e.g., `*args`).
        IsKwargsDict = 1 << 1, // Indicates if the attribute is a keyword argument dictionary (e.g., `**kwargs`).
    }

    export interface Attribute {
        // The name of the attribute. This is the name used to access the attribute in code.
        // For a function, this would be the name of a parameter or a special name like `__return__` for the return value.
        name: string;

        // The type of the attribute.
        type: Type;

        // The type the attribute came from (can be a class, function, module, etc.).
        owner: Type | undefined;

        // The type the attribute is bound to, if applicable.
        boundType: Type | undefined;
        // Flags describing extra data about an attribute.
        // For example, if the attribute is a parameter, this could indicate if it's a positional or keyword parameter.
        flags: number;
        // The declarations for the attribute.
        decls: Declaration[];
    }

    // Flags that are used for searching for attributes of a class Type.
    export const enum AttributeAccessFlags {
        None = 0,
        SkipInstanceAttributes = 1 << 0, // Skip instance attributes when searching for attributes of a type.
        SkipTypeBaseClass = 1 << 2, // Skip members from the base class of a type when searching for members of a type.
        SkipAttributeAccessOverride = 1 << 3, // Skip attribute access overrides when searching for members of a type.
        GetBoundAttributes = 1 << 4, // Look for bound attributes when searching for attributes of a type. That is methods bound specifically to an instance.
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

    // Symbol information for a node, which includes
    // a list of declarations and potentially synthesized types for those declarations.
    export interface Symbol {
        // The node for which the declaration information is being requested.
        node: Node;
        // The name of the symbol found.
        name: string;
        // The declarations for the symbol.
        // This can include multiple declarations for the same symbol, such as when a symbol is defined in multiple files.
        decls: Declaration[];
        // Synthesized type information for a declaration that is not directly
        // represented in the source code, but is derived from the declaration. Other languages
        // may refer to this as an anonymous type.
        synthesizedTypes: TypeServerProtocol.Type[];
    }

    export interface FileSymbolInfo {
        // The URI of the source file.
        uri: string;
        // The symbols in the file.
        symbols: Symbol[];
    }

    // Options for resolving an import declaration.
    // TODO: See if we can remove this as these are pretty specific to Pyright at the moment.
    export interface ResolveImportOptions {
        resolveLocalNames?: boolean; // Whether to resolve local names in the import declaration.
        allowExternallyHiddenAccess?: boolean; // Whether to allow access to members that are hidden by external modules.
        skipFileNeededCheck?: boolean; // Whether to skip checking if the file is needed for the import  resolution.
    }

    // Who owns file contents?
    // That depends on the file.
    // For a file that's open in an IDE, the IDE owns the file contents and forwards those contents and changes to the type server (and language server).
    // For a file that's not open in an IDE, the file system owns the file contents.
    // Changes for the file system owned files are sent to the type server (and language server) as file events.

    // Describes a file that's been opened in the language server which the type server needs to be aware of.
    export interface TextDocumentOpenParams {
        uri: string;
        text: string;
        // The version of the file, which is used to track changes to the file. It will be incremented each time the file is modified.
        version: number;
        // Optional: If the file is part of a chain of files, this can be used to indicate the URI of the
        // file that is automatically 'imported' by this file. This is useful for cases like Jupyter notebooks
        chainedFileUri?: string;
    }

    // Describes a file that's been closed in the language server which the type server needs to be aware of.
    export interface TextDocumentCloseParams {
        uri: string;
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
    }

    export interface SearchForTypeAttributeParams {
        // The starting point in the type heirarchy to search for the attribute.
        startType: Type;
        // The name of the attribute being requested.
        attributeName: string;
        // Flags that control how the attribute is accessed.
        accessFlags: AttributeAccessFlags;
        // Optional: The expression node that the member is being accessed from.
        expressionNode?: Node;
        // Optional: The type of an instance that the attribute is being accessed from.
        // Example: type of `a` in `a = MyClass()`, where `MyClass` is a class and `a` is an instance of that class.
        instanceType?: Type;
        // The snapshot version of the type server state.
        snapshot: number;
    }

    export interface GetTypeAttributesParams {
        // The type for which the attributes are being requested.
        type: Type;
        // The snapshot version of the type server state.
        snapshot: number;
    }
    export interface GetDeclarationInfoParams {
        // The node for which the declaration information is being requested.
        node: Node;
        // The name of the symbol being requested. This is optional and can be undefined especially when the node is a name node.
        // If this node is a module node, this would be the name of the symbol being requested.
        name?: string;
        // Whether to skip unreachable code when looking for the symbol declaration.
        skipUnreachableCode: boolean;
        // The snapshot version of the type server state.
        snapshot: number;
    }

    export interface GetBuiltinTypeParams {
        // The node that is used to scope the builtin type. Every module may have a different set of builtins based on
        // where the module is located.
        scopingNode: Node;
        // The name of the builtin type being requested.
        name: string;
        // The snapshot version of the type server state.
        snapshot: number;
    }

    // Represents settings that can be sent to the type server.
    export type Settings = {
        [key: string]: any;
    };

    // Parts of a function, including its parameters and return type.
    // This is used to provide a string representation of a function's signature.
    export type FunctionParts = {
        params: string[];
        returnType: string;
    };

    export interface TypeAliasInfo {
        // The original name of the alias.
        name: string;
        // The arguments for the type alias, if any.
        typeArgs: Type[] | undefined;
    }

    // Requests and notifications for the type server protocol.
    export enum Requests {
        // First request to initialize the type server.
        Initialize = 'typeServer/initialize',
        // Request from client to shut down the type server.
        ShutDown = 'typeServer/shutdown',
        // Request from client to get the current snapshot of the type server.
        // A snapshot is a point-in-time representation of the type server's state, including all loaded files and their types.
        // A type server should change its snapshot whenever any type it might have returned is no longer valid. Meaning types are
        // only usable for the snapshot they were returned with.
        //
        // Snapshots are not meant to survive any changes that would make the type server throw away its internal cache. They are merely an
        // identifier to indicate to the client that the type server will accept requests for types from that snapshot.
        GetSnapshot = 'typeServer/getSnapshot',
        // Request to get diagnostics for a specific file.
        GetDiagnostics = 'typeServer/getDiagnostics',
        // Request to get the version of diagnostics for a specific file.
        GetDiagnosticsVersion = 'typeServer/getDiagnosticsVersion',
        // Request to get the type information for a specific node.
        GetType = 'typeServer/getType',
        // Request to get the type information for a specific builtin type.
        GetBuiltinType = 'typeServer/getBuiltinType',
        // Request to get the collection of subtypes that make up a union type or the types that makes up a generic type.
        GetTypeArgs = 'typeServer/getTypeArgs',
        // Request to find an attribute of a class.
        SearchForTypeAttribute = 'typeServer/searchForTypeAttribute',
        // Request to get the attributes of a specific class or the parameters and return value of a specific function.
        GetTypeAttributes = 'typeServer/getTypeAttributes',
        // Request to get all overloads of a function or method. The returned value doesn't include the implementation signature.
        GetOverloads = 'typeServer/getOverloads',
        // Request to get the overloads that a call node matches.
        GetMatchingOverloads = 'typeServer/getMatchingOverloads',
        // Request to get the meta class of a type.
        GetMetaclass = 'typeServer/getMetaclass',
        // Request to get the type of a declaration.
        GetTypeOfDeclaration = 'typeServer/getTypeOfDeclaration',
        // Request to get symbol declaration information for a node.
        GetSymbol = 'typeServer/getSymbol',
        // Request to get all symbols for a file. This is used to get all symbols in a file.
        GetSymbolsForFile = 'typeServer/getSymbolsForFile',
        // Request to get the string representation of a function's parts, meaning its parameters and return type.
        GetFunctionParts = 'typeServer/getFunctionParts',
        // Request to get the string representation of a type in a human-readable format. This may or may not be the same as the type's "name".
        GetRepr = 'typeServer/getRepr',
        // Request to get the docstring for a specific declaration.
        GetDocString = 'typeServer/getDocString',
        // Request to resolve an import declaration. Example: `from module import something`. The `something` is the import declaration. Resolving it
        // means finding the actual declaration of `something` in the module.
        ResolveImportDeclaration = 'typeServer/resolveImportDeclaration',
        // Request to resolve an import. This is used to resolve the import name to its location in the file system.
        ResolveImport = 'typeServer/resolveImport',
        // Get information about a type alias.
        // Example: `MyType = List[int]` is a type alias. In this case the List[int] is the type passed to this function but it has the Alias TypeFlag set.
        // The type alias info will return the name 'MyType' and the args [int]
        GetTypeAliasInfo = 'typeServer/getTypeAliasInfo',
        // Request to combine types. This is used to combine multiple types into a single type.
        // Example:
        // `if (someCondition) { x = 1 } else { x = "hello" }`. The combined type of `x` would be `int | str`.
        CombineTypes = 'typeServer/combineTypes',
        // Request to get the search paths that the type server uses for Python modules.
        GetPythonSearchPaths = 'typeServer/getPythonSearchPaths',
    }

    export enum Notifications {
        // Notification sent by the server to indicate that the type server has been initialized.
        Initialized = 'typeServer/initialized',
        // Notification sent by the server to indicate that the type server has shut down.
        ShutDown = 'typeServer/shutdown',
        // Notification sent by the client to indicate that a text document has been opened.
        TextDocumentOpen = 'textDocument/open',
        // Notification sent by the client to indicate that a text document has been closed.
        TextDocumentClose = 'textDocument/close',
        // Notification sent by the client to indicate that settings have changed.
        SettingsChange = 'typeServer/settingsChange',
        // Notification sent by the client to indicate that files have changed.
        FilesChanged = 'typeServer/filesChanged',
        // Notification sent by the server to indicate any outstanding snapshots are invalid.
        SnapshotChanged = 'typeServer/snapshotChanged',
        // Notification sent by the server to indicate that diagnostics have changed and the client
        // should re-request diagnostics for the file.
        DiagnosticsChanged = 'typeServer/diagnosticsChanged',
    }

    export interface Params {
        [Requests.Initialize]: { workspace: WorkspaceFolder; initialSettings: string };
        [Requests.ShutDown]: void;
        [Requests.GetSnapshot]: void;
        [Requests.GetDiagnostics]: { uri: string; snapshot: number };
        [Requests.GetDiagnosticsVersion]: { uri: string; snapshot: number };
        [Requests.GetType]: { node: Node; snapshot: number };
        [Requests.GetBuiltinType]: GetBuiltinTypeParams;
        [Requests.GetTypeArgs]: { type: Type; snapshot: number };
        [Requests.SearchForTypeAttribute]: SearchForTypeAttributeParams;
        [Requests.GetTypeAttributes]: GetTypeAttributesParams;
        [Requests.GetOverloads]: { type: Type; snapshot: number };
        [Requests.GetMatchingOverloads]: { callNode: Node; snapshot: number };
        [Requests.GetMetaclass]: { type: Type; snapshot: number };
        [Requests.GetTypeOfDeclaration]: { decl: Declaration; snapshot: number };
        [Requests.GetRepr]: {
            type: Type;
            flags: TypeReprFlags;
            snapshot: number;
        };
        [Requests.GetFunctionParts]: {
            type: Type;
            flags: TypeReprFlags;
            snapshot: number;
        };
        [Requests.GetDocString]: {
            type: Type | undefined; // The type of declaration if known.
            decl: Declaration; // The symbol to get the docstring for.
            boundObjectOrClass: Type | undefined; // The object or class the docstring is bound to, if applicable.
            snapshot: number;
        };
        [Requests.GetSymbol]: GetDeclarationInfoParams;
        [Requests.GetSymbolsForFile]: { uri: string; snapshot: number };
        [Requests.ResolveImportDeclaration]: {
            decl: Declaration;
            options: ResolveImportOptions;
            snapshot: number;
        };
        [Requests.ResolveImport]: ResolveImportParams;
        [Requests.GetTypeAliasInfo]: {
            type: Type;
            snapshot: number;
        };
        [Requests.CombineTypes]: {
            types: Type[];
            snapshot: number;
        };
        [Requests.GetPythonSearchPaths]: { fromUri: string; snapshot: number };
        [Notifications.Initialized]: void;
        [Notifications.ShutDown]: void;
        [Notifications.TextDocumentOpen]: TextDocumentOpenParams;
        [Notifications.TextDocumentClose]: TextDocumentCloseParams;
        [Notifications.SettingsChange]: Settings;
        [Notifications.FilesChanged]: { changes: FileEvent[] };
        [Notifications.SnapshotChanged]: { old: number; new: number };
        [Notifications.DiagnosticsChanged]: { uri: string; snapshot: number; version: number };
    }

    export interface Response {
        [Requests.Initialize]: { configRoots: string[] };
        [Requests.ShutDown]: { success: boolean };
        [Requests.GetSnapshot]: number;
        [Requests.GetDiagnostics]: Diagnostic[] | undefined;
        [Requests.GetDiagnosticsVersion]: number | undefined;
        [Requests.GetType]: Type | undefined;
        [Requests.GetBuiltinType]: Type | undefined;
        [Requests.GetTypeArgs]: Type[] | undefined;
        [Requests.SearchForTypeAttribute]: Attribute | undefined;
        [Requests.GetTypeAttributes]: Attribute[] | undefined;
        [Requests.GetOverloads]: Type[] | undefined;
        [Requests.GetMatchingOverloads]: Type[] | undefined;
        [Requests.GetMetaclass]: Type | undefined;
        [Requests.GetTypeOfDeclaration]: Type | undefined;
        [Requests.GetRepr]: string | undefined;
        [Requests.GetFunctionParts]: FunctionParts | undefined;
        [Requests.GetDocString]: string | undefined;
        [Requests.GetSymbol]: Symbol | undefined;
        [Requests.GetSymbolsForFile]: FileSymbolInfo | undefined;
        [Requests.ResolveImportDeclaration]: Declaration | undefined;
        [Requests.ResolveImport]: string | undefined;
        [Requests.GetTypeAliasInfo]: TypeAliasInfo | undefined;
        [Requests.GetPythonSearchPaths]: string[] | undefined;
        [Requests.CombineTypes]: Type | undefined;
    }

    export function sendRequest<P extends Params, R extends Response, M extends Requests & keyof P & keyof R & string>(
        connection: RequestSender,
        method: M,
        params: P[M],
        token?: CancellationToken
    ): Promise<R[M]> {
        return connection.sendRequest(method, params, token);
    }

    export function sendNotification<P extends Params, M extends Notifications & keyof P & string>(
        connection: NotificationSender,
        method: M,
        params: P[M]
    ): void {
        connection.sendNotification(method, params);
    }

    export function onRequest<P extends Params, R extends Response, M extends Requests & keyof P & keyof R & string, E>(
        connection: RequestReceiver,
        method: M,
        handler: RequestHandler<P[M], R[M], E>
    ): Disposable {
        return connection.onRequest(method, handler);
    }

    export function onNotification<P extends Params, M extends Notifications & keyof P & string>(
        connection: NotificationReceiver,
        method: M,
        handler: NotificationHandler<P[M]>
    ): Disposable {
        return connection.onNotification(method, handler);
    }
}

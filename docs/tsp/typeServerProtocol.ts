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
    // Represents a node in an AST (Abstract Syntax Tree) or similar structure.
    export interface Node {
        // URI of the source file containing this node.
        uri: string;
        // Hash of the content of the source file at the time the AST was created.
        contentHash: number;
        // The start byte position (zero-based) of the node in the source file.
        // Note this is per byte and not per character.
        start: number;
        // The length of the node (in number of bytes) in the source file.
        length: number;
    }

    // Represents a category of a type, such as class, function, variable, etc.
    export const enum TypeCategory {
        Class = 0,
        Function = 1,
        Overloaded = 2,
        Module = 3,
        Variable = 4,
        Parameter = 5,
        Property = 6,
        TypeAlias = 7,
        TypeVariable = 8,
        Generic = 9,
        Unknown = 10,
        Any = 11,
        None = 12,
        Union = 13,
    }

    // Flags that describe the characteristics of a type.
    // These flags can be combined using bitwise operations.
    export const enum TypeFlags {
        None = 0,
        Instantiable = 1 << 0, // Indicates if the type can be instantiated.
        Instance = 1 << 1, // Indicates if the type represents an instance (as opposed to a class or type itself).
        Callable = 1 << 2, // Indicates if an instance of the type can be called like a function. (It has a `__call__` method).
        BuiltIn = 1 << 3, // Indicates if the type is a built-in type (like `int`, `str`, etc.).
        Literal = 1 << 4, // Indicates if the instance is a literal (like `42`, `"hello"`, etc.).
        Interface = 1 << 5, // Indicates if the type is an interface (a type that defines a set of methods and properties). In Python this would be a Protocol.
        Generic = 1 << 6, // Indicates if the type is a generic type (a type that can be parameterized with other types).
    }

    // Flags that describe the characteristics of a function or method.
    // These flags can be combined using bitwise operations.
    export const enum FunctionFlags {
        None = 0,
        Async = 1 << 0, // Indicates if the function is asynchronous.
        Generator = 1 << 1, // Indicates if the function is a generator (can yield values).
        Abstract = 1 << 2, // Indicates if the function is abstract (must be implemented in a subclass).
        Static = 1 << 3, // Indicates if the function is static (belongs to the class rather than an instance).
    }

    // Flags that describe the characteristics of a class.
    // These flags can be combined using bitwise operations.
    export const enum ClassFlags {
        None = 0,
        Enum = 1 << 0, // Indicates if the class is an enum (a special kind of class that defines a set of named values).
    }

    export interface Type {
        // Unique identifier for the type definition within the session.
        handle: string | number;

        // Essential classification of the symbol.
        category: TypeCategory;

        // Flags describing the type.
        flags: TypeFlags;

        // Name of the module the type comes from
        moduleName: string | undefined;

        // Name of the type.
        name: string;

        // Flags specific to the category
        categoryFlags: number;
    }

    export interface Member {
        // The name of the member.
        name: string;

        // The type of the member.
        type: Type;

        // The type the member came from
        classType: Type | undefined;
    }

    // Flags that are used for searching for members of a type.
    export const enum MemberAccessFlags {
        None = 0,
        SkipInstanceMembers = 1 << 0, // Skip instance members when searching for members of a type.
        SkipObjectBaseClass = 1 << 1, // Skip members from the `object` base class when searching for members of a type.
    }

    // Represents the category of a declaration in the type system.
    // This is used to classify declarations such as variables, functions, classes, etc.
    export const enum DeclarationCategory {
        Intrinsic = 0, // An intrinsic is a built-in type or function that is part of the language itself, such as `int`, `str`, `len`, etc.
        Variable = 1, // A variable is a named storage location that can hold a value.
        Param = 2, // A parameter is a variable that is passed to a function or method.
        TypeParam = 3, // A type parameter is a placeholder for a type that can be specified when the type is used, such as in generics.
        TypeAlias = 4, // A type alias is a name that refers to another type, such as `List[int]` or `Dict[str, int]`.
        Function = 5, // A function is a named block of code that can be called with arguments and returns a value.
        Class = 6, // A class is a blueprint for creating objects that encapsulates data and behavior.
        SpecialBuiltInClass = 7, // Special built-in types like 'Tuple', 'Generic',  'Protocol', 'Callable', 'Type', etc
        Alias = 8, // An alias declaration, which is a reference to another declaration.
    }

    // Represents a symbol declaration in the type system.
    // A declaration is a specific instance of a symbol in the source code, such as a variable, function, or class.
    export interface Declaration {
        // Unique identifier for the declaration within the session.
        handle: string | number;

        // Category of this symbol (function, variable, etc.).
        category: DeclarationCategory;

        // Parse node associated with the declaration
        node?: Node;

        // The dot-separated import name for the file that
        // contains the declaration (may not be definitive
        // because a source file can be accessed via different
        // import names in some cases).
        moduleName: string;
    }

    // Synthesized type information for a declaration that is not directly
    // represented in the source code, but is derived from the declaration. Other languages
    // may refer to this as an anonymous type.
    export interface SynthesizedTypeInfo {
        type: Type;

        // An optional node that is not used by the type evaluator
        // but can be used by language services to provide additional
        // functionality (such as go-to-definition).
        node?: Node;
    }

    // Declaration information for a symbol, which includes
    // a list of declarations and potentially synthesized types for those declarations.
    export interface SymbolDeclInfo {
        decls: Declaration[];
        synthesizedTypes: SynthesizedTypeInfo[];
    }

    // Describes an import
    export interface ImportedModuleDescriptor {
        leadingDots: number;
        nameParts: string[];
    }

    // Options for resolving an alias declaration.
    export interface ResolveAliasOptions {
        resolveLocalNames?: boolean; // Whether to resolve local names in the alias declaration.
        allowExternallyHiddenAccess?: boolean; // Whether to allow access to members that are hidden by external modules.
        skipFileNeededCheck?: boolean; // Whether to skip checking if the file is needed for the alias resolution.
    }

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
        moduleDescriptor: ImportedModuleDescriptor;
        snapshot: number;
    }

    // Represents settings that can be sent to the type server.

    export type Settings = {
        [key: string]: any;
    };

    // Requests and notifications for the type server protocol.
    export enum Requests {
        // First request to initialize the type server.
        Initialize = 'typeServer/initialize',
        // Request from client to shut down the type server.
        Shutdown = 'typeServer/shutdown',
        // Request from client to get the current snapshot of the type server.
        // A snapshot is a point-in-time representation of the type server's state, including all loaded files and their types.
        // A type server should change its snapshot whenever any type it might have returned is no longer valid. Meaning types are
        // only usable for the snapshot they were returned with.
        GetSnapshot = 'typeServer/getSnapshot',
        // Request to get diagnostics for a specific file.
        GetDiagnostics = 'typeServer/getDiagnostics',
        // Request to get the version of diagnostics for a specific file.
        GetDiagnosticsVersion = 'typeServer/getDiagnosticsVersion',
        // Request to get the type information for a specific node.
        GetType = 'typeServer/getType',
        // Request to get the union types for a specific type.
        GetUnionTypes = 'typeServer/getUnionTypes',
        // Request to find a member of a type.
        GetTypeMember = 'typeServer/getTypeMember',
        // Request to get all overloads of a function or method.
        GetOverloads = 'typeServer/getOverloads',
        // Request to get the effective meta class of a type.
        GetEffectiveMetaClass = 'typeServer/getEffectiveMetaClass',
        // Request to get the type of a declaration.
        GetTypeOfDeclaration = 'typeServer/getTypeOfDeclaration',
        // Request to get symbol declaration information for a node.
        GetSymbolDeclarationInfo = 'typeServer/getSymbolDeclarationInfo',
        // Request to get the bound magic method for a type.
        GetBoundMagicMethod = 'typeServer/getBoundMagicMethod',
        // Request to resolve an alias declaration.
        // This request is sent by the client to resolve an alias declaration, which may involve looking up the
        // declaration in the type server's cache or performing additional resolution logic.
        ResolveAliasDeclaration = 'typeServer/resolveAliasDeclaration',
        // Request to resolve an import.
        ResolveImport = 'typeServer/resolveImport',
    }

    export enum Notifications {
        // Notification sent by the server to indicate that the type server has been initialized.
        Initialized = 'typeServer/initialized',
        // Notification sent by the server to indicate that the type server has shut down.
        Shutdown = 'typeServer/shutdown',
        // Notification sent by the client to indicate that a text document has been opened.
        TextDocumentOpen = 'textDocument/open',
        // Notification sent by the client to indicate that a text document has been closed.
        TextDocumentClose = 'textDocument/close',
        // Notification sent by the client to indicate that settings have changed.
        SettingsChange = 'typeServer/settingsChange',
        // Notification sent by the client to indicate that files have changed.
        FilesChanged = 'typeServer/filesChanged',
        // Notification sent by the client to indicate that the type server's cache should be flushed (and snapshots reset)
        FlushCache = 'typeServer/flushCache',
    }

    export interface Params {
        [Requests.Initialize]: { workspace: WorkspaceFolder; initialSettings: string };
        [Requests.Shutdown]: void;
        [Requests.GetSnapshot]: void;
        [Requests.GetDiagnostics]: { uri: string; snapshot: number };
        [Requests.GetDiagnosticsVersion]: { uri: string };
        [Requests.GetType]: { node: Node; snapshot: number };
        [Requests.GetUnionTypes]: { type: Type; snapshot: number };
        [Requests.GetTypeMember]: {
            type: Type;
            memberName: string;
            accessFlags: MemberAccessFlags;
            snapshot: number;
        };
        [Requests.GetOverloads]: { type: Type; snapshot: number };
        [Requests.GetEffectiveMetaClass]: { type: Type; snapshot: number };
        [Requests.GetTypeOfDeclaration]: { decl: Declaration; snapshot: number };
        [Requests.GetSymbolDeclarationInfo]: {
            node: Node;
            skipUnreachableCode: boolean;
            snapshot: number;
        };
        [Requests.GetBoundMagicMethod]: { type: Type; name: string; snapshot: number };
        [Requests.ResolveAliasDeclaration]: {
            decl: Declaration;
            options: ResolveAliasOptions;
            snapshot: number;
        };
        [Requests.ResolveImport]: ResolveImportParams;
        [Notifications.Initialized]: void;
        [Notifications.Shutdown]: void;
        [Notifications.FlushCache]: void;
        [Notifications.TextDocumentOpen]: TextDocumentOpenParams;
        [Notifications.TextDocumentClose]: TextDocumentCloseParams;
        [Notifications.SettingsChange]: Settings;
        [Notifications.FilesChanged]: { changes: FileEvent[] };
    }

    export interface Response {
        [Requests.Initialize]: { configRoots: string[] };
        [Requests.Shutdown]: { success: boolean };
        [Requests.GetSnapshot]: number;
        [Requests.GetDiagnostics]: Diagnostic[] | undefined;
        [Requests.GetDiagnosticsVersion]: number | undefined;
        [Requests.GetType]: Type | undefined;
        [Requests.GetUnionTypes]: Type[] | undefined;
        [Requests.GetTypeMember]: Member | undefined;
        [Requests.GetOverloads]: Type[] | undefined;
        [Requests.GetEffectiveMetaClass]: Type | undefined;
        [Requests.GetTypeOfDeclaration]: Type | undefined;
        [Requests.GetSymbolDeclarationInfo]: SymbolDeclInfo | undefined;
        [Requests.GetBoundMagicMethod]: Type | undefined;
        [Requests.ResolveAliasDeclaration]: Declaration | undefined;
        [Requests.ResolveImport]: string | undefined;
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

# Type Server Protocol

The Type Server Protocol (TSP) is a JSON-RPC protocol for asking a type server for Python analysis data. A type server maintains the type-analysis state for a workspace and answers requests for snapshots, import resolution, diagnostics, type information, symbols, overloads, and related metadata.

The protocol uses Language Server Protocol (LSP) data shapes where they are useful, such as `URI`, `Position`, `Range`, and `Diagnostic`. TSP methods use the `typeServer/` prefix.

The protocol artifacts in this folder are the authoritative definitions:

- [typeServerProtocol.ts](typeServerProtocol.ts) defines the TypeScript interfaces and request types.
- [tsp.json](tsp.json) is the machine-readable protocol model.
- [tsp.schema.json](tsp.schema.json) is the JSON schema for the protocol model.

## Version History

TSP uses semantic version strings for client/server compatibility checks. While the protocol is in the `0.x` line, minor version changes may be breaking. Patch version changes remain backward compatible within the same minor line.

| Version | Changes                                                                             |
| ------- | ----------------------------------------------------------------------------------- |
| `0.1.0` | Initial protocol version.                                                           |
| `0.2.0` | Added request types and fields.                                                     |
| `0.3.0` | Switched to more complex type shapes.                                               |
| `0.4.0` | Switched to the `Type` union and stub-based type payloads.                          |
| `0.4.1` | Added multi-connection negotiation and the `typeServer/connection` control request. |

## Connection Model

A client starts a type server and communicates with it over stdio on the main JSON-RPC connection. stdout must be reserved for JSON-RPC protocol messages.

A type server is expected to receive enough workspace and document state to answer the TSP requests it supports. Clients commonly use normal LSP initialization and document synchronization for this state, then send `typeServer/*` requests on the same JSON-RPC connection.

TSP also supports optional extra read-only connections. The original connection remains the main connection and owns initialization, workspace state, document synchronization, state-changing notifications, and connection control. Extra connections are opened only after client and server negotiate support during initialization.

## Startup Sequence

A typical session follows this order:

1. The client starts or connects to the type server.
1. The client and server initialize any shared workspace state, commonly through the LSP `initialize` and `initialized` messages.
1. The client calls `typeServer/getSupportedProtocolVersion` and verifies that the returned semver string is compatible with the protocol version it expects.
1. The client calls `typeServer/getSnapshot` to obtain the first snapshot identifier.
1. The client sends type, import, symbol, diagnostic, or metadata requests that include the current snapshot when required by the request shape.
1. The server sends `typeServer/snapshotChanged` when prior type results are no longer valid.

## Multi-Connection Mode

Multi-connection mode is an optional performance feature. It lets a client open additional local channels to the same type server for read-only TSP requests, while the main connection continues to own the mutable workspace state.

Clients should use multi-connection mode only when they can benefit from concurrent read-only work, such as high-volume type queries or background workers that should not block the main JSON-RPC connection. A server must still work correctly in single-connection mode. Multi-connection support must not be required for protocol correctness.

### Capability Handshake

Multi-connection support is negotiated through the normal LSP `initialize` request and response. A client that can open extra TSP channels advertises the supported transport kinds under `capabilities.experimental.typeServerMultiConnection`:

```json
{
    "capabilities": {
        "experimental": {
            "typeServerMultiConnection": {
                "supportedTransports": ["ipc"]
            }
        }
    }
}
```

A server that can serve extra TSP channels returns the same capability shape in the `initialize` result:

```json
{
    "capabilities": {
        "experimental": {
            "typeServerMultiConnection": {
                "supportedTransports": ["ipc"]
            }
        }
    }
}
```

Multi-connection mode is enabled only when both sides advertise `typeServerMultiConnection` and the two `supportedTransports` lists have at least one transport in common. If either side omits the capability, or if there is no common transport, the session remains single-connection and the client must not send `typeServer/connection`.

The currently supported built-in transport kind for extra connections is `ipc`. The main connection uses stdio; `ipc` applies only to dynamically opened extra connections.

### Opening An Extra Connection

After initialization and transport negotiation, the client opens an extra channel by sending `typeServer/connection` on the main connection:

```json
{
    "type": "open",
    "kind": "ipc",
    "args": ["<ipc-endpoint>"]
}
```

For `ipc`, the `args` array identifies the endpoint or endpoints that the server should connect to. The server should validate the request, connect to the supplied endpoint promptly, and return a result with `success: true` when it accepts the request. If the server cannot open the channel, it should return `success: false` and include a short `message` when useful for logs.

### IPC Endpoint Arguments

An `ipc` endpoint is expected to provide a full-duplex JSON-RPC stream when the platform IPC mechanism supports it. In that case, `args` contains one endpoint string:

```json
{
    "type": "open",
    "kind": "ipc",
    "args": ["<full-duplex-ipc-endpoint>"]
}
```

If the platform IPC mechanism exposes only one-way endpoints, `args` contains two endpoint strings. The endpoint names are from the type server's perspective: the first endpoint is the server input stream, and the second endpoint is the server output stream.

```json
{
    "type": "open",
    "kind": "ipc",
    "args": ["<input-ipc-endpoint>", "<output-ipc-endpoint>"]
}
```

### Closing An Extra Connection

The client closes an extra channel by sending `typeServer/connection` on the main connection with the same transport kind and endpoint identity:

```json
{
    "type": "close",
    "kind": "ipc",
    "args": ["<ipc-endpoint>"]
}
```

The server should stop serving the matching extra channel and close the transport promptly. A client may also tear down its local transport if the server does not complete the close within the client's timeout budget.

The `close` request should use the same `args` shape that opened the channel: one endpoint for a full-duplex IPC stream, or the same input/output endpoint pair for a split IPC stream.

### Allowed Traffic

The main connection owns all state-changing traffic. The following must remain main-connection-only:

- LSP initialization and lifecycle messages.
- Workspace, configuration, file-watcher, and document synchronization notifications.
- Server-to-client snapshot and diagnostics notifications.
- The `typeServer/connection` control request.

Extra connections are TSP-only and read-only. They may be used for requests that do not mutate server state and whose results are valid for the snapshot supplied by the client.

The allowed TSP messages on an extra connection are bound to the negotiated TSP version. If a server reports support for a TSP version and advertises multi-connection support for that session, it must support every extra-connection TSP message defined for that version.

The table below lists the TSP version that first allows each message on an extra connection:

| TSP version | Extra-connection message                 |
| ----------- | ---------------------------------------- |
| `0.4.1`     | `typeServer/getSupportedProtocolVersion` |
| `0.4.1`     | `typeServer/getSnapshot`                 |
| `0.4.1`     | `typeServer/getPythonSearchPaths`        |
| `0.4.1`     | `typeServer/resolveImport`               |
| `0.4.1`     | `typeServer/getComputedType`             |
| `0.4.1`     | `typeServer/getDeclaredType`             |
| `0.4.1`     | `typeServer/getExpectedType`             |

Servers should reject LSP traffic, state-changing notifications, `typeServer/connection`, and any TSP message not allowed for the negotiated TSP version when received on an extra connection.

## Snapshots

A snapshot is a non-negative integer that identifies a point-in-time view of the type server's analysis state. Type handles, declarations, symbols, and other returned objects are valid only for the snapshot in which they were returned unless a request explicitly says otherwise.

The type server must advance the snapshot whenever a previously returned type-analysis result may be invalid. Typical invalidating events include opened-file changes, closed files, configuration changes, watched-file changes, dependency changes, or any cache reset that changes analysis results.

Snapshot rules:

- `typeServer/getSnapshot` returns the current snapshot identifier.
- Snapshot identifiers must not decrease during a session.
- `typeServer/snapshotChanged` reports the previous and new snapshot identifiers.
- Requests that include a stale snapshot should fail with a JSON-RPC error that lets the client retry with a fresh snapshot. LSP's `ServerCancelled` error code (`-32802`) is the preferred error for this case.

## Positions And Ranges

TSP follows LSP position conventions:

- Lines are zero-based.
- Character offsets are zero-based UTF-16 code units.
- Ranges identify source spans using a start position and end position.

If a type server stores source locations in another encoding, it must convert locations at the protocol boundary. Incorrect conversion can cause the client to request information for the wrong syntax node.

## Nodes, Declarations, And Handles

Many requests identify source constructs by node, declaration, type handle, or symbol handle. A node is a URI plus a source range. A declaration describes where and how a symbol is defined. Handles identify protocol objects that the type server can resolve within the current snapshot.

`InvalidHandle` is `-1` and represents an invalid or unavailable handle. Clients and servers should treat it as a sentinel value, not as a valid object identifier.

## Type Results

Type results are JSON-serializable tagged objects. Each type includes a discriminator that tells the client how to interpret the rest of the object. The protocol supports built-in types, declared types, functions, classes, unions, modules, type variables, overload sets, synthesized types, and type references.

Type objects are snapshot-bound, and type IDs are response-local:

- A returned type object is valid only for the snapshot used by the request that produced it.
- Type IDs are used to connect `TypeReference` objects to earlier type objects in the same serialized response graph.
- Type IDs are not a stable global identity for a snapshot and should not be compared across separate responses.
- Type references should be used to avoid duplicating large or recursive type graphs within one response.

## Protocol Surface

The exact parameters and result shapes are defined in the protocol artifacts. At a high level, TSP includes these categories of messages:

| Category                     | Messages                                                                                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Compatibility and state      | `typeServer/getSupportedProtocolVersion`, `typeServer/getSnapshot`, `typeServer/snapshotChanged`                                                                               |
| Connection control           | `typeServer/connection`                                                                                                                                                        |
| Diagnostics                  | `typeServer/getDiagnostics`, `typeServer/getDiagnosticsVersion`, `typeServer/diagnosticsChanged`                                                                               |
| Import and search paths      | `typeServer/getPythonSearchPaths`, `typeServer/resolveImport`, `typeServer/resolveImportDeclaration`                                                                           |
| Type queries                 | `typeServer/getType`, `typeServer/getComputedType`, `typeServer/getDeclaredType`, `typeServer/getExpectedType`, `typeServer/getBuiltinType`, `typeServer/getTypeOfDeclaration` |
| Type structure               | `typeServer/getTypeArgs`, `typeServer/getTypeAliasInfo`, `typeServer/combineTypes`, `typeServer/createInstanceType`, `typeServer/fetchTypeProperties`                          |
| Symbols and callable details | `typeServer/getSymbolsForType`, `typeServer/getSymbolsForNode`, `typeServer/getOverloads`, `typeServer/getMatchingOverloads`, `typeServer/getMetaclass`                        |
| Display metadata             | `typeServer/getRepr`, `typeServer/getDocString`                                                                                                                                |

A type server should implement the messages required by the client it integrates with and return `null` or `undefined` only where the protocol's result type allows it.

## Error Handling

Use standard JSON-RPC error responses.

| Situation          | Error code                   | Guidance                                                       |
| ------------------ | ---------------------------- | -------------------------------------------------------------- |
| Stale snapshot     | `-32802` (`ServerCancelled`) | The client can request a fresh snapshot and retry.             |
| Invalid parameters | `-32602` (`InvalidParams`)   | Required fields are missing or malformed.                      |
| Internal failure   | `-32603` (`InternalError`)   | The server failed unexpectedly while handling a valid request. |

Errors should include enough message detail for a client log to identify the failed request, but they should not expose local secrets or implementation-only state.

## Compatibility Checklist

A compatible type server should verify these behaviors:

1. `typeServer/getSupportedProtocolVersion` returns a semver string supported by the client.
1. All request and notification payloads serialize and deserialize according to the protocol artifacts.
1. `typeServer/getSnapshot` returns a non-negative snapshot and snapshots do not go backward.
1. Document, configuration, and watched-file changes invalidate snapshots when they can change returned analysis data.
1. Requests with stale snapshots fail with a retryable cancellation error.
1. Position and range conversions use LSP zero-based UTF-16 conventions.
1. Import-resolution requests return document URIs or no result according to the protocol result type.
1. Type, symbol, overload, diagnostic, and display requests return well-formed objects for the snapshot supplied by the client.
1. Multi-connection support is advertised only when the server can serve the negotiated extra transport.
1. Extra connections accept every TSP request allowed for the negotiated TSP version and reject LSP traffic, state-changing notifications, `typeServer/connection`, and TSP requests not allowed for that version.

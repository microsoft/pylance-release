---
name: pylance-type-server-protocol
description: Reference for the Pylance Type Server Protocol (TSP) — the JSON-RPC protocol for programmatically querying a type server for Python analysis data (snapshots, search paths, import resolution, computed/declared/expected types). Use when building tooling, MCP servers, or editors that speak typeServer/*. Triggers on "Type Server Protocol", "TSP", "typeServer", "type query", "programmatic type analysis".
---

# Type Server Protocol (TSP)

The **Type Server Protocol** is a JSON-RPC protocol for asking a type server for Python analysis data. A type server maintains the type-analysis state for a workspace and answers requests for: protocol version, snapshots, Python search paths, import resolution, and type queries (computed, declared, expected). TSP methods use the `typeServer/` prefix and reuse LSP data shapes (`Position`, `Range`, string URIs).

## When to use TSP vs LSP

TSP is for tooling that needs *type-level data* beyond what the Language Server Protocol exposes — e.g. computing the declared vs. inferred type at a position, or resolving what a symbol imports to. Use TSP when building an editor, an MCP/AI tool that reasons about types, or a custom analyzer backed by Pylance/Pyright.

## Authoritative artifacts

- [../../docs/tsp/type-server-protocol.md](../../docs/tsp/type-server-protocol.md) — human-readable spec (connection model, version history `0.1.0`–`0.4.1`, multi-connection negotiation).
- [../../docs/tsp/typeServerProtocol.ts](../../docs/tsp/typeServerProtocol.ts) — the authoritative TypeScript interfaces and request/notification types.
- [../../docs/tsp/tsp.json](../../docs/tsp/tsp.json) — machine-readable protocol model (all `typeServer/*` methods).
- [../../docs/tsp/tsp.schema.json](../../docs/tsp/tsp.schema.json) — JSON schema for the model.

## Connection model

A client starts a type server and communicates over stdio on the main JSON-RPC connection; stdout is reserved for protocol messages. Clients synchronize workspace/document state via normal LSP initialization, then send `typeServer/*` requests on the same connection. Full detail: [../../docs/tsp/type-server-protocol.md](../../docs/tsp/type-server-protocol.md).

## Related context

For the existing Pylance MCP-tooling workflow with Copilot (resolving interpreters, listing files, querying diagnostics, applying fixes), see [../../docs/howto/copilot-pylance-workflow.md](../../docs/howto/copilot-pylance-workflow.md).

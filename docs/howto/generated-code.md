# How to Work with Generated Code in Pylance

Projects often contain generated Python files — protobuf/gRPC stubs, SQLAlchemy models, Django migrations, Pydantic datamodel-code-generator output, and similar. These files can cause noisy diagnostics or missing type information. This guide covers strategies for making Pylance work well with generated code.

---

## Table of Contents

- [Strategy 1: Add Generated Output to extraPaths](#strategy-1-add-generated-output-to-extrapaths)
- [Strategy 2: Use stubPath for Hand-Written Stubs](#strategy-2-use-stubpath-for-hand-written-stubs)
- [Strategy 3: Suppress Diagnostics with ignore](#strategy-3-suppress-diagnostics-with-ignore)
- [Strategy 4: Use useNearestConfiguration with a Relaxed Config](#strategy-4-use-usenearestconfiguration-with-a-relaxed-config)
- [Choosing a Strategy](#choosing-a-strategy)
- [FAQ](#faq)

---

## Strategy 1: Add Generated Output to extraPaths

If your build step generates Python files in an output directory, add that directory to [`extraPaths`](../settings/python_analysis_extraPaths.md) so Pylance can resolve imports from it:

```
project/
├── proto/
│   └── service.proto
├── generated/          # protoc output: service_pb2.py, service_pb2_grpc.py
├── src/api/
│   └── client.py       # from generated.service_pb2 import ServiceRequest
```

```json
{
    "python.analysis.extraPaths": ["./generated"]
}
```

**When to use**: The generated files have useful type information and you want Pylance to resolve imports from them.

---

## Strategy 2: Use stubPath for Hand-Written Stubs

If generated code is complex or has missing type info, create `.pyi` stub files that provide accurate type annotations:

```json
{
    "python.analysis.stubPath": "./typestubs"
}
```

```
project/
├── typestubs/
│   └── generated/
│       ├── __init__.pyi
│       └── service_pb2.pyi   # hand-written or mypy-protobuf generated
```

**When to use**: The generated code exists but lacks type information, or you want cleaner type annotations than what the generator produces (e.g., `mypy-protobuf` stubs for protobuf).

---

## Strategy 3: Suppress Diagnostics with ignore

To keep Pylance from reporting errors _in_ generated files you don't want to fix:

```json
{
    "python.analysis.ignore": ["generated/**"]
}
```

This still allows imports _from_ generated code to resolve — it only suppresses diagnostics _in_ those files.

**When to use**: The generated files are importable and work fine, but contain patterns that trigger Pylance diagnostics (missing annotations, dynamic attributes, etc.) that you don't want to see.

---

## Strategy 4: Use useNearestConfiguration with a Relaxed Config

Drop a [`pyrightconfig.json`](https://microsoft.github.io/pyright/#/configuration) in the generated directory with relaxed rules:

```json
// generated/pyrightconfig.json
{
    "typeCheckingMode": "off"
}
```

This requires [`python.analysis.useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md) to be `true` so Pylance picks up the per-directory config.

**When to use**: You want different type-checking strictness for generated code vs. hand-written code, and you're already using `useNearestConfiguration`.

---

## Choosing a Strategy

| Scenario                                                        | Recommended Strategy                                                                             |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Generated files have good types, just need import resolution    | Strategy 1 ([`extraPaths`](../settings/python_analysis_extraPaths.md))                           |
| Generated files lack types, need manual `.pyi` stubs            | Strategy 2 ([`stubPath`](../settings/python_analysis_stubPath.md))                               |
| Generated files work but produce noisy diagnostics              | Strategy 3 ([`ignore`](../settings/python_analysis_ignore.md))                                   |
| Different strictness levels for generated vs. hand-written code | Strategy 4 ([`useNearestConfiguration`](../settings/python_analysis_useNearestConfiguration.md)) |
| Import resolution + suppress diagnostics in generated files     | Combine Strategy 1 + Strategy 3                                                                  |

---

## FAQ

### Q: Can I combine multiple strategies?

Yes. A common pattern is to add the generated output to [`extraPaths`](../settings/python_analysis_extraPaths.md) (so imports resolve) and also add it to [`ignore`](../settings/python_analysis_ignore.md) (so diagnostics in those files are suppressed):

```json
{
    "python.analysis.extraPaths": ["./generated"],
    "python.analysis.ignore": ["generated/**"]
}
```

### Q: My protobuf/gRPC stubs have no type information. What should I do?

Use [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf) to generate `.pyi` stubs alongside the Python files:

```bash
protoc --python_out=generated --mypy_out=generated service.proto
```

Then either put the `.pyi` files alongside the generated `.py` files (Strategy 1 handles both) or move them to [`stubPath`](../settings/python_analysis_stubPath.md) (Strategy 2).

---

## Related Guides

- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — import resolution and `extraPaths` configuration
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — `ignore`, `include`, `exclude` differences
- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — generated code in monorepo layouts

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

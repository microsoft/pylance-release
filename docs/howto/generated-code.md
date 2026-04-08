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

```text
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

```text
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

## Framework-Specific Guidance

### Django

Django uses metaclasses and dynamic model fields that Pylance cannot analyze from source alone. Install [django-stubs](https://github.com/typeddjango/django-stubs) to provide type information:

```bash
pip install django-stubs
```

Add to `pyproject.toml`:

```toml
[tool.django-stubs]
django_settings_module = "myproject.settings"
```

For `django-stubs` to work properly with Pylance, you may also need [django-stubs-ext](https://pypi.org/project/django-stubs-ext/) and a `manage.py` or settings module reachable from the workspace root.

For dynamic model fields that stubs don't cover, create custom stubs under [`stubPath`](../settings/python_analysis_stubPath.md).

### Protobuf / gRPC

Use [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf) to generate `.pyi` stubs alongside the Python files:

```bash
pip install mypy-protobuf
protoc --python_out=generated --mypy_out=generated service.proto
```

Then add the generated directory to [`extraPaths`](../settings/python_analysis_extraPaths.md) so Pylance resolves the imports. The `.pyi` stubs colocated with `.py` files are picked up automatically.

### FastAPI and Pydantic

**Pydantic v2** ships type annotations natively (`py.typed`), so Pylance recognizes `BaseModel` fields, `model_validator`, and `field_validator` out of the box. If Pylance doesn't recognize Pydantic features:

1. Ensure you have Pydantic v2+ installed (`pip install pydantic>=2.0`)
2. Restart Pylance after installing (**Ctrl+Shift+P → Pylance: Restart Language Server**)

**FastAPI** builds on Pydantic and uses `Depends()` extensively. Pylance understands FastAPI's `Depends` typing when the dependency function has return type annotations:

```python
from fastapi import Depends, FastAPI

def get_db() -> Database:  # Return type annotation required
    ...

@app.get("/items")
async def read_items(db: Database = Depends(get_db)):  # Pylance infers db type
    ...
```

Common issues:

- **`response_model` not validated**: `response_model=MyModel` on route decorators is not statically checked by Pylance — use return type annotations instead: `async def read_items(...) -> MyModel`
- **Missing attributes on request body**: Ensure the Pydantic model is imported and the field types are annotated
- **Pydantic v1 compatibility**: If using `pydantic.v1` compat layer, Pylance may not recognize v1-style validators — migrate to v2 `@field_validator` / `@model_validator`

### SQLAlchemy 2.0

SQLAlchemy 2.0 uses `Mapped[]` type annotations and `mapped_column()` which Pylance recognizes natively. For best results:

```python
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
```

If Pylance doesn't recognize `Mapped` attributes, ensure SQLAlchemy 2.0+ is installed in your selected interpreter. For SQLAlchemy 1.4 projects that haven't migrated, install [sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs) (`pip install sqlalchemy2-stubs`). Note: `sqlalchemy2-stubs` is **only compatible with SQLAlchemy 1.4** and must be uninstalled before upgrading to 2.0.

### Dynamic Attribute Access (`__getattr__` / `__getitem__`)

If your code or a library uses `__getattr__` for dynamic attribute access, Pylance cannot infer what attributes are available. Provide explicit type information:

**Option 1: Type the dunder method in a stub**

```python
# typings/my_dynamic_lib/__init__.pyi
from typing import Any

class DynamicConfig:
    # Allow any attribute access:
    def __getattr__(self, name: str) -> Any: ...

    # Or be specific with overloads:
    from typing import overload
    @overload
    def __getitem__(self, key: str) -> str: ...
    @overload
    def __getitem__(self, key: int) -> bytes: ...
```

**Option 2: Annotate in your code**

```python
from typing import Any

class Config:
    def __getattr__(self, name: str) -> Any:
        return self._data[name]
```

When `__getattr__` returns `Any`, Pylance suppresses [`reportAttributeAccessIssue`](../diagnostics/reportAttributeAccessIssue.md) for that class. When it returns a more specific type, Pylance validates attribute usage against that type.

---

## Dataclass, attrs, and Decorator-Synthesized Members

Pylance has built-in support for `@dataclasses.dataclass`, `@attrs.define`, and several other common decorators that synthesize methods (`__init__`, `__eq__`, `__repr__`, etc.). If Pylance does not recognize fields or methods on a decorated class, check these common causes:

### Missing stubs for attrs

For `attrs`, install the stubs package:

```bash
pip install attrs  # attrs >= 22.1 ships py.typed; older versions need types-attrs
```

### `from __future__ import annotations` interaction

When `from __future__ import annotations` is active, all annotations are strings at runtime. Pylance handles this correctly for `@dataclass` and `@attrs.define`, but some less common decorators may not be recognized. If fields appear as `Unknown`, try removing `from __future__ import annotations` as a test to confirm this is the cause.

### Custom decorators that synthesize attributes

Pylance only recognizes a fixed set of well-known decorators (`@dataclass`, `@attrs.define`, `@attrs.s`, `@pydantic.BaseModel`, etc.). For custom decorators that add attributes:

1. **Write a stub** listing the synthesized attributes explicitly:

```python
# typings/my_framework/__init__.pyi
class MyModel:
    id: int
    name: str
    def save(self) -> None: ...
```

2. **Use `__getattr__`** as a fallback for truly dynamic attributes (see [Dynamic Attribute Access](#dynamic-attribute-access-__getattr__--__getitem__) above).

### reportAttributeAccessIssue on known fields

If `reportAttributeAccessIssue` fires on fields that should exist (e.g., `@dataclass` fields), check:

- The decorator import is correct (`from dataclasses import dataclass`, not a custom wrapper)
- Field types are annotated (`name: str`, not just `name = "default"`)
- The class is not inheriting from a dynamic base that shadows the decorator behavior

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

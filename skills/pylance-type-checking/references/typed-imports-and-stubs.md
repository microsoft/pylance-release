# Typed Imports & Type Stubs

Several `report*` errors trace back to imports: a library has no type stubs (`reportMissingTypeStubs`) or returns `Unknown` types (`reportUnknown*`), or an import can't resolve at all (`reportMissingImports`). This reference covers what to do **in your code and project dependencies** — not editor configuration.

## `reportMissingTypeStubs` (strict)

Fires when an imported library has no `.pyi` stub files or `py.typed` marker, so Pylance can't infer precise types from it.

```python
import some_library  # Warning: Stub file not found for "some_library"
```

### Fix — install a stub package as a dev dependency

Many popular libraries have separate `types-*` or `*-stubs` packages on PyPI:

```bash
pip install types-requests types-PyYAML types-toml
# AWS SDK stubs (service-scoped):
pip install 'boto3-stubs[s3,ec2]'
```

**Keep stub versions aligned** with the library they describe — mismatched versions cause false errors:

```bash
pip install requests==2.31.0 types-requests==2.31.0
```

Diagnose mismatches: `pip list | grep -E 'types-|stubs'` and compare versions against the library.

### Fix — prefer `py.typed` libraries

Libraries that ship their own type annotations include a `py.typed` marker (PEP 561). When choosing a dependency, prefer one that's `py.typed` — no stub package needed and the types stay in sync with the implementation.

### Fix — write `.pyi` stubs for untyped dependencies

If no stub package exists and the library isn't `py.typed`, hand-write `.pyi` stub files declaring the symbols you use. Place them in a `typings/` directory (or wherever `stubPath` points) following PEP 561 partial-stub-package layout:

```
typings/
└── my_library/
    └── __init__.pyi
```

```python
# typings/my_library/__init__.pyi
def do_thing(x: int) -> str: ...
```

### Fix — suppress the rule for that import

If none of the above fit (e.g., a deliberately dynamic library), suppress just this line or relax the rule for the file. It's strict-only and often noisy with untyped dependencies:

```python
import some_dynamic_lib  # pyright: ignore[reportMissingTypeStubs]
```

## `reportUnknown*` (strict)

`reportUnknownVariableType`/`reportUnknownArgumentType`/`reportUnknownMemberType`/`reportUnknownParameterType` fire when a type is `Unknown` — usually because it flowed from an untyped library or an unannotated function call.

**Fix at the source**: annotate the function whose return is `Unknown`, or install stubs / write `.pyi` for the library producing it. Don't paper over it with `# pyright: ignore` unless the source is genuinely dynamic.

```python
import untyped_lib

result = untyped_lib.compute()  # reportUnknownVariableType
# Fix: install types-untyped_lib, or write a typings/untyped_lib/__init__.pyi
```

## `reportMissingImports` (off)

Fires when an import can't be resolved at all.

### The package isn't installed

```bash
pip install the_package
```

### Circular imports — use `TYPE_CHECKING`

Imports only needed for annotations often cause circular imports. Guard them under `TYPE_CHECKING` and use **string annotations** (or `from __future__ import annotations`) so they aren't evaluated at runtime:

```python
from __future__ import annotations  # makes all annotations strings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User  # only imported by the type checker, not at runtime

def process(user: User) -> None:  # safe — annotation is a string at runtime
    ...
```

`from __future__ import annotations` is the simplest fix: every annotation becomes a string literal, so forward references and `TYPE_CHECKING`-only imports never execute at runtime. Without it, use explicit string annotations: `def process(user: "User") -> None:`.

### `reportMissingModuleSource` (off, warning)

The module resolves but its source can't be found (e.g., a compiled extension, or a module that only ships stubs). Usually harmless — install stubs to get rich types.

## Generated / dynamic code

For generated code (Protobuf, Django models, dataclass/attrs/Pydantic synthesized members) Pylance can't analyze statically, the code-level options are:

- `# pyright: ignore` at the top of the generated file — suppresses all diagnostics for that file while keeping imports resolvable.
- Hand-write `.pyi` stubs declaring the synthesized members (e.g., the dataclass fields).

See the [generated code how-to](https://github.com/microsoft/pylance-release/blob/main/docs/howto/generated-code.md) for framework-specific notes (Django, Protobuf, FastAPI/Pydantic, SQLAlchemy, attrs/dataclasses).

## See Also

- [Fixing type errors](fixing-type-errors.md) — `reportUnknown*` and `reportMissingTypeArgument` fixes
- [Type-checking levels](type-checking-levels.md) — which levels flag stub/import issues
- [Type narrowing](type-narrowing.md) — narrowing `Any` with `isinstance`
- Bundled stubs how-to: https://github.com/microsoft/pylance-release/blob/main/docs/howto/bundled-stubs.md
- Unresolved imports how-to: https://github.com/microsoft/pylance-release/blob/main/docs/howto/unresolved-imports.md

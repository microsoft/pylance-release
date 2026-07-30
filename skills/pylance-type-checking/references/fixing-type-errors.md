# Fixing Type Errors

Organized by the `report*` diagnostic that fires. Always prefer fixing the code over suppressing; suppress only as a last resort (see [When to suppress](#when-to-suppress-vs-fix) below).

The level column shows when the rule first becomes active. See [type-checking-levels.md](type-checking-levels.md) for level details and [diagnostics-reference.md](diagnostics-reference.md) for the full rule lookup.

## Missing annotations / unknown types

### `reportMissingParameterType` (strict)

A function/method parameter has no type annotation.

```python
def greet(name):  # Warning: Type of parameter "name" is unknown
    print(f"Hello, {name}")
```

**Fix — add the annotation:**

```python
def greet(name: str) -> None:
    print(f"Hello, {name}")
```

### `reportUnknownParameterType` / `reportUnknownLambdaType` (strict)

A parameter's type can't be inferred (often from an untyped call or `Any`). Same fix: add an explicit annotation. If the unknown type originates from an untyped library, see [typed-imports-and-stubs.md](typed-imports-and-stubs.md).

### `reportUnknownVariableType` / `reportUnknownArgumentType` / `reportUnknownMemberType` (strict)

A variable/argument/member access has type `Unknown`, usually because it came from an untyped library or an unannotated function.

**Fix**: add a type annotation at the source, or install stubs for the library (`types-*` packages) or write `.pyi` stubs. See [typed-imports-and-stubs.md](typed-imports-and-stubs.md).

### `reportMissingTypeArgument` (strict)

A generic class or type alias is used without its type arguments.

```python
# Warning: Type argument expected
def get_items() -> list:
    return [1, 2, 3]
```

**Fix — add the type argument:**

```python
def get_items() -> list[int]:
    return [1, 2, 3]
```

### `reportInvalidTypeArguments` / `reportInvalidTypeVarUse` (basic)

Wrong or inconsistent generic arguments, or misuse of a constrained `TypeVar` (e.g., `Box[int, str]` where one arg is expected). Fix by supplying the correct number/type of generic arguments, or by fixing the `TypeVar` definition (correct bounds, constraints, variance).

## Return / argument / assignment mismatches

### `reportReturnType` (basic)

The returned value doesn't match the declared return type.

```python
def greet(name: str) -> str:
    if not name:
        return None  # 'None' is not assignable to 'str'
    return f"Hello, {name}"
```

**Fix — either correct the value or correct the annotation:**

```python
def greet(name: str) -> str | None:
    if not name:
        return None
    return f"Hello, {name}"
```

### `reportArgumentType` (basic)

The argument passed to a function doesn't match the parameter's declared type. Fix by passing the correct type, or by widening/narrowing the annotation, or by narrowing the value (see [type-narrowing.md](type-narrowing.md)).

### `reportAssignmentType` (basic)

Assigning a value whose type doesn't match the variable's declared type. Fix by correcting the value or the annotation.

### `reportGeneralTypeIssues` (basic)

Umbrella rule for type incompatibilities not covered by more specific rules — protocol mismatches, subclassing a `@final` class, covariant `TypeVar` misuse, etc. Fix by correcting the annotation or the value to match.

## Optional / `None` handling (the `reportOptional*` family)

All of these fire when you use a possibly-`None` value (`X | None` / `Optional[X]`) in a context that requires a non-`None` value:

| Rule | Fires when you |
| ---- | -------------- |
| `reportOptionalMemberAccess` | access an attribute (`x.foo`) |
| `reportOptionalCall` | call it (`x()`) |
| `reportOptionalSubscript` | subscript it (`x[0]`) |
| `reportOptionalIterable` | iterate it (`for i in x`) |
| `reportOptionalContextManager` | use as `with x:` |
| `reportOptionalOperand` | use as an operand (`x + 1`) |

**Fix — narrow away `None` first.** This is the single most common type-error fix:

```python
from typing import Optional

def process(value: Optional[str]) -> str:
    return value.upper()  # Error: "upper" not known on None
```

**Fix — narrow with a check:**

```python
def process(value: Optional[str]) -> str:
    if value is None:
        return ""
    return value.upper()  # OK — Pylance knows value is str here
```

See [type-narrowing.md](type-narrowing.md) for all narrowing patterns (`is None`, `isinstance`, truthiness, `TypeGuard`/`TypeIs`).

## Inheritance / overrides

### `reportIncompatibleMethodOverride` / `reportIncompatibleVariableOverride` (standard)

A subclass override has a signature incompatible with the parent (e.g., extra required params, narrower param type, broader return type). Fix by aligning the override signature to the parent's contract.

### `reportUntypedBaseClass` (strict)

Inheriting from a base class Pylance can't see types for. Fix by installing stubs for that base, adding a `py.typed` marker, or inheriting from a typed base. See [typed-imports-and-stubs.md](typed-imports-and-stubs.md).

### `reportImplicitOverride` (opt-in)

A method overrides a parent method without `@override`. Fix by adding the `@override` decorator (typing/`typing_extensions`).

## Unused / dead code (mostly strict)

| Rule | Fix |
| ---- | --- |
| `reportUnusedImport` | remove the import (or prefix with `_` if intentionally unused) |
| `reportUnusedVariable` | remove the variable, or rename to `_`/`_unused` |
| `reportUnusedFunction` / `reportUnusedClass` | remove it, or add `__all__` / prefix with `_` |
| `reportUnusedExpression` | make it an assignment or remove it |
| `reportUnnecessaryCast` | remove the redundant `cast(...)` — the type was already correct |
| `reportUnnecessaryComparison` / `reportUnnecessaryIsInstance` / `reportUnnecessaryContains` | remove the redundant check — the type is already narrowed |
| `reportDuplicateImport` | remove the duplicate import |
| `reportDeprecated` | replace the deprecated symbol with its replacement |

## Stubs and imports

### `reportMissingTypeStubs` (strict)

An imported library has no `.pyi` stubs or `py.typed` marker. See [typed-imports-and-stubs.md](typed-imports-and-stubs.md) for full fixes (install `types-*` packages, write `.pyi` stubs, or prefer `py.typed` libraries).

### `reportMissingImports` (off)

An import can't be resolved at all. See [typed-imports-and-stubs.md](typed-imports-and-stubs.md) (install the package, `TYPE_CHECKING` imports for circular dependencies).

### `reportMissingModuleSource` (off, warning)

The module resolves but its source can't be found (e.g., installed as a compiled extension). Usually harmless; install stubs to get types.

## Attribute access

### `reportAttributeAccessIssue` (basic)

Accessing an undefined or typo'd attribute, or an instance attribute not initialized in `__init__`.

**Fix — initialize instance variables in `__init__`:**

```python
class Counter:
    def __init__(self) -> None:
        self.count = 0  # declare all instance attributes here

    def increment(self) -> None:
        self.count += 1
```

### `reportUninitializedInstanceVariable` (opt-in)

Instance variable declared via annotation but never assigned in `__init__`. Assign it, or use a default.

## When to suppress vs fix

Prefer fixing the code. Suppress only when:

- The code is genuinely dynamic and a static type can't express it.
- A third-party stub is wrong and you're waiting on an upstream fix.
- Temporarily unblocking work on a legacy file.

### Suppression options (preferred to least)

1. **`# pyright: ignore[ruleName]`** — scoped to one rule on one line. Preferred.
   ```python
   x = dynamic_thing()  # pyright: ignore[reportUnknownVariableType]
   ```
2. **`# type: ignore`** — broad, suppresses everything on the line. Avoid unless you must (it suppresses other checkers too and hides future errors).
3. **`cast(TargetType, value)`** — assert a type without a runtime check. Use when you know more than the type system.
   ```python
   from typing import cast
   items = cast(list[str], raw)
   ```
4. **Per-file comment** — `# pyright: reportMissingTypeStubs=false` at the top of a file disables one rule for that whole file. See [type-checking-levels.md](type-checking-levels.md).
5. **Project-wide** — to disable a rule across the whole project, set it to `none` in `pyrightconfig.json` or `[tool.pyright]` (see the [settings docs](https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_diagnosticSeverityOverrides.md)).

### `reportUnnecessaryTypeIgnoreComment`

Fires (opt-in) when a `# type: ignore` or `# pyright: ignore` no longer suppresses anything — i.e., the error it was hiding is already fixed. Remove the now-dead comment to keep the codebase clean.

> **Tip**: prefer `# pyright: ignore[ruleName]` over `# type: ignore` so that `reportUnnecessaryTypeIgnoreComment` can later flag it for cleanup, and so you only suppress exactly what you intend.

## See Also

- [Type narrowing](type-narrowing.md) — the fix for almost all `reportOptional*` errors and many `reportArgumentType`/`reportReturnType` errors
- [Typed imports & stubs](typed-imports-and-stubs.md) — fixes for `reportMissingTypeStubs`, `reportMissingImports`, `reportUnknown*`
- [Type-checking levels](type-checking-levels.md) — what fires at each level and per-file overrides
- [Diagnostics reference](diagnostics-reference.md) — full lookup table

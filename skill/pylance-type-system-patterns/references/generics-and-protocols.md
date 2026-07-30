# Generics, Protocol, TypedDict, and Literal

A distilled mini-guide. The Pylance docs corpus has **no standalone page** for generics/Protocol — these topics are covered only via diagnostic pages and the narrowing guide. This reference fills that gap and links back to the authoritative diagnostics.

## TypeVar and generics

`TypeVar` parameterizes a generic. Use it for functions that preserve the argument type, and for generic classes.

```python
from typing import TypeVar

T = TypeVar("T")

def first(xs: list[T]) -> T:          # return type tracks the element type
    return xs[0]

class Stack[T]:                      # Python 3.12+ generic class syntax
    def push(self, x: T) -> None: ...
```

Constrain or bound a TypeVar:

```python
T = TypeVar("T", bound=int)           # T must be int or subtype
T2 = TypeVar("T2", str, bytes)        # T2 is str | bytes
```

Related diagnostics when generics are misused:
- [reportInvalidTypeVarUse](../../docs/diagnostics/reportInvalidTypeVarUse.md) — TypeVar declared/used incorrectly.
- [reportInvalidTypeArguments](../../docs/diagnostics/reportInvalidTypeArguments.md) — wrong type arguments supplied to a generic.
- [reportMissingTypeArgument](../../docs/diagnostics/reportMissingTypeArgument.md) — a generic used without its type argument.

## Protocol (structural typing)

A `Protocol` defines an interface structurally — a class satisfies it by having the right members, no inheritance required.

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None: ...

def shutdown(c: Closeable) -> None:
    c.close()

class Resource:                        # implicitly satisfies Closeable
    def close(self) -> None: ...

shutdown(Resource())                   # OK
```

`@runtime_checkable` protocols can be used with `isinstance` (only checks attributes exist, not their types).

> The docs surface Protocol indirectly through override/access diagnostics; there is no dedicated guide. The main gotchas Pyright flags: mismatched member signatures in overrides and `reportAttributeAccessIssue`.

Related: [reportIncompatibleMethodOverride](../../docs/diagnostics/reportIncompatibleMethodOverride.md), [reportAttributeAccessIssue](../../docs/diagnostics/reportAttributeAccessIssue.md).

## TypedDict

A `TypedDict` types dict literals with a fixed key set and per-key value types. `NotRequired`/`Required` mark optional/mandatory keys.

```python
from typing import TypedDict, NotRequired

class User(TypedDict):
    id: int
    name: str
    email: NotRequired[str]

u: User = {"id": 1, "name": "Ann"}
```

Related diagnostic: [reportTypedDictNotRequiredAccess](../../docs/diagnostics/reportTypedDictNotRequiredAccess.md) — accessing a `NotRequired` key without first checking presence.

## Literal

`Literal` pins a value to a specific constant, enabling discriminated-union narrowing.

```python
from typing import Literal, overload

Mode = Literal["r", "w"]

def open(path: str, mode: Mode) -> None: ...
```

`Literal` pairs with `match`/narrowing to discriminate unions — see the narrowing guide: [../../docs/howto/type-narrowing.md](../../docs/howto/type-narrowing.md).

## Further reading

- Type narrowing (the companion pattern to all of the above): [../../docs/howto/type-narrowing.md](../../docs/howto/type-narrowing.md)
- Deprecation of old `typing` aliases (`List`, `Tuple`, …): [../../docs/settings/python_analysis_typeEvaluation_deprecateTypingAliases.md](../../docs/settings/python_analysis_typeEvaluation_deprecateTypingAliases.md)

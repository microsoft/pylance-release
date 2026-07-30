# Type Narrowing

Pylance uses **type narrowing** to track how a variable's type changes through your code. When you see type errors on variables with union types (`str | None`, `int | str`), type narrowing is usually the fix — use a conditional check to tell Pylance which variant you have.

This is the single most common fix for the `reportOptional*` family and many `reportArgumentType`/`reportReturnType` errors. See [fixing-type-errors.md](fixing-type-errors.md).

## The Basic Idea

```python
from typing import Optional

def process(value: Optional[str]) -> str:
    # value is str | None here
    return value.upper()  # Error: "upper" is not a known attribute of None
```

**Fix — narrow with a check:**

```python
def process(value: Optional[str]) -> str:
    if value is None:
        return ""
    # After the check, Pylance knows value is str
    return value.upper()  # OK
```

Narrowing works in both branches:

```python
def describe(val: int | str):
    if isinstance(val, int):
        print(val + 1)      # OK — val is int
    else:
        print(val.upper())  # OK — val is str
```

## Patterns

### Check for `None`

The most common case — narrowing `Optional[X]` (which is `X | None`):

```python
if x is not None:      # Preferred
    ...

if x is None:
    return             # Early return narrows x to non-None after this line

assert x is not None   # Narrows x to non-None from here onward
```

### `isinstance` checks

Narrow a union to a specific class:

```python
def handle(event: KeyEvent | MouseEvent | CloseEvent):
    if isinstance(event, KeyEvent):
        print(event.key)        # event is KeyEvent
    elif isinstance(event, MouseEvent):
        print(event.x, event.y) # event is MouseEvent
    else:
        print("closing")        # event is CloseEvent
```

`isinstance` also works with tuples of types: `if isinstance(val, (int, float)):`.

### Truthiness checks

```python
def greet(name: str | None):
    if name:  # narrows to str (excludes None and "")
        print(f"Hello, {name}")
```

> **Note**: truthiness narrowing for numerics is limited — `if val:` on `float | None` only narrows away `None` in the positive branch, because `0.0` is also falsy.

### `type()` checks (exact type, not subclasses)

```python
if type(val) is int:
    print(val + 1)  # val is exactly int, not a subclass
```

### Discriminated unions (TypedDict / Literal field)

```python
from typing import Literal, TypedDict

class Dog(TypedDict):
    kind: Literal["dog"]
    bark_volume: int

class Cat(TypedDict):
    kind: Literal["cat"]
    purr_frequency: float

Pet = Dog | Cat

def describe(pet: Pet):
    if pet["kind"] == "dog":
        print(pet["bark_volume"])     # pet is Dog
    else:
        print(pet["purr_frequency"])  # pet is Cat
```

### `in` / `not in`

```python
from typing import Literal

def handle_status(status: Literal["ok", "error", "pending"]):
    if status in ("ok", "pending"):
        print("not an error")  # status is Literal["ok", "pending"]
```

`in` also narrows TypedDict key access: `if "name" in d:` makes `d["name"]` safe.

### `len()` on tuples

```python
def process(val: tuple[int] | tuple[int, str]):
    if len(val) == 2:
        print(val[1].upper())  # val is tuple[int, str]
```

### `callable()`

```python
if callable(x):
    x()  # x is a callable
```

## Supported Type Guards

| Pattern | Narrows both `if`/`else`? |
| ------- | ------------------------- |
| `x is None` / `x is not None` | Yes |
| `isinstance(x, T)` | Yes |
| `issubclass(x, T)` | Yes |
| `type(x) is T` / `type(x) == T` | Yes |
| `x is C` (class identity) | Yes |
| Truthiness (`if x:`) | Partial (falsy values overlap) |
| `x == L` (literal comparison) | Depends on type |
| `x in collection` | Yes |
| `S in D` (TypedDict key check) | Yes |
| `len(x) == L` (tuple length) | Yes |
| `x.field is/== V` (discriminator) | Yes |
| `callable(x)` | Yes |
| Aliased conditions (`is_valid = x is not None; if is_valid:`) | Yes |
| User-defined `TypeGuard` / `TypeIs` | See below |

Full list: [Pyright Type Guards](https://microsoft.github.io/pyright/#/type-concepts-advanced?id=type-guards).

## Custom Type Guards (`TypeGuard` and `TypeIs`)

When built-in narrowing isn't enough, define a guard function.

### `TypeIs` (Python 3.13+ / `typing_extensions`) — preferred

Narrows in **both** `if` and `else` branches:

```python
from typing import TypeIs  # or typing_extensions.TypeIs

def is_str(val: object) -> TypeIs[str]:
    return isinstance(val, str)

def process(val: int | str):
    if is_str(val):
        print(val.upper())  # val is str
    else:
        print(val + 1)      # val is int
```

### `TypeGuard` (Python 3.10+ / `typing_extensions`)

Narrows **only** the `if` branch — use when the narrowed type isn't a true subtype:

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in val)

def process(val: list[object]):
    if is_str_list(val):
        print(val[0].upper())  # val is list[str]
    # else: val is still list[object] (not narrowed)
```

> **When to use which**: prefer `TypeIs` when possible (narrows both branches). Use `TypeGuard` when the output type isn't a true narrowing of the input (e.g., `list[object]` → `list[str]`).

## Why Narrowing Might Not Work

### Narrowing resets after reassignment

```python
def process(val: str | None):
    if val is not None:
        val = some_function()  # type is now some_function's return type
        print(val.upper())     # may error — narrowing was reset
```

### Narrowing in closures depends on mutation

Pyright retains narrowing for variables captured by closures **only if** it can prove the variable isn't reassigned after the closure is defined and doesn't use `nonlocal`/`global`. If either is violated, the narrowed type is lost:

```python
def process_broken(val: str | None):
    if val is not None:
        def inner():
            print(val.upper())  # Error — val is reassigned below
        val = None               # reassignment after closure definition
        inner()
```

**Fix — capture the narrowed value in a local before the closure:**

```python
def process_safe(val: str | None):
    if val is not None:
        captured = val  # captured is str (narrowed, not reassigned)
        def inner():
            print(captured.upper())  # OK
        val = None
        inner()
```

### Unsupported expression forms

Narrowing only works on simple names, member-access chains (`a.b.c`), integer subscripts (`a[0]`), and string subscripts (`a["key"]`). Results of method calls or arithmetic are not narrowed.

### `assert` vs `if`

- `assert x is not None` — narrows from that line forward (good for preconditions). Note: disabled under `python -O`.
- `if x is not None:` — narrows within the `if` block only.

## Narrowing `Any`

`isinstance` narrows `Any` to the checked type — the most common way to work with `Any` safely:

```python
from typing import Any

def process(data: Any):
    if isinstance(data, dict):
        for key in data:  # data is dict
            print(key)
```

## Debugging Narrowing

Use `reveal_type(x)` to see exactly what Pylance thinks the type is at a given point:

```python
def process(val: str | None):
    if val is not None:
        reveal_type(val)   # info: str
        ...
```

`reveal_type` is a Pyright/Pylance built-in with no runtime effect (it errors at type-check time, printing the type). Remove it after debugging.

## See Also

- [Fixing type errors](fixing-type-errors.md) — which `report*` rules narrowing resolves
- [Typed imports & stubs](typed-imports-and-stubs.md) — when the unknown type comes from an untyped library
- Full how-to: https://github.com/microsoft/pylance-release/blob/main/docs/howto/type-narrowing.md
- Pyright type narrowing spec: https://microsoft.github.io/pyright/#/type-concepts-advanced?id=type-narrowing

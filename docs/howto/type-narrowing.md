# How to Use Type Narrowing to Fix Type Errors

Pylance uses **type narrowing** to track how a variable's type changes through your code. When you see type errors on variables or parameters with union types (like `str | None` or `int | str`), type narrowing is usually the fix — use a conditional check to tell Pylance which type you're working with.

---

## Table of Contents

- [What Is Type Narrowing?](#what-is-type-narrowing)
- [Common Patterns](#common-patterns)
- [Supported Type Guards](#supported-type-guards)
- [Custom Type Guards (`TypeGuard` and `TypeIs`)](#custom-type-guards-typeguard-and-typeis)
- [Why Narrowing Might Not Work](#why-narrowing-might-not-work)
- [FAQ](#faq)
- [Related Guides](#related-guides)

---

## What Is Type Narrowing?

When a variable has a union type (like `str | None`), Pylance doesn't know which variant you have at any given point. Type narrowing uses conditional checks to eliminate possibilities:

```python
from typing import Optional

def process(value: Optional[str]) -> str:
    # Here, value is str | None
    return value.upper()  # Error: "upper" is not a known attribute of "None"
```

**Fix — narrow with a check:**

```python
def process(value: Optional[str]) -> str:
    if value is None:
        return ""
    # After the check, Pylance knows value is str
    return value.upper()  # OK
```

Narrowing works in both the `if` and `else` branches:

```python
def describe(val: int | str):
    if isinstance(val, int):
        print(val + 1)      # OK — val is int here
    else:
        print(val.upper())  # OK — val is str here
```

---

## Common Patterns

### Check for `None`

The most common use case — narrowing `Optional[X]` (which is `X | None`):

```python
# All of these narrow away None:
if x is not None:      # Preferred
    ...

if x is None:
    return             # Early return narrows x to non-None after this line

assert x is not None   # Narrows x to non-None from here onward
```

### `isinstance` checks

Narrow union types to a specific class:

```python
def handle(event: KeyEvent | MouseEvent | CloseEvent):
    if isinstance(event, KeyEvent):
        print(event.key)        # OK — event is KeyEvent
    elif isinstance(event, MouseEvent):
        print(event.x, event.y) # OK — event is MouseEvent
    else:
        print("closing")        # event is CloseEvent
```

`isinstance` also works with tuples of types:

```python
if isinstance(val, (int, float)):
    print(val + 1)  # val is int | float
```

### Truthiness checks

Narrowing based on truthy/falsy values:

```python
def greet(name: str | None):
    if name:  # Narrows to str (excludes None and empty string)
        print(f"Hello, {name}")
```

> **Note**: Truthiness narrowing for numeric types is limited — `if val:` on `float | None` only narrows away `None` in the positive branch, because `0.0` is also falsy.

### `type()` checks

More precise than `isinstance` — checks exact type, not subclasses:

```python
if type(val) is int:
    print(val + 1)  # val is exactly int, not a subclass
```

### Discriminated unions

Narrow based on a distinguishing field:

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
        print(pet["bark_volume"])     # OK — pet is Dog
    else:
        print(pet["purr_frequency"])  # OK — pet is Cat
```

### `in` / `not in` checks

```python
from typing import Literal

def handle_status(status: Literal["ok", "error", "pending"]):
    if status in ("ok", "pending"):
        print("not an error")  # status is Literal["ok", "pending"]
```

### `len()` checks for tuples

```python
def process(val: tuple[int] | tuple[int, str]):
    if len(val) == 2:
        print(val[1].upper())  # OK — val is tuple[int, str]
```

---

## Supported Type Guards

Pylance supports these narrowing expressions:

| Pattern                             | Example                                  | Narrows both `if`/`else`?      |
| ----------------------------------- | ---------------------------------------- | ------------------------------ |
| `x is None` / `x is not None`       | `if x is not None:`                      | Yes                            |
| `isinstance(x, T)`                  | `if isinstance(x, str):`                 | Yes                            |
| `issubclass(x, T)`                  | `if issubclass(cls, Base):`              | Yes                            |
| `type(x) is T` / `type(x) == T`     | `if type(x) is int:`                     | Yes                            |
| `x is C` (class identity)           | `if x is MyClass:`                       | Yes                            |
| Truthiness (`if x:`)                | `if name:`                               | Partial (falsy values overlap) |
| `x == L` (literal comparison)       | `if x == "hello":`                       | Depends on type                |
| `x in collection`                   | `if x in valid_set:`                     | Yes                            |
| `S in D` (TypedDict key check)      | `if "name" in d:`                        | Yes                            |
| `len(x) == L` (tuple length)        | `if len(t) == 2:`                        | Yes                            |
| `x.field is/== V` (discriminator)   | `if obj.kind == "a":`                    | Yes                            |
| `callable(x)`                       | `if callable(x):`                        | Yes                            |
| `bool(x)`                           | Same as truthiness                       | Partial                        |
| Aliased conditions                  | `is_valid = x is not None; if is_valid:` | Yes                            |
| User-defined `TypeGuard` / `TypeIs` | `if is_str_list(x):`                     | See below                      |

For the full list, see Pyright's [Type Guards documentation](https://microsoft.github.io/pyright/#/type-concepts-advanced?id=type-guards).

---

## Custom Type Guards (`TypeGuard` and `TypeIs`)

When built-in narrowing isn't enough, define a custom type guard function:

### `TypeIs` (Python 3.13+ / `typing_extensions`)

`TypeIs` narrows in **both** `if` and `else` branches — preferred when the check is a true subtype test:

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

`TypeGuard` narrows only in the `if` branch — use when the narrowed type isn't a true subtype:

```python
from typing import TypeGuard  # or typing_extensions.TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in val)

def process(val: list[object]):
    if is_str_list(val):
        print(val[0].upper())  # val is list[str]
    # else: val is still list[object] (not narrowed)
```

> **When to use which**: Prefer `TypeIs` when possible (narrows both branches). Use `TypeGuard` when the output type isn't a true narrowing of the input type (e.g., `list[object]` → `list[str]`).

---

## Why Narrowing Might Not Work

### Narrowing resets after mutation

If you reassign the variable, the narrowed type is lost:

```python
def process(val: str | None):
    if val is not None:
        val = some_function()  # Type is now the return type of some_function
        print(val.upper())     # May error — narrowing was reset
```

### Narrowing in closures depends on mutation

Pyright retains narrowing for variables captured by closures **if** it can prove the variable is not reassigned after the closure is defined and does not use a `nonlocal` or `global` binding. If either condition is violated, the narrowed type is lost:

```python
def process(val: str | None):
    if val is not None:
        def inner():
            print(val.upper())  # OK — val is not reassigned after inner() is defined
        inner()

def process_broken(val: str | None):
    if val is not None:
        def inner():
            print(val.upper())  # Error — val is reassigned below, so narrowing is lost
        val = None              # Reassignment after closure definition
        inner()
```

If you hit this, capture the narrowed value in a local before the closure:

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

Narrowing only works on certain expression forms: simple names, member access chains (`a.b.c`), integer subscripts (`a[0]`), and string subscripts (`a["key"]`). Complex expressions like `a.method()` results or arithmetic are not narrowed.

### `assert` vs `if`

Both `assert` and `if` work for narrowing, but use them differently:

- `assert x is not None` — narrows from that line forward (good for preconditions)
- `if x is not None:` — narrows within the `if` block only

---

## FAQ

### Q: I did `isinstance(x, MyClass)` but Pylance still shows an error

Common causes:

1. **The variable was reassigned** between the check and the usage. Check that `x` isn't modified between the `isinstance` call and the member access.
2. **The check is in a different scope** (e.g., a helper function). The helper needs to return `TypeIs[MyClass]` or `TypeGuard[MyClass]` for the narrowing to propagate to the caller.
3. **The class is imported from a different module** and Pylance sees a different type than expected. Use `reveal_type(x)` to check what Pylance thinks the type is.

### Q: How do I narrow `Any`?

`isinstance` checks narrow `Any` to the checked type. This is the most common way to work with `Any` safely:

```python
from typing import Any

def process(data: Any):
    if isinstance(data, dict):
        # data is narrowed to dict here
        for key in data:
            print(key)
```

### Q: How do I suppress a type error instead of narrowing?

If type narrowing doesn't apply (e.g., dynamic code), you can:

- `# type: ignore[rule-name]` — suppress a specific diagnostic on one line
- `# pyright: ignore[rule-name]` — Pyright-specific equivalent
- `cast(TargetType, value)` — assert a type without runtime check
- `python.analysis.ignore` — suppress all diagnostics for entire files

See [How to Gradually Adopt Strict Type Checking](gradual-strict-adoption.md) for strategies.

---

## Related Guides

- [How to Gradually Adopt Strict Type Checking](gradual-strict-adoption.md) — suppress or enable diagnostics incrementally
- [Settings Troubleshooting](settings-troubleshooting.md) — why settings may not take effect
- Pyright's [Type Narrowing documentation](https://microsoft.github.io/pyright/#/type-concepts-advanced?id=type-narrowing) — full specification

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

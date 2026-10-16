# Docstring Resolution Order

When you hover a symbol in an editor — or trigger signature help or read the documentation attached to a completion — a Python language server shows a single docstring. For many symbols there is more than one candidate: a function and its `@overload` declarations, an `__init__` and a `__new__`, a class docstring, an inherited member on any base class, and the same again in a stub (`.pyi`) versus its source (`.py`).

This document describes **which** docstring Pylance selects. Python concepts such as method resolution order, overloads, stub files and assignment docstrings provide the candidates; the rules below describe Pylance's choices.

Hover and completions use the same priorities, but a call hover can narrow the overload candidates while completion documentation uses the symbol's full type. Signature help uses the active-entry borrowing described below.

Hover and completions resolve to a single docstring. Signature help is the exception: it enumerates **every** overload as its own signature entry, each paired with its own docstring. There, the borrowing steps in the rules below (falling back from an undocumented candidate to the implementation, a sibling overload, or a class docstring) apply only to the **active** signature — the entry currently selected in the editor, not necessarily the one matching the argument types. Every other enumerated overload shows only its own docstring, or nothing. The active entry can borrow docstring text, but each entry uses its own parameter documentation.

---

## Table of Contents

- [Design Principles](#design-principles)
- [Docstring Kinds](#docstring-kinds)
- [Terminology](#terminology)
- [Resolution by Symbol Kind](#resolution-by-symbol-kind)
- [Constructor Resolution — The Algorithm](#constructor-resolution--the-algorithm)
- [Rule A — Overload Selection](#rule-a--overload-selection)
- [Rule B — `__init__` vs `__new__`](#rule-b---init--vs---new)
- [Rule C — Override and Inheritance](#rule-c--override-and-inheritance)
- [Rule D — Multiple Inheritance (MRO)](#rule-d--multiple-inheritance-mro)
- [Rule E — Constructor Methods vs Class Docstring](#rule-e--constructor-methods-vs-class-docstring)
- [Rule F — Stub vs Source](#rule-f--stub-vs-source)
- [The Full Ordered List (Constructors)](#the-full-ordered-list-constructors)
- [Examples](#examples)
- [Edge Cases and Special Constructs](#edge-cases-and-special-constructs)
- [Open Policy Decision](#open-policy-decision)

---

## Design Principles

Every rule derives from four principles. When a case is not covered explicitly, resolve it by applying these in order:

1. **Most specific first.** The docstring closest to what the reader points at wins: the call-matched overload over other overloads; the derived class over its base classes.
2. **Prefer documentation of the thing being invoked.** A constructor is documentation _about constructing_, so a constructor docstring outranks a generic class docstring.
3. **Exhaust before inheriting.** Never take a docstring from a base class while a more-derived class still offers one for the same tier (methods before methods; class docstrings before class docstrings).
4. **Empty is usually not a stop.** A missing or empty docstring is skipped; resolution continues. A class's own explicitly empty docstring blocks base-class docstring inheritance.

Resolution returns the **first non-empty** docstring found in the defined order, or nothing (signature only) if none exists.

---

## Docstring Kinds

The following docstring kinds are supported; each is a string literal placed where the language defines documentation for that symbol:

| Kind                     | Where it lives                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------ |
| **Module**               | The leading string literal of a `.py`/`.pyi` file                                    |
| **Class**                | The leading string literal in a class body                                           |
| **Function**             | The leading string literal in a `def` body                                           |
| **Method**               | A function docstring on a class member                                               |
| **Constructor**          | The docstring of `__init__` and/or `__new__`                                         |
| **Overload**             | A docstring on an individual `@overload` declaration                                 |
| **Property**             | The docstring of a property getter or setter                                         |
| **Variable / attribute** | A string literal immediately following an assignment (a widely supported convention) |

---

## Terminology

- **Call hover** — hovering a call expression, e.g. `Line(a, b)`. Arguments participate in overload resolution.
- **Symbol hover** — hovering a bare name, e.g. the class `Line`, with no call. No arguments, so no overload is "matched."
- **Matched overload** — an overload selected for a call's arguments. More than one can match. For documentation:
    - **Zero overloads match** (e.g. an argument-type error): consider the full overload set as documentation candidates.
    - **Multiple overloads match** (ambiguous): use the first candidate with documentation; fall back to the implementation if none has it.
- **Implementation** — the non-`@overload` `def` that carries the runtime body. Present in source files; absent in `.pyi` stubs.
- **Declaration order** — the order of overload declarations in the analyzed symbol. Stub→source fallback happens within each candidate (Rule F), rather than merging source and stub overload lists.
- **MRO** — the C3-linearized method resolution order of a class, `[C, …bases…, object]`. **Builtin base classes** (such as `object` and `int`) are excluded by design as _inherited_ docstring sources, so their generic constructor docstrings never leak into user classes. The class **being constructed** is always considered, even when it is itself builtin — so hovering `object()` or `int()` still shows that builtin's own constructor docstring.
- **Directly defined** — a member appearing in a class's own body (its namespace), as opposed to one it only inherits. Inheritance is expressed by the MRO walk, never by a per-class lookup that reaches into base classes.
- **Tier** — a category of source: _constructor-method_ docstrings vs _class_ docstrings. Rule E orders the tiers.

---

## Resolution by Symbol Kind

Simple kinds resolve directly; constructors are the complex case and have their own algorithm below.

### Modules

The module-level docstring (the leading string literal). Rule F applies if a `.pyi` has none.

### Functions

1. Documented overload candidates (narrowed by a call when possible; otherwise the full overload set)
2. Implementation docstring
3. Other overloads, in declaration order

When signature help enumerates these overloads (one entry per overload), the fallback to the implementation or another overload applies only to the **active** entry selected in the editor: an undocumented active overload still falls back to the implementation and then the other overloads, but a non-active overload entry shows only its own docstring, or nothing. Parameter documentation always comes from that entry's own docstring.

### Classes (symbol hover on the class name, no call)

1. The class's own docstring
2. Stub → source fallback for the class (Rule F)
3. A base class's own non-empty docstring, in MRO order, only when the class has no docstring of its own. An explicitly empty own class docstring blocks this inheritance; undocumented base stubs do not borrow source class documentation.

### Methods

Same as functions, extended with inheritance: if the derived method is undocumented, the same-named method on each base class is consulted in MRO order (Rules C/D).

### Properties

A property checks its getter and setter declarations before inherited property declarations:

1. The first documented getter or setter declaration on the current class
2. Inherited property getter or setter documentation from a base class, in MRO order
3. Otherwise none

### Variables and attributes

1. A string literal immediately following the assignment, if present
2. For instance/class attributes: the docstring on the declaring class member, following the MRO walk (Rule D)
3. Otherwise, an instance value does not fall back to its declared type's class docstring — hover the type name to read that documentation. Function, module and class-object aliases can show the referenced value's documentation, combined with distinct assignment documentation when present.

### Callable instances

When a source-defined, non-builtin callable value has no assignment/member docstring, hovering it can show its `__call__` documentation. For a callable type declared in a `.pyi` stub, this fallback is not available on plain-variable hover.

### Constructors

A construction expression (`ClassName(...)`) is the one case with competing method/class/hierarchy candidates. It follows the dedicated algorithm in the next section.

---

## Constructor Resolution — The Algorithm

Resolution runs in two phases over the MRO. Return at the first non-empty result.

```
resolveConstructorDoc(C, call?):
    mro = MRO(C) excluding builtin BASE classes   # C itself is always kept, even if builtin

    # -- Phase 1: constructor-method docstrings (Rules A, B, C, D) --
    for M in mro:                      # derived -> base
        d = constructorMethodDoc(M, call)
        if d: return d

    # -- Phase 2: class docstrings (Rule E) --
    for M in ([C] if classDeclOf(C) has an explicit empty docstring else mro):  # derived -> base
        d = docstringOf(classDeclOf(M)) if M is C else classDeclOf(M).docstring
        if d: return d

    return none                        # nothing found -> render signature only


constructorMethodDoc(M, call):         # only docstrings DIRECTLY on class M
    d = methodDoc(M, "__init__", call) # Rule B: __init__ first
    if d: return d
    d = methodDoc(M, "__new__", call)  # Rule B: __new__ only if __init__ empty
    if d: return d
    return none


methodDoc(M, name, call):              # Rule A ordering within one class
    if name not in directMembersOf(M): return none   # not defined here -> caller's MRO loop handles inheritance
    method = directMembersOf(M)[name]

    candidates = []                    # Rule A priority order
    if call:
        m = the call's overload candidates for this method name, otherwise []
        candidates.extend(m + their original overload declarations)  # tier 1
    if method.implementation and method.implementation not in candidates:
        candidates.append(method.implementation)   # tier 2: implementation
    for ov in overloadsOf(method):          # tier 3: @overloads only, in declaration order
        if ov not in candidates: candidates.append(ov)

    for decl in candidates:
        d = docstringOf(decl)          # Rule F (stub->source) lives here
        if d: return d
    return none


docstringOf(decl):                     # single choke point for Rule F
    if decl has a non-empty docstring: return it
    if decl is declared in a .pyi stub:
        src = correspondingSourceDecl(decl)   # matching .py declaration, if any
        if src and src has a non-empty docstring: return src's docstring
    return none
```

Notes for implementers:

- `methodDoc` takes the class `M` explicitly and only inspects members **directly defined** on `M`. Inheritance is never a per-class lookup that reaches into bases — it is expressed solely by the `for M in mro` loop.
- Rule F is centralized in `docstringOf` for matched overloads, implementations, other overloads, and the original class's own declaration. Inherited class docstrings are read directly from each base, without stub→source recovery for that base.
- Constructor-method resolution uses the call's overload candidates for the same method name through the MRO. A failed match retains the full set rather than matching arguments again for each base.

Helper predicates used above:

- `directMembersOf(M)` — the members declared in `M`'s own body, excluding anything only inherited.
- `overloadsOf(method)` — the method's `@overload` declarations **only** (never the implementation), in declaration order. `matchedOverload` likewise returns one of these `@overload` declarations, never the implementation.
- `method.implementation` — the single non-`@overload` `def` with a runtime body, or `none` for a stub-only symbol.
- `classDeclOf(M)` — the declaration of class `M` from which its class docstring is read.
- `correspondingSourceDecl(decl)` — for a `.pyi` declaration, the first mapped source declaration with documentation, or `none` if none is available.

Phase 1 walks the **entire** MRO for constructor-method docstrings before Phase 2 ever considers a class docstring — a deliberate consequence of Principle 2 (see [Rule E](#rule-e--constructor-methods-vs-class-docstring)).

---

## Rule A — Overload Selection

Within one method on one class, order candidates as:

| Priority | Candidate                                 | Applies to                       |
| -------- | ----------------------------------------- | -------------------------------- |
| 1        | **Overload candidates**                   | narrowed by a call, or full set  |
| 2        | **Implementation** (`def` with a body)    | source files (a `.pyi` has none) |
| 3        | **Other overloads**, in declaration order | always                           |

Rationale:

- **Matched first** — if the reader writes `Widget(42)` and the `int` overload is documented, that is the most relevant text.
- **Implementation second** — the implementation body holds the method's canonical/general docstring; the best fallback when the matched overload is undocumented.
- **Other overloads last** — a deterministic, source-ordered last resort.

For ordinary function/method **symbol hover**, consider the full overload set: the first documented overload can win before the implementation. A call matching **zero** overloads uses the same full set. If none has documentation, try the implementation and then the remaining overloads. Each candidate is subject to Rule F stub→source fallback.

---

## Rule B — `__init__` vs `__new__`

Within a single class:

- `__init__` is the primary constructor; all of its Rule A candidates are checked first.
- `__new__` is checked **only if** `__init__` on that same class yields nothing.
- A class defining only `__new__` (e.g. an immutable type) still resolves correctly.
- `__init__` and `__new__` from **different** classes are never combined in one step — the MRO walk handles cross-class ordering.

---

## Rule C — Override and Inheritance

When a derived class overrides a constructor (or method):

- The derived class's candidates are evaluated **before** the base class's.
- If the derived override is **undocumented** across all of its Rule A/B candidates, resolution continues up the MRO and **inherits** the base docstring for the same tier.
- If the derived override is documented anywhere in its candidates, it wins and the base is never consulted.

This yields the expected "inherited documentation" behavior: re-declaring without a docstring does not erase inherited docs, but adding any docstring on the derived side overrides them.

---

## Rule D — Multiple Inheritance (MRO)

For multiple base classes, the walk follows the class's **C3-linearized MRO**, not the source order of base declarations:

- Each class is visited exactly once, in MRO order.
- When two ancestors both document the same tier, the one **earlier in the MRO** wins.
- Diamonds resolve naturally: the shared base appears once, after all classes that derive from it.

For `class D(B, C)` where `B(A)` and `C(A)`, the MRO is `[D, B, C, A]` (then `object`, excluded).

---

## Rule E — Constructor Methods vs Class Docstring

Across the whole hierarchy, **all** constructor-method docstrings (Phase 1) are preferred over **any** class docstring (Phase 2):

- A base class's documented `__init__` outranks a derived class's class docstring, because Phase 1 spans the full MRO before Phase 2 begins.
- A class docstring is used only when no class in the MRO documents `__init__`/`__new__` at all.
- Class docstrings are then ordered by MRO (derived → base).

This is the primary tier-ordering decision; the alternative is discussed under [Open Policy Decision](#open-policy-decision).

---

## Rule F — Stub vs Source

Stub-to-source fallback applies to selected declarations and the original class's own docstring. It does not apply uniformly to inherited class docstrings: those are read directly from each base, so a doc-less base stub does not supply its source class docstring.

- If a selected declaration lives in a `.pyi` stub and has no docstring, resolve to the corresponding `.py` source declaration and use that docstring.
- If the symbol is **stub-only** (no `.py`), there is nothing to fall back to; the stub's own docstring (or nothing) is used.
- This never reorders the tiers above.

---

## The Full Ordered List (Constructors)

For a **call hover** on class `C` with MRO `[C, B₁, B₂, …]` (builtin bases such as `object` excluded), consult in order and return the first non-empty docstring:

**Phase 1 — constructor-method docstrings (walk the full MRO):**

1. `C.__init__` — call's overload candidates for this member
2. `C.__init__` — implementation
3. `C.__init__` — other overloads (declaration order)
4. `C.__new__` — call's overload candidates for this member
5. `C.__new__` — implementation
6. `C.__new__` — other overloads
7. `B₁.__init__` — call's overload candidates for this member
8. `B₁.__init__` — implementation
9. `B₁.__init__` — other overloads
10. `B₁.__new__` — call's overload candidates for this member
11. `B₁.__new__` — implementation
12. `B₁.__new__` — other overloads
13. …repeat steps 7–12 for `B₂`, `B₃`, … in MRO order…

**Phase 2 — class docstrings (walk the full MRO again):**

14. `C` — class docstring
15. `B₁` — class docstring
16. `B₂` — class docstring
17. …in MRO order…

**Phase 3:**

18. No docstring — render the signature only.

Each numbered entry is a flat step; the first non-empty docstring wins. For a **symbol hover** on the class name, use the class-docstring order instead; constructor-method entries do not participate.

---

## Examples

The examples are ordered from the simplest kind to the most complex composition. Each demonstrates a **different** case; none repeats an idea already shown. In each, `⇒` marks the resolved docstring.

Examples that hover a construction expression `ClassName(...)` follow the [constructor algorithm](#constructor-resolution--the-algorithm); every other example follows the [Resolution by Symbol Kind](#resolution-by-symbol-kind) rules.

### 1. Module docstring

```python
"""Utilities for geometry math."""
import math
```

Hovering the module `geometry` ⇒ **"Utilities for geometry math."**

### 2. Plain function

```python
def area(r: float) -> float:
    """Return the area of a circle of radius r."""
    ...
```

Hovering `area` or a call `area(2)` ⇒ **"Return the area of a circle of radius r."**

### 3. Plain class (symbol hover)

```python
class Vector:
    """A 2-D vector."""
```

Hovering the name `Vector` (not a call) ⇒ **"A 2-D vector."**

### 4. Instance method

```python
class Vector:
    def length(self) -> float:
        """Euclidean length."""
        ...
```

Hovering `v.length()` ⇒ **"Euclidean length."**

### 5. Variable / attribute docstring

```python
MAX_RETRIES = 5
"""Number of times a request is retried before failing."""
```

Hovering `MAX_RETRIES` ⇒ **"Number of times a request is retried before failing."**

### 6. Attribute with no own docstring shows no type docstring

```python
class Clock:
    """A monotonic clock."""

class Service:
    clock: Clock          # no assignment docstring, no member docstring
```

Hovering `service.clock` ⇒ **nothing** (signature only). The attribute has no docstring of its own, and a value reference is not documented by its type's class docstring; `Clock`'s docstring is shown only when you hover `Clock` itself.

### 7. Property getter

```python
class Circle:
    @property
    def diameter(self) -> float:
        """Twice the radius."""
        return self._r * 2
```

Hovering `c.diameter` ⇒ **"Twice the radius."**

### 8. Plain constructor

```python
class Timer:
    def __init__(self, seconds: float) -> None:
        """Create a timer that fires after `seconds`."""
        ...
```

Hovering `Timer(5)` ⇒ **"Create a timer that fires after `seconds`."**

### 9. Constructor falling back to the class docstring

```python
class Config:
    """Runtime configuration."""
    def __init__(self, path: str) -> None:   # no docstring
        ...
```

Hovering `Config("x.ini")` ⇒ **"Runtime configuration."** (no constructor-method docstring anywhere in the MRO ⇒ Phase 2 class docstring).

### 10. `__new__`-only constructor

```python
class Handle:
    def __new__(cls, raw: int) -> "Handle":
        """Wrap a raw OS handle."""
        ...
```

Hovering `Handle(3)` ⇒ **"Wrap a raw OS handle."** (`__init__` is absent ⇒ Rule B falls to `__new__`).

### 11. Overload — best match wins

```python
class Query:
    @overload
    def where(self, name: str) -> "Query":
        """Filter by column name."""
    @overload
    def where(self, index: int) -> "Query":
        """Filter by column index."""
    def where(self, key): ...
```

Hovering `q.where(0)` ⇒ **"Filter by column index."** (the matched `int` overload beats the other overload and the implementation).

<a id="12-overload--symbol-hover-uses-the-implementation"></a>

### 12. Overload — symbol hover uses the first documented overload

Same `Query.where` as example 11, but hovering the bare method `Query.where` (no call) ⇒ **"Filter by column name."** (first documented overload). The implementation is used only when the overload candidates have no documentation.

### 13. Overload — matched overload undocumented, a sibling supplies the text

```python
class Path:
    @overload
    def __init__(self) -> None: ...                 # matched by Path(), no docstring
    @overload
    def __init__(self, raw: str) -> None:
        """Build a path from a string."""
    def __init__(self, raw=""): ...
```

Hovering `Path()` ⇒ **"Build a path from a string."** (the matched no-arg overload is undocumented and the implementation is undocumented, so the next candidate — the sibling `str` overload on the **same class** — supplies the text, before any inheritance is considered).

### 14. Undocumented override inherits the base

```python
class Widget:
    def __init__(self, name: str) -> None:
        """Create a widget."""

class Button(Widget):
    def __init__(self, name: str) -> None:   # override, no docstring
        super().__init__(name)
```

Hovering `Button("ok")` ⇒ **"Create a widget."** (inherited through the undocumented override; Rule C).

### 15. Documented override shadows the base

```python
class Widget:
    def __init__(self, name: str) -> None:
        """Create a widget."""

class Toggle(Widget):
    def __init__(self, name: str) -> None:
        """Create a toggle."""
```

Hovering `Toggle("x")` ⇒ **"Create a toggle."** (the base is never consulted).

### 16. Method inheritance across the hierarchy

```python
class Base:
    def save(self) -> None:
        """Persist to storage."""

class Mid(Base): ...
class Leaf(Mid):
    def save(self) -> None:      # override, no docstring
        ...
```

Hovering `Leaf().save()` ⇒ **"Persist to storage."** (walks `Leaf → Mid → Base`).

### 17. Multiple inheritance / diamond

```python
class A:
    def __init__(self) -> None:
        """A init."""
class B(A):
    def __init__(self) -> None:
        """B init."""
class C(A):
    def __init__(self) -> None:
        """C init."""
class D(B, C):        # MRO: D, B, C, A
    pass
```

Hovering `D()` ⇒ **"B init."** (`D` has no `__init__`; `B` precedes `C` and `A` in the MRO).

### 18. Class docstring vs an inherited constructor docstring

```python
class Base:
    def __init__(self, x: int) -> None:
        """Create with x."""

class Derived(Base):
    """A derived thing."""
    def __init__(self, x: int) -> None:   # override, no docstring
        super().__init__(x)
```

Hovering `Derived(1)` ⇒ **"Create with x."** — the inherited constructor docstring (Phase 1, full MRO) is preferred over `Derived`'s class docstring (Phase 2). See [Rule E](#rule-e--constructor-methods-vs-class-docstring) and [Open Policy Decision](#open-policy-decision).

### 19. Alternate constructor (`@classmethod`) is independent

```python
class Image:
    def __init__(self, pixels: bytes) -> None:
        """Create from raw pixels."""
    @classmethod
    def open(cls, path: str) -> "Image":
        """Load an image from a file."""
```

- Hovering `Image(b"...")` ⇒ **"Create from raw pixels."**
- Hovering `Image.open("a.png")` ⇒ **"Load an image from a file."**

The two are resolved separately; a classmethod is never merged into `Image(...)` resolution.

### 20. Callable instance (`__call__`)

```python
class Adder:
    def __call__(self, x: int) -> int:
        """Add the configured offset to x."""
        ...

add = Adder()
```

Hovering the call `add(1)` ⇒ **"Add the configured offset to x."** (resolved via `type(add).__call__`, using the method rules — not constructor resolution).

### 21. Stub overrides source, then falls back to source

```python
# shapes.pyi  (stub)
class Polygon:
    def __init__(self, sides: int) -> None: ...   # no docstring in stub

# shapes.py  (source)
class Polygon:
    def __init__(self, sides: int) -> None:
        """Create a polygon with the given number of sides."""
```

Hovering `Polygon(6)` ⇒ **"Create a polygon with the given number of sides."** (the stub declaration has no docstring, so Rule F resolves to the `.py` source).

### 22. Synthesized constructor falls through to the class docstring

```python
@dataclass
class Point:
    """A point in the plane."""
    x: int
    y: int
```

Hovering `Point(1, 2)` ⇒ **"A point in the plane."** (the generated `__init__` carries no docstring, so Phase 2 supplies the class docstring).

### 23. Capstone — deep hierarchy, mixed overloads, override, and a stub

```python
# geo.pyi  (stub)
class Shape:
    def __init__(self) -> None: ...          # no docstring in the stub

# geo.py  (source)
class Shape:
    def __init__(self) -> None:
        """Base shape."""                     # docstring only in source

class Sized:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, size: float) -> None:
        """A sized object."""
    def __init__(self, size: float = 0) -> None: ...

class Rect(Shape, Sized):                      # MRO: Rect, Shape, Sized, object
    def __init__(self, w: float, h: float) -> None:   # override, no docstring
        super().__init__()
```

Hovering `Rect(3, 4)`:

| Order                      | Candidate                   | Result              |
| -------------------------- | --------------------------- | ------------------- |
| Phase 1 · `Rect.__init__`  | matched (single def)        | empty               |
| Phase 1 · `Shape.__init__` | stub decl → source (Rule F) | **"Base shape."** ⇒ |

Resolution stops at `Shape`; `Sized` and all class docstrings are never reached. This one example exercises MRO ordering, an undocumented override, and stub→source fallback together.

---

## Edge Cases and Special Constructs

| Case                                                           | Resolution                                                                                                                     |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Plain `def __init__` (no overloads)                            | Implementation docstring; MRO walk if empty.                                                                                   |
| Class defines neither `__init__` nor `__new__`                 | Search inherited constructor methods first; use the class docstring (Phase 2) only if none is documented.                      |
| Call matches zero overloads (type error)                       | Consider the full overload set, as for ordinary function/method symbol hover.                                                  |
| Derived adds new overloads; call matches an inherited overload | If the derived class has no implementation or other-overload documentation, the MRO walk continues to the base (Rule C).       |
| Stub-only class (no `.py`)                                     | Rule F has no source to fall back to; the stub's own docstrings are used.                                                      |
| `object.__init__` / `object.__new__` (and any builtin base)    | Builtin base classes are never inherited as constructor docstring sources; a builtin constructed directly still shows its own. |
| Synthesized constructors (dataclass, `NamedTuple`)             | No method docstring → fall through to the class docstring.                                                                     |
| Generic class, e.g. `Box[int]()`                               | Specialization does not change docstrings; resolve using the unparameterized class's candidates and MRO.                       |
| Decorated constructor/method                                   | Use the docstring the decorated callable exposes (e.g. one preserved by `functools.wraps`).                                    |
| Metaclass `__call__`                                           | Out of scope: constructor resolution considers only `__init__`/`__new__`.                                                      |
| `__init_subclass__`                                            | Not a per-instance constructor; not part of this resolution.                                                                   |
| Abstract base / `Protocol`                                     | Treated as ordinary classes; their `__init__`/`__new__` participate normally.                                                  |

---

## Open Policy Decision

One tier-ordering choice is deliberately called out because both answers are defensible. It is the single tunable knob:

**Should a derived class's class docstring outrank an _inherited_ base-class constructor docstring?**

- **Chosen (this spec): No.** Constructor-method docstrings across the whole MRO (Phase 1) are preferred over any class docstring (Phase 2). Rationale: a constructor is about constructing the object, so real constructor documentation — even inherited — is more useful than a generic class summary. See [Example 18](#18-class-docstring-vs-an-inherited-constructor-docstring).
- **Alternative:** interleave each class's docstring into its own Phase-1 step, so a class's own docstring is used before advancing to a base class. This makes a derived class docstring outrank a base constructor docstring — more "local," but hides inherited parameter documentation.

Only the placement of the class docstring moves; everything else is unaffected. To adopt the alternative, delete the standalone Phase 2 loop and fold the class docstring into the per-class step:

```
resolveConstructorDoc(C, call?):                # ALTERNATIVE
    for M in MRO(C) excluding builtin bases:    # derived -> base
        d = constructorMethodDoc(M, call)
        if d: return d
        d = docstringOf(classDeclOf(M))         # class docstring interleaved per class
        if d: return d
    return none
```

---

## Related Guides

- [Auto-Import Guide](auto-import-guide.md)
- [Type Narrowing](type-narrowing.md)

Last content update aligned with [Pylance 2026.4.1](https://github.com/microsoft/pylance-release/blob/8095001387e5aa5295b9f6070b97989693de9988/CHANGELOG.md#202641-23-september-2026-release).

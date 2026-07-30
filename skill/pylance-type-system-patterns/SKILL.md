---
name: pylance-type-system-patterns
description: Write and fix Python typing so Pylance/Pyright infers and accepts it — type narrowing (isinstance, is None, TypeGuard/TypeIs, discriminated unions), generics/TypeVar, Protocol, TypedDict, Literal, overloads, and method overrides. Use when authoring annotations or resolving reportInvalidTypeVarUse, reportInvalidTypeArguments, reportMissingTypeArgument, reportInconsistentOverload, reportIncompatibleMethodOverride, reportTypedDictNotRequiredAccess. Triggers on "type narrowing", "TypeGuard", "Protocol", "TypedDict", "overload", "generic", "TypeVar", "discriminated union".
---

# Python type-system patterns

Authoring typing that Pylance/Pyright infers and accepts. For per-rule meaning, see `pylance-diagnostics-triage`.

## Type narrowing

The full pattern table (isinstance, `is None`, truthiness, `type()`, `in`/`len`, discriminated unions, `TypeGuard` vs `TypeIs`, narrowing in closures): [../../docs/howto/type-narrowing.md](../../docs/howto/type-narrowing.md).

Quick patterns:

```python
def f(x: int | None) -> int:
    if x is None:
        raise ValueError
    return x + 1          # narrowed to int here

# TypeGuard
from typing import TypeGuard
def is_str_list(v: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(i, str) for i in v)
```

## Generics, Protocol, TypedDict, Literal

The in-repo docs have **no dedicated guide** for generics/Protocol — coverage is spread across diagnostic pages. This skill fills that gap with a distilled mini-guide: read [references/generics-and-protocols.md](references/generics-and-protocols.md) first, then drill into the linked diagnostics.

## Overloads

Author overloads so signatures are compatible (not overlapping):

- [reportInconsistentOverload](../../docs/diagnostics/reportInconsistentOverload.md) — overload signatures incompatible with each other.
- [reportOverlappingOverload](../../docs/diagnostics/reportOverlappingOverload.md) — an overload is shadowed by another.

```python
from typing import overload

@overload
def g(x: int) -> int: ...
@overload
def g(x: str) -> str: ...
def g(x: int | str) -> int | str: ...
```

## Method/variable overrides

Subclass overrides must keep the parent's contract:

- [reportIncompatibleMethodOverride](../../docs/diagnostics/reportIncompatibleMethodOverride.md)
- [reportIncompatibleVariableOverride](../../docs/diagnostics/reportIncompatibleVariableOverride.md)
- [reportImplicitOverride](../../docs/diagnostics/reportImplicitOverride.md)

Docstring resolution across overloads / `__init__` / MRO / stub-vs-source: [../../docs/howto/docstring-resolution-order.md](../../docs/howto/docstring-resolution-order.md).

## Type-form and TypedDict access

- [reportInvalidTypeForm](../../docs/diagnostics/reportInvalidTypeForm.md) — a type expression that isn't valid.
- [reportTypedDictNotRequiredAccess](../../docs/diagnostics/reportTypedDictNotRequiredAccess.md) — accessing a `NotRequired`/`Required` key incorrectly.
- [reportInvalidTypeVarUse](../../docs/diagnostics/reportInvalidTypeVarUse.md) / [reportInvalidTypeArguments](../../docs/diagnostics/reportInvalidTypeArguments.md) / [reportMissingTypeArgument](../../docs/diagnostics/reportMissingTypeArgument.md) — generic-usage errors.

## Typing-alias & promotion settings

- [deprecateTypingAliases](../../docs/settings/python_analysis_typeEvaluation_deprecateTypingAliases.md) — flag deprecated `typing` aliases (e.g. `List` → `list`).
- [disableBytesTypePromotions](../../docs/settings/python_analysis_typeEvaluation_disableBytesTypePromotions.md)
- [enableExperimentalFeatures](../../docs/settings/python_analysis_typeEvaluation_enableExperimentalFeatures.md)

## Related skills

- **pylance-diagnostics-triage** — per-rule meaning and suppression.
- **pylance-strict-migration** — clearing the `reportUnknown*` family by adding annotations.

---
name: pylance-type-checking
description: Write Python code that passes Pylance/Pyright type checking — add type annotations, fix report* diagnostics in the source (optional/None, unknown types, missing annotations, generics, return/argument/assignment mismatches), apply type narrowing (isinstance, is None, TypeGuard/TypeIs), use TYPE_CHECKING imports and type stubs, and suppress with # pyright: ignore. Use when writing or reviewing Python type annotations, narrowing union/optional types, resolving Pylance/Pyright type errors, or choosing what level of type checking to write toward.
---

# Pylance Type Checking

This skill helps you **write Python code that satisfies Pylance/Pyright's type-checking rules.** It is about the Python source you produce — annotations, type narrowing, fixing `report*` errors in the code, and inline suppression — not about configuring the editor or CI.

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is the VS Code Python language server; [Pyright](https://github.com/microsoft/pyright) is its underlying static type checker. Both report the same `report*` diagnostics described here. The rules they enforce are the same rules mypy and other PEP 484 checkers respect, so code written to pass them is portable.

## Quick Reference

- **What each checking level catches** (`off`/`basic`/`standard`/`strict`) and what to write toward → [type-checking-levels.md](references/type-checking-levels.md)
- **Fix a `report*` type error in the code** → [fixing-type-errors.md](references/fixing-type-errors.md)
- **Narrow a union/optional** (`is None`, `isinstance`, `TypeGuard`/`TypeIs`) → [type-narrowing.md](references/type-narrowing.md)
- **Typed imports & type stubs** (`TYPE_CHECKING`, `types-*`, `py.typed`) → [typed-imports-and-stubs.md](references/typed-imports-and-stubs.md)
- **Look up a specific `report*` rule** → [diagnostics-reference.md](references/diagnostics-reference.md)

## Decision Flow

When writing or fixing typed Python:

1. **Know which level you're writing toward** (`off` → `basic` → `standard` → `strict`). Stricter levels demand more annotations and fewer `Any`s. See [type-checking-levels.md](references/type-checking-levels.md).
2. **Annotate everything the level requires**: all function parameters and returns, generic type arguments, instance attributes in `__init__`. Avoid bare `Any`.
3. **Fix errors by fixing the code** — narrow optionals, correct return/argument/assignment types, align override signatures, remove dead code — before suppressing. See [fixing-type-errors.md](references/fixing-type-errors.md).
4. **Suppress last-resort, inline and scoped**: `# pyright: ignore[ruleName]` on the line, or `cast(T, v)` when you know more than the checker. Use per-file `# pyright: strict` / `# pyright: reportX=false` comments to tighten or relax one file.
5. **Debug with `reveal_type(x)`** to see exactly what Pylance infers at a point.

## Write-To Conventions

- **Annotate parameters and returns** on every function/method — `reportMissingParameterType` and `reportUnknownParameterType` (strict) require it.
- **Supply generic arguments** — `list[int]`, not `list`; `dict[str, int]`, not `dict`. `reportMissingTypeArgument` (strict) flags bare generics.
- **Narrow optionals before use** — `if x is None: ...` then use `x`. Never call `.upper()` on `str | None`. See [type-narrowing.md](references/type-narrowing.md).
- **Declare instance attributes in `__init__`** — `reportAttributeAccessIssue` (basic) flags attributes not initialized there.
- **Align override signatures** with the parent — `reportIncompatibleMethodOverride` (standard). Add `@override` for clarity.
- **Prefer `X | None` narrowing** over `Optional[X]` boilerplate; both are fine, but narrowing is what removes the `None` variant.
- **Suppress scoped, not broad**: `# pyright: ignore[reportUnknownVariableType]` over bare `# type: ignore` — the scoped form only hides what you intend and lets `reportUnnecessaryTypeIgnoreComment` flag it later for cleanup.

> This skill does not cover editor/CI configuration (`.vscode/settings.json`, `pyrightconfig.json`, `languageServerMode`, GitHub Actions, etc.). For that, see the official [Pylance settings docs](https://github.com/microsoft/pylance-release/tree/main/docs/settings) and [how-to guides](https://github.com/microsoft/pylance-release/tree/main/docs/howto).

## Links to Source Documentation

This skill distills the official Pylance documentation. For full detail, see:

- Pylance docs index: https://github.com/microsoft/pylance-release/blob/main/docs/INDEX.md
- `typeCheckingMode` reference (what rules each level enables): https://github.com/microsoft/pylance-release/blob/main/docs/settings/python_analysis_typeCheckingMode.md
- Per-diagnostic rule pages: https://github.com/microsoft/pylance-release/blob/main/docs/diagnostics/
- Pyright diagnostic defaults table: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#diagnostic-settings-defaults
- Type narrowing how-to: https://github.com/microsoft/pylance-release/blob/main/docs/howto/type-narrowing.md

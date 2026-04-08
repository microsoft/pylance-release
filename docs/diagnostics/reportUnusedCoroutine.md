## Overview

`reportUnusedCoroutine` is a Pylance and Pyright diagnostic that warns when a coroutine is defined but never awaited or used. This helps catch bugs where asynchronous code is silently ignored, which can lead to unexpected behavior.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
- [#9579](https://github.com/microsoft/pyright/issues/9579): Always ensure that coroutine calls are either awaited or explicitly checked for truthiness to avoid bugs where the coroutine is silently ignored.

## Examples

**Error:**

```python
import asyncio

async def fetch_data() -> str:
    return "data"

async def main():
    fetch_data()  # Coroutine created but never awaited
```

**Fix — await the coroutine:**

```python
import asyncio

async def fetch_data() -> str:
    return "data"

async def main():
    result = await fetch_data()  # Now the coroutine runs
```

## Common Fixes & Workarounds

1. Always use `await` when calling coroutines if you need their result.
2. If you intentionally do not await a coroutine, document this with a comment for clarity.
3. Review your code for places where asynchronous functions are called but not awaited.
4. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedCoroutine) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

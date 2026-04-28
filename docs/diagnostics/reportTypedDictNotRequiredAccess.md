## Overview

`reportTypedDictNotRequiredAccess` flags cases where you access a non-required (optional) field of a `TypedDict` without first checking if it is present. This diagnostic helps prevent runtime errors and ensures safe access to optional fields in typed dictionaries.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode.
- [#1693](https://github.com/microsoft/pyright/issues/1693): Use type inheritance in TypedDict to clearly define required and not required fields.
- [#4173](https://github.com/microsoft/pyright/issues/4173): Implement per-module configuration settings in Pyright for more flexible type checking.

## Examples

**Error:**

```python
from typing import TypedDict, NotRequired

class UserProfile(TypedDict):
    name: str
    nickname: NotRequired[str]

def greet(profile: UserProfile) -> str:
    return f"Hi, {profile['nickname']}"  # 'nickname' may not exist
```

**Fix — check for the key first:**

```python
def greet(profile: UserProfile) -> str:
    nick = profile.get("nickname", profile["name"])
    return f"Hi, {nick}"
```

Or use `in` to guard access:

```python
def greet(profile: UserProfile) -> str:
    if "nickname" in profile:
        return f"Hi, {profile['nickname']}"
    return f"Hi, {profile['name']}"
```

## Common Fixes & Workarounds

1. Check for the presence of a non-required field in a `TypedDict` before accessing it (e.g., using `if "field" in my_dict:`).
2. Use type inheritance to clearly define required and not required fields in your `TypedDict` definitions.
3. Use per-module configuration settings to adjust diagnostics as needed.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportTypedDictNotRequiredAccess) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

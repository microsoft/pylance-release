## Overview

`reportInvalidStringEscapeSequence` is a Pylance diagnostic that warns when your Python code contains a string with an invalid escape sequence. This helps catch typos or mistakes in string literals that could lead to unexpected behavior or runtime errors.

## Representative Issues

- [#1762](https://github.com/microsoft/pylance-release/issues/1762): Ensure that configuration settings in `settings.json` are correctly applied and not overridden by other configurations.
- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
- [#715](https://github.com/microsoft/pylance-release/issues/715): When using generic types like dictionaries in Python, prefer the `typing.Dict` syntax over the older `dict[t, t]` syntax to ensure compatibility across different Python versions.

## Examples

```python
path = "C:\new_folder\test"  # Warning: Unsupported escape character "\n" and "\t"
                             #   (\n is treated as newline, \t as tab)

pattern = "\d+\.\d+"  # Warning: Unsupported escape character "\d"
```

**Fix — use raw strings for regex patterns and file paths:**

```python
path = r"C:\new_folder\test"  # OK: raw string, backslashes are literal

pattern = r"\d+\.\d+"  # OK: raw string
```

**Fix — use double backslashes:**

```python
path = "C:\\new_folder\\test"  # OK: escaped backslashes
```

## Common Fixes & Workarounds

1. Double-check your string literals for typos in escape sequences (e.g., use `\n` for newline, `\t` for tab).
2. Use raw strings (prefix with `r`) if you want backslashes to be treated literally (e.g., `r"C:\path\to\file"`).
3. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportInvalidStringEscapeSequence) to adjust the severity or disable this diagnostic if needed.
4. Update your code to use valid escape sequences or raw strings as appropriate.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

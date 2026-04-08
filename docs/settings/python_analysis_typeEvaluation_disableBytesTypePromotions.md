# Understanding `python.analysis.typeEvaluation.disableBytesTypePromotions` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.disableBytesTypePromotions` setting controls whether Pylance applies the legacy type promotion that treats `bytearray` and `memoryview` as subtypes of `bytes`.

## What `python.analysis.typeEvaluation.disableBytesTypePromotions` does

Historically, Python type checkers allowed `bytearray` and `memoryview` to be used wherever `bytes` was expected, even though they are distinct types with no inheritance relationship. [PEP 688](https://peps.python.org/pep-0688/#no-special-meaning-for-bytes) deprecates this behavior.

When this setting is `true`, Pylance disables the legacy promotion and treats `bytes`, `bytearray`, and `memoryview` as distinct, incompatible types. When `false`, the legacy promotion remains active.

The default value is `false`.

```json
"python.analysis.typeEvaluation.disableBytesTypePromotions": false
```

### Example

```python
def write_data(data: bytes) -> None:
    ...

buf = bytearray(b"hello")
write_data(buf)
```

- With `false` (default): No error — `bytearray` is promoted to `bytes`.
- With `true`: Pylance reports an error because `bytearray` is not assignable to `bytes`.

## Accepted values

- `true`: Disable bytes type promotions. `bytes`, `bytearray`, and `memoryview` are treated as distinct types.
- `false` (default): Enable legacy promotions. `bytearray` and `memoryview` are accepted where `bytes` is expected.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.disableBytesTypePromotions`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.disableBytesTypePromotions": true
    ```

## When to enable this setting

### Enforcing strict type checking

If your project requires precise type distinctions between `bytes`, `bytearray`, and `memoryview`, enable this setting to catch places where the wrong type is passed.

### Aligning with PEP 688

[PEP 688](https://peps.python.org/pep-0688/) deprecates the implicit promotion. Enabling this setting brings your type checking in line with the updated standard.

### Keeping the default

If your codebase passes `bytearray` or `memoryview` to functions annotated with `bytes` and you are not ready to update those call sites, leave this at `false`.

## Resolving type errors after enabling

When you enable this setting, you may see new errors. Common fixes:

1. **Convert explicitly**: `write_data(bytes(buf))`
2. **Broaden the annotation**: `def write_data(data: bytes | bytearray) -> None:`
3. **Use a protocol**: Accept `collections.abc.Buffer` (Python 3.12+) or `typing.Union[bytes, bytearray, memoryview]`.

## Related settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.
- [`python.analysis.diagnosticSeverityOverrides`](python_analysis_diagnosticSeverityOverrides.md)
    - Fine-grained control over individual diagnostic rule severities.

## Frequently asked questions

### Q: Will disabling promotions affect other types?

**A:** No. This setting specifically controls the `bytes`/`bytearray`/`memoryview` promotion. Other types are unaffected.

### Q: Does this affect runtime behavior?

**A:** No. This is a static analysis setting only. Your code runs the same regardless of this setting.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

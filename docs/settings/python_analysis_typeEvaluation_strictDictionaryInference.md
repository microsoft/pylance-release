# Understanding `python.analysis.typeEvaluation.strictDictionaryInference` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.strictDictionaryInference` setting controls how Pylance infers the types of dictionary keys and values when no explicit type annotation is provided.

## What `python.analysis.typeEvaluation.strictDictionaryInference` does

When inferring the type of a dictionary literal, Pylance must decide how to combine the types of its keys and values. With this setting disabled, Pylance may use a broader type like `dict[str, Any]`. With it enabled, Pylance uses a stricter union of the observed types.

The default value is `false`.

```json
"python.analysis.typeEvaluation.strictDictionaryInference": false
```

### Example

```python
my_dict = {"a": 1, "b": "hello"}
```

- With `false` (default): Pylance infers `dict[str, Any]` or a broad common type.
- With `true`: Pylance infers `dict[str, int | str]`, using the union of observed value types.

## Accepted values

- `true`: Use strict type assumptions when inferring dictionary types. Keys and values are inferred as the union of their observed types.
- `false` (default): Use broader type assumptions for dictionary inference.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.strictDictionaryInference`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.strictDictionaryInference": true
    ```

You can also enable it per file:

```python
# pyright: strictDictionaryInference=true
```

## When to enable this setting

### Catching mixed-type errors

If your dictionaries are expected to have uniform value types, enabling strict inference helps catch accidental type mixing.

### Precise type checking

With strict inference, Pylance produces narrower types that are more likely to trigger errors when the dictionary is passed to functions with specific type expectations.

### Keeping the default

If your code intentionally uses dictionaries with mixed value types and you prefer fewer diagnostics, leave this at `false`.

## Interaction with explicit type annotations

If you provide an explicit type annotation for a dictionary, Pylance uses that annotation regardless of this setting:

```python
my_dict: dict[str, int | str] = {"a": 1, "b": "hello"}  # annotation takes precedence
```

Strict dictionary inference primarily affects unannotated dictionary literals.

## Related settings

- [`python.analysis.typeEvaluation.strictListInference`](python_analysis_typeEvaluation_strictListInference.md)
    - Same concept applied to list literals.
- [`python.analysis.typeEvaluation.strictSetInference`](python_analysis_typeEvaluation_strictSetInference.md)
    - Same concept applied to set literals.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.

## Frequently asked questions

### Q: Will enabling this setting break existing code?

**A:** It does not change runtime behavior. It may introduce new diagnostics where Pylance previously inferred broader types. You may need to add explicit annotations or adjust call sites.

### Q: How does this interact with `typeCheckingMode`?

**A:** The `typeCheckingMode` setting controls which diagnostic rules are enabled. `strictDictionaryInference` specifically controls how dictionary types are inferred. They are independent but complementary — stricter inference can surface more issues when diagnostic rules are also strict.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

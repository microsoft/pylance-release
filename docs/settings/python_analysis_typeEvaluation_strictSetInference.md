# Understanding `python.analysis.typeEvaluation.strictSetInference` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.strictSetInference` setting controls how Pylance infers the element type of set literals when no explicit type annotation is provided.

## What `python.analysis.typeEvaluation.strictSetInference` does

When inferring the type of a set literal, Pylance must decide how to combine the types of its elements. With this setting disabled, Pylance may use a broader type like `set[Any]`. With it enabled, Pylance infers the element type as the union of the observed types.

The default value is `false`.

```json
"python.analysis.typeEvaluation.strictSetInference": false
```

### Example

```python
my_set = {1, "a", 3.4}
```

- With `false` (default): Pylance may infer `set[Any]` or find a common supertype.
- With `true`: Pylance infers `set[int | str | float]`, using the union of observed element types.

## Accepted values

- `true`: Use strict type assumptions when inferring set types. Elements are inferred as a union of their observed types.
- `false` (default): Use broader type assumptions for set inference.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.strictSetInference`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.strictSetInference": true
    ```

You can also enable it per file:

```python
# pyright: strictSetInference=true
```

## When to enable this setting

### Catching unexpected element types

With strict inference, adding an element of an unexpected type to a set produces a diagnostic:

```python
numbers = {1, 2, 3}  # inferred as set[int] with strict inference

numbers.add(4)      # OK
numbers.add(5.5)    # error — float is not assignable to int
```

### Consistent behavior with lists and dictionaries

If you already use `strictListInference` or `strictDictionaryInference`, enabling `strictSetInference` brings set inference in line with the same stricter behavior.

### Keeping the default

If your code uses sets with mixed element types and you prefer fewer diagnostics, leave this at `false`.

## Interaction with explicit type annotations

If you provide an explicit type annotation, Pylance uses that annotation regardless of this setting:

```python
my_set: set[int | str] = {1, "hello"}  # annotation takes precedence
```

Strict set inference primarily affects unannotated set literals.

## Related settings

- [`python.analysis.typeEvaluation.strictListInference`](python_analysis_typeEvaluation_strictListInference.md)
    - Same concept applied to list literals.
- [`python.analysis.typeEvaluation.strictDictionaryInference`](python_analysis_typeEvaluation_strictDictionaryInference.md)
    - Same concept applied to dictionary literals.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.

## Frequently asked questions

### Q: How does strict set inference interact with explicit type annotations?

**A:** If you explicitly annotate the set's type, Pylance uses that annotation. `strictSetInference` only affects unannotated set literals.

### Q: Will enabling this setting break existing code?

**A:** It does not change runtime behavior. It may introduce new diagnostics where Pylance previously inferred broader types.

### Q: Can I enable this for specific files only?

**A:** Yes. Add `# pyright: strictSetInference=true` at the top of the file.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

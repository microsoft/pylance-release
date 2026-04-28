# Understanding `python.analysis.typeEvaluation.strictListInference` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.strictListInference` setting controls how Pylance infers the element type of list literals when no explicit type annotation is provided.

## What `python.analysis.typeEvaluation.strictListInference` does

When inferring the type of a list literal, Pylance must decide how to combine the types of its elements. With this setting disabled, Pylance may find a common supertype or use a broader type like `list[Any]`. With it enabled, Pylance infers the element type as the union of the observed types.

The default value is `false`.

```json
"python.analysis.typeEvaluation.strictListInference": false
```

### Example

```python
my_list = [1, "a", 3.4]
```

- With `false` (default): Pylance may infer `list[Any]` or find a common supertype.
- With `true`: Pylance infers `list[int | str | float]`, using the union of observed element types.

## Accepted values

- `true`: Use strict type assumptions when inferring list types. Elements are inferred as a union of their observed types.
- `false` (default): Use broader type assumptions for list inference.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.strictListInference`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.strictListInference": true
    ```

You can also enable it per file:

```python
# pyright: strictListInference=true
```

## When to enable this setting

### Catching type mismatches at call sites

With strict inference, passing a mixed-type list to a function expecting a specific element type produces a diagnostic:

```python
def process(numbers: list[int]) -> None:
    ...

my_list = [1, 2.0]

# With strict inference: error — list[int | float] is not assignable to list[int]
# Without strict inference: may not produce an error
process(my_list)
```

### Heterogeneous lists

If your code works with lists containing elements of different types, strict inference gives Pylance the precise union type, improving downstream type checking accuracy.

### Keeping the default

If you prefer fewer diagnostics or your codebase relies on Pylance finding common supertypes for list elements, leave this at `false`.

## Interaction with explicit type annotations

If you provide an explicit type annotation, Pylance uses that annotation regardless of this setting:

```python
my_list: list[int | str] = [1, "hello"]  # annotation takes precedence
```

Strict list inference primarily affects unannotated list literals.

## Related settings

- [`python.analysis.typeEvaluation.strictDictionaryInference`](python_analysis_typeEvaluation_strictDictionaryInference.md)
    - Same concept applied to dictionary literals.
- [`python.analysis.typeEvaluation.strictSetInference`](python_analysis_typeEvaluation_strictSetInference.md)
    - Same concept applied to set literals.
- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.

## Frequently asked questions

### Q: Why am I getting type errors after enabling strict list inference?

**A:** Strict inference produces narrower types. If a list contains `[1, 2.0]`, Pylance infers `list[int | float]` instead of a broader type. This may not be assignable to `list[int]`, producing a new diagnostic.

### Q: Can I enable this for specific files only?

**A:** Yes. Add `# pyright: strictListInference=true` at the top of the file.

### Q: How does this relate to `strict` type checking mode?

**A:** `typeCheckingMode: "strict"` enables stricter diagnostic rules overall. `strictListInference` specifically changes how list types are inferred. They are independent settings that can be used separately or together.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

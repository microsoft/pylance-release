# Understanding `python.analysis.importFormat` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and code actions that help keep imports consistent across a codebase.

The `python.analysis.importFormat` setting controls how Pylance formats new import statements.

## What `python.analysis.importFormat` does

`python.analysis.importFormat` tells Pylance whether it should prefer absolute or relative imports when it creates new import statements.

Accepted values:

- `absolute` (default)
    - Use absolute import format when creating new import statements.
- `relative`
    - Use relative import format when creating new import statements.

Example:

```json
"python.analysis.importFormat": "relative"
```

## Absolute and relative imports

With `absolute`, Pylance prefers imports such as:

```python
from mypackage.subpackage.module import MyClass
```

With `relative`, Pylance prefers imports such as:

```python
from .module import MyClass
from ..subpackage.module import MyClass
```

## Where this setting is used

Pylance uses `python.analysis.importFormat` when it creates or rewrites imports through features such as:

- auto-import suggestions
- import-adding code actions
- the `source.convertImportFormat` whole-file code action
- `source.fixAll.pylance` when [`python.analysis.fixAll`](python_analysis_fixAll.md) includes `source.convertImportFormat`

## Use with the Convert Import Format code action

Pylance exposes a whole-file source action named `source.convertImportFormat`.

That code action rewrites imports in the current file to match `python.analysis.importFormat`.

For example, if you set:

```json
"python.analysis.importFormat": "relative"
```

then running **Convert Import Format** rewrites eligible imports in the file toward relative form.

If you set:

```json
"python.analysis.importFormat": "absolute"
```

the same code action rewrites eligible imports toward absolute form.

## Use with Pylance Fix All

If you want Pylance Fix All to convert imports automatically, include `source.convertImportFormat` in [`python.analysis.fixAll`](python_analysis_fixAll.md):

```json
{
    "python.analysis.importFormat": "relative",
    "python.analysis.fixAll": ["source.convertImportFormat"]
}
```

When you then run `source.fixAll.pylance`, Pylance applies import-format conversion using the format selected in `python.analysis.importFormat`.

## Use on save in VS Code

If you want this behavior to run on save through Pylance Fix All, combine `python.analysis.fixAll` with `editor.codeActionsOnSave`:

```json
{
    "python.analysis.importFormat": "relative",
    "python.analysis.fixAll": ["source.convertImportFormat"],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll.pylance": "explicit"
        }
    }
}
```

With that configuration, saving a Python file runs Pylance Fix All, and the import-format conversion uses the format selected by `python.analysis.importFormat`.

## Important behavior with `relative`

Setting `python.analysis.importFormat` to `relative` does not mean every import becomes relative.

Pylance only generates relative imports for non-library imports where a relative module path can be formed from the current file. Standard library and third-party imports remain absolute.

This matters in layouts such as:

- multiple top-level packages in one workspace
- separate `tests` folders
- workspaces where some imports cross package boundaries

In those cases, some imports may still stay absolute, and that is expected.

## Choosing between `absolute` and `relative`

Use `absolute` when:

- your project style prefers fully qualified imports
- your workspace contains multiple top-level packages
- relative imports often cross boundaries that should stay absolute

Use `relative` when:

- your project prefers package-local relative imports
- most imports stay within the same package tree
- you want auto-imports and import-conversion actions to follow that style where possible

## Frequently asked questions

### Why are some imports still absolute when `python.analysis.importFormat` is set to `relative`?

Because Pylance does not convert library imports to relative form, and some user-code imports do not have a valid relative path from the current file.

### Why did Convert Import Format not rewrite an import the way I expected?

In multi-package or test-folder layouts, the import that looks "local" in the workspace may still need to remain absolute to match package boundaries.

### Does this setting change existing imports by itself?

No. It affects how Pylance formats new imports and how import-conversion actions behave. Existing imports change only when you apply a code action such as `source.convertImportFormat` or run Pylance Fix All with `source.convertImportFormat` enabled.

### Does this setting affect third-party and standard library imports?

It affects the formatting choice for new imports, but standard library and third-party imports remain absolute rather than being rewritten as relative imports.

## Related Settings

- [`python.analysis.fixAll`](python_analysis_fixAll.md): Configure Fix All to include `source.convertImportFormat` for automatic format conversion on save.
- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md): Controls whether auto-import suggestions appear in completions.

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.

# Understanding `python.analysis.fixAll` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, refactorings, and code actions that help keep Python codebases consistent.

One of those code actions is Pylance Fix All. The `python.analysis.fixAll` setting controls which Pylance fixes are included when you run that action.

## What `python.analysis.fixAll` does

`python.analysis.fixAll` is an array of fix commands. When Pylance runs its Fix All code action, it applies only the commands listed in this setting.

The default value is an empty array:

```json
"python.analysis.fixAll": []
```

That means `source.fixAll.pylance` does not apply any changes until you explicitly opt in to one or more fix commands.

## Accepted values

`python.analysis.fixAll` currently supports these values:

- `source.unusedImports`
    - Remove unused imports.
- `source.convertImportFormat`
    - Convert import format according to the [`python.analysis.importFormat`](python_analysis_importFormat.md) setting.
- `source.convertImportStar`
    - Convert wildcard imports such as `from module import *` into explicit imports.
- `source.addTypeAnnotation`
    - Add type annotations to variables and functions when Pylance can infer them.

## How to configure the setting

You can configure `python.analysis.fixAll` in your workspace or user `settings.json`.

### Example: remove unused imports only

```json
"python.analysis.fixAll": [
    "source.unusedImports"
]
```

### Example: combine multiple Pylance fixes

```json
"python.analysis.fixAll": [
    "source.unusedImports",
    "source.convertImportFormat",
    "source.convertImportStar",
    "source.addTypeAnnotation"
]
```

Use a smaller list if you want a more conservative Fix All workflow.

## Use with VS Code Fix All

After you configure `python.analysis.fixAll`, you can use VS Code's Fix All workflow for the current file.

Pylance uses the configured list when VS Code runs Fix All or requests fix-all source actions. In practice, that means the Pylance fixes you opted into are the ones available through the `source.fixAll.pylance` code action.

For example, if you configure:

```json
"python.analysis.fixAll": [
  "source.unusedImports",
  "source.convertImportStar"
]
```

then Pylance Fix All applies only those two fixes.

## Use on save in VS Code

You can also run Pylance Fix All automatically through VS Code's save actions.

Add `source.fixAll.pylance` to `editor.codeActionsOnSave` in your `settings.json`:

```json
{
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll.pylance": "explicit"
        }
    }
}
```

This tells VS Code to run the Pylance fix-all source action on save for Python files, using whatever commands you configured in `python.analysis.fixAll`.

For example:

```json
{
    "python.analysis.fixAll": ["source.unusedImports", "source.convertImportFormat"],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll.pylance": "explicit"
        }
    }
}
```

With that configuration, saving a Python file runs Pylance Fix All and applies only unused-import removal and import-format conversion.

## Related settings

- [`python.analysis.importFormat`](python_analysis_importFormat.md)
    - Used by `source.convertImportFormat` to decide whether imports should be written in absolute or relative form.

## Frequently asked questions

### Why does Pylance Fix All do nothing?

If `python.analysis.fixAll` is left at its default empty array, `source.fixAll.pylance` has no configured fixes to apply.

### Does `python.analysis.fixAll` affect all fix providers in VS Code?

No. It controls the fixes applied by Pylance's `source.fixAll.pylance` code action.

### Can I enable only one kind of fix?

Yes. Add only the commands you want to the array. For example, if you want Fix All to remove unused imports but nothing else, configure only `source.unusedImports`.

---

For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.

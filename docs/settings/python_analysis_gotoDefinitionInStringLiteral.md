# Understanding `python.analysis.gotoDefinitionInStringLiteral` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast and feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker.

The `python.analysis.gotoDefinitionInStringLiteral` setting controls whether **Go to Definition** works on string literals that look like module names.

## What is `python.analysis.gotoDefinitionInStringLiteral`?

Module names sometimes appear inside string literals rather than in `import` statements — for example in dynamic imports, plugin registries, or framework configuration that references modules by name. When this setting is enabled, invoking **Go to Definition** (F12) on such a string navigates to the referenced module.

This exists because many Python frameworks identify modules and objects with strings, and being able to jump from those strings to the underlying module improves navigation in configuration-heavy codebases.

**Type**: `boolean`
**Default**: `true`
**Scope**: resource (can be set per workspace or folder)

## Example

Frameworks such as Django reference modules and objects by name inside strings. For example, in a URL configuration:

```python
from django.urls import include, path

urlpatterns = [
    path("blog/", include("blog.urls")),
    #                      ^ invoke Go to Definition (F12) here
]
```

With the setting **enabled** (the default), invoking **Go to Definition** on the `"blog.urls"` string navigates to that module (for example `blog/urls.py`). It also resolves a string that names a member of a module — for example **Go to Definition** on `"myapp.Reporter"` in a Django `ForeignKey` jumps to the `Reporter` class. The same works for dynamic imports such as `importlib.import_module("my_package.utils")`.

With the setting **disabled**, **Go to Definition** does nothing on the string, because the text is treated as a plain literal rather than a module reference.

## How to Change `python.analysis.gotoDefinitionInStringLiteral`

### Using the Settings UI

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Preferences: Open Settings (UI)**.
2. Search for `python.analysis.gotoDefinitionInStringLiteral`.
3. Uncheck the box to disable it.

### Using `settings.json`

```json
{
    "python.analysis.gotoDefinitionInStringLiteral": false
}
```

## When to Use It

- **Keep enabled** (the default) if you work with frameworks that reference modules by name in strings and want to navigate to them quickly.
- **Disable** if you find that strings are being interpreted as module references when you do not intend them to be.

## Frequently Asked Questions

### Why does Go to Definition do nothing on my string?

The string must resolve to a module that Pylance can find in your environment, or to a member of such a module (for example `"package.module"` or `"package.module.ClassName"`). Arbitrary text that does not name an importable module is treated as a plain literal.

### Does it work on any string?

No. It only applies to string literals that look like module names (and members of those modules). It does not turn every string into a navigable link.

### Is it enabled by default?

Yes. The default is `true`.

## Related Settings

- [`python.analysis.autoImportCompletions`](python_analysis_autoImportCompletions.md) — offers completions for symbols that are not yet imported.
- [`python.analysis.indexing`](python_analysis_indexing.md) — builds the symbol index that powers navigation features.

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._

# Understanding `python.analysis.typeEvaluation.enableExperimentalFeatures` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and diagnostics to enhance your Python development experience.

The `python.analysis.typeEvaluation.enableExperimentalFeatures` setting enables a set of experimental features that correspond to proposed or exploratory changes to the Python typing standard.

## What `python.analysis.typeEvaluation.enableExperimentalFeatures` does

When enabled, Pylance activates experimental (mostly undocumented) type evaluation features. These correspond to proposed PEPs or exploratory typing features that are not yet part of the stable Python typing specification. They are likely to change or be removed.

The default value is `false`.

```json
"python.analysis.typeEvaluation.enableExperimentalFeatures": false
```

## Accepted values

- `true`: Enable experimental type evaluation features.
- `false` (default): Use only stable, fully supported type evaluation behavior.

## How to change the setting

To adjust this setting in Visual Studio Code:

- Open **Settings** and search for `python.analysis.typeEvaluation.enableExperimentalFeatures`.
- Check or uncheck the box.

Alternatively, edit your `settings.json` file directly:

- Open **Command Palette**, type `Preferences: Open Settings (JSON)`, and select it.
- Add or update the following line:

    ```json
    "python.analysis.typeEvaluation.enableExperimentalFeatures": true
    ```

## When to enable this setting

### Testing upcoming features

Enable this setting if you want to try proposed typing features before they are finalized. This can help you assess how upcoming changes might affect your codebase.

### Providing feedback

Enabling experimental features and reporting issues helps the Pylance and Pyright teams improve the features before they ship as stable.

### Keeping the default

For production projects where stability is important, leave this at `false`. Experimental features may produce unexpected diagnostics, change behavior between releases, or be removed entirely.

## Important considerations

- **Stability**: Experimental features may not be fully tested and can change or be removed in future releases.
- **No granular control**: This setting is a single toggle that enables all experimental features. You cannot enable or disable individual experimental features.

## Related settings

- [`python.analysis.typeCheckingMode`](python_analysis_typeCheckingMode.md)
    - Controls the baseline strictness of type-checking rules.

## Frequently asked questions

### Q: How can I find out what experimental features are currently available?

**A:** Experimental features are documented in the [Pyright changelog](https://github.com/microsoft/pyright/blob/main/packages/pyright-internal/src/common/CHANGELOG.md) and [configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#type-evaluation-settings) when they are introduced.

### Q: Will enabling experimental features affect Pylance's stability?

**A:** Potentially. Experimental features are intended for testing and may introduce unexpected behavior. They should not be relied upon for production workflows.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*

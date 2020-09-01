# Migrating from the Microsoft Python Language Server to Pylance

If you are a Microsoft Python Language Server user switching to the Pylance language server, there are a couple of changes that you should note.

## Updates to Settings and Configurations

When switching from the Microsoft Python Language Server to Pylance, there are a couple of settings that you'll notice have changed. Most changed settings are updated automatically when you install Pylance. However, `python.analysis.errors`, `python.analysis.warnings`, `python.analysis.information` or `python.analysis.disabled` cannot be ported over to be used in Pylance and so you'll need to revisit these settings using `python.analysis.diagnosticSeverityOverrides`.

## Configuring python.analysis.diagnosticSeverityOverrides

In Pylance, we've restructured the way you can override diagnostic severities via the `python.analysis.diagnosticSeverityOverrides` setting. We've taken the `python.analysis.errors/warnings/information/disabled` and created this new map-type setting to allow you to configure diagnostic severities using rules as the keys and the severity for diagnostics produced by that rule as the values. Pylance also has a new set of rules to produce diagnostics. Because of these new rules, we are unable to port your `python.analysis.errors/warnings/information/disabled` settings to Pylance.

If you wish to configure this setting, you'll want to edit it via your settings.json or via the settings editor in VS Code.

Supported rule keys and associated descriptions can be found in our diagnostic severity rules doc.

Supported severity values include:

-   `"error"`
-   `"warning"`
-   `"information"`
-   `"none"` (disabled)

Example structure for settings.json:

```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnboundVariable": "information",
        "reportImplicitStringConcatenation": "warning"
    }
}
```

## Automatically Ported Settings

There are two settings which we have ported over from your Microsoft Python Language Server settings to Pylance automatically. No additional action is required.

### python.autoComplete.extraPaths

This setting has been renamed in Pylance to python.analysis.extraPaths. If you install the new language server, Pylance will automatically copy the values you've set for extraPaths and use it to set the extraPaths setting in Pylance. The setting value's structure remains the same.

| Original setting/value                                    | New setting/value                                     |
| --------------------------------------------------------- | ----------------------------------------------------- |
| `python.autoComplete.extraPaths: [some, list, of, paths]` | `python.analysis.extraPaths: [some, list, of, paths]` |

### python.autoComplete.addBrackets

This setting has been renamed in Pylance to `python.analysis.completeFunctionParens`. If you install the new language server, Pylance will automatically copy the value you've set for addBrackets and use it to set the completeFunctionParens in Pylance. The setting value's structure remains the same.

| Original setting/value                             | New setting/value                                         |
| -------------------------------------------------- | --------------------------------------------------------- |
| `python.autoComplete.addBrackets: [true or false]` | `python.analysis.completeFunctionParens: [true or false]` |

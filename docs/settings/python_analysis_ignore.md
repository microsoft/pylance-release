# Understanding `python.analysis.ignore` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, auto-completions, code navigation, and other language features to enhance your Python development experience.

In large projects or specific development environments, you might encounter situations where certain files or directories generate unwanted diagnostics (errors and warnings) from Pylance. This can occur with third-party libraries, generated files, or code that intentionally deviates from standard practices. To manage this, Pylance provides the `python.analysis.ignore` setting, allowing you to suppress diagnostics for specified paths.

This guide explains what `python.analysis.ignore` does, how to configure it, and how it can help you tailor Pylance's behavior to your project's needs.

## What is `python.analysis.ignore`?

The `python.analysis.ignore` setting in Pylance allows you to specify paths to files or directories whose diagnostic output (errors and warnings) should be suppressed. Even if these files are included in your workspace or are part of the transitive closure (imported by other files), Pylance will not report any diagnostics for them when they are listed in `python.analysis.ignore`.

### Key Points

- **Diagnostic Suppression**: Pylance will not display any errors or warnings for the files or directories specified in `python.analysis.ignore`.
- **Files Still Processed If Opened**: If you open a file that's in the ignore list, Pylance will still provide IntelliSense features like code completion and hover information, but it will not show errors or warnings.
- **Wildcard Support**: Paths can include wildcard characters:
  - `**`: Matches any directory or multiple levels of directories.
  - `*`: Matches any sequence of zero or more characters.
  - `?`: Matches a single character.

### Use Cases

- **Third-Party Libraries**: Suppress diagnostics in third-party libraries that might not adhere to strict type checking or have type stubs.
- **Generated Code**: Ignore generated files that you don't edit manually and may contain code that triggers diagnostics.
- **Legacy Code**: Exclude old code that you don't want to refactor immediately.

## How to Use `python.analysis.ignore`

You can configure `python.analysis.ignore` in your Visual Studio Code settings.

### Setting in Visual Studio Code Settings

To add `python.analysis.ignore` to your VS Code settings:

1. **Open Settings (JSON)**:

   - Click on the gear icon in the lower-left corner and select **Command Palette**.
   - Type `Preferences: Open Settings (JSON)` and select it.

2. **Add the Setting**:

   - In your `settings.json`, add the `python.analysis.ignore` setting with the paths you want to ignore.

   ```json
   {
       "python.analysis.ignore": ["**/legacy_code/**", "**/generated/**", "**/third_party/**"]
   }
   ```

## Difference Between `ignore` and `exclude`

While both `python.analysis.ignore` and [`python.analysis.exclude`](python_analysis_exclude.md) deal with controlling Pylance's behavior on certain files, they serve different purposes:

- **`python.analysis.ignore`**:

  - Suppresses diagnostics (errors and warnings) for the specified files or directories.
  - The files are still processed if they are imported by other files, but no diagnostics are reported.
  - If you open an ignored file, Pylance provides IntelliSense features but does not report errors or warnings.

- **`python.analysis.exclude`**:

  - Excludes the specified paths from the workspace.
  - Pylance does not process these files for features like code navigation, auto-imports, or symbol searches.
  - If an excluded file is imported by a non-excluded file, Pylance still reports diagnostics for the non-excluded file, potentially generating import errors.

The `ignore` setting is useful when you want Pylance to recognize the files (e.g., for code completion when imported), but you don't want to see diagnostics for them.

## Examples

### Suppressing Diagnostics in Third-Party Libraries

If you're using third-party libraries that are causing unwanted diagnostics, you can ignore them:

```json
{
    "python.analysis.ignore": ["**/site-packages/**"]
}
```

### Ignoring Generated Files

Suppose your project generates code into a `generated` directory:

```json
{
    "python.analysis.ignore": ["src/generated/**"]
}
```

This way, Pylance won't show errors or warnings for the generated code but will still provide IntelliSense when you import from it.

### Ignoring Files in Virtual Environments

Sometimes, Pylance may display diagnostics for files in your virtual environment. You can suppress these by ignoring the virtual environment directories:

```json
{
    "python.analysis.ignore": ["**/venv/**", "**/.venv/**", "**/env/**"]
}
```

## Frequently Asked Questions

### Q: Will Pylance still provide IntelliSense for ignored files?

**A:** Yes, Pylance will still process ignored files for providing IntelliSense features like code completion and hover information, especially when they are imported by other files. The `ignore` setting only suppresses diagnostics (errors and warnings).

### Q: If I open an ignored file, will Pylance show errors in that file?

**A:** No, if a file is specified in `python.analysis.ignore`, Pylance will not show errors or warnings in that file, even if you open it in the editor. However, code completion and other IntelliSense features will still be available.

### Q: How does `python.analysis.ignore` affect performance?

**A:** `python.analysis.ignore` does not significantly affect performance. To improve performance in large projects, use `python.analysis.exclude` to completely exclude files from being processed.

### Q: Can I use `python.analysis.ignore` to suppress specific types of diagnostics?

**A:** No, `python.analysis.ignore` suppresses all diagnostics for the specified files or directories. If you want to suppress specific types of diagnostics, you can use `python.analysis.diagnosticSeverityOverrides` to adjust the severity or disable specific diagnostic rules.

### Q: Should I use `python.analysis.ignore` or `python.analysis.exclude` in most cases?

**A:** Most of the time, users would want to use `python.analysis.exclude` rather than `python.analysis.ignore`. The `exclude` setting removes files from processing, ensuring no errors or warnings appear from those files. `ignore` should only be used in situations where files are included in the workspace but you want to suppress diagnostics specifically without excluding them entirely, such as for complex file structures.

## Related Documentation

For additional guidance on managing large workspaces, refer to the [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code#manually-configure-your-workspace) guide.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference#_python-languag-server-settings)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*


# Understanding `python.analysis.exclude` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a performant and feature-rich language support extension for Python in Visual Studio Code, leveraging the Pyright static type checker. It offers advanced type checking, code navigation, auto-import suggestions, and other IntelliSense features to enhance your Python development experience.

Managing large codebases or repositories with numerous files can sometimes lead to performance issues or unwanted analysis of certain files or directories. Pylance allows you to customize which files and directories should be included or excluded from the workspace through the `python.analysis.exclude` setting.

This guide explains what the `python.analysis.exclude` setting is, how it works, and how you can use it to fine-tune Pylance's workspace to suit your project's needs.

## What Is `python.analysis.exclude`?

The `python.analysis.exclude` setting in Pylance specifies paths to directories or files that should **not** be included in Pylance's workspace. By configuring this setting, you can omit irrelevant, temporary, or large files and directories, which can improve performance and streamline your workspace.

### Default Behavior

By default, Pylance automatically excludes certain directories from workspace to optimize performance. These default exclusions are:

- `**/node_modules`
- `**/__pycache__`
- `.*` directories
- Virtual environment directories (e.g., those containing `bin/activate`, `Scripts/activate`, or `pyvenv.cfg`)

This means that unless you specify your own exclusions, Pylance will ignore these directories.

### Customizing Exclusions

When you specify the `python.analysis.exclude` setting in your `settings.json`, Pylance will **override** the default exclusions. This means that if you customize this setting, you need to explicitly include the default exclusions if you still want them to be ignored including virtual environments.

## How to Use `python.analysis.exclude`

### Configuring the Setting

You can add the `python.analysis.exclude` setting to your Visual Studio Code workspace.

#### Using `settings.json`

To modify your settings in `settings.json`:

1. **Open Settings (JSON)**:
   - Open the Command Palette and select **Preferences: Open Settings (JSON)**.
2. **Add the Setting**:
   - Include the `python.analysis.exclude` setting with the paths you want to exclude.

Example:

```json
{
    "python.analysis.exclude": ["**/node_modules", "**/__pycache__", ".git", "**/build", "env/**"]
}
```

### Specifying Paths

- **Wildcard Characters**:
  - `**`: Matches any directory or multiple levels of directories.
  - `*`: Matches any sequence of zero or more characters.
  - `?`: Matches a single character.
- **Relative Paths**: Paths are typically specified relative to the workspace root.
- **Absolute Paths**: Can be used but are less common and may reduce portability.

### Caveats

- **Overriding Defaults**: Remember that setting `python.analysis.exclude` overrides the default exclusions. If you want to keep the defaults, you need to include them explicitly.
- **Excluded Files May Still Be Processed**: If an excluded file is imported by a file that is included in the workspace, Pylance may still process the excluded file to provide IntelliSense and type checking for the importing file.
- **Opened Files**: Even if a file is in the excluded paths, if you open it in the editor, Pylance will provide analysis for that file.

## Interaction with Other Settings

### [`python.analysis.include`](python_analysis_include.md)

The `python.analysis.include` setting specifies paths to directories or files that should be included in Pylance's workspace. By default, Pylance includes all files in the workspace root.

- **Order of Precedence**: The `exclude` setting takes precedence over the `include` setting. This means you can include broad directories and then fine-tune specific exclusions.

### [`python.analysis.ignore`](python_analysis_ignore.md)

The `python.analysis.ignore` setting specifies paths whose diagnostic output (errors and warnings) should be suppressed, even if they are included in the analysis.

- **Difference from `exclude`**: While `exclude` prevents files from being processed (unless imported), `ignore` allows files to be processed but suppresses diagnostic messages.

## Examples

### Excluding Specific Directories

To exclude directories like `build`, `env`, and keep the default exclusions, your settings might look like:

```json
{
    "python.analysis.exclude": ["**/node_modules", "**/__pycache__", ".git", "**/build", "env/**"]
}
```

### Excluding All Files Except Opened Ones

To exclude all files from workspace, effectively processing only the files you have open:

```json
{
    "python.analysis.exclude": ["**"]
}
```

### Excluding Large or Irrelevant Directories

If your workspace contains a large directory that you don't need Pylance to include (e.g., `data`), you can exclude it:

```json
{
    "python.analysis.exclude": ["**/data/**"]
}
```

### Re-including a Subdirectory

If you want to exclude a directory but include a specific subdirectory, you can adjust both `include` and `exclude`:

```json
{
    "python.analysis.include": ["src/**/*", "scripts/**/*"],
    "python.analysis.exclude": ["**/tests/**", "**/data/**"]
}
```

## Common Use Cases

### Improving Performance in Large Workspaces

In large projects, Pylance may spend significant time processing files you don't need to edit or inspect.

- **Solution**: Exclude directories that are not relevant to your current work, such as build artifacts, generated files, or large data directories.

### Excluding Generated or External Code

If your workspace includes generated code or external libraries that you do not need to use:

- **Example**: Exclude the `gen` directory containing auto-generated code:

```json
{
    "python.analysis.exclude": ["gen/**"]
}
```

### Virtual Environments Inside the Workspace

If your virtual environment is located within your workspace (e.g., `./venv`), and you customize `python.analysis.exclude`, you need to exclude your virtual environment directory explicitly:

```json
{
    "python.analysis.exclude": ["**/node_modules", "**/__pycache__", ".git", "venv/**"]
}
```

## Frequently Asked Questions

### Why is Pylance still processing files I've excluded?

If an excluded file or directory is imported by files that are included, Pylance may still process those files to ensure accurate IntelliSense.

### Does excluding files improve performance?

Yes, excluding unnecessary files and directories can improve Pylance's performance by reducing the workload.

### What happens if I specify `python.analysis.exclude` and don't include the default exclusions?

If you specify `python.analysis.exclude` without including the default exclusions, Pylance will stop automatically excluding the default directories (`**/node_modules`, `**/__pycache__`, `.git`, and virtual environments). You need to include them explicitly if you still want them excluded.

### How can I exclude all files and only analyze open files?

Set `python.analysis.exclude` to `["**"]`:

```json
{
    "python.analysis.exclude": ["**"]
}
```

This configuration tells Pylance to exclude all files from analysis, effectively only analyzing files you have open in the editor.

## Related Documentation

For additional guidance on managing large workspaces, refer to the [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code#manually-configure-your-workspace) guide.

---

For more information on Pylance settings and customization, refer to the [Pylance README](https://github.com/microsoft/pylance-release#settings-and-customization) and the [Pyright Configuration Documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md).

---

*"This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness."*


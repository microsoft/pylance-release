# Understanding `python.analysis.exclude` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a performant and feature-rich language server extension for Python in Visual Studio Code, leveraging the Pyright static type checker. It offers advanced type checking, code navigation, auto-import suggestions, and other IntelliSense features to enhance your Python development experience.

Managing large codebases or repositories with numerous files can sometimes lead to performance issues or unwanted analysis of certain files or directories. Pylance allows you to customize which files and directories should be included or excluded from the workspace through the `python.analysis.exclude` setting.

This guide explains what the `python.analysis.exclude` setting is, how it works, and how you can use it to fine-tune Pylance's workspace to suit your project's needs.

## What Is `python.analysis.exclude`?

The `python.analysis.exclude` setting in Pylance specifies paths to directories or files that should **not** be included in Pylance's workspace. By configuring this setting, you can omit irrelevant, temporary, or large files and directories, which can improve performance and streamline your workspace.

### Default Behavior

By default, Pylance excludes certain directories from the workspace to optimize performance. These default exclusions are:

- `**/node_modules`
- `**/__pycache__`
- `**/__editable__.*`
- Hidden directories (dotfiles), i.e. any directory whose name begins with a `.` (for example `.git`, `.venv`, `.tox`)
- Auto-detected virtual environment directories (e.g., those containing `bin/activate`, `Scripts/activate`, or `pyvenv.cfg`)

These built-in exclusions are controlled by [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md), which is enabled by default. They are applied *in addition to* any paths you set in `python.analysis.exclude` (see [Customizing Exclusions](#customizing-exclusions) below).

### Customizing Exclusions

The `python.analysis.exclude` setting is **additive**: any paths you specify are added *on top of* the default exclusions rather than replacing them. Specifying your own excludes never disables the built-in ones, so you do **not** need to repeat the defaults (such as `**/node_modules` or your virtual environment) to keep them excluded.

> **Note**: This is a change from older versions of Pylance, where specifying any custom exclude path silently dropped the built-in default exclusions and virtual-environment auto-detection. Custom excludes are now always additive, similar to VS Code's `files.exclude` and `search.exclude`. You can turn the built-in defaults off entirely with [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md).

### Precedence Over `include`

The default exclusions take precedence over [`python.analysis.include`](python_analysis_include.md). This means a directory that Pylance auto-detects as a virtual environment (or that matches another default exclusion) stays excluded **even if you explicitly list it in `include`**. Adding a path to `include` does not override the built-in excludes.

### Turning Off the Built-in Defaults

If you need Pylance to analyze a directory that a default exclusion is skipping — for example, a directory that was incorrectly auto-detected as a virtual environment — set [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md) to `false`. This disables **all** of the built-in default exclusions (including virtual-environment auto-detection), so only the paths you list in `python.analysis.exclude` are excluded:

```json
{
    "python.analysis.useDefaultExcludes": false,
    "python.analysis.exclude": ["**/node_modules", "**/build"]
}
```

Because this turns off every built-in exclude, you'll typically want to re-add the ones you still care about (such as `**/node_modules`) to `python.analysis.exclude` yourself. Disabling the defaults can slow analysis significantly in workspaces that contain large dependency or environment directories.

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
    "python.analysis.exclude": ["**/build", "env/**"]
}
```

Because the default exclusions are always applied, you only need to list the *additional* paths you want to exclude — the defaults (`**/node_modules`, `**/__pycache__`, dotfiles, virtual environments, etc.) remain excluded automatically.

### Specifying Paths

- **Wildcard Characters**:
    - `**`: Matches any directory or multiple levels of directories.
    - `*`: Matches any sequence of zero or more characters.
    - `?`: Matches a single character.
- **Relative Paths**: Paths are typically specified relative to the workspace root.
- **Absolute Paths**: Can be used but are less common and may reduce portability.

### Caveats

- **Defaults Are Additive**: Paths you set in `python.analysis.exclude` are added on top of the default exclusions — they do not replace them. You don't need to re-list the defaults to keep them excluded.
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

To exclude directories like `build` and `env`, your settings might look like:

```json
{
    "python.analysis.exclude": ["**/build", "env/**"]
}
```

The default exclusions (`**/node_modules`, `**/__pycache__`, dotfiles, virtual environments, etc.) remain in effect automatically, so you don't need to list them here.

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

Virtual environments are auto-detected and excluded by default, so a venv located inside your workspace (e.g., `./venv`) is excluded automatically — even when you specify other custom excludes. You do **not** need to list it explicitly:

```json
{
    "python.analysis.exclude": ["**/build"]
}
```

In the rare case that Pylance misdetects a regular directory as a virtual environment, note that adding it to `python.analysis.include` will **not** rescue it — the default exclusions take precedence over `include`. Instead, set [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md) to `false` to turn off the built-in excludes (including virtual-environment auto-detection).

## Frequently Asked Questions

### Why is Pylance still processing files I've excluded?

If an excluded file or directory is imported by files that are included, Pylance may still process those files to ensure accurate IntelliSense.

### Does excluding files improve performance?

Yes, excluding unnecessary files and directories can improve Pylance's performance by reducing the workload.

### What happens if I specify `python.analysis.exclude` and don't include the default exclusions?

Nothing changes for the defaults — they're always applied. Custom excludes are **additive**: the paths you specify are added on top of the default exclusions (`**/node_modules`, `**/__pycache__`, `**/__editable__.*`, dotfiles, and virtual environments), which stay excluded automatically. You don't need to re-list them. To turn the defaults off entirely, use [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md).

### Pylance excluded a directory that isn't a virtual environment. How do I get it analyzed again?

Virtual-environment detection is a heuristic, so Pylance can occasionally treat a regular directory as a virtual environment and exclude it. Because the default exclusions take precedence over `include`, adding the directory to [`python.analysis.include`](python_analysis_include.md) will **not** rescue it. Instead, set [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md) to `false`, which disables all built-in excludes (including virtual-environment auto-detection) so only your explicit `python.analysis.exclude` paths apply.

### How can I exclude all files and only analyze open files?

Set `python.analysis.exclude` to `["**"]`:

```json
{
    "python.analysis.exclude": ["**"]
}
```

This configuration tells Pylance to exclude all files from analysis, effectively only analyzing files you have open in the editor.

### Why do certain `**` patterns fail to match the file structure?

In the given file structure:

```
my_project/
├── src/
│   ├── module1/
│   │   ├── module2/
```

The pattern `**/src/**` does not match `src/` because there is no folder preceding `src`. Similarly, `src/**/module1` does not match `src/module1/` because there is no folder between `src` and `module1`. However, `src/**/module2` successfully matches `module2/` because `module1` exists between `src` and `module2`.

## Related Settings

- [`python.analysis.useDefaultExcludes`](python_analysis_useDefaultExcludes.md): Turns the built-in default exclusions on or off.
- [`python.analysis.include`](python_analysis_include.md): Controls which files are included in analysis.
- [`python.analysis.ignore`](python_analysis_ignore.md): Suppresses diagnostics without excluding files.
- [`python.analysis.diagnosticMode`](python_analysis_diagnosticMode.md): Controls whether diagnostics run on all files or only open files.

## See Also

- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — per-subfolder exclusion patterns
- [How to Tune Pylance Performance](../howto/performance-tuning.md) — using `exclude` to reduce analysis scope
- [How to Troubleshoot Settings](../howto/settings-troubleshooting.md) — what happens when `pyrightconfig.json` overrides `exclude`

## Related Documentation

For additional guidance on managing large workspaces, refer to the [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code#manually-configure-your-workspace) guide.

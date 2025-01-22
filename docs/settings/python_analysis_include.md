# Understanding `python.analysis.include` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides advanced type checking, IntelliSense, code navigation, and other language features to enhance your Python development experience.

One of Pylance's capabilities is to analyze your project's codebase to provide accurate IntelliSense and code navigation features. However, in large projects or when you want to focus Pylance's features on specific directories, you may need to customize which files and directories Pylance includes in its workspace.

This guide explains what `python.analysis.include` is, how it affects Pylance's behavior, and how you can use it to control which parts of your codebase are included in the workspace.

## What Is `python.analysis.include`?

The `python.analysis.include` setting in Pylance allows you to specify paths to directories or files that Pylance should consider as part of your workspace for its features. By customizing this setting, you can control which parts of your codebase Pylance monitors, which can help manage performance and focus on relevant code sections, especially in large projects.

### Key Points

- **Default Behavior**: By default, Pylance includes everything in the editor's workspace root directory when analyzing your code. This means all files and subdirectories are considered part of the workspace.

- **Customizing `include` Overrides Defaults**: If you customize `python.analysis.include`, Pylance's automatic inclusion of the entire workspace is overridden. You need to explicitly specify all directories and files you want to include in the analysis, including the workspace root if desired.

- **Wildcard Support**: Paths specified in `python.analysis.include` can include wildcard characters:

  - `**`: Matches any directory or multiple levels of directories.
  - `*`: Matches any sequence of zero or more characters.
  - `?`: Matches a single character.

- **Interaction with `exclude`**: The `python.analysis.exclude` setting specifies paths to directories or files that Pylance should ignore, even if they are included in `include`. Paths specified in `exclude` take precedence over those in `include`. This allows you to fine-tune which parts of your included directories should be ignored.

## How to Use `python.analysis.include`

You can modify the `python.analysis.include` setting in your VS Code settings, either globally (User settings) or for your workspace.

### Modifying the Setting

1. **Open the Settings**:

   - In Visual Studio Code, open the settings by selecting **Settings** from the gear icon in the lower-left corner.

2. **Search for the Setting**:

   - In the search bar at the top of the Settings pane, type `python.analysis.include`.

3. **Modify the Setting**:

   - Add the paths to the directories or files you want Pylance to include. For example:
     ```json
     "python.analysis.include": ["src/**/*", "scripts/**/*"]
     ```

Alternatively, you can edit your `settings.json` file directly:

1. **Open Settings (JSON)**:

   - Open the Command Palette and select **Preferences: Open Settings (JSON)**.

2. **Add the Setting**:

   - Add or modify the following line in your `settings.json` file:
     ```json
     "python.analysis.include": ["src/**/*", "scripts/**/*"]
     ```

### Using Wildcards

- **`**` (Double Asterisk)**: Matches any directory or multiple levels of directories. For example,`src/**`includes all files and subdirectories under`src`.

- **`*` (Asterisk)**: Matches any sequence of zero or more characters within a single directory level. For example, `src/*` includes all immediate subdirectories and files under `src`.

- **`?` (Question Mark)**: Matches any single character. For example, `src/fil?.py` matches `src/file.py` and `src/filx.py`.

## Examples

### 1. Including Specific Directories

Suppose your workspace has the following structure:

```
my_project/
├── src/
│   ├── module1/
│   ├── module2/
├── tests/
├── scripts/
├── build/
├── .git/
```

To include only the `src` and `scripts` directories in Pylance's analysis:

```json
"python.analysis.include": ["src/**/*", "scripts/**/*"]
```

### 2. Including Files with Specific Patterns

To include only Python files in the `src` directory:

```json
"python.analysis.include": ["src/**/*.py"]
```

### 3. Including the Workspace Root

If you customize `python.analysis.include` and still want to include the entire workspace root, you need to specify it explicitly:

```json
"python.analysis.include": ["**/*"]
```

### 4. Combining `include` and `exclude`

To include all files in the `src` directory but exclude temporary files:

```json
{
    "python.analysis.include": ["src/**/*"],
    "python.analysis.exclude": ["src/temp/**/*"]
}
```

## When and Why to Use `python.analysis.include`

### Managing Performance in Large Projects

In large projects, Pylance's analysis of the entire codebase can consume significant resources and may affect performance. By limiting the analysis to specific directories using `python.analysis.include`, you can improve performance by reducing the scope of files Pylance needs to process.

### Focusing on Relevant Code Sections

When working on a particular module or component of your project, you might want Pylance to focus its analysis on that specific part. Customizing `python.analysis.include` allows you to include only the directories relevant to your current work.

### Avoiding Analysis of Generated or External Code

Your project may contain directories with generated code, build artifacts, or external dependencies that you don't want Pylance to analyze. By specifying the directories to include, you can prevent Pylance from analyzing these parts of your codebase.

## Frequently Asked Questions

### Q: What happens if I customize `python.analysis.include` but forget to include the workspace root?

**A:** If you set `python.analysis.include` without including the workspace root (e.g., `"**/*"`), Pylance will only analyze the paths you specified. This means any files not under the specified paths will be ignored in the analysis. If you want to include the entire workspace root along with additional paths, you should explicitly include it:

```json
"python.analysis.include": ["**/*", "/additional/path/**/*"]
```

### Q: Do paths in `python.analysis.include` support wildcards?

**A:** Yes, paths can include wildcard characters

### Q: How does `python.analysis.include` interact with `python.analysis.exclude`?

**A:** Paths specified in [`python.analysis.exclude`](python_analysis_exclude.md) take precedence over those in `python.analysis.include`. This means you can include a broad set of directories and then use `exclude` to remove specific subdirectories or files from the analysis.

### Q: Can I use `python.analysis.include` to include files outside of my workspace?

**A:** Yes, you can specify absolute paths or paths relative to the workspace. This is useful if you want Pylance to analyze code in directories outside of your current workspace, such as shared libraries or dependencies located elsewhere on your system.

### Q: Why is Pylance not recognizing my files even after setting `python.analysis.include`?

**A:** If Pylance isn't recognizing your files, ensure that:

- The paths specified in `python.analysis.include` are correct and match the actual directory structure.
- You haven't overridden the default include paths without including the workspace root (if needed).
- There are no conflicting settings in [`python.analysis.exclude`](python_analysis_exclude.md) that might be excluding the files you want to include.

### Q: Can users use `${workspaceFolder:rootName}` in `include/exclude/ignore`, and when would they use it?

**A:** Yes, `${workspaceFolder:rootName}` can be used. In a multi-root workspace, if you want to specify `include`, `exclude`, or `ignore` settings for each workspace root individually, you can prefix those settings with `${workspaceFolder:rootName}` to indicate which root the setting applies to.

For example, consider the following multi-root workspace configuration:

```json
{
	"folders": [
		{
			"path": "first"
		},
		{
			"path": "second"
		},
		{
			"name": "third",
			"path": "../extraRoot"
		}
	],
	"settings": {
		"python.analysis.include": [
			"${workspaceFolder:first}/src/**",
			"${workspaceFolder:second}/**"
		],
		"python.analysis.exclude": [
			"${workspaceFolder:third}/testFiles/**"
		]
	}
}
```

In this example:

- `first` will get `src/**` as its include setting.
- `second` will get `**` as its include setting.
- `third` will use the default include settings but exclude `testFiles/**`.

This approach allows you to provide `include`, `exclude`, or `ignore` configurations tailored to each workspace root in a multi-root environment in VS Code.

### Q: Is there any other way to provide `include/exclude/ignore` settings per workspace in a multi-root workspace?

**A:** Yes, besides using `${workspaceFolder:rootName}`, users can also:

1. Create a `.vscode/settings.json` file for each root folder and define `python.analysis.include`, `python.analysis.exclude`, or `python.analysis.ignore` settings there.
2. Place a `pyrightconfig.json` file in each root folder to customize include/exclude/ignore settings.
3. Use `pyproject.toml` files in each root folder to configure these settings, especially if you’re following a specific project structure or build system.

These methods offer flexibility for managing analysis settings per workspace root in a multi-root VS Code environment.

## Related Documentation

For additional guidance on managing large workspaces, refer to the [Opening Large Workspaces in VS Code](https://github.com/microsoft/pylance-release/wiki/Opening-Large-Workspaces-in-VS-Code#manually-configure-your-workspace) guide.

---

*For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation.*

---

*This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness.*


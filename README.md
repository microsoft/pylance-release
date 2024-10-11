# Pylance

### Fast, feature-rich language support for Python

This repository is for providing feedback and documentation on the [Pylance language server extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) in Visual Studio Code. You can use the repository to report issues or submit feature requests. The Pylance codebase is not open-source but you can contribute to [Pyright](https://github.com/microsoft/pyright) to make improvements to the core typing engine that powers the Pylance experience.

Pylance is the default language support for [Python in Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and is shipped as part of that extension as an optional dependency.

# Quick Start

1. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) from the marketplace. Pylance will be installed as an optional extension.
1. Open a Python (.py) file and the Pylance extension will activate.

Note: If you've previously set a language server and want to try Pylance, make sure you've set `"python.languageServer": "Default" or "Pylance"` in your settings.json file using the text editor, or using the Settings Editor UI.

# Features

<img src=images/all-features.gif>

Pylance provides some awesome features for Python 3, including:

-   Docstrings
-   Signature help, with type information
-   Parameter suggestions
-   Code completion
-   Auto-imports (as well as add and remove import code actions)
-   As-you-type reporting of code errors and warnings (diagnostics)
-   Code outline
-   Code navigation
-   Type checking mode
-   Native multi-root workspace support
-   IntelliCode compatibility
-   Jupyter Notebooks compatibility
-   Semantic highlighting

See the [changelog](CHANGELOG.md) for the latest release.

# Settings and Customization

Pylance provides users with the ability to customize their Python language support via a host of settings which can either be placed in the `settings.json` file in your workspace, or edited through the Settings Editor UI. 

- [`python.analysis.languageServerMode`](docs/settings/python_analysis_languageServerMode.md)
    - Offers predefined configurations to help users optimize Pylance's performance based on their development needs. It controls how many IntelliSense features Pylance provides, allowing you to choose between full language service functionality or a lightweight experience optimized for performance.
    - Default value: `default`
    - Available values:
        - `default` (default)
        - `light`
    - Description:
        - `default`: Provides a balanced experience with many useful features enabled by default. It ensures that the language server delivers sufficient functionality for most users without overloading the system. Advanced features can be enabled as needed, allowing for further customization at the cost of performance.
        - `light`: Designed for users seeking a lightweight, memory-efficient setup. This mode disables various features to make Pylance function more like a streamlined text editor. Ideal for those who do not require the full breadth of IntelliSense capabilities and prefer Pylance to be as resource-friendly as possible.
    -  Modifies the default value of the following settings:      
        | Setting                           | `light` mode   | `default` mode   |
        | :----------------------------- | :--------- | :--------- |
        | python.analysis.exclude                   | ["**"]      | []         |
        | python.analysis.useLibraryCodeForTypes    | false       | true       |
        | python.analysis.enablePytestSupport       | false       | true       |
        | python.analysis.indexing                  | false       | true       |
    - The  settings above can be changed individually to override the default values. 

- `python.analysis.typeCheckingMode`
    - Used to specify the level of type checking analysis performed.
    - Default: `off`. 
        > Note that the value of this setting can be overridden by having a pyrightconfig.json or a pyproject.toml. For more information see this [link](https://aka.ms/AArua4c).
    - Available values:
        - `off`: No type checking analysis is conducted; unresolved imports/variables diagnostics are produced
        - `basic`: All `off` rules + basic type checking rules
        - `standard`: All `off` rules + basic type checking rules + standard type checking rules
        - `strict`: All `off` rules + all type checking rules.
    - Performance Consideration:
        - Setting `python.analysis.typeCheckingMode` to `off` can improve performance by disabling type checking analysis, which can be resource-intensive, especially in large codebases.

- `python.analysis.diagnosticMode`
    - Used to allow a user to specify what files they want the language server to analyze to get problems flagged in their code.
    - Available values:
        - `workspace`
        - `openFilesOnly` (default)
    - Performance Consideration:
        - Setting `python.analysis.diagnosticMode` to `openFilesOnly` limits analysis to open files, improving performance by reducing the amount of code Pylance needs to process in large workspaces.

- `python.analysis.include`
    - Paths of directories or files that should be included. If no paths are specified, Pylance defaults to the directory that contains workspace root. Paths may contain wildcard characters `**` (a directory or multiple levels of directories), `*` (a sequence of zero or more characters), or `?` (a single character).
    - Default value: empty array

- `python.analysis.exclude`
    - Paths of directories or files that should not be included. These override the include directories, allowing specific subdirectories to be excluded. Note that files in the exclude paths may still be included in the analysis if they are referenced (imported) by source files that are not excluded. Paths may contain wildcard characters `**` (a directory or multiple levels of directories), `*` (a sequence of zero or more characters), or `?` (a single character). If no exclude paths are specified, Pylance automatically excludes the following: `**/node_modules`, `**/__pycache__`, `.git` and any virtual environment directories.
    - Default value: empty array (or `["**"]` in `light` mode)
    - Performance Consideration:
        - Excluding unnecessary files or directories can significantly improve performance by reducing the scope of analysis. For example, setting `python.analysis.exclude` to `["**"]` will exclude all files except those currently open, minimizing resource consumption.

- `python.analysis.ignore`
    - Paths of directories or files whose diagnostic output (errors and warnings) should be suppressed even if they are an included file or within the transitive closure of an included file. Paths may contain wildcard characters `**` (a directory or multiple levels of directories), `*` (a sequence of zero or more characters), or `?` (a single character).
    - Default value: empty array

- `python.analysis.stubPath`
    - Used to allow a user to specify a path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory.
    - Default value: `./typings`

- `python.analysis.autoSearchPaths`
    - Used to automatically add search paths based on some predefined names (like `src`).
    - Available values:
        - `true` (default)
        - `false`

- `python.analysis.extraPaths`
    - Used to specify extra search paths for import resolution. This replaces the old `python.autoComplete.extraPaths` setting.
    - Default value: empty array

- `python.analysis.diagnosticSeverityOverrides`
    - Used to allow a user to override the severity levels for individual diagnostics should they desire.
    - Accepted severity values:
        - `error` (red squiggle)
        - `warning` (yellow squiggle)
        - `information` (blue squiggle)
        - `none` (disables the rule)
    - Available rules to use as keys can be found [here](DIAGNOSTIC_SEVERITY_RULES.md)
    - Example:
    ```json
    {
        "python.analysis.diagnosticSeverityOverrides": {
            "reportUnboundVariable": "information",
            "reportImplicitStringConcatenation": "warning"
        }
    }
    ```

- `python.analysis.typeEvaluation`
    - Used to allow a user to override the behavior of type evaluator should they desire.
    - Available rules to use as subkeys can be found [here](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#type-evaluation-settings)
    - Example:
    ```json
    {
        "python.analysis.typeEvaluation.enableReachabilityAnalysis": true,
        "python.analysis.typeEvaluation.strictDictionaryInference": false
    }
    ```

- `python.analysis.disableTaggedHints`
    - Disable hint diagnostics with special hints for grayed-out or strike-through text.
    - Accepted values:
        - `true`
        - `false` (default)

- `python.analysis.useLibraryCodeForTypes`
    - Used to parse the source code for a package when a typestub is not found.
    - Default value: `true` (or `false` in `light` mode)
    - Accepted values:
        - `true` (default)
        - `false`
    - Performance Consideration:
        - Setting `python.analysis.useLibraryCodeForTypes` to `false` can improve performance by preventing Pylance from parsing the source code of third-party libraries when type stubs are unavailable, thereby reducing resource usage.

- [`python.analysis.indexing`](docs/settings/python_analysis_indexing.md)
    - Used to specify whether Pylance should index installed third party libraries and user files to improve features such as auto-import, add import, workspace symbols, etc.
    - Without indexing, auto-import, add import, and workspace symbols will have less information.
    - Default value: `true` (or `false` in `light` mode)
    - Available values:
        - `true` (default)
        - `false`
    - Performance Consideration:
        - Disabling indexing by setting `python.analysis.indexing` to `false` can improve performance by reducing resource consumption, especially in large projects, at the cost of making features like auto-imports and workspace symbol search find fewer symbols.

- `python.analysis.userFileIndexingLimit`
    - Maximum number of user files to index in the workspace. Indexing files is a performance-intensive task. Please use this setting to limit the number of files you want us to index. If you enter -1, we will index all files.
    - Default value: 2000

- [`python.analysis.packageIndexDepths`](docs/settings/python_analysis_packageIndexDepths.md)
    - Used to override how many levels under installed packages to index on a per package basis. By default, only top-level modules are indexed (depth = 1). To index submodules, increase depth by 1 for each level of submodule you want to index.
    - Accepted values:
        ```jsonc
        {
            "name": "package name (str)",
            "depth": "depth to scan (int)",
            "includeAllSymbols": "whether to include all symbols (bool)"
        }
        ```
        If `includeAllSymbols` is set to `false`, only symbols in each package's `__all__` are included. When it's set to `true`, Pylance will index every module/top level symbol declarations in the file.
    - Example:
        ```jsonc
        [
            { "name": "sklearn", "depth": 2, "includeAllSymbols": true },
            { "name": "matplotlib", "depth": 3, "includeAllSymbols": false }
        ]
        ```
    - Performance Consideration:
        - Adjusting this setting will cause Pylance to allocate more resources for indexing third-party libraries.

- [`python.analysis.includeAliasFromUserFiles`](docs/settings/python_analysis_includeAliasesFromUserFiles.md)
    - Include alias symbols from user files. This will make alias symbols appear in features such as `add import` and `auto import`.
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Enabling this can impact performance by increasing the number of completion items and indexing multiple files as changes occur.

- `python.analysis.autoImportCompletions`
    - Used to control the offering of auto-imports in completions. This will impact number of items shown in the completion and performance.
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Enabling `python.analysis.autoImportCompletions` can impact performance by increasing the number of completion items and resource usage. Disabling it can improve performance by reducing the computational overhead during code completion.

- `python.analysis.importFormat`
    - Defines the default format for import module.
    - Accepted values:
        - `absolute` (default)
        - `relative`

- `python.analysis.completeFunctionParens`
    - Add parentheses to function completions.
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Disabling `python.analysis.completeFunctionParens` can slightly improve performance by reducing the overhead during code completion, though the impact is minimal.

- `python.analysis.inlayHints.variableTypes`
    - Enable/disable inlay hints for variable types.
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Disabling inlay hints for variable types by setting `python.analysis.inlayHints.variableTypes` to `false` can improve performance by reducing the processing required to generate these hints, which can be beneficial in large codebases.

- `python.analysis.inlayHints.functionReturnTypes`
    - Enable/disable inlay hints for function return types.
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Disabling inlay hints for function return types can improve performance by reducing the overhead of generating these hints.

- `python.analysis.inlayHints.callArgumentNames`
    - Enable/disable inlay hints for call argument names.
    - Accepted values:
        - `off` (default)
        - `partial`
        - `all`
    - Performance Consideration:
        - Setting `python.analysis.inlayHints.callArgumentNames` to `off` can improve performance by reducing the processing needed to display argument names during function calls.

- `python.analysis.inlayHints.pytestParameters`
    - Enable/disable inlay hints for pytest function parameters.
    - Accepted values:
        - `true`
        - `false` (default)
    - Example:
        ```python
        def test_foo(my_fixture):
            assert(my_fixture)
        ```
        becomes
        ```python
        def test_foo(my_fixture: str):
            assert(my_fixture)
        ```
    - Performance Consideration:
        - Disabling inlay hints for pytest parameters can improve performance by reducing the overhead associated with generating these hints.

- `python.analysis.fixAll`
    - The set of commands to run when doing a `fixall`.
    - Accepted values:
        - `source.unusedImports`
        - `source.convertImportFormat`

- `python.analysis.enablePytestSupport`
    - Enable pytest goto def and inlay hint support for fixtures. 
    - Default value: `true` (or `false` in `light` mode)
    - Accepted values:
        - `true` (default)
        - `false`
    - Performance Consideration:
        - Disabling pytest support by setting `python.analysis.enablePytestSupport` to `false` can improve performance by reducing the overhead associated with providing IntelliSense features for pytest fixtures.

- `python.analysis.autoFormatStrings`
    - When typing a `{` in a string, automatically puts an `f` on the front of the string. 
    - Accepted values:
        - `true` 
        - `false` (default)
    - Performance Consideration:
        - Disabling `python.analysis.autoFormatStrings` can slightly improve performance by reducing the processing required during string formatting, though the impact is minimal.

- `python.analysis.nodeExecutable`
    - Path to a node executable to use to run Pylance. If this value is empty, Pylance uses VS Code's node executable.
    - Set this value when you are having out of memory issues. Using a custom node executable allows Pylance to allocate more memory.
    - Accepted values:
        - `any executable path` 

- `python.analysis.autoIndent`
    - Automatically adjust indentation based on language semantics when typing Python code.
    - Accepted values:
        - `true` (default)
        - `false` 

- `python.analysis.supportRestructuredText`
    - Enable/disable support for reStructuredText in docstrings. Experimental, may cause docstrings to no longer render.
    - Accepted values:
        - `true` 
        - `false` (default)
    - Performance Consideration:
        - Disabling support for reStructuredText in docstrings by setting `python.analysis.supportRestructuredText` to `false` can improve performance by reducing the overhead of parsing complex docstrings.

- `python.analysis.aiCodeActions`
    - Enable/disable AI-assisted code actions. Requires the Copilot Chat extension to be enabled.
    - Accepted values:
        - `true` 
        - `false` (default)
    - Available code actions to use as keys: `implementAbstractClasses`.
    - Example:
    ```json
    {
        "python.analysis.aiCodeActions": {
            "implementAbstractClasses": true
        }
    }
    ```

- `python.analysis.supportDocstringTemplate`
    - Enable/disable support for docstring generation.
    - Accepted values:
        - `true` 
        - `false` (default)
    - Example:
        ```python
        def foo(arg):
            """
            |<Trigger completions here
            """
        ```

# Semantic highlighting

Visual Studio Code uses TextMate grammars as the main tokenization engine. TextMate grammars work on a single file as input and break it up based on lexical rules expressed in regular expressions.

Semantic tokenization allows language servers to provide additional token information based on the language server's knowledge on how to resolve symbols in the context of a project. Themes can opt-in to use semantic tokens to improve and refine the syntax highlighting from grammars. The editor applies the highlighting from semantic tokens on top of the highlighting from grammars.

Here's an example of what semantic highlighting can add:

Without semantic highlighting:

![ semantic highlighting disabled ](semantic-disabled.png)

With semantic highlighting:

![ semantic highlighting enabled ](semantic-enabled.png)

Semantic colors can be customized in settings.json by associating the Pylance semantic token types and modifiers with the desired colors.

-   Semantic token types

    -   class, enum
    -   parameter, variable, property, enumMember
    -   function, member
    -   module
    -   intrinsic
    -   magicFunction (dunder methods)
    -   selfParameter, clsParameter

-   Semantic token modifiers
    -   declaration
    -   readonly, static, abstract
    -   async
    -   typeHint, typeHintComment
    -   decorator
    -   builtin

The [scope inspector](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide#scope-inspector) tool allows you to explore what semantic tokens are present in a source file and what theme rules they match to.

Example of customizing semantic colors in settings.json:

```jsonc
{
    "editor.semanticTokenColorCustomizations": {
        "[One Dark Pro]": {
            // Apply to this theme only
            "enabled": true,
            "rules": {
                "magicFunction:python": "#ee0000",
                "function.declaration:python": "#990000",
                "*.decorator:python": "#0000dd",
                "*.typeHint:python": "#5500aa",
                "*.typeHintComment:python": "#aaaaaa"
            }
        }
    }
}
```
# Source Code Actions

- `source.unusedImports`

    -   Remove all unused imports in a file

- `source.convertImportFormat`

    -   Convert import format according to `python.analysis.importFormat`.

- `source.fixall.pylance`
    - Apply the commands listed in the `python.analysis.fixall` setting

# Troubleshooting

Known issues are documented in [TROUBLESHOOTING](TROUBLESHOOTING.md).

# Contributing

Pylance leverages Microsoft's open-source static type checking tool, Pyright, to provide performant language support for Python.

Code contributions are welcomed via the [Pyright](https://github.com/microsoft/pyright) repo.

Pylance ships with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking. Our type stubs are sourced from [typeshed](https://github.com/python/typeshed) and our work-in-progress stub repository, [microsoft/python-type-stubs]( https://github.com/microsoft/python-type-stubs). Type stubs in microsoft/python-type-stubs will be contributed back to typeshed or added inline to source packages once they are of high enough quality.

For information on getting started, refer to the [CONTRIBUTING instructions](https://github.com/microsoft/pyright/blob/main/CONTRIBUTING.md).

# Feedback

-   File a bug in [GitHub Issues](https://github.com/microsoft/pylance-release/issues/new/choose)
-   [Tweet us](https://twitter.com/pythonvscode/) with other feedback

# License

See [LICENSE](LICENSE) for more information.

Pylance
=====================
### Fast, feature-rich language support for Python

This repository is for providing feedback and documentation on the [Pylance language server extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) in Visual Studio Code. You can use the repository to report issues or submit feature requests. The Pylance codebase is not open-source but you can contribute to [Pyright](https://github.com/microsoft/pyright) to make improvements to the core typing engine that powers the Pylance experience.

Pylance is the default language support for [Python in Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and is shipped as part of that extension as an optional dependency. 

The Pylance name is a small ode to Monty Python's Lancelot who was the first knight to answer the bridgekeeper's questions in the Holy Grail.

Quick Start
============
1. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) from the marketplace. Pylance will be installed as an optional extension.
1. Open a Python (.py) file and the Pylance extension will activate.

Note: If you've previously set a language server and want to try Pylance, make sure you've set `"python.languageServer": "Default" or "Pylance"` in your settings.json file using the text editor, or using the Settings Editor UI.

Features
=========

![ features ](images/all-features.gif)

Pylance provides some awesome features for Python 3, including:

* Docstrings
* Signature help, with type information
* Parameter suggestions
* Code completion
* Auto-imports (as well as add and remove import code actions)
* As-you-type reporting of code errors and warnings (diagnostics)
* Code outline
* Code navigation
* Type checking mode
* Native multi-root workspace support
* Jupyter Notebooks compatibility
* Semantic highlighting

See the [changelog](CHANGELOG.md) for the latest release.

Settings and Customization
===============
Pylance provides users with the ability to customize their Python language support via a host of settings which can either be placed in the `settings.json` file in your workspace, or edited through the Settings Editor UI. 

- [`python.analysis.languageServerMode`](docs/settings/python_analysis_languageServerMode.md)
    - Offers predefined configurations to help users optimize Pylance's performance based on their development needs. It controls how many IntelliSense features Pylance provides, allowing you to choose between full language service functionality or a lightweight experience optimized for performance.
    - Default value: `default`
    - Available values:
        - `light`
        - `default` (default)
        - `full`
    - Description:
        - `default`: Provides a balanced experience with many useful features enabled by default. It ensures that the language server delivers sufficient functionality for most users without overloading the system. Advanced features can be enabled as needed, allowing for further customization at the cost of performance.
        - `light`: Designed for users seeking a lightweight, memory-efficient setup. This mode disables various features to make Pylance function more like a streamlined text editor. Ideal for those who do not require the full breadth of IntelliSense capabilities and prefer Pylance to be as resource-friendly as possible.
        - `full`: Designed for users seeking the most extensive feature set. This mode enables most of Pylance's features, offering the richest IntelliSense experience. Ideal for those who want access to the full range of available functionality.
    - Individual settings can be configured to override the defaults set by `languageServerMode`.
    - Default settings based on mode are:
      
        | Mode                           | light      | default    | full       |
        | :----------------------------- | :--------- | :--------- | :--------- |
        | python.analysis.exclude                   | ["**"]      | []         | []         |
        | python.analysis.useLibraryCodeForTypes    | false       | true       | true       |
        | python.analysis.enablePytestSupport       | false       | true       | true       |
        | python.analysis.indexing                  | false       | true       | true       |
        | python.analysis.autoImportCompletions     | false       | false      | true       |
        | python.analysis.showOnlyDirectDependenciesInAutoImport | false | false | true     |
        | python.analysis.packageIndexDepths        | See | settings | below |
        | python.analysis.regenerateStdLibIndices   | false       | false      | true       |
        | python.analysis.userFileIndexingLimit     | 2000        | 2000       | -1         |
        | python.analysis.includeAliasesFromUserFiles | false     | false      | true       |
        | python.analysis.functionReturnTypes       | false       | false      | true       |
        | python.analysis.pytestParameters          | false       | false      | true       |
        | python.analysis.supportRestructuredText   | false       | true      | true       |
        | python.analysis.supportDocstringTemplate  | false       | false      | true       |
        | python.analysis.nodeExecutable            | ""          | ""         | "auto"     |

- `python.analysis.typeCheckingMode`
    - Used to specify the level of type checking analysis performed.
    - Default: `off`. 
        > Note that the value of this setting can be overridden by having a pyrightconfig.json or a pyproject.toml. For more information see this [link](https://aka.ms/AArua4c).
    - Available values:
        - `off`: No type checking analysis is conducted; unresolved imports/variables diagnostics are produced.
        - `basic`: All rules from `off` + `basic` type checking rules.
        - `standard`: All rules from `basic` + `standard` type checking rules.
        - `strict`: All rules from `standard` + `strict` type checking rules.
        > You can refer to [pyright](https://microsoft.github.io/pyright/#/configuration?id=diagnostic-settings-defaults) documentation to reference the default type checking rules for each of the type checking modes. 
    - Performance Consideration:
        - Setting `python.analysis.typeCheckingMode` to `off` can improve performance by disabling type checking analysis, which can be resource-intensive, especially in large codebases.

- `python.analysis.diagnosticMode`
    - Used to allow a user to specify what files they want the language server to analyze to get problems flagged in their code.
    - Available values:
        - `workspace`
        - `openFilesOnly` (default)
    - Performance Consideration:
        - Setting `python.analysis.diagnosticMode` to `openFilesOnly` limits analysis to open files, improving performance by reducing the amount of code Pylance needs to process in large workspaces.

- [`python.analysis.include`](docs/settings/python_analysis_include.md)
    - Paths of directories or files that should be included. If no paths are specified, Pylance defaults to the directory that contains workspace root. Paths may contain wildcard characters `**` (a directory or multiple levels of directories), `*` (a sequence of zero or more characters), or `?` (a single character).
    - Default value: empty array

- [`python.analysis.exclude`](docs/settings/python_analysis_exclude.md)
    - Paths of directories or files that should not be included. These override the include directories, allowing specific subdirectories to be excluded. Note that files in the exclude paths may still be included in the analysis if they are referenced (imported) by source files that are not excluded. Paths may contain wildcard characters `**` (a directory or multiple levels of directories), `*` (a sequence of zero or more characters), or `?` (a single character). If no exclude paths are specified, Pylance automatically excludes the following: `**/node_modules`, `**/__pycache__`, `.git` and any virtual environment directories.
    - Default value: empty array (or `["**"]` in `light` mode)
    - Performance Consideration:
        - Excluding unnecessary files or directories can significantly improve performance by reducing the scope of analysis. For example, setting `python.analysis.exclude` to `["**"]` will exclude all files except those currently open, minimizing resource consumption.

- `python.analysis.useNearestConfiguration` (**Experimental**)
    - When enabled, Pylance will search for and use `pyrightconfig.json` or `pyproject.toml` files in subdirectories, creating virtual workspaces for each configuration. This allows different type-checking settings for different parts of your codebase.
    - Default value: `false`
    - Available values:
        - `true`
        - `false` (default)
    - Note:
        - This feature is experimental and may have performance implications in large workspaces.
        - Virtual workspaces respect `python.analysis.exclude` patterns.
        - Only `pyproject.toml` files containing `[tool.pyright]` sections are discovered.
        - **Important**: Files in different virtual workspaces are isolated from each other. If you need files in one workspace to import from another workspace, you must configure `extraPaths` in your `pyrightconfig.json` or `pyproject.toml` to reference the other workspace directories. For example:
          ```json
          {
            "extraPaths": ["../other-workspace"]
          }
          ```

- [`python.analysis.ignore`](docs/settings/python_analysis_ignore.md)
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

- [`python.analysis.extraPaths`](docs/settings/python_analysis_extraPaths.md)
    - Used to specify extra search paths for import resolution. This replaces the old `python.autoComplete.extraPaths` setting.
    - Default value: empty array

- `python.analysis.includeExtraPathSymbolsInSymbolSearch`
    - Include symbols from `python.analysis.extraPaths` in Workspace Symbol search.
    - Default value: `false`
    - Performance Consideration:
        - Enabling this setting may slow down Workspace Symbol search.
    - Note:
        - For non-`py.typed` libraries, only symbols exported via a package `__init__.py` `__all__` are included.

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

- [`python.analysis.useLibraryCodeForTypes`](docs/settings/python_analysis_useLibraryCodeForTypes.md)
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

- [`python.analysis.userFileIndexingLimit`](docs/settings/python_analysis_userFileIndexingLimit.md)
    - Maximum number of user files to index in the workspace. Indexing files is a performance-intensive task. Please use this setting to limit the number of files you want us to index. If you enter -1, we will index all files.
    - Default value: 2000 (or -1 for `full` mode)
    - Performance Consideration:
        - Increasing this number will cause Pylance to allocate more resources for user file indexing.

- [`python.analysis.packageIndexDepths`](docs/settings/python_analysis_packageIndexDepths.md)
    - Used to override how many levels under installed packages to index on a per package basis. By default, only top-level modules are indexed (depth = 1). To index submodules, increase depth by 1 for each level of submodule you want to index.
    - If `depth` is set to `0`, the entry is treated as an *exclude prefix* and is removed from the index. Exclusions are module-boundary aware: `pydantic.v1` excludes `pydantic.v1` and `pydantic.v1.*`, but does not exclude `pydantic.v10`.
    - Default value:
        ```jsonc
        [
            { "name": "sklearn", "depth": 2 }, 
            { "name": "matplotlib", "depth": 2 }, 
            { "name": "scipy", "depth": 2 }, 
            { "name": "django", "depth": 2 }, 
            { "name": "flask", "depth": 2 }, 
            { "name": "fastapi", "depth": 2 }
        ]
        ```
        or in `full` mode
        ```jsonc
        [
            { "name": "", "depth": 4,  "includeAllSymbols": true }
        ]
        ```
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
    - Exclusion example:
        ```jsonc
        [
            { "name": "ctypes", "depth": 0 },
            { "name": "pydantic.v1", "depth": 0 }
        ]
        ```
    - Performance Consideration:
        - Adjusting this setting will cause Pylance to allocate more resources for indexing third-party libraries.

- [`python.analysis.persistAllIndices`](docs/settings/python_analysis_persistAllIndices.md)
    - Used to specify whether indices for all third-party libraries should be persisted to disk.
    - Default value: `true`
    - Performance Consideration:
        - Enabling this setting can improve startup performance by reducing the need to re-index third-party libraries.

- [`python.analysis.regenerateStdLibIndices`](docs/settings/python_analysis_regenerateStdLibIndices.md)
    - Instead of relying on the shared `stdlib.json` indices for all Python versions, generate unique indices tailored to each workspace's specific Python version and platform. This regeneration process will affect performance, unlike using the prebuilt stdlib indices.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Enabling this can impact performance by creating its own indices for standard libraries.

- [`python.analysis.includeAliasesFromUserFiles`](docs/settings/python_analysis_includeAliasesFromUserFiles.md)
    - Include alias symbols from user files. This will make alias symbols appear in features such as `add import` and `auto import`.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Enabling this can impact performance by increasing the number of completion items and indexing multiple files as changes occur.

- [`python.analysis.autoImportCompletions`](docs/settings/python_analysis_autoImportCompletions.md)
    - Used to control the offering of auto-imports in completions. This will impact number of items shown in the completion and performance.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true`
        - `false` (default)
    - Performance Consideration:
        - Enabling `python.analysis.autoImportCompletions` can impact performance by increasing the number of completion items and resource usage. Disabling it can improve performance by reducing the computational overhead during code completion.

- `python.analysis.showOnlyDirectDependenciesInAutoImport`
    - Show only direct dependencies declared in `requirements.txt` or `pyproject.toml` in `auto import` suggestions, if they exist. This only affects `auto import` for completions. The `add import` code action will continue to show all possible imports.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true`
        - `false` (default)

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
    - Default value: `false` (or `true` in `full` mode)
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
    - Default value: `false` (or `true` in `full` mode)
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
    - The set of commands to run when doing a fix all.
    - Accepted values:
        - `source.unusedImports`
        - `source.convertImportFormat`
        - `source.convertImportStar`
        - `source.addTypeAnnotation`

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
    - Path to a node executable to use to run Pylance. If this value is empty, Pylance uses VS Code's node executable. If set to `auto`, it will automatically download a version from [nodejs](https://nodejs.org/dist/)
    - Set this value when you are having out of memory issues. Using a custom node executable allows Pylance to allocate more memory.
    - Accepted values:
        - `any executable path` or `auto`

-   `python.analysis.nodeArguments`
    -   Extra arguments to pass to node when using `python.analysis.nodeExecutable`. Defaults to `--max-old-space-size=8192`
    -   Accepted values:
        -   `Any argument that node accepts`

- `python.analysis.autoIndent`
    - Automatically adjust indentation based on language semantics when typing Python code.
    - Accepted values:
        - `true` (default)
        - `false` 

- `python.analysis.autoSplitStrings`
    - Automatically add quote and line continuation characters when splitting strings.
    - Accepted values:
        - `true` (default)
        - `false` 

- `python.analysis.autoTranslateDocstrings`
    - Automatically translate Python docstrings in hover tooltips to the user's preferred language using GitHub Copilot.
    - When enabled, docstrings will be translated to the language specified by the GitHub Copilot locale setting (`github.copilot.chat.localeOverride`). If set to `auto`, Pylance will use the VS Code display language. Translations preserve Python code blocks, keywords, and markdown formatting.
    - Default value: `false`
    - Accepted values:
        - `true`
        - `false` (default)
    - Note: Requires GitHub Copilot to be installed and active.
    - Performance Consideration:
        - Enabling `python.analysis.autoTranslateDocstrings` may make hover tooltips display significantly slower due to the time required to call GitHub Copilot for AI-powered translation before showing the hover content.

- `python.analysis.supportRestructuredText`
    - Enable/disable support for reStructuredText in docstrings.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true` (default)
        - `false` 
    - Performance Consideration:
        - Disabling support for reStructuredText in docstrings by setting `python.analysis.supportRestructuredText` to `false` can improve performance by reducing the overhead of parsing complex docstrings.

- `python.analysis.aiCodeActions`
    - Enable/disable AI-assisted code actions. Requires the Copilot Chat extension to be enabled.
    - This setting accepts objects where the keys are the available AI-assisted code actions, and the values are `true` or `false` to enable or disable each action.
    - Available code actions to use as keys:
        - `convertFormatString`
        - `convertLambdaToNamedFunction`
        - `generateDocstring`
        - `generateSymbol`
        - `implementAbstractClasses`
    - Example:
    ```json
    {
        "python.analysis.aiCodeActions": {
            "implementAbstractClasses": true,
            "generateSymbol": true,
            "generateDocstring": true
        }
    }
    ```

- `python.analysis.supportDocstringTemplate`
    - Enable/disable support for reStructuredText docstring generation.
    - Default value: `false` (or `true` in `full` mode)
    - Accepted values:
        - `true`
        - `false` (default)
    - Example:
        ```python
        def foo(arg):
            """|<Trigger completion or code action here"""
        ```

- `python.analysis.displayEnglishDiagnostics`
    - Display diagnostics in English regardless of VS Code's display language.
    - Accepted values:
        - `true`
        - `false` (default)

- `python.analysis.generateWithTypeAnnotation`
    - Add type annotations when generating code. Defaults to `false` for type checking mode `off`, and `true` for other modes.
    - Accepted values:
        - `true`
        - `false` (default)

- `python.analysis.diagnosticsSource`
    - Allows specifing a different language server to use for diagnostics. Pylance will merge its results with this other server. The merge algorithm depends upon which server is chosen.
    - Accepted values:
        - `Pylance` (default)
        - `Pyright` - Allows running a different version of Pyright to generate diagnostics. Pyright diagnostics will completely replace the diagnostics for Pylance. See the `python.analysis.pyrightVersion` setting.

- `python.analysis.pyrightVersion`
    - Specifies the version of Pyright to use for diagnostics. This setting is only used when `python.analysis.diagnosticsSource` is set to `Pyright`. Minimum version required is 1.1.397 or higher.
    - Accepted values:
        - version string, i.e. `1.1.397`
        - path to a pyright-langserver.js file. For example, the Pyright installed by the PyPI Pyright module. In that case the path would be something like `~/.cache/pyright-python/1.1.397/node_modules/pyright/dist/pyright-langserver.js`

- `python.analysis.enableColorPicker`
    - Enable/disable color picker in the editor for '#RRGGBB' and '#RRGGBBAA' strings.
    - Accepted values:
        - `true` (default)
        - `false`

- `python.analysis.enableTroubleshootMissingImports`
    - Enable/disable the Quick Fix for troubleshooting missing imports. This Quick Fix requires the Python Environments extension to be installed and enabled.
    - Accepted values:
        - `true`
        - `false` (default)

Semantic highlighting
=====================

Visual Studio Code uses TextMate grammars as the main tokenization engine. TextMate grammars work on a single file as input and break it up based on lexical rules expressed in regular expressions.

Semantic tokenization allows language servers to provide additional token information based on the language server's knowledge on how to resolve symbols in the context of a project. Themes can opt-in to use semantic tokens to improve and refine the syntax highlighting from grammars. The editor applies the highlighting from semantic tokens on top of the highlighting from grammars.

Here's an example of what semantic highlighting can add:

Without semantic highlighting:

![ semantic highlighting disabled ](semantic-disabled.png)

With semantic highlighting:

![ semantic highlighting enabled ](semantic-enabled.png)

Semantic colors can be customized in settings.json by associating the Pylance semantic token types and modifiers with the desired colors.

- Semantic token types
    - class, enum
    - parameter, variable, property, enumMember
    - function, member
    - module
    - intrinsic
    - magicFunction (dunder methods)
    - selfParameter, clsParameter

- Semantic token modifiers
    - declaration
    - readonly, static, abstract
    - async
    - typeHint, typeHintComment
    - decorator
    - builtin
    - documentation
    - overridden
    - callable

The [scope inspector](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide#scope-inspector) tool allows you to explore what semantic tokens are present in a source file and what theme rules they match to. 

Example of customizing semantic colors in settings.json:

```jsonc
{
    "editor.semanticTokenColorCustomizations": {
        "[One Dark Pro]": { // Apply to this theme only
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

Code Actions
============

Pylance provides a set of code actions that are available through the lightbulb menu (or `Ctrl+.` / `Cmd+.`).
The exact titles can vary depending on context (e.g. the unresolved symbol name), but the actions below are what
Pylance can offer.

Quick Fixes
-----------
- Remove unused import
- Remove all unused imports
- Add import: `...` (adds a missing import for an unresolved symbol)
- Search for additional imports
- Change spelling to `...` (may also add an import when the best match is an auto-import)
- Add `# type: ignore` / `# pyright: ignore[...]` for a diagnostic
- Add `...` to `python.analysis.extraPaths` (for unresolved imports)
- Troubleshoot missing imports (third-party imports; requires Python Environments extension)
- Select Interpreter / Select Kernel (for unresolved imports)
- Learn more about import resolution
- Fix formatted string (for specific diagnostics that provide a fix)

Refactorings
------------
- Extract Variable
- Extract Method
- Move symbols to file...
- Move symbols to new file...
- Convert to explicit imports (for `from module import *`)
- Convert to module import (for `from x import y`)
- Convert import to relative path / absolute path (and Convert all... variants)
- Add type annotation (at cursor)
- Rename module (shadows stdlib module)
- Implement all abstract classes
- Add pytest fixture type annotation (and Add all... variants)

AI-assisted code actions (require Copilot)
----------------------------------------
- Generate docstring (for empty docstrings)
- Generate docstring (with Copilot)
- Generate function `...` / Generate class `...`
- Generate member `...`
- Convert to f-string / Convert to format()
- Convert lambda to named function
- Implement all abstract classes (with Copilot)

Source (whole-file) code actions
--------------------------------
- `source.unusedImports`
    - Remove all unused imports in a file

- `source.convertImportFormat`
    - Convert import format according to `python.analysis.importFormat`.

- `source.convertImportStar`
    - Convert all wildcard imports (`from module import *`) to explicit imports listing all imported symbols.

- `source.convertImportToModule`
    - Convert `from x import y` style imports into module imports.

- `source.addTypeAnnotation`
    - Add type annotations throughout the file where they can be inferred.

- `source.renameShadowedStdlibImports`
    - Rename imported user modules that shadow stdlib module names.

- `source.fixAll.pylance`
    - Apply the commands listed in the `python.analysis.fixAll` setting

Troubleshooting
===============
Known issues are documented in [TROUBLESHOOTING](TROUBLESHOOTING.md).

Contributing
===============
Pylance leverages Microsoft's open-source static type checking tool, Pyright, to provide performant language support for Python. 

Code contributions are welcomed via the [Pyright](https://github.com/microsoft/pyright) repo.

Pylance ships with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking. Our type stubs are sourced from [typeshed](https://github.com/python/typeshed) and our work-in-progress stub repository, [microsoft/python-type-stubs](https://github.com/microsoft/python-type-stubs). Type stubs in microsoft/python-type-stubs will be contributed back to typeshed or added inline to source packages once they are of high enough quality.

For information on getting started, refer to the [CONTRIBUTING instructions](https://github.com/microsoft/pyright/blob/main/CONTRIBUTING.md).


Feedback
===============
* File a bug in [GitHub Issues](https://github.com/microsoft/pylance-release/issues/new/choose)
* [Tweet us](https://twitter.com/pythonvscode/) with other feedback

# License

See [Pylance's license](https://marketplace.visualstudio.com/items/ms-python.vscode-pylance/license) and [the pylance-release repository's license](LICENSE) for more information.
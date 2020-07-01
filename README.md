Pylance
=====================
### Fast, feature-rich language support for Python

This repository is for providing feedback and documentation on the Pylance language server extension in Visual Studio Code. You can use the repository to report issues or submit feature requests. Pylance is not open source, but you can contribute by filing issues or by making contributions to the open-source [Pyright](www.github.com/microsoft/pyright) type checking engine that powers Pylance.

Quick Start
============
1. Install the [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) from the marketplace.
1. Open a Python (.py) file and the Pylance extension will activate.

Features
=========
![ screencast ](screencap.gif)

* Docstrings
* Signature help, with type information
* Parameter suggestions
* Code completion
* Auto-imports (as well as add and remove import code actions)
* As-you-type reporting of code errors and warnings (diagnostics)
* Code outline
* Code navigation
* Code lens (references/implementations)
* Type checking mode
* Native multi-root workspace support
* IntelliCode compatibility
* Jupyter Notebooks compatibility

See the [changelog](CHANGELOG.md) for the latest release.

Settings and Customization
===============
Pylance provides users with the ability to customize their Python language support via a host of settings which can either be placed in the settings.json file in your workspace, or edited through the Settings Editor UI. 

- `python.analysis.typeCheckingMode`
    - Used to specify the level of type checking analysis performed;
    - Default: `off`
    - Available values:
        - `off`: No type checking analysis is conducted; unresolved imports/variables diagnostics are produced
        - `basic`: Non-type checking-related rules (all rules in `off`) + basic type checking rules
        - `strict`:	All type checking rules at the highest severity of error (includes all rules in `off` and `basic` categories)

- `python.analysis.diagnosticMode`
    - Used to allow a user to specify what files they want the language server to analyze to get problems flagged in their code.
    - Available values:
        - `workspace`
        - `openFilesOnly` (default)

- `python.analysis.stubPaths`
    - Used to allow a user to specify a path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory.
    - Default value: `./typings`

- `python.analysis.autoSearchPaths`
    - Used to automatically add search paths based on some predefined names (like `src`).
    - Available values:
        - `true` (default)
        - `false`

- `python.analysis.diagnosticSeverityOverrides`
    - Used to allow a user to override the severity levels for individual diagnostics should they desire
    - Accepted severity values:
        - `error` (red squiggle)
        - `warning` (yellow squiggle)
        - `information` (blue squiggle)
        - `none` (disables the rule)

    - Available rule to use as keys can be found [here](DIAGNOSTIC_SEVERITY_RULES.md)
    - Example:
    ```
    { 
        "python.analysis.diagnosticSeverityOverrides:" { 
            "reportUnboundVariable" : "information", 
            "reportImplicitStringConcatenation" : "warning" 
        } 
    } 
    ```

- `python.analysis.useLibraryCodeForTypes`
    - Used to parse the source code for a package when a typestub is not found
    - Accepted values:
        - `true` (default)
        - `false`


Contributing
===============
Pylance leverages Microsoft's open-source static type checking tool, Pyright, to provide performant language support for Python. 

Code contributions are welcomed via the [Pyright](https://github.com/microsoft/pyright) repo.

For information on getting started, refer to the [CONTRIBUTING instructions](https://github.com/microsoft/pyright/blob/master/CONTRIBUTING.md).


Feedback
===============
* File a bug in [GitHub Issues](https://github.com/microsoft/pylance-release/issues/new/choose)
* [Tweet us](https://twitter.com/pythonvscode/) with other feedback


License
===============
See [LICENSE](LICENSE) for more information.
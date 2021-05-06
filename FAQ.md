# Pylance Frequently Asked Questions

### What is the relationship between Pylance, Pyright and the Python extension?
Pylance is a language server, which provides features like IntelliSense, logical linting (e.g., errors and warnings), code actions, code navigation, semantic colorization, etc. Pyright is the open-source type checker which Pylance uses under the hood to provide its functionality. Pylance provides a superset of Pyright’s functionality. To use Pylance, you must have the core Python extension installed in Visual Studio Code as it builds upon that experience.

### What features are in Pylance but not in Pyright? What is the difference exactly?
Pylance has a handful of valuable features that are not available in Pyright, including semantic highlighting, refactoring code actions (extract variable/extract method), docstrings for built-in/standard library modules, and IntelliCode compatibility. Pylance  also ships with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking.

### Are there any plans to open-source Pylance in the future?
Because we have plans to include Pylance in Microsoft products outside of VS Code that do not have the same license, business models and/or are closed-source (for example, fully managed products and services), we do not currently have plans to open-source Pylance. 

However, a substantial portion of Pylance’s source code is open source via the [Pyright type checker](https://github.com/microsoft/pyright). We welcome contributions via that repository, and feedback on Pylance via our [pylance-release repo](https://github.com/microsoft/pylance-release).

### Can I load Pylance in Code – OSS?
Pylance is licensed for use in Microsoft products and services only, so can only be used on official Microsoft builds of Visual Studio Code and GitHub Codespaces.

### What telemetry and user data do you collect? Can I opt out?
You can read about how we use collect and use telemetry [here](https://code.visualstudio.com/docs/getstarted/telemetry). You can read about how we use collect and use telemetry, including how to disable it [here](https://code.visualstudio.com/docs/getstarted/telemetry).

## Overview

`reportPrivateUsage` flags cases where private variables or functions (those prefixed with an underscore) are accessed from outside their defining module or class. This diagnostic helps enforce encapsulation and prevent accidental use of private implementation details.

## Representative Issues

-   [#3102](https://github.com/microsoft/pylance-release/issues/3102): Ensure that default argument types in functions match the annotated parameter types.
-   [#3853](https://github.com/microsoft/pylance-release/issues/3853): Configure Pylance's packageIndexDepths and ensure the correct Python environment for accurate auto-imports.
-   [#3855](https://github.com/microsoft/pylance-release/issues/3855): Enable Python indexing in VSCode settings for auto-imports.
-   [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings.
-   [#495](https://github.com/microsoft/pylance-release/issues/495): Use the `exclude` property in Pyright's config to prevent analysis of unwanted folders.
-   [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities by type checking mode.
-   [#5755](https://github.com/microsoft/pylance-release/issues/5755): Avoid accessing functions with a leading underscore from other modules.
-   [#6300](https://github.com/microsoft/pylance-release/issues/6300): Exclude unnecessary folders like .venv to improve performance.
-   [#7001](https://github.com/microsoft/pylance-release/issues/7001): Prefer 'openFilesOnly' diagnostic mode for large projects.
-   [#1443](https://github.com/microsoft/pyright/issues/1443): Use comments to indicate strict type checking for new files and configure directories in pyrightconfig.json.
-   [#1462](https://github.com/microsoft/pyright/issues/1462): Always verify that configuration settings are respected by CLI tools.
-   [#2277](https://github.com/microsoft/pyright/issues/2277): Use alias imports to indicate public interface symbols in `py.typed` libraries.

## Common Fixes & Workarounds

1. Avoid accessing private variables or functions from outside their defining module or class.
2. Use alias imports to clarify public API symbols.
3. Configure your project to exclude unnecessary folders from analysis.
4. Use strict type checking and configure directories as needed in your config files.
5. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportPrivateUsage) for details on configuring or disabling this diagnostic.
